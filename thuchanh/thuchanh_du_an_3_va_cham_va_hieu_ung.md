# Dự Án Tốt Nghiệp: Sinh Tồn
## Phần 3: Đạn mạc, Va chạm và Hạt (Particles)

Người chơi không thể bỏ chạy mãi. Chúng ta cần hệ thống Đạn (Bullets) tự động bắn, tính toán va chạm để tiêu diệt quái, và hệ thống Hạt lấp lánh (Particles) văng ra khi quái chết.

*(Kỹ năng áp dụng: Chương 8, Chương 13, Chương 17)*

---

### 1. Hệ thống Đạn (Bullets) tự động

Player sẽ tự động bắn viên đạn gần nhất vào kẻ địch. Sử dụng ECS tương tự như quái vật.

```odin
MAX_BULLETS :: 500
bullet_active: [MAX_BULLETS]bool
bullet_pos:    [MAX_BULLETS]rl.Vector2
bullet_vel:    [MAX_BULLETS]rl.Vector2
bullet_life:   [MAX_BULLETS]f32 // Sống tối đa 2 giây

spawn_bullet :: proc(pos, dir: rl.Vector2) {
    for i in 0..<MAX_BULLETS {
        if !bullet_active[i] {
            bullet_active[i] = true
            bullet_pos[i] = pos
            bullet_vel[i] = dir * 800.0 // Tốc độ đạn
            bullet_life[i] = 2.0
            break
        }
    }
}
```

### 2. Xử lý Va chạm Đạn vs Quái

Chúng ta dùng kiểm tra khoảng cách vòng tròn (Circle Collision).

```odin
check_bullet_collisions :: proc() {
    for b in 0..<MAX_BULLETS {
        if !bullet_active[b] do continue
        
        for e in 0..<MAX_ENEMIES {
            if !enemy_active[e] do continue
            
            // Nếu khoảng cách giữa Đạn và Quái < Tổng bán kính của chúng
            if rl.Vector2Distance(bullet_pos[b], enemy_pos[e]) < 15.0 {
                // Trúng đích!
                bullet_active[b] = false // Hủy đạn
                enemy_hp[e] -= 10.0      // Quái mất máu
                
                if enemy_hp[e] <= 0 {
                    enemy_active[e] = false // Quái chết
                    // TODO: Gọi hàm spawn_particles() tại đây
                    // TODO: Gọi hàm spawn_xp_gem() tại đây
                }
                break // Đạn này đã nổ, không xét va chạm với quái khác nữa
            }
        }
    }
}
```

### 3. Blend Mode & Hiệu ứng Đạn Phát Sáng

Những viên đạn phép thuật trông sẽ vô cùng rẻ tiền nếu chỉ là vẽ hình tròn. Bằng cách áp dụng **Additive Blend Mode** (Chương 8), các viên đạn sẽ chói lòa như pháo sáng.

```odin
// Trong phần Draw, sau BeginMode2D
rl.BeginBlendMode(.ADDITIVE)
    for b in 0..<MAX_BULLETS {
        if bullet_active[b] {
            // Vẽ quầng sáng mờ xung quanh (To hơn)
            rl.DrawCircleV(bullet_pos[b], 20, rl.Color{0, 200, 255, 100})
            // Vẽ tâm sáng chói (Nhỏ hơn)
            rl.DrawCircleV(bullet_pos[b], 5, rl.WHITE)
        }
    }
rl.EndBlendMode()
```

### 4. Hệ thống Hạt Máu (Blood Particles)

Mỗi khi quái chết, máu văng tung tóe sẽ làm tăng "Game Feel". Dùng kỹ thuật Object Pooling (Chương 13).

```odin
// Gọi hàm này khi quái máu = 0
spawn_blood_explosion :: proc(x, y: f32) {
    for i in 0..<20 { // 20 giọt máu
        // Tạo Particle, random vận tốc bay tứ tung
        // ... (Xem lại Chương 13) ...
    }
}
```

**Thành quả:** Đạn tự động bay chéo màn hình, sáng lấp lánh chói lòa. Mỗi lần trúng quái là một đám hạt li ti màu đỏ văng ra làm bãi chiến trường trở nên vô cùng khốc liệt!
