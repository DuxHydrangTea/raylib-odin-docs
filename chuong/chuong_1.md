# Chương 1: Nền tảng cốt lõi và Vòng lặp Game (Game Loop)

Chào mừng bạn đến với Chương 1! Trong chương này, chúng ta sẽ xây dựng những viên gạch đầu tiên cho bất kỳ tựa game 2D nào: Khởi tạo cửa sổ, giữ cho game chạy liên tục với vòng lặp chính (Game Loop), tìm hiểu các cấu trúc dữ liệu quan trọng nhất và cách xử lý chuỗi an toàn trong Odin.

---

## 1. Cấu trúc dữ liệu cốt lõi (Core Structs)

Khi làm game 2D bằng Raylib, bạn sẽ thường xuyên làm việc với 3 kiểu dữ liệu sau đây. Chúng là "linh hồn" của hệ thống tọa độ và hình học.

* **`Vector2`**: Biểu diễn một điểm hoặc hướng trong không gian 2 chiều.
  * Cấu trúc: `{x, y: f32}`
  * Ứng dụng: Lưu tọa độ (vị trí của nhân vật), vận tốc di chuyển, hoặc kích thước chiều rộng/cao.
  * Ví dụ: `player_pos: rl.Vector2 = {100.5, 200.0}`

* **`Rectangle`**: Biểu diễn một hình chữ nhật.
  * Cấu trúc: `{x, y, width, height: f32}`
  * Ứng dụng: Xác định vùng không gian, vẽ hitbox (hộp va chạm) hoặc để cắt khung hình (spritesheet). `x` và `y` là tọa độ góc trên cùng bên trái.
  * Ví dụ: `hitbox: rl.Rectangle = {10, 10, 50, 50}`

* **`Color`**: Biểu diễn màu sắc.
  * Cấu trúc: `{r, g, b, a: u8}` (Các kênh màu Đỏ, Lục, Lam, và Alpha từ 0 đến 255).
  * Ứng dụng: Raylib có sẵn các hằng số màu rất tiện dụng như `rl.RED`, `rl.RAYWHITE`, `rl.BLUE`, `rl.BLANK` (trong suốt).

---

## 2. Quản lý Cửa sổ & Hệ thống (Window)

Bất kỳ game nào cũng cần một cửa sổ hiển thị.

* **`InitWindow(width, height: c.int, title: cstring)`**
  * Tác dụng: Mở cửa sổ game. Bắt buộc phải gọi hàm này **đầu tiên** trước khi tải bất kỳ ảnh hay âm thanh nào.
  * Ví dụ: `rl.InitWindow(800, 600, "Game Của Tôi")`

* **`WindowShouldClose() -> bool`**
  * Tác dụng: Hàm này kiểm tra xem người chơi có bấm nút [X] ở góc cửa sổ hoặc bấm phím `ESC` hay không.
  * Ứng dụng: Dùng làm điều kiện dừng cho vòng lặp chính (Game Loop).

* **`CloseWindow()`**
  * Tác dụng: Dọn dẹp bộ nhớ và đóng cửa sổ game.
  * Ứng dụng: Gọi ở cuối file `main` bằng từ khóa `defer` để đảm bảo game luôn dọn dẹp sạch sẽ khi thoát.

---

## 3. Vòng lặp Game (Game Loop)

Đây là nhịp tim của mọi trò chơi. Game loop chạy hàng chục (hoặc hàng trăm) lần mỗi giây để liên tục Cập nhật logic (Update) và Vẽ ra màn hình (Draw).

Cấu trúc cơ bản sẽ trông như thế này:

