# Chương 14: Thuật Toán Cường Hóa (Đập Đồ)

Nỗi ám ảnh kinh hoàng nhưng cũng đầy phấn khích của làng Tonek là Kenshinto và lò rèn của ông ta. Để cường hóa vũ khí từ +1 lên +16, bạn cần Đá cường hóa và Yên. Nếu xịt (thất bại), vũ khí sẽ bị rớt cấp!

---

## 1. Cấu Trúc Yêu Cầu Cường Hóa (Upgrade Config)

Ta lập một bảng tra cứu tỷ lệ thành công và nguyên liệu yêu cầu cho từng cấp độ từ +1 đến +16.

Tạo file `ecs/upgrade.odin`:

```odin
package ecs

import rl "vendor:raylib"

UpgradeRequirement :: struct {
    success_rate: int, // Phần ngàn (VD: 500 = 50%)
    cost: int,         // Lượng Yên (Tiền) cần thiết
    bonus_multiplier: f32, // Tỷ lệ cộng thêm sức mạnh nếu đập thành công
}

g_upgrade_table: [17]UpgradeRequirement = {
    1 = { success_rate = 1000, cost = 100,  bonus_multiplier = 1.1 },  // Lên +1: 100% thành công
    2 = { success_rate = 900,  cost = 200,  bonus_multiplier = 1.2 },  // Lên +2: 90%
    3 = { success_rate = 800,  cost = 300,  bonus_multiplier = 1.3 },  // Lên +3: 80%
    4 = { success_rate = 700,  cost = 500,  bonus_multiplier = 1.4 },  // Lên +4: 70% (Bắt đầu rớt cấp nếu xịt)
    // ... Cắt bớt cho ngắn ...
    16 = { success_rate = 50,  cost = 50000, bonus_multiplier = 3.0 }, // Lên +16: 5% (Tỉ lệ ảo ma)
}
```

## 2. Hàm Thực Thi Đập Đồ

Thuật toán đập đồ nhận vào 1 vật phẩm, nếu thành công thì tăng `upgrade_lvl` và tăng sức mạnh. Nếu xịt thì rớt cấp. Trả về kết quả cho Giao diện (UI) hiển thị "Ting Ting" hoặc "Xịt rồi".

```odin
UpgradeResult :: enum {
    Success,
    FailDropLevel, // Xịt rớt 1 cấp
    FailDropZero,  // Xịt rớt về +0 (Nếu đen)
    MaxLevel,      // Đã +16, không đập được nữa
}

// Truyền vào con trỏ (Pointer) của món đồ để sửa trực tiếp dữ liệu của nó
upgrade_equipment :: proc(item: ^Item, player_yen: ^int) -> UpgradeResult {
    if item.type != .Equipment do return .MaxLevel
    
    next_lvl := item.upgrade_lvl + 1
    if next_lvl > 16 do return .MaxLevel
    
    req := g_upgrade_table[next_lvl]
    
    // 1. Trừ tiền (Giả định luôn đủ tiền để test)
    player_yen^ -= req.cost
    
    // 2. Quay số nhân phẩm
    roll := rl.GetRandomValue(1, 1000)
    
    if roll <= i32(req.success_rate) {
        // =============== THÀNH CÔNG ===============
        item.upgrade_lvl = next_lvl
        
        // Tăng sức mạnh (Cập nhật lại tên hiển thị thành +1)
        item.bonus_damage = int(f32(item.bonus_damage) * req.bonus_multiplier)
        item.bonus_hp = int(f32(item.bonus_hp) * req.bonus_multiplier)
        
        return .Success
    } else {
        // =============== THẤT BẠI (XỊT) ===============
        // Cơ chế NSO: Nếu xịt từ +1 đến +3 thường giữ nguyên.
        // Xịt từ +4 đến +7 rớt 1 cấp. Xịt từ +8 trở lên rớt về +0 (nếu không có bùa).
        
        if next_lvl <= 3 {
            return .FailDropLevel // Coi như không rớt
        } else if next_lvl <= 7 {
            item.upgrade_lvl -= 1 // Rớt 1 cấp
            
            // Trừ lùi sức mạnh tương ứng (Cần tính toán kỹ hơn ở Game thực tế)
            item.bonus_damage = int(f32(item.bonus_damage) / req.bonus_multiplier) 
            return .FailDropLevel
        } else {
            // Rớt thẳng về +0
            item.upgrade_lvl = 0
            // Gọi lại dữ liệu base từ db để gán lại chỉ số gốc...
            return .FailDropZero
        }
    }
}
```

> [!CAUTION]
> Trong môi trường mạng (Online Game), **TOÀN BỘ thuật toán Đập Đồ phải được đặt ở Server**. Nếu bạn để Logic này ở Client, người chơi sẽ dùng phần mềm Cheat Engine hoặc Hack Mod để sửa `roll = 1` và đập 1 phát lên +16. Luôn nhớ: Không bao giờ tin tưởng Client!

Chương 15 tiếp theo, chúng ta sẽ làm nốt tính năng **Ghép Đá** (10 cục Đá cấp 1 -> 1 cục Đá cấp 2) với công thức tương tự.
