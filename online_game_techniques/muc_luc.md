# Lộ Trình Kỹ Thuật Lập Trình Game Online (Từ Cơ Bản Đến Nâng Cao)

Để đi từ con số 0 đến khi có thể làm được một game online thời gian thực (Real-time Multiplayer) hoàn chỉnh với chất lượng thương mại, nội dung thường được chia thành **10 Chương** cốt lõi như sau:

## Phần 1: Nền Tảng Mạng (Network Fundamentals)
### Chương 1: Cơ Bản Về Mạng Cầu Nối (Networking Basics)
- Các khái niệm: IP, Port, LAN, WAN, NAT.
- So sánh giao thức TCP và UDP trong game.
- Khi nào dùng TCP (Game turn-based, chat, login) và khi nào dùng UDP (Game thời gian thực, FPS, MOBA).
- RUDP (Reliable UDP) là gì?

### Chương 2: Kiến Trúc Mạng Trong Game (Network Architectures)
- Mô hình Peer-to-Peer (P2P) Lockstep (Thường dùng cho game đối kháng, RTS cũ).
- Mô hình Client - Server.
- Khái niệm Authoritative Server (Máy chủ có toàn quyền quyết định) và Dumb Client (Client chỉ là màn hình hiển thị).

### Chương 3: Gói Tin & Truyền Tải Dữ Liệu (Serialization & Packets)
- Cách cấu trúc một gói tin (Packet Header, Payload).
- Tuần tự hóa dữ liệu (Serialization/Deserialization).
- So sánh Binary vs JSON (Tại sao game online lại dùng Binary).
- Endianness (Little Endian vs Big Endian).

## Phần 2: Xây Dựng Game Multiplayer Đơn Giản
### Chương 4: Lập Trình Socket Thực Hành
- Khởi tạo UDP Socket.
- Cơ chế Non-blocking Sockets và Polling.
- Gửi và nhận gói tin cơ bản giữa Server và Client.
- Quản lý danh sách kết nối (Connections / Sessions).

### Chương 5: Đồng Bộ Trạng Thái Đơn Giản (State Synchronization)
- Khái niệm Tickrate (Server Tick) và Framerate (Client Tick).
- Gửi toàn bộ trạng thái (Snapshots) từ Server về Client.
- Nội suy vị trí thực thể (Entity Interpolation) để hình ảnh nhân vật di chuyển mượt mà trên màn hình Client dù mạng giật.

## Phần 3: Kỹ Thuật Chuyên Sâu (Advanced Techniques)
Đây là phần quan trọng nhất tạo nên sự khác biệt giữa game online nghiệp dư và chuyên nghiệp.

### Chương 6: Dự Đoán Phía Client (Client-Side Prediction & Server Reconciliation)
- Vấn đề Input Lag (Cảm giác bấm nút nhưng nhân vật delay mới đi).
- Client-Side Prediction: Cho phép Client tự mô phỏng trước hành động ngay khi người chơi bấm nút.
- Server Reconciliation: Cách Client sửa sai (giật lùi lại) khi kết quả của Server trả về khác với dự đoán của Client.

### Chương 7: Bồi Thường Độ Trễ (Lag Compensation)
- Vấn đề: Bắn trúng trên màn hình Client nhưng Server lại bảo trượt (do độ trễ mạng).
- Kỹ thuật Hit Registration và Rollback trên Server.
- Server tua ngược thời gian để kiểm tra xem "tại thời điểm Client bấm bắn, kẻ địch có thực sự ở đó không".

### Chương 8: Kỹ Thuật Ngoại Suy (Extrapolation & Dead Reckoning)
- Khi gói tin bị rớt (Packet Loss), Client phải làm gì?
- Ngoại suy: Đoán trước hướng đi của kẻ địch dựa trên vận tốc hiện tại để tiếp tục vẽ nhân vật thay vì để nhân vật đứng im.

## Phần 4: Tối Ưu, Bảo Mật và Mở Rộng
### Chương 9: Tối Ưu Băng Thông Mạng (Bandwidth Optimization)
- Delta Compression (Chỉ gửi những gì thay đổi so với frame trước).
- Quantization (Làm tròn số thập phân để giảm dung lượng byte).
- Bit-packing (Nén nhiều cờ boolean hoặc số nhỏ vào cùng 1 byte).
- Interest Management (Area of Interest - AoI): Server chỉ gửi thông tin quái vật/người chơi nào nằm gần tầm nhìn của Client, bỏ qua những nơi quá xa.

### Chương 10: Bảo Mật Hệ Thống & Scale (Security & Scaling)
- Validate dữ liệu đầu vào để chống Hack Speed, Hack Map, Hack tọa độ.
- Mã hóa gói tin (Encryption) chống bắt gói.
- Khái niệm về Matchmaking, Lobby, Relay Server.
- Quản lý Dedicated Server trên hệ thống cloud.
