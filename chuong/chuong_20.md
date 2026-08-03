# Chương 20: "Game Juice" - Cảm giác Game (Game Feel)

Chương cuối cùng này không dạy bạn cú pháp lập trình, mà dạy bạn "Nghệ thuật Thiết kế Game".
Bạn có bao giờ tự hỏi: Tại sao cùng một code "Bấm phím -> Nhân vật nhảy", nhưng Mario nhảy chơi rất sướng tay, còn game mình làm nhảy cảm giác như khúc gỗ? Sự khác biệt nằm ở **"Game Juice"** (Độ ép nước).

Game Juice là việc đánh lừa bộ não người chơi bằng hàng loạt phản hồi vi mô (micro-feedback) cực nhanh, khiến cho mỗi thao tác đều cảm thấy có sức mạnh và sức nặng.

Dưới đây là 5 gia vị bắt buộc phải rắc vào game:

---

## 1. Rung màn hình (Screen Shake)

Mỗi khi nhân vật bị trúng đạn, hay khi nổ bom, hãy làm màn hình rung lên.
* **Cách code:** Thêm biến `shake_intensity`. Khi nổ, gán nó = 10. Trong vòng lặp, giảm dần nó về 0. Lấy số ngẫu nhiên từ `-shake_intensity` đến `+shake_intensity` cộng vào `camera.offset`.

## 2. Khựng hình (Hit Stop / Sleep)

Khi bạn chém trúng quái vật trong game đối kháng, game sẽ khựng lại (đứng hình) khoảng 50 mili-giây (0.05 giây).
* **Hiệu ứng tâm lý:** Nó tạo cảm giác vũ khí của bạn vừa va chạm vào một vật siêu cứng (ma sát cao), khiến cú chém có "lực" hơn rất nhiều so với việc lưỡi kiếm lướt qua mượt mà.
* **Cách code:** Thêm biến `hit_stop_timer`. Khi trúng đòn, set timer. Nếu timer > 0, bỏ qua lệnh Update(), nhưng vẫn chạy lệnh Draw().

## 3. Co giãn biến dạng (Squash & Stretch)

Đừng để nhân vật là một bức ảnh cứng đơ.
* Khi nhân vật nhảy lên, hãy kéo dài chiều dọc (Stretch), bóp hẹp chiều ngang.
* Khi nhân vật rớt xuống đất, bóp dẹp chiều dọc (Squash), bè rộng chiều ngang.
* **Cách code:** Dùng hàm `DrawTexturePro`, thay đổi tham số `dest` dựa vào vận tốc Y của nhân vật.

## 4. Hạt (Particles) văng khắp nơi

Một đồng xu rớt ra không bao giờ thú vị bằng việc nó nổ ra 5 tia sáng nhỏ lấp lánh (Sparkles) xung quanh. Đi bộ trên đất phải văng bụi ra đằng sau.
Dùng hệ thống hạt ở Chương 13 để nhồi nhét thật nhiều hiệu ứng thị giác này vào mọi thao tác của người chơi.

## 5. Tweening & Easing

Giao diện UI (Nút bấm, bảng cài đặt) bật lên màn hình không bao giờ được xuất hiện cái "bụp" một cách tuyến tính (vận tốc đều). 
Chúng phải nảy lên (Elastic, Bounce) hoặc tuột vào mượt mà (Ease Out, Ease In). 
* **Cách code:** Sử dụng các hàm nội suy Easing (Odin có module toán học cho việc này, hoặc bạn có thể tự viết bằng công thức `x * x` cho EaseIn). Ví dụ khi di chuột vào nút bấm, kích thước nút phóng to lên `1.2x` bằng Tweening, đi kèm một tiếng "Tick" nhỏ xíu.

---

### LỜI KHUYÊN CUỐI CÙNG
Khi bạn làm xong logic game, game của bạn mới hoàn thiện được 50%.
50% thời gian còn lại, hãy dành riêng nó để code **"Game Juice"**. Đó mới là điểm mấu chốt quyết định game của bạn là rác hay là kiệt tác.

**Xin chúc mừng. Khóa học thực sự đã khép lại. Thế giới Indie Game Development đang chờ đón bạn. Tiến lên thôi!**
