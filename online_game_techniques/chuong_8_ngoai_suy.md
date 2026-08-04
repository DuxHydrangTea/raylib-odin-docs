# Chương 8: Kỹ Thuật Ngoại Suy (Extrapolation & Dead Reckoning)

Ở Chương 5 chúng ta đã học Nội Suy (Interpolation) - nối 2 điểm quá khứ lại với nhau để nhân vật di chuyển mượt mà. 

Tuy nhiên, Internet luôn tiềm ẩn những cơn giật lag (Lag Spike) và Rớt gói tin (Packet Loss). Nếu Server đột nhiên ngừng gửi dữ liệu trong 1 giây, điều gì sẽ xảy ra với Interpolation?

---

## 1. Giới Hạn Của Interpolation

Interpolation chỉ hoạt động được khi bạn **CÓ TỪ 2 ĐIỂM TRỞ LÊN**.
Nếu bạn đang trượt nhân vật từ điểm A đến điểm B, và khi tới B bạn vẫn chưa nhận được gói tin nào chứa tọa độ C từ Server, nhân vật sẽ:
1. Đứng khựng lại hoàn toàn.
2. Vài trăm mili-giây sau mạng có lại, gói tin tới, nhân vật Dịch Chuyển Tức Thời (Teleport) lên thẳng điểm C.

Điều này làm game bị "Giật hình" (Rubber-banding) cực kì đau mắt.

---

## 2. Kỹ Thuật Ngoại Suy (Extrapolation)

Ngoại suy (Extrapolation) là hành động: "Vì tao không biết tương lai mày đi đâu, nên tao sẽ lấy vận tốc hiện tại của mày để **Đoán** tiếp con đường mày sẽ đi".

### Cơ chế hoạt động:
Khi Client hết dữ liệu để Nội suy (đã trượt tới điểm cuối cùng nhận được), Client chuyển sang chế độ Ngoại Suy.
1. Client đọc gói tin cuối cùng của kẻ địch.
2. Gói tin này ngoài Tọa Độ, thường gửi kèm cả **Vận Tốc (Velocity/Direction)**.
3. Client tự động tiếp tục đẩy kẻ địch di chuyển thẳng theo hướng Vận Tốc đó trên màn hình (Sử dụng code `Pos += Velocity * dt`).
4. Kết quả: Mặc dù rớt mạng, kẻ địch vẫn tiếp tục chạy mượt mà theo quán tính!

---

## 3. Dead Reckoning - Ngoại Suy Siêu Cấp

Dead Reckoning (Dự đoán đường băng) là một kỹ thuật Ngoại suy chuyên sâu hơn, được dùng rất nhiều trong các game có quỹ đạo vật lý rõ ràng (Đua xe, Lái máy bay, Phi thuyền).

Trong các game này, di chuyển không chỉ là đi thẳng, mà có ma sát, gia tốc, trọng lực, góc lái vô lăng.

### Cách Dead Reckoning tiết kiệm băng thông:
Trong game đua xe, thay vì Server phải gửi tọa độ xe 60 lần/giây, Server chỉ gửi:
- Tọa độ hiện tại: `X = 0, Y = 0`.
- Vận tốc: `100 km/h`.
- Trọng trường / Gia tốc: `a = 5`.
- Độ bẻ lái: `Xoay phải 15 độ`.

Và Server... nín im không gửi gì nữa trong suốt nửa giây.
Ở phía Client, sử dụng **cùng một công thức vật lý y hệt Server** (Thuật toán Dead Reckoning), Client sẽ tự bẻ lái chiếc xe theo một đường cong hoàn hảo. Nửa giây sau Server mới gửi gói tin tiếp theo để cập nhật lại những sai số nhỏ.

Bằng cách này, Dead Reckoning có thể giảm lượng gói tin phải gửi qua mạng đi tới 80%!

---

## 4. Rủi Ro Của Ngoại Suy (Lỗi Đâm Xuyên Tường)

Đoán tương lai thì luôn có nguy cơ đoán sai.
Hãy tưởng tượng kẻ địch đang chạy thẳng về phía bức tường. 
1. Mạng bị rớt ngay trước khi hắn tới tường.
2. Client dùng Extrapolation, tiếp tục đẩy hắn chạy thẳng.
3. Kẻ địch... chạy xuyên qua tường luôn (vì Client mù quáng đẩy hắn theo vận tốc cũ).
4. Mạng có lại! Server báo rằng: "Thằng đó đụng tường và quẹo trái rồi cha nội".
5. Client giật mình (Snap), xóa sổ kẻ địch đằng sau tường và Teleport hắn ra ngoài quẹo trái.

> [!WARNING]
> Để tránh hiện tượng Ngoại suy sai lệch quá thô thiển, người ta thường áp dụng quy tắc:
> - Chỉ cho phép Extrapolate trong một khoảng thời gian ngắn (tối đa 250ms - 500ms). Nếu mạng đứt lâu hơn, hãy bắt nhân vật dừng lại đứng im để tránh chạy xuyên tường/bay khỏi bản đồ.
> - Kết hợp nội suy (Lerp) khi mạng có lại thay vì Dịch chuyển tức thời, giúp việc "kéo" kẻ địch về đúng quỹ đạo trông mượt mà hơn.