```odin
package game

import rl "vendor:raylib"

main :: proc() {
    // Khởi tạo
    rl.InitWindow(800, 600, "Chương 1")
    defer rl.CloseWindow() // Sẽ chạy tự động trước khi thoát hàm main

    // Vòng lặp chính
    for !rl.WindowShouldClose() {
        // --- 1. UPDATE ---
        // Xử lý di chuyển, kiểm tra phím bấm ở đây...
        
        // --- 2. DRAW ---
        rl.BeginDrawing()
            rl.ClearBackground(rl.RAYWHITE) // Rất quan trọng: Xoá khung hình cũ!
            
            // Vẽ các thứ ra màn hình...
            rl.DrawRectangle(100, 100, 50, 50, rl.RED)
            
        rl.EndDrawing()
    }
}
```
**Lưu ý:** `rl.ClearBackground()` là cực kì cần thiết ở đầu mỗi bước vẽ để xoá đi tàn dư của khung hình cũ (tránh hiện tượng bóng mờ - ghosting).

---

## 4. In Log & Debug hệ thống

Thay vì dùng `fmt.println`, Raylib cung cấp hệ thống in log mạnh mẽ hơn:

* **`TraceLog(logLevel: TraceLogLevel, text: cstring, ...)`**
  * Các mức độ log: `.INFO` (thông tin), `.WARNING` (cảnh báo), `.ERROR` (lỗi), `.FATAL` (lỗi nghiêm trọng).
  * Ví dụ: `rl.TraceLog(.INFO, "Nhân vật đã được tạo thành công!")`

---

## 5. Đặc thù Odin: Xử lý chuỗi C-String (CỰC KỲ QUAN TRỌNG)

Raylib là một thư viện viết bằng C. Ngôn ngữ C dùng mảng ký tự kết thúc bằng số 0 (Null-terminated string / C-string) để lưu văn bản. Tuy nhiên, String của Odin lại hoạt động khác (có lưu độ dài cứng).

Do đó, các hàm của Raylib như `rl.InitWindow` hay `rl.DrawText` yêu cầu tham số kiểu `cstring` chứ không phải `string` mặc định của Odin. 

Để xử lý văn bản (đặc biệt là giao diện UI như điểm số thay đổi liên tục), bạn có **2 cách** để tránh crash game hoặc Memory Leak:

### Cách 1: Dùng Temp Allocator cho văn bản thay đổi liên tục (Khuyên dùng cho UI)
Trong Game Loop, điểm số thay đổi từng frame. Bạn hãy dùng bộ nhớ tạm của Odin để ghép chuỗi, sau đó **bắt buộc dọn dẹp** ở cuối vòng lặp.

```odin
import "core:fmt"

for !rl.WindowShouldClose() {
    score := 1500

    rl.BeginDrawing()
        rl.ClearBackground(rl.RAYWHITE)
        
        // Lắp ráp chuỗi trên bộ nhớ tạm (temp_allocator)
        c_str := fmt.ctprintf("Điểm của bạn: %d", score) 
        rl.DrawText(c_str, 10, 10, 20, rl.DARKGRAY)
    rl.EndDrawing()
    
    // LƯU Ý: Phải giải phóng bộ nhớ tạm ở cuối mỗi vòng lặp
    free_all(context.temp_allocator)
}
```

### Cách 2: Clone string động (Cần free thủ công)
Dùng khi bạn nhận nội dung từ file hoặc server và cần giữ lại lâu dài.
```odin
import "core:strings"

str := "Nội dung động từ API"
c_str := strings.clone_to_cstring(str)
defer delete(c_str) // Đừng quên delete nếu không RAM sẽ bị rò rỉ!

rl.TraceLog(.INFO, c_str)
```

---

## Bài tập thực hành Chương 1

1. Hãy tạo một file `main.odin`.
2. Khởi tạo một cửa sổ kích thước 1280 x 720 với tên "Bài Tập Chương 1".
3. Thiết lập vòng lặp game chính.
4. Ở phần vẽ (Draw), hãy vẽ một hình chữ nhật màu `BLUE` tại tọa độ x = 200, y = 200, kích thước 100x100.
5. In ra một dòng log "Trò chơi đã khởi động" bằng `TraceLog`.
6. Biên dịch và chạy thử!

*Nếu bạn đã hoàn thành hoặc gặp khó khăn ở đâu, hãy cho mình biết để cùng sửa lỗi trước khi sang Chương 2 nhé!*
