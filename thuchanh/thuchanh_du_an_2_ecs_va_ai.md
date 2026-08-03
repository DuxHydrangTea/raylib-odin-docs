# Dự Án Tốt Nghiệp: Sinh Tồn
## Phần 2: Kiến trúc ECS & Sinh sản 1000 Quái vật

Sức hấp dẫn của thể loại này là cảm giác ngộp thở khi bị hàng ngàn con quái vật truy đuổi. Nếu dùng lập trình OOP thông thường, CPU của bạn sẽ bốc cháy. Đây là lúc sử dụng **ECS (Entity Component System)** và **Arena Allocator**.

*(Kỹ năng áp dụng: Chương 10, Chương 11, Chương 12, Chương 16)*

---

### 1. Định nghĩa ECS cho Quái vật

Vì có rất nhiều quái vật, chúng ta sử dụng mảng tĩnh (SoA) để CPU đọc dữ liệu siêu nhanh.

```odin
MAX_ENEMIES :: 2000

// Các mảng Component song song
enemy_active:   [MAX_ENEMIES]bool
enemy_pos:      [MAX_ENEMIES]rl.Vector2
enemy_hp:       [MAX_ENEMIES]f32
enemy_speed:    [MAX_ENEMIES]f32

// Hàm sinh quái vật
spawn_enemy :: proc(x, y: f32) {
    for i in 0..<MAX_ENEMIES {
        if !enemy_active[i] {
            enemy_active[i] = true
            enemy_pos[i] = {x, y}
            enemy_hp[i] = 20.0
            enemy_speed[i] = f32(rl.GetRandomValue(50, 100))
            break
        }
    }
}
```

### 2. Trí tuệ Nhân tạo (AI Pathfinding) cơ bản

Mỗi khung hình, Hệ thống di chuyển (Movement System) sẽ lặp qua 2000 con quái vật. Chúng sẽ tự động xoay hướng (Vector Normalize) và tiến thẳng về phía Player.

```odin
// Hệ thống Cập nhật Quái vật (Bỏ vào trong Game Loop)
update_enemies :: proc(player_pos: rl.Vector2, dt: f32) {
    for i in 0..<MAX_ENEMIES {
        if enemy_active[i] {
            // 1. Tính toán Vector chỉ hướng từ Quái -> Player
            direction := player_pos - enemy_pos[i]
            
            // 2. Bình thường hóa (Normalize) Vector để lấy phương hướng chuẩn
            if rl.Vector2Length(direction) > 0 {
                direction = rl.Vector2Normalize(direction)
            }
            
            // 3. Cộng vận tốc vào vị trí
            enemy_pos[i] += direction * enemy_speed[i] * dt
        }
    }
}
```

### 3. Tối ưu Vật lý (Đẩy lùi - Knockback/Separation)

Khi hàng ngàn con quái vật cùng đi về 1 điểm (Player), chúng sẽ dính chặt vào nhau thành 1 cục cặn duy nhất. Để tránh hiện tượng này, chúng ta cần luật tách bầy (Separation).

*Thuật toán:* Lặp lại mảng quái vật. Nếu 2 con quái đứng quá gần nhau, tự động đẩy chúng dạt ra xa một chút.
*(Lưu ý: Để kiểm tra 2000x2000 con quái vật = 4 triệu phép tính, bạn sẽ cần tới `QuadTree` hoặc `Spatial Hashing` ở Chương 18. Nhưng tạm thời ta dùng vòng lặp lồng nhau cho đơn giản).*

```odin
// Hệ thống Tách bầy (Separation)
separate_enemies :: proc(dt: f32) {
    min_dist: f32 = 20.0 // Bán kính không cho phép đè lên nhau
    
    for i in 0..<MAX_ENEMIES {
        if !enemy_active[i] do continue
        
        for j in i+1..<MAX_ENEMIES { // Chỉ so sánh với các con đứng sau để tránh lặp
            if !enemy_active[j] do continue
            
            dist := rl.Vector2Distance(enemy_pos[i], enemy_pos[j])
            if dist < min_dist && dist > 0 {
                // Vector đẩy nhau ra
                push_dir := rl.Vector2Normalize(enemy_pos[i] - enemy_pos[j])
                push_force := (min_dist - dist) * 2.0 * dt
                
                enemy_pos[i] += push_dir * push_force
                enemy_pos[j] -= push_dir * push_force // Con kia lùi ngược lại
            }
        }
    }
}
```

### 4. Đưa vào Game Loop

```odin
// Spawn 1000 quái vật ngẫu nhiên ngoài màn hình khi khởi động
for i in 0..<1000 {
    spawn_enemy(f32(rl.GetRandomValue(-2000, 2000)), f32(rl.GetRandomValue(-2000, 2000)))
}

// Bên trong vòng lặp chính (Update)
update_enemies(player_pos, dt)
separate_enemies(dt)

// Bên trong BeginMode2D (Draw)
for i in 0..<MAX_ENEMIES {
    if enemy_active[i] {
        rl.DrawCircleV(enemy_pos[i], 10, rl.RED)
    }
}
```

**Thành quả:** Khi chạy, bạn sẽ thấy 1000 đốm đỏ bò lổn nhổn trên màn hình đuổi theo bạn, chúng tự dạt ra khỏi nhau như một đàn kiến khổng lồ!
