# Tài liệu Raylib Odin - Tổng hợp Toàn bộ Hàm 2D

Dưới đây là danh sách liệt kê **từng hàm một** liên quan đến lập trình đồ họa 2D (bao gồm hệ thống, cửa sổ, vẽ hình, xử lý ảnh, chữ viết và đầu vào) trong `vendor:raylib`. (Đã loại trừ hoàn toàn các hàm 3D, Audio, và VR).

---

## 1. QUẢN LÝ CỬA SỔ & HỆ THỐNG (Window-related functions)

**`InitWindow(width, height: c.int, title: cstring)`**
* **Tham số:** `width` (Chiều rộng), `height` (Chiều cao), `title` (Tiêu đề).
* **Tác dụng:** Khởi tạo cửa sổ game và context đồ hoạ OpenGL.
* **Cách dùng:** `rl.InitWindow(800, 600, "Tên Game")`
* **Lưu ý:** Bắt buộc gọi đầu tiên trước khi dùng bất kì hàm vẽ hay load ảnh/âm thanh nào.

**`WindowShouldClose() -> bool`**
* **Tham số:** (Không có)
* **Tác dụng:** Trả về true nếu người dùng bấm dấu X hoặc phím ESC để đóng cửa sổ.
* **Cách dùng:** `for !rl.WindowShouldClose() { ... }` (Dùng làm điều kiện vòng lặp chính).
* **Lưu ý:** Mặc định phím ESC sẽ làm hàm này trả về true. Đổi phím thoát bằng `SetExitKey()`.

**`CloseWindow()`**
* **Tham số:** (Không có)
* **Tác dụng:** Đóng cửa sổ và giải phóng toàn bộ tài nguyên.
* **Cách dùng:** `rl.CloseWindow()`
* **Lưu ý:** Chỉ gọi 1 lần khi kết thúc game.

**`IsWindowReady() -> bool`**
* **Tham số:** (Không có)
* **Tác dụng:** Kiểm tra xem cửa sổ đã được khởi tạo và sẵn sàng chưa.
* **Cách dùng:** `if rl.IsWindowReady() { ... }`

**`IsWindowFullscreen() -> bool`**
* **Tham số:** (Không có)
* **Tác dụng:** Kiểm tra xem cửa sổ có đang ở chế độ toàn màn hình không.
* **Cách dùng:** `if rl.IsWindowFullscreen() { ... }`

**`IsWindowHidden() -> bool`**
* **Tham số:** (Không có)
* **Tác dụng:** Kiểm tra xem cửa sổ có đang bị ẩn không.
* **Cách dùng:** `if rl.IsWindowHidden() { ... }`

**`IsWindowMinimized() -> bool`**
* **Tham số:** (Không có)
* **Tác dụng:** Kiểm tra xem cửa sổ có đang bị thu nhỏ không.
* **Cách dùng:** `if rl.IsWindowMinimized() { ... }`
* **Lưu ý:** Game nên tạm dừng (pause) update khi thu nhỏ để đỡ tốn CPU.

**`IsWindowMaximized() -> bool`**
* **Tham số:** (Không có)
* **Tác dụng:** Kiểm tra xem cửa sổ có đang phóng to hết cỡ không.
* **Cách dùng:** `if rl.IsWindowMaximized() { ... }`

**`IsWindowFocused() -> bool`**
* **Tham số:** (Không có)
* **Tác dụng:** Kiểm tra xem cửa sổ có đang được người dùng focus vào không.
* **Cách dùng:** `if !rl.IsWindowFocused() { pauseGame() }`

**`IsWindowResized() -> bool`**
* **Tham số:** (Không có)
* **Tác dụng:** Kiểm tra xem cửa sổ có vừa bị đổi kích thước trong frame hiện tại không.
* **Cách dùng:** `if rl.IsWindowResized() { capNhatGiaoDien() }`

**`IsWindowState(flags: ConfigFlags) -> bool`**
* **Tham số:** `flags` (Các cờ trạng thái).
* **Tác dụng:** Kiểm tra một trạng thái cụ thể có đang bật không.
* **Cách dùng:** `if rl.IsWindowState({.WINDOW_RESIZABLE}) { ... }`

**`SetWindowState(flags: ConfigFlags)`**
* **Tham số:** `flags` (Cờ trạng thái).
* **Tác dụng:** Kích hoạt cấu hình trạng thái.
* **Cách dùng:** `rl.SetWindowState({.WINDOW_RESIZABLE, .VSYNC_HINT})`

**`ClearWindowState(flags: ConfigFlags)`**
* **Tham số:** `flags` (Cờ trạng thái).
* **Tác dụng:** Xóa/Tắt cấu hình trạng thái của cửa sổ.
* **Cách dùng:** `rl.ClearWindowState({.WINDOW_RESIZABLE})`

**`ToggleFullscreen()`**
* **Tham số:** (Không có)
* **Tác dụng:** Chuyển qua lại giữa toàn màn hình và cửa sổ.
* **Cách dùng:** `if rl.IsKeyPressed(.F11) { rl.ToggleFullscreen() }`

**`ToggleBorderlessWindowed()`**
* **Tham số:** (Không có)
* **Tác dụng:** Chuyển sang chế độ cửa sổ không viền.
* **Cách dùng:** `rl.ToggleBorderlessWindowed()`

**`MaximizeWindow()`** / **`MinimizeWindow()`** / **`RestoreWindow()`**
* **Tác dụng:** Phóng to / Thu nhỏ / Phục hồi cửa sổ.
* **Cách dùng:** `rl.MaximizeWindow()`

**`SetWindowIcon(image: Image)`**
* **Tham số:** `image` (Hình ảnh tải trên RAM).
* **Tác dụng:** Cài đặt biểu tượng cho cửa sổ game.
* **Cách dùng:** 
  ```odin
  icon := rl.LoadImage("icon.png")
  rl.SetWindowIcon(icon)
  rl.UnloadImage(icon)
  ```

**`SetWindowIcons(images: [^]Image, count: c.int)`**
* **Tham số:** Mảng hình ảnh và số lượng.
* **Tác dụng:** Cài nhiều kích thước icon.
* **Cách dùng:** `rl.SetWindowIcons(raw_data(icons_array), 3)`

**`SetWindowTitle(title: cstring)`**
* **Tham số:** `title` (Tên tiêu đề).
* **Tác dụng:** Thay đổi tiêu đề cửa sổ ngay cả khi game đang chạy.
* **Cách dùng:** `rl.SetWindowTitle("Điểm hiện tại: 100")`

**`SetWindowPosition(x, y: c.int)`**
* **Tham số:** `x`, `y` (Tọa độ trên desktop).
* **Tác dụng:** Đặt vị trí cửa sổ.
* **Cách dùng:** `rl.SetWindowPosition(100, 100)`

