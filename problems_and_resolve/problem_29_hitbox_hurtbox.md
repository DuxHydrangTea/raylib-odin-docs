# Vấn Đề 29: Xung đột Vùng sát thương (Hitbox vs Hurtbox)

**Vấn đề:**
Game đối kháng. Nhân vật A vung kiếm chém nhân vật B. Bạn dùng hộp va chạm (Collider) của A để va chạm với B. Chuyện gì xảy ra nếu 2 nhân vật đứng im và thanh kiếm đụng vào người B? B mất máu dù A không hề tung đòn!

**Nguyên nhân:**
Bạn đang dùng chung một loại Hộp Va Chạm (Collision Box) cho cả 2 mục đích: Vật lý (Đẩy nhau, chặn tường) và Chiến đấu (Gây sát thương, Nhận sát thương).

**Giải pháp (Tách biệt logic):**
Một nhân vật phức tạp cần có ít nhất 3 loại Hộp Hư Cấu:
1. **Collision Box (Màu xanh dương):** Hộp cứng, nằm dưới chân, dùng để trượt trên sàn và không đi xuyên tường.
2. **Hurtbox (Màu xanh lá):** Hộp thịt, bọc quanh cơ thể. Kẻ địch chém trúng hộp này thì bạn mất máu. Đầu có Hurtbox riêng để nhận x2 sát thương (Headshot).
3. **Hitbox (Màu đỏ):** Hộp vũ khí, chỉ xuất hiện đúng 0.2 giây khi tung đòn chém. Trượt theo đường vung kiếm. Nếu hộp Đỏ này chạm vào hộp Xanh Lá của đối phương -> Trừ máu.

```odin
// Khi đang chém
if is_attacking && frame_index == 3 {
    sword_hitbox := rl.Rectangle{player.x + 20, player.y, 40, 40}
    
    if rl.CheckCollisionRecs(sword_hitbox, enemy_hurtbox) {
        enemy.take_damage(10)
    }
}
```
