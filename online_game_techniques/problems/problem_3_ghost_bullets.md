# Vấn Đề 3: Ghost Bullets (Đạn ảo / Bắn không mất máu)

## 1. Biểu hiện của Lỗi
Đây là ác mộng lớn nhất của các nhà làm game FPS (Đặc biệt là CS:GO hoặc PUBG ngày xưa).
- Bạn áp sát kẻ địch, bắn trúng hồng tâm rõ ràng.
- Màn hình của bạn hiện tia máu tóe ra từ đầu kẻ địch. Cửa sổ chat thông báo "Bạn đã bắn!".
- Nhưng kẻ địch không chết và quay lại bắn chết bạn. Bạn chết với bảng thống kê: "Sát thương gây ra: 0". Đạn của bạn trở thành Đạn ma (Ghost Bullets).

## 2. Nguyên nhân

Có hai lý do chính tạo ra hiện tượng đạn ma:

1. **Hiệu ứng tia máu là Fake (Ảo tưởng):** Để game mượt, Client tự vẽ tia đạn và hiệu ứng máu ngay lập tức khi bạn bấm chuột (Dự đoán phía Client). Nhưng sau đó Server phán quyết là bạn bắn hụt (Do Server không có Lag Compensation đủ tốt).
2. **Bạn đã chết trước khi viên đạn tới nơi:**
   - Bạn và Kẻ địch bắn nhau CÙNG 1 MILI-GIÂY.
   - Nhưng Ping của kẻ địch là `10ms`, còn Ping của bạn là `100ms`.
   - Gói tin "Kẻ địch bắn trúng bạn" bay tới Server trước. Server phán quyết bạn đã chết lúc `T = 50`.
   - Lúc `T = 100`, gói tin "Bạn bắn trúng kẻ địch" mới bay tới Server. Server check thấy bạn đã chết từ 50 mili-giây trước, nên Server HỦY BỎ hoàn toàn viên đạn của bạn!

## 3. Cách khắc phục chi tiết

### Giải pháp 1: Không bao giờ vẽ máu từ Client
Hiệu ứng tia lửa ở nòng súng thì có thể vẽ ngay (để có cảm giác bắn). Nhưng **Hiệu ứng máu văng ra** TUYỆT ĐỐI chỉ được vẽ khi có gói tin xác nhận "TRÚNG" từ Server gửi về.
- Sẽ có độ trễ nhỏ giữa lúc bóp cò và lúc thấy máu (bằng ping của người chơi), nhưng người chơi thà thấy máu trễ một chút, còn hơn là thấy máu mà địch không chết!

### Giải pháp 2: Hoàn thiện Lag Compensation (Chương 7)
Hãy đảm bảo Server của bạn có khả năng tua ngược thời gian (Rollback) một cách chính xác dựa trên Hitbox chứ không phải dựa trên tọa độ bao bọc (Bounding Box) đơn giản.
- Luôn lưu lại Animation State và góc xoay của từng khúc xương (Bone) của kẻ địch vào History Buffer trên Server.

### Giải pháp 3: Chấp nhận Cùng Chết (Trade-kill)
Một số game hiện đại không Hủy bỏ viên đạn của kẻ Ping cao. Nếu 2 người bắn nhau và gói tin tới sau, Server vẫn áp dụng sát thương và cho cả 2 cùng lăn ra chết. Cách này mang lại cảm giác công bằng hơn, dù không thực tế ngoài đời thực.
