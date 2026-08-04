# Chương 1: Cơ Bản Về Mạng Cầu Nối (Networking Basics)

Để bắt đầu làm game online, chúng ta cần nắm vững các thuật ngữ và công nghệ lõi chịu trách nhiệm luân chuyển dữ liệu từ máy người chơi này sang máy người chơi khác.

## 1. Khái Niệm Cơ Bản

### Địa chỉ IP & Port (Cổng)
- **IP Address (Địa chỉ IP):** Giống như địa chỉ nhà của máy tính bạn trên không gian mạng. Để hai máy tính nói chuyện được với nhau, chúng phải biết địa chỉ IP của đối phương.
  - *Ví dụ:* `192.168.1.15` (IPv4) hoặc `::1` (IPv6).
- **Port (Cổng):** Nếu IP là số nhà, thì Port là "số phòng" bên trong tòa nhà đó. Một máy tính chạy rất nhiều ứng dụng cùng lúc (Lướt web, nghe nhạc, chơi game). Port giúp hệ điều hành biết gói tin này đang gửi cho ứng dụng nào.
  - *Ví dụ:* Game của bạn chạy ở Port `7777`. Vậy dữ liệu gửi đến máy bạn sẽ mang địa chỉ `192.168.1.15:7777`.

### LAN, WAN và NAT
- **LAN (Local Area Network):** Mạng nội bộ (trong cùng một nhà/công ty). Các máy tính cắm chung 1 cục router sẽ có IP LAN (thường bắt đầu bằng `192.168...`). Chúng có thể dễ dàng kết nối trực tiếp với nhau.
- **WAN (Wide Area Network):** Mạng Internet rộng lớn.
- **NAT (Network Address Translation):** Do địa chỉ IPv4 trên thế giới đã cạn kiệt, các nhà mạng dùng NAT để gộp hàng ngàn máy tính chung một địa chỉ IP Public. Đây là lý do tại sao hai máy tính cá nhân ở hai nhà khác nhau **không thể** tự do kết nối trực tiếp với nhau, mà thường phải thông qua một Server trung gian trên Cloud.

---

## 2. TCP vs UDP: Cuộc Chiến Bất Tận Trong Game

Mọi dữ liệu trên Internet đều được đóng gói thành các "Gói tin" (Packets) và gửi đi bằng 2 giao thức chính: **TCP** và **UDP**.

### TCP (Transmission Control Protocol)
- **Đặc điểm:** Tuyệt đối an toàn. Chắc chắn gửi tới nơi. Đảm bảo đúng thứ tự.
- **Cách hoạt động:** Khi A gửi cho B, B phải nhắn lại "Tôi nhận được rồi". Nếu A không thấy B nhắn lại, A sẽ gửi lại gói đó cho đến khi B nhận được. Nếu gửi gói số 1, 2, 3 mà gói 2 bị kẹt, gói 3 sẽ phải đứng đợi ở máy B cho đến khi gói 2 tới nơi.
- **Nhược điểm:** Chậm. Gây ra hiện tượng "nghẽn cổ chai" (Head-of-line blocking).
- **Ứng dụng:**
  - Login (Đăng nhập, đăng ký).
  - Chat (Kênh thế giới).
  - Game Turn-based (Đánh theo lượt như Hearthstone, Cờ liên quân) vì độ trễ 1-2 giây không ảnh hưởng tới gameplay.

### UDP (User Datagram Protocol)
- **Đặc điểm:** Siêu nhanh, liều mạng. Gửi xong là quên luôn (Fire and Forget).
- **Cách hoạt động:** A cứ liên tục ném dữ liệu cho B. Không cần quan tâm B có nhận được không, cũng không quan tâm thứ tự gói 1, 2, 3 có lộn xộn không. Gói nào rớt mạng thì mất luôn.
- **Ưu điểm:** Độ trễ (Latency/Ping) cực kỳ thấp. Không bị đứng hình chờ gói tin cũ.
- **Ứng dụng:** BẮT BUỘC dùng cho game Real-time (FPS bắn súng, MOBA Liên Minh Huyền Thoại, đua xe). 
  - *Lý do:* Giả sử gói tin "Vị trí người chơi lúc giây thứ 1" bị rớt, thì ta không cần bắt hệ thống gửi lại, vì lúc nó gửi lại đến nơi thì người chơi đã đi tới vị trí của giây thứ 2 mất rồi! Dữ liệu cũ đã trở nên vô nghĩa.

---

## 3. RUDP (Reliable UDP) - Giải Pháp Hoàn Hảo

Nếu dùng UDP thì sẽ bị mất gói tin, nhưng trong game FPS, đôi khi có những gói tin bắt buộc không được mất (Ví dụ: Gói tin báo "Người chơi A đã chết", hoặc "A vừa đổi súng").

Vậy phải làm sao? Lập trình viên game đã tạo ra một thứ gọi là **RUDP (Reliable UDP)**.
- Về bản chất, nó vẫn là UDP (gửi siêu tốc, bỏ qua thứ tự).
- NHƯNG, lập trình viên sẽ tự code thêm một cơ chế riêng: Nếu gói tin đó được đánh dấu là `RELIABLE` (Đáng tin cậy), thì người nhận sẽ phản hồi lại (ACK). Nếu không thấy phản hồi, Server sẽ tự gửi lại riêng gói đó.

Hầu hết các thư viện mạng làm game ngày nay (ENet, KCP, LiteNetLib, hay `bnet` của Odin) đều là **RUDP**.

---

> [!TIP]
> **Quy tắc vàng trong lập trình Game Online:** Luôn luôn dùng **UDP** làm nền tảng truyền tải dữ liệu game loop (Movement, Combat). TCP chỉ dùng làm cầu kết nối riêng cho tải dữ liệu tĩnh (như hình ảnh avatar, cập nhật file).
