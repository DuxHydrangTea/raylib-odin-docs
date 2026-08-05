# Chương 8: Hệ Thống Vật Phẩm Nông Nghiệp & Phân Bón

Trong các game Nông Trại, ngoài việc chờ đợi thời gian, người chơi có thể bỏ tiền Xu (hoặc Đô la tiền nạp thẻ) để mua Phân bón ép cây chín lẹ.

## 1. Định nghĩa Vật phẩm Phân Bón (Fertilizer)

Phân bón không phải là Hạt giống, cũng không phải Nông sản. Nó là một loại Vật phẩm Tương tác (Consumable Tool). Cấu hình của nó sẽ chứa chỉ số **Giảm bao nhiêu % thời gian trồng**.

```odin
FertilizerConfig :: struct {
    id: int,
    name: string,
    time_reduction_percent: f64, // Ví dụ: 0.2 (Giảm 20%), 1.0 (Chín ngay lập tức)
    price: int,
}

// Registry
g_fertilizers: map[int]FertilizerConfig
```

## 2. Mở rộng Crop Component

Để ghi nhớ cây đã được bón phân, ta thêm một thuộc tính bù trừ thời gian (Time Boost).

```odin
package ecs

CropComponent :: struct {
    // ... (các biến cũ)
    
    // Phân bón
    is_fertilized: bool,
    boost_time: f64, // Tổng số giây được rút ngắn
}
```

## 3. Tương tác Bón Phân (Sử dụng Vật phẩm)

Khi người chơi cầm Bao phân bón trên tay và tương tác với một Ô đất đang có Cây.

```odin
// Đăng ký Handler Bón Phân vào init_tool_handlers()
tool_handlers[.FERTILIZER] = proc(world: ^World, event: InteractEvent) {
    plot_entity, found := find_plot_at(world, event.target_grid_x, event.target_grid_y)
    if !found do return
    plot := &world.farm_plots[plot_entity]

    if plot.has_plant {
        crop := &world.crops[plot.plant_entity]
        cfg := g_plant_configs[crop.config_id]
        
        // Chỉ cho phép bón 1 lần để tránh lạm dụng, và không bón cây đã chín
        if !crop.is_fertilized && crop.current_phase < (cfg.phases - 1) {
            
            fertilizer_cfg := g_fertilizers[get_equipped_fertilizer_id()]
            
            // Tính số giây được trừ đi
            reduced_seconds := cfg.growth_duration * fertilizer_cfg.time_reduction_percent
            
            crop.is_fertilized = true
            crop.boost_time = reduced_seconds
            
            // Trừ vật phẩm khỏi túi đồ người chơi
            remove_item_from_inventory(event.entity_id, fertilizer_cfg.id, 1)
            
            play_sound("fertilizer_sparkle.wav")
        }
    }
}
```

## 4. Tích hợp vào Phương trình Thời Gian Lớn của Cây (Master Equation)

Đến lúc này, công thức tính **Tuổi Thực (Effective Age)** của một cái cây tại Chương 6 và Chương 7 phải được gộp lại toàn diện.

```odin
// Công thức tính tuổi thực tuyệt đối của cây
effective_age := (current_time - crop.planted_at) - crop.total_sick_time - current_sick_penalty + crop.boost_time

// Dùng effective_age này so sánh với growth_duration để lấy Phase
```

### Tại sao lại CỘNG `boost_time`?
Tuổi của cây được tính bằng thời gian nó đã sống từ lúc gieo hạt (current_time - planted_at). 
Khi ta bón phân, ta muốn cây già đi nhanh hơn. Vì vậy, cộng thêm `boost_time` vào `effective_age` có nghĩa là ta đang "buff" cho cây già thêm N giây (giống như tua nhanh thời gian đi tới tương lai N giây).

Ngược lại, khi cây bị bệnh, thời gian bị bệnh `total_sick_time` được TRỪ ĐI, làm cây trẻ lại (nghĩa là nó lớn chậm hơn bình thường).

Bằng một phương trình đại số tuyến tính đơn giản này, bạn đã quản lý toàn bộ vòng đời sinh, lão, bệnh, tử của vạn vật trong nông trại mà không tốn một chút RAM dư thừa nào!
