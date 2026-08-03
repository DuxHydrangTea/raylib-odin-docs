# Vấn Đề 3: Méo hình khi Resize (Resolution Scaling)

**Vấn đề:**
Khi người dùng thu nhỏ cửa sổ game hoặc phóng to toàn màn hình, thanh máu bị bóp dẹp, UI bị lộn xộn, nhân vật bị mờ.

**Nguyên nhân:**
Bạn vẽ trực tiếp mọi thứ lên cửa sổ với tọa độ cứng (vd: `X = 500`). Khi cửa sổ co lại còn 400 pixel, vật thể đó sẽ nằm ngoài màn hình hoặc bị Engine ép nhỏ lại sai tỷ lệ.

**Giải pháp:**
Giữ nguyên độ phân giải gốc của game (Ví dụ: `1920x1080`), và vẽ toàn bộ game vào một **RenderTexture ảo** (Chương 7). Sau đó, khi vẽ RenderTexture ra màn hình thực, hãy tính toán hộp thư (Letterboxing) để giữ nguyên tỷ lệ khung hình (Aspect Ratio), chấp nhận có viền đen ở hai bên hoặc trên dưới.

```odin
// Tính toán kích thước để vẽ không bị méo
scale := min(
    f32(window_width) / f32(VIRTUAL_WIDTH),
    f32(window_height) / f32(VIRTUAL_HEIGHT)
)

dest_width := f32(VIRTUAL_WIDTH) * scale
dest_height := f32(VIRTUAL_HEIGHT) * scale

// Tính khoảng trống viền đen để căn giữa
offset_x := (f32(window_width) - dest_width) / 2.0
offset_y := (f32(window_height) - dest_height) / 2.0

// Vẽ từ Canvas ảo ra màn hình thật
dest_rec := rl.Rectangle{offset_x, offset_y, dest_width, dest_height}
rl.DrawTexturePro(canvas.texture, source_rec, dest_rec, {0,0}, 0.0, rl.WHITE)
```