**`SetWindowMonitor(monitor: c.int)`**
* **Tham số:** `monitor` (ID màn hình).
* **Tác dụng:** Đưa cửa sổ sang màn hình khác.
* **Cách dùng:** `rl.SetWindowMonitor(1)`

**`SetWindowMinSize(width, height: c.int)`** / **`SetWindowMaxSize(width, height: c.int)`**
* **Tác dụng:** Giới hạn kích thước khi người dùng kéo viền cửa sổ.
* **Cách dùng:** `rl.SetWindowMinSize(800, 600)`

**`SetWindowSize(width, height: c.int)`**
* **Tác dụng:** Thay đổi kích thước trực tiếp.
* **Cách dùng:** `rl.SetWindowSize(1280, 720)`

**`SetWindowOpacity(opacity: f32)`**
* **Tham số:** `opacity` (Độ trong suốt 0.0 - 1.0).
* **Tác dụng:** Làm cửa sổ game trong suốt.
* **Cách dùng:** `rl.SetWindowOpacity(0.8)`

**`SetWindowFocused()`**
* **Tác dụng:** Kéo cửa sổ game lên trên cùng.
* **Cách dùng:** `rl.SetWindowFocused()`

**`GetWindowHandle() -> rawptr`**
* **Tác dụng:** Lấy con trỏ gốc. Dùng khi cần tích hợp thư viện Windows API/X11.

**`GetScreenWidth() -> c.int`** / **`GetScreenHeight() -> c.int`**
* **Tác dụng:** Lấy kích thước logic của vùng vẽ.
* **Cách dùng:** `w := rl.GetScreenWidth()`
* **Lưu ý:** Liên tục gọi hàm này để cập nhật GUI (tránh dùng số tĩnh nếu cửa sổ đổi kích thước).

**`GetRenderWidth() -> c.int`** / **`GetRenderHeight() -> c.int`**
* **Tác dụng:** Kích thước thực (có tính HighDPI, màn hình Retina).

**`GetMonitorCount() -> c.int`**
* **Tác dụng:** Lấy số lượng màn hình đang cắm.
* **Cách dùng:** `num_monitors := rl.GetMonitorCount()`

**`GetCurrentMonitor() -> c.int`**
* **Tác dụng:** Lấy ID màn hình đang chứa game.
* **Cách dùng:** `mon_id := rl.GetCurrentMonitor()`

**`GetMonitorPosition(...)`, `GetMonitorWidth(...)`, `GetMonitorHeight(...)`**
* **Tác dụng:** Lấy toạ độ / kích thước màn hình theo ID.

**`GetMonitorRefreshRate(monitor: c.int) -> c.int`**
* **Tác dụng:** Tần số quét (Hz).
* **Cách dùng:** `hz := rl.GetMonitorRefreshRate(0)`
* **Lưu ý:** Dùng để set FPS limit: `rl.SetTargetFPS(hz)`

**`GetWindowPosition() -> Vector2`** / **`GetWindowScaleDPI() -> Vector2`**
* **Tác dụng:** Toạ độ cửa sổ / Hệ số scale (HighDPI).

**`GetMonitorName(monitor: c.int) -> cstring`**
* **Tác dụng:** Tên màn hình.

**`SetClipboardText(text: cstring)`** / **`GetClipboardText() -> cstring`**
* **Tác dụng:** Copy/Paste vào clipboard HĐH.
* **Cách dùng:** `rl.SetClipboardText("Cheat Code 123")`

**`EnableEventWaiting()`** / **`DisableEventWaiting()`**
* **Tác dụng:** Chế độ vẽ khi có sự kiện (như dùng trong App không phải game).
* **Lưu ý:** Trong game KHÔNG nên gọi hàm này vì game cần chạy ở 60FPS liên tục.

---

## 2. QUẢN LÝ CON TRỎ CHUỘT (Cursor-related functions)

**`ShowCursor()`** / **`HideCursor()`**
* **Tác dụng:** Hiện/Ẩn con trỏ chuột.
* **Cách dùng:** `rl.HideCursor()` (khi vẽ chuột custom).

**`IsCursorHidden() -> bool`**
* **Tác dụng:** Kiểm tra trạng thái ẩn chuột.

**`EnableCursor()`** / **`DisableCursor()`**
* **Tác dụng:** Khoá/Mở khoá con trỏ ở giữa màn hình (dành cho game FPS hoặc look camera).
* **Cách dùng:** `rl.DisableCursor()` (chuột sẽ bị giam).

**`IsCursorOnScreen() -> bool`**
* **Tác dụng:** Kiểm tra chuột có nằm trong cửa sổ game không.
* **Cách dùng:** `if rl.IsCursorOnScreen() { banSung() }`

---

## 3. VÒNG LẶP VẼ & RENDER (Drawing-related functions)

**`ClearBackground(color: Color)`**
* **Tham số:** `color` (Màu).
* **Tác dụng:** Xóa toàn màn hình bằng một màu nền.
* **Cách dùng:** `rl.ClearBackground(rl.RAYWHITE)`
* **Lưu ý:** Phải gọi hàm này CẦN THIẾT ở đầu mỗi frame (trong BeginDrawing) để tránh hiện tượng bóng mờ (ghosting) do frame trước còn lưu lại.

**`BeginDrawing()`**
* **Tác dụng:** Setup hệ thống để bắt đầu gửi lệnh vẽ.
* **Cách dùng:** `rl.BeginDrawing()`

**`EndDrawing()`**
* **Tác dụng:** Kết thúc lệnh vẽ và đưa hình ảnh lên màn hình (Swap buffer).
* **Cách dùng:** `rl.EndDrawing()`
* **Lưu ý:** Bất kì hàm vẽ hình hay vẽ chữ nào cũng bắt buộc phải nằm giữa `BeginDrawing()` và `EndDrawing()`.

**`BeginMode2D(camera: Camera2D)`**
* **Tham số:** `camera` (Camera 2D chứa offset, target, zoom, rotation).
* **Tác dụng:** Bắt đầu chế độ vẽ qua góc nhìn của Camera.
* **Cách dùng:** `rl.BeginMode2D(camera)`
* **Lưu ý:** Giống BeginDrawing, nhưng các toạ độ vẽ sau đó sẽ thuộc hệ quy chiếu của thế giới (World Space).

**`EndMode2D()`**
* **Tác dụng:** Kết thúc chế độ vẽ bằng Camera.
* **Cách dùng:** `rl.EndMode2D()`

**`BeginTextureMode(target: RenderTexture2D)`** / **`EndTextureMode()`**
* **Tác dụng:** Chuyển việc vẽ hình lên một Render Texture thay vì vẽ ra màn hình.
* **Lưu ý:** Rất hữu ích để vẽ map, hoặc làm các hiệu ứng post-processing. Khi vẽ lên RenderTexture thì Texture đó sẽ bị lật ngược trục Y, nhớ lưu ý khi vẽ nó ra lại màn hình.

