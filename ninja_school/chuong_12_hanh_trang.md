# Chương 12: Kiến Trúc Túi Đồ & Vật Phẩm (Inventory System)

Tạm gác lại những trận chiến nảy lửa rợp trời ám khí, chúng ta sẽ bước vào **Phần 4: Trang bị & Đập đồ**. Đây là nơi tiêu tốn thời gian, tiền bạc và chất xám của người chơi MMO nhiều nhất.

Bước đầu tiên là phải thiết kế một cái "Hành trang" (Túi đồ) có giới hạn ô, có thể nhặt, vứt, và đeo trang bị lên người.

---

## 1. Định nghĩa Cấu Trúc Vật Phẩm (Item)

Vật phẩm trong NSO chia làm 3 loại chính:
1. **Trang bị (Equipment):** Quần, Áo, Vũ khí, Nhẫn... Có chỉ số, có Cấp độ cường hóa (+1 -> +16).
2. **Vật phẩm tiêu hao (Consumables):** Bình HP, Bình MP, Bánh mì... Dùng xong thì mất, có số lượng xếp chồng (Stackable).
3. **Vật liệu (Materials):** Đá nâng cấp, Ngọc rồng... Không dùng trực tiếp mà để thợ rèn xài, có số lượng.

Tạo một file mới `ecs/items.odin`:

```odin
package ecs

ItemType :: enum {
    Equipment,
    Consumable,
    Material,
}

EquipSlot :: enum {
    Weapon,
    Armor,
    Pants,
    Amulet, // Dây chuyền
    Ring,
    None, // Dành cho Bình máu/Đá (Không mặc lên người được)
}

Item :: struct {
    id:          int, // ID tĩnh trong Cơ sở dữ liệu (VD: 100 = Kiếm gỗ)
    type:        ItemType,
    name:        string,
    
    // Thuộc tính riêng của Trang bị
    equip_slot:  EquipSlot,
    upgrade_lvl: int, // Cấp đập đồ (+0 đến +16)
    
    // Thuộc tính của Vật phẩm xếp chồng
    quantity:    int, 
    max_stack:   int, // Số lượng tối đa 1 ô (VD: 99 bình máu/ô)
    
    // Chỉ số cộng thêm (Tạm gộp chung vào đây cho đơn giản)
    bonus_damage: int,
    bonus_hp:     int,
}
```

## 2. Component Hành Trang (Inventory)

Ninja của bạn sẽ mang trên người một cái Balo (Hành trang). Do đó, `Inventory` cũng là một Component gắn vào Entity!

Mở `ecs/components.odin`:

```odin
INVENTORY_SIZE :: 30 // Hành trang giới hạn 30 ô

InventoryComponent :: struct {
    // Mảng cố định 30 ô. Nếu ô nào có item.id == 0 nghĩa là ô đó Trống!
    slots: [INVENTORY_SIZE]Item, 
    
    // Đồ đang mặc trên người (Khác với Balo)
    // Tận dụng sức mạnh của Enum làm Key cho Map!
    equipped: map[EquipSlot]Item,
}

// Bảng dữ liệu
inventories: map[EntityID]InventoryComponent
```

> [!NOTE]
> Tại sao lại chia Hành trang thành mảng `slots: [30]` cố định thay vì dùng `[dynamic]` (Mảng co giãn)? 
> Trả lời: Game RPG rất khắt khe về vị trí của đồ vật. Bạn mở hành trang ra, để cái áo ở Ô số 12, thì lần sau mở ra nó vẫn phải ở Ô số 12. Dùng mảng cố định `[30]` giúp bạn map (ánh xạ) trực tiếp 30 phần tử này vào 30 ô vuông UI trên màn hình một cách chính xác tuyệt đối!

## 3. Hàm Thêm Vật Phẩm Vào Hành Trang

Bây giờ Ninja đánh chết con cóc, rớt ra 1 viên Đá Cấp 1, Ninja chạy qua nhặt. Ta phải code logic nhét viên Đá đó vào Balo. 

Mở `ecs/items.odin`:

```odin
// Trả về true nếu nhặt thành công, false nếu Hành trang ĐẦY!
add_item_to_inventory :: proc(player_id: EntityID, new_item: Item) -> bool {
    if player_id not_in inventories do return false
    
    inv := &inventories[player_id]
    
    // Bước 1: Nếu là đồ cộng dồn được (Ví dụ: Bình máu, Đá), tìm ô đang có sẵn để nhét thêm vào
    if new_item.type != .Equipment && new_item.max_stack > 1 {
        for i in 0..<INVENTORY_SIZE {
            if inv.slots[i].id == new_item.id {
                // Ô này đang chứa đồ giống hệt
                space_left := inv.slots[i].max_stack - inv.slots[i].quantity
                if space_left >= new_item.quantity {
                    // Đủ chỗ chứa tất cả
                    inv.slots[i].quantity += new_item.quantity
                    return true
                } else if space_left > 0 {
                    // Nhét đầy ô này, phần còn dư thì chạy tiếp vòng for tìm ô khác
                    inv.slots[i].quantity += space_left
                    new_item.quantity -= space_left // Ở dòng này biến truyền vào phải dạng pointer nhé
                }
            }
        }
    }
    
    // Bước 2: Tìm ô trống đầu tiên (Slot trống là slot có id == 0)
    for i in 0..<INVENTORY_SIZE {
        if inv.slots[i].id == 0 {
            inv.slots[i] = new_item // Nhét món đồ mới vào đây
            return true // Thành công!
        }
    }
    
    return false // Hành trang đầy!!
}
```

## 4. Hàm Mặc Đồ (Equip)

Khi người chơi bấm "Sử dụng" lên cái Kiếm Gỗ ở ô số 5, ta lấy cái kiếm đó đắp vào ô `.Weapon` trên người, đồng thời cộng dồn chỉ số của Kiếm vào máu/lực tay của Ninja.

```odin
equip_item :: proc(player_id: EntityID, slot_index: int) {
    inv := &inventories[player_id]
    item_to_equip := inv.slots[slot_index]
    
    // Chỉ trang bị mới mặc được
    if item_to_equip.type != .Equipment do return
    
    // Rút đồ ra khỏi balo (Gán id = 0 để xóa)
    inv.slots[slot_index] = Item{id = 0} 
    
    // 1. Nếu trên người ĐANG MẶC 1 món đồ cũ, phải tháo nó ra cất vào chỗ trống vừa nãy
    slot_type := item_to_equip.equip_slot
    if slot_type in inv.equipped {
        old_item := inv.equipped[slot_type]
        inv.slots[slot_index] = old_item // Cất đồ cũ vào đúng cái ô vừa lấy đồ mới ra (Swap)
        
        // Trừ chỉ số của đồ cũ khỏi Ninja
        stats[player_id].damage -= old_item.bonus_damage
        stats[player_id].max_hp -= old_item.bonus_hp
    }
    
    // 2. Mặc đồ mới lên người
    inv.equipped[slot_type] = item_to_equip
    
    // 3. Cộng chỉ số của đồ mới cho Ninja
    stats[player_id].damage += item_to_equip.bonus_damage
    stats[player_id].max_hp += item_to_equip.bonus_hp
}
```

Cấu trúc Hành trang này vừa chặt chẽ, vừa tối ưu O(1) khi truy xuất các ô lưới. Ở Chương 13, chúng ta sẽ biến tấu các dòng thuộc tính `bonus_damage` này thành **Tùy chọn Ngẫu nhiên (Random Stats)** để phân cấp đồ Trắng - Lục - Lam - Tím rớt ra từ Boss như một game Diablo thực thụ.
