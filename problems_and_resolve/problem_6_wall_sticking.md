# Vấn Đề 6: Kẹt vào tường (Wall Sticking)

**Vấn đề:**
Trong game Platformer (Mario), khi nhảy lên áp sát vào bờ tường và bấm giữ nút tiến lên, nhân vật bị treo lơ lửng trên tường, không chịu rơi xuống đất.

**Nguyên nhân:**
Khi di chuyển, mã nguồn của bạn dồn nhân vật vào tường. Hệ thống va chạm nhận thấy sự giao cắt và dùng lực "đẩy ra". Trọng lực (Gravity) đẩy nhân vật xuống, nhưng va chạm tiếp tục đẩy ngang ra. Sự giằng co liên tục khiến nhân vật bị kẹt do sai số thập phân.

**Giải pháp:**
Tách biệt việc xử lý va chạm trục X và trục Y thành 2 bước riêng lẻ.
1. Di chuyển trục X.
2. Kiểm tra va chạm trục X -> Nếu đụng tường, dừng trục X lại.
3. Di chuyển trục Y (Trọng lực).
4. Kiểm tra va chạm trục Y -> Nếu đụng sàn, dừng trục Y lại.

```odin
// BƯỚC 1: Trục X
player.pos.x += vel.x * dt
if is_colliding_with_wall(player.pos) {
    player.pos.x -= vel.x * dt // Lùi lại
    vel.x = 0
}

// BƯỚC 2: Trục Y (Độc lập hoàn toàn)
vel.y += gravity * dt
player.pos.y += vel.y * dt
if is_colliding_with_wall(player.pos) {
    player.pos.y -= vel.y * dt // Đụng trần nhà hoặc sàn
    vel.y = 0
}
```
*Việc tách trục sẽ giúp bộ máy Vật lý không bị bối rối và giải quyết triệt để lỗi Wall Sticking.*
