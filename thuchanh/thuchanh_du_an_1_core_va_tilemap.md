# Dự Án Tốt Nghiệp: Sinh Tồn (Vampire Survivors Clone)
## Phần 1: Core, Camera và Bản đồ vô tận (Tilemap)

Chào mừng bạn đến với dự án tốt nghiệp. Chúng ta sẽ xây dựng một tựa game nơi bạn bị bao vây bởi hàng ngàn con quái vật.
Trong phần đầu tiên, chúng ta sẽ thiết lập cốt lõi (Core), tạo Camera bám theo nhân vật và vẽ một bản đồ khổng lồ.

*(Kỹ năng áp dụng: Chương 1-6, Chương 14)*

---

### 1. Khởi tạo Boilerplate và Camera

Chúng ta dùng lại khung 8 bước ở bài trước, nhưng thêm một `Camera2D` trỏ vào nhân vật.

```odin
package game
import rl "vendor:raylib"

WINDOW_WIDTH :: 1280
WINDOW_HEIGHT :: 720

main :: proc() {
    rl.InitWindow(WINDOW_WIDTH, WINDOW_HEIGHT, "Vampire Survivors Clone")
    defer rl.CloseWindow()
    rl.SetTargetFPS(60)
    
    player_pos := rl.Vector2{0, 0}
    player_speed: f32 = 300.0

    // Khởi tạo Camera bám theo người chơi
    camera := rl.Camera2D {
        offset = {WINDOW_WIDTH / 2.0, WINDOW_HEIGHT / 2.0}, // Đặt player ở giữa màn hình
        target = player_pos,
        rotation = 0.0,
        zoom = 1.0,
    }

    for !rl.WindowShouldClose() {
        dt := rl.GetFrameTime()

        // 1. Input di chuyển
        if rl.IsKeyDown(.W) { player_pos.y -= player_speed * dt }
        if rl.IsKeyDown(.S) { player_pos.y += player_speed * dt }
        if rl.IsKeyDown(.A) { player_pos.x -= player_speed * dt }
        if rl.IsKeyDown(.D) { player_pos.x += player_speed * dt }

        // Camera luôn bám theo player
        camera.target = player_pos

        // 2. Vẽ
        rl.BeginDrawing()
            rl.ClearBackground(rl.BLACK)
            
            // Bật Camera để vẽ Thế giới
            rl.BeginMode2D(camera)
                // Vẽ nền cỏ (Tilemap) ở đây...
                rl.DrawRectangleV(player_pos, {32, 32}, rl.BLUE) // Vẽ Player
            rl.EndMode2D()
            
            // Vẽ UI ngoài Camera
            rl.DrawFPS(10, 10)
        rl.EndDrawing()
        
        free_all(context.temp_allocator)
    }
}
```

### 2. Vẽ Tilemap khổng lồ với Kỹ thuật Culling

Nếu ta vẽ mặt cỏ rải rác từ tọa độ -10.000 đến +10.000, game sẽ cực kỳ lag. Áp dụng Culling, ta chỉ vẽ cỏ xung quanh Camera.

```odin
// Thêm đoạn code này vào bên trong BeginMode2D
TILE_SIZE :: 64

// Tính tọa độ ô bắt đầu dựa trên góc trên-trái của Camera
cam_top_left := rl.Vector2{
    camera.target.x - camera.offset.x,
    camera.target.y - camera.offset.y
}

start_col := int(cam_top_left.x / TILE_SIZE) - 1
start_row := int(cam_top_left.y / TILE_SIZE) - 1

// Tính số lượng ô cần vẽ cho 1 khung hình (1280x720)
cols_per_screen := (WINDOW_WIDTH / TILE_SIZE) + 3
rows_per_screen := (WINDOW_HEIGHT / TILE_SIZE) + 3

for r in start_row ..< start_row + rows_per_screen {
    for c in start_col ..< start_col + cols_per_screen {
        // Tọa độ thế giới của ô gạch hiện tại
        tile_x := f32(c * TILE_SIZE)
        tile_y := f32(r * TILE_SIZE)
        
        // Vẽ gạch caro nền
        color := (r + c) % 2 == 0 ? rl.DARKGREEN : rl.GREEN
        rl.DrawRectangleV({tile_x, tile_y}, {TILE_SIZE, TILE_SIZE}, color)
    }
}
```

**Thành quả:** Khi chạy đoạn code trên, bạn sẽ thấy nhân vật màu xanh chạy giữa một cánh đồng xanh lá vô tận. Khung hình luôn ổn định ở mức 60FPS dù bản đồ lớn đến đâu!
