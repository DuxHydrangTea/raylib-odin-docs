# Dự Án Tốt Nghiệp: Sinh Tồn
## Phần 5: Game Juice, Shaders & Biên dịch WASM

Mọi logic đã xong. Bây giờ là 50% khối lượng công việc quyết định game của bạn là "siêu phẩm" hay "game sinh viên rác". 

*(Kỹ năng áp dụng: Chương 7, Chương 18, Chương 19, Chương 20)*

---

### 1. Game Feel: Rung màn hình (Screen Shake) & Khựng (Hit Stop)

* **Screen Shake:** Khi bị quái cắn, màn hình phải rung bần bật.
* **Hit Stop:** Khi đạn nổ trúng nhiều quái, game phải "khựng" lại 2 khung hình để tạo uy lực.

```odin
shake_timer: f32 = 0.0
hit_stop_frames: int = 0

// KHI BỊ QUÁI CẮN:
shake_timer = 0.3 // Rung trong 0.3s

// KHI BẮN TRÚNG ĐÍCH (Uy lực mạnh):
hit_stop_frames = 2 // Đứng hình 2 frame

// ------------------------------------
// BÊN TRONG GAME LOOP (Phần Update)
if hit_stop_frames > 0 {
    hit_stop_frames -= 1
    // LƯU Ý: Lệnh return hoặc bỏ qua toàn bộ Update quái, đạn ở frame này
} else {
    // Cập nhật quái, đạn, người chơi như bình thường
}

// Cập nhật Camera Shake
cam_offset := rl.Vector2{WINDOW_WIDTH/2, WINDOW_HEIGHT/2} // Mặc định
if shake_timer > 0 {
    shake_timer -= dt
    // Cộng thêm nhiễu ngẫu nhiên
    cam_offset.x += f32(rl.GetRandomValue(-10, 10))
    cam_offset.y += f32(rl.GetRandomValue(-10, 10))
}
camera.offset = cam_offset
```

### 2. Shaders: Nhấp nháy đỏ khi sắp chết

Thay vì chỉnh màu toàn bộ game bằng Code, ta dùng Shader để bao phủ màng đỏ (Vignette) quanh màn hình khi HP thấp (Chương 8).

```odin
damage_shader := rl.LoadShader(nil, "assets/vignette.fs")
// ...
rl.BeginShaderMode(damage_shader)
    // Cung cấp máu cho Shader
    hp_ratio := player_hp / max_hp
    rl.SetShaderValue(damage_shader, hp_loc, &hp_ratio, .FLOAT)
    
    // Shader sẽ tự biến viền màn hình thành màu đỏ nếu máu dưới 20%
    
    // (Vẽ toàn bộ Camera Game ở trong này bằng RenderTexture - Chương 7)
rl.EndShaderMode()
```

### 3. Tối ưu hoá (Profiling) bằng Spatial Grid

Bạn nhận ra game chỉ spawn được 1000 quái. Lên 5000 quái FPS rớt thê thảm do hàm "Tách bầy" duyệt O(N^2).
Bạn có thể tự tìm hiểu thuật toán **Spatial Hashing**: Chia bản đồ thành các ô 64x64. Quái ở ô nào thì chỉ kiểm tra va chạm với quái/đạn ở cùng ô đó và 8 ô lân cận. Tính toán giảm từ 25 triệu phép tính xuống còn 10,000! (FPS lại kịch trần 60).

### 4. Bước Cuối Cùng: Tỏa sáng trên Trình duyệt!

Đừng đưa file `.exe` cho bạn bè. Hãy biên dịch game ra WebAssembly (WASM).

1. Bạn cài đặt `Emscripten` theo [hướng dẫn trên mạng](https://emscripten.org/docs/getting_started/downloads.html).
2. Viết lại cấu trúc vòng lặp Game Loop để hàm `main` không còn `while` nữa, mà tạo một proc `UpdateDrawFrame()` riêng.
3. Chạy lệnh:
   ```bash
   odin build . -target:freestanding_wasm32 -build-mode:obj
   emcc game.o -s USE_GLFW=3 -o index.html
   ```
4. Đẩy file `index.html` và thư mục `assets/` lên Github Pages hoặc Itch.io.

### 🏆 LỜI TỔNG KẾT

Bạn đã bắt đầu từ một cửa sổ màn hình đen xì, và kết thúc bằng một siêu phẩm hành động nghẹt thở chạy mượt mà ngay trên Trình duyệt web với hàng ngàn Entity, Shaders chói lòa và kiến trúc đỉnh cao.

**Bạn đã chính thức tốt nghiệp Khóa Lập Trình Game 2D với Odin và Raylib. Thế giới ảo giờ nằm trong tay bạn!**
