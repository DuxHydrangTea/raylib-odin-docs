# Chương 13: Hệ thống Hạt (Particle System)

Khi bom nổ, máu bắn ra, hay tia lửa từ ống xả xe tăng... bạn không thể tạo hàng trăm Entity cho chúng vì như thế rất lãng phí. Bạn cần một **Particle System** - một hệ thống sinh ra các hạt ảnh nhỏ xíu, tồn tại trong vài giây rồi biến mất.

Bí quyết của Particle System nằm ở việc tái sử dụng bộ nhớ (Object Pooling / Ring Buffer) để không bao giờ phải gọi hàm cấp phát `new()` trong vòng lặp.

---

## 1. Cấu trúc Hạt (Particle)

Mỗi hạt cần biết vị trí, vận tốc, màu sắc, thời gian sống (lifetime) và độ mờ (alpha).

```odin
package game
import rl "vendor:raylib"

Particle :: struct {
    active: bool,
    pos: rl.Vector2,
    vel: rl.Vector2,
    color: rl.Color,
    life: f32,       // Thời gian sống tối đa (vd: 1.0 giây)
    life_left: f32,  // Thời gian còn lại
    size: f32,
}

MAX_PARTICLES :: 2000
particles: [MAX_PARTICLES]Particle
```

## 2. Hàm Bắn Hạt (Emit)

Chúng ta duyệt qua mảng `particles` tìm hạt nào đang "chết" (không active) để tái chế nó thành hạt mới.

```odin
emit_particle :: proc(x, y: f32, color: rl.Color) {
    for i in 0..<MAX_PARTICLES {
        if !particles[i].active {
            particles[i].active = true
            particles[i].pos = {x, y}
            
            // Random vận tốc bay tứ tung (Vụ nổ)
            vx := f32(rl.GetRandomValue(-100, 100))
            vy := f32(rl.GetRandomValue(-100, 100))
            particles[i].vel = {vx, vy}
            
            particles[i].color = color
            particles[i].life = 1.0
            particles[i].life_left = 1.0
            particles[i].size = f32(rl.GetRandomValue(2, 6))
            
            break // Chỉ sinh 1 hạt rồi thoát
        }
    }
}
```
*(Thực tế, khi làm nổ bom, bạn sẽ bọc hàm này trong một vòng lặp `for` chạy 50 lần để sinh ra 50 mảnh vỡ cùng lúc).*

## 3. Cập nhật và Vẽ (Update & Render)

Hạt càng gần chết thì càng mờ đi, hoặc rớt xuống đất do trọng lực.
*Đây là lúc kết hợp tuyệt vời với chế độ **Blend Mode** (Chương 8) để các hạt sáng lên khi đè vào nhau.*

```odin
update_and_draw_particles :: proc(dt: f32) {
    rl.BeginBlendMode(.ADDITIVE) // Làm các tia lửa cộng màu phát sáng
    
    for i in 0..<MAX_PARTICLES {
        if particles[i].active {
            // 1. Cập nhật thời gian sống
            particles[i].life_left -= dt
            if particles[i].life_left <= 0 {
                particles[i].active = false
                continue
            }
            
            // 2. Cập nhật vị trí (thêm trọng lực rơi xuống)
            particles[i].vel.y += 200.0 * dt
            particles[i].pos += particles[i].vel * dt
            
            // 3. Tính toán độ mờ (Fade out)
            // Tỷ lệ từ 1.0 giảm dần về 0.0
            ratio := particles[i].life_left / particles[i].life
            fade_color := rl.Fade(particles[i].color, ratio)
            
            // Tính toán thu nhỏ dần
            current_size := particles[i].size * ratio
            
            // 4. Vẽ hạt
            rl.DrawCircleV(particles[i].pos, current_size, fade_color)
        }
    }
    
    rl.EndBlendMode()
}
```

## Tổng kết
Hệ thống hạt hoạt động cực nhanh vì toàn bộ 2000 hạt đã được xin RAM ngay từ đầu (Tĩnh). Với đoạn code trên, bạn có thể tạo ra mọi thứ: Tuyết rơi (vận tốc Y nhỏ), Lửa (vận tốc Y hướng lên, màu Đỏ->Vàng->Trắng), hay Máu văng (Có thêm va chạm với mặt đất).
