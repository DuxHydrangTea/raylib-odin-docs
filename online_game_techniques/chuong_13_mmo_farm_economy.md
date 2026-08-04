# Chương 13: Kinh Tế, Giao Dịch & Chống Dupe Item

Kẻ thù lớn nhất của một game bắn súng là Hacker Aimbot (tự nhắm đầu). Nhưng kẻ thù phá hủy một game MMO Nông trại chính là **Dupe Item (Hack nhân bản vật phẩm)**.
Chỉ cần 1 người chơi phát hiện ra lỗi nhân bản Vàng hoặc Đá quý, hệ thống kinh tế của toàn bộ Game sẽ sụp đổ hoàn toàn trong vòng 24 giờ.

---

## 1. Vấn Đề Lỗi Đồng Thời (Race Condition)

Hãy xem xét kịch bản sau: 
Có 1 Quả Táo quý hiếm rớt trên đất. Hai người chơi A và B đứng cạnh nhau và cùng bấm nút "Nhặt".
Gói tin của A và B bay tới Server **cùng một mili-giây**.

Nếu Server code ẩu, logic sẽ chạy như sau:
- Xử lý gói của A: Thấy Quả Táo trên đất -> Chuyển Quả Táo vào túi A.
- Cùng lúc đó, Xử lý gói của B: Thấy Quả Táo CŨNG CÒN TRÊN ĐẤT (Vì lệnh xoá trái táo của A chưa kịp lưu xong) -> Chuyển 1 Quả Táo nữa vào túi B.

**Boom!** 1 Quả Táo biến thành 2 Quả Táo. 
Trò này áp dụng tương tự khi hai người cùng lấy đồ từ Rương Bang Hội, hoặc rút tiền từ ngân hàng.

---

## 2. Giải Pháp: Mutex Lock và Transaction

Để chống lại Race Condition, mọi thao tác đụng chạm tới số lượng vật phẩm hoặc tiền bạc bắt buộc phải được "Khoá" (Lock) hoặc xử lý theo hàng đợi tuần tự.

### Cơ chế Lock rương hòm
Khi một người (A) mở Rương chứa đồ chung. Server lập tức set cờ `is_locked = true` cho cái rương đó.
Nếu người B bấm mở Rương, Server sẽ đá B ra và hiện thông báo: *"Rương đang được sử dụng bởi người khác!"*. 
Chỉ khi A đóng Rương, `is_locked = false`, B mới được quyền thao tác. (Đây là cách các game MMO cũ làm, hơi bất tiện nhưng an toàn tuyệt đối).

### Khóa mức cơ sở dữ liệu (Database Transaction)
Khi cấn trừ tiền tài khoản, đừng bao giờ đọc tiền ra biến số, cộng trừ rồi mới lưu vào. Hacker có thể gửi 10 lệnh mua hàng cùng lúc để khai thác khoảng hở lúc tính toán.

**Sử dụng Transaction của SQL:**
```sql
UPDATE players SET gold = gold - 500 WHERE id = 'PlayerA' AND gold >= 500;
```
Bằng cách đẩy trách nhiệm kiểm tra `gold >= 500` xuống tầng Database (nơi đã có sẵn hàng rào bảo vệ Race Condition độc quyền), dù có 1000 lệnh đến cùng lúc, Database cũng sẽ tự động xử lý từng dòng một và trừ đúng số tiền, hoặc báo Lỗi nếu tiền không đủ.

---

## 3. Inventory System (Túi đồ Authoritative)

Ở Client, Túi đồ của bạn có vẻ như là những biểu tượng vuông vuông, kéo thả mượt mà, đổi vị trí ô số 1 sang ô số 2.
NHƯNG ở Server, Túi đồ là một sinh vật hoàn toàn khác:

- Khi bạn kéo thanh kiếm từ ô số 1 sang ô số 2 trên màn hình Client, Client KHÔNG ĐƯỢC tự ý hoán đổi. 
- Client gửi gói tin: `Lệnh SWAP(ô_1, ô_2)`.
- Server nhận lệnh, kiểm tra xem ô số 1 có tồn tại thanh kiếm không, ô số 2 có trống không (hoặc có hợp lệ để đổi không). 
- Server đổi mảng dữ liệu trong RAM của nó, rồi mới gửi xác nhận `OK` về cho Client.
- Client lúc này mới chính thức hoán đổi hình ảnh 2 vật phẩm trên màn hình.

**Cách chống lag trải nghiệm:**
Để tránh việc người chơi kéo thả đồ bị "cứng đơ" chờ Server phản hồi. Client thường dùng mẹo "Giao diện ảo". Khi người chơi kéo thả, vật phẩm lập tức nhảy sang ô mới tạo cảm giác rất sướng tay. Nhưng đó chỉ là hình ảnh. Vài chục mili-giây sau Server báo "Không hợp lệ", vật phẩm tự động búng ngược về chỗ cũ. (Người chơi sẽ nghĩ do Lag mạng chứ không phải do lỗi game).

---

## 4. Tóm Kết: Kinh Nghiệm Xương Máu

Làm game MMO Nông Trại hay kinh tế, hãy tuân thủ nguyên tắc:
1. **Server là kẻ nắm Database.** Không một logic thay đổi Item nào được phép chạy độc lập ở Client.
2. **Giao dịch (Trade) phải dùng Two-Phase Commit.** Người A khóa đồ, người B khóa đồ. Hai bên cùng bấm "Xác nhận". Lúc này Server mới thực hiện phép hoán đổi 1 chạm (Atomic) ở database.
3. Luôn lưu Log (Lịch sử) của mọi giao dịch giá trị lớn. Khi phát hiện Item bị Dupe (có 2 ID vật phẩm sinh ra trùng nhau), Admin chỉ việc tra Log và khoá tài khoản Hacker dễ dàng.

> [!TIP]
> Các quy tắc này trông có vẻ khô khan, nhưng nó bảo vệ công sức hàng ngàn giờ chơi của Game thủ. Một game nông trại có kinh tế vững vàng sẽ tồn tại mãi mãi!
