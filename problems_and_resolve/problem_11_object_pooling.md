# Vấn Đề 11: Lỗi tạo mới Object liên tục (Instantiation Lag)

**Vấn đề:**
Khi bắn một khẩu súng máy (Machine Gun), cứ mỗi mili-giây lại có đạn mới sinh ra. FPS của game rớt thê thảm từ 60 xuống 15.

**Nguyên nhân:**
Mỗi lần nhấn nút bắn, bạn gọi lệnh `new(Bullet)`. Lệnh này xin Hệ điều hành cấp phát một mảng RAM nhỏ. Việc giao tiếp với Hệ điều hành để xin/trả RAM (Allocate/Deallocate) là cực kỳ đắt đỏ và tốn thời gian đối với CPU.

**Giải pháp (Object Pooling):**
Khởi tạo toàn bộ lượng đạn tối đa ngay khi game mới bật (Màn hình Loading). Khi bắn, chỉ cần tìm viên đạn đang "Tắt" và "Bật" nó lên. Khi đạn nổ, không xóa nó khỏi RAM mà chỉ đánh dấu "Tắt" để chờ tái chế.

```odin
MAX_BULLETS :: 1000
bullets: [MAX_BULLETS]Bullet // Đã chiếm sẵn RAM tĩnh

fire_weapon :: proc() {
    // Tái chế (Pooling)
    for i in 0..<MAX_BULLETS {
        if !bullets[i].active {
            bullets[i].active = true // Hồi sinh viên đạn
            bullets[i].pos = gun_barrel
            return
        }
    }
    // Nếu hết mảng 1000 viên, ta không bắn được nữa, nhưng tuyệt đối không lag!
}
```
