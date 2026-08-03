# Vấn Đề 7: Tốc độ phụ thuộc FPS (Frame-rate Dependence)

**Vấn đề:**
Bạn chơi game trên laptop cũ đạt 30 FPS, game chạy chậm rì dễ chơi. Khi bạn tải game đó sang dàn PC mới với 144 FPS, nhân vật chạy như siêu xe, đạn bay không kịp nhìn, game trở nên siêu khó.

**Nguyên nhân:**
Bạn cộng thẳng vận tốc vào tọa độ mà không quan tâm đến thời gian.
`pos.x += speed`
Nếu 1 giây chạy 30 vòng lặp (30 FPS) -> Đi được 30 đoạn. Chạy 144 vòng -> Đi được 144 đoạn.

**Giải pháp:**
Mọi công thức liên quan đến tốc độ, gia tốc hoặc thời gian chờ (cooldown) bắt buộc phải nhân với **Delta Time (dt)** - Khoảng thời gian trôi qua giữa 2 frame.

```odin
// Lấy dt (tính bằng giây, thường là 0.016s ở 60FPS)
dt := rl.GetFrameTime()

// SAI:
// pos.x += 10 

// ĐÚNG:
pos.x += speed_per_second * dt

// GIA TỐC VÀ TRỌNG LỰC:
velocity.y += gravity * dt
pos.y += velocity.y * dt
```
Nhờ `dt`, cho dù máy lag (dt cao) hay máy xịn (dt thấp), khoảng cách nhân vật đi được sau 1 giây luôn bằng đúng `speed_per_second`.
