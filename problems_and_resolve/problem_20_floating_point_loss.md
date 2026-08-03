# Vấn Đề 20: Mất độ chính xác số thực (Floating Point Precision Loss)

**Vấn đề:**
Bản đồ game của bạn cực kỳ lớn (Minecraft 2D, No Man's Sky). Người chơi bay tàu vũ trụ ra xa điểm gốc (0, 0) khoảng 1.000.000 pixel. Bỗng nhiên, chuyển động của phi thuyền bắt đầu bị rung giật kinh khủng, va chạm văng xuyên tường, mọi công thức vật lý bị hỏng.

**Nguyên nhân:**
Biến `f32` (Số thực 32-bit float) chỉ có độ chính xác khoảng 7 chữ số. 
Ở tọa độ `X = 1,000,000`, nếu bạn cộng thêm `0.01` (vận tốc di chuyển nhỏ), biến `f32` sẽ làm tròn bỏ qua số `0.01` vì không đủ ô nhớ lưu phần thập phân! Nhân vật không nhích lên tí nào cho đến khi vận tốc tích lũy đủ lớn để làm tròn lên `1`, gây ra hiện tượng dịch chuyển giật cục từng mét một.

**Giải pháp (Floating Origin):**
Kỹ thuật "Gốc tọa độ trôi nổi". Không bao giờ cho phép tọa độ vượt quá vài vạn.
Khi người chơi đi cách xa điểm gốc quá `10,000` pixel:
1. Đặt lại tọa độ của người chơi về `0, 0`.
2. Dịch chuyển tọa độ của TẤT CẢ mọi thứ trên thế giới (quái vật, cục đá, hành tinh) trừ đi `10,000` pixel.
3. Từ góc nhìn của Camera, thế giới không hề xê dịch, nhưng trong RAM, các con số đã trở lại mức nhỏ và lấy lại độ chính xác thập phân!

*(Đây là bí mật đằng sau mọi tựa game thế giới mở vũ trụ không giới hạn).*
