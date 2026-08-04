# Vấn Đề 2: Rubber-banding (Hiệu ứng Dây thun / Giật lùi)

## 1. Biểu hiện của Lỗi
Bạn điều khiển nhân vật chạy tới trước được 5 bước, đột nhiên "Khựng" một cái, nhân vật bị búng ngược trở lại vị trí cũ cách đó 3 bước. Cứ đi vài bước lại bị giật lùi, cảm giác cực kì khó chịu.

## 2. Nguyên nhân
Rubber-banding là hệ quả trực tiếp của việc **Client-side Prediction** cãi lộn với **Server Reconciliation** (Xem lại Chương 6).

Trình tự xảy ra:
1. Client dự đoán: "Mình chạy tới X=10". (Trên màn hình bạn đang ở X=10).
2. Tuy nhiên, mạng của bạn đột nhiên bị lag (Packet Loss), lệnh "Chạy" không bao giờ tới được Server.
3. Server không nhận được lệnh, nó đinh ninh bạn vẫn đang đứng im ở X=5.
4. Server gửi gói tin đồng bộ về Client: "Vị trí của mày là X=5".
5. Client nhận được, nhận ra mình đang bị sai trái so với Server, lập tức **Kéo (Snap)** nhân vật từ 10 lùi về lại 5. Sự kiện này tạo ra lực búng như dây thun.

## 3. Cách khắc phục chi tiết

### Tối ưu 1: Nới lỏng Dung sai (Tolerance) của Server
Server không nên quá "Máy móc". Khi Client và Server lệch nhau 1-2 pixel, đừng bắt Client lùi lại.
- Chỉ khi nào Client cách xa Server quá một ngưỡng (Ví dụ: `Tolerance = 50 units`), Server mới ra lệnh ép giật lùi.

### Tối ưu 2: Nội suy kéo lùi (Smooth Rewind)
Khi Client bị Server ép lùi về, **ĐỪNG** thay đổi tọa độ `X` ngay lập tức (Snap).
Hãy thiết lập một quỹ đạo nội suy (Lerp) kéo nhân vật trượt nhanh về vị trí cũ trong khoảng 0.1 giây. Mắt người chơi sẽ nghĩ đó là một hiệu ứng lướt lùi hoặc do địa hình trơn, chứ không phải do game bị lag.

### Tối ưu 3: Gửi lại phím (Input Redundancy)
Vì mạng Internet hay rớt gói (Packet Loss). Thay vì mỗi gói tin Client chỉ chứa nút bấm của khung hình hiện tại (Khung 100), hãy đóng gói **3 khung hình gần nhất** vào cùng một gói UDP.
- Gói tin gửi đi: `[Khung 98, Khung 99, Khung 100]`.
- Nếu gói 98 bị rớt dọc đường, lúc Server nhận được gói 100, Server vẫn có đủ dữ liệu phím bấm của cả 98 và 99 để chạy bù vào! Cách này triệt tiêu hoàn toàn Rubber-banding do Packet Loss.
