# Vấn Đề 5: Đi chéo bị nhanh hơn (Diagonal Movement)

**Vấn đề:**
Trong game Top-down, nhân vật chạy với tốc độ 100 pixel/s. Nhưng khi người chơi bấm đồng thời 2 phím (Đi Lên + Đi Phải), nhân vật chạy nhanh hơn hẳn (Tốc độ thực tế lên tới 141 pixel/s).

**Nguyên nhân:**
Lỗi toán học cơ bản (Định lý Pytago). Vector vận tốc của bạn là `X = 100`, `Y = -100`. Chiều dài của Vector này là căn bậc 2 của (100^2 + (-100)^2) = 141.42.

**Giải pháp:**
Khi nhận input từ người chơi, tạo ra một Vector Chỉ Hướng (Direction Vector). Sau đó, bạn phải **Bình thường hóa (Normalize)** nó để chiều dài luôn luôn bằng 1, rồi mới nhân với tốc độ.

```odin
dir := rl.Vector2{0, 0}

if rl.IsKeyDown(.W) { dir.y -= 1 }
if rl.IsKeyDown(.S) { dir.y += 1 }
if rl.IsKeyDown(.A) { dir.x -= 1 }
if rl.IsKeyDown(.D) { dir.x += 1 }

// KHI ĐI CHÉO, VectorLength(dir) sẽ là 1.414, ta phải Normalize nó về 1
if rl.Vector2Length(dir) > 0 {
    dir = rl.Vector2Normalize(dir)
}

// Giờ thì dù đi chéo hay thẳng, tốc độ vẫn chuẩn 100%
player.pos += dir * speed * dt
```
