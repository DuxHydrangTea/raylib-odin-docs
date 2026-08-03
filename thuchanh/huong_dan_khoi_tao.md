# Hướng dẫn Khởi động Dự án - 3 Bước Đầu Tiên

Chào mừng bạn đến với phần thực hành! Để bắt đầu bất kỳ một dự án Game 2D nào với Raylib và Odin, chúng ta luôn cần một bộ khung (boilerplate) vững chắc. 

Dưới đây là tài liệu hướng dẫn chi tiết về **3 bước đầu tiên** vô cùng quan trọng để cấu hình trước khi trò chơi thực sự bắt đầu.

---

## 1. Định nghĩa hằng số toàn cục

Thay vì viết cứng các con số như `800`, `600` rải rác khắp nơi trong code (được gọi là magic numbers), chúng ta nên định nghĩa chúng thành các hằng số ngay đầu file. Điều này giúp bạn dễ dàng thay đổi độ phân giải hoặc tên game sau này mà không cần dò tìm từng dòng.

Trong Odin, hằng số được định nghĩa bằng dấu `::`.

```odin
package game

import rl "vendor:raylib"

// Các hằng số toàn cục
WINDOW_WIDTH  :: 1280
WINDOW_HEIGHT :: 720
GAME_TITLE    :: "Dự án Game 2D Đầu Tiên"
```

---

## 2. Khởi tạo Hệ thống và Cửa sổ

Mọi thứ đều bắt đầu bằng một cửa sổ. Đây là nơi GPU sẽ vẽ hình ảnh lên đó.

* **`InitWindow`**: Hàm này mở cửa sổ và khởi tạo context đồ họa (OpenGL) đằng sau nó. Bắt buộc phải gọi hàm này trước khi bạn muốn dùng bất kỳ tính năng đồ họa nào.
* **`defer CloseWindow()`**: Một tính năng tuyệt vời của Odin. Khi bạn dùng `defer`, câu lệnh này sẽ bị trì hoãn và được gọi tự động ngay trước khi hàm `main()` kết thúc. Nó đảm bảo rằng dù game có bị crash hay thoát ra bằng cách nào, cửa sổ và RAM cũng sẽ được dọn dẹp sạch sẽ.

```odin
main :: proc() {
    // Gọi hàm khởi tạo cửa sổ
    rl.InitWindow(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
    
    // Đảm bảo dọn dẹp cửa sổ khi người chơi thoát game
    defer rl.CloseWindow() 
}
```

---

## 3. Khởi tạo Hệ thống Âm thanh

Raylib quản lý âm thanh thông qua một thiết bị (Audio Device). Nếu bạn không khởi động thiết bị này mà lại cố gắng tải một file nhạc (LoadSound / LoadMusicStream), game của bạn sẽ văng (crash) ngay lập tức!

* **`InitAudioDevice`**: Bật card âm thanh và chuẩn bị loa để phát nhạc.
* **`defer CloseAudioDevice()`**: Tương tự như cửa sổ, luôn luôn nhớ dùng `defer` để tắt thiết bị âm thanh khi thoát game.

```odin
main :: proc() {
    // ... (Code khởi tạo cửa sổ nằm ở đây) ...

    // Bật hệ thống âm thanh
    rl.InitAudioDevice()
    
    // Đảm bảo tắt thiết bị âm thanh khi thoát game
    defer rl.CloseAudioDevice()
    
    // ---------------------------------------------------------
    // Tới đây, toàn bộ Màn hình và Loa đã sẵn sàng.
    // Bước tiếp theo (Phần 4, 5, 6...) sẽ là thiết lập FPS, 
    // load hình ảnh và chạy vòng lặp Game Loop!
    // ---------------------------------------------------------
}
```

---

## Bài Tập Thực Hành

Bạn hãy thử tự tạo một file `main.odin` trong folder này, sau đó gõ lại thủ công 3 bước trên (đừng copy/paste nhé, gõ lại sẽ giúp bạn nhớ lâu hơn). 

Sau khi gõ xong, bạn có thể chạy thử bằng lệnh `odin run .`. Game sẽ chớp hiện ra cửa sổ rồi tắt ngay (do chúng ta chưa viết Vòng lặp Game), nhưng nếu không có dòng báo lỗi nào màu đỏ trong Terminal, tức là bạn đã cấu hình 3 bước khởi tạo thành công mỹ mãn!
