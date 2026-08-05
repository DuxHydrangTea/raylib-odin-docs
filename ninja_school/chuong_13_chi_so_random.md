# Chương 13: Sinh Chỉ Số Trang Bị (Random Stats)

Trong NSO, khi bạn đánh chết tinh anh hoặc Boss tà thú, vũ khí rớt ra sẽ có các chỉ số ngẫu nhiên (Ví dụ: Kiếm Gỗ Trắng thì cùi, nhưng Kiếm Gỗ Tím thì cộng rất nhiều Sát thương và Máu).

Kỹ thuật này được gọi là **Procedural Item Generation** (Sinh vật phẩm theo thuật toán).

---

## 1. Phân Cấp Độ Hiếm (Rarity)

Mở `ecs/items.odin` và bổ sung Enum `Rarity`.

```odin
Rarity :: enum {
    Common,   // Trắng (Bình thường)
    Uncommon, // Lục (Khá)
    Rare,     // Lam (Hiếm)
    Epic,     // Tím (Hoàn Mỹ)
}

// Cập nhật lại struct Item
Item :: struct {
    id:          int,
    type:        ItemType,
    name:        string,
    rarity:      Rarity, // Cấp độ hiếm
    equip_slot:  EquipSlot,
    upgrade_lvl: int,
    quantity:    int, 
    max_stack:   int,
    bonus_damage: int,
    bonus_hp:     int,
}
```

## 2. Bảng Dữ Liệu Vũ Khí Gốc (Base Item Table)

Giống hệt hệ thống 6 Môn Phái ở Chương 5, ta cần một Bảng tra cứu cho tất cả vật phẩm Tĩnh (Base). Sau đó ta sẽ "Clone" món đồ từ bảng này ra và tẩm thêm "Gia vị ngẫu nhiên".

```odin
// Dữ liệu Gốc (Không bao giờ thay đổi)
BaseItem :: struct {
    name:         string,
    type:         ItemType,
    equip_slot:   EquipSlot,
    base_damage:  int,
    base_hp:      int,
}

g_item_db: map[int]BaseItem = {
    100 = {name = "Kiem Go", type = .Equipment, equip_slot = .Weapon, base_damage = 10, base_hp = 0},
    101 = {name = "Ao Vai", type = .Equipment, equip_slot = .Armor, base_damage = 0, base_hp = 50},
    // ...
}
```

## 3. Hàm Rớt Đồ Ngẫu Nhiên (Drop Item)

Viết hàm `generate_random_equipment` để Boss gọi khi nó chết:

```odin
import rl "vendor:raylib"
import "core:fmt"

// Lấy 1 món đồ từ DB, random độ hiếm và nhân phẩm chỉ số!
generate_random_equipment :: proc(item_id: int) -> Item {
    base := g_item_db[item_id]
    
    // 1. Roll Độ hiếm (Gacha)
    roll := rl.GetRandomValue(1, 100)
    rarity: Rarity
    stat_multiplier: f32 = 1.0
    prefix := ""
    
    if roll <= 50 {         // 50% ra Trắng
        rarity = .Common
        stat_multiplier = 1.0
    } else if roll <= 80 {  // 30% ra Lục
        rarity = .Uncommon
        stat_multiplier = 1.2
        prefix = "[Luc] "
    } else if roll <= 95 {  // 15% ra Lam
        rarity = .Rare
        stat_multiplier = 1.5
        prefix = "[Lam] "
    } else {                // 5% ra Tím
        rarity = .Epic
        stat_multiplier = 2.0
        prefix = "[Tim] "
    }
    
    // 2. Tính toán chỉ số cuối cùng
    // Ta cho dao động ngẫu nhiên +- 10% quanh mức nhân phẩm (stat_multiplier)
    variance := rl.GetRandomValue(90, 110) // 90% đến 110%
    final_mult := stat_multiplier * f32(variance) / 100.0
    
    final_dmg := int(f32(base.base_damage) * final_mult)
    final_hp  := int(f32(base.base_hp) * final_mult)
    
    // Lưu ý: Chuỗi tên cần được cấp phát cẩn thận bằng Allocator
    full_name := fmt.tprintf("%s%s", prefix, base.name)
    
    // 3. Trả về Vật phẩm ĐỘC NHẤT
    return Item{
        id = item_id,
        type = base.type,
        name = full_name,
        rarity = rarity,
        equip_slot = base.equip_slot,
        upgrade_lvl = 0,
        quantity = 1,
        bonus_damage = final_dmg,
        bonus_hp = final_hp,
    }
}
```

Mỗi lần chạy hàm này cho ID `100` (Kiếm gỗ), nó có thể trả ra `Kiếm Gỗ (Sát thương 10)` hoặc trúng Jackpot ra `[Tim] Kiếm Gỗ (Sát thương 22)`. Đây chính là động lực thôi thúc người chơi treo máy đánh quái cả ngày đêm! 

Chương 14, chúng ta sẽ mang thanh kiếm này đến gặp Kenshinto để Đập Đồ!
