# Chương 9: Tối Ưu Băng Thông Mạng (Bandwidth Optimization)

Khi game của bạn có ít người chơi, mọi thứ có vẻ rất tuyệt. Nhưng khi số lượng người chơi trong 1 phòng tăng lên 100 người (như PUBG), Server sẽ chết ngạt vì cạn kiệt Băng thông (Bandwidth). Lúc này, từng byte dữ liệu đều quý giá như vàng.

Lập trình viên sử dụng 4 kỹ thuật chính để vắt kiệt từng bit dữ liệu.

---

## 1. Delta Compression (Nén khác biệt)

Thay vì mỗi lần gửi nguyên một mảng tọa độ `(X, Y, Z)` tốn 12 bytes. 
Nếu người chơi đang đứng im hoặc chỉ nhúc nhích 1 chút xíu, tọa độ của họ hầu như không đổi.

**Giải pháp:** Chỉ gửi những gì THAY ĐỔI (Delta) so với gói tin trước đó.
- Gói 1 (Toàn bộ): `X=100.0, Y=200.0`
- Gói 2 (Delta): `Y_thay_đổi = +0.5`. (Không gửi X vì X không đổi).
- Kết quả: Ta tiết kiệm được một nửa số lượng byte gửi đi!

---

## 2. Quantization (Lượng tử hóa)

Một biến số thực `float32` (ví dụ `100.123456`) tốn tới 4 bytes. Nhưng trong thực tế, mắt người không thể nhận ra sự khác biệt giữa `100.12` và `100.123456` pixel trên màn hình.

**Giải pháp:**
- Giới hạn độ chính xác. Nhân số đó cho 10 (thành `1001.2`).
- Chặt bỏ phần thập phân, ép kiểu về số nguyên ngắn `int16` (2 bytes) thành số `1001`.
- Khi Client nhận được `1001`, nó chia lại cho 10 để thành `100.1`.
- Kết quả: Từ 4 bytes giảm xuống còn 2 bytes (Tiết kiệm 50%!). Kỹ thuật này gọi là Quantization.

---

## 3. Bit-packing (Nhồi nhét Bit)

Nhiều lập trình viên ngây thơ hay gửi các trạng thái Boolean qua mạng:
- `is_jumping: bool` (1 byte)
- `is_shooting: bool` (1 byte)
- `is_crouching: bool` (1 byte)
Tốn tổng cộng 3 bytes. Đây là sự lãng phí khủng khiếp! Bản chất của boolean chỉ cần 1 Bit (0 hoặc 1). Nhưng máy tính luôn cấp phát tối thiểu 1 Byte (8 bits).

**Giải pháp:**
Dùng phép toán thao tác Bit (`Bitwise Operations`) để nhét 8 biến boolean vào chung MỘT byte duy nhất.

```odin
player_state: u8 = 0

// Gắn cờ Nhảy vào bit đầu tiên
if is_jumping { player_state |= (1 << 0) } 
// Gắn cờ Bắn vào bit thứ hai
if is_shooting { player_state |= (1 << 1) }

// Chỉ cần gửi ĐÚNG 1 BYTE `player_state` qua mạng!
```
Client nhận được 1 Byte này, nó dùng phép toán `AND` (`&`) để giải mã ra lại.

---

## 4. Interest Management (Area of Interest - AoI)

Đây là kỹ thuật mạnh mẽ nhất để cứu sống Server MMORPG.

Giả sử Server có 1000 người chơi trên bản đồ. Nếu Server cập nhật vị trí của 1000 người này cho NHAU mỗi giây:
`1000 người x 1000 gói tin = 1,000,000 gói tin / 1 giây`. Server sẽ sập ngay lập tức!

**Giải pháp (AoI):**
Mắt người chơi không thể nhìn thấy toàn bộ bản đồ. Kẻ địch ở cách xa 5000 mét có nhảy múa hay không thì màn hình Client cũng không thấy.
- Server chia bản đồ thành một "Lưới" (Grid).
- Server kiểm tra: Người chơi A đang đứng ở ô số 5. Nó chỉ lấy những quái vật và người chơi khác nằm ở ô số 5 (hoặc các ô liền kề) để gửi về cho A.
- Những người ở ô số 10, cách quá xa, Server **KHÔNG GỬI** bất kì gói tin nào về cho A.

Nhờ AoI, từ 1,000,000 gói tin, Server có thể chỉ phải gửi vài ngàn gói tin mỗi giây. Kỹ thuật này là bí quyết để các game như Võ Lâm Truyền Kỳ hay WoW có thể chứa cả ngàn người 1 server hồi những năm 2000!
