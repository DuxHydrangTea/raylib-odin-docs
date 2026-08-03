# Vấn Đề 28: Dư thừa kiểm tra Va chạm (Broadphase Missing)

**Vấn đề:**
Bản đồ có 10,000 cái cây ngẫu nhiên và 10 con quái vật. FPS của game sụt giảm mạnh mỗi khi quái vật di chuyển.

**Nguyên nhân:**
Vì không muốn quái đâm vào cây, bạn tạo vòng lặp cho mỗi con quái kiểm tra va chạm với TẤT CẢ 10,000 cái cây. 
10 quái x 10,000 cây = 100,000 phép tính `CheckCollision` mỗi giây. Thực tế 9,990 cái cây nằm xa lơ xa lắc ngoài rìa bản đồ, không có khả năng va chạm.

**Giải pháp (Phân chia Không gian - Spatial Partitioning / Broadphase):**
Chia toàn bộ bản đồ ra thành các ô vuông lớn (Ví dụ lưới 500x500 pixel).
Mỗi cái cây được ghi danh vào 1 ô vuông.
Khi quái vật di chuyển, nó tính toán xem nó đang đứng ở ô vuông nào. Nó CHỈ cần kiểm tra va chạm với các cái cây nằm trong CÙNG ô vuông đó (hoặc 8 ô lân cận).

Số lượng phép tính giảm từ 100,000 xuống còn... 10 phép tính!

*(Ngoài Lưới không gian (Grid), bạn có thể dùng cấu trúc cây QuadTree để tối ưu sâu hơn).*
