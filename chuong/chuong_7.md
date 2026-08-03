# Chương 7: Kết xuất Ảo (RenderTexture) và Pixel-Perfect

Chào mừng bạn đến với phần Nâng cao! Trong chương này, chúng ta sẽ học kỹ thuật **RenderTexture**, một công cụ không thể thiếu đối với các tựa game Pixel Art hoặc khi bạn muốn tạo các hiệu ứng màn hình như rung lắc (Camera Shake) hay chia đôi màn hình (Split Screen).

---

## 1. RenderTexture2D là gì?

Thông thường, mọi thứ bạn vẽ (`Draw...`) sẽ được đẩy thẳng ra màn hình máy tính (gọi là Backbuffer). 

Với `RenderTexture2D`, bạn tạo ra một **khung tranh ảo** nằm ẩn trên Card Đồ Họa (GPU). Bạn sẽ vẽ toàn bộ game lên khung tranh ảo này trước. Sau đó, bạn lấy chính khung tranh ảo đó (dưới dạng một Texture) và vẽ nó ra màn hình thật.

### Tại sao lại làm thế?
Giả sử bạn làm một game Pixel Art có độ phân giải gốc cực nhỏ: `320 x 180` pixel.
Nếu bạn tạo cửa sổ `rl.InitWindow(320, 180)`, cửa sổ game sẽ bé tí tẹo bằng bao diêm trên màn hình máy tính 1080p. 
Giải pháp: 
1. Khởi tạo cửa sổ to: `1280 x 720`.
2. Tạo một RenderTexture nhỏ: `320 x 180`.
3. Vẽ mọi thứ lên bản nhỏ.
4. Phóng to bản nhỏ đó gấp 4 lần rồi in lên cửa sổ to!

---

## 2. Cách sử dụng RenderTexture

### Khởi tạo và Dọn dẹp
Giống hệt như Texture bình thường, bạn phải tải nó trước vòng lặp và dọn dẹp nó.

```odin
// Độ phân giải gốc của game (Canvas ảo)
VIRTUAL_WIDTH :: 320
VIRTUAL_HEIGHT :: 180

// Khởi tạo Canvas ảo
canvas := rl.LoadRenderTexture(VIRTUAL_WIDTH, VIRTUAL_HEIGHT)
defer rl.UnloadRenderTexture(canvas)
```

### Sử dụng trong vòng lặp Game

Bước này có một **LƯU Ý CỰC KỲ QUAN TRỌNG**: Khi bạn lấy hình ảnh từ `RenderTexture` để vẽ ra màn hình thực, ảnh sẽ **BỊ LẬT NGƯỢC (Upside Down)** do cơ chế hệ tọa độ của OpenGL. Để giải quyết, chúng ta phải truyền chiều cao âm (`-height`) khi vẽ nó.

```odin
for !rl.WindowShouldClose() {
    
    // --- 1. VẼ LÊN CANVAS ẢO ---
    rl.BeginTextureMode(canvas)
        rl.ClearBackground(rl.BLACK)
        
        // Vẽ nhân vật, map, UI... ở độ phân giải 320x180
        rl.DrawRectangle(10, 10, 20, 20, rl.RED)
        
    rl.EndTextureMode() // Kết thúc vẽ ảo


    // --- 2. VẼ CANVAS ẢO RA MÀN HÌNH THỰC ---
    rl.BeginDrawing()
        rl.ClearBackground(rl.DARKGRAY) // Viền đen ngoài màn hình (nếu có)
        
        // Trích xuất Texture từ Canvas
        canvas_tex := canvas.texture
        
        // HÌNH CHỮ NHẬT CẮT (Lưu ý chiều cao bị ĐẢO NGƯỢC: -VIRTUAL_HEIGHT)
        source_rec := rl.Rectangle{0, 0, f32(canvas_tex.width), -f32(canvas_tex.height)}
        
        // HÌNH CHỮ NHẬT ĐÍCH ĐẾN (Phóng to vừa màn hình 1280x720)
        dest_rec := rl.Rectangle{0, 0, f32(WINDOW_WIDTH), f32(WINDOW_HEIGHT)}
        
        // Vẽ Canvas lên màn hình thực
        rl.DrawTexturePro(canvas_tex, source_rec, dest_rec, {0,0}, 0.0, rl.WHITE)
        
    rl.EndDrawing()
}
```

---

## 3. Các Ứng dụng khác của RenderTexture

* **Bản đồ con (Minimap):** Vẽ thế giới 1 lần nữa nhưng thu nhỏ lại, lưu vào `RenderTexture`, sau đó vẽ cục Texture đó ở góc phải màn hình của người chơi.
* **Camera Shake (Rung lắc):** Khi vẽ `canvas_tex` ra màn hình thực ở bước 2, thay vì vẽ ở toạ độ `{0, 0}`, bạn cộng thêm một lượng bù trừ ngẫu nhiên `offsetX, offsetY` (từ -5 đến 5 pixel). Màn hình sẽ rung lên bần bật khi có vụ nổ!
* **Gương phản chiếu / Nước:** Vẽ thế giới lộn ngược vào `RenderTexture` rồi áp dụng Shader bóp méo (Distortion) lên nó.

---

## Bài Tập Thực Hành

1. Hãy sửa dự án `thuchanh` của bạn: Đặt `WINDOW_WIDTH = 1280` nhưng khởi tạo một `RenderTexture` kích thước `320 x 180`.
2. Vẽ một hình tròn nhỏ ở góc màn hình ảo.
3. Phóng to khung hình ảo ra màn hình 1280x720. Đừng quên **lật ngược trục Y** ở `source_rec` nhé! 
*(Bạn sẽ thấy hình tròn bị răng cưa, đó chính xác là hiệu ứng Pixel Art cổ điển!)*
