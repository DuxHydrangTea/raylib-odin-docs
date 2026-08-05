# Chương 16: Giao Diện Người Dùng (UI - HP & MP)

Phần khó nhất khi làm UI trong Raylib không phải là vẽ hình chữ nhật, mà là **Không gian Tọa độ**. 
Lưu ý Tối Quan Trọng: **Mọi lệnh vẽ UI phải nằm NGOÀI khối `BeginMode2D(camera)`**. 
Nếu bạn vẽ thanh máu bên trong khối Camera, thanh máu sẽ dính vào mặt đất và trôi đi mất khi Ninja chạy!

---

## 1. Thanh Máu (HP) và Năng lượng (MP)

Mở `core/game.odin` và chèn đoạn code này xuống dưới lệnh `rl.EndMode2D()` trong hàm `render_game`:

```odin
render_ui :: proc() {
    // 1. Kiểm tra xem Player có tồn tại không
    if len(ecs.entities) == 0 do return
    player_id := ecs.entities[0] // Giả định Player là entity 0
    if player_id not_in ecs.stats do return
    
    s := ecs.stats[player_id]
    
    // Tọa độ tĩnh trên Màn hình máy tính (Không phụ thuộc vào Camera)
    ui_x: i32 = 20
    ui_y: i32 = 20
    bar_width: i32 = 200
    bar_height: i32 = 20
    
    // ==========================================
    // 2. VẼ THANH HP (MÀU ĐỎ)
    // ==========================================
    // Khung nền đen
    rl.DrawRectangle(ui_x, ui_y, bar_width, bar_height, rl.BLACK)
    
    // Tính % HP còn lại
    hp_percent := f32(s.hp) / f32(s.max_hp)
    if hp_percent < 0 do hp_percent = 0
    
    // Vẽ vạch máu
    current_hp_width := i32(f32(bar_width) * hp_percent)
    rl.DrawRectangle(ui_x, ui_y, current_hp_width, bar_height, rl.RED)
    
    // Vẽ Text (100/100) ở giữa thanh
    hp_text := rl.TextFormat("%d / %d", s.hp, s.max_hp)
    rl.DrawText(hp_text, ui_x + 50, ui_y + 2, 16, rl.WHITE)
    
    // ==========================================
    // 3. VẼ THANH MP (MÀU XANH LỤC/LAM)
    // ==========================================
    ui_y += bar_height + 5 // Đẩy xuống dưới thanh máu 5px
    
    rl.DrawRectangle(ui_x, ui_y, bar_width, bar_height, rl.BLACK)
    
    mp_percent := f32(s.mp) / f32(s.max_mp)
    if mp_percent < 0 do mp_percent = 0
    
    current_mp_width := i32(f32(bar_width) * mp_percent)
    rl.DrawRectangle(ui_x, ui_y, current_mp_width, bar_height, rl.BLUE)
    
    mp_text := rl.TextFormat("%d / %d", s.mp, s.max_mp)
    rl.DrawText(mp_text, ui_x + 50, ui_y + 2, 16, rl.WHITE)
}
```

## 2. Vẽ UI Hotkeys (Ô phím tắt kỹ năng)

NSO có giao diện phím tắt góc dưới màn hình. Ta có thể vẽ các ô vuông tượng trưng.

```odin
    // Đoạn này cũng nằm trong render_ui()
    
    screen_h := rl.GetScreenHeight()
    screen_w := rl.GetScreenWidth()
    
    box_size: i32 = 50
    padding: i32 = 10
    
    // Đặt 3 ô kỹ năng ở góc dưới bên phải
    start_x := screen_w - (box_size * 3) - (padding * 2) - 20
    start_y := screen_h - box_size - 20
    
    keys := [3]string{"J (Danh)", "K (Nhay)", "L (Skill)"}
    
    for i in 0..<3 {
        x := start_x + (box_size + padding) * i32(i)
        
        // Vẽ khung
        rl.DrawRectangleLines(x, start_y, box_size, box_size, rl.GRAY)
        
        // Vẽ nút tương ứng
        rl.DrawText(rl.TextFormat("%s", keys[i]), x + 5, start_y + box_size + 5, 10, rl.BLACK)
    }
```

### Kết nối Giao diện vào Update Loop

Nếu bạn muốn khi nhấn phím K thì Nút trên màn hình sáng lên (Feedback trực quan), bạn có thể lấy giá trị `rl.IsKeyDown(.K)` từ vòng lặp Update và đổi màu vẽ `rl.DrawRectangle(..., rl.YELLOW)` tương ứng. 

Phần UI của game C++ tự code thường tốn rất nhiều thời gian tọa độ thủ công. Nếu sau này làm dự án thương mại, bạn nên nghiên cứu các thư viện như `raygui` để tích hợp vào Raylib sẽ nhàn hơn rất nhiều!

Chương 17, chúng ta sẽ viết Cơ chế đi vào Vòng sáng (Portal) để chuyển bản đồ và thuật toán lưu (Save) dữ liệu nhân vật xuống ổ cứng!
