# Bài 1: Khởi tạo Project, State Machine và Game Loop

Chào mừng bạn đến với khóa Thực hành Code Game Nông Trại 2D! Thay vì lý thuyết suông, trong chuỗi bài này, chúng ta sẽ mở VSCode lên, tạo file và gõ code thật sự. Kết thúc chuỗi bài, bạn sẽ có một con game nông trại mini chơi được.

## 1. Cấu trúc thư mục chuẩn
Tạo một thư mục mới mang tên `my_farm_game` trên máy bạn. Tạo file `main.odin` bên trong nó.

```text
my_farm_game/
└── main.odin
```

## 2. Khung xương cơ bản của Raylib (Game Loop)
Hãy bắt đầu với những dòng code cơ bản nhất. Khởi tạo cửa sổ màn hình và vòng lặp chính.

Mở file `main.odin` và chép đoạn code sau:

```odin
package main

import "core:fmt"
import rl "vendor:raylib"

// Các hằng số cấu hình màn hình
SCREEN_WIDTH  :: 800
SCREEN_HEIGHT :: 600

main :: proc() {
    // 1. Khởi tạo cửa sổ game
    rl.InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Thực hành Game Nông Trại 2D")
    defer rl.CloseWindow() // Đảm bảo đóng cửa sổ khi tắt game

    // Chỉnh tốc độ khung hình (FPS) mượt mà
    rl.SetTargetFPS(60)

    // 2. Vòng lặp chính của Game (Game Loop)
    for !rl.WindowShouldClose() {
        
        // --- PHẦN 1: CẬP NHẬT LOGIC (UPDATE) ---
        dt := rl.GetFrameTime() // Lấy thời gian trôi qua giữa 2 frame (Delta time)
        
        // (Chúng ta sẽ viết code di chuyển nhân vật ở đây sau)


        // --- PHẦN 2: VẼ ĐỒ HỌA (RENDER) ---
        rl.BeginDrawing()
        rl.ClearBackground(rl.RAYWHITE) // Dọn sạch màn hình cũ bằng màu trắng

        // Test vẽ một dòng chữ ra giữa màn hình
        rl.DrawText("Chao mung den voi Nong Trai!", 250, 300, 20, rl.DARKGRAY)

        rl.EndDrawing()
    }
}
```

Hãy mở Terminal, gõ lệnh `odin run .` và bạn sẽ thấy một cửa sổ màu trắng hiện lên. Xin chúc mừng, bạn đã có Game Loop!

## 3. Thiết kế State Machine đơn giản
Trong game thực tế, bạn không nhảy bộp vào Nông Trại ngay. Bạn phải qua Màn Hình Chính (Title Screen), rồi mới bấm "Chơi". Ta gọi đó là các Trạng Thái (States).

Hãy nâng cấp `main.odin` một chút:

```odin
package main

import rl "vendor:raylib"

SCREEN_WIDTH  :: 800
SCREEN_HEIGHT :: 600

// Định nghĩa các trạng thái của Game
GameState :: enum {
    TITLE_SCREEN, // Màn hình menu
    PLAYING,      // Đang chơi game
}

// Biến lưu trạng thái hiện tại
current_state : GameState = .TITLE_SCREEN

main :: proc() {
    rl.InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Thực hành Game Nông Trại 2D")
    defer rl.CloseWindow()
    rl.SetTargetFPS(60)

    for !rl.WindowShouldClose() {
        dt := rl.GetFrameTime()

        // --- UPDATE LOGIC DỰA TRÊN STATE ---
        switch current_state {
        case .TITLE_SCREEN:
            // Bấm phím ENTER để vào game
            if rl.IsKeyPressed(.ENTER) {
                current_state = .PLAYING
            }
        case .PLAYING:
            // Sẽ chứa logic trồng cây ở các bài sau
            // Bấm ESC để quay lại (Raylib mặc định dùng ESC để thoát, ta tạm dùng phím B)
            if rl.IsKeyPressed(.B) {
                current_state = .TITLE_SCREEN
            }
        }

        // --- RENDER ĐỒ HỌA DỰA TRÊN STATE ---
        rl.BeginDrawing()
        rl.ClearBackground(rl.RAYWHITE)

        switch current_state {
        case .TITLE_SCREEN:
            rl.ClearBackground(rl.DARKBLUE)
            rl.DrawText("GAME NONG TRAI AVATAR 2D", 200, 250, 30, rl.YELLOW)
            rl.DrawText("Nhan ENTER de bat dau", 250, 300, 20, rl.WHITE)
            
        case .PLAYING:
            rl.ClearBackground(rl.GREEN) // Màu nền cỏ
            rl.DrawText("Dang o trong Nong Trai...", 10, 10, 20, rl.BLACK)
            rl.DrawText("Nhan B de quay lai Menu", 10, 40, 20, rl.DARKGRAY)
        }

        rl.EndDrawing()
    }
}
```

**Thử nghiệm:** Chạy game (`odin run .`). Màn hình đầu tiên màu xanh đậm. Bấm `ENTER`, nó chuyển sang màu xanh lá! Bấm phím `B`, nó lùi về Menu.

Khung xương của bạn đã xong. Ở **Bài 2**, chúng ta sẽ tải ảnh (Texture) vào để vẽ lưới đất và nhân vật thay vì những dòng chữ khô khan này.
