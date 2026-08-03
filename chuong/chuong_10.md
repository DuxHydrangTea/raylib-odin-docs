# Chương 10: Tổ chức Code & Tối ưu Bộ nhớ (Odin Đặc quyền)

Chào mừng bạn đến với Chương cuối cùng của lộ trình nâng cao! Ở các chương trước, bạn đã học cách dùng Raylib. Ở chương này, chúng ta sẽ học cách phát huy tối đa sức mạnh của ngôn ngữ **Odin** để kiến trúc hệ thống game không bị rối như tơ vò (spaghetti code) khi dự án phình to.

---

## 1. Tổ chức Game bằng Máy Trạng Thái (State Machine)

Nếu bạn nhét toàn bộ logic của Màn hình chính (Main Menu), Đang chơi (Gameplay), Tạm dừng (Pause), và Thua cuộc (Game Over) vào một hàm `main()` duy nhất, file code của bạn sẽ dài hàng nghìn dòng với hàng đống lệnh `if...else`.

Giải pháp: Sử dụng `enum` và `switch` của Odin để làm **State Machine**.

```odin
package game
import rl "vendor:raylib"

// Định nghĩa các trạng thái
GameState :: enum {
    MAIN_MENU,
    PLAYING,
    PAUSE,
    GAME_OVER,
}

main :: proc() {
    rl.InitWindow(800, 600, "State Machine")
    defer rl.CloseWindow()
    
    current_state := GameState.MAIN_MENU
    
    for !rl.WindowShouldClose() {
        // -------------------------
        // A. CẬP NHẬT LOGIC
        // -------------------------
        switch current_state {
            case .MAIN_MENU:
                if rl.IsKeyPressed(.ENTER) { current_state = .PLAYING }
                
            case .PLAYING:
                if rl.IsKeyPressed(.ESC) { current_state = .PAUSE }
                if player_hp <= 0 { current_state = .GAME_OVER }
                // Update player, enemy...
                
            case .PAUSE:
                if rl.IsKeyPressed(.ESC) { current_state = .PLAYING }
                
            case .GAME_OVER:
                if rl.IsKeyPressed(.ENTER) { current_state = .MAIN_MENU }
        }

        // -------------------------
        // B. VẼ RA MÀN HÌNH
        // -------------------------
        rl.BeginDrawing()
        rl.ClearBackground(rl.RAYWHITE)
        
        switch current_state {
            case .MAIN_MENU:
                rl.DrawText("BẤM ENTER ĐỂ BẮT ĐẦU", 100, 100, 40, rl.BLACK)
                
            case .PLAYING, .PAUSE: // Vẽ Gameplay cho cả 2 trạng thái
                // Vẽ map, player...
                if current_state == .PAUSE {
                    rl.DrawRectangle(0, 0, 800, 600, rl.Fade(rl.BLACK, 0.5)) // Phủ mờ
                    rl.DrawText("ĐANG TẠM DỪNG", 300, 300, 40, rl.WHITE)
                }
                
            case .GAME_OVER:
                rl.DrawText("BẠN ĐÃ CHẾT!", 300, 300, 40, rl.RED)
        }
        rl.EndDrawing()
    }
}
```
*(Thực tế, khi dự án lớn hơn, bạn sẽ tách mỗi cụm `case` thành các hàm riêng biệt `UpdateMainMenu()`, `DrawGameplay()`,... vào các file `.odin` khác nhau).*

---

## 2. Quản lý Bộ nhớ "Đẳng cấp" (Memory Allocators)

Một trong những lý do khiến các Game Engine dùng C++ (hoặc Odin) thay vì C#/Java là khả năng kiểm soát bộ nhớ hoàn toàn, không bị hiện tượng "Giật lag rác" (Garbage Collection Spike).

Ở Chương 1, chúng ta đã làm quen với `temp_allocator` để chứa chuỗi String dùng 1 lần. Nhưng với các mảng (Array) chứa 1000 viên đạn (Bullets) hoặc hạt nổ (Particles) thì sao?

### Sử dụng Context và Arena Allocator
Arena là kỹ thuật xin hệ điều hành một cục RAM bự (vd: 100MB) ngay từ đầu. Sau đó mọi mảng đạn, quái vật đều được khởi tạo bên trong cục 100MB này. Khi chuyển cảnh (sang màn 2), bạn chỉ cần gạt một công tắc là **giải phóng toàn bộ** mà không tốn công dò tìm từng biến!

```odin
import "core:mem"

main :: proc() {
    // Xin 16MB RAM cấp phát 1 lần duy nhất
    arena_buffer := make([]byte, 16 * mem.Megabyte)
    defer delete(arena_buffer)
    
    // Khởi tạo Arena
    arena: mem.Arena
    mem.arena_init(&arena, arena_buffer)
    
    // Chuyển toàn bộ vùng cấp phát mặc định của context sang Arena
    context.allocator = mem.arena_allocator(&arena)
    
    // TỪ BÂY GIỜ, mọi lệnh 'make()' hay 'new()' đều lấy RAM từ Arena siêu tốc
    bullets := make([dynamic]Bullet)
    
    for !rl.WindowShouldClose() {
        // Game Loop...
        
        // Khi người chơi chuyển cảnh (qua Màn 2)
        if level_completed {
            // "Quét dọn" sạch sẽ toàn bộ quái vật, vật phẩm màn cũ TRONG 1 NỐT NHẠC
            mem.arena_free_all(&arena)
            
            // bullets cũ đã bị xóa, khởi tạo mảng mới cho màn 2
            bullets = make([dynamic]Bullet) 
        }
    }
}
```

Việc sử dụng **Context Allocator** là sức mạnh độc quyền giúp mã nguồn Odin của bạn chạy nhanh ngang ngửa C/C++ thuần túy, nhưng lại an toàn và nhàn hạ hơn rất nhiều.

---

### Lời kết cho Lộ trình Nâng cao
Đến đây, bạn đã nắm vững từ kỹ năng thao tác Đồ hoạ cấp thấp (Shader, Texture) đến Kiến trúc hệ thống (State Machine, Arena Memory). Cánh cổng tạo ra các tựa game hiệu suất cao và chuẩn thương mại bằng Raylib + Odin đã hoàn toàn mở rộng! Chúc bạn chinh phục thành công!