**`BeginShaderMode(shader: Shader)`** / **`EndShaderMode()`**
* **Tác dụng:** Bắt đầu áp dụng Shader tuỳ chỉnh.
* **Cách dùng:** `rl.BeginShaderMode(my_shader)`

**`BeginBlendMode(mode: BlendMode)`** / **`EndBlendMode()`**
* **Tác dụng:** Bắt đầu chế độ hòa trộn màu (Blend Mode).
* **Cách dùng:** `rl.BeginBlendMode(.ADDITIVE)` (Dùng vẽ ánh sáng, tia lửa điện).

**`BeginScissorMode(x, y, width, height: c.int)`** / **`EndScissorMode()`**
* **Tác dụng:** Cắt xén (clip) tất cả các nét vẽ nằm ngoài vùng chữ nhật này.
* **Cách dùng:** Dùng làm ScrollView trong UI. Chỉ vẽ phần tử nằm lọt trong khung (khung nhìn).

---

## 4. TỌA ĐỘ MÀN HÌNH & THẾ GIỚI 2D (Screen-space-related)

**`GetWorldToScreen2D(position: Vector2, camera: Camera2D) -> Vector2`**
* **Tham số:** `position` (Tọa độ trong thế giới), `camera` (Camera đang dùng).
* **Tác dụng:** Biến đổi tọa độ của thế giới ảo thành tọa độ pixel thực trên màn hình.
* **Cách dùng:** `screen_pos := rl.GetWorldToScreen2D(player.pos, camera)`

**`GetScreenToWorld2D(position: Vector2, camera: Camera2D) -> Vector2`**
* **Tác dụng:** Biến đổi tọa độ màn hình thành tọa độ trong thế giới ảo.
* **Cách dùng:** `world_mouse := rl.GetScreenToWorld2D(rl.GetMousePosition(), camera)` (Dùng để biết click chuột vào viên gạch nào trong map).

**`GetCameraMatrix2D(camera: Camera2D) -> Matrix`**
* **Tác dụng:** Lấy ma trận biến đổi của Camera 2D (Dùng khi viết Shader hoặc tính toán ma trận tuỳ chỉnh).

---

## 5. THỜI GIAN & FPS (Timing-related functions)

**`SetTargetFPS(fps: c.int)`**
* **Tham số:** `fps` (Khung hình/giây).
* **Tác dụng:** Đặt giới hạn tốc độ chạy game.
* **Cách dùng:** `rl.SetTargetFPS(60)`
* **Lưu ý:** Raylib sẽ tự động delay (sleep) trong vòng lặp để duy trì mức FPS này. Không nên dùng VSYNC và SetTargetFPS cùng lúc.

**`GetFPS() -> c.int`**
* **Tác dụng:** Lấy FPS thực tế hiện tại.
* **Cách dùng:** `fmt.println(rl.GetFPS())`

**`GetFrameTime() -> f32`**
* **Tác dụng:** Lấy thời gian render frame trước (delta time, tính bằng giây).
* **Cách dùng:** `dt := rl.GetFrameTime()`
* **Lưu ý:** CỰC KỲ QUAN TRỌNG. Phải luôn nhân vận tốc nhân vật với biến này để game chạy đều trên mọi màn hình. `pos.x += speed * dt`.

**`GetTime() -> f64`**
* **Tác dụng:** Lấy tổng thời gian (giây) kể từ lúc gọi InitWindow.
* **Cách dùng:** `time_elapsed := rl.GetTime()` (Dùng làm timer đếm ngược hoặc tạo animation sóng hình Sin).

---

## 6. SỐ NGẪU NHIÊN (Random)

**`SetRandomSeed(seed: c.uint)`**
* **Tác dụng:** Cài đặt mầm sinh số ngẫu nhiên.
* **Cách dùng:** `rl.SetRandomSeed(12345)` (Game sẽ luôn sinh ra map giống hệt nhau nếu seed giống nhau).

**`GetRandomValue(min, max: c.int) -> c.int`**
* **Tác dụng:** Trả về một số nguyên ngẫu nhiên nằm trong khoảng `min` và `max` (bao gồm cả min, max).
* **Cách dùng:** `damage := rl.GetRandomValue(10, 20)`

**`LoadRandomSequence(count: c.uint, min, max: c.int) -> [^]c.int`** / **`UnloadRandomSequence(...)`**
* **Tác dụng:** Sinh ra một chuỗi ngẫu nhiên không trùng lặp (vd: Xáo trộn bộ bài).
* **Lưu ý:** Nhớ Unload khi dùng xong để giải phóng bộ nhớ.

---

## 7. ĐẦU VÀO: BÀN PHÍM (Keyboard)

**`IsKeyPressed(key: KeyboardKey) -> bool`**
* **Tham số:** `key` (Mã phím).
* **Tác dụng:** Trả về true trong đúng 1 frame khi phím được nhấn xuống.
* **Cách dùng:** `if rl.IsKeyPressed(.SPACE) { nhayLen() }` (Dùng cho nhảy, lướt, bắn 1 viên đạn).

**`IsKeyPressedRepeat(key: KeyboardKey) -> bool`**
* **Tác dụng:** Giống `IsKeyPressed` nhưng kích hoạt liên tục theo cơ chế tự lặp lại phím của hệ điều hành.
* **Cách dùng:** `if rl.IsKeyPressedRepeat(.BACKSPACE) { xoaKiTu() }` (Dùng nhập liệu văn bản).

**`IsKeyDown(key: KeyboardKey) -> bool`**
* **Tác dụng:** Trả về true liên tục nếu phím đang bị giữ.
* **Cách dùng:** `if rl.IsKeyDown(.D) { player.x += speed * dt }` (Dùng cho di chuyển liên tục).

**`IsKeyReleased(key: KeyboardKey) -> bool`**
* **Tác dụng:** Trả về true 1 frame khi vừa nhả phím.
* **Cách dùng:** `if rl.IsKeyReleased(.SPACE) { ngungNhay() }`

**`IsKeyUp(key: KeyboardKey) -> bool`**
* **Tác dụng:** Trả về true nếu phím KHÔNG bị nhấn.

**`GetKeyPressed() -> KeyboardKey`**
* **Tác dụng:** Lấy mã phím vừa nhấn ra khỏi hàng đợi. Dùng để xem người dùng bấm phím gì bất kỳ.

**`GetCharPressed() -> rune`**
* **Tác dụng:** Lấy ký tự Unicode vừa gõ.
* **Lưu ý:** Hàm quan trọng nhất khi làm ô nhập tên người chơi (Text Input box) vì nó hỗ trợ bắt ký tự thực tế (kể cả Shift, Unikey).

**`SetExitKey(key: KeyboardKey)`**
* **Tác dụng:** Cài đặt phím dùng để thoát game.
* **Cách dùng:** `rl.SetExitKey(.NONE)` (Tắt tính năng bấm ESC tự out game).

---

## 8. ĐẦU VÀO: CHUỘT (Mouse)

