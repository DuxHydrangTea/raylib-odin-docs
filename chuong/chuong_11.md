# Chương 11: Hệ thống Vật lý 2D (Physics System)

Trong các chương trước, nhân vật của chúng ta di chuyển bằng cách cộng thẳng vận tốc vào tọa độ (`pos.x += speed * dt`). Cách này rất thô cứng. Trong chương này, chúng ta sẽ áp dụng các định luật vật lý Newton cơ bản để làm cho game có "sức nặng".

---

## 1. Gia tốc (Acceleration) và Vận tốc (Velocity)

Để nhân vật trượt đi một đoạn khi ngừng bấm phím (quán tính), chúng ta cần tách biệt Vận tốc và Gia tốc.
* **Gia tốc (acc)**: Lực tác động vào vật (như lực đẩy của động cơ, lực bấm phím).
* **Vận tốc (vel)**: Tốc độ hiện tại của vật. Gia tốc sẽ làm thay đổi vận tốc.
* **Vị trí (pos)**: Vận tốc sẽ làm thay đổi vị trí.

```odin
player_pos := rl.Vector2{100, 100}
player_vel := rl.Vector2{0, 0}
player_acc := rl.Vector2{0, 0}

friction   : f32 = 0.9  // Ma sát (0.0 đến 1.0)
move_force : f32 = 2000.0 // Lực đẩy
max_speed  : f32 = 500.0

for !rl.WindowShouldClose() {
    dt := rl.GetFrameTime()
    player_acc = {0, 0} // Reset gia tốc mỗi frame

    // 1. Áp dụng lực từ phím bấm
    if rl.IsKeyDown(.D) { player_acc.x += move_force }
    if rl.IsKeyDown(.A) { player_acc.x -= move_force }

    // 2. Tính toán Vận tốc (Velocity)
    player_vel += player_acc * dt
    
    // 3. Áp dụng Ma sát (Friction) để xe dừng lại từ từ
    player_vel *= friction

    // Giới hạn tốc độ tối đa
    if rl.Vector2Length(player_vel) > max_speed {
        player_vel = rl.Vector2Normalize(player_vel) * max_speed
    }

    // 4. Cập nhật vị trí
    player_pos += player_vel * dt
}
```

---

## 2. Trọng lực (Gravity) và Nhảy (Jump)

Trọng lực thực chất là một lực gia tốc (hướng xuống dưới) luôn luôn tồn tại trong mỗi khung hình.

```odin
gravity : f32 = 1500.0
jump_force : f32 = -800.0 // Lực hướng lên (âm Y)
is_grounded := false

// Trong vòng lặp Update:
// Luôn luôn kéo nhân vật xuống
player_vel.y += gravity * dt

// Nhảy
if rl.IsKeyPressed(.SPACE) && is_grounded {
    player_vel.y = jump_force
    is_grounded = false
}

// Xử lý chạm đất
if player_pos.y >= ground_y {
    player_pos.y = ground_y
    player_vel.y = 0 // Dừng rơi
    is_grounded = true
}
```

---

## 3. Raycasting (Bắn tia dò đường)

Raycast là kỹ thuật "bắn" một tia từ điểm A đến điểm B để xem tia đó có cắt qua bức tường nào không. 
Ứng dụng:
* Dò tầm nhìn (Line of Sight) của quái vật: Xem có bức tường nào chắn giữa quái vật và người chơi không.
* Làm súng bắn tỉa nổ ngay lập tức (Hitscan weapon) thay vì đạn bay từ từ.

*Thuật toán Raycast 2D cơ bản nhất là kiểm tra tia cắt với các đoạn thẳng (Line segments) của bức tường. Raylib hỗ trợ hàm `CheckCollisionLines`.*

```odin
origin := player_pos
target := rl.GetMousePosition()
hit_point: rl.Vector2

// Bắn tia từ súng đến chuột
if rl.CheckCollisionLines(origin, target, wall_start, wall_end, &hit_point) {
    // Tia laser bị chặn lại tại 'hit_point'
    rl.DrawLineV(origin, hit_point, rl.RED)
    rl.DrawCircleV(hit_point, 5, rl.YELLOW) // Hiệu ứng tia lửa chạm tường
} else {
    // Không trúng tường, vẽ hết chiều dài tia
    rl.DrawLineV(origin, target, rl.GREEN)
}
```

Với các định luật cơ bản này, nhân vật của bạn sẽ có cảm giác di chuyển cực kỳ "đã tay" giống như các tựa game platformer nổi tiếng (Celeste, Hollow Knight).
