# Chương 18: Tối ưu hoá & Phân tích hiệu năng (Profiling)

"Code chạy được là tốt, nhưng code chạy 60FPS trên máy cùi bắp mới là Master."
Khi game của bạn bắt đầu phức tạp, việc sụt FPS là không thể tránh khỏi. Chương này cung cấp tư duy của một kỹ sư hệ thống.

---

## 1. Kẻ thù số 1: Memory Leak và Cấp phát động

Game chạy giật cục thường do Garbage Collector (Trình thu gom rác) hoặc hệ điều hành bị quá tải vì phải liên tục `malloc/free`.
* **Quy tắc:** Tuyệt đối không gọi lệnh `new`, `make`, `append` (tạo mảng động) ở bên trong Vòng lặp Game (Vùng Update và Draw).
* **Giải pháp:** Cấp phát mọi thứ ở màn hình Loading. Sử dụng **Object Pooling** (như hệ thống hạt ở Chương 13) hoặc **Arena Allocator** (Chương 10) để tái chế bộ nhớ.

## 2. Kẻ thù số 2: Lệnh Vẽ (Draw Calls) quá lớn

Mỗi khi bạn gọi `rl.DrawTexture()`, CPU phải ra lệnh cho GPU. Nếu bạn vẽ 10,000 viên gạch tilemap bằng 10,000 lệnh gọi, game sẽ lag nát bét.
* **Giải pháp:** Gộp lệnh vẽ (Batching). Thay vì vẽ rời rạc, hãy gộp toàn bộ bản đồ tĩnh thành 1 cái `RenderTexture` khổng lồ duy nhất (chỉ vẽ 1 lần lúc Load map). Trong Game Loop, bạn chỉ cần gọi ĐÚNG 1 lệnh `DrawTexture` để vẽ toàn bộ nền.

## 3. Profiling - Bắt bệnh bằng công cụ

Đừng dùng cảm giác để đoán xem hàm nào làm lag game. Hãy dùng dữ liệu.

Odin có tích hợp sẵn công cụ theo dõi thời gian chạy. Hoặc cao cấp hơn, bạn có thể tích hợp thư viện C như **Tracy Profiler**.

```odin
import "core:time"

// Cách đo tốc độ thủ công rẻ tiền nhất:
start_time := time.now()

// ... Gọi hàm tính toán AI siêu nặng ...
calculate_massive_ai_pathfinding()

duration := time.diff(start_time, time.now())
rl.TraceLog(.INFO, "Hàm AI mất %v để xử lý", duration)

// Nếu duration > 16.6ms, game của bạn CHẮC CHẮN bị rớt dưới 60 FPS.
```

## 4. Tối ưu Không gian và Cấu trúc dữ liệu

* Đừng dùng mảng 2 chiều khổng lồ nếu map phần lớn là trống rỗng. Hãy tìm hiểu **Spatial Hash Grid** hoặc **QuadTree**.
* Khi kiểm tra va chạm của 100 viên đạn với 100 quái vật, thay vì kiểm tra 10.000 lần (O(N^2)), QuadTree sẽ chia không gian thành các ô vuông. Đạn ở ô nào thì chỉ kiểm tra va chạm với quái vật ở chung ô đó (O(N log N)). Tốc độ tăng lên hàng chục lần!
