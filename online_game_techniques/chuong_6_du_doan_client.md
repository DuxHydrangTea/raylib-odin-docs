# Chương 6: Dự Đoán Phía Client (Client-Side Prediction & Server Reconciliation)

Chào mừng bạn đến với kỹ thuật "Ma thuật" đầu tiên trong thế giới Game Networking. Kỹ thuật này sinh ra để giải quyết một và chỉ một vấn đề duy nhất: **Input Lag (Độ trễ thao tác)** của chính người chơi.

---

## 1. Nỗi Đau Của Input Lag

Trong kiến trúc Authoritative Server (Chương 2), khi bạn bấm nút `W` (Đi tới), quy trình tốn thời gian như sau:
1. Máy bạn gửi lệnh `[Bấm W]` lên Server (Mất `50ms`).
2. Server duyệt lệnh, tính toán toạ độ mới là `X=10`, gửi kết quả về (Mất `50ms`).
3. Màn hình của bạn nhận kết quả `X=10`, nhân vật bắt đầu bước đi.

**Tổng thời gian:** `100ms` (Bằng đúng Ping của bạn).
Điều này có nghĩa là, bạn bấm nút xong, 1/10 giây sau nhân vật mới nhúc nhích. Cảm giác điều khiển sẽ giống như nhân vật đang lội dưới bùn. Rất kinh khủng!

---

## 2. Giải Pháp: Dự Đoán Phía Client (Client-Side Prediction)

Nếu chúng ta không thể làm cho Internet truyền nhanh hơn tốc độ ánh sáng, tại sao chúng ta không "Dự đoán" tương lai?

Ý tưởng rất đơn giản: 
- Khi bạn bấm nút `W`, Client **KHÔNG CHỜ** Server trả lời nữa. 
- Màn hình của bạn **TỰ ĐỘNG DI CHUYỂN** nhân vật lên phía trước ngay lập tức (Áp dụng vật lý cục bộ).
- Cùng lúc đó, Client vẫn gửi lệnh `[Bấm W]` lên Server.

**Kết quả:** Cảm giác điều khiển mượt mà 100%, y hệt như đang chơi game Offline (Ping 0ms). 

Nhưng khoan đã... Điều gì xảy ra nếu Client đoán sai?

---

## 3. Hoà Giải Với Server (Server Reconciliation)

Giả sử phía trước mặt bạn có một Bức Tường Tàng Hình (mà chỉ Server mới biết). 
- Client tự đoán: "Bấm W thì mình sẽ tiến lên tọa độ `X=10`". 
- Tuy nhiên, Server nhận lệnh `W`, thấy bạn đụng tường, nên Server tính ra kết quả thực tế là `X=5` (Đứng khựng lại).

Khi kết quả của Server (`X=5`) gửi về tới Client, nó sẽ mâu thuẫn với thực tại ảo tưởng của Client (`X=10`). Chuyện gì sẽ xảy ra? **Teleport (Giật lùi)!**
Nhân vật của bạn đang đứng ở 10, đột nhiên bị hệ thống búng ngược về 5.

Để giải quyết việc giật lùi thô bạo này, ta dùng **Server Reconciliation (Hoà giải Server)**.

### Cách thức hoạt động của Server Reconciliation:
Thuật toán này cực kỳ phức tạp và là ác mộng của mọi Lập trình viên game mạng. Nó hoạt động qua 4 bước:

1. **Đánh số Input:** Mỗi khi Client gửi một lệnh, nó gắn một con số (Input ID). 
   - Lệnh thứ 1 (Tiến lên): `ID = 100` -> Client đoán mình tới `X=10`.
   - Lệnh thứ 2 (Tiến lên): `ID = 101` -> Client đoán mình tới `X=20`.
   - Client phải lưu 2 lịch sử này vào một danh sách dự đoán (Pending Inputs).

2. **Server trả kết quả:** Server phản hồi: *"Tao vừa xử lý xong lệnh ID=100 của mày. Kết quả mày đụng tường, X của mày chỉ là 5 thôi."*

3. **Client tua ngược thời gian (Rewind):** Client nhận được phản hồi, nó thấy kết quả `X=5` khác với dự đoán cũ `X=10`.
   - Client buộc phải dời nhân vật về `X=5` (Thời điểm của ID=100).
   - Client vứt bỏ dự đoán sai `ID=100` khỏi danh sách.

4. **Client mô phỏng lại tương lai (Re-simulate):** 
   - Trong danh sách chờ vẫn còn lệnh `ID=101` (chưa được Server duyệt).
   - Client bắt đầu từ `X=5`, tự chạy lại vật lý ảo với lệnh `ID=101`.
   - Kết quả mới: `X=5` (Tiến lên nhưng vẫn kẹt tường).
   - Nhân vật trên màn hình của bạn sẽ nhanh chóng trượt từ 20 về lại 5 cực kỳ mượt (hoặc giật lùi nhẹ nếu quá sai lệch), nhưng thế giới ảo cuối cùng đã đồng nhất với Server!

---

> [!CAUTION]
> **Tóm tắt quy luật vàng:**
> 1. Client tự chạy vật lý cục bộ ngay lập tức để người chơi sướng tay.
> 2. Luôn lưu lại các phím đã bấm (cùng ID) chưa được Server duyệt.
> 3. Khi Server trả về kết quả cũ, so sánh ID. Nếu sai, dời nhân vật về vị trí thật, sau đó Áp dụng lại (Re-apply) toàn bộ các phím chưa được duyệt.
>
> Thuật toán này biến mọi tựa game Lag trở nên cực kì mượt mà!
