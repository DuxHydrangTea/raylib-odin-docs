# Chương 8: AI Quái Vật Platformer (Cóc Độc & Ốc Sên)

Làm quái vật cho Platformer thú vị và đau đầu hơn Top-down rất nhiều. Con quái vật không thể cứ mù quáng đuổi theo Ninja theo đường chim bay được, vì nó sẽ cắm đầu đi thẳng xuống vực sâu hoặc đâm vào tường cộc cộc.

Chúng ta sẽ sử dụng cấu trúc **State Machine (Máy Trạng Thái)** siêu kinh điển cho AI: `Wander` (Đi tuần) và `Chase` (Rượt đuổi).

---

## 1. Máy Trạng Thái AI

Mở `ecs/components.odin` và định nghĩa:

```odin
AIState :: enum {
    Wander, // Đi thẩn thơ quanh khu vực
    Chase,  // Gầm gừ rượt theo Ninja
}

AIComponent :: struct {
    state: AIState,
    patrol_center: f32, // Tọa độ X gốc để đi tuần không bị lạc
    patrol_range: f32,  // Phạm vi đi tuần (VD: 100 pixel quanh gốc)
    timer: f32,         // Đồng hồ đếm ngược (VD: Đứng im 2 giây rồi đi tiếp)
}
```

Và khai báo mảng `ais: map[EntityID]AIComponent`.

## 2. Khởi tạo một con Cóc

```odin
// entities.odin
spawn_monster :: proc(x, y: f32) {
    id := create_entity()
    
    transforms[id] = TransformComponent{
        position = {x, y},
        size = {32, 32}, // Con cóc bé hơn người
    }
    velocities[id] = VelocityComponent{}
    
    stats[id] = StatsComponent{
        hp = 150, max_hp = 150,
        damage = 10, defense = 2,
        speed = 50.0, // Chạy chậm
    }
    
    combats[id] = CombatComponent{
        entity_type = .Monster,
        attack_range = 40.0, // Tầm cắn cận chiến
    }
    
    ais[id] = AIComponent{
        state = .Wander,
        patrol_center = x,
        patrol_range = 150.0,
        timer = 0.0,
    }
}
```

## 3. Trí Tuệ của Cóc (System AI)

Mở `ecs/systems.odin` và tạo `system_ai`:

```odin
import "core:math"

system_ai :: proc(dt: f32) {
    // Lấy tọa độ Ninja (Giả sử id = 0)
    if len(entities) == 0 do return
    player_id := entities[0]
    if player_id not_in transforms do return
    player_pos := transforms[player_id].position
    
    for id in entities {
        if id not_in ais do continue
        ai := &ais[id]
        t := &transforms[id]
        v := &velocities[id]
        s := &stats[id]
        c := &combats[id]
        
        // 1. CHUYỂN ĐỔI TRẠNG THÁI (Transition)
        // Nếu Ninja lại gần dưới 200 Pixel -> Chuyển sang rượt đuổi
        dist_x := math.abs(t.position.x - player_pos.x)
        dist_y := math.abs(t.position.y - player_pos.y)
        
        // Trong Platformer, quái chỉ rượt nếu chung một mặt phẳng ngang (dist_y nhỏ)
        if dist_x < 200.0 && dist_y < 100.0 {
            ai.state = .Chase
        } else {
            ai.state = .Wander
        }
        
        // 2. THỰC THI TRẠNG THÁI (Action)
        switch ai.state {
        case .Wander:
            // Lượn lờ trái phải quanh điểm patrol_center
            if ai.timer > 0 {
                ai.timer -= dt
                v.vel.x = 0 // Đứng im suy nghĩ
            } else {
                // Đi bừa 1 hướng
                if v.vel.x == 0 do v.vel.x = s.speed
                
                // Nếu đi quá xa giới hạn tuần tra, quay đầu
                if t.position.x > ai.patrol_center + ai.patrol_range {
                    v.vel.x = -s.speed
                } else if t.position.x < ai.patrol_center - ai.patrol_range {
                    v.vel.x = s.speed
                }
                
                // Đi được 1 lúc thì dừng lại nghỉ
                if rl.GetRandomValue(0, 100) < 2 {
                    ai.timer = 2.0 // Đứng nghỉ 2 giây
                }
            }
            
        case .Chase:
            // Lao tới Ninja
            if t.position.x < player_pos.x {
                v.vel.x = s.speed * 1.5 // Rượt nhanh hơn 50%
            } else {
                v.vel.x = -s.speed * 1.5
            }
            
            // Nếu đủ gần thì Tấn Công
            if dist_x < c.attack_range && c.attack_timer <= 0 {
                v.vel.x = 0 // Dừng lại để cắn
                spawn_melee_hitbox(id) // Cóc dùng hàm Hitbox hệt như Ninja chém!
                c.attack_timer = 2.0   // 2 giây cắn 1 cái
            }
        }
    }
}
```

> [!IMPORTANT]
> **Edge Detection (Nhận diện Vực sâu)**
> Quái vật của bạn lúc này sẽ cắm đầu chạy theo bạn rơi tõm xuống vực. Để khắc phục, bạn có thể kiểm tra xem ô lưới (Grid) ở dưới chân phía trước của quái vật có phải là số `0` (Không khí) hay không. Nếu là số `0`, quái vật sẽ không dám bước tiếp mà sẽ tự động quay đầu! Đây là thủ thuật được dùng cho loài rùa báo thù Koopa Troopa trong Super Mario.

Đến đây, bạn đã có một "Hệ sinh thái" tương tác hoàn chỉnh: Ninja di chuyển, bắn đạn. Đạn trúng cóc. Cóc trừ máu. Cóc thấy Ninja, Cóc rượt Ninja, Cóc cắn ra Hitbox, Ninja mất máu.

Ở Chương 9, ta sẽ làm cho logic trừ máu này sâu sắc hơn với Toán Học: Tỷ lệ Bạo Kích (Crit) và Né Tránh (Miss)!
