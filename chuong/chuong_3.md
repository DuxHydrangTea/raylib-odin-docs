# Chương 3: Tương tác người chơi và Toán học Vector

Chào mừng bạn đến với Chương 3! Trong chương này, trò chơi của bạn sẽ không còn "tự động chạy" nữa. Chúng ta sẽ thêm linh hồn cho nó bằng cách lắng nghe các sự kiện từ bàn phím, chuột, và sử dụng toán học Vector để xử lý hướng đi một cách chuyên nghiệp.

---

## 1. Đầu vào Bàn phím (Keyboard)

Raylib cung cấp các hàm rất trực quan để kiểm tra phím. Bạn cần phân biệt rõ **Nhấn giữ** và **Bấm 1 lần**.

* **`IsKeyDown(key: KeyboardKey) -> bool`**
  * Tác dụng: Trả về `true` liên tục chừng nào phím còn đang bị đè xuống.
  * Ứng dụng: Dùng để di chuyển nhân vật (đi bộ, lái xe, bắn súng liên thanh).
  ```odin
  if rl.IsKeyDown(.D) { player_pos.x += speed * dt }
  ```

* **`IsKeyPressed(key: KeyboardKey) -> bool`**
  * Tác dụng: Chỉ trả về `true` đúng 1 frame duy nhất khoảnh khắc bạn ấn phím xuống. Bạn phải nhả ra và ấn lại thì nó mới `true` lần 2.
  * Ứng dụng: Dùng để nhảy lên (không thể nhảy liên tục bằng cách đè phím), mở/đóng túi đồ (Inventory), hoặc bắn 1 viên đạn.
  ```odin
  if rl.IsKeyPressed(.SPACE) { char_jump() }
  ```

* Các hàm khác ít dùng hơn: `IsKeyReleased` (khi vừa nhả phím ra), `IsKeyUp` (khi không bấm).

---

## 2. Đầu vào Chuột (Mouse)

Tương tự bàn phím, chúng ta cũng có nút chuột và toạ độ.

* **Kiểm tra nút bấm:**
  * `IsMouseButtonDown(button: MouseButton)` (Giữ chuột, vd: `.LEFT`, `.RIGHT`)
  * `IsMouseButtonPressed(button: MouseButton)` (Click 1 phát)

* **Lấy toạ độ chuột:**
  * **`GetMousePosition() -> Vector2`**: Lấy tọa độ (x, y) của con trỏ chuột trên cửa sổ game. Rất cần thiết để làm nút bấm (UI) hoặc ngắm bắn.
  * `GetMouseWheelMove() -> f32`: Lấy giá trị lăn chuột (âm hoặc dương). Dùng để làm chức năng Zoom Camera.

---

## 3. Toán học Vector (Raymath)

Trong game 2D, chúng ta rất hiếm khi thao tác lẻ tẻ biến `x` và `y`. Chúng ta thao tác trực tiếp trên `Vector2`. 
Ngôn ngữ Odin đã tự động tích hợp sẵn các hàm toán học này vào thư viện `rl` (`vendor:raylib`).

* **Tính khoảng cách: `Vector2Distance(v1, v2: Vector2) -> f32`**
  * Dùng để biết kẻ địch có đang ở gần người chơi để lao vào tấn công không.
  ```odin
  if rl.Vector2Distance(player_pos, enemy_pos) < 100 { enemy_attack() }
  ```

* **Chuẩn hóa hướng đi: `Vector2Normalize(v: Vector2) -> Vector2`**
  * **CỰC KỲ QUAN TRỌNG:** Nếu người chơi bấm nút Đi Lên (W) và Đi Phải (D) cùng lúc, nhân vật sẽ đi chéo. Theo định lý Pytago, vận tốc chéo sẽ dài hơn (~1.414 lần) vận tốc đi thẳng. 
  * Để tránh việc đi chéo nhanh hơn đi thẳng, bạn **phải** Normalize (Đưa độ dài vector về đúng bằng 1) trước khi nhân với `speed`.
  ```odin
  dir := rl.Vector2{0, 0}
  if rl.IsKeyDown(.W) { dir.y -= 1 }
  if rl.IsKeyDown(.S) { dir.y += 1 }
  if rl.IsKeyDown(.A) { dir.x -= 1 }
  if rl.IsKeyDown(.D) { dir.x += 1 }

  if rl.Vector2Length(dir) > 0 { // Phải kiểm tra độ dài > 0 trước khi Normalize
      dir = rl.Vector2Normalize(dir)
  }
  
  player_pos += dir * speed * dt // Di chuyển an toàn
  ```

* **Tính toán vector trỏ từ điểm A đến điểm B: `Vector2Subtract(target, origin)`**
  * Nếu bạn muốn viên đạn bay từ nòng súng về phía con trỏ chuột, bạn lấy `MousePos` trừ đi `GunPos`, sau đó Normalize kết quả để lấy "Hướng", rồi nhân với "Vận tốc".

* **Nội suy mượt mà (Lerp): `Vector2Lerp(v1, v2: Vector2, amount: f32)`**
  * Dùng để làm chuyển động mượt (không bị giật cục). Ví dụ: Camera không nhảy cái "bụp" bám sát nhân vật, mà trôi từ từ theo.

---

## 4. Số ngẫu nhiên (Random)

Game không có ngẫu nhiên thì rất nhàm chán.

* **`GetRandomValue(min, max: c.int) -> c.int`**: Lấy số ngẫu nhiên giữa `min` và `max` (bao gồm cả min và max).
* **`SetRandomSeed(seed: c.uint)`**: Nếu bạn truyền vào cùng 1 hạt mầm (seed), chuỗi ngẫu nhiên sinh ra sẽ Y HỆT NHAU. Rất hữu ích khi làm các game sinh tồn có Map Seed (như Minecraft, Terraria).

---

## Bài tập thực hành Chương 3

1. Hãy sửa code di chuyển ở bài trước để nhân vật có thể di chuyển 4 hướng (WASD) mượt mà bằng cách sử dụng `IsKeyDown`.
2. Áp dụng `Vector2Normalize` để đảm bảo tốc độ đi chéo không bị nhanh hơn đi thẳng.
3. Khi bấm phím SPACE (dùng `IsKeyPressed`), hãy đưa nhân vật (bằng cách sửa `player_pos`) dịch chuyển ngẫu nhiên đến một toạ độ bất kỳ trên màn hình (dùng `GetRandomValue`).
4. (Nâng cao) Vẽ một vạch kẽ (`DrawLineEx`) nối từ nhân vật đến vị trí con trỏ chuột. Vạch này sẽ biến đổi màu thành `RED` nếu chuột nằm trong bán kính 150 pixel so với nhân vật (dùng `Vector2Distance`), ngược lại nó màu `GRAY`.
