# Chương 2: Va chạm Bản đồ (Tilemap Platforming AABB)

Trong Chương 1, chúng ta đã hard-code một đường thẳng `GROUND_Y = 400` làm mặt đất. Giờ là lúc biến nó thành một bản đồ thực sự với các bậc thang, vách núi giống như bãi luyện công Tonek.

## 1. Bản đồ lưới (Grid Map)

Chúng ta sẽ định nghĩa một bản đồ dạng mảng 2 chiều đơn giản. Số `1` là tường đất, số `0` là không khí.

```odin
package core

import rl "vendor:raylib"
import "../ecs"

TILE_SIZE :: 32
MAP_WIDTH :: 25
MAP_HEIGHT :: 15

// Bản đồ mẫu (0: Trống, 1: Đất)
map_data: [MAP_HEIGHT][MAP_WIDTH]int = {
    {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0},
    {0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0},
    {1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0},
    {1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0},
    {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
    {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
    {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
    {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
}
```

## 2. Bí quyết xử lý Va chạm Platformer (Trục nào đi trục đó)

Lỗi kinh điển nhất khi làm game đi cảnh là nhân vật bị **kẹt vào góc tường** hoặc **xuyên qua tường** khi chạy nhanh. 
**Quy tắc vàng:** Luôn di chuyển và kiểm tra va chạm trục X TRƯỚC, giải quyết xong xuôi mới di chuyển và kiểm tra va chạm trục Y.

Mở `ecs/systems.odin` và sửa lại `system_physics_and_input`:

```odin
package ecs

import rl "vendor:raylib"
import "../core" // Để lấy dữ liệu map_data và TILE_SIZE

// Hàm hỗ trợ kiểm tra va chạm với Map
check_map_collision :: proc(rect: rl.Rectangle) -> bool {
    // Tìm các ô Grid mà hình chữ nhật này đang đè lên
    min_col := int(rect.x) / core.TILE_SIZE
    max_col := int(rect.x + rect.width - 1) / core.TILE_SIZE
    min_row := int(rect.y) / core.TILE_SIZE
    max_row := int(rect.y + rect.height - 1) / core.TILE_SIZE

    // Chặn viền bản đồ
    if min_col < 0 || max_col >= core.MAP_WIDTH do return true
    if min_row < 0 || max_row >= core.MAP_HEIGHT do return true

    for r in min_row..=max_row {
        for c in min_col..=max_col {
            if core.map_data[r][c] == 1 {
                return true // Có va chạm với đất/tường!
            }
        }
    }
    return false
}

system_physics_and_input :: proc(dt: f32) {
    if len(transforms) == 0 do return
    
    player_t := &transforms[0]
    player_v := &velocities[0]

    // 1. Lấy input
    player_v.vel.x = 0
    if rl.IsKeyDown(.LEFT) do player_v.vel.x = -MOVE_SPEED
    if rl.IsKeyDown(.RIGHT) do player_v.vel.x = MOVE_SPEED
    
    if rl.IsKeyPressed(.SPACE) && player_v.is_grounded {
        player_v.vel.y = JUMP_FORCE
        player_v.is_grounded = false
    }

    if !player_v.is_grounded {
        player_v.vel.y += GRAVITY * dt
    }

    // ==============================================
    // 2. GIẢI QUYẾT VA CHẠM TRỤC X
    // ==============================================
    player_t.position.x += player_v.vel.x * dt
    player_rect := rl.Rectangle{player_t.position.x, player_t.position.y, player_t.size.x, player_t.size.y}
    
    if check_map_collision(player_rect) {
        // Nếu đâm vào tường theo chiều ngang, phải lùi lại
        if player_v.vel.x > 0 { // Đang đi sang phải
            // Đẩy ra sát mép tường bên trái
            player_t.position.x = f32(int(player_rect.x + player_rect.width) / core.TILE_SIZE * core.TILE_SIZE) - player_rect.width
        } else if player_v.vel.x < 0 { // Đang đi sang trái
            // Đẩy ra sát mép tường bên phải
            player_t.position.x = f32(int(player_rect.x) / core.TILE_SIZE * core.TILE_SIZE + core.TILE_SIZE)
        }
        player_v.vel.x = 0 // Tắt vận tốc
    }

    // ==============================================
    // 3. GIẢI QUYẾT VA CHẠM TRỤC Y
    // ==============================================
    player_t.position.y += player_v.vel.y * dt
    player_rect.x = player_t.position.x // Cập nhật lại X mới nhất
    player_rect.y = player_t.position.y 
    
    player_v.is_grounded = false // Reset mỗi frame

    if check_map_collision(player_rect) {
        if player_v.vel.y > 0 { // Đang rơi xuống (Đập chân xuống đất)
            player_t.position.y = f32(int(player_rect.y + player_rect.height) / core.TILE_SIZE * core.TILE_SIZE) - player_rect.height
            player_v.is_grounded = true // Xác nhận chạm đất an toàn
        } else if player_v.vel.y < 0 { // Đang nhảy lên (Đập đầu vào trần nhà)
            player_t.position.y = f32(int(player_rect.y) / core.TILE_SIZE * core.TILE_SIZE + core.TILE_SIZE)
        }
        player_v.vel.y = 0 // Hết lực
    }
}
```

> [!TIP]
> Việc chia làm 2 bước X và Y đảm bảo game tự động biết được bạn đang va vào vách núi (X) hay tiếp đất (Y). Thuật toán đẩy mép tường (`/ TILE_SIZE * TILE_SIZE`) rất phổ biến trong các game Grid-based (Minecraft, Terraria, Mario).

## 3. Vẽ Bản Đồ

Cập nhật `render_game` trong `core/game.odin`:

```odin
    // Vẽ Tilemap
    for r in 0..<MAP_HEIGHT {
        for c in 0..<MAP_WIDTH {
            if map_data[r][c] == 1 {
                rl.DrawRectangle(i32(c * TILE_SIZE), i32(r * TILE_SIZE), TILE_SIZE, TILE_SIZE, rl.DARKBROWN)
            }
        }
    }
```

Hãy thử chạy game và điều khiển Ninja nhảy lên các bục gỗ hệt như Ninja School nhé! Ở chương tiếp theo, chúng ta sẽ lắp Camera để màn hình di chuyển theo Ninja.
