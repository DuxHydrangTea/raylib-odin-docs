# Chương 6: Vòng Đời Cây Trồng Thời Gian Thực

Cơ chế "Nghiện" nhất của Avatar 2D chính là việc chờ đợi Cây Lớn Lên. Mỗi loại cây (Lúa, Cà chua, Dưa hấu) có một biểu đồ thời gian sống và số lượng Phase (Giai đoạn) hình ảnh khác nhau.

## 1. Data-Driven Design cho Cây Trồng

**Anti-pattern:** 
```odin
if plant.type == "Tomato" do plant.harvest_time = 3600
if plant.type == "Watermelon" do plant.harvest_time = 7200
```
Tuyệt đối không hardcode (viết cứng) thông số cây vào Logic Code. Phải tách nó ra thành Dữ Liệu (Ví dụ: `config.json`). Trong Odin, chúng ta sẽ tải cấu hình này vào một Map toàn cục (Registry).

```odin
// Dữ liệu định nghĩa Cây
PlantConfig :: struct {
    id: int,
    name: string,
    growth_duration: f64,  // Tổng thời gian lớn (Giây)
    phases: int,           // Có bao nhiêu hình ảnh lớn lên (Ví dụ: 4 pha: Hạt -> Mầm -> Cây non -> Quả)
    sell_price: int,
    sprite_row: int,       // Hàng đồ họa trong Tileset Cây trồng
}

// Registry tra cứu
g_plant_configs: map[int]PlantConfig
```

## 2. Component Cây trồng (CropComponent)

Khi một hạt giống được gieo xuống `FarmPlot`, một Entity mới (Mang Component Cây) sẽ được sinh ra, neo (anchor) vào tọa độ của Ô đất.

```odin
package ecs

CropComponent :: struct {
    config_id: int,       // ID hạt giống (Tra cứu config)
    planted_at: f64,      // Timestamp thời điểm gieo
    plot_entity: EntityID, // Link ngược lại về ô đất
    
    // Trạng thái cache để render
    current_phase: int,   // 0 (Hạt), 1 (Mầm), ... phases-1 (Chín)
    is_dead: bool,        // Nếu héo chết
}
```

## 3. Thuật toán Tính Pha Phát Triển (Growth System)

Để tính xem cây đang ở hình hài (Phase) nào, ta KHÔNG dùng `while` đếm lùi từng mili-giây. Ta làm một phép chia toán học đơn giản dựa trên thời gian thực.

```odin
update_crop_growth :: proc(world: ^World) {
    current_time := get_current_time()
    
    for i := 0; i < int(world.next_entity_id); i += 1 {
        if world.mask_crop[i] {
            crop := &world.crops[i]
            if crop.is_dead do continue
            
            cfg := g_plant_configs[crop.config_id]
            
            // Thời gian đã sống
            age := current_time - crop.planted_at
            
            // Thời gian của mỗi Pha
            time_per_phase := cfg.growth_duration / f64(cfg.phases)
            
            // Tính toán Phase hiện tại
            phase := int(age / time_per_phase)
            
            // Kịch trần ở mức chín (Max Phase)
            if phase >= cfg.phases {
                phase = cfg.phases - 1
            }
            
            crop.current_phase = phase
        }
    }
}
```

## 4. Tương Tác Thu Hoạch (Harvesting)

Trở lại hàng đợi sự kiện (Interaction Event) ở Chương 5. Khi người chơi nhấn phím (dùng Tay không `tool == HAND`) lên một ô đất đang có Cây chín.

```odin
// Xử lý sự kiện (Bên trong event_queue)
if tool == .HAND {
    if plot.has_plant {
        crop := &world.crops[plot.plant_entity]
        cfg := g_plant_configs[crop.config_id]
        
        // Kiểm tra cây đã chín chưa? (Phase cuối cùng)
        if crop.current_phase == (cfg.phases - 1) && !crop.is_dead {
            // 1. Chuyển Nông sản vào Túi đồ người chơi (Inventory)
            add_item_to_inventory(event.entity_id, crop.config_id, 1)
            
            // 2. Tiêu hủy Entity Cây
            destroy_entity(world, plot.plant_entity)
            
            // 3. Reset lại trạng thái Ô đất (Trả về đất tơi xốp)
            plot.has_plant = false
            plot.state = .PLOWED
            
            play_sound("harvest_money.wav")
        }
    }
}
```

Cấu trúc này mô phỏng chuẩn xác 100% thời gian thực. Khi Server tắt nguồn 3 tiếng, lúc bật lên, đoạn code `age := current_time - crop.planted_at` sẽ nhảy vọt lên 3 tiếng và tự động đặt `current_phase` thành chín, người chơi vào game sẽ thấy cây đã mọc xong ngay lập tức!
