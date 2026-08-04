# Vấn Đề 6: NAT Traversal Thất Bại (Không Thể Kết Nối P2P)

## 1. Biểu hiện của Lỗi
Bạn viết xong một game Co-op 2 người (mô hình P2P Host-Client). 
Bạn làm Host trên máy tính ở nhà. Game báo IP của bạn là `192.168.1.15`.
Bạn đưa IP đó cho bạn bè ở nhà khác. Họ gõ IP vào và... vòng tròn Loading quay vô tận. Kết nối thất bại (Connection Timeout).

## 2. Nguyên nhân: Cục Router và NAT
Cái IP `192.168.1.15` là **IP Nội Bộ (LAN)**, chỉ những ai xài chung cục Wifi với bạn mới thấy được.
Bên ngoài Internet, cục Router của nhà mạng đã bọc máy tính của bạn lại bằng một lớp giáp gọi là **NAT (Network Address Translation)** và thay bằng một địa chỉ Public (Ví dụ: `14.232.xxx.xxx`).

Nhưng kể cả khi bạn đưa IP Public đó cho bạn bè, cục Router ở nhà bạn thấy một gói tin lạ bay từ ngoài Internet vào, nó sẽ lập tức chặn lại và vứt đi (Drop) vì lý do bảo mật (Firewall).

## 3. Cách khắc phục chi tiết

Có 3 cách từ thấp đến cao để vượt qua bức tường NAT này.

### Cách 1: Port Forwarding (Mở Port thủ công)
- Bạn truy cập vào trang quản trị cục Router Wifi ở nhà (thường là `192.168.1.1`).
- Mở tính năng NAT/Port Forwarding. 
- Thiết lập: "Bất cứ ai gửi dữ liệu vào Port 7777 ở bên ngoài, hãy tuồn nó thẳng vào máy tính có IP nội bộ 192.168.1.15".
- **Nhược điểm:** Phức tạp, người chơi bình thường không biết chỉnh Router, và rất nguy hiểm cho bảo mật.

### Cách 2: NAT Punch-through (Đục lỗ Tường lửa bằng UDP)
Đây là cách phổ biến nhất để 2 máy tính sau lưng Router có thể kết nối với nhau.
Bạn cần thuê 1 Server rẻ tiền trên Cloud đóng vai trò **STUN Server** (Người mai mối).
1. Máy A gửi 1 gói UDP cho Server. Khi UDP bay ngang qua cục Router của A, Router vô tình **đục 1 cái lỗ** để chờ Server phản hồi lại. Máy B cũng làm y hệt.
2. Server nhìn thấy IP Public và số hiệu "cái lỗ" của A và B. Server gửi thông tin này cho 2 bên.
3. Máy A bắt đầu ném gói tin trực tiếp vào "cái lỗ" của cục Router nhà máy B.
4. Chúc mừng, A và B đã kết nối P2P thành công!

### Cách 3: Relay Server (Giải pháp tối hậu)
Khoảng 20% các cục NAT trên thế giới là loại NAT vô cùng nghiêm ngặt (Symmetric NAT), không cho phép Đục lỗ kiểu trên.
Lúc này bắt buộc phải dùng **Relay Server (hay TURN Server)**.
- Relay Server nằm trên Cloud.
- A gửi dữ liệu cho Relay Server. Relay Server gửi lại cho B.
- Máy chủ sẽ chịu toàn bộ chi phí băng thông của A và B. (Cách này tốn tiền mua băng thông mạng nhất, nhưng chắc chắn 100% kết nối thành công, Discord Voice Call đang dùng cách này).
