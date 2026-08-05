# Chương 15: Luyện Đá & Ghép Ngọc

Để Đập đồ ở Chương 14, người chơi cần Đá Cường Hóa (Cấp 1 đến Cấp 10). Nếu đánh quái chỉ rớt ra Đá cấp 1, họ phải tốn tiền đi ghép 10 cục Đá cấp 1 thành 1 cục Đá cấp 2. Đây là một cơ chế "Hút Tiền" (Gold Sink) kinh điển của NSO để kiềm chế lạm phát trong game.

---

## 1. Cơ chế Vật Phẩm Xếp Chồng (Stackable)

Đá Cường Hóa là vật phẩm loại `.Material` (Nguyên liệu). Điểm khác biệt là chúng có thể xếp chồng (Stack) lên tới số lượng 99 trong cùng 1 ô Hành trang.

Giả sử `g_item_db` có khai báo:
```odin
    201 = {name = "Da Cuong Hoa Cap 1", type = .Material, max_stack = 99},
    202 = {name = "Da Cuong Hoa Cap 2", type = .Material, max_stack = 99},
```

## 2. Thuật toán Luyện Đá

Thuật toán ghép đá không phức tạp về mặt toán học sát thương, nhưng cực kỳ đau đầu về mặt **Quản lý Inventory**. Bạn phải xóa 10 cục đá nhỏ từ các ô khác nhau, và sinh ra 1 cục đá lớn.

Mở `ecs/items.odin`:

```odin
import rl "vendor:raylib"

// Hàm đếm và xóa số lượng vật phẩm bất kỳ trong Hành Trang
consume_item_quantity :: proc(player_id: EntityID, item_id: int, amount_needed: int) -> bool {
    inv := &inventories[player_id]
    amount_found := 0
    
    // Bước 1: Kiểm tra xem có đủ hàng không đã
    for i in 0..<INVENTORY_SIZE {
        if inv.slots[i].id == item_id {
            amount_found += inv.slots[i].quantity
        }
    }
    
    if amount_found < amount_needed do return false // Báo lỗi: Không đủ đá!
    
    // Bước 2: Đã đủ hàng, bắt đầu trừ (Xóa lùi)
    amount_to_remove := amount_needed
    for i in 0..<INVENTORY_SIZE {
        if inv.slots[i].id == item_id {
            if inv.slots[i].quantity >= amount_to_remove {
                // Ô này chứa đủ số cần xóa
                inv.slots[i].quantity -= amount_to_remove
                if inv.slots[i].quantity == 0 {
                    inv.slots[i].id = 0 // Biến ô này thành Ô trống
                }
                return true // Xóa xong!
            } else {
                // Ô này không đủ, xóa sạch ô này rồi trừ tiếp ở ô sau
                amount_to_remove -= inv.slots[i].quantity
                inv.slots[i].quantity = 0
                inv.slots[i].id = 0
            }
        }
    }
    
    return true
}

// Luyện 10 viên Đá Cấp N thành 1 viên Đá Cấp N+1
craft_upgrade_stone :: proc(player_id: EntityID, stone_lvl: int, player_yen: ^int) -> bool {
    // 1. Tính toán ID
    stone_id := 200 + stone_lvl       // Đá cấp 1 là 201
    next_stone_id := stone_id + 1     // Đá cấp 2 là 202
    
    cost := stone_lvl * 500 // Phí luyện đá
    if player_yen^ < cost do return false // Không đủ tiền
    
    // 2. Trừ 10 viên đá cấp thấp
    if consume_item_quantity(player_id, stone_id, 10) {
        
        // Trừ tiền
        player_yen^ -= cost
        
        // 3. Tỉ lệ thành công 100% (Hoặc có thể thêm xác suất thất bại mất đá ở đây)
        
        // 4. Bỏ 1 viên đá cấp cao vào hành trang
        new_stone := Item{
            id = next_stone_id,
            type = .Material,
            name = fmt.tprintf("Da Cuong Hoa Cap %d", stone_lvl + 1),
            quantity = 1,
            max_stack = 99,
        }
        
        add_item_to_inventory(player_id, new_stone)
        return true
    }
    
    return false
}
```

> [!NOTE]
> Hàm `consume_item_quantity` là một hàm cực kỳ quan trọng. Nó được dùng cho mọi hệ thống giao dịch trong game: Từ Luyện đá, Mua đồ Shop, Trả nhiệm vụ NPC, cho đến Trừ bình máu khi sử dụng. Đảm bảo hàm này không có Bug nhân đồ (Dupe Item) là bạn đã thành công 50% khi làm game MMO.

Vậy là toàn bộ Logic Backend cốt lõi của Ninja School đã hoàn thành. 3 Chương cuối cùng (16, 17, 18), chúng ta sẽ mặc áo cho game bằng Giao diện Người dùng (UI), Chuyển cảnh Bản đồ và ráp nối thành một File Source Code hoàn chỉnh!
