# Chương 3: Gói Tin & Truyền Tải Dữ Liệu (Serialization & Packets)

Một khi các máy đã kết nối qua Socket (UDP/TCP), dữ liệu thực tế trôi trên dây mạng cáp quang chỉ là các dòng byte (1 và 0). Chúng ta làm cách nào để nhét nguyên một con quái vật với vị trí, máu, sát thương vào một dòng byte đó để gửi đi?

Đó chính là quá trình **Serialization (Tuần tự hoá)**.

---

## 1. Tuần Tự Hoá (Serialization / Deserialization)
- **Serialization:** Là quá trình "đập bẹp" một Struct/Object trong RAM máy tính (vốn nằm lộn xộn trong bộ nhớ) thành một mảng byte (array of bytes) xếp hàng ngang liên tiếp, để gửi qua dây mạng.
- **Deserialization:** Ở đầu nhận, máy tính đọc mảng byte đó và dựng ngược lại thành Struct/Object ban đầu để dùng trong game.

---

## 2. So Sánh JSON vs Binary

Có 2 trường phái mã hoá dữ liệu phổ biến:

### A. Dạng văn bản (JSON, XML)
```json
{
  "type": "MOVE",
  "x": 120.5,
  "y": 55.2
}
```
- **Ưu điểm:** Con người đọc được (Human readable). Cực kì dễ debug. Dễ mở rộng trường dữ liệu.
- **Nhược điểm:** Rất phình to (Bulky). Chữ `"type"` tốn 6 byte. Các dấu ngoặc nhọn cũng tốn byte. Chuyển đổi chuỗi chữ sang số float (Parsing) cực kỳ tốn CPU.
- **Ứng dụng:** Thường dùng gửi dữ liệu đăng nhập, web API, game thẻ bài nhịp độ chậm.

### B. Dạng nhị phân (Binary Packets)
Thay vì dùng chữ, ta ép trực tiếp byte nhị phân.
Ví dụ gói tin di chuyển trên chỉ mất vỏn vẹn **9 bytes**:
- `1 byte` để lưu Type (ID: `1` = MOVE).
- `4 bytes` lưu toạ độ X (kiểu `float32`).
- `4 bytes` lưu toạ độ Y (kiểu `float32`).
- **Ưu điểm:** Siêu nhỏ, cực kì tiết kiệm băng thông. Tốc độ đọc (deserialization) gần như tức thời vì máy tính chỉ việc đúc thẳng byte vào bộ nhớ (casting).
- **Ứng dụng:** Game Real-time Multiplayer (FPS, MOBA) **bắt buộc** phải dùng Binary Packet để đạt hiệu năng cao nhất.

---

## 3. Cấu Trúc Cơ Bản Của Một Gói Tin (Packet Structure)

Dù gửi bằng TCP hay UDP, một gói tin Binary tiêu chuẩn trong game luôn chia làm 2 phần: **Header** và **Payload**.

### Packet Header (Phần đầu)
Là thông tin hướng dẫn cách đọc gói tin. Thường chứa:
1. **Packet ID / Opcode (1-2 bytes):** Định danh xem gói tin này làm nhiệm vụ gì. 
   - *Ví dụ:* 0x01 là Kết Nối, 0x02 là Bắn Súng, 0x03 là Cập Nhật Vị Trí.
2. **Packet Size / Length (2-4 bytes) (Quan trọng cho TCP):** Kích thước toàn bộ gói tin, để đầu nhận biết đọc tới đâu thì ngắt (đề phòng 2 gói tin dính liền vào nhau).
3. **Sequence Number (2 bytes):** Số thứ tự của gói (Rất quan trọng với UDP để phát hiện gói tin tới sai thứ tự hoặc rớt mạng).

### Packet Payload (Phần thân)
Là dữ liệu thực tế thay đổi tuỳ thuộc vào Packet ID.
- *Nếu ID = Bắn súng:* Payload chứa vị trí viên đạn, ID người bắn.
- *Nếu ID = Chat:* Payload chứa chiều dài chuỗi kí tự và nội dung đoạn chat.

---

## 4. Endianness (Trật tự Byte) - Kẻ Thù Thầm Lặng

Khi gửi dữ liệu Binary giữa 2 máy tính, bạn phải đối mặt với **Endianness**.
Một biến kiểu `int32` (ví dụ số `0x1A2B3C4D`) chiếm 4 bytes. 
- CPU Intel / AMD (Windows, PC) lưu trữ 4 byte này theo kiểu ngược (Little Endian): `4D 3C 2B 1A`.
- Vài loại CPU khác (hoặc chuẩn giao thức mạng) lưu theo chiều thuận (Big Endian): `1A 2B 3C 4D`.

Nếu Client xài Intel gửi cho Server xài kiến trúc khác, Server đúc thẳng 4 byte đó thành số, số đó sẽ bị lộn ngược và sai bét!

> [!WARNING]
> **Cách giải quyết:** Hãy luôn quy định 1 chuẩn (thường là Little Endian vì 99% phần cứng chơi game là Little Endian). Nếu viết server trên ngôn ngữ như Go/Odin, khi nhét số `int32` vào mảng byte, hãy cẩn thận dùng các hàm ghi ép kiểu Little Endian (`encoding/binary` hoặc tương đương).

---

## Code Mẫu Bằng Odin (Tạo gói tin Binary)
Ngôn ngữ Odin hỗ trợ casting thẳng memory sang byte nên viết Binary Packet cực kì dễ và hiệu năng cao không thua gì C/C++.

```odin
import "core:mem"

// 1. Định nghĩa gói tin
PacketMove :: struct #packed {
    packet_id: u8,
    x: f32,
    y: f32,
}

// 2. Chuẩn bị dữ liệu
pack := PacketMove{
    packet_id = 2, // 2 = MOVE
    x = 100.5,
    y = 50.0,
}

// 3. Serialize (Đúc struct thành mảng byte để ném qua Socket)
// Chuyển con trỏ struct thành slice các bytes (len = 9 bytes)
bytes_to_send := mem.byte_slice(&pack, size_of(PacketMove)) 

// Gửi bytes_to_send qua mạng...
```
