# Chương 4: Đồ họa chất lượng cao và Giao diện (UI)

Chào mừng bạn đến với Chương 4! Thay vì chỉ vẽ những hình khối cơ bản (vuông, tròn), ở chương này chúng ta sẽ nhập (import) đồ họa thực thụ: Các tệp hình ảnh (`.png`), hiển thị chữ viết với phông chữ đẹp (`.ttf`), và cách cắt ảnh từ một SpriteSheet (tấm ảnh chứa nhiều khung hình hoạt ảnh).

---

## 1. Kết xuất Hình ảnh (Texture trên GPU)

Trong Raylib 2D, chúng ta vẽ hình bằng cấu trúc `Texture2D`. Dữ liệu này nằm trực tiếp trên VRAM của Card Đồ Hoạ nên tốc độ vẽ ra màn hình là cực kỳ nhanh.

### 1.1 Tải và Dọn dẹp
* **`LoadTexture(fileName: cstring) -> Texture2D`**
  * Tác dụng: Đọc file ảnh từ máy tính (`.png`, `.jpg`) và đẩy thẳng lên GPU.
  * Lưu ý: Gọi hàm này ở **ngoài** Vòng lặp Game (trước lệnh `for`). Đừng bao giờ LoadTexture liên tục bên trong vòng lặp!
* **`UnloadTexture(texture: Texture2D)`**
  * Tác dụng: Xóa ảnh khỏi VRAM. Phải nhớ dùng `defer` ngay sau khi load để tránh thất thoát RAM (Memory Leak).

```odin
// Ví dụ
player_tex := rl.LoadTexture("assets/hero.png")
defer rl.UnloadTexture(player_tex)
```

### 1.2 Vẽ Texture ra màn hình
* **`DrawTexture(texture: Texture2D, posX, posY: c.int, tint: Color)`**
  * Tác dụng: Vẽ ảnh với kích thước 1:1, không thể xoay hay phóng to. `tint` là màu màng lọc (dùng `rl.WHITE` để giữ nguyên màu gốc).
* **`DrawTextureEx(texture: Texture2D, position: Vector2, rotation: f32, scale: f32, tint: Color)`**
  * Tác dụng: Dùng khi cần vẽ ảnh to/nhỏ hơn (`scale`) và có thể xoay (`rotation`).
* **`SetTextureFilter(texture: Texture2D, filter: TextureFilter)`**
  * Tác dụng: Nếu bạn làm game Pixel Art và muốn phóng to ảnh lên 4-5 lần mà không bị mờ (nhòe), bạn bắt buộc phải gọi `rl.SetTextureFilter(tex, .POINT)` ngay sau khi load.

---

## 2. Animation và Cắt Khung Hình (SpriteSheet)

Các game 2D hiếm khi lưu mỗi khung hình nhân vật chạy thành 1 file ảnh riêng lẻ. Thay vào đó, chúng được ghép vào một file ảnh lớn gọi là **SpriteSheet**.

* **`DrawTextureRec(texture: Texture2D, source: Rectangle, position: Vector2, tint: Color)`**
  * Tác dụng: Thay vì vẽ cả tấm ảnh, hàm này chỉ "cắt" lấy một hình chữ nhật (`source`) trên ảnh gốc và vẽ nó lên màn hình tại toạ độ `position`.
  * Thay đổi `source.x` sau mỗi khoảng thời gian để tạo ra hoạt ảnh (Animation) chuyển động!

* **`DrawTexturePro(texture: Texture2D, source, dest: Rectangle, origin: Vector2, rotation: f32, tint: Color)`**
  * Tác dụng: Đây là hàm vẽ mạnh nhất. Nó cho phép bạn vừa **cắt (source)**, vừa **phóng to/đặt toạ độ (dest)**, và xoay quanh một **điểm tâm (origin)**.
  * **Bí kíp lật hình:** Để làm nhân vật quay mặt sang trái/phải, bạn không cần 2 file ảnh. Hãy thay đổi `source.width` thành số âm (VD: `-32.0`), ảnh sẽ tự động bị lật ngang (Flip Horizontal)!

---

## 3. Văn bản và Phông chữ (Fonts)

Mặc dù `DrawText` dễ dùng, nhưng nó chỉ hỗ trợ phông chữ pixel nhỏ bé mặc định của Raylib và **không hỗ trợ Tiếng Việt**. Để làm UI chuyên nghiệp, bạn phải dùng Font riêng.

* **`LoadFontEx(fileName: cstring, fontSize: c.int, codepoints: [^]rune, codepointCount: c.int) -> Font`**
  * Tác dụng: Tải phông `.ttf`. Đối với Tiếng Việt, bạn KHÔNG THỂ dùng `LoadFont()` thông thường vì nó không nạp các kí tự như `ă, ơ, ê` vào GPU. Bắt buộc dùng `LoadFontEx` nếu muốn hiển thị tiếng Việt. (Phải truyền danh sách các ký tự cần load).
  * Đừng quên `defer rl.UnloadFont(myFont)`.

* **`DrawTextEx(font: Font, text: cstring, position: Vector2, fontSize: f32, spacing: f32, tint: Color)`**
  * Tác dụng: Dùng Font bạn vừa load để hiển thị chữ. Có thể chỉnh kích thước và khoảng cách giữa các chữ (`spacing`).

* **`MeasureTextEx(font: Font, text: cstring, fontSize: f32, spacing: f32) -> Vector2`**
  * Tác dụng: Trả về chiều rộng và chiều cao của đoạn văn bản đó trên màn hình (Bao nhiêu pixel).
  * Ứng dụng: Dùng để căn giữa (Center-align) đoạn văn bản vào giữa màn hình hoặc giữa nút bấm. `X_mới = ScreenWidth/2 - TextWidth/2`.

---

## 4. Ảnh RAM tĩnh (Image) - Nâng cao

Bạn cần phân biệt `Texture2D` (trên GPU) và `Image` (trên CPU/RAM).
* Texture dùng để **VẼ**.
* Image dùng để **ĐỌC DỮ LIỆU PIXEL**. Bạn không thể vẽ Image trực tiếp.

* **Sinh bản đồ ngẫu nhiên:** Hàm `GenImagePerlinNoise()` giúp sinh ra một bức ảnh có các vùng xám ngẫu nhiên trông giống hệt như đồi núi, sông hồ.
* Bạn có thể quét qua bức ảnh `Image` này, gọi hàm `GetImageColor(x, y)` để đọc màu. Ví dụ: Nếu màu là xanh lam -> Đặt 1 cục đất là nước, nếu là xanh lá -> Đặt cỏ. (Rất hợp để làm game như Terraria hay Minecraft).
* Sau khi xử lý xong, gọi `LoadTextureFromImage()` để chuyển Image thành Texture và dọn dẹp biến Image cũ.

---

## Bài tập thực hành Chương 4

*(Bài này yêu cầu bạn tải sẵn 1 file ảnh PNG bất kỳ trên mạng để thực hành)*
1. Tải ảnh vào biến bằng `LoadTexture` (và `defer Unload`).
2. Dùng `DrawTexture` để vẽ nó ra giữa màn hình.
3. Dùng `DrawTexturePro` để vẽ lại hình ảnh đó, nhưng lần này phóng to nó lên gấp đôi, và liên tục xoay vòng tròn quanh tâm của nó (Sử dụng biến `rotation` tăng dần theo thời gian).
4. Viết lên màn hình dòng chữ "Texture đã được tải thành công" bằng `DrawText` với màu đen (Nhớ kết hợp với `temp_allocator` và C-String ở Chương 1 nhé).