**`IsMouseButtonPressed(button: MouseButton) -> bool`**
* **Tham số:** `button` (Nút chuột: `.LEFT`, `.RIGHT`, `.MIDDLE`).
* **Tác dụng:** Trả về true 1 frame khi vừa click chuột.
* **Cách dùng:** `if rl.IsMouseButtonPressed(.LEFT) { clickGiaoDien() }`

**`IsMouseButtonDown(button: MouseButton) -> bool`**
* **Tác dụng:** Trả về true liên tục khi đang giữ nút chuột.
* **Cách dùng:** `if rl.IsMouseButtonDown(.LEFT) { keoThaVatPham() }`

**`IsMouseButtonReleased(...)`** / **`IsMouseButtonUp(...)`**
* **Tác dụng:** Kiểm tra nhả chuột và không bấm chuột.

**`GetMouseX() -> c.int`** / **`GetMouseY() -> c.int`**
* **Tác dụng:** Lấy tọa độ X, Y của chuột (trên màn hình máy tính).

**`GetMousePosition() -> Vector2`**
* **Tác dụng:** Lấy tọa độ XY của chuột dạng vector.
* **Cách dùng:** `mousePos := rl.GetMousePosition()`

**`GetMouseDelta() -> Vector2`**
* **Tác dụng:** Lấy khoảng cách di chuyển của chuột so với frame trước.
* **Cách dùng:** `delta := rl.GetMouseDelta()` (Rất hay dùng để xoay camera 3D hoặc kéo thả bản đồ).

**`SetMousePosition(x, y: c.int)`**
* **Tác dụng:** Bắt buộc chuột phải ở 1 tọa độ bằng code.

**`SetMouseOffset(...)`** / **`SetMouseScale(...)`**
* **Tác dụng:** Offset và Scale chuột.
* **Lưu ý:** Hay dùng khi game vẽ lên 1 RenderTexture ảo nhỏ rồi phóng to ra màn hình lớn (giúp chuột vẫn khớp với UI).

**`GetMouseWheelMove() -> f32`**
* **Tác dụng:** Lấy chỉ số lăn của chuột Y (dương = lên, âm = xuống).
* **Cách dùng:** `zoom += rl.GetMouseWheelMove() * 0.1` (Làm zoom camera bằng con lăn).

**`GetMouseWheelMoveV() -> Vector2`**
* **Tác dụng:** Lấy chỉ số lăn trục X và Y.

**`SetMouseCursor(cursor: MouseCursor)`**
* **Tham số:** `cursor` (Loại con trỏ: `.POINTING_HAND`, `.IBEAM`, ...).
* **Tác dụng:** Đổi hình ảnh con trỏ HĐH.
* **Cách dùng:** `rl.SetMouseCursor(.POINTING_HAND)` (khi di chuột qua Nút bấm UI).

---

## 9. VẼ HÌNH CƠ BẢN (Basic Shapes)

### 9.1 Vẽ Điểm & Đoạn thẳng
**`DrawPixel(posX, posY: c.int, color: Color)`** / **`DrawPixelV(...)`**
* **Tác dụng:** Vẽ 1 điểm.
* **Cách dùng:** `rl.DrawPixel(10, 10, rl.RED)`

**`DrawLine(startPosX, startPosY, endPosX, endPosY: c.int, color: Color)`** / **`DrawLineV(...)`**
* **Tác dụng:** Vẽ đường thẳng dày 1 pixel.
* **Cách dùng:** `rl.DrawLine(0, 0, 100, 100, rl.BLUE)`

**`DrawLineEx(startPos, endPos: Vector2, thick: f32, color: Color)`**
* **Tác dụng:** Vẽ đường thẳng có thể chỉnh độ dày.
* **Cách dùng:** `rl.DrawLineEx(p1, p2, 5.0, rl.GREEN)`

**`DrawLineStrip(points: [^]Vector2, pointCount: c.int, color: Color)`**
* **Tác dụng:** Vẽ một chuỗi đường thẳng đi qua các điểm (như vẽ đồ thị).

**`DrawLineBezier(startPos, endPos: Vector2, thick: f32, color: Color)`**
* **Tác dụng:** Vẽ đường cong mềm mại (Bezier) nối 2 điểm. Rất đẹp cho UI hoặc dây cung.

### 9.2 Vẽ Hình Chữ Nhật
**`DrawRectangle(posX, posY: c.int, width, height: c.int, color: Color)`**
* **Tác dụng:** Vẽ hình chữ nhật đặc.
* **Cách dùng:** `rl.DrawRectangle(10, 10, 50, 50, rl.RED)`
* **Lưu ý:** Tâm vẽ bắt đầu từ góc trên cùng bên trái.

**`DrawRectangleV(position: Vector2, size: Vector2, color: Color)`** / **`DrawRectangleRec(rec: Rectangle, color: Color)`**
* **Tác dụng:** Tương tự DrawRectangle nhưng truyền bằng struct.
* **Cách dùng:** `rl.DrawRectangleRec(player_rect, rl.BLUE)`

**`DrawRectanglePro(rec: Rectangle, origin: Vector2, rotation: f32, color: Color)`**
* **Tác dụng:** Vẽ hình chữ nhật đặc, có tâm xoay (`origin`) và góc xoay (`rotation`).
* **Cách dùng:** `rl.DrawRectanglePro(rect, {rect.width/2, rect.height/2}, 45.0, rl.RED)` (Xoay quanh tâm hình).

**`DrawRectangleGradientV(...)`** / **`DrawRectangleGradientH(...)`** / **`DrawRectangleGradientEx(...)`**
* **Tác dụng:** Vẽ chữ nhật đổ màu gradient (dọc, ngang, 4 góc).
* **Cách dùng:** Dùng làm thanh máu (HP bar) hoặc nền trời hoàng hôn.

**`DrawRectangleLines(posX, posY: c.int, width, height: c.int, color: Color)`**
* **Tác dụng:** Vẽ viền (khung) hình chữ nhật, dày 1 pixel. Dùng để debug va chạm hitbox.

**`DrawRectangleLinesEx(rec: Rectangle, lineThick: f32, color: Color)`**
* **Tác dụng:** Vẽ viền có thể tùy chỉnh độ dày.

**`DrawRectangleRounded(rec: Rectangle, roundness: f32, segments: c.int, color: Color)`**
* **Tham số:** `roundness` (Tỉ lệ bo tròn 0.0-1.0), `segments` (Độ phân giải đường cong).
* **Tác dụng:** Vẽ hình chữ nhật bo góc (Cực đẹp cho UI).
* **Cách dùng:** `rl.DrawRectangleRounded(btn_rect, 0.5, 10, rl.GRAY)`

**`DrawRectangleRoundedLines(...)`** / **`DrawRectangleRoundedLinesEx(...)`**
* **Tác dụng:** Vẽ viền chữ nhật bo góc.

