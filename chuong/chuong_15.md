# Chương 15: Đa luồng (Multithreading) và Mạng (Networking)

Chào mừng đến với "trùm cuối". Chương này dành cho các bạn muốn viết game Multiplayer (Nhiều người chơi) và các hệ thống tải nền (Background Loading) siêu mượt. Raylib không hỗ trợ mạng, nhưng ngôn ngữ Odin thì có sẵn!

---

## 1. Đa luồng cơ bản (Multithreading)

Khái niệm: Game Loop luôn chạy trên Luồng Chính (Main Thread). Bất kỳ tác vụ nào làm mất hơn 16ms trên luồng chính sẽ làm sụt FPS.
Ví dụ: Bạn cần tải một file Map khổng lồ mất 2 giây. Nếu tải thẳng trong Game Loop, màn hình game sẽ bị đơ hoàn toàn trong 2 giây.

Giải pháp: Đẩy việc tải Map sang một Luồng Nền (Worker Thread). Luồng chính vẫn cứ vẽ chữ "Loading..." quay xoay mượt mà.

### Sử dụng `core:thread` của Odin

```odin
package game

import "core:thread"
import "core:fmt"
import rl "vendor:raylib"

// Biến chia sẻ giữa 2 luồng (Cần cẩn thận vấn đề Race Condition)
is_map_loaded := false

// Hàm sẽ chạy ngầm dưới nền
loading_task :: proc(t: ^thread.Thread) {
    // Giả lập việc tải dữ liệu nặng (Ngủ 3 giây)
    // Thực tế bạn sẽ Parse JSON Map ở đây.
    rl.TraceLog(.INFO, "[THREAD] Đang tải bản đồ siêu nặng...")
    
    // KHÔNG ĐƯỢC GỌI HÀM DRAW VÀ LOAD_TEXTURE TRONG THREAD!
    // GPU Context chỉ dính với luồng chính. Ở đây chỉ tải dữ liệu lên CPU/RAM.
    
    // ... tải xong
    is_map_loaded = true
    rl.TraceLog(.INFO, "[THREAD] Tải xong!")
}

main :: proc() {
    rl.InitWindow(800, 600, "Multithreading")
    defer rl.CloseWindow()
    rl.SetTargetFPS(60)

    // Tạo và khởi chạy Luồng nền
    t := thread.create(loading_task)
    thread.start(t)

    for !rl.WindowShouldClose() {
        rl.BeginDrawing()
        rl.ClearBackground(rl.RAYWHITE)
        
        if !is_map_loaded {
            // Luồng chính không hề bị gián đoạn, chữ vẫn nhấp nháy!
            rl.DrawText("Đang tải dữ liệu...", 300, 300, 20, rl.DARKGRAY)
        } else {
            rl.DrawText("TẢI XONG! BẮT ĐẦU GAME!", 250, 300, 20, rl.GREEN)
        }
        
        rl.EndDrawing()
    }
    
    // Chờ luồng phụ kết thúc và dọn dẹp trước khi tắt app
    thread.join(t)
    thread.destroy(t)
}
```

---

## 2. Lập trình Mạng (Networking) cơ bản

Để làm game nhiều người chơi, cấu trúc tiêu chuẩn là **Server - Client**. Server quản lý tọa độ, Client chỉ việc nhấn nút gửi lên Server và vẽ kết quả.
Game hành động thời gian thực ưu tiên dùng **UDP** vì nó nhanh (bắn trượt gói tin thì bỏ qua luôn), còn game đánh theo lượt dùng **TCP** (đảm bảo không rớt dữ liệu).

### Sử dụng `core:net` để tạo Client UDP đơn giản

```odin
import "core:net"

// (Đây chỉ là mã giả định cấu trúc mạng cơ bản)

main :: proc() {
    // 1. Tạo Socket UDP Client
    endpoint, _ := net.parse_endpoint("127.0.0.1:27015")
    socket, _ := net.dial_udp(endpoint)
    defer net.close(socket)

    // Bật chế độ Non-blocking (Không bắt game phải đứng chờ server phản hồi)
    net.set_blocking(socket, false)

    for !rl.WindowShouldClose() {
        // --- 1. Gửi Input lên Server ---
        if rl.IsKeyPressed(.SPACE) {
            msg := "JUMP\n"
            net.send_udp(socket, transmutate([]u8)(msg), endpoint)
        }

        // --- 2. Nhận kết quả cập nhật từ Server ---
        buf: [1024]byte
        bytes_read, sender_endpoint, err := net.recv_udp(socket, buf[:])
        
        if bytes_read > 0 {
            // Server gửi tọa độ mới về, cập nhật nhân vật...
            // parse_server_data(buf[:bytes_read])
        }

        // --- 3. Vẽ ra màn hình ---
        rl.BeginDrawing()
            // ...
        rl.EndDrawing()
    }
}
```

Viết Server/Client là một bầu trời kiến thức khổng lồ về dự đoán di chuyển (Client Prediction) và nội suy mạng (Network Interpolation) để game không bị giật lag. Kiến thức ở chương này là những viên gạch đầu tiên giúp bạn tự tin khám phá những khái niệm phức tạp đó bằng chính ngôn ngữ Odin.

---
**Chúc mừng bạn đã chinh phục toàn bộ 15 Chương học từ Cơ bản đến Bậc thầy! Chúc bạn tạo ra được những siêu phẩm Game 2D mang đậm dấu ấn riêng!**
