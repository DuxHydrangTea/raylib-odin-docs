# Chương 9: AI Động Vật Cơ Bản (Bò, Lợn, Gà)

Trái ngược với Cây cối nằm bất động trên Grid, Vật nuôi trong nông trại là những Sinh vật (Entities) di chuyển tự do. Chúng cần một Trí thông minh nhân tạo (AI) cơ bản để lang thang quanh chuồng, dừng lại ăn uống, và đi ngủ.

Thay vì viết Logic AI cứng nhắc bằng các câu lệnh `if/else` dài dằng dặc, chúng ta sẽ áp dụng mẫu thiết kế **Máy Trạng Thái Hữu Hạn (Finite State Machine - FSM)**.

## 1. Khai báo Component cho Vật Nuôi

```odin
package ecs

LivestockType :: enum { CHICKEN, PIG, COW }
AnimalState :: enum { IDLE, WANDER, EAT, SLEEP }

LivestockComponent :: struct {
    type: LivestockType,
    state: AnimalState,
    
    // Bộ đếm thời gian cho State hiện tại
    state_timer: f32, 
    
    // Nơi con vật được nhốt (để nó không chạy ra ngoài lưới chuồng)
    pen_rect: rl.Rectangle, 
    
    // Các chỉ số sinh học
    hunger: f32,  // 0.0 (Đói lả) -> 100.0 (No)
}
```
Lưu ý: Vật nuôi CŨNG PHẢI có `Position` và `MovementComponent` giống như Nhân vật người chơi ở Chương 2. Điểm khác biệt duy nhất là Input của con vật được điều khiển bởi Máy tính, chứ không phải bàn phím.

## 2. Hệ Thống Máy Trạng Thái (AI System)

AI System sẽ chạy mỗi frame, suy nghĩ xem con vật nên làm gì tiếp theo dựa trên trạng thái hiện tại (`state`).

```odin
update_livestock_ai :: proc(world: ^World, dt: f32) {
    for i := 0; i < int(world.next_entity_id); i += 1 {
        if world.mask_livestock[i] && world.mask_movement[i] {
            animal := &world.livestock[i]
            mov := &world.movements[i]
            pos := &world.positions[i]
            
            // Giảm độ no theo thời gian
            animal.hunger -= 2.0 * dt
            if animal.hunger < 0 do animal.hunger = 0
            
            // Nếu con vật đang thực thi việc trượt sang ô khác (do MovementSystem quản lý)
            // thì không suy nghĩ hành động mới.
            if mov.is_moving do continue 
            
            // Giảm timer của trạng thái hiện tại
            animal.state_timer -= dt
            
            // CHUYỂN TRẠNG THÁI (STATE TRANSITION)
            if animal.state_timer <= 0 {
                choose_next_state(animal, mov, pos)
            }
        }
    }
}
```

## 3. Suy nghĩ và Ra Quyết định (Transition Logic)

Hàm `choose_next_state` chịu trách nhiệm gán lệnh cho con vật.

```odin
choose_next_state :: proc(animal: ^LivestockComponent, mov: ^MovementComponent, pos: ^Position) {
    import "core:math/rand"
    
    // Ưu tiên 1: Quá đói -> Đi tìm máng ăn (Sẽ học ở Chương 10)
    if animal.hunger < 30.0 {
        // animal.state = .EAT
        // return
    }
    
    // Xổ số ngẫu nhiên xem nên Đứng im hay Đi dạo
    chance := rand.float32()
    
    if chance < 0.4 {
        // 40% Đứng im (IDLE)
        animal.state = .IDLE
        animal.state_timer = rand.float32() * 3.0 + 2.0 // Đứng im từ 2 đến 5 giây
        
    } else {
        // 60% Lang thang (WANDER)
        animal.state = .WANDER
        animal.state_timer = 0 // Đi 1 ô xong sẽ suy nghĩ lại ngay
        
        // Random hướng đi
        dir := rand.int31() % 4
        dx, dy := 0, 0
        
        switch dir {
            case 0: dx = 1;  mov.facing = .RIGHT
            case 1: dx = -1; mov.facing = .LEFT
            case 2: dy = 1;  mov.facing = .DOWN
            case 3: dy = -1; mov.facing = .UP
        }
        
        target_x := pos.grid_x + dx
        target_y := pos.grid_y + dy
        
        // Kiểm tra xem ô đích có nằm trong Hàng rào chuồng (pen_rect) không
        if target_x >= int(animal.pen_rect.x) && target_x <= int(animal.pen_rect.x + animal.pen_rect.width) &&
           target_y >= int(animal.pen_rect.y) && target_y <= int(animal.pen_rect.y + animal.pen_rect.height) {
           
            // Giao nhiệm vụ cho MovementSystem (Từ Chương 2) tự động trượt con vật đi
            mov.target_grid_x = target_x
            mov.target_grid_y = target_y
            mov.is_moving = true
        } else {
            // Đụng hàng rào, đứng im lại
            animal.state = .IDLE
            animal.state_timer = 1.0
        }
    }
}
```

Bằng cách nhét Đầu vào (Input) giả lập vào `MovementComponent`, bạn tái sử dụng 100% logic di chuyển trượt siêu mượt mà của Nhân vật chính áp dụng cho Gà và Bò. Code cực kỳ "Sạch" và DRY (Don't Repeat Yourself)!
