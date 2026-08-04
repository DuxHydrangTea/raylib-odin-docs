# Chương 11: Kiến Trúc Server & Quản Lý Thời Gian Thực (Farm MMO)

Làm game MMO Nông Trại khác hoàn toàn với game Bắn súng. Trong CS:GO, một trận đấu kéo dài 30 phút rồi Server tự hủy. Nhưng trong game Nông Trại, thế giới (World) tồn tại **vĩnh viễn**. 

Vấn đề hóc búa nhất là: Làm sao một luống cải bắp vẫn đếm thời gian và lớn lên ngay cả khi Server bị tắt bảo trì hoặc không có ai trong phòng?

---

## 1. Vòng lặp Game (Game Loop) vs Cronjob

### Cách làm sai (Cách của người mới):
Bạn dùng một vòng lặp `while` chạy liên tục trên Server. Cứ mỗi khung hình (frame), bạn lặp qua 10,000 cái cây, trừ đi `delta_time`, nếu `time_left <= 0` thì chuyển cây sang trạng thái "Thu hoạch".
- **Hậu quả:** CPU Server sẽ chạy 100% chỉ để đếm ngược thời gian cho những cái cây không ai thèm ngó tới. Và khi Server bảo trì tắt đi bật lại, toàn bộ quá trình đếm ngược bị reset hoặc dừng lại.

### Cách làm đúng (Tick tĩnh / Timestamp):
Không bao giờ dùng vòng lặp thời gian thực để đếm giờ lớn lên của cây!
Mỗi khi người chơi gieo một hạt giống, bạn chỉ lưu 2 thông tin vào Database:
- `plant_id = 1` (Bắp cải)
- `planted_at = 1690000000` (Unix Timestamp - số giây tính từ năm 1970).

Cây bắp cải cần 4 tiếng (14,400 giây) để lớn. Suy ra thời điểm thu hoạch là:
`harvest_at = planted_at + 14400`

Mọi thứ đứng im, không có vòng lặp nào chạy cả. 

Khi một người chơi đi ngang qua luống đất đó, Server mới nhìn vào đồng hồ hiện tại (`current_time = 1690005000`). Server làm một phép trừ đơn giản: 
- `current_time > harvest_at`? -> Gửi về cho Client hình ảnh cây **Đã chín**.
- Nếu chưa tới giờ? -> Tính phần trăm `(current_time - planted_at) / 14400` -> Gửi về cho Client hình ảnh **Cây đang nhú mầm**.

Bằng cách này, dù Server có tắt nguồn 2 ngày, khi mở lên lại, cây vẫn sẽ lớn lên bình thường dựa trên đối chiếu Timestamp!

---

## 2. Lưu Trữ Thế Giới: File Save vs Database

Khi bạn chơi Stardew Valley một mình, nông trại được lưu ra file `.json` hoặc `.xml`. 
Nhưng nếu 1,000 người cùng cày ruộng một lúc, bạn không thể mở file `.json` ra ghi liên tục hàng ngàn lần một giây được. Ổ cứng sẽ cháy hoặc file sẽ bị lỗi (Corruption).

**Giải pháp: Sử dụng Hệ Quản Trị Cơ Sở Dữ Liệu (Database).**

- **Redis (In-memory DB):** Dùng để chứa những thứ cần đọc/ghi với tốc độ sấm sét (như tọa độ người chơi đang chạy nhảy). Dữ liệu này nếu mất cũng không sao.
- **PostgreSQL / MySQL:** Dùng để lưu trữ những thứ tuyệt đối không được mất: Tiền, Cấp độ, Vị trí rương hòm, Vị trí các luống đất.

**Kỹ thuật lưu gián đoạn (Lazy Save / Dirty Flag):**
Khi người chơi đào một mảnh đất. Đừng gõ lệnh `UPDATE sql` vào Database ngay lập tức.
1. Server sửa mảnh đất đó trên RAM.
2. Đánh dấu mảng đất đó là `is_dirty = true` (Đã bị thay đổi).
3. Khoảng 5 phút một lần, Server sẽ quét qua toàn bộ bản đồ, gôm tất cả những mảng đất có cờ `is_dirty` thành một câu lệnh SQL duy nhất và lưu thẳng vào Database (Bulk Update).
4. Việc này giảm tải số lượng câu lệnh SQL từ 10,000 lần/giây xuống còn 1 lần/5 phút!

---

## 3. Kiến Trúc "Room" Ảo Cho Nông Trại
Một bản đồ nông trại lớn không thể là 1 mảnh đất duy nhất cho tất cả 10,000 người vào trồng (Sẽ bị giẫm đạp và phá hoại). 

Thường các game thiết kế thành **Instanced Farming (Nông trại cá nhân/Bang hội)**:
- Lõi trò chơi (Thị trấn, Cửa hàng) là một Server chung.
- Mỗi khi người chơi đi vào cửa Nông Trại của mình, Server sẽ sinh ra một "Phòng" (Room) logic chỉ dành riêng cho người chơi đó và bạn bè được mời.
- Dữ liệu Nông trại được kéo từ Database lên RAM khi chủ nhân online, và đẩy lại xuống Database khi chủ nhân offline để giải phóng RAM cho Server.
