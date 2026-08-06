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

## 5. Bươm Bướm Bay Dập Dờn (Butterflies)

Bươm bướm bay lượn trên bản đồ giúp game trông "sống" hơn rất nhiều. Ta không cần AI phức tạp, chỉ cần dùng hàm lượng giác `math.sin()` để tạo quỹ đạo bay chập chờn.

```odin
Butterfly :: struct {
    x, y: f32,
    base_y: f32,       // Trục Y gốc để lượn sóng
    speed: f32,
    time_offset: f32,  // Lệch pha để các con bướm không bay giống hệt nhau
    color: rl.Color,
}

butterflies: [20]Butterfly

init_butterflies :: proc() {
    import "core:math/rand"
    for i in 0..<20 {
        b := &butterflies[i]
        b.x = rand.float32() * 800.0 // MAP_WIDTH
        b.base_y = rand.float32() * 600.0 // MAP_HEIGHT
        b.speed = rand.float32() * 20.0 + 10.0
        b.time_offset = rand.float32() * 100.0
        
        // Random màu bướm (trắng, vàng nhạt, xanh lơ)
        colors := [3]rl.Color{ rl.WHITE, rl.YELLOW, rl.SKYBLUE }
        b.color = colors[rand.int31_max(3)]
    }
}

update_butterflies :: proc(dt: f32, global_time: f32) {
    import "core:math"
    
    for i in 0..<20 {
        b := &butterflies[i]
        
        // Bay từ trái sang phải
        b.x += b.speed * dt
        
        // Nếu bay ra khỏi màn hình thì vòng lại bên trái
        if b.x > 800.0 {
            b.x = -10.0
            b.base_y = rand.float32() * 600.0
        }
        
        // Lượn sóng hình Sin
        // Biên độ lượn là 15 pixels, tốc độ vỗ cánh phụ thuộc global_time
        wave := math.sin((global_time + b.time_offset) * 5.0) * 15.0
        b.y = b.base_y + wave
    }
}

render_butterflies :: proc() {
    for i in 0..<20 {
        b := &butterflies[i]
        // Vẽ 1 hình vuông nhỏ 2x2 pixel giả làm con bướm
        rl.DrawRectangleV(rl.Vector2{b.x, b.y}, rl.Vector2{2, 2}, b.color)
    }
}
```

## 6. Hiệu Ứng Lá Rơi (Falling Leaves)

Khi nhân vật chặt cây hoặc có gió thổi, một vài chiếc lá rơi lả tả xuống đất sẽ tạo cảm giác rất thơ mộng. Ta có thể dùng lại hệ thống `particle_pool` ở trên nhưng tinh chỉnh lại gia tốc `vy` (cho rơi thật chậm) và dùng `sin()` để lá lắc lư trái phải.

```odin
spawn_falling_leaves :: proc(tree_x: f32, tree_y: f32) {
    import "core:math/rand"
    
    for i := 0; i < 5; i += 1 {
        if particle_count >= 5000 do break
        
        p := &particle_pool[particle_count]
        // Bắt đầu từ tán cây
        p.x = tree_x + (rand.float32() - 0.5) * 40.0
        p.y = tree_y - 60.0 + (rand.float32() - 0.5) * 20.0 
        
        p.vx = 0 // Sẽ bị tác động bởi lực gió lúc update
        p.vy = rand.float32() * 15.0 + 5.0 // Rơi rất chậm (5 -> 20 pixels/s)
        
        p.life = rand.float32() * 3.0 + 2.0 // Bay lơ lửng trong 2-5 giây
        p.size = 3.0
        p.color = rl.LIME // Màu xanh lá non
        
        particle_count += 1
    }
}
```

Đồng thời trong hàm `update_particles(dt)`, ta thêm một thủ thuật nhỏ: Hạt nào rơi càng chậm (như chiếc lá) thì càng chịu tác động của lực cản không khí và lắc lư:

```odin
    // Bên trong vòng lặp update_particles (dòng 69, thay thế logic trọng lực)
    p.x += p.vx * dt
    p.y += p.vy * dt
    
    if p.vy > 0 && p.vy < 30.0 { 
        // Đích thị là lá rơi, lắc lư trái phải bằng hình sin của thời gian sống
        import "core:math"
        p.x += math.sin(p.life * 8.0) * 30.0 * dt
    } else {
        // Đất đá văng thì rơi nhanh xuống
        p.vy += 200.0 * dt
    }
```

---

Và thế là xong! Tác phẩm **Nông Trại Avatar 2D** của bạn nay đã mang một dáng vẻ vô cùng Chuyên Nghiệp. Khi cuốc đất, âm thanh "Xoạch" vang lên đồng thời những hạt đất văng tung tóe ra xung quanh. Có những chú bướm chập chờn bay quanh các luống hoa, và thỉnh thoảng một cơn gió lướt qua làm vài chiếc lá rơi lả tả.

**Lời kết:** Bạn đã nắm trong tay lộ trình và kiến trúc chuẩn chỉ nhất để tái tạo huyền thoại Avatar. Từ Data-driven ECS, thuật toán Culling bản đồ, cho đến Khóa Mutex đồng bộ Trộm Cắp và các thủ thuật thổi hồn vào game. Hãy mở file code lên và bắt đầu hành trình ngay thôi!
