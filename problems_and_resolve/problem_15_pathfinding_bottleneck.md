# Vấn Đề 15: Tràn CPU vì Tìm đường (Pathfinding Bottleneck)

**Vấn đề:**
Thuật toán tìm đường A* (A-Star) hoạt động hoàn hảo khi có 10 con quái vật. Khi nâng lên 500 con quái vật truy đuổi người chơi, game sụp đổ hoàn toàn còn 5 FPS vì CPU phải tính đường cho cả 500 con cùng lúc.

**Nguyên nhân:**
A* là một thuật toán rất nặng về CPU (Duyệt mảng, kiểm tra H-cost, G-cost). Gọi nó 500 lần mỗi khung hình là điều không tưởng đối với bất kỳ máy tính nào.

**Giải pháp:**
1. **Chia lưới tính toán (Time Slicing):** Đừng bắt 500 con tìm đường mỗi frame. Chia đều ra: Frame 1 cho 10 con đầu tính, Frame 2 cho 10 con tiếp theo... Chúng không cần cập nhật đường đi liên tục, 1 giây cập nhật đích đến 2 lần là đủ mượt rồi.
2. **Flow Field Pathfinding (Vector Field):** Đây là kỹ thuật của game chiến thuật đám đông (RTS) như Starcraft. 
   - Thay vì từng con tự tìm đường, **Mặt đất sẽ nói cho quái biết phải đi đâu**. 
   - Vẽ một bảng ma trận (Vector Field) hướng tất cả mũi tên trên đường về phía người chơi. 500 con quái chỉ việc đọc mũi tên dưới chân mình và rẽ theo. CPU chỉ tốn tài nguyên cập nhật cái bảng ma trận đó 1 lần duy nhất!
