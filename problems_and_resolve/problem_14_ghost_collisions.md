# Vấn Đề 14: Kẹt va chạm ở góc tường (Ghost Collisions)

**Vấn đề:**
Bản đồ được ráp từ hàng trăm viên gạch (Tile) hình vuông nằm sát nhau tạo thành mặt đất bằng phẳng. Nhân vật chạy trên mặt đất, đôi lúc tự nhiên bị "vấp" đứng khựng lại, dù không hề có chướng ngại vật nào!

**Nguyên nhân:**
Dù 2 viên gạch nằm sát khít nhau, do cách quét va chạm hình hộp AABB, ở một số vị trí thập phân nhạy cảm, cạnh bên của hộp va chạm nhân vật đâm nhẹ vào *cạnh bên* của viên gạch tiếp theo (Ghost vertex), sinh ra lực cản ngang làm nhân vật khựng lại.

**Giải pháp:**
1. **Dùng Capsule Collider (Hình con nhộng):** Thay vì dùng hộp chữ nhật có góc vuông sắc lẹm, đổi hộp va chạm của người chơi thành dạng bo tròn đáy (hoặc lục giác chém góc đáy). Khi quệt qua các kẽ hở của Tile, đáy tròn sẽ trượt mượt mà.
2. **Gộp Collider (Composite Collider):** Viết thuật toán gom các viên gạch sát nhau thành 1 khối AABB liền mạch duy nhất nằm ngang, xóa bỏ hoàn toàn kẽ hở bên trong lòng đất.
3. **Thêm hệ số khoan dung (Tolerance):** Bỏ qua va chạm ngang nếu điểm va chạm quá gần (ví dụ < 2 pixel) so với đáy chân nhân vật.
