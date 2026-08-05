# Chương 10: Trạng Thái Dị Thường (Buff/Debuff)

Game nhập vai NSO cực kỳ nổi tiếng với các hiệu ứng Dị Thường. Phái Phong ném tiêu dính độc giật máu lách tách. Phái Băng làm quái vật bị đóng băng đứng im. Phái Hỏa gây bỏng. 

Thuật ngữ chuyên ngành làm game gọi hệ thống này là **Status Effects (Buffs/Debuffs)**.

---

## 1. Component Dị Thường

Một thực thể có thể bị dính nhiều loại độc, nhiều loại bỏng cùng một lúc. Do đó, Component này nên chứa mảng (Array) các hiệu ứng đang bám trên người.

Thêm vào `ecs/components.odin`:

```odin
StatusEffectType :: enum {
    Poison, // Trúng độc (Trừ máu mỗi giây)
    Freeze, // Đóng băng (Vận tốc = 0)
    Burn,   // Bỏng
    Haste,  // Buff: Chạy nhanh
}

StatusEffect :: struct {
    type: StatusEffectType,
    duration: f32, // Thời gian hiệu lực còn lại (giây)
    power: int,    // Sức mạnh của hiệu ứng (Ví dụ: Độc độc mất 50 HP/s)
}

StatusComponent :: struct {
    effects: [dynamic]StatusEffect,
}

// Bảng dữ liệu SoA
statuses: map[EntityID]StatusComponent
```

## 2. Gán Hiệu Ứng Lên Người Nạn Nhân

Trong hàm `apply_advanced_damage` ở Chương 9, ta thêm logic: Nếu Đòn đánh hoặc Kỹ năng mang thuộc tính gì, ta ném hiệu ứng tương ứng vào người nạn nhân.

```odin
// (Ví dụ) Nếu vũ khí là hệ Phong, có 20% gây Trúng Độc
add_status_effect :: proc(target_id: EntityID, type: StatusEffectType, duration: f32, power: int) {
    if target_id not_in statuses {
        // Nếu mục tiêu chưa có Component Status, thì tạo cho nó
        statuses[target_id] = StatusComponent{
            effects = make([dynamic]StatusEffect)
        }
    }
    
    // Ném cục hiệu ứng lên người nó
    comp := &statuses[target_id]
    append(&comp.effects, StatusEffect{type = type, duration = duration, power = power})
}
```

## 3. System Xử Lý Hiệu Ứng (Update Loop)

Mỗi Frame của game, ta phải duyệt qua tất cả những nạn nhân đang bị dính hiệu ứng, giảm thời gian `duration` của hiệu ứng đi. Nếu là Độc thì trừ máu, nếu là Băng thì khóa chân.

Tạo `system_status_effects` trong `ecs/systems.odin`:

```odin
system_status_effects :: proc(dt: f32) {
    for id in entities {
        if id not_in statuses do continue
        
        comp := &statuses[id]
        
        // 1. Phục hồi chỉ số gốc (Giả sử Quái vật vừa hết bị Đóng băng, nó phải đi lại được)
        // Chúng ta tạm reset Tốc độ về mức chuẩn. (Cách tốt nhất là thiết kế Base_Speed và Current_Speed riêng).
        if id in stats {
            // stats[id].speed = base_speed_of_this_monster
        }

        // 2. Lặp qua các cục hiệu ứng dính trên người
        i := 0
        for i < len(comp.effects) {
            effect := &comp.effects[i]
            effect.duration -= dt
            
            // XỬ LÝ LOGIC CỦA TỪNG LOẠI
            switch effect.type {
            case .Poison:
                // Rút máu (Giả sử rút `power` Máu mỗi giây. Dùng xác suất đơn giản)
                // dt thường là 0.016s. Ta có thể trừ trực tiếp hp -= power * dt (Dùng số Float)
                // Hoặc cứ 1 giây trừ 1 lần bằng Timer. Ở đây ta giả lập trừ thẳng:
                if id in stats {
                    // Mẹo: Dùng biến accumulator riêng để trừ máu nguyên (int)
                }
                
            case .Freeze:
                // Đóng băng: Tước đoạt hoàn toàn Vận tốc của nạn nhân!
                if id in velocities {
                    velocities[id].vel.x = 0
                }
                if id in ais {
                    ais[id].timer = 0.5 // Khóa mõm AI không cho cắn
                }
                
            case .Haste:
                // Buff Tốc chạy
                if id in stats {
                    stats[id].speed *= 1.5 // Chạy nhanh gấp rưỡi
                }
            }
            
            // Hết hạn thì lột hiệu ứng ra khỏi người
            if effect.duration <= 0 {
                unordered_remove(&comp.effects, i)
            } else {
                i += 1
            }
        }
    }
}
```

> [!WARNING]
> Việc sửa đổi trực tiếp (như nhân 1.5 Tốc độ, hoặc ép Vận tốc về 0) cực kỳ nguy hiểm, vì nếu làm không khéo nạn nhân sẽ vĩnh viễn không khôi phục lại tốc độ cũ khi hết Buff. Giải pháp chuyên nghiệp nhất là chia Stats ra làm 2 mảng: `BaseStats` (Chỉ số gốc, không bao giờ thay đổi) và `CurrentStats` (Chỉ số tạm tính). Mỗi đầu frame, ta gán `Current = Base`, sau đó System Status sẽ cộng trừ thẳng vào `Current`.

Ở Chương 11, ta sẽ làm hệ thống **Floating Text** (Chữ máu văng ra) để người chơi có thể thỏa mãn nhìn thấy những dòng chữ `-100`, `Trượt`, `Độc -5` nhảy nhót trên màn hình!
