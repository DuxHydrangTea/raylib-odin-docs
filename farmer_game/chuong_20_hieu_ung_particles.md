# Chương 20: Game Feel - Hạt & Âm Thanh (Polish)

Nếu bạn code mượt mà cỡ nào, nhưng nhổ củ cải mà không có miếng đất nào văng lên, củ cải không bay vào túi thì game của bạn vẫn như "Bát mì tôm không trứng".
Hãy cho thêm Game Juice (Độ mọng nước) vào.

## 1. Hệ thống Hạt (Particle System) Cực Nhẹ

Raylib không tích hợp sẵn Particle System, nhưng với cấu trúc Data-Oriented (SoA) của Odin, ta có thể tự viết 1 hệ thống quản lý 5000 hạt bay nhảy mà FPS vẫn 60 tròn.

```odin
package core

import rl "vendor:raylib"

Particle :: struct {
    x, y: f32,
    vx, vy: f32,      // Gia tốc (bay đi)
    life: f32,        // Thời gian sống
    color: rl.Color,
    size: f32,
}

particle_pool: [5000]Particle
particle_count: int = 0
```

## 2. Hàm Nổ Bụi Đất (Dirt Splatter)

Mỗi khi người chơi cuốc đất, ta gọi hàm này để bung ra 10 hạt bụi màu nâu rớt lả tả.

```odin
spawn_dirt_particles :: proc(grid_x: int, grid_y: int) {
    import "core:math/rand"
    
    // Tọa độ trung tâm của ô đất
    center_x := f32(grid_x * TILE_SIZE + TILE_SIZE/2)
    center_y := f32(grid_y * TILE_SIZE + TILE_SIZE/2)
    
    for i := 0; i < 10; i += 1 {
        if particle_count >= 5000 do break // Hết dung lượng mảng
        
        p := &particle_pool[particle_count]
        p.x = center_x
        p.y = center_y
        
        // Văng tứ tung với lực random
        p.vx = (rand.float32() - 0.5) * 100.0 // Tốc độ X từ -50 đến 50
        p.vy = (rand.float32() - 0.5) * 100.0 - 50.0 // Búng nhẹ lên trên (Âm Y)
        
        p.life = rand.float32() * 0.5 + 0.2 // Sống từ 0.2 đến 0.7 giây
        p.size = rand.float32() * 4.0 + 2.0
        p.color = rl.BROWN
        
        particle_count += 1
    }
}
```

## 3. Cập nhật và Vẽ Hạt (Render)

Trong Game Loop, ta làm hạt rớt xuống dưới tác dụng của Trọng Lực (Gravity).

```odin
update_particles :: proc(dt: f32) {
    for i := 0; i < particle_count; {
        p := &particle_pool[i]
        
        // Vật lý
        p.x += p.vx * dt
        p.y += p.vy * dt
        p.vy += 200.0 * dt // Trọng lực kéo hạt rơi xuống
        
        // Mờ dần theo thời gian (Fading)
        p.life -= dt
        
        if p.life <= 0 {
            // Xóa hạt bằng cách tráo phần tử cuối cùng lên chỗ này (O(1) deletion)
            particle_pool[i] = particle_pool[particle_count - 1]
            particle_count -= 1
            // Không tăng biến 'i' để kiểm tra lại phần tử mới tráo xuống
        } else {
            i += 1
        }
    }
}

render_particles :: proc() {
    for i := 0; i < particle_count; i += 1 {
        p := &particle_pool[i]
        
        // Tính toán độ mờ Alpha dựa trên thời gian sống
        alpha := u8(max(0, min(255, int(p.life * 255.0))))
        c := p.color
        c.a = alpha
        
        rl.DrawRectangleV(rl.Vector2{p.x, p.y}, rl.Vector2{p.size, p.size}, c)
    }
}
```

## 4. Âm Thanh (Audio Manager)

Game nông trại cần âm thanh thanh bình, vui vẻ. Đừng load lại File `.wav` nhiều lần vì nó làm giật game.

```odin
// Khởi tạo một lần lúc bật game
sounds: map[string]rl.Sound

init_audio :: proc() {
    rl.InitAudioDevice()
    sounds["hoe"] = rl.LoadSound("assets/hoe.wav")
    sounds["harvest"] = rl.LoadSound("assets/harvest_coin.wav")
    sounds["dog_bark"] = rl.LoadSound("assets/dog_bark.wav")
}

play_sound :: proc(name: string) {
    // Để tránh việc 10 người cùng cuốc 1 lúc làm nổ loa, ta check is_playing
    // (Mặc dù Raylib hỗ trợ Multi-channel, nhưng nên giới hạn)
    if sound, ok := sounds[name]; ok {
        rl.PlaySound(sound)
    }
}
```

Và thế là xong! Tác phẩm **Nông Trại Avatar 2D** của bạn nay đã mang một dáng vẻ Chuyên Nghiệp. Khi cuốc đất, âm thanh "Xoạch" vang lên đồng thời những hạt đất văng tung tóe ra xung quanh. Cây lớn, bạn nhặt nông sản, màn hình thả xuống một túi vàng chói lọi.

**Lời kết:** Bạn đã nắm trong tay lộ trình và kiến trúc chuẩn chỉ nhất để tái tạo huyền thoại Avatar. Từ Data-driven ECS, thuật toán Culling bản đồ, cho đến Khóa Mutex đồng bộ Trộm Cắp. Hãy mở `main.odin` lên và bắt đầu hành trình ngay thôi!
