# Chương 6: Hệ thống Kỹ Năng & Tung Chiêu (Hitbox)

Trong Action RPG, việc tấn công không đơn giản là gán số trừ máu như Turn-based. Khi bạn vung kiếm, game phải tạo ra một "Vùng chém" vô hình phía trước nhân vật (gọi là **Hitbox cận chiến**). Bất kỳ con quái nào vô tình chạm vào vùng này trong vài phần trăm giây sẽ bị trừ máu.

Ngược lại, nếu bạn dùng Cung/Tiêu, game phải tạo ra một viên đạn (Projectile) bay xuyên qua bản đồ.

---

## 1. Thuật toán Vung Kiếm (Melee Hitbox)

Khi phím `Z` (hoặc Nút Đánh) được bấm, ta kiểm tra xem Cooldown (Thời gian hồi chiêu) đã xong chưa. Nếu xong, nhân vật sẽ chuyển sang trạng thái `is_attacking = true`.

Mở `ecs/systems.odin` và tạo `system_combat`.

```odin
package ecs

import rl "vendor:raylib"

system_combat :: proc(dt: f32) {
    for id in entities {
        if id not_in combats do continue
        c := &combats[id]
        
        // 1. Giảm Cooldown
        if c.attack_timer > 0 {
            c.attack_timer -= dt
        }
        
        // 2. Chỉ xử lý cho Player (Ninja) khi bấm phím Đánh (Phím J)
        if c.entity_type == .Player {
            if rl.IsKeyPressed(.J) && c.attack_timer <= 0 {
                // Bắt đầu chém!
                c.is_attacking = true
                c.attack_timer = c.attack_speed // Khóa mõm, chờ hồi chiêu
                
                // Gọi hàm sinh ra vùng sát thương
                spawn_melee_hitbox(id)
            }
        }
    }
}
```

## 2. Sinh ra Hitbox Cận Chiến (Melee) vô hình

Cơ chế: Ta sẽ tạo ra một Entity Tạm Thời đại diện cho Cú Chém. Thực thể này không vẽ hình ảnh gì cả, nó chỉ là 1 hình chữ nhật (Hitbox) tồn tại trong đúng `0.1s` (Vừa đủ 1 frame chém) ở ngay trước mặt Ninja. Ai chạm vào hình chữ nhật này sẽ ăn đòn.

Thêm vào `ecs/entities.odin`:

```odin
// Cần biết Ninja đang quay mặt sang trái hay phải để sinh Hitbox cho đúng
// (Giả sử bạn đã thêm biến `facing_right: bool` vào VelocityComponent)

spawn_melee_hitbox :: proc(attacker_id: EntityID) {
    pos := transforms[attacker_id].position
    vel := velocities[attacker_id]
    combat_info := combats[attacker_id]
    stat_info := stats[attacker_id]
    
    hitbox_id := create_entity()
    
    // Tính toán tọa độ Vùng chém
    hitbox_x := pos.x 
    if vel.facing_right {
        hitbox_x += 32.0 // Chém sang phải
    } else {
        hitbox_x -= combat_info.attack_range // Chém sang trái
    }
    
    // Khởi tạo Hitbox
    transforms[hitbox_id] = TransformComponent{
        position = {hitbox_x, pos.y},
        size = {combat_info.attack_range, 64}, // Rộng bằng Tầm đánh, cao bằng Người
    }
    
    // Khởi tạo sát thương cho Hitbox này
    combats[hitbox_id] = CombatComponent{
        entity_type = .Projectile, // Coi như đạn
        attack_timer = 0.1,        // Tồn tại đúng 0.1 giây rồi tự hủy
        // Sát thương của cú chém lấy từ lực tay của Ninja
    }
    stats[hitbox_id] = StatsComponent{ damage = stat_info.damage }
}
```

## 3. Hệ thống Hủy Hitbox và Xét Va Chạm

Bây giờ, ta cần một System để xử lý tuổi thọ của các Hitbox (Cú chém) này, đồng thời kiểm tra xem chúng có chém trúng quái vật nào không.

Quay lại `ecs/systems.odin`:

```odin
system_hitbox_collision :: proc(dt: f32) {
    // Duyệt qua tất cả các Hitbox (Đạn/Cú chém)
    for id in entities {
        if id not_in combats do continue
        
        c := &combats[id]
        if c.entity_type != .Projectile do continue
        
        // Trừ tuổi thọ của Hitbox
        c.attack_timer -= dt
        if c.attack_timer <= 0 {
            // Hitbox hết hạn -> Xóa xổ (Kết thúc cú chém)
            destroy_entity(id)
            continue
        }
        
        // KỊCH BẢN: Hitbox đang tồn tại, kiểm tra va chạm với mọi Quái Vật
        my_rect := rl.Rectangle{transforms[id].position.x, transforms[id].position.y, transforms[id].size.x, transforms[id].size.y}
        my_damage := stats[id].damage
        
        for target_id in entities {
            if target_id not_in combats do continue
            
            // Chỉ chém quái vật (Không tự chém mình)
            if combats[target_id].entity_type == .Monster {
                target_rect := rl.Rectangle{transforms[target_id].position.x, transforms[target_id].position.y, transforms[target_id].size.x, transforms[target_id].size.y}
                
                // Thuật toán kiểm tra 2 Hình chữ nhật có đè lên nhau không
                if rl.CheckCollisionRecs(my_rect, target_rect) {
                    // TRÚNG ĐÒN! Gọi hàm trừ máu ở Chương 4
                    apply_damage(target_id, my_damage)
                    
                    // (Tùy chọn) Hủy Hitbox ngay khi chạm 1 con đầu tiên để không chém trúng 2 con
                    destroy_entity(id) 
                    break 
                }
            }
        }
    }
}
```

> [!NOTE]
> Đây là kiến trúc **Broad-casting Hitbox** rất phổ biến trong các game đối kháng (Fighting Games) và Action RPG. Bất kỳ kỹ năng nào (Chém bồi, Đâm chớp nhoáng, Quạt lửa) thực chất chỉ là việc sinh ra các hình chữ nhật (Hitbox) với tọa độ, kích thước và Sát thương khác nhau vào những thời điểm khác nhau!

Ở chương 7 tiếp theo, chúng ta sẽ mở rộng logic này để bắn ra Đạn (Projectile cho Tiêu, Cung) – thay vì Hitbox đứng yên 0.1s, Đạn sẽ có `Velocity` để bay vút qua màn hình!
