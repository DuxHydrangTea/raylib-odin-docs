# Chương 2: Xây Dựng Hệ Thống Grid-Based Movement

Điểm đặc trưng nhất của Avatar 2D và các game Nông trại (như Stardew Valley, Harvest Moon) là bản đồ được chia thành các ô vuông (Grid). Nhân vật và cây cối tương tác dựa trên hệ tọa độ Lưới (`grid_x`, `grid_y`), thay vì tọa độ Pixel.

Tuy nhiên, nếu chỉ cập nhật tọa độ Grid, nhân vật sẽ bị "dịch chuyển tức thời" (Teleport) từ ô này sang ô khác. Chúng ta cần kết hợp giữa **Tọa độ Grid logic** và **Di chuyển trượt (Smooth Pixel Movement)**.

## 1. Định nghĩa Hằng số Grid

```odin
package core

TILE_SIZE :: 32 // Mỗi ô đất có kích thước 32x32 pixel
```

## 2. Trạng thái Di chuyển của Nhân vật

Khi người chơi ấn nút Mũi tên, nhân vật không lập tức cập nhật vị trí tự do, mà sẽ bị khóa (khởi tạo một hành trình từ ô hiện tại sang ô tiếp theo).

```odin
package ecs

import rl "vendor:raylib"

Direction :: enum { DOWN, UP, LEFT, RIGHT, NONE }

MovementComponent :: struct {
    is_moving: bool,
    target_grid_x, target_grid_y: int,
    facing: Direction,
    speed: f32, // Số pixel mỗi giây
}
```

## 3. Hệ thống Di chuyển Grid (MovementSystem)

Hệ thống này kiểm tra: Nếu nhân vật đang không di chuyển, cho phép nhận phím. Nếu đang di chuyển, ép nhân vật trượt tới ô đích trước khi nhận phím mới. (Ngăn chặn việc đi nửa chừng ô).

```odin
package ecs

import rl "vendor:raylib"
import "core:math"

// Update được gọi mỗi frame trong Game Loop
update_movement_system :: proc(world: ^World, dt: f32) {
    for i := 0; i < int(world.next_entity_id); i += 1 {
        if world.mask_position[i] && world.mask_movement[i] {
            pos := &world.positions[i]
            mov := &world.movements[i]
            
            if mov.is_moving {
                // Tính tọa độ pixel đích đến
                target_px := f32(mov.target_grid_x * TILE_SIZE)
                target_py := f32(mov.target_grid_y * TILE_SIZE)
                
                // Trượt mượt mà (Lerp hoặc MoveTowards)
                step := mov.speed * dt
                
                if abs(pos.pixel_x - target_px) <= step && abs(pos.pixel_y - target_py) <= step {
                    // Đã tới nơi, Snap vào lưới chính xác
                    pos.pixel_x = target_px
                    pos.pixel_y = target_py
                    pos.grid_x = mov.target_grid_x
                    pos.grid_y = mov.target_grid_y
                    mov.is_moving = false // Mở khóa nhận phím
                } else {
                    // Tiếp tục di chuyển
                    if pos.pixel_x < target_px do pos.pixel_x += step
                    if pos.pixel_x > target_px do pos.pixel_x -= step
                    if pos.pixel_y < target_py do pos.pixel_y += step
                    if pos.pixel_y > target_py do pos.pixel_y -= step
                }
            } 
            else {
                // Xử lý Input khi đứng yên tại 1 ô lưới
                process_input(pos, mov)
            }
        }
    }
}

process_input :: proc(pos: ^Position, mov: ^MovementComponent) {
    dx, dy := 0, 0
    if rl.IsKeyDown(.RIGHT) {
        dx = 1
        mov.facing = .RIGHT
    } else if rl.IsKeyDown(.LEFT) {
        dx = -1
        mov.facing = .LEFT
    } else if rl.IsKeyDown(.DOWN) {
        dy = 1
        mov.facing = .DOWN
    } else if rl.IsKeyDown(.UP) {
        dy = -1
        mov.facing = .UP
    }
    
    // Nếu có bấm phím, tính toán đích đến
    if dx != 0 || dy != 0 {
        next_x := pos.grid_x + dx
        next_y := pos.grid_y + dy
        
        // KIỂM TRA VA CHẠM (Grid Collision)
        // Gọi hàm từ hệ thống Tilemap để kiểm tra cả 2 lớp (Lớp nền và Lớp vật thể)
        // Chỉ cho phép đi nếu tọa độ nằm trong bản đồ VÀ không bị chặn
        if is_walkable(next_x, next_y) {
            mov.target_grid_x = next_x
            mov.target_grid_y = next_y
            mov.is_moving = true
        } else {
            // Có thể play âm thanh "cộc cộc" khi đâm vào hàng rào
        }
    }
}
```

### Ưu điểm của kiến trúc này (So với Anti-pattern):
1. **Kiểm tra va chạm chuẩn tuyệt đối:** Việc check va chạm với cây cỏ, hàng rào chỉ diễn ra 1 lần ở cấp độ Lưới (Grid), không cần dùng thuật toán quét hộp AABB nặng nề ở cấp độ Pixel.
2. **Đồng bộ Mạng (Multiplayer):** Khi làm Game Online, thay vì gửi tọa độ `X=12.55, Y=45.22` liên tục, bạn chỉ cần gửi gói tin `Lệnh đi sang phải`. Các Client khác sẽ tự trượt (Interpolate) nhân vật sang ô tiếp theo cực kì mượt mà. Đỡ tốn 90% băng thông mạng.