### 9.3 Vẽ Hình Tròn & Ellipse
**`DrawCircle(centerX, centerY: c.int, radius: f32, color: Color)`** / **`DrawCircleV(...)`**
* **Tác dụng:** Vẽ hình tròn đặc. Toạ độ là TÂM (không giống hcn).
* **Cách dùng:** `rl.DrawCircle(100, 100, 50.0, rl.RED)`

**`DrawCircleSector(center: Vector2, radius: f32, startAngle, endAngle: f32, segments: c.int, color: Color)`**
* **Tác dụng:** Vẽ hình quạt (phần hình tròn).
* **Cách dùng:** Dùng làm kỹ năng AOE hình quạt phía trước nhân vật, hoặc cooldown xoay vòng tròn.

**`DrawCircleGradient(centerX, centerY: c.int, radius: f32, inner, outer: Color)`**
* **Tác dụng:** Vẽ hình tròn đổ màu tỏa từ tâm (rất hợp làm nguồn sáng ảo giác hoặc quả cầu ma thuật).

**`DrawCircleLines(...)`** / **`DrawCircleSectorLines(...)`**
* **Tác dụng:** Vẽ viền tròn, viền quạt.

**`DrawEllipse(...)`** / **`DrawEllipseLines(...)`**
* **Tác dụng:** Vẽ hình bầu dục (ellipse) có 2 bán kính (ngang, dọc). Dùng vẽ bóng nhân vật rọi xuống đất.

**`DrawRing(...)`** / **`DrawRingLines(...)`**
* **Tác dụng:** Vẽ hình vành khăn (chiếc nhẫn / bánh donut). Dùng làm vòng sáng xung quanh boss.

### 9.4 Vẽ Đa Giác & Tam Giác
**`DrawTriangle(v1, v2, v3: Vector2, color: Color)`** / **`DrawTriangleLines(...)`**
* **Tác dụng:** Vẽ tam giác bằng 3 đỉnh tọa độ. (Chú ý thứ tự vẽ đỉnh phải ngược chiều kim đồng hồ để không bị lật mặt nếu dùng Face Culling).

**`DrawPoly(center: Vector2, sides: c.int, radius: f32, rotation: f32, color: Color)`**
* **Tác dụng:** Vẽ đa giác đều (ngũ giác, lục giác, ...).
* **Cách dùng:** `rl.DrawPoly(pos, 6, 20.0, 0, rl.YELLOW)` (Vẽ tổ ong lục giác).

### 9.5 Vẽ Spline (Đường cong phức tạp)
**`DrawSplineLinear(...)`**, **`DrawSplineCatmullRom(...)`**, **`DrawSplineBezierCubic(...)`**
* **Tác dụng:** Vẽ đường cong mềm mại chạy qua nhiều điểm. Dùng làm đuôi xe, vết chém của kiếm, quỹ đạo tên lửa đuổi.

---

## 10. XỬ LÝ VA CHẠM 2D (Basic shapes collision detection)

**`CheckCollisionRecs(rec1, rec2: Rectangle) -> bool`**
* **Tác dụng:** Kiểm tra 2 hình chữ nhật có đè lên nhau không (AABB).
* **Cách dùng:** `if rl.CheckCollisionRecs(player, quaiVat) { matMau() }`
* **Lưu ý:** Đây là hàm va chạm rẻ và được sử dụng nhiều nhất (99% game 2D dùng hàm này).

**`CheckCollisionCircles(center1: Vector2, radius1: f32, center2: Vector2, radius2: f32) -> bool`**
* **Tác dụng:** Kiểm tra 2 hình tròn có giao nhau không. (Nhanh hơn cả CheckCollisionRecs vì chỉ cần tính khoảng cách).

**`CheckCollisionCircleRec(center: Vector2, radius: f32, rec: Rectangle) -> bool`**
* **Tác dụng:** Va chạm giữa tròn (đạn súng cối) và vuông (xe tank).

**`CheckCollisionPointRec(point: Vector2, rec: Rectangle) -> bool`**
* **Tác dụng:** Điểm có nằm trong hình chữ nhật không?
* **Cách dùng:** `if rl.CheckCollisionPointRec(rl.GetMousePosition(), buttonRect) { click() }` (Làm nút bấm UI đơn giản nhất).

**`CheckCollisionPointCircle(point, center: Vector2, radius: f32) -> bool`**
* **Tác dụng:** Kiểm tra điểm nằm trong hình tròn.

**`CheckCollisionLines(startPos1, endPos1, startPos2, endPos2: Vector2, collisionPoint: [^]Vector2) -> bool`**
* **Tác dụng:** 2 đường thẳng có cắt nhau không? Nếu có, `collisionPoint` sẽ lưu toạ độ cắt. (Dùng làm tia laser bắn trúng tường).

**`GetCollisionRec(rec1, rec2: Rectangle) -> Rectangle`**
* **Tác dụng:** Trả về hình chữ nhật là phần giao nhau của 2 chữ nhật bị đè. Rất cần thiết trong việc xử lý đẩy lùi nhân vật khi kẹt vào tường.

---

## 11. XỬ LÝ ẢNH TRÊN CPU (Image functions)
*(Dữ liệu dạng `Image`, xử lý trực tiếp trên RAM, không dùng để vẽ trực tiếp ra màn hình bằng GPU mà dùng để sinh map, đọc pixel)*

**`LoadImage(fileName: cstring) -> Image`**
* **Tác dụng:** Tải ảnh từ ổ cứng lên RAM (Chưa thể vẽ ra màn hình).
* **Cách dùng:** `img := rl.LoadImage("map.png")`
* **Lưu ý:** Vì ảnh nằm trên RAM nên bạn có thể đọc từng Pixel của nó (dùng cho việc lấy dữ liệu tạo TileMap).

**`LoadImageRaw(...)`** / **`LoadImageAnim(...)`** / **`LoadImageFromMemory(...)`**
* **Tác dụng:** Tải ảnh raw, ảnh gif động, hoặc tải ảnh từ mảng byte trong RAM.

**`LoadImageFromTexture(texture: Texture2D) -> Image`**
* **Tác dụng:** Tải ngược dữ liệu từ GPU (Texture) về CPU (Image). Khá tốn kém hiệu năng, chỉ dùng khi cần chụp ảnh màn hình hoặc lưu save.

**`LoadImageFromScreen() -> Image`**
* **Tác dụng:** Chụp màn hình và lưu vào RAM dạng Image.

**`IsImageValid(image: Image) -> bool`**
* **Tác dụng:** Kiểm tra ảnh có tải đúng chưa (không bị lỗi file).

**`UnloadImage(image: Image)`**
* **Tác dụng:** Giải phóng RAM. (Bắt buộc gọi khi không dùng nữa).
* **Cách dùng:** `rl.UnloadImage(img)`

**`ExportImage(image: Image, fileName: cstring) -> bool`**
* **Tác dụng:** Lưu Image thành file ảnh trên ổ cứng (.png, .jpg). Dùng để làm tính năng "Screenshot" trong game.

