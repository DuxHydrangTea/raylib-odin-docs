# Chương 2: Kiến Trúc Mạng Trong Game (Network Architectures)

Sau khi đã hiểu TCP và UDP, câu hỏi tiếp theo là: Làm sao để nhiều máy tính kết nối lại với nhau và thống nhất được luật chơi? Có 2 trường phái kiến trúc chính từng thống trị thế giới game.

---

## 1. Mô Hình Peer-to-Peer (P2P) Lockstep

Đây là kiến trúc cổ điển, thường thấy ở các game chiến thuật thời gian thực (RTS) ngày xưa như *Age of Empires (Đế chế)*, *StarCraft 1*, hoặc các game đối kháng (Fighting).

### Cơ chế hoạt động
Trong mô hình P2P, **không có máy chủ trung tâm (No Server)**. Tất cả máy người chơi (Client) sẽ tự kết nối chéo với nhau thành một mạng nhện.
- **Lockstep:** Mỗi bước thời gian (Turn/Tick), các máy sẽ gửi phím bấm (Input) của mình cho tất cả các máy còn lại.
- Trò chơi bị "khóa" (Lock). Máy A chỉ thực thi kết quả của Tick 1 nếu nó đã nhận đủ Input của cả máy B, C, D.
- Vì tất cả các máy cùng chạy một mã code giống nhau y hệt (Deterministic), nên nếu chúng nhận cùng Input, chúng sẽ ra cùng kết quả (Vị trí quân lính, máu, sát thương).

### Ưu điểm
- Chỉ tốn rất ít băng thông. Game chỉ cần truyền lệnh (vd: "Tạo lính ở nhà chính") chứ không truyền tọa độ chi tiết của 1000 con lính.
- Nhà phát hành không tốn tiền nuôi Server đắt đỏ (chỉ cần 1 server mồi để matchmaking).

### Nhược điểm (Lý do nó chết dần)
- **Dễ bị hack (Desync):** Nếu một người chơi dùng phần mềm sửa đổi chỉ số quân lính trên máy của họ, máy họ sẽ tính toán ra kết quả khác máy người khác. Dẫn tới hiện tượng "Desync" (Bất đồng bộ) -> Văng game.
- **Phụ thuộc vào người yếu nhất:** Nếu 1 người bị lag, game của TẤT CẢ mọi người sẽ bị khựng lại chờ người đó (Waiting for other players...).

---

## 2. Mô Hình Client - Server

Đây là mô hình tiêu chuẩn hiện đại, áp dụng cho 99% game online ngày nay từ *CS:GO, Valorant* đến *MMORPG*.

### Cơ chế hoạt động
Có một máy chủ mạnh mẽ đặt tại trung tâm (Data Center). Tất cả người chơi (Clients) không kết nối với nhau, mà chỉ kết nối với duy nhất Server này.
- Máy A gửi hành động tới Server.
- Server tính toán kết quả, rồi thông báo cho máy A, B, C biết.

---

## 3. Authoritative Server (Máy chủ độc tài)

Trong mô hình Client-Server, khái niệm **Authoritative Server** là chìa khóa chống hack. 
"Authoritative" có nghĩa là: **Server không bao giờ tin tưởng Client**.

### Dumb Client (Client mù quáng)
- Client không được phép nói: *"Tao đang ở tọa độ X=100, máu tao 9999"*. Nếu cho phép, Hacker sẽ gửi luôn gói tin này lên để bất tử.
- Thay vào đó, Client (Dumb Client) chỉ được phép gửi nút bấm (Input): *"Tao bấm phím W, tao click chuột trái"*.
- Server nhận được phím W, Server tính toán: *"Người chơi A đi tới X=100, tao thấy trước mặt nó có quái, tao cho nó bị trừ 10 máu"*.
- Server gửi kết quả về lại Client: *"Vị trí mới của mày là 100, máu còn 90"*. Client ngoan ngoãn vẽ lại hình ảnh lên màn hình theo lời Server.

### Tại sao lại gọi là "Dumb" Client?
Vì Client về cơ bản chỉ là một "Cái màn hình + Bàn phím". Mọi logic game (Va chạm, sát thương, máu) đều do Server chạy mô phỏng ngầm (Headless) bằng vật lý riêng của nó.

### Nhược điểm lớn nhất: Delay (Độ trễ)
Vì Client phải chờ Server phán quyết, nên từ lúc bấm phím W đến lúc nhân vật nhúc nhích trên màn hình sẽ có độ trễ bằng với Ping của mạng. 
- *Ví dụ:* Ping 100ms. Bấm W -> 50ms bay lên Server -> Server duyệt -> 50ms kết quả bay về -> Nhân vật mới di chuyển. Điều này gây ra cảm giác cực kì giật, khó chịu.

> [!NOTE]
> Để giải quyết nhược điểm "Delay" của Authoritative Server mà vẫn giữ được tính chống hack, lập trình viên phát minh ra các thuật toán cao cấp (như **Client-side Prediction**). Chúng ta sẽ tìm hiểu chi tiết điều này ở Phần 3.
