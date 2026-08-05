# Chương 11: Text Sát Thương Văng Lên (Floating Text)

Không có gì sướng mắt trong NSO bằng việc tung một chiêu Phân thân chém đứt 3 con cóc, và hàng tá con số sát thương Màu Vàng/Đỏ nhảy loạn xạ lên trời rực rỡ.

Kỹ thuật này được gọi là **Floating Combat Text (FCT)**.

---

## 1. Component Dành Cho Chữ

Về bản chất, các con số văng lên trời đó CŨNG CHỈ LÀ MỘT ENTITY! Nó có Tọa độ, có Vận tốc (bay văng lên trên), và có Thời gian sống (Tuổi thọ).

Thay vì phải tạo Component mới, ta lại đẻ ra 1 thực thể, ném `Transform` và `Velocity` vào nó, kèm theo một Component `FloatingText`.

Mở `ecs/components.odin`:

```odin
FloatingTextComponent :: struct {
    text:  string,
    color: raylib.Color,
    timer: f32, // Tuổi thọ (ví dụ sống được 1 giây)
}

// Bảng dữ liệu 
floating_texts: map[EntityID]FloatingTextComponent
```

## 2. Hàm Sinh Ra Con Số

Mở `ecs/entities.odin`, chúng ta tạo một hàm tiện ích mà ở Chương 9 chúng ta đã gọi tạm bằng `spawn_floating_text`.

```odin
import rl "vendor:raylib"
import "core:fmt"

// Lời khuyên: String sinh ra từ fmt.tprintf là cấp phát động, cần quản lý bộ nhớ.
// Trong Odin, nên sử dụng `context.temp_allocator` để lưu text nhằm tránh tràn RAM.

spawn_floating_text :: proc(victim_id: EntityID, text: string, color: rl.Color) {
    if victim_id not_in transforms do return
    pos := transforms[victim_id].position
    
    id := create_entity()
    
    // Bắt đầu từ đầu của nạn nhân, và ngẫu nhiên văng sang trái/phải 1 chút
    start_x := pos.x + f32(rl.GetRandomValue(-10, 10))
    start_y := pos.y - 20.0
    
    transforms[id] = TransformComponent{
        position = {start_x, start_y},
        size = {0, 0},
    }
    
    // Vận tốc văng vút lên trên (Trục Y âm)
    velocities[id] = VelocityComponent{
        vel = {0, -150.0},
        is_grounded = false,
    }
    
    // Copy chuỗi text bằng Arena hoặc Temp Allocator (Rất quan trọng trong Odin)
    // Để đơn giản hóa bài học, ta ép text ngọc nhỏ ở đây
    
    floating_texts[id] = FloatingTextComponent{
        text = text, // Cẩn thận Memory Leak nếu bạn không free nó sau này
        color = color,
        timer = 1.0, // Tồn tại đúng 1 giây
    }
}
```

## 3. Cập nhật và Vẽ (Render) Chữ

Tạo System dọn dẹp các con số hết tuổi thọ trong `ecs/systems.odin`:

```odin
system_floating_text :: proc(dt: f32) {
    for id in entities {
        if id not_in floating_texts do continue
        
        ft := &floating_texts[id]
        ft.timer -= dt
        
        // Càng về cuối chữ càng bay chậm lại (Giảm xóc)
        if id in velocities {
            v := &velocities[id]
            v.vel.y *= 0.9 // Ma sát không khí
        }
        
        // Hết tuổi thọ -> Bay màu
        if ft.timer <= 0 {
            // (Chú ý: Nếu ft.text cấp phát động thì phải free(ft.text) ở đây)
            destroy_entity(id)
        }
    }
}
```

Cuối cùng, ở vòng lặp Vẽ (Render Loop) trong `core/game.odin` (NHỚ ĐẶT BÊN TRONG CAMERA NHÉ!):

```odin
    // Trong hàm render_game(), đoạn nằm giữa BeginMode2D và EndMode2D
    for id in ecs.entities {
        if id not_in ecs.floating_texts do continue
        
        ft := ecs.floating_texts[id]
        pos := ecs.transforms[id].position
        
        // Fade out mờ dần theo thời gian (Tạo độ sang chảnh)
        alpha := u8((ft.timer / 1.0) * 255.0)
        c := ft.color
        c.a = alpha
        
        // Bạn có thể dùng Font tùy chỉnh, ở đây xài Default của Raylib
        rl.DrawText(rl.TextFormat("%s", ft.text), i32(pos.x), i32(pos.y), 20, c)
    }
```

> [!TIP]
> Việc tận dụng chung `VelocityComponent` và hệ thống Physics của Chương 1 cho các Dòng chữ (Floating Text) chính là quyền năng khủng khiếp của ECS. Hàng nghìn con số bay nhảy tuân theo vật lý một cách cực kỳ gọn nhẹ mà bạn không phải code thêm một lớp Vật Lý riêng cho UI!

Phần 3 (Quái Vật & Combat) đã kết thúc mỹ mãn! Sang **Phần 4: Trang bị & Đập đồ**, chúng ta sẽ đối mặt với linh hồn gây nghiện khét lẹt của NSO: Hành trang 50 ô chứa, Áo vải, Nhẫn Ngọc, và ông Thợ rèn đập đồ xịt lên xịt xuống.
