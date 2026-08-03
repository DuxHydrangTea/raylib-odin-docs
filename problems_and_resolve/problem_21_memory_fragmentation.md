# Vấn Đề 21: Phân mảnh bộ nhớ (Memory Fragmentation)

**Vấn đề:**
Game của bạn lúc mới mở chạy cực kỳ mượt. Nhưng sau khi cày 3-4 tiếng liên tục, tốc độ khung hình (FPS) bắt đầu tụt dần đều, và cuối cùng game crash mà không rõ nguyên nhân dù máy tính vẫn còn RAM.

**Nguyên nhân:**
Khi bạn cấp phát (Allocate) và giải phóng (Free) bộ nhớ liên tục cho quái vật, đạn, hạt... những khối RAM nhỏ lẻ bị xóa sẽ tạo ra các "lỗ hổng" rải rác khắp thanh RAM. Theo thời gian, thanh RAM trông như một miếng phô mai Thụy Sĩ. 
Khi bạn cần tạo một vật thể lớn (vd: Load map mới), hệ điều hành không tìm được một mảng RAM *liền mạch* đủ to, dẫn đến tốn rất nhiều CPU để phân trang, hoặc văng lỗi "Out of Memory" (OOM).

**Giải pháp:**
Giống như Vấn đề 11 (Object Pooling), nhưng quy mô lớn hơn: **Arena Allocator** (Bộ nhớ Vùng).
Thay vì mượn RAM lắt nhắt từng chút một, hãy xin thẳng một cục RAM 1GB ngay khi bật game. Tự quản lý việc chia nhỏ cục 1GB này cho các biến tạm thời. Khi kết thúc một vòng lặp, thay vì dọn dẹp từng biến, chỉ cần "Reset" con trỏ (Pointer) của 1GB đó về số 0. Tốc độ dọn dẹp là O(1) và không bao giờ bị phân mảnh.

```odin
// Xin hẳn 100MB RAM từ Hệ điều hành
arena: virtual.Arena
virtual.arena_init_growing(&arena)
context.allocator = virtual.arena_allocator(&arena)

// Tha hồ cấp phát thoải mái, RAM sẽ được lấy từ cục 100MB này một cách liền mạch!
```
