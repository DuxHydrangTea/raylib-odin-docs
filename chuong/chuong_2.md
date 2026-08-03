# Chương 2: Hiển thị, Thời gian và Vẽ hình cơ bản

Chào mừng bạn đến với Chương 2! Bây giờ chúng ta đã có một cửa sổ trống từ Chương 1, nhiệm vụ tiếp theo là vẽ lên đó các hình khối cơ bản, quản lý màu sắc và quan trọng nhất là: **Kiểm soát thời gian (FPS và Delta Time)**.

---

## 1. Vòng lặp vẽ (Drawing)

Mọi lệnh vẽ trong Raylib BẮT BUỘC phải nằm giữa hai hàm `BeginDrawing()` và `EndDrawing()`.

* **`BeginDrawing()`**: Báo cho GPU biết chúng ta sắp gửi dữ liệu lên để vẽ.
* **`ClearBackground(color: Color)`**: Quét sơn lại toàn bộ màn hình bằng một màu nền. **Luôn gọi hàm này đầu tiên** sau `BeginDrawing()`, nếu không các hình ảnh của frame cũ sẽ bị lưu lại tạo thành vệt kéo dài (ghosting).
* **`EndDrawing()`**: Kết thúc việc gửi lệnh và đẩy hình ảnh ra màn hình (hoán đổi buffer).

```odin
rl.BeginDrawing()
    rl.ClearBackground(rl.RAYWHITE)
    // Các hàm Draw... nằm ở đây
rl.EndDrawing()
```

---

## 2. Vẽ hình cơ bản (Basic Shapes)

Raylib hỗ trợ vẽ rất nhiều hình cơ bản. Dưới đây là những hình bạn sẽ dùng nhiều nhất:

* **Vẽ Hình chữ nhật:**
  * `DrawRectangle(posX, posY, width, height: c.int, color: Color)`: Vẽ hcn đặc. (Lưu ý x, y là toạ độ **góc trên cùng bên trái**).
  * `DrawRectangleLines(...)`: Chỉ vẽ đường viền (rất tốt để debug khung va chạm).
  * `DrawRectangleRounded(rec: Rectangle, roundness: f32, segments: c.int, color: Color)`: Vẽ hcn bo góc (rất đẹp cho UI/Nút bấm).

* **Vẽ Hình tròn:**
  * `DrawCircle(centerX, centerY: c.int, radius: f32, color: Color)`: Vẽ hình tròn đặc. (Lưu ý x, y là toạ độ **TÂM**).
  * `DrawCircleGradient(...)`: Tròn toả màu (dùng làm nguồn sáng).

* **Vẽ Đường thẳng:**
  * `DrawLine(startPosX, startPosY, endPosX, endPosY: c.int, color: Color)`: Vẽ đoạn thẳng dày 1 pixel.
  * `DrawLineEx(startPos, endPos: Vector2, thick: f32, color: Color)`: Vẽ đoạn thẳng có thể chỉnh độ dày.

---

## 3. Màu sắc & Độ trong suốt (Colors & Alpha)

Bạn có thể tạo màu bằng cách dùng các hằng số (`rl.RED`, `rl.BLUE`) hoặc tự tạo cấu trúc `{R, G, B, A}`. Tuy nhiên, có một hàm cực kì hữu ích là:

* **`Fade(color: Color, alpha: f32) -> Color`**
  * Tác dụng: Lấy một màu có sẵn và thay đổi độ trong suốt của nó (`alpha` từ `0.0` đến `1.0`).
  * Ứng dụng: Ví dụ, khi bấm `ESC` để dừng game (Pause), bạn có thể vẽ một hình chữ nhật đen che phủ toàn bộ màn hình với độ mờ 50%:
    `rl.DrawRectangle(0, 0, width, height, rl.Fade(rl.BLACK, 0.5))`

---

## 4. Quản lý Thời gian & Khung hình (CỰC KỲ QUAN TRỌNG)

Khi lập trình game, chúng ta không dùng vòng lặp `for` bình thường hoặc hàm `sleep` để làm chậm nhân vật. Tốc độ game phụ thuộc vào **FPS (Frames Per Second)** và **Delta Time**.

### 4.1. Giới hạn FPS
* **`SetTargetFPS(fps: c.int)`**
  * Tác dụng: Khóa số khung hình mỗi giây. Tránh việc game chạy hàng ngàn FPS khiến CPU/GPU bị quá tải và nóng máy.
  * Cách dùng: Gọi **1 lần** sau khi `InitWindow()`. Thường là `rl.SetTargetFPS(60)`.

### 4.2. Khái niệm Delta Time (dt)
Máy tính mạnh có thể chạy 60 FPS, máy tính yếu chỉ chạy 30 FPS. Nếu mỗi frame nhân vật tiến lên 1 pixel, thì:
* Máy mạnh: 1 giây tiến 60 pixel.
* Máy yếu: 1 giây tiến 30 pixel.
-> **Lỗi nghiêm trọng: Tốc độ game phụ thuộc vào sức mạnh máy tính.**

Để giải quyết, chúng ta dùng **Delta Time (thời gian đã trôi qua kể từ frame trước)**.
* **`GetFrameTime() -> f32`**: Lấy ra giá trị delta time (tính bằng giây, vd: 0.016s).

**Quy tắc Vàng:** Mọi sự thay đổi về vị trí, xoay, thời gian chờ **đều phải nhân với Delta Time**.

```odin
// Ví dụ: Nhân vật chạy với vận tốc 200 pixel/giây (bất kể FPS là bao nhiêu)
speed: f32 = 200.0
dt := rl.GetFrameTime()

// Cập nhật vị trí
player_pos.x += speed * dt
```

### 4.3. Lấy thời gian tổng
* **`GetTime() -> f64`**: Trả về tổng thời gian (giây) kể từ lúc game bắt đầu. Thường dùng để làm hiệu ứng nhấp nháy (kết hợp với hàm `sin()`) hoặc đếm ngược.

---

## Bài tập thực hành Chương 2

Hãy nâng cấp file code từ Chương 1 với các yêu cầu sau:
1. Đặt `SetTargetFPS(60)`.
2. Tạo một biến `player_pos` kiểu `Vector2`. Khởi tạo nó ở giữa màn hình.
3. Trong vòng lặp chính, hãy làm cho `player_pos.x` tự động di chuyển sang phải với tốc độ 300 pixel/giây (nhớ sử dụng `GetFrameTime()`).
4. Nếu `player_pos.x` đi vượt quá cạnh phải của màn hình, hãy reset nó về lại toạ độ 0 (cạnh trái màn hình).
5. Thay vì vẽ hình chữ nhật, hãy dùng `DrawCircleV` để vẽ một hình tròn làm nhân vật.
6. Vẽ một hình chữ nhật mờ 50% ở góc màn hình làm "khung điểm" giả.
