# Chương 12: AI Chó Canh Nông Trại (Anti-Thief)

Đặc sản của Avatar 2D là tính năng "Ăn trộm". Để bảo vệ thành quả của mình, chủ nông trại sẽ mua Chó. 
Đây là một AI hoàn toàn khác biệt so với Gà và Bò. AI của Chó là sự kết hợp giữa **Tuần tra (Patrol)** và **Rượt đuổi mục tiêu (Chasing)**.

## 1. Thành phần của Chó (GuardDog Component)

```odin
package ecs

DogState :: enum { PATROL, ALERT, CHASE, BITE }

GuardDogComponent :: struct {
    state: DogState,
    target_thief_id: EntityID, // ID của kẻ trộm đang bị rượt
    alert_timer: f32,          // Thời gian đứng khựng lại gầm gừ trước khi rượt
    bite_cooldown: f32,
    detection_radius: int,     // Tầm nhìn (Ví dụ: 5 ô)
}
```

## 2. Hệ Thống Cảm Biến Kẻ Gian (Sensor System)

Mỗi khung hình, chú Chó sẽ dùng tầm nhìn (Radar) quét xung quanh. Nếu phát hiện một `Player` lạ (không phải chủ nhà), nó sẽ chuyển sang trạng thái cảnh giác (`ALERT`).

```odin
update_dog_sensor :: proc(world: ^World, dog_id: EntityID, dog_pos: ^Position, dog_comp: ^GuardDogComponent) {
    if dog_comp.state != .PATROL do return // Đang rượt thì không cần quét nữa
    
    // Quét tìm tất cả người chơi trong bản đồ
    for i := 0; i < int(world.next_entity_id); i += 1 {
        if world.mask_player[i] {
            player := &world.players[i]
            p_pos := &world.positions[i]
            
            // Bỏ qua chủ nhà
            if player.is_owner do continue
            
            // Tính khoảng cách (Manhattan distance)
            dist_x := abs(dog_pos.grid_x - p_pos.grid_x)
            dist_y := abs(dog_pos.grid_y - p_pos.grid_y)
            
            if dist_x + dist_y <= dog_comp.detection_radius {
                // Phát hiện kẻ gian!
                dog_comp.state = .ALERT
                dog_comp.alert_timer = 1.0 // Sủa gâu gâu 1 giây đe dọa
                dog_comp.target_thief_id = EntityID(i)
                play_sound("dog_bark.wav")
                return
            }
        }
    }
}
```

## 3. Logic Rượt Đuổi và Cắn

Sau khi sủa đe dọa 1 giây, Chó sẽ bắt đầu rượt.

```odin
update_dog_ai :: proc(world: ^World, dt: f32) {
    // ... Lặp qua các Entity Chó ...
    
    switch dog.state {
        case .PATROL:
            // Chạy AI lang thang giống Bò Gà (Chương 9)
            update_dog_sensor(world, dog_id, pos, dog)
            
        case .ALERT:
            dog.alert_timer -= dt
            if dog.alert_timer <= 0 {
                dog.state = .CHASE
            }
            
        case .CHASE:
            thief_pos := &world.positions[dog.target_thief_id]
            
            // Kiểm tra khoảng cách
            dist_x := abs(pos.grid_x - thief_pos.grid_x)
            dist_y := abs(pos.grid_y - thief_pos.grid_y)
            
            if dist_x + dist_y > 10 { // Trộm chạy xa quá thì tha
                dog.state = .PATROL
            } else if dist_x <= 1 && dist_y <= 1 {
                // Đủ gần để cắn
                dog.state = .BITE
                dog.bite_cooldown = 0.5
            } else {
                // Dùng Pathfinding đuổi theo
                next_x, next_y := calculate_next_step_towards(pos.grid_x, pos.grid_y, thief_pos.grid_x, thief_pos.grid_y)
                mov.target_grid_x = next_x
                mov.target_grid_y = next_y
                mov.is_moving = true
            }
            
        case .BITE:
            // Cắn kẻ trộm
            dog.bite_cooldown -= dt
            if dog.bite_cooldown <= 0 {
                // 1. Gửi sự kiện Cắn lên Server (hoặc trừ máu trực tiếp nếu là Offline)
                damage_player(world, dog.target_thief_id, 20) // Trừ 20 máu
                
                // 2. Rớt một ít tiền của kẻ trộm ra đất
                drop_money_from_player(world, dog.target_thief_id, 100)
                
                // 3. Trộm bị hiệu ứng Stun (Khựng lại 1 giây)
                stun_player(world, dog.target_thief_id, 1.0)
                
                play_sound("dog_bite.wav")
                
                // Cắn xong tiếp tục đánh giá xem nên rượt tiếp không
                dog.state = .CHASE 
            }
    }
}
```

**Mẹo tối ưu Pathfinding:**
Đừng chạy thuật toán A* phức tạp cho chó mỗi khung hình. Chó chỉ cần tính toán hướng đi (trái phải trên dưới) làm sao để rút ngắn khoảng cách với kẻ trộm là đủ. Kẻ trộm thì luôn loay hoay trong nông trại ít vật cản, nên A* là quá dư thừa và ngốn CPU Server vô ích.
