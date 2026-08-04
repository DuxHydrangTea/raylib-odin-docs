# Chương 4: Lập Trình Socket Thực Hành

Để ứng dụng những lý thuyết từ Phần 1, chúng ta sẽ đi vào thực hành lập trình mạng (Network Programming) cơ bản. Trong thế giới lập trình, "cánh cửa" để gửi và nhận dữ liệu ra ngoài Internet được gọi là **Socket**.

---

## 1. Socket Là Gì?

Hãy tưởng tượng máy tính của bạn là một bưu điện, còn **Socket** chính là một hộp thư.
- Khi bạn muốn gửi thư (dữ liệu), bạn bỏ thư vào hộp thư (viết dữ liệu vào Socket), hệ điều hành sẽ lo việc chuyển thư đi.
- Khi có thư gửi đến máy bạn, bưu tá sẽ nhét nó vào hộp thư (Socket), và ứng dụng của bạn (Game) chỉ việc mở hộp thư ra để đọc.

Để tạo một hộp thư, bạn cần 2 thứ:
1. Giao thức sẽ dùng (TCP hay UDP).
2. Port (số phòng) để gắn cái hộp thư đó vào.

---

## 2. Các Bước Khởi Tạo UDP Socket

Khác với TCP cần có bước "Bắt tay" (Handshake) và kết nối (Connect/Accept) lằng nhằng, UDP cực kì đơn giản. Cả Server và Client đều làm những bước tương tự nhau:

1. **Khởi tạo Socket:** Xin hệ điều hành một hộp thư UDP.
2. **Bind (Trói buộc):** Gắn hộp thư đó vào một Port cụ thể trên máy tính.
   - *Với Server:* Phải Bind vào một Port cố định (VD: 7777) để mọi người biết đường gửi tới.
   - *Với Client:* Thường để hệ điều hành tự chọn bừa một Port ngẫu nhiên còn trống.

---

## 3. Vấn Đề Chặn Đứng (Blocking) vs Không Chặn (Non-blocking)

Đây là lỗi phổ biến nhất của người mới học lập trình mạng!

Khi bạn gọi hàm `nhận_dữ_liệu_từ_socket()` (Receive), nếu trong hộp thư chưa có bức thư nào bay tới, mặc định hàm này sẽ **bắt game của bạn đứng im (Freeze)** để chờ cho đến khi có thư mới được chạy tiếp. Cơ chế này gọi là **Blocking**.

Trong Game, vòng lặp (`Game Loop`) phải chạy liên tục 60 khung hình/giây để vẽ hình ảnh và nhận nút bấm bàn phím. Nếu bị đứng im để chờ gói tin mạng, game sẽ bị treo (Not Responding).

**Giải pháp:** Bắt buộc phải thiết lập Socket sang chế độ **Non-blocking** (Không chặn).
- Ở chế độ này, khi gọi hàm `nhận_dữ_liệu_từ_socket()`, nếu có thư thì nó lấy thư, nếu KHÔNG CÓ THƯ, nó sẽ trả về một lỗi kiểu `EAGAIN` (hay `WSAEWOULDBLOCK` trên Windows) và cho phép code chạy tiếp ngay lập tức. Game loop của bạn vẫn sẽ mượt mà.

---

## 4. Polling (Vét Máng Dữ Liệu)

Vì gói tin có thể bay tới máy bạn bất cứ lúc nào với tốc độ cực nhanh, có thể trong 1 khung hình (1/60 giây) có tới 10 gói tin bay đến.
Do đó, ở mỗi đầu khung hình, bạn KHÔNG ĐƯỢC chỉ đọc 1 gói tin. Bạn phải dùng một vòng lặp `while` để "vét" toàn bộ thư trong hộp ra xử lý cho đến khi hộp rỗng. Phương pháp này gọi là **Polling**.

---

## Code Mẫu Bằng Odin (Tạo Server UDP Cơ Bản)

Dưới đây là mã giả (nhưng rất gần với code thật) viết bằng Odin, sử dụng thư viện socket mặc định `core:net` để tạo một Game Server UDP đơn giản.

```odin
import "core:net"
import "core:fmt"

main :: proc() {
    // 1. Tạo và Bind UDP Socket vào Port 7777
    endpoint := net.Endpoint{ address = net.IP4_Any, port = 7777 }
    socket, err := net.bind_udp(endpoint)
    if err != nil {
        fmt.println("Lỗi tạo server!")
        return
    }
    defer net.close(socket)

    // 2. Chuyển Socket sang Non-blocking
    net.set_blocking(socket, false)

    fmt.println("Server đang chạy tại cổng 7777...")

    buffer: [1024]byte // Bộ đệm 1KB để hứng dữ liệu

    // 3. VÒNG LẶP GAME (Game Loop)
    for {
        // [POLLING] Vét toàn bộ gói tin đến
        for {
            bytes_read, remote_endpoint, recv_err := net.recv_udp(socket, buffer[:])
            
            // Nếu không có dữ liệu (EAGAIN/Non-blocking), thoát vòng lặp vét
            if recv_err != nil {
                break
            }

            // Có dữ liệu!
            fmt.printf("Nhận được %d bytes từ %v\n", bytes_read, remote_endpoint)
            
            // TODO: Deserialization (Lấy mảng byte chuyển thành struct Packet)
            // TODO: Cập nhật máu, tọa độ của nhân vật trên Server...
        }

        // [LOGIC] Cập nhật AI, vật lý trên server...

        // [GỬI] Gửi trạng thái mới về lại cho các Client
        // net.send_udp(socket, dữ_liệu, remote_endpoint)
        
        // Ngủ 1 chút để server chạy ở 60 Tick/s
        // time.sleep(16 * time.Millisecond)
    }
}
```

> [!TIP]
> **Quản lý danh sách kết nối (Sessions):** Vì UDP là "Phi kết nối" (Connectionless), nên khái niệm "Client A đã kết nối" không tồn tại sẵn.
> Lập trình viên phải tự tạo một biến `map[net.Endpoint]Player` để lưu danh sách. Mỗi khi nhận được gói tin từ một IP lạ, ta tự thêm IP đó vào map và tạo cho họ một nhân vật mới. Nếu quá 5 giây không nhận được gói tin nào từ IP đó, ta xoá họ khỏi map (Timeout/Disconnect).
