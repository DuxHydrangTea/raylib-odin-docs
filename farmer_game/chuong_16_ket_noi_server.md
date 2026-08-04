# Chương 16: Kết Nối Server Và Lưu Trữ Database

Để đưa một Game Nông Trại từ Offline (tự kỷ một mình) lên tầm cao MMO (Avatar 2D), chúng ta cần tách đôi dự án: Một cục code chạy phía Client (Đồ họa Raylib), và một cục code chạy phía Server (Xử lý Data thầm lặng không có đồ họa).

## 1. Khai Báo Gói Tin Cơ Bản

Để giao tiếp giữa Client và Server, ta định nghĩa gói tin (Packet) cấu trúc đơn giản. Tránh gửi chuỗi Text (JSON) gây chậm. Chúng ta dùng Binary (như trong phần kỹ thuật Game Online).

```odin
// shared/network_packets.odin
package shared

PacketType :: enum u8 {
    LOGIN = 1,
    MOVE = 2,
    INTERACT_PLOT = 3,   // Cuốc đất, Gieo hạt
    MAP_SNAPSHOT = 4,    // Server gửi cả cái bản đồ về
}

PacketHeader :: struct {
    type: PacketType,
    client_id: u32,
    timestamp: f64,
}

InteractPlotPacket :: struct {
    header: PacketHeader,
    grid_x: u16,
    grid_y: u16,
    tool_id: u16,  // ID của Hạt giống hoặc công cụ đang xài
}
```

## 2. Authoritative Server (Server Quyền Lực Tuyệt Đối)

Khi Client bấm phím cuốc đất, Client tuyệt đối KHÔNG ĐƯỢC tự đổi trạng thái ô đất thành `.PLOWED`.

**Quy trình chuẩn:**
1. **Client:** Gửi `InteractPlotPacket` qua UDP/TCP (TCP an toàn hơn cho game nông trại, tránh mất gói tin).
2. **Server:** Nhận gói tin. Kiểm tra `client_id` có đang đứng gần `grid_x, y` không? Có đang cầm cái Cuốc không? Ô đất đó có trống không?
3. **Server:** Thấy mọi thứ hợp lệ. Server tự đổi trạng thái đất của nó thành `PLOWED`. 
4. **Server:** Gửi một gói tin Broadcast (Phát sóng) cho TOÀN BỘ người chơi đang có mặt trong bản đồ đó: "Ô x, y vừa thành đất đã cuốc".
5. **Client:** Nhận gói phản hồi, lúc này mới hiện hình ảnh đất đã cuốc và phát âm thanh "Xoạch".

## 3. Ánh Xạ Bản Đồ Nông Trại (Instanced Rooms)

Trong Avatar, có một cái "Thị Trấn" (Town) nơi 50 người chạy lăng xăng chung. Nhưng khi bạn đi qua "Cổng Nông Trại", bạn bị tống vào cái nông trại của riêng bạn (Room cá nhân).

Server phải phân bổ hàng chục ngàn "Room" này trên RAM sao cho tối ưu:

```odin
// server/farm_manager.odin

Room :: struct {
    owner_id: u32,
    farm_map: ^GameMap,  // Tham chiếu tới Tilemap (Giống Chương 3)
    players_inside: [dynamic]u32, // Chứa cả chủ nhà và bạn bè sang trộm
}

active_rooms: map[u32]Room // Key là owner_id
```

Khi Player `123` kết nối vào Game:
1. Server check xem `active_rooms[123]` có trên RAM chưa.
2. Chưa có thì truy vấn (Query) PostgreSQL Database: `SELECT map_data FROM farms WHERE owner_id = 123`.
3. Giải nén chuỗi bit-packing `map_data` nạp lên bộ nhớ `active_rooms`.
4. Khi Player này Offline và phòng không còn ai, Server gom 100 luống đất thành mảng nhị phân và `UPDATE sql` cất trở lại vào ổ cứng, giải phóng RAM.

## 4. Xử Lý Khác Biệt Giờ Giấc (Delta Time)

Như đã đề cập ở Kỹ thuật MMO Farm, Server lưu Timestamp trồng cây. Nhưng khi Player bật game lên, Server tải dữ liệu từ DB, nó lấy Timestamp hiện tại trừ đi Timestamp gieo hạt. Kết quả là Cây mọc tức thời lên giai đoạn chín ngay khi Player vừa bước chân vào Room! 

Toàn bộ Vòng đời ô đất (Chương 5, 6, 7) được BÊ NGUYÊN XI từ Client sang nằm ở máy chủ Server. Client Raylib giờ đây chỉ còn là một chiếc "Tivi" nhận lệnh vẽ từ Server phát xuống. Mọi logic giả mạo (Cheat/Hack tốc độ mọc cây, hack xu) của Client đều vô dụng!
