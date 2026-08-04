# Chương 5: Đồng Bộ Trạng Thái Đơn Giản (State Synchronization)

Giờ đây Server và Client đã có thể gửi/nhận byte cho nhau. Vấn đề tiếp theo: Làm sao để 2 máy tính cách nhau nửa vòng trái đất có thể hiển thị cùng một cảnh tượng mà không bị sai lệch?

Câu trả lời chính là: **Gửi Snapshots (Ảnh chụp trạng thái)**.

---

## 1. Tickrate (Server Tick) và Framerate (Client Tick)

Trong game online, thời gian của Client và Server trôi đi không giống nhau.

- **Framerate (FPS - Client):** Là tốc độ màn hình người chơi vẽ hình ảnh. Thường là 60 FPS, 144 FPS. Càng cao hình ảnh càng mượt.
- **Tickrate (Server Tick):** Là tốc độ Server mô phỏng thế giới và gửi gói tin về Client. Thường thì Server không có card màn hình (để vẽ hình) nên nó chỉ chạy mô phỏng vật lý ngầm. Tốc độ lý tưởng thường là 20 Tick/s, 30 Tick/s (Game FPS là 60 hoặc 128 Tick/s).

**Tại sao Server không chạy 144 Tick/s luôn cho mượt?**
Vì băng thông (Internet) không cho phép. Gửi 144 gói tin mỗi giây cho 100 người chơi sẽ làm sập mạng cục bộ hoặc tốn quá nhiều tiền thuê máy chủ. Hơn nữa, CPU Server sẽ không tính toán kịp nếu trong game có quá nhiều quái vật.

---

## 2. Cơ Chế Snapshot Gửi Đi

Với mô hình Authoritative Server, mỗi nhịp Tick (Ví dụ: 30 lần/giây), Server sẽ "chụp" lại toàn bộ thế giới (vị trí người chơi, máu quái vật) và đóng gói thành một gói tin siêu to gọi là **Snapshot**.

Quy trình diễn ra như sau:
1. `Client` liên tục ném các nút bấm (A, W, S, D, click chuột) lên Server.
2. `Server` hứng lấy các nút bấm đó, chạy vật lý để di chuyển các nhân vật trong bộ nhớ của nó.
3. Cứ mỗi 33 mili-giây (30 Tick/s), `Server` ném trả một bản **Snapshot** về `Client`. Bản snapshot này chứa:
   - Toạ độ chính xác của Client.
   - Toạ độ của tất cả kẻ địch xung quanh.
4. `Client` nhận được Snapshot, liền ép tọa độ nhân vật trên màn hình của mình khớp với lời Server phán.

---

## 3. Nội Suy Vị Trí (Entity Interpolation) - Phép Màu Hiển Thị

Nếu Server chỉ gửi dữ liệu 30 lần 1 giây (tức là 33ms mới có 1 cục dữ liệu), mà màn hình Client chạy 60 FPS (16ms phải vẽ 1 khung hình), thì sẽ có những khung hình Client KHÔNG nhận được dữ liệu gì mới.

**Nếu code ngây thơ:**
Khi có gói tin tới, bạn dịch chuyển ngay kẻ địch đến vị trí mới. Những lúc không có gói tin, kẻ địch đứng im.
-> Kết quả: Kẻ địch di chuyển bị **giật cục (stutter / teleport)** liên tục 30 lần/s, nhìn rất đau mắt.

**Giải pháp: Entity Interpolation (Nội suy thực thể)**
Thay vì dịch chuyển tức thời nhân vật, Client sẽ giữ lại **2 Snapshot gần nhất** trong bộ nhớ (Quá khứ 1 và Quá khứ 2).
Sau đó, Client sẽ lấy 2 điểm đó ra, và từ từ di chuyển nhân vật (nội suy) giữa 2 điểm đó.

> Kỹ thuật này đòi hỏi màn hình của Client phải **xem hình ảnh trễ đi một chút** (thường là trễ khoảng 1-2 Tick) so với thời gian thật của gói tin mới nhất. Điều này để đảm bảo Client luôn có 2 mốc thời gian để vẽ đường thẳng nối qua.

### Code mẫu Nội Suy (Odin + Raymath)

Mỗi nhân vật trên Client cần lưu lại `target_pos` (vị trí mới nhận từ gói tin mạng) và `current_pos` (vị trí đang vẽ trên màn hình).

```odin
import "core:math"
import rl "vendor:raylib"

// Bên trong Game Loop (60 FPS) của Client:
dt := rl.GetFrameTime()

// 1. Khi nhận gói tin mạng mới, cập nhật target
// packet := doc_tu_mang()
// enemy.target_pos = {packet.x, packet.y}

// 2. Thay vì gán thẳng, ta Nội Suy (Lerp) dần dần
smooth_speed: f32 = 10.0 // Tốc độ trượt theo (tuỳ chỉnh sao cho mượt)
enemy.current_pos = rl.Vector2Lerp(enemy.current_pos, enemy.target_pos, smooth_speed * dt)

// 3. Vẽ ra màn hình
rl.DrawCircleV(enemy.current_pos, 20.0, rl.RED)
```

Nhờ có `Lerp`, nhân vật kẻ địch sẽ trượt mượt mà trên màn hình người chơi ở tần số 144Hz, mặc cho dữ liệu mạng thực tế giật cục ở 30Hz!

---

## 4. Tóm Lược Vấn Đề Của Đồng Bộ Đơn Giản

Interpolation giải quyết rất tốt việc kẻ địch di chuyển mượt mà. **Tuy nhiên**, đối với nhân vật CỦA CHÍNH NGƯỜI CHƠI điều khiển, nó lại gây ra thảm họa:
Vì Client chờ Server gửi Snapshot về mới được phép vẽ mình di chuyển, người chơi sẽ cảm nhận độ trễ (Input Lag) đúng bằng độ trễ của mạng.
Bấm nút W -> Chờ 100ms -> Nhân vật mới nhấc chân đi.

Điều này là KHÔNG THỂ CHẤP NHẬN trong game hiện đại.
Để sửa lỗi này, lập trình viên đẻ ra một thuật toán cực kỳ hack não mang tên: **Client-side Prediction (Dự đoán phía Client)**, mà chúng ta sẽ tìm hiểu ở Phần 3!
