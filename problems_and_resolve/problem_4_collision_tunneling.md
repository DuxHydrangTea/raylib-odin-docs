# Vấn Đề 4: Đạn bay xuyên tường (Collision Tunneling)

**Vấn đề:**
Bắn đạn tốc độ siêu cao vào một bức tường rất mỏng. Viên đạn bay xuyên qua tường, không hề phát nổ hay va chạm.

**Nguyên nhân:**
Kiểm tra va chạm được gọi rời rạc mỗi khung hình (frame). Nếu Frame 1 đạn ở TRƯỚC tường, Frame 2 đạn đi quá xa và nằm ở SAU tường. Ở cả 2 frame, viên đạn đều không "nằm trong" bức tường, nên hàm CheckCollision trả về false.

**Giải pháp (Kỹ thuật Raycast / Swept AABB):**
Thay vì kiểm tra đạn có giao cắt với tường ở frame hiện tại không, hãy kiểm tra **đoạn thẳng** nối từ vị trí cũ đến vị trí mới của viên đạn.

```odin
// Vị trí frame trước
old_pos := bullet.pos 
// Vị trí frame nay
bullet.pos += bullet.vel * dt 

// Kiểm tra đoạn thẳng nối giữa cũ và mới có cắt bức tường không
hit_point: rl.Vector2
if rl.CheckCollisionLines(old_pos, bullet.pos, wall_start, wall_end, &hit_point) {
    // Đạn đã bay xuyên qua tường, ép nó dừng lại ở điểm va chạm!
    bullet.pos = hit_point
    explode_bullet(bullet)
}
```
