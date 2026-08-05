# Chương 3: Camera 2D Bám Đuổi & Cuộn Nền (Parallax)

Trong Ninja School, bản đồ trải dài rất rộng. Nhân vật di chuyển đến đâu, màn hình sẽ "trượt" theo đến đó. Raylib cung cấp cấu trúc `rl.Camera2D` tuyệt vời để làm việc này mà không cần bạn phải dịch chuyển tọa độ của toàn bộ quái vật và bản đồ.

---

## 1. Khởi tạo Camera2D

Chúng ta sẽ khai báo một biến `camera` toàn cục bên trong `core/game.odin`.

```odin
package core

import rl "vendor:raylib"
import "../ecs"

main_camera: rl.Camera2D

init_game :: proc() {
    // Khởi tạo Camera
    main_camera = rl.Camera2D{
        offset = rl.Vector2{ f32(rl.GetScreenWidth()) / 2.0, f32(rl.GetScreenHeight()) / 2.0 }, // Tâm màn hình
        target = rl.Vector2{0, 0}, // Sẽ bám theo Ninja
        rotation = 0.0,
        zoom = 1.0,
    }
}
```

## 2. Thuật toán bám đuôi (Lerp / Smooth Follow)

Nếu gán cứng `camera.target = player.position`, màn hình sẽ giật cục theo từng bước di chuyển của nhân vật. Lập trình viên thường dùng thuật toán nội suy tuyến tính (Lerp - Linear Interpolation) để camera "lướt" theo mượt mà.

Mở `ecs/systems.odin` và tạo một System mới cho Camera:

```odin
import "core:math"

system_camera :: proc(camera: ^rl.Camera2D, dt: f32) {
    if len(transforms) == 0 do return
    player_pos := transforms[0].position

    // Nội suy mượt mà từ vị trí hiện tại của Camera đến vị trí của Ninja
    // Tốc độ lướt = 5.0 (Càng lớn càng bám gắt)
    camera.target.x = math.lerp(camera.target.x, player_pos.x, 5.0 * dt)
    camera.target.y = math.lerp(camera.target.y, player_pos.y, 5.0 * dt)

    // Giới hạn Camera không cho quay lọt ra ngoài bản đồ (Deadzone clamping)
    min_x := camera.offset.x
    max_x := f32(core.MAP_WIDTH * core.TILE_SIZE) - camera.offset.x
    
    // Ép giá trị X nằm trong khoảng min_x và max_x
    if camera.target.x < min_x do camera.target.x = min_x
    if camera.target.x > max_x do camera.target.x = max_x
    
    // Làm tương tự cho trục Y nếu bản đồ có vực sâu
}
```

## 3. Render thông qua Camera

Để áp dụng góc nhìn của Camera vào quá trình vẽ đồ họa, bạn phải kẹp toàn bộ lệnh `DrawTexture` hoặc `DrawRectangle` vào giữa 2 lệnh `BeginMode2D` và `EndMode2D`.

Quay lại `core/game.odin`:

```odin
update_game :: proc() {
    dt := rl.GetFrameTime()
    ecs.system_physics_and_input(dt)
    
    // Cập nhật Camera sau khi Ninja đã di chuyển
    ecs.system_camera(&main_camera, dt)
}

render_game :: proc() {
    rl.ClearBackground(rl.SKYBLUE)
    
    // MỌI THỨ VẼ SAU LỆNH NÀY SẼ BỊ CHI PHỐI BỞI CAMERA
    rl.BeginMode2D(main_camera)

        // Vẽ Bản Đồ Tilemap
        for r in 0..<MAP_HEIGHT {
            for c in 0..<MAP_WIDTH {
                if map_data[r][c] == 1 {
                    rl.DrawRectangle(i32(c * TILE_SIZE), i32(r * TILE_SIZE), TILE_SIZE, TILE_SIZE, rl.DARKBROWN)
                }
            }
        }
        
        // Vẽ Ninja
        if len(ecs.transforms) > 0 {
            pos := ecs.transforms[0].position
            rl.DrawRectangle(i32(pos.x), i32(pos.y), 32, 32, rl.RED)
        }

    rl.EndMode2D()
    // KẾT THÚC CAMERA
    
    // Mọi thứ vẽ ở đây sẽ dính chặt vào màn hình (Dùng cho Giao diện UI: Máu, Nút bấm)
    rl.DrawText("UI: Mau = 100/100", 10, 10, 20, rl.RED)
}
```

## 4. Cuộn nền Đa tầng (Parallax Background) - Tùy chọn nâng cao

Khi bạn chạy ở làng Tonek, bạn sẽ thấy những ngọn núi ở xa trôi rất chậm, còn những hàng cây ở gần trôi nhanh hơn. Đó là Parallax Effect.

Cách làm cực kỳ đơn giản: Bạn chỉ cần vẽ bức ảnh ngọn núi với tọa độ X được dịch chuyển bằng `camera.target.x * 0.1` (Tốc độ trôi 10%), và bức ảnh hàng cây bằng `camera.target.x * 0.5` (Tốc độ trôi 50%). Kỹ thuật này đánh lừa thị giác tạo ra không gian 3D rất có chiều sâu.

> Bạn có thể thử nghiệm Parallax sau khi đã load được Ảnh (Texture). Ở chương sau, chúng ta sẽ bắt tay vào thiết kế 6 môn phái - phần cốt lõi của Ninja School!