**`GenImageColor(width, height: c.int, color: Color) -> Image`**
* **Tác dụng:** Sinh ra 1 ảnh trơn bằng mã màu.

***(Các hàm sinh ảnh tự động khác)***
* **`GenImageGradientLinear(...)`**: Sinh ảnh dải màu tuyến tính.
* **`GenImagePerlinNoise(...)`**: Sinh ảnh Perlin Noise. **Lưu ý**: Cực kỳ hữu ích để sinh địa hình ngẫu nhiên (như Minecraft, Terraria) mà không cần vẽ tay.

***(Các hàm chỉnh sửa ảnh trên CPU)***
* **`ImageCopy(...)`**, **`ImageCrop(...)`**, **`ImageResize(...)`**, **`ImageFlipHorizontal(...)`**
* **Lưu ý:** Chỉ thao tác trên Image (RAM), thao tác xong phải chuyển thành Texture2D mới vẽ lên màn hình được.

**`GetImageColor(image: Image, x, y: c.int) -> Color`**
* **Tác dụng:** Lấy màu của 1 pixel cụ thể.
* **Cách dùng:** Đọc màu pixel tại vị trí (x,y) của bản đồ (Image) để quyết định spawn cây, đá, hay nước.

---

## 12. TEXTURE 2D TRÊN GPU (Texture functions)
*(Dữ liệu dạng `Texture2D`, nằm trên VRAM của Card Đồ Hoạ, dùng để vẽ ra màn hình cực nhanh)*

**`LoadTexture(fileName: cstring) -> Texture2D`**
* **Tác dụng:** Đọc file và nạp thẳng lên VRAM của GPU thành Texture.
* **Cách dùng:** `tex := rl.LoadTexture("player.png")`
* **Lưu ý:** Dùng hàm này cho mọi Sprite / Hình ảnh bạn muốn vẽ ra màn hình.

**`LoadTextureFromImage(image: Image) -> Texture2D`**
* **Tác dụng:** Chuyển ảnh từ CPU lên GPU.
* **Cách dùng:** Thường kết hợp sau khi `GenImagePerlinNoise` xong thì gọi hàm này để nạp lên GPU.

**`LoadRenderTexture(width, height: c.int) -> RenderTexture2D`**
* **Tác dụng:** Tạo một framebuffer ảo (canvas ảo) trên GPU.
* **Cách dùng:** `canvas := rl.LoadRenderTexture(320, 180)` (Dùng để vẽ game độ phân giải thấp, sau đó phóng to canvas này ra toàn màn hình để giữ chất lượng Pixel Art).

**`IsTextureValid(texture: Texture2D) -> bool`**
* **Tác dụng:** Kiểm tra texture đã tồn tại trên GPU chưa.

**`UnloadTexture(texture: Texture2D)`** / **`UnloadRenderTexture(...)`**
* **Tác dụng:** Giải phóng VRAM. Tránh memory leak.

**`UpdateTexture(texture: Texture2D, pixels: rawptr)`**
* **Tác dụng:** Cập nhật nóng dữ liệu cho Texture đang có trên GPU mà không cần tải lại file. (Dùng khi làm mini-map thời gian thực).

**`SetTextureFilter(texture: Texture2D, filter: TextureFilter)`**
* **Tham số:** `filter` (Ví dụ: `.POINT`, `.BILINEAR`).
* **Tác dụng:** Cài đặt chế độ lọc ảnh.
* **Lưu ý:** QUAN TRỌNG: Với game Pixel Art, BẮT BUỘC dùng `rl.SetTextureFilter(tex, .POINT)` để khi phóng to ảnh không bị mờ (blur).

**`SetTextureWrap(texture: Texture2D, wrap: TextureWrap)`**
* **Tác dụng:** Cài đặt chế độ lặp họa tiết khi vẽ. Dùng làm background bầu trời cuộn vô tận.

**`DrawTexture(texture: Texture2D, posX, posY: c.int, tint: Color)`** / **`DrawTextureV(...)`**
* **Tác dụng:** Vẽ texture ra màn hình ở tỉ lệ 1:1.
* **Cách dùng:** `rl.DrawTexture(tex, 100, 100, rl.WHITE)`

**`DrawTextureEx(texture: Texture2D, position: Vector2, rotation: f32, scale: f32, tint: Color)`**
* **Tác dụng:** Vẽ texture có thể phóng to (scale) và xoay (rotation).

**`DrawTextureRec(texture: Texture2D, source: Rectangle, position: Vector2, tint: Color)`**
* **Tác dụng:** Cắt 1 khung hình nhỏ (Rectangle `source`) bên trong một SpriteSheet to để vẽ ra màn hình.
* **Lưu ý:** Hàm này là "xương sống" của hệ thống Animation 2D (nhân vật chạy nhảy).

**`DrawTexturePro(texture: Texture2D, source, dest: Rectangle, origin: Vector2, rotation: f32, tint: Color)`**
* **Tác dụng:** Hàm vẽ Texture MẠNH NHẤT. Kết hợp Cắt (source), Phóng to/ép nhỏ/lật (dest), và Xoay quanh tâm (origin).
* **Lưu ý:** Để lật ngược nhân vật khi quay đầu, đổi chiều `source.width` thành số âm (vd: `-32.0`).

**`DrawTextureNPatch(texture: Texture2D, nPatchInfo: NPatchInfo, dest: Rectangle, origin: Vector2, rotation: f32, tint: Color)`**
* **Tác dụng:** Vẽ UI (nút bấm, bảng thoại) bằng kỹ thuật 9-patch để không bị méo các góc khi kéo dãn.

---

## 13. MÀU SẮC (Color functions)

**`Fade(color: Color, alpha: f32) -> Color`**
* **Tác dụng:** Trả về màu mới với độ trong suốt được thay đổi (alpha từ 0.0 - 1.0).
* **Cách dùng:** `rl.DrawRectangle(0, 0, 800, 600, rl.Fade(rl.BLACK, 0.5))` (Làm mờ nền khi bật Menu Pause).

**`ColorToInt(color: Color) -> c.uint`**
* **Tác dụng:** Biến màu về dạng số Hex 0xRRGGBBAA.

**`ColorNormalize(color: Color) -> Vector4`**
* **Tác dụng:** Trả về màu dạng Float RGBA (0.0 đến 1.0). Dùng để truyền biến Uniform vào Shader.

**`ColorToHSV(color: Color) -> Vector3`** / **`ColorFromHSV(hue, saturation, value: f32) -> Color`**
* **Tác dụng:** Chuyển đổi qua lại hệ màu RGB và HSV. (Dùng làm hiệu ứng nhấp nháy cầu vồng bằng cách thay đổi Hue theo thời gian).

**`ColorLerp(color1, color2: Color, factor: f32) -> Color`**
* **Tác dụng:** Pha trộn mượt mà giữa 2 màu. Dùng làm hiệu ứng chuyển ngày-đêm.

