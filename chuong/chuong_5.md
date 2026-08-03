# Chương 5: Xử lý Logic Game nâng cao (Va chạm & Camera)

Chào mừng bạn đến với Chương 5! Ở chương này, chúng ta sẽ làm cho thế giới game trở nên "thật" hơn. Nhân vật sẽ không thể đi xuyên tường nhờ hệ thống Va chạm (Collision), và thế giới sẽ trở nên rộng lớn hơn màn hình máy tính nhờ hệ thống Camera 2D.

---

## 1. Xử lý Va chạm (Collision Detection)

Để biết viên đạn có trúng quái vật hay không, hoặc nhân vật có chạm vào đồng tiền hay không, chúng ta dùng các hàm kiểm tra va chạm. Hầu hết các game 2D chỉ cần dùng hitbox hình chữ nhật hoặc hình tròn.

### 1.1. Va chạm Hình chữ nhật (AABB)
* **`CheckCollisionRecs(rec1, rec2: Rectangle) -> bool`**
  * Tác dụng: Trả về `true` nếu 2 hình chữ nhật đang đè lên nhau.
  * Ứng dụng: Gần như 99% game 2D dùng hàm này để xử lý kẹt tường, ăn item, bị quái cắn.
  ```odin
  player_rect := rl.Rectangle{player_pos.x, player_pos.y, 50, 50}
  coin_rect   := rl.Rectangle{coin_pos.x, coin_pos.y, 20, 20}
  
  if rl.CheckCollisionRecs(player_rect, coin_rect) {
      score += 10
      // Ẩn đồng tiền hoặc random vị trí mới
  }
  ```

### 1.2. Va chạm Hình tròn
* **`CheckCollisionCircles(center1: Vector2, radius1: f32, center2: Vector2, radius2: f32) -> bool`**
  * Tác dụng: Nhanh hơn cả kiểm tra hình chữ nhật (vì nó chỉ dùng định lý Pytago để đo khoảng cách giữa 2 tâm). Rất hợp để làm vùng nổ (AoE) của bom hoặc kỹ năng.

### 1.3. Các hàm va chạm khác
* `CheckCollisionCircleRec`: Tròn va chạm với Vuông.
* `CheckCollisionPointRec`: Kiểm tra 1 điểm (như con trỏ chuột) có nằm trong hình chữ nhật (Nút bấm) hay không. Rất tuyệt để tự code hệ thống UI.
* `GetCollisionRec(rec1, rec2)`: Trả về phần diện tích giao nhau. Rất cần thiết để xử lý logic "đẩy lùi" nhân vật khi bị kẹt vào tường.

---

## 2. Hệ thống Camera 2D

Nếu bạn làm một tựa game nhập vai thế giới mở, bản đồ sẽ to gấp nhiều lần màn hình máy tính. Camera 2D chính là "con mắt" của người chơi nhìn vào thế giới ảo đó.

### 2.1. Cấu trúc Camera2D
Bạn cần khởi tạo 1 biến `Camera2D` với các thông số:
* `target`: Điểm trong thế giới ảo mà bạn muốn Camera nhìn vào (Thường là tọa độ của Nhân vật).
* `offset`: Điểm trên màn hình máy tính mà `target` sẽ được vẽ ra. Đặt là `{ScreenWidth/2, ScreenHeight/2}` để nhân vật luôn nằm ở **chính giữa màn hình**.
* `zoom`: Mức độ phóng to (Mặc định là 1.0).

```odin
camera: rl.Camera2D
camera.target = player_pos
camera.offset = {WINDOW_WIDTH / 2.0, WINDOW_HEIGHT / 2.0}
camera.rotation = 0.0
camera.zoom = 1.0
```

### 2.2. Sử dụng Camera (BẮT BUỘC NHỚ)
Khi bắt đầu vẽ, bạn phải chia làm 2 không gian: **Không gian Thế giới** (Vẽ bị ảnh hưởng bởi Camera) và **Không gian UI** (Cố định trên màn hình, ví dụ như thanh máu).

```odin
rl.BeginDrawing()
    rl.ClearBackground(rl.RAYWHITE)
    
    // 1. VẼ THẾ GIỚI ẢO (Bật Camera lên)
    rl.BeginMode2D(camera)
        rl.DrawRectangleV(player_pos, {50, 50}, rl.BLUE) // Vẽ nhân vật
        rl.DrawRectangle(500, 500, 100, 100, rl.RED)    // Vẽ một cái cây ở xa
    rl.EndMode2D() // Tắt Camera
    
    // 2. VẼ UI (Không dùng Camera)
    rl.DrawText("Máu: 100/100", 10, 10, 20, rl.BLACK) // Chữ luôn dính ở góc trái
    
rl.EndDrawing()
```

### 2.3. Quy đổi hệ tọa độ chuột
Khi dùng Camera, tọa độ `GetMousePosition()` chỉ trả về vị trí con trỏ trên màn hình máy tính, chứ KHÔNG phải vị trí của chuột chiếu xuống nền đất trong game ảo.
* Giải pháp: Dùng **`GetScreenToWorld2D(rl.GetMousePosition(), camera)`** để biết chính xác chuột đang chỉ vào viên gạch nào trong bản đồ.

---

## 3. Đầu vào Nâng cao (Gamepad & Cảm ứng)

*(Phần này dành cho những bạn muốn làm game hỗ trợ Tay cầm hoặc xuất ra Mobile)*
* `IsGamepadAvailable(0)`: Kiểm tra tay cầm 1 có cắm không.
* `IsGamepadButtonPressed(0, .RIGHT_FACE_DOWN)`: Kiểm tra nút X (PS) hoặc A (Xbox) được bấm.
* `GetGamepadAxisMovement(0, .LEFT_X)`: Đọc cần gạt Analog (-1.0 đến 1.0) giúp nhân vật di chuyển tinh tế hơn (nghiêng ít thì đi bộ, đè mạnh thì chạy).

---

## Bài tập thực hành Chương 5

1. Tạo một biến `player_rect` (hình chữ nhật màu xanh) và `enemy_rect` (hình chữ nhật màu đỏ).
2. Code cho người chơi di chuyển `player_rect` bằng phím WASD.
3. Trong vòng lặp Update, dùng `CheckCollisionRecs` để xem 2 hình có đè lên nhau không. Nếu có đè lên nhau, hãy đổi màu `enemy_rect` thành màu vàng (`YELLOW`).
4. Khởi tạo một `Camera2D`, gán `target` của nó theo `player_rect.x` và `player_rect.y`.
5. Bao bọc các lệnh vẽ `player_rect` và `enemy_rect` bằng `BeginMode2D` và `EndMode2D` để chiêm ngưỡng Camera chạy theo nhân vật của bạn!
