# Chương 9: Toán Học Sát Thương (Damage Math)

Một tựa game MMORPG như Ninja School không thể chỉ dùng công thức tính máu ngây thơ như `Máu - Lực tay` được. Trái tim giữ chân người chơi nạp tiền nâng cấp chính là các chỉ số ngẫu nhiên: Tỷ lệ Bạo kích (Critical), Sát thương Bạo Kích (Crit Damage), Tỷ lệ Né tránh (Evasion/Miss), và Phản đòn.

---

## 1. Nâng cấp StatsComponent

Mở `ecs/components.odin` và mở rộng `StatsComponent`. Chúng ta sẽ lưu các giá trị tỷ lệ dưới dạng Phần ngàn (0 - 1000) để không phải dùng số thực (Float). VD: Tỷ lệ 15.5% = `155`.

```odin
StatsComponent :: struct {
    hp, max_hp: int,
    mp, max_mp: int,
    
    // Tấn công
    damage: int,
    crit_rate: int, // Phần ngàn (0-1000). 100 = 10%
    crit_dmg:  int, // Phần trăm (%). Mặc định là 150%
    
    // Phòng thủ
    defense: int,
    miss_rate: int, // Tỷ lệ né tránh (Phần ngàn)
    
    speed: f32,
}
```

*(Lưu ý cập nhật lại các hàm `spawn_ninja` để điền giá trị mặc định cho các trường này).*

## 2. Hàm Tính Sát Thương Nâng Cao

Quay lại `ecs/entities.odin`, chúng ta sẽ đập bỏ hàm `apply_damage` cũ kỹ ở Chương 4 và thay bằng một thuật toán chuyên nghiệp.

```odin
import rl "vendor:raylib"

// Hàm trả về số nguyên ngẫu nhiên từ 1 đến 1000
random_1000 :: proc() -> int {
    return int(rl.GetRandomValue(1, 1000))
}

apply_advanced_damage :: proc(attacker_id: EntityID, victim_id: EntityID) {
    if attacker_id not_in stats do return
    if victim_id not_in stats do return
    
    attacker_stats := &stats[attacker_id]
    victim_stats   := &stats[victim_id]
    
    // 1. KIỂM TRA NÉ TRÁNH (Miss)
    // VD: Miss rate là 50 (5%). Nếu random ra số 20 <= 50 -> Né thành công!
    if random_1000() <= victim_stats.miss_rate {
        // TODO: Sinh ra chữ "Trượt" bay lên ở tọa độ của nạn nhân
        spawn_floating_text(victim_id, "Trượt!", rl.GRAY)
        return // Không tính sát thương nữa
    }
    
    // 2. KIỂM TRA BẠO KÍCH (Critical Hit)
    is_crit := false
    raw_dmg := attacker_stats.damage
    
    if random_1000() <= attacker_stats.crit_rate {
        is_crit = true
        // Sát thương x Crit_Dmg (%)
        raw_dmg = (raw_dmg * attacker_stats.crit_dmg) / 100
    }
    
    // 3. DAO ĐỘNG SÁT THƯƠNG (Variance 10%)
    // Lực tay không bao giờ là con số cố định. Ta cho dao động ngẫu nhiên +- 10%
    variance := raw_dmg / 10
    raw_dmg += int(rl.GetRandomValue(i32(-variance), i32(variance)))
    
    // 4. TRỪ PHÒNG THỦ (Armor Mitigation)
    actual_dmg := raw_dmg - victim_stats.defense
    if actual_dmg < 1 do actual_dmg = 1
    
    // 5. ÁP DỤNG MẤT MÁU
    victim_stats.hp -= actual_dmg
    
    // TODO: Sinh ra chữ số sát thương màu Đỏ (hoặc Vàng nếu là Chí mạng)
    if is_crit {
        spawn_floating_text(victim_id, fmt.tprintf("-%d!", actual_dmg), rl.YELLOW)
    } else {
        spawn_floating_text(victim_id, fmt.tprintf("-%d", actual_dmg), rl.RED)
    }
    
    // 6. KIỂM TRA TỬ VONG
    if victim_stats.hp <= 0 {
        victim_stats.hp = 0
        destroy_entity(victim_id)
    }
}
```

> [!TIP]
> Việc thiết kế Toán học sát thương là công đoạn tách rời hoàn toàn với Game Engine. Dù bạn làm trên Unity, Unreal hay Raylib Odin, công thức tính Crit và Miss này vẫn không thay đổi. Nếu game bị mất cân bằng (Player kêu ca Phái Cung quá mạnh), bạn chỉ cần điều chỉnh các chỉ số `crit_rate` thay vì phải đập đi xây lại Code.

Nhưng khoan đã, làm sao Hitbox vô danh (ở Chương 6, 7) biết được chủ nhân của nó là ai để lấy `crit_rate`? Rất đơn giản, ở phần tính va chạm của Đạn, thay vì lấy chỉ số của viên Đạn, hãy lấy chỉ số từ `owner_id` (Chủ nhân phóng ra viên đạn)!

Trong Chương 10, chúng ta sẽ cho Cóc Độc một kỹ năng mới: Gây Trúng Độc rút máu theo thời gian (DoT - Damage over Time).