---

## 14. CHỮ VIẾT & FONT (Text & Font functions)

**`GetFontDefault() -> Font`**
* **Tác dụng:** Lấy font mặc định của Raylib (pixel art siêu nhỏ). Không hỗ trợ Tiếng Việt.

**`LoadFont(fileName: cstring) -> Font`**
* **Tác dụng:** Tải font (.ttf) và nạp lên GPU.
* **Cách dùng:** `font := rl.LoadFont("arial.ttf")`

**`LoadFontEx(fileName: cstring, fontSize: c.int, codepoints: [^]rune, codepointCount: c.int) -> Font`**
* **Tác dụng:** Tải font chất lượng cao và CHỈ load danh sách các ký tự cần thiết.
* **Lưu ý:** Bắt buộc dùng hàm này nếu muốn render font Tiếng Việt (load các codepoint tiếng việt như 'ă', 'ơ', 'ư' vào VRAM).

**`IsFontValid(font: Font) -> bool`** / **`UnloadFont(font: Font)`**
* **Tác dụng:** Kiểm tra / Giải phóng Font.

**`DrawFPS(posX, posY: c.int)`**
* **Tác dụng:** In nhanh số FPS ra màn hình ở góc định trước. (Chỉ dùng debug).

**`DrawText(text: cstring, posX, posY: c.int, fontSize: c.int, color: Color)`**
* **Tác dụng:** Vẽ chữ (chỉ ASCII, KHÔNG hỗ trợ Tiếng Việt vì dùng font mặc định).

**`DrawTextEx(font: Font, text: cstring, position: Vector2, fontSize: f32, spacing: f32, tint: Color)`**
* **Tác dụng:** Vẽ chữ bằng Font tuỳ chỉnh (Hỗ trợ Tiếng Việt, Unicode).
* **Cách dùng:** `rl.DrawTextEx(myFont, "Xin Chào", {10, 10}, 24, 2, rl.WHITE)`

**`DrawTextPro(font: Font, text: cstring, position, origin: Vector2, rotation: f32, fontSize: f32, spacing: f32, tint: Color)`**
* **Tác dụng:** Vẽ chữ và có khả năng xoay đoạn chữ đó quanh `origin`.

**`SetTextLineSpacing(spacing: c.int)`**
* **Tác dụng:** Chỉnh khoảng cách các dòng khi có kí tự xuống dòng `\n`.

**`MeasureText(text: cstring, fontSize: c.int) -> c.int`**
* **Tác dụng:** Trả về độ dài (pixel) của chuỗi chữ.
* **Cách dùng:** `width := rl.MeasureText("Start Game", 20); rl.DrawText(..., screenW/2 - width/2, ...)` (Cách chuẩn để căn giữa văn bản).

**`MeasureTextEx(font: Font, text: cstring, fontSize: f32, spacing: f32) -> Vector2`**
* **Tác dụng:** Tính toán cả chiều ngang lẫn dọc của khung chứa đoạn văn bản (Bounding Box).

**`LoadUTF8(...)`** / **`LoadCodepoints(...)`**
* **Tác dụng:** Chuyển đổi chuỗi rune (Unicode) sang C-string UTF8 hoặc ngược lại.

*(Cùng với các hàm xử lý C-string cơ bản được tích hợp sẵn: `TextLength`, `TextIsEqual`, `TextSubtext`, `TextToUpper`, v.v... dùng để thao tác với cstring mà không phụ thuộc stdlib của C)*

---

## 15. CẤU TRÚC DỮ LIỆU CỐT LÕI (Core Structs)
Mặc dù bạn thao tác qua nhiều hàm, các cấu trúc dữ liệu sau là nền tảng khi làm việc với Raylib 2D:

**`Vector2`**: `{x, y: f32}`
* **Tác dụng:** Dùng cực kì phổ biến để chỉ vị trí, vận tốc, kích thước 2 chiều.
* **Cách dùng:** `pos: rl.Vector2 = {100.5, 200.0}`

**`Rectangle`**: `{x, y, width, height: f32}`
* **Tác dụng:** Cực kỳ quan trọng để vẽ, cắt hình từ SpriteSheet và xét va chạm.
* **Cách dùng:** `hitbox: rl.Rectangle = {10, 10, 50, 50}`

**`Color`**: `{r, g, b, a: u8}`
* **Tác dụng:** Mỗi kênh màu từ 0 đến 255. `a` là độ trong suốt (alpha).
* **Lưu ý:** Raylib có định nghĩa sẵn rất nhiều màu, ví dụ `rl.RED`, `rl.RAYWHITE`, `rl.BLANK`.

**`Camera2D`**: `{offset: Vector2, target: Vector2, rotation: f32, zoom: f32}`
* **Tác dụng:** 
  - `target`: Điểm trong thế giới ảo mà camera nhắm tới (ví dụ toạ độ của nhân vật chính).
  - `offset`: Điểm trên màn hình mà target sẽ được vẽ ở đó (thường đặt ở `{screenWidth/2, screenHeight/2}` để căn giữa màn hình).
* **Lưu ý:** Đừng nhầm lẫn giữa offset và target. Nếu bạn muốn camera đi theo người chơi, hãy cập nhật `camera.target = player.pos`.

---

## 16. TOÁN HỌC VECTOR & TIỆN ÍCH (Raymath)
Khi làm game 2D, raymath hỗ trợ rất nhiều thao tác toán học với `Vector2`. (Ghi chú: Import thư viện bằng `import "vendor:raylib"` là đã dùng được các hàm này, vì Odin tự gộp raymath vào namespace `rl`).

**`Vector2Distance(v1, v2: Vector2) -> f32`**
* **Tác dụng:** Tính khoảng cách vật lý giữa 2 điểm.
* **Cách dùng:** Dùng làm AI quái vật: `if rl.Vector2Distance(player.pos, enemy.pos) < 200 { rượtĐuổi() }`

**`Vector2Length(v: Vector2) -> f32`**
* **Tác dụng:** Tính độ dài (magnitude) của vector vận tốc. Dùng để giới hạn tốc độ tối đa của nhân vật.

**`Vector2Normalize(v: Vector2) -> Vector2`**
* **Tác dụng:** Chuẩn hoá vector (có độ dài bằng 1).
* **Lưu ý:** Khi người chơi đi chéo (bấm cả W và D), vận tốc sẽ bị tăng lên 1.4 lần so với đi thẳng. Phải luôn luôn normalize vector hướng di chuyển trước khi nhân với `speed`.

**`Vector2Add(v1, v2: Vector2) -> Vector2`** / **`Vector2Subtract(...)`**
* **Tác dụng:** Cộng / Trừ 2 vector. Phép trừ cực kì hữu ích để tìm hướng bắn đạn từ điểm A sang điểm B.

