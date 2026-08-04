# Chương 12: Chunking & Quản Lý Bản Đồ (Map Management)

Trong một game MMO Nông trại, một thế giới có thể rộng bằng cả ngàn màn hình, chứa hàng vạn luống đất, hàng rào, vật trang trí, cây ăn quả. Nếu Client phải tải toàn bộ thông tin này, máy sẽ đứng hình. Nếu Server phải kiểm tra vòng lặp cho tất cả chúng, CPU Server sẽ bốc cháy.

Làm thế nào để quản lý thế giới rộng lớn này? Học thuyết từ Minecraft chính là câu trả lời: **Chunking (Chia nhỏ bản đồ)**.

---

## 1. Chunk Là Gì?

Thay vì lưu bản đồ thành một mảng khổng lồ `Tile[10000][10000]`, ta cắt bản đồ ra thành nhiều mảnh hình vuông nhỏ, gọi là **Chunk**. 
Ví dụ: Mỗi Chunk có kích thước 16x16 ô (Tiles).

Mỗi Chunk sẽ là một Struct độc lập, chứa:
- Danh sách các luống đất trong 16x16 ô này.
- Danh sách các cây cối, hạt giống đang trồng.
- Danh sách các con vật (Gà, Bò) đang đi lại trong ranh giới của Chunk này.

---

## 2. Kỹ Thuật Load/Unload Chunk Khỏi RAM (Dành cho Server)

Ở Chương 11, chúng ta nói về việc dùng Timestamp để đếm giờ lớn cho cây mà không cần vòng lặp. Nhưng còn những thứ BẮT BUỘC phải dùng vòng lặp thì sao? (Ví dụ: Con gà đi loanh quanh tìm thức ăn, máy tưới nước tự động quay tròn).

**Cơ chế ngủ đông (Sleep/Unload):**
1. Khi có người chơi bước chân vào Chunk số 5. Server lập tức móc từ Database ra dữ liệu của Chunk số 5, nạp lên RAM. Con gà bắt đầu thức dậy và đi lại (Chạy Update loop).
2. Khi người chơi chạy đi xa khỏi Chunk số 5 quá 1 phút (và không còn ai khác ở đó).
3. Server "Đóng băng" toàn bộ Chunk số 5. Lưu vị trí con gà xuống Database, và gỡ Chunk 5 khỏi RAM (Unload).

Kỹ thuật này giúp một Server chỉ với vài GB RAM có thể mô phỏng một thế giới rộng lớn vô tận, vì nó **CHỈ CHẠY** những khu vực có người chơi đang đứng.

---

## 3. Area of Interest (AoI) Dựa Trên Chunk (Dành cho Client)

Thay vì gửi dữ liệu toàn bộ bản đồ cho Client, Server dùng các Chunk để giới hạn (Culling).

- Khung hình Camera của người chơi ở Client có thể nhìn bao quát khoảng 3x3 Chunk.
- Người chơi đang đứng ở Chunk trung tâm (Chunk số 5).
- Server chỉ gửi gói tin cập nhật trạng thái của những con gà, cái cây nằm ở Chunk 5 và 8 Chunk lân cận (Tổng 9 Chunk) cho Client.
- Khi người chơi chạy sang Chunk mới, Client sẽ gửi lệnh: `Xin cấp dữ liệu của Chunk mới này`. Server trả về Snapshot toàn bộ hạt giống, cây trồng của Chunk đó để Client vẽ lên màn hình.

---

## 4. Quản Lý Tilemap Nhiều Lớp (Multi-layer) Trong Mạng

Trong game nông trại, một ô đất (Tile) có thể có rất nhiều trạng thái chồng chéo lên nhau:
1. Đất thường.
2. Đã dùng cuốc xới lên.
3. Đã tưới nước (Màu sẫm hơn).
4. Có hạt giống (Trạng thái mầm non).
5. Có bón phân (Tăng tốc độ phát triển).

**Cách nén dữ liệu Tile khi gửi qua mạng (Bit-packing):**
Nếu mỗi thuộc tính trên bạn dùng 1 biến riêng, 1 ô đất sẽ tốn rất nhiều byte. Gửi 1 Chunk 16x16 (256 ô) sẽ làm nghẽn mạng.

Hãy dùng kỹ thuật **Bit-Flag** (Cờ nhị phân) nhét vào chung 1 biến số nguyên 16-bit (`u16`).
- Bit 0: Đã cuốc chưa? (1/0)
- Bit 1: Có tưới nước chưa? (1/0)
- Bit 2: Có phân bón không? (1/0)
- Bit 3-15: Chứa ID của Hạt giống (Lên tới hàng ngàn loại hạt giống).

Chỉ với `2 bytes`, bạn biểu diễn được TẤT CẢ trạng thái phức tạp nhất của một ô ruộng. Một Chunk 16x16 gửi về Client chỉ tốn vỏn vẹn **512 bytes**. Nhanh như chớp!
