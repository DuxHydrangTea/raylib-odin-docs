# Vấn Đề 1: Desync (Bất đồng bộ Thế giới)

## 1. Biểu hiện của Lỗi
Đây là lỗi kinh điển nhất của mọi game Multiplayer sơ khai.
- **Trên màn hình của bạn (A):** Bạn đã giết con Quái vật. Xác nó nằm trên đất. Bạn nhặt được vàng.
- **Trên màn hình bạn bè (B):** Con Quái vật vẫn còn sống nhăn răng và đang tấn công bạn.
- Càng chơi lâu, hai máy càng lệch nhau (Butterfly Effect - Hiệu ứng cánh bướm). Cuối cùng game crash hoặc không thể tương tác được nữa.

## 2. Nguyên nhân
Desync thường xảy ra nhiều nhất trong kiến trúc P2P (Lockstep), hoặc khi Client-Server chia sẻ quá nhiều trách nhiệm tính toán vật lý (Ví dụ: Server không gửi tọa độ quái, mà chỉ bảo Client "Con quái bắt đầu đi tới"). Do chênh lệch mili-giây giữa 2 máy, cộng với sai số của dấu phẩy động (Float), toạ độ quái vật trên máy A và máy B sẽ lệch nhau dần dần.

## 3. Cách khắc phục chi tiết

### Giải pháp 1: Chuyển hẳn sang Authoritative Server (Vô phương cứu chữa)
Đừng bắt Client tự tính toán vật lý phức tạp nữa. Bắt Server tính toán toàn bộ, và mỗi 1/30 giây, Server ép Client nhận một tọa độ chính xác tuyệt đối (Snapshot). Cách này triệt tiêu hoàn toàn Desync nhưng bù lại ngốn băng thông mạng.

### Giải pháp 2: Checksum (Kiểm tra chéo)
Nếu bạn vẫn muốn dùng P2P (ví dụ làm game cờ vua, game đối kháng RTS):
- Mỗi khung hình, mỗi máy (A và B) phải tính tổng tất cả các biến quan trọng (Máu, tọa độ, số tiền) rồi băm thành một mã Hash (gọi là **Checksum**).
- Hai máy trao đổi Checksum cho nhau.
- Nếu Checksum của máy A != máy B. Lập tức game tạm dừng và báo lỗi "Bất đồng bộ! Đang tải lại trạng thái gốc...".

### Giải pháp 3: Khử sai số Float (Deterministic Physics)
Nếu dùng P2P, bạn **TUYỆT ĐỐI** không được dùng biến `float32` hoặc `float64` để tính toán vật lý. Mỗi loại CPU (Intel vs AMD) tính toán phép nhân số Float khác nhau vài phần triệu.
- Hãy dùng thư viện Toán học Cố định (Fixed-point Math) thay vì Float. Tất cả các số thập phân đều phải chuyển thành Số nguyên (Ví dụ: tọa độ `X = 1005` thay vì `100.5`).
