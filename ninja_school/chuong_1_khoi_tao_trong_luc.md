# Chương 1: Nền tảng Platformer & Trọng Lực (Gravity)

Khác với thể loại Top-down 2D (nhìn từ trên xuống) như Game Nông Trại nơi bạn có thể thoải mái di chuyển 4 hướng (Lên, Xuống, Trái, Phải), game **Ninja School** thuộc thể loại **Side-scrolling Platformer** (Màn hình ngang). 

Trong Platformer, quy luật vật lý quan trọng nhất và khó nhằn nhất chính là **Trọng Lực (Gravity)**. Bạn không thể bấm phím "Lên" để đi lên bầu trời được, thay vào đó bạn phải "Nhảy" (Jump) và sau đó bị lực hấp dẫn kéo tụt xuống đất.

---

## 1. Kiến trúc thư mục dự án

Chúng ta sẽ áp dụng lại mô hình Multi-package chia nhỏ file giống hệt như game Nông Trại. Sự gọn gàng là chìa khóa để chống lại mớ code hỗn độn sau này!

Cấu trúc dự án mới của bạn sẽ trông như thế này:
```text
ninja_school/
├── main.odin           (Điểm bắt đầu - Entry Point)
├── core/
│   └── game.odin       (Game Loop chính, khởi tạo cửa sổ)
└── ecs/
    ├── components.odin (Định nghĩa Dữ liệu: Vị trí, Vận tốc)
    ├── systems.odin    (Xử lý Vật lý, Di chuyển, Trọng lực)
    └── entities.odin   (Quản lý sinh/diệt Ninja)
```

---

## 2. Định nghĩa Component cho Platformer

Đầu tiên, hãy mở file `ecs/components.odin` và định nghĩa 2 Component cốt lõi nhất cho bất kỳ vật thể nào biết chuyển động: **Tọa độ** và **Vận tốc**.

```odin
package ecs

import "vendor:raylib"

// 1. Component Tọa Độ & Kích thước (AABB)
TransformComponent :: struct {
    position: raylib.Vector2,
    size:     raylib.Vector2, // Cần size để kiểm tra va chạm mặt đất
}

// 2. Component Vận Tốc (Physics)
VelocityComponent :: struct {
    vel:      raylib.Vector2,
    is_grounded: bool, // Rất quan trọng! Xác định Ninja có đang chạm đất không
}

// Các mảng dữ liệu (SoA - Struct of Arrays)
transforms: [dynamic]TransformComponent
velocities: [dynamic]VelocityComponent
```

> [!NOTE]
> Biến `is_grounded` là trái tim của game Platformer. Bạn chỉ được phép bấm phím Nhảy (Jump) nếu `is_grounded == true` (đang đứng trên mặt đất). Nếu không có nó, Ninja của bạn sẽ đạp không khí bay thẳng lên trời như chim!

---

## 3. Lực Hấp Dẫn & Nhảy (Gravity & Jump)

Bây giờ là lúc chúng ta mô phỏng định luật Newton. Mở file `ecs/systems.odin`.

Trong game, Trọng lực thực chất chỉ là một **Gia tốc hướng xuống dưới** (Trục Y tăng dần). Mỗi Frame, chúng ta sẽ cộng thêm gia tốc này vào Vận tốc Y của Ninja.

