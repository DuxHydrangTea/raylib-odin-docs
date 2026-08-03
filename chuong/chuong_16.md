# Chương 16: Trí tuệ nhân tạo (Game AI & Pathfinding)

Chào mừng bạn bước vào cảnh giới của các nhà phát triển game thương mại. Ở chương này, chúng ta sẽ thổi hồn vào kẻ địch, khiến chúng không chỉ biết "đi thẳng về phía người chơi" một cách ngốc nghếch nữa.

---

## 1. Thuật toán tìm đường (A* Pathfinding)

Giả sử người chơi đứng sau một bức tường, nếu quái vật chỉ di chuyển bằng cách lấy vector `player_pos - enemy_pos`, nó sẽ đâm đầu vào tường và đi dạo tại chỗ mãi mãi. Bạn cần thuật toán A* (A-Star).

Thuật toán A* sẽ quy đổi Tilemap (Chương 14) thành một bản đồ các điểm lưới (Grid). Nó sẽ dò tìm đường đi ngắn nhất từ ô hiện tại của quái vật đến ô của người chơi, né tránh các ô Tường.

*(Ghi chú: Việc tự viết A* khá phức tạp, thông thường chúng ta sẽ duyệt một danh sách các "Nút" mở và đóng, so sánh chi phí `G` (đường đã đi) và `H` (khoảng cách ước tính tới đích)).*

Kết quả của A* trả về là một mảng tọa độ (Danh sách các điểm cần đi tới - Waypoints). Quái vật chỉ việc đi đến điểm đầu tiên trong mảng, khi đến nơi thì xóa điểm đó đi và đi tới điểm tiếp theo.

## 2. Máy Trạng Thái Cấp Cao (FSM cho AI)

Mỗi quái vật nên có một biến trạng thái `AIState`. Cấu trúc này giúp quái vật hành động có mục đích.

```odin
AIState :: enum {
    IDLE,      // Đứng im thở
    PATROL,    // Đi tuần tra quanh 1 khu vực
    CHASE,     // Phát hiện người chơi -> Rượt đuổi (Dùng A*)
    ATTACK,    // Đủ gần -> Tấn công
    FLEE,      // Sắp chết -> Bỏ chạy
}
```

Trong vòng lặp cập nhật của quái vật, bạn chia logic theo trạng thái:

```odin
switch enemy.state {
    case .PATROL:
        // Đi lại giữa điểm A và B
        // Nếu rl.Vector2Distance(enemy, player) < 200 { enemy.state = .CHASE }
        
    case .CHASE:
        // Tính A* tìm đường tới player
        // Nếu máu < 10% { enemy.state = .FLEE }
        // Nếu khoảng cách < 20 { enemy.state = .ATTACK }
        
    case .ATTACK:
        // Đứng lại, play animation chém
        // Tính sát thương
}
```

## 3. Cây hành vi (Behavior Trees)

Khi AI của bạn trở nên quá phức tạp (Ví dụ: Một NPC vừa biết nấu ăn, vừa biết nói chuyện, vừa biết nhặt vũ khí đánh giặc), FSM sẽ trở thành một mớ bòng bong. Lúc này, người ta dùng **Behavior Tree**. 

Behavior Tree phân cấp các quyết định từ trên xuống dưới giống như rễ cây:
- Nút Gốc: Kẻ địch có thấy người chơi không? 
  - Nếu CÓ -> Người chơi có cầm súng không?
    - Nếu CÓ -> Bỏ chạy núp vào tường.
    - Nếu KHÔNG -> Lao vào cắn.
  - Nếu KHÔNG -> Đang đói không?
    - Nếu CÓ -> Đi tìm thức ăn.
    - Nếu KHÔNG -> Đi ngủ.

Behavior Tree tách biệt các điều kiện (Conditions) và hành động (Actions), giúp bạn dễ dàng lắp ghép và tạo ra một AI thông minh như con người.
