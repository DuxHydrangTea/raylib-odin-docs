# Vấn Đề 8: Rớt phím bấm (Input Dropping)

**Vấn đề:**
Người chơi bấm phím Cách (Space) để nhảy, nhưng đôi lúc bấm mạnh mà nhân vật không nhảy. Rất ức chế.

**Nguyên nhân:**
Thường xảy ra khi bạn gọi hàm đọc Input (`rl.IsKeyPressed`) **sai chỗ**, ví dụ như gọi nó bên trong các hàm xử lý Physics (chạy theo FixedUpdate) hoặc gọi nó sau nhiều lệnh rẽ nhánh `if` có thể bị bỏ qua. 
Hàm `IsKeyPressed` chỉ lưu trạng thái phím ĐÚNG trong 1 frame duy nhất. Nếu bạn không đọc nó ngay, frame sau nó sẽ biến mất.

**Giải pháp:**
1. Thu thập toàn bộ Input vào một Struct ngay từ đầu vòng lặp Game.
2. Lưu các trạng thái nút bấm (Button down, Button Just Pressed) vào các biến bool.
3. Truyền các biến bool đó xuống cho các hàm cấp thấp xử lý thay vì gọi trực tiếp `rl.IsKeyPressed` ở khắp mọi nơi.

```odin
InputState :: struct {
    jump_pressed: bool,
    attack_pressed: bool,
    move_dir: rl.Vector2,
}

// Đầu vòng lặp (Main Loop)
current_input := InputState {
    jump_pressed = rl.IsKeyPressed(.SPACE),
    attack_pressed = rl.IsMousePressed(.LEFT),
    // ...
}

// Bất kì hàm nào cần kiểm tra phím đều đọc từ current_input
update_player(&player, current_input)
```