```odin
package ecs

import rl "vendor:raylib"

// Các hằng số Vật Lý
GRAVITY       :: 1500.0 // Lực hút trái đất (Pixel/giây^2)
JUMP_FORCE    :: -600.0 // Lực bật nhảy (Âm vì trục Y hướng lên trên)
MOVE_SPEED    :: 250.0  // Tốc độ chạy ngang

system_physics_and_input :: proc(dt: f32) {
    // Trong game này, giả sử Entity 0 luôn là Player (Ninja của chúng ta)
    if len(transforms) == 0 do return
    
    player_t := &transforms[0]
    player_v := &velocities[0]

    // 1. Xử lý Input (Di chuyển Trái/Phải)
    player_v.vel.x = 0
    if rl.IsKeyDown(.LEFT) {
        player_v.vel.x = -MOVE_SPEED
    }
    if rl.IsKeyDown(.RIGHT) {
        player_v.vel.x = MOVE_SPEED
    }

    // 2. Xử lý Bật Nhảy
    // Chỉ được nhảy nếu phím SPACE được bấm VÀ Ninja đang đứng trên đất
    if rl.IsKeyPressed(.SPACE) && player_v.is_grounded {
        player_v.vel.y = JUMP_FORCE
        player_v.is_grounded = false // Vừa nảy lên là mất chạm đất ngay
    }

    // 3. Áp dụng Trọng Lực (Rơi tự do)
    if !player_v.is_grounded {
        // Vận tốc = Gia tốc * Thời gian
        player_v.vel.y += GRAVITY * dt 
    }

    // 4. Cập nhật Tọa Độ (Quãng đường = Vận tốc * Thời gian)
    player_t.position.x += player_v.vel.x * dt
    player_t.position.y += player_v.vel.y * dt

    // 5. Hard-code Tạm Thời Mặt Đất (Sẽ làm Tilemap ở Chương 2)
    GROUND_Y :: 400.0
    if player_t.position.y >= GROUND_Y {
        player_t.position.y = GROUND_Y // Ép không cho lọt thỏm xuống lòng đất
        player_v.vel.y = 0             // Triệt tiêu vận tốc rơi
        player_v.is_grounded = true    // Xác nhận đã chạm đất
    }
}
```

### Tại sao JUMP_FORCE lại là số Âm?
Trong màn hình máy tính (bao gồm cả Raylib), tọa độ `(0, 0)` nằm ở **Góc trên cùng bên trái**. Trục Y chỉ hướng xuống dưới!
Do đó:
- Đi xuống (Rơi) = Cộng thêm vào Y (Trọng lực Dương).
- Đi lên (Nhảy) = Trừ đi khỏi Y (Lực Nhảy Âm).

---

## 4. Hiển thị Lên Màn Hình

Mở `core/game.odin` để gắn mọi thứ vào Game Loop.

```odin
package core

import rl "vendor:raylib"
import "../ecs"

update_game :: proc() {
    dt := rl.GetFrameTime()
    
    // Gọi hệ thống vật lý
    ecs.system_physics_and_input(dt)
}

render_game :: proc() {
    // Vẽ nền trời
    rl.ClearBackground(rl.SKYBLUE)
    
    // Vẽ mặt đất (Một hình chữ nhật màu Xanh lá cây)
    rl.DrawRectangle(0, int(400 + 32), 800, 200, rl.GREEN)

    // Vẽ Ninja của chúng ta (Tạm thời là khối vuông màu Đỏ)
    if len(ecs.transforms) > 0 {
        pos := ecs.transforms[0].position
        // Vẽ trừ đi chiều cao để khối vuông đứng TRÊN mặt đất (GROUND_Y)
        rl.DrawRectangle(int(pos.x), int(pos.y), 32, 32, rl.RED)
    }
    
    rl.DrawText("Dung phim Mui Ten de chay - SPACE de Nhay", 10, 10, 20, rl.BLACK)
}
```

*(Nhớ khởi tạo cửa sổ 800x600 ở file `main.odin` và `append` một Entity Ninja vào mảng Component nhé).*

### Chạy Thử Nào!
Khi bạn biên dịch xong và chạy, bạn sẽ thấy Ninja (khối vuông đỏ) rơi cái "bịch" xuống mặt cỏ xanh. Nhấn Phím cách (Space), khối vuông sẽ nảy lên rất mượt mà theo đúng quỹ đạo Parabol của vật lý đời thực! 

> [!TIP]
> Bạn có thể thử thay đổi giá trị `GRAVITY = 500` (Ninja sẽ bay bổng nhẹ tựa lông hồng trên mặt trăng) hoặc `GRAVITY = 3000` (Ninja đeo tạ sắt ngã sấp mặt). Việc tách rời các hằng số này giúp chúng ta dễ dàng tạo ra các kỹ năng "Khinh công" sau này!

Trong **Chương 2**, chúng ta sẽ loại bỏ biến `GROUND_Y` rác rưởi kia, và làm quen với hệ thống **Va chạm đa hướng (AABB)** cho những bản đồ Tilemap có vách núi, bậc thang phức tạp. Mời sếp lật trang!
