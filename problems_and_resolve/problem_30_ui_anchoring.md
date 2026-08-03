# Vấn Đề 30: UI văng khỏi màn hình (Multi-resolution UI Anchoring)

**Vấn đề:**
Bản đồ thu nhỏ (Minimap) của bạn được vẽ ở tọa độ `(X=1000, Y=20)`. Rất đẹp trên màn hình Laptop 1280x720. 
Nhưng khi gửi game cho một Streamer dùng màn hình Ultrawide 21:9 (Độ phân giải 2560x1080), cái Minimap lại nằm lơ lửng ngay giữa màn hình thay vì nằm gọn ở góc phải trên.

**Nguyên nhân:**
UI của bạn bị hard-code bằng Tọa độ Tuyệt đối (Absolute Coodinates). Tọa độ X=1000 là góc phải của màn hình 1280, nhưng lại là khu vực trung tâm của màn hình 2560.

**Giải pháp (Mỏ neo - Anchoring):**
Tính toán tọa độ UI dựa trên % hoặc các góc cạnh của kích thước Cửa sổ hiện tại.

```odin
// Lấy độ phân giải động
w := f32(rl.GetScreenWidth())
h := f32(rl.GetScreenHeight())

// Vẽ Avatar ở Góc trên Bên trái (Luôn luôn 20x20)
rl.DrawTexture(avatar, 20, 20, rl.WHITE)

// Vẽ Minimap ở Góc trên Bên Phải (Mỏ neo Right-Top)
map_width: f32 = 200.0
// Tọa độ X = Cạnh phải màn hình (w) trừ đi kích thước Map, lùi vô 20px
rl.DrawTexture(minimap, i32(w - map_width - 20), 20, rl.WHITE)

// Vẽ Thanh Kỹ Năng ở Giữa Màn Hình Dưới (Mỏ neo Bottom-Center)
skill_width: f32 = 400.0
rl.DrawTexture(skillbar, i32((w - skill_width) / 2.0), i32(h - 60), rl.WHITE)
```
*Nhờ dùng Anchor, UI game của bạn sẽ tự động bám dính vào các cạnh màn hình một cách hoàn hảo, hỗ trợ từ màn vuông tỉ lệ 4:3 cho tới màn siêu rộng 21:9.*
