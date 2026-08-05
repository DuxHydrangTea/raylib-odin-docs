# Chương 5: Vòng Đời Ô Đất (Farm Plot Lifecycle)

Trong game Nông trại, một mảnh đất không chỉ là cái hình nền (Texture). Nó là một "Thực thể" (Entity) chứa trạng thái sống động (Đã cày, Đã tưới, Khô cằn).

Quy trình chuẩn của Avatar 2D:
`ĐẤT TRỐNG (Cỏ) -> [Dùng Cuốc] -> ĐẤT TƠI XỐP -> [Dùng Bình Tưới] -> ĐẤT ĐÃ TƯỚI (Sẵn sàng gieo hạt)`.

## 1. Dữ liệu Ô Đất (Farm Plot Component)

Ta sẽ tạo một Component riêng biệt gán cho những Grid có thể trồng trọt.

```odin
package ecs

PlotState :: enum {
    EMPTY,       // Đất cỏ rêu phong (Chưa cày)
    PLOWED,      // Đất tơi xốp (Màu nâu sáng)
    WATERED,     // Đất ẩm ướt (Màu nâu sẫm, được phép gieo hạt)
}

FarmPlot :: struct {
    state: PlotState,
    water_dry_time: f64, // Thời gian (Unix) đất bị khô lại nếu không gieo hạt
    has_plant: bool,     // Có cây đang mọc trên này không
    plant_entity: EntityID, // Link tới Entity Cây trồng
}
```

Bản đồ có 100 luống đất, ta sẽ tạo 100 Entity mang component `FarmPlot` và `Position`. Tránh lưu trực tiếp trạng thái này vào mảng `Tilemap` 2D tĩnh vì nó quá nặng nề và kém linh hoạt.

## 2. Xử lý Tương tác (Xẻng & Bình tưới)

Dựa vào Hàng đợi sự kiện (`InteractEvent`) từ Chương 4, Hệ thống Nông nghiệp sẽ xử lý logic công cụ. Giả sử người chơi có một Component `Inventory` cho biết họ đang cầm vật phẩm gì trên tay.

```odin
package ecs

import "core:fmt"

ToolType :: enum { HOE, WATERING_CAN, SEED, HAND }

// Định nghĩa kiểu Hàm xử lý sự kiện (Function Pointer)
ActionHandler :: proc(world: ^World, event: InteractEvent)

// Bảng tra cứu (Router) định tuyến công cụ tới đúng hàm xử lý
tool_handlers: map[ToolType]ActionHandler

// Khởi tạo và đăng ký các hàm xử lý công cụ (Gọi 1 lần duy nhất ở đầu game)
init_tool_handlers :: proc() {
    tool_handlers[.HOE] = proc(world: ^World, event: InteractEvent) {
        plot_entity, found := find_plot_at(world, event.target_grid_x, event.target_grid_y)
        if !found do return
        plot := &world.farm_plots[plot_entity]
        
        if plot.state == .EMPTY {
            plot.state = .PLOWED
            play_sound("hoe_hit.wav")
        }
    }
    
    tool_handlers[.WATERING_CAN] = proc(world: ^World, event: InteractEvent) {
        plot_entity, found := find_plot_at(world, event.target_grid_x, event.target_grid_y)
        if !found do return
        plot := &world.farm_plots[plot_entity]
        
        if plot.state == .PLOWED {
            plot.state = .WATERED
            plot.water_dry_time = get_current_time() + 3600 // Đất sẽ khô lại sau 1 tiếng
            play_sound("water_splash.wav")
        }
    }
    
    tool_handlers[.SEED] = proc(world: ^World, event: InteractEvent) {
        plot_entity, found := find_plot_at(world, event.target_grid_x, event.target_grid_y)
        if !found do return
        plot := &world.farm_plots[plot_entity]
        
        if plot.state == .WATERED && !plot.has_plant {
            // Logic Gieo hạt sẽ nằm ở Chương 6
            plant_seed(world, plot_entity, get_equipped_seed_id())
        }
    }
}

// Hệ thống xử lý sự kiện chính (Vô cùng sạch sẽ, loại bỏ hoàn toàn mã mì Ý if-else!)
process_farming_events :: proc(world: ^World) {
    for event in event_queue {
        tool := get_equipped_tool(world, event.entity_id)
        
        // Giao phó sự kiện cho đúng Handler đã được đăng ký
        if handler, ok := tool_handlers[tool]; ok {
            handler(world, event)
        }
    }
    // Xóa event queue sau khi xử lý xong
    clear(&event_queue)
}
```

## 3. System Cập nhật Môi trường (Cơ chế Đất Khô)

Luống đất ẩm ướt không giữ nước mãi mãi. Nếu qua 1 khoảng thời gian mà không ai gieo hạt, đất sẽ trở lại trạng thái tơi xốp (Mất nước). Đây là lúc áp dụng `Timestamp` để không làm nghẽn CPU (giống bài toán MMO Farm ở giáo trình trước).

```odin
update_environment_system :: proc(world: ^World) {
    current_time := get_current_time() // Lấy thời gian thực
    
    for i := 0; i < int(world.next_entity_id); i += 1 {
        if world.mask_farm_plot[i] {
            plot := &world.farm_plots[i]
            
            // Nếu đất đang ẩm, không có cây, và đã quá hạn giờ khô
            if plot.state == .WATERED && !plot.has_plant {
                if current_time > plot.water_dry_time {
                    plot.state = .PLOWED // Đất bị khô lại
                }
            }
        }
    }
}
```

**Thành quả:** Bằng cấu trúc này, 1000 ô đất cũng chỉ tiêu tốn chưa tới 1 mili-giây CPU để kiểm tra và cập nhật trạng thái. Bạn đã sẵn sàng để Hạt giống nảy mầm!
