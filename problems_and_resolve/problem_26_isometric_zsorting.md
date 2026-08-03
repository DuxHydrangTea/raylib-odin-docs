# Vấn Đề 26: Lỗi che khuất đồ họa chéo (Z-Fighting in Isometric)

**Vấn đề:**
Trong các game góc nhìn chéo (Isometric / 2.5D) như Đế Chế, Diablo, Stardew Valley. Cây cối và công trình xếp chồng chéo lên nhau rất phức tạp. Thỉnh thoảng nhân vật đi ngang qua góc tường thì tay chân lại lòi ra ngoài đâm xuyên qua mái nhà.

**Nguyên nhân:**
Góc nhìn chéo sử dụng hệ tọa độ giả 3D trên mặt phẳng 2D (Tọa độ Descartes). Việc dùng Y-Sorting cơ bản (Vấn đề 1) đôi khi bị sai lệch do gốc tọa độ dưới chân nhân vật (Pivot) đặt chưa chuẩn, hoặc hình ảnh bị phình ra quá to che lấp các ô lân cận.

**Giải pháp:**
1. **Thiết lập Pivot thật khắt khe:** Tọa độ Y-Sort CẦN PHẢI luôn luôn nằm ở điểm chạm đất (Đáy của cái bóng). Không dùng tâm ảnh (Center).
2. **Thuật toán lưới Kim Cương (Diamond Grid):** Tách mặt đất ra riêng (luôn vẽ trước). Các vật thể nổi (Nhân vật, Tường, Cây) được tính toán tọa độ lưới (Grid X, Grid Y) để chuyển sang tọa độ màn hình (Screen X, Screen Y). Sắp xếp theo công thức `Grid X + Grid Y`.
3. **Cắt nhỏ vật thể (Asset Slicing):** Nếu một cái cây chiếm 4x4 ô lưới, đừng vẽ nó thành 1 cục bự. Hãy cắt nó ra làm 16 ô hình vuông nhỏ và vẽ theo thứ tự Y-Sort chung với nhân vật. Nhân vật sẽ lấp ló sau cành cây cực kỳ chuẩn xác.
