# Vấn Đề 27: Con trỏ lơ lửng & Crash Game (Dangling Pointers)

**Vấn đề:**
Người chơi nhắm bắn vào mục tiêu (Enemy 1). Mục tiêu đó vừa bị một viên đạn khác tiêu diệt và bị xóa khỏi RAM. Tia laser của người chơi vẫn tiếp tục tìm tọa độ của Enemy 1 -> Lỗi truy cập bộ nhớ rỗng -> Crash văng game ngay lập tức!

**Nguyên nhân:**
Hệ thống ngắm bắn của bạn lưu giữ một Con Trỏ (Pointer) hoặc Tham Chiếu trỏ tới con quái vật đó. Khi quái vật chết, bộ nhớ bị xóa, nhưng con trỏ vẫn còn trỏ vào ô nhớ cũ chứa toàn rác.

**Giải pháp (Hệ thống ID Thế hệ - Generational IDs / Handles):**
Đừng bao giờ giữ Pointer của một Entity có thể bị chết/xóa. Thay vào đó, dùng `ID`.
Mỗi Entity được cấp 1 số ID duy nhất và 1 số Thế hệ (Generation).

```odin
EntityHandle :: struct {
    index: int,
    generation: int,
}

// Khi người chơi ngắm bắn:
target_handle := enemy_system.get_handle(enemy)

// Mỗi frame, thay vì update trực tiếp target, ta phải hỏi Hệ thống xem nó còn sống không
if enemy_system.is_alive(target_handle) {
    actual_enemy := enemy_system.get_data(target_handle)
    fire_laser(actual_enemy.pos)
} else {
    // Quái đã chết, ngừng bắn!
    target_handle = nil
}
```
*(Đây là một trong những tính năng cốt lõi giúp kiến trúc ECS cực kỳ an toàn và khó bị crash).*