**`Vector2Lerp(v1, v2: Vector2, amount: f32) -> Vector2`**
* **Tác dụng:** Nội suy tuyến tính (Linear Interpolation) mượt mà giữa 2 vị trí.
* **Cách dùng:** `camera.target = rl.Vector2Lerp(camera.target, player.pos, 5.0 * dt)` (Làm camera đi theo nhân vật rất mượt mà không bị giật cứng).

---

## 17. ĐẦU VÀO: TAY CẦM (Gamepad) & CẢM ỨNG (Touch)

### Gamepad (Tay Cầm)
**`IsGamepadAvailable(gamepad: c.int) -> bool`**
* **Tham số:** `gamepad` (id tay cầm, mặc định là 0).
* **Tác dụng:** Kiểm tra xem có cắm tay cầm vào không (để hiện UI hướng dẫn A B X Y thay vì chuột).

**`IsGamepadButtonPressed(gamepad: c.int, button: GamepadButton) -> bool`** / **`IsGamepadButtonDown(...)`**
* **Tác dụng:** Kiểm tra nhấn nút / giữ nút (như `IsKeyPressed`). Nút `.RIGHT_FACE_DOWN` tương ứng với nút A trên Xbox, nút X trên PlayStation.

**`GetGamepadAxisMovement(gamepad: c.int, axis: GamepadAxis) -> f32`**
* **Tác dụng:** Đọc độ nghiêng của cần analog (từ -1.0 đến 1.0) dùng để di chuyển linh hoạt (VD: nghiêng nhẹ thì đi bộ, đẩy mạnh thì chạy).

### Cảm ứng (Touch - Cho game Mobile)
**`GetTouchX() -> c.int`** / **`GetTouchY() -> c.int`** / **`GetTouchPosition(...)`**
* **Tác dụng:** Lấy toạ độ chạm màn hình. Chạm cảm ứng mặc định cũng kích hoạt chuột trái (chuột ảo).

---

## 18. LƯU TRỮ HỆ THỐNG & FILE (Save / Load)

**`LoadFileText(fileName: cstring) -> cstring`** / **`SaveFileText(...)`**
* **Tác dụng:** Đọc / Ghi toàn bộ nội dung file text (ví dụ định dạng JSON).
* **Cách dùng:** Dùng cho tính năng Lưu / Tải Game (Save/Load). Nhớ gọi `rl.UnloadFileText` khi đọc xong.

**`FileExists(fileName: cstring) -> bool`** / **`DirectoryExists(...)`**
* **Tác dụng:** Kiểm tra file / thư mục có tồn tại trên đĩa cứng không (Vd: Kiểm tra xem có file save hay chưa trước khi Load).

---

## 19. IN LOG & DEBUG (TraceLog)
Thay vì dùng thư viện chuẩn `fmt.println`, Raylib có hệ thống in log chuyên nghiệp giúp phân loại cảnh báo:

**`TraceLog(logLevel: TraceLogLevel, text: cstring, ...)`**
* **Tham số:** Mức độ log (`.INFO`, `.WARNING`, `.ERROR`, `.FATAL`), và chuỗi thông báo.
* **Tác dụng:** In log ra màn hình console. (Ví dụ báo lỗi khi không load được file ảnh).

**`SetTraceLogLevel(logLevel: TraceLogLevel)`**
* **Tác dụng:** Cài đặt mức độ ưu tiên in log.
* **Cách dùng:** `rl.SetTraceLogLevel(.WARNING)` (Tắt bớt các log `.INFO` hiển thị quá nhiều lúc khởi tạo game để đỡ rối mắt).

---

## 20. ĐẶC THÙ ODIN: XỬ LÝ C-STRING (Quan trọng)
Raylib viết bằng ngôn ngữ C nên tất cả các hàm nhận chuỗi ký tự đều nhận vào loại `cstring` (có kí tự Null kết thúc). Trong khi string mặc định của Odin là có độ dài cố định.
Khi truyền string động từ Odin vào Raylib, bạn có 2 cách chính để tránh game bị crash:

1. **Dùng hàm của thư viện strings (cần free):**
```odin
import "core:strings"

str := "Nội dung động"
c_str := strings.clone_to_cstring(str)
defer delete(c_str) // LƯU Ý BẮT BUỘC: Nếu không sẽ bị rò rỉ bộ nhớ (memory leak).

rl.DrawText(c_str, 10, 10, 20, rl.WHITE)
```

2. **Dùng bộ nhớ tạm `temp_allocator` (Khuyên dùng cho việc vẽ UI):**
```odin
import "core:fmt"

// Lắp ráp chuỗi ngay trên bộ nhớ tạm, tự động xoá bộ nhớ dư thừa ở hàm free_all(context.temp_allocator) cuối game loop.
c_str := fmt.ctprintf("Điểm của bạn: %d", score) 
rl.DrawText(c_str, 10, 10, 20, rl.WHITE)
```

---

## 21. ÂM THANH & NHẠC NỀN (Audio)
*(Phần này tuy nằm trong module Audio, nhưng nó là không thể thiếu đối với mọi tựa game).*

**`InitAudioDevice()`** / **`CloseAudioDevice()`**
* **Tác dụng:** Khởi tạo / Tắt thiết bị âm thanh.
* **Lưu ý:** Bắt buộc gọi `InitAudioDevice()` 1 lần khi mở game (thường gọi ngay sau InitWindow). NẾU QUÊN, game sẽ crash khi load nhạc.

### Tiếng động ngắn (Sound)
*(Hiệu ứng tiếng chém, tiếng nhảy, tiếng nhặt tiền)*

**`LoadSound(fileName: cstring) -> Sound`** / **`UnloadSound(sound: Sound)`**
* **Tác dụng:** Tải file âm thanh ngắn (.wav, .ogg) lên RAM / Giải phóng.

**`PlaySound(sound: Sound)`**
* **Tác dụng:** Phát tiếng động 1 lần.
* **Cách dùng:** Gọi khi viên đạn chạm vào kẻ địch. Có thể phát nhiều sound chồng lên nhau cùng lúc.

### Nhạc nền dài (Music)
*(Nhạc nền chạy lặp đi lặp lại)*

**`LoadMusicStream(fileName: cstring) -> Music`**
* **Tác dụng:** Tải stream nhạc nền (.ogg, .mp3). Load dạng luồng (stream) sẽ tốn rất ít RAM vì nó vừa đọc vừa phát.

**`PlayMusicStream(music: Music)`** / **`StopMusicStream(...)`**
* **Tác dụng:** Bắt đầu phát / Dừng nhạc.

**`UpdateMusicStream(music: Music)`**
* **Tác dụng:** Cập nhật bộ đệm âm thanh.
* **Lưu ý cực kỳ quan trọng:** Hàm này phải được gọi LIÊN TỤC mỗi frame bên trong vòng lặp game chính (`for !rl.WindowShouldClose()`) để luồng nhạc tiếp tục trôi đi, nếu không nhạc sẽ bị giật hoặc đứt quãng.
