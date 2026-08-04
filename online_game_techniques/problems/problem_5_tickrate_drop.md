# Vấn Đề 5: Server Tickrate Drop (Server Quá Tải)

## 1. Biểu hiện của Lỗi
Game của bạn chạy cực kì mượt khi chỉ có 10 người trong phòng. 
Nhưng khi 100 người chơi cùng tụ tập lại một nơi để đánh Boss, toàn bộ Server bắt đầu chạy như Slow-motion (chuyển động chậm). Tốc độ di chuyển của mọi người chậm lại, quái vật khựng liên tục, Ping nhảy lên hàng ngàn.

## 2. Nguyên nhân
Đây không phải là lỗi rớt mạng, mà là lỗi **Cạn kiệt CPU Server (CPU Bottleneck)**.
Server của bạn được thiết lập chạy ở `Tickrate = 30` (Tức là phải hoàn thành mọi tính toán trong vòng 33 mili-giây).
Nhưng khi 100 người đánh nhau, vòng lặp Server của bạn phải thực hiện:
- Kiểm tra va chạm (Collision) cho 10,000 viên đạn với 100 người.
- Cập nhật Pathfinding (tìm đường) cho 500 con quái vật.
- Tuần tự hoá 1000 gói tin gửi qua mạng.

Tất cả đống việc này tốn tới 100 mili-giây mới làm xong. Kết quả: Vòng lặp bị kéo dài ra, Tickrate rớt từ 30 xuống còn 10. Mọi thứ trên Server bị chậm lại gấp 3 lần.

## 3. Cách khắc phục chi tiết

Đây là bài toán khó nhất của việc Tối ưu hóa (Optimization) Server.

### Tối ưu 1: Spatial Partitioning (Chia lưới không gian)
Tuyệt đối không dùng vòng lặp `O(N^2)` để kiểm tra va chạm (Lấy từng viên đạn check với toàn bộ người chơi).
- Hãy chia bản đồ thành các ô Grid.
- Một viên đạn nằm ở Ô số 1, thì chỉ cần check va chạm với những người chơi đang đứng ở Ô số 1 và các ô liền kề. Giảm lượng phép tính từ 1,000,000 xuống còn 1,000! (Sử dụng QuadTree hoặc Grid).

### Tối ưu 2: Tách biệt Vòng lặp Mạng và Vòng lặp Logic
Người mới thường viết code Mạng và Logic chung 1 vòng `while`.
```odin
for {
   doc_du_lieu_mang() // Tốn 10ms
   cap_nhat_vat_ly()  // Tốn 50ms
   gui_du_lieu_mang() // Tốn 10ms
}
```
Hãy dùng **Đa luồng (Multithreading)**.
- Thread 1 (Network Thread): Chỉ lo việc đọc và nhận gói tin vào hàng đợi (Queue), không làm gì khác.
- Thread 2 (Logic Thread): Rút gói tin từ hàng đợi ra xử lý vật lý.
- Điều này đảm bảo Socket không bị quá tải bộ đệm (Buffer overflow) khi vật lý tính toán chậm.

### Tối ưu 3: Tắt tính toán cho những khu vực chết
Những con quái vật ở quá xa không ai nhìn thấy, hãy đưa chúng vào trạng thái Ngủ (Sleep). Không chạy AI, không chạy vật lý cho đến khi có người chơi bước lại gần. (Kỹ thuật Chunking).
