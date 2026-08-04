# Chương 7: Bồi Thường Độ Trễ (Lag Compensation)

Client-side Prediction (Chương 6) giúp bản thân bạn di chuyển mượt mà không bị Input Lag. Nhưng nó không giải quyết được vấn đề khi bạn tương tác với **Người chơi khác**.

Chào mừng bạn đến với Kỹ thuật bắn súng Mạng: **Lag Compensation**.

---

## 1. Nghịch Lý Của Kẻ Đang Di Chuyển

Giả sử bạn đang nhắm súng vào đầu một kẻ địch đang chạy ngang qua. Bạn bấm Chuột Trái (Bắn).
Trên màn hình của bạn, máu nổ (Trúng!). Nhưng Server lại báo là... Trượt (Miss). Tại sao?

Hãy nhớ lại bài học về Nội Suy (Interpolation) ở Chương 5:
- Màn hình của bạn luôn vẽ kẻ địch TRỄ HƠN một chút so với thực tế (Khoảng 50ms - 100ms) để di chuyển mượt.
- Hơn nữa, gói tin "Bắn" của bạn tốn thêm 50ms để bay lên Server.
- Lúc Server nhận được lệnh Bắn, thời gian thực đã trôi qua 100ms. Trong 100ms đó, kẻ địch đã chạy qua khỏi hồng tâm của bạn từ đời nào rồi!

**Kết quả:** Nếu Server dùng toạ độ hiện tại của nó để phán xét, bạn sẽ LUÔN LUÔN bắn trượt mọi mục tiêu đang di chuyển, trừ khi bạn cố tình "bắn đón" (nhắm ra đằng trước mặt kẻ địch). Điều này hủy hoại mọi game bắn súng Hit-scan (CS:GO, Valorant).

---

## 2. Giải Pháp: Bồi Thường Độ Trễ

Triết lý của Lag Compensation là: **"Hãy đối xử công bằng với người bắn"**.
Nếu trên màn hình của người bắn, lúc họ bóp cò, tâm súng đang chỉ ngay đầu kẻ địch, thì hệ thống phải công nhận là Trúng Đầu, bất chấp việc trên Server kẻ địch đã chạy đi chỗ khác.

Làm sao Server biết được trên màn hình của người bắn lúc đó đang hiển thị cái gì?
Bằng cách **Tua Ngược Thời Gian (Rollback/Time Travel)**.

---

## 3. Cách Thuật Toán Rollback Hoạt Động

Để làm được trò này, Server phải có khả năng ghi nhớ Quá Khứ.

### Bước 1: Lưu giữ lịch sử (History Buffer)
Server liên tục lưu lại tọa độ của TẤT CẢ mọi người chơi vào một mảng lịch sử (History Buffer) kéo dài khoảng 1 giây gần nhất. Mỗi bản lưu đi kèm với một mốc thời gian (Timestamp).

### Bước 2: Client khai báo thời điểm bắn
Khi Client bấm Chuột Trái, gói tin gửi lên Server không chỉ ghi là "Tao bắn", mà phải ghi rõ:
*"Tao bắn viên đạn này vào lúc thời gian ảo của tao là: `T = 100`"*.

### Bước 3: Server tua ngược (Rewind)
Khi Server nhận lệnh bắn, có thể lúc này thời gian thật trên Server đã là `T = 150`.
Server nhận thấy viên đạn được bắn ở `T = 100`. Server sẽ:
1. "Bấm nút Dừng hình" thế giới hiện tại.
2. Mở cuốn sổ lịch sử (History Buffer), lôi tất cả người chơi **dịch chuyển lùi lại** đúng toạ độ mà họ đang đứng ở thời điểm `T = 100`. (Đây chính là bức tranh giống hệt những gì người bắn nhìn thấy trên màn hình).

### Bước 4: Kiểm tra va chạm (Hit Registration)
Khi mọi người đã bị kéo lùi về quá khứ `T=100`, Server vẽ tia đạn (Raycast).
- Nếu tia đạn trúng đầu kẻ địch -> Khai báo Headshot!
- Nếu tia đạn trượt -> Khai báo Miss.

### Bước 5: Trả lại thực tại (Fast Forward)
Xử lý xong, Server lập tức dịch chuyển mọi người chơi về lại đúng thời điểm hiện tại `T=150` và cho game tiếp tục chạy bình thường. 
Toàn bộ quá trình từ lúc tua ngược đến lúc đưa về hiện tại diễn ra cực nhanh (chưa tới 1 mili-giây trên CPU Server), nên những người chơi khác hoàn toàn không nhận ra mình vừa bị lôi về quá khứ!

---

## 4. Vấn Đề Gây Tranh Cãi: "Bị bắn chết sau bức tường"

Lag Compensation giải quyết được việc bắn chuẩn xác, nhưng nó sinh ra một tác dụng phụ cực kì ức chế cho Kẻ Bị Bắn: Kẻ bị bắn cảm giác như mình bị trúng đạn dù đã nấp sau tường!

**Kịch bản:**
1. Kẻ địch (Ping 200ms) nhắm bắn bạn.
2. Cùng lúc đó, bạn chạy nấp vào sau bức tường tường. Trên màn hình của bạn, bạn ĐÃ an toàn.
3. Tuy nhiên, trên màn hình của kẻ địch (vì Ping cao nên hắn thấy mọi thứ chậm hơn 200ms), bạn VẪN ĐANG ở ngoài tường.
4. Hắn bóp cò. Server tua ngược thời gian về 200ms trước, và xác nhận: Hắn bắn trúng bạn!
5. Bạn chết một cách tức tưởi dù màn hình của bạn đã ở sau bức tường.

> [!NOTE]
> Đây là đặc thù không thể tránh khỏi của Lag Compensation. Hầu hết các game FPS chấp nhận điều này (Ưu tiên người Bắn gọi là **Favor the Shooter**). Tuy nhiên, để tránh lạm dụng, các game thường giới hạn thời gian Rollback tối đa chỉ khoảng 200ms-300ms. Nếu Ping của người bắn cao hơn 300ms, Server sẽ từ chối bồi thường độ trễ cho họ.
