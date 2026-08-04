# Chương 10: Quy Trình Cho Ăn & Thu Hoạch (Sinh Sản)

Động vật khác cái cây ở chỗ nó không "lớn lên" rồi biến mất (Trừ khi bán thịt). Nó là công cụ sinh sản tuần hoàn: Ăn thức ăn -> Đợi thời gian -> Đẻ trứng/Vắt sữa -> Lại ăn tiếp.

## 1. Máng Ăn (Trough / Feeder)

Thay vì cho từng con gà ăn thủ công, Avatar thiết kế một Máng ăn chung cho cả chuồng. Người chơi nhét Cỏ / Lúa vào Máng, động vật sẽ tự động tới ăn.
Máng ăn cũng là một Thực Thể (Entity).

```odin
package ecs

FeederComponent :: struct {
    food_amount: int, // Số lượng thức ăn đang có trong máng
    capacity: int,    // Chứa tối đa bao nhiêu
    food_type: int,   // ID Lúa (cho Gà) hoặc Cỏ (cho Bò)
}
```

## 2. Quy trình Tìm Thức Ăn (AI)

Trong Chương 9, ở hàm `choose_next_state`, chúng ta đã để ngỏ phần code nếu con vật đói (`hunger < 30`). Bây giờ ta sẽ điền logic tìm đường tới Máng ăn.

```odin
// Tìm máng ăn gần nhất có thức ăn
target_feeder_grid_x, target_feeder_grid_y := find_nearest_feeder_with_food(world, animal.type)

if target_feeder_grid_x != -1 {
    // 1. Dùng thuật toán tìm đường (A* hoặc đơn giản là đi theo Manhattan distance) 
    //    để bước từng bước về phía máng ăn.
    next_step_x, next_step_y := calculate_next_step_towards(pos.grid_x, pos.grid_y, target_feeder_grid_x, target_feeder_grid_y)
    
    // Nếu đứng sát máng ăn rồi
    if next_step_x == pos.grid_x && next_step_y == pos.grid_y {
        animal.state = .EAT
        animal.state_timer = 5.0 // Tốn 5 giây để nhai
        
        // Trừ thức ăn trong máng
        consume_food(world, target_feeder_grid_x, target_feeder_grid_y)
        
        // Phục hồi độ no
        animal.hunger = 100.0
        
        // Đánh dấu thời điểm bắt đầu tạo ra sản phẩm (Mang thai/Sản xuất sữa)
        animal.last_fed_time = get_current_time()
        animal.is_producing = true 
    } else {
        // Tiếp tục di chuyển tới máng ăn
        mov.target_grid_x = next_step_x
        mov.target_grid_y = next_step_y
        mov.is_moving = true
    }
}
```

## 3. Hệ thống Thu Hoạch (Sữa, Trứng)

Tương tự cây cối, thay vì đếm bằng Vòng lặp Real-time, ta dùng Timestamp để không ngốn CPU.
Mở rộng thêm vào `LivestockComponent`:

```odin
    is_producing: bool,
    last_fed_time: f64,
    has_product: bool, // Đã có trứng/sữa, chờ người tới nhặt
```

**Cập nhật vòng lặp vắt sữa:**
Mỗi chu kỳ (VD: 10 phút), Server sẽ kiểm tra.

```odin
update_livestock_production :: proc(world: ^World) {
    current_time := get_current_time()
    
    for i := 0; i < int(world.next_entity_id); i += 1 {
        if world.mask_livestock[i] {
            animal := &world.livestock[i]
            
            if animal.is_producing && !animal.has_product {
                // Giả sử Bò cần 3600 giây (1 tiếng) để có sữa
                production_time := get_production_time(animal.type) 
                
                if current_time - animal.last_fed_time >= production_time {
                    animal.has_product = true
                    animal.is_producing = false
                    
                    // Tạo một Entity "Sữa" rớt ra dưới chân con bò
                    spawn_item_drop(world, pos.grid_x, pos.grid_y, ITEM_MILK)
                }
            }
        }
    }
}
```

Khi Bò đẻ ra bình sữa, Bình sữa nằm trên đất dưới dạng `ItemDrop`. Người chơi chạy ngang qua nhặt (hoặc click vào) sẽ kích hoạt sự kiện `InteractEvent` (Chương 4), đẩy Bình Sữa vào Túi đồ (`Inventory`) của họ và chuyển thành Xu/Tiền!
