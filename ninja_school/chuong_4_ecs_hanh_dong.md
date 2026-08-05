# Chương 4: Kiến Trúc ECS Cho Game Hành Động

Ở thể loại RPG đánh nhau, mỗi thực thể (Ninja, Quái vật, Bù nhìn) không chỉ cần Tọa độ, Vận tốc mà còn cần máu (HP), năng lượng (MP), Lực tay, Kháng phép... 

Sử dụng kiến trúc Entity Component System (ECS) với Data Locality (Struct of Arrays) không chỉ giúp game mượt mà mà còn tách biệt logic của Kỹ năng và AI ra khỏi nhau.

---

## 1. Các Component Nền Tảng

Mở file `ecs/components.odin` và định nghĩa thêm các Component RPG kinh điển:

```odin
package ecs

// 1. Component Thống Kê (RPG Stats)
StatsComponent :: struct {
    hp, max_hp: int,
    mp, max_mp: int,
    damage:     int,    // Lực tay tấn công
    defense:    int,    // Phòng thủ
    speed:      f32,    // Tốc độ di chuyển
}

// 2. Enum định dạng Loại Thực thể
EntityType :: enum {
    Player,
    Monster,
    NPC,
    Projectile, // Ám khí (Phi tiêu)
}

// 3. Component Combat (Chiến đấu)
CombatComponent :: struct {
    entity_type:   EntityType,
    target_id:     EntityID, // Mục tiêu đang nhắm đến
    attack_timer:  f32,      // Thời gian chờ đánh đòn tiếp theo (Cooldown)
    attack_speed:  f32,      // Tốc độ đánh
    attack_range:  f32,      // Tầm đánh
    is_attacking:  bool,
}

// Danh sách các ID Entity còn sống
entities: [dynamic]EntityID

// SoA Mảng Component
stats:      map[EntityID]StatsComponent
combats:    map[EntityID]CombatComponent
```

> [!NOTE]
> Tại sao dùng `map[EntityID]` thay vì `[dynamic]` cho Stats?
> Không phải thực thể nào cũng có máu (ví dụ: Nút bấm trên đường, Cột mốc). Việc dùng `map` (Sparse Set) giúp tiết kiệm bộ nhớ cho những Entity không cần thiết.

## 2. Hệ thống Quản lý Vòng Đời Sinh/Diệt (Entities)

Tạo file `ecs/entities.odin`. Ở đây chúng ta áp dụng kỹ thuật **Object Pooling (Tái sử dụng ID)** đã nhắc đến ở Chương 22 của game Nông Trại để quản lý.

```odin
package ecs

next_id: EntityID = 0
free_ids: [dynamic]EntityID // Kho chứa ID của những quái vật đã chết

create_entity :: proc() -> EntityID {
    id: EntityID
    if len(free_ids) > 0 {
        id = pop(&free_ids) // Lấy lại ID cũ dùng tiếp
    } else {
        id = next_id
        next_id += 1
    }
    
    append(&entities, id)
    return id
}

destroy_entity :: proc(id: EntityID) {
    // 1. Xóa nó khỏi danh sách entities đang hoạt động
    for i in 0..<len(entities) {
        if entities[i] == id {
            unordered_remove(&entities, i)
            break
        }
    }
    
    // 2. Dọn dẹp Dữ liệu Component
    delete_key(&stats, id)
    delete_key(&combats, id)
    
    // Chú ý: Ở đây bạn cần xóa cả Transform và Velocity nếu đang dùng `map`
    
    // 3. Cho ID vào kho tái chế
    append(&free_ids, id)
}
```

## 3. Hàm Bơm Máu & Trừ Máu Cơ Bản

Bây giờ bạn có thể dễ dàng viết một hàm tiện ích để trừ máu bất kỳ Entity nào (bất kể nó là Ninja hay Quái Cóc, Heo rừng).

```odin
apply_damage :: proc(victim_id: EntityID, raw_damage: int) {
    if victim_id not_in stats do return // Trúng thực thể không có máu (như cột gỗ)
    
    s := &stats[victim_id]
    
    // Thuật toán sát thương đơn giản: Sát thương - Phòng thủ
    actual_damage := raw_damage - s.defense
    if actual_damage < 1 do actual_damage = 1 // Ít nhất cũng mất 1 máu
    
    s.hp -= actual_damage
    
    if s.hp <= 0 {
        s.hp = 0
        destroy_entity(victim_id)
        // TODO: Rớt tiền vàng, vật phẩm, phát âm thanh quái chết
    }
}
```

Sức mạnh của ECS nằm ở chỗ: Hàm `apply_damage` này hoàn toàn mù tịt về việc ai đang đánh ai. Dù là Ninja chém Bù nhìn, Quái cắn Ninja, hay Lửa đốt Quái... chỉ cần truyền đúng `EntityID`, logic sát thương sẽ luôn chạy chuẩn xác!

Chương tiếp theo, chúng ta sẽ định nghĩa sức mạnh của 6 Môn Phái Huyền Thoại của trường Haruna và Hirosaki.
