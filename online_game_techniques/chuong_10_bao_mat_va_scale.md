# Chương 10: Bảo Mật Hệ Thống & Scale (Security & Scaling)

Cuộc hành trình vạn dặm nào cũng phải đến hồi kết. Ở chương cuối cùng, chúng ta sẽ tìm cách bảo vệ thành quả của mình khỏi Hacker và mở rộng hệ thống để phục vụ hàng vạn người chơi.

---

## 1. Bảo Mật: Xác Thực Đầu Vào (Input Validation)

Quy tắc tối thượng: **Không bao giờ tin tưởng Client**.
Dù bạn đã dùng Authoritative Server (Chương 2), Hacker vẫn có thể chế tạo ra các công cụ (Cheat Engine) để gửi những gói tin Input không có thật.

- *Hacker gửi:* `Bấm nút Dịch chuyển đến toạ độ X=9999, Y=9999`.
- *Server xử lý:* Khoan đã, 1 giây trước nó đang ở `X=0`. Không thể nào trong 1 giây mà con người chạy được 9999 mét. Gói tin này vô lý!
- *Kết quả:* Server **Từ chối (Reject)** gói tin đó, và "Dịch chuyển ngược" Hacker về vị trí cũ (Rubber-banding), hoặc thẳng tay Ban (Khóa tài khoản).

Bạn luôn phải viết code kiểm tra vận tốc tối đa, khoảng cách tấn công tối đa, và thời gian Hồi chiêu (Cooldown) trên Server để chặn đứng Speedhack và Teleport.

---

## 2. Packet Encryption & Rate Limiting

Hacker có thể không cần đổi dữ liệu, mà chỉ cần dùng công cụ bắt gói (Wireshark) để xem dữ liệu thô.

**Encryption (Mã hoá):**
- Mọi gói tin nhạy cảm (Đăng nhập, giao dịch) phải được mã hoá (Ví dụ dùng AES, hoặc DTLS). Để dù Hacker có bắt được gói tin, nó cũng chỉ thấy một đống ký tự rác vô nghĩa.

**Rate Limiting (Chống Spam):**
- Kẻ xấu có thể gửi 1 triệu gói tin "Đăng nhập" mỗi giây để đánh sập Server (Tấn công DDoS).
- Bạn phải cài đặt Rate Limiter: Nếu một IP lạ gửi quá 50 gói tin/giây, lập tức chặn (Drop) mọi kết nối từ IP đó ở tầng Tường lửa (Firewall) trước khi gói tin lọt vào Game Server làm nặng CPU.

---

## 3. Kiến Trúc Scale Hệ Thống Multiplayer

Khi game của bạn có 1 triệu người chơi, một cái máy tính (Server) không thể gánh nổi. Bạn phải chia nhỏ chúng ra (Microservices).

### A. Login / Matchmaking Server
Đây là "Bác bảo vệ". Nó chạy bằng giao thức **TCP/HTTP**.
- Người chơi mở game, gửi Request lên Login Server.
- Login Server kiểm tra mật khẩu. Đúng mật khẩu, nó xếp người chơi vào Hàng đợi (Matchmaking).
- Khi tìm đủ 10 người, Matchmaking Server làm gì tiếp theo?

### B. Dedicated Server (Server Chuyên Dụng)
Đây là "Đấu trường". Nó chạy bằng giao thức **UDP**.
- Mỗi trận đấu (Match) 10 người sẽ được cấp phát cho một chương trình Server vô danh (Dedicated Server) chạy ẩn trên Đám mây (Cloud như AWS, Google Cloud).
- Matchmaking Server sẽ báo cho 10 người kia: *"Đã tìm thấy trận! Các bạn hãy kết nối vào địa chỉ IP `102.33.44.55:7777` để bắn nhau nhé!"*
- 10 người rời khỏi Login Server, lao vào Dedicated Server để chơi. Xong trận, Dedicated Server lưu kết quả, tự hủy (Tắt tiến trình) để tiết kiệm tiền điện.

### C. Master Server / Relay Server (Dùng cho P2P)
Nếu bạn không có tiền thuê Cloud Server (như các game Indie hoặc Co-op 2-4 người), bạn dùng mô hình Relay.
- Game sẽ lấy máy tính của **Chủ phòng (Host)** làm Server.
- Những người khác (Client) kết nối vào máy Host.
- **Vấn đề NAT:** Máy Host xài mạng gia đình, có cục NAT che IP, nên không ai kết nối được.
- **Giải pháp:** Bạn thuê một Server nhỏ (Relay Server / STUN Server) làm "Kẻ đưa thư". Nó đục lỗ tường lửa (NAT Punch-through), đứng giữa lấy gói tin từ Client và ném vào nhà của Host, giúp hai bên kết nối P2P thành công mà không cần Dedicated Server tốn kém!

---

> [!TIP]
> **TỔNG KẾT:** Bạn đã đi qua 10 chương từ việc hiểu byte nhị phân, thiết lập Socket, cho đến ảo thuật đồng bộ thời gian và mở rộng hệ thống. Lập trình Game Network là một lĩnh vực cực kỳ phức tạp nhưng cực kỳ thú vị. Hãy bắt tay vào tạo một phòng tập bắn UDP 2 người đơn giản với Odin và Raylib ngay hôm nay!
