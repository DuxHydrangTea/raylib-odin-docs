# Chương 7: Vòng Đời của Ám Khí (Projectiles)

Khác với Nhát kiếm cận chiến chỉ tồn tại 0.1s ở trước mặt, một chiếc **Phi Tiêu (Dart)** hoặc **Mũi tên (Bow)** là một vật thể sống: Nó có vận tốc, nó bay vút đi, nó có thể trượt và đâm vào tường (biến mất) hoặc đâm trúng quái vật (nổ tung).

---

## 1. Mở rộng Component Đạn

Trong `ecs/components.odin`, chúng ta không cần thêm Component mới, mà chỉ cần tận dụng `VelocityComponent` cho các Đạn (Projectile).

Đồng thời, ta thêm 1 biến để Đạn biết nó được phóng ra từ ai (để không lỡ tự bắn trúng mình).

```odin
// Cập nhật CombatComponent
CombatComponent :: struct {
    entity_type:   EntityType,
    attack_timer:  f32,      
    attack_speed:  f32,      
    attack_range:  f32,
    is_attacking:  bool,
    owner_id:      EntityID, // MỚI: Chủ nhân của Đạn này là ai?
}
```

## 2. Hàm Bắn Phi Tiêu

Khi Ninja chọn hệ Phi Tiêu bấm phím đánh, thay vì sinh ra vùng Hitbox đứng yên, chúng ta sinh ra một Entity có `Velocity`.

Mở `ecs/entities.odin`:

```odin
spawn_projectile :: proc(attacker_id: EntityID) {
    pos := transforms[attacker_id].position
    vel := velocities[attacker_id]
    stat_info := stats[attacker_id]
    
    proj_id := create_entity()
    
    // 1. Tọa độ (Bắt đầu từ giữa bụng Ninja)
    transforms[proj_id] = TransformComponent{
        position = {pos.x, pos.y + 16},
        size = {16, 16}, // Phi tiêu nhỏ
    }
    
    // 2. Vận tốc (Bay cực nhanh)
    SPEED :: 600.0
    vx: f32 = 0
    if vel.facing_right {
        vx = SPEED
    } else {
        vx = -SPEED
    }
    
    velocities[proj_id] = VelocityComponent{
        vel = {vx, 0}, // Bay thẳng, không rớt (Không trọng lực)
        is_grounded = false,
    }
    
    // 3. Sát thương & Quyền sở hữu
    combats[proj_id] = CombatComponent{
        entity_type = .Projectile,
        owner_id = attacker_id, // Đánh dấu bản quyền
        attack_timer = 2.0,     // Tuổi thọ: Tự hủy sau 2 giây nếu bay mù mịt ra ngoài map
    }
    
    stats[proj_id] = StatsComponent{ damage = stat_info.damage }
}
```

> [!TIP]
> Trong Game Loop, Phi Tiêu sẽ tự động bay nhờ vào `system_physics_and_input` đã viết ở Chương 1! Vì nó có `VelocityComponent`. Tuy nhiên bạn cần sửa lại một chút để Trọng lực `GRAVITY` không tác động lên `Projectile`, trừ phi bạn muốn ném một cục đá hình vòng cung (Parabol).

## 3. Va Chạm Của Đạn

Mở `ecs/systems.odin` và sửa `system_hitbox_collision` ở chương trước:

```odin
system_projectile_collision :: proc(dt: f32) {
    for id in entities {
        if id not_in combats do continue
        c := &combats[id]
        if c.entity_type != .Projectile do continue
        
        // 1. Tự hủy do hết hạn (Tuổi thọ 2 giây)
        c.attack_timer -= dt
        if c.attack_timer <= 0 {
            destroy_entity(id)
            continue
        }
        
        my_rect := rl.Rectangle{transforms[id].position.x, transforms[id].position.y, transforms[id].size.x, transforms[id].size.y}
        
        // 2. Kiểm tra va chạm với Tường đá (Đạn vỡ)
        if check_map_collision(my_rect) { // Hàm check_map_collision viết ở Chương 2
            destroy_entity(id)
            // TODO: Sinh ra Hiệu ứng (Particle) tia lửa tóe ra ở góc tường
            continue
        }
        
        // 3. Kiểm tra va chạm với Quái vật
        hit_target := false
        for target_id in entities {
            // Bỏ qua nếu chính là Chủ nhân (Ninja bắn ra)
            if target_id == c.owner_id do continue 
            if target_id not_in combats do continue
            
            // Nếu trúng Quái vật
            if combats[target_id].entity_type == .Monster {
                t_rect := rl.Rectangle{transforms[target_id].position.x, transforms[target_id].position.y, transforms[target_id].size.x, transforms[target_id].size.y}
                
                if rl.CheckCollisionRecs(my_rect, t_rect) {
                    apply_damage(target_id, stats[id].damage)
                    hit_target = true
                    break // Chỉ bắn trúng 1 con, không bắn xuyên (Trừ phi skill xuyên thấu)
                }
            }
        }
        
        // Hủy đạn nếu đã đâm trúng
        if hit_target {
            destroy_entity(id)
        }
    }
}
```

Hoàn hảo! Lúc này, bạn bấm phím tấn công, Ninja Tiêu của bạn sẽ phóng ra những hình vuông nhỏ lao vút qua màn hình. Hãy thay hình vuông đó bằng 1 cái `Texture2D` ngôi sao Ninja (Shuriken) ở phần `render_game` nhé! Mọi thứ sẽ mượt như lụa. 

Trong Chương 8, chúng ta sẽ thả vài con Cóc Độc và Ốc Sên vào Bản đồ để bạn tập bắn.
