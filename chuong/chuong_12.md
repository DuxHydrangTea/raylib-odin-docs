# Chương 12: Kiến trúc ECS (Entity Component System)

Khi code game theo kiểu C++ truyền thống (OOP - Hướng đối tượng), bạn thường tạo ra một class `QuaiVat` kế thừa `NhanVat`, trong đó có chứa máu, tốc độ, hình ảnh, và một hàm `Update()`. Cách này rất nặng nề và khó bảo trì khi game phình to.

**ECS (Entity Component System)** là kiến trúc Data-Oriented (Hướng dữ liệu). Nó chia game thành 3 phần rạch ròi:
1. **Entity (Thực thể):** Chỉ là một con số ID (ví dụ: `ID = 1`). Nó không chứa dữ liệu gì cả.
2. **Component (Thành phần):** Các mảnh dữ liệu thuần túy. Ví dụ: `Position{x, y}`, `Health{hp}`, `Sprite{texture}`. Bạn dán các thẻ Component này vào Entity.
3. **System (Hệ thống):** Hàm logic đi tìm TẤT CẢ những Entity nào có các Component nhất định và xử lý chúng cùng 1 lúc.

Odin hỗ trợ mảng cấu trúc SoA (Structure of Arrays) cực mạnh để làm điều này.

---

## 1. Định nghĩa Data (Components)

```odin
package game
import rl "vendor:raylib"

// Các mảng song song chứa dữ liệu (SoA)
MAX_ENTITIES :: 1000

entities_active: [MAX_ENTITIES]bool
positions:       [MAX_ENTITIES]rl.Vector2
velocities:      [MAX_ENTITIES]rl.Vector2
healths:         [MAX_ENTITIES]f32
has_health:      [MAX_ENTITIES]bool // Đánh dấu Entity này có hệ thống Máu không
```

## 2. Tạo Thực thể (Entity)

Một con quái vật bây giờ chỉ là một chỉ số (index) kết nối các mảng dữ liệu với nhau.

```odin
spawn_monster :: proc(x, y: f32) {
    for i in 0..<MAX_ENTITIES {
        if !entities_active[i] { // Tìm ID trống
            entities_active[i] = true
            
            // Gắn Component Vị trí
            positions[i] = {x, y}
            velocities[i] = {-50, 0} // Đi sang trái
            
            // Gắn Component Máu
            has_health[i] = true
            healths[i] = 100
            
            return
        }
    }
}
```

## 3. Hệ thống xử lý (Systems)

Chúng ta không có hàm `monster.Update()`. Thay vào đó, chúng ta có một "Hệ thống Di chuyển" (Movement System) cập nhật TẤT CẢ mọi thứ biết di chuyển (người, quái, đạn).

```odin
// Hệ thống Di chuyển (Cập nhật hàng ngàn vật thể cùng lúc)
movement_system :: proc(dt: f32) {
    for i in 0..<MAX_ENTITIES {
        if entities_active[i] { // Nếu entity còn sống
            // Đọc và ghi dữ liệu trên các mảng liên tục, CPU sẽ chạy nhanh X10 lần!
            positions[i] += velocities[i] * dt
        }
    }
}

// Hệ thống Vẽ
render_system :: proc() {
    for i in 0..<MAX_ENTITIES {
        if entities_active[i] {
            rl.DrawCircleV(positions[i], 10, rl.RED)
            
            // Nếu entity này có máu, vẽ thanh máu trên đầu nó
            if has_health[i] {
                rl.DrawRectangle(c.int(positions[i].x) - 10, c.int(positions[i].y) - 20, c.int(healths[i]/100.0 * 20), 5, rl.GREEN)
            }
        }
    }
}
```

---

## 4. Tại sao lại dùng ECS?

1. **Linh hoạt tuyệt đối:** Bạn muốn một hòn đá có thể bị đánh vỡ? Chỉ cần `has_health[rock_id] = true`. Không cần sửa lại class `Rock` rườm rà.
2. **Siêu tốc độ (Cache Coherency):** CPU cực kỳ thích đọc dữ liệu từ mảng 1 chiều (như mảng `positions`). Việc duyệt mảng 1000 phần tử liên tục này nhanh hơn hàng chục lần so với việc con trỏ nhảy lung tung trong RAM để tìm class OOP.
3. **Rất hợp với Odin:** Ngôn ngữ Odin có cú pháp `#soa` giúp bạn viết ECS một cách ngắn gọn và thanh lịch hơn rất nhiều.
