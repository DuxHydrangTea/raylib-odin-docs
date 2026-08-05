# Chương 13: Túi Đồ & Hành Trang (Inventory System)

Túi đồ là mạch máu của nền kinh tế trong mọi tựa game. Thiết kế Túi đồ sai, bạn sẽ gặp lỗi mất đồ, hoặc nghiêm trọng hơn là **Lỗi Nhân bản vật phẩm (Dupe Item)** khi chuyển sang Game Online.

## 1. Thiết Kế Cấu Trúc Túi Đồ Chống Lỗi

**Anti-pattern:** Dùng một mảng động `[dynamic]Item`.
```odin
// SAI LẦM:
inventory: [dynamic]Item 
append(&inventory, Item{"Hạt giống", 10})
// Nếu xóa phần tử ở giữa, các Index bị dồn lại, gây crash giao diện!
```

**Cách làm đúng (Slot-based / Mảng tĩnh):**
Túi đồ của người chơi thường có số ô cố định (Ví dụ: 30 ô). Mỗi ô (Slot) luôn tồn tại trong bộ nhớ, dù nó trống hay có đồ.

```odin
package core

ItemType :: enum { SEED, CROP, FERTILIZER, TOOL, ANIMAL_FOOD }

InventorySlot :: struct {
    item_id: int,     // 0 nghĩa là ô trống
    type: ItemType,
    quantity: int,
}

Inventory :: struct {
    slots: [30]InventorySlot,
    money: int, // Tiền xu gắn liền với Inventory
}
```

## 2. Thuật Toán Thêm Vật Phẩm (Add Item)

Khi bạn thu hoạch được 5 quả cà chua, hệ thống không chỉ nhét đại vào 1 ô. Nó phải ưu tiên **Cộng dồn (Stack)** vào ô đã có cà chua trước. Nếu ô đó đầy (ví dụ max stack = 99), nó mới tìm ô trống tiếp theo.

```odin
// Trả về số lượng item CÒN THỪA không thể thêm vào (do túi đầy)
add_item :: proc(inv: ^Inventory, item_id: int, type: ItemType, amount: int) -> int {
    remaining := amount
    MAX_STACK :: 99
    
    // Bước 1: Tìm ô đã có item này để cộng dồn
    for i := 0; i < 30; i += 1 {
        if inv.slots[i].item_id == item_id {
            space_left := MAX_STACK - inv.slots[i].quantity
            
            if space_left > 0 {
                add := min(remaining, space_left)
                inv.slots[i].quantity += add
                remaining -= add
                
                if remaining == 0 do return 0
            }
        }
    }
    
    // Bước 2: Tìm ô trống hoàn toàn để nhét phần còn thừa
    for i := 0; i < 30; i += 1 {
        if inv.slots[i].item_id == 0 { // Ô trống
            add := min(remaining, MAX_STACK)
            
            inv.slots[i].item_id = item_id
            inv.slots[i].type = type
            inv.slots[i].quantity = add
            
            remaining -= add
            if remaining == 0 do return 0
        }
    }
    
    // Không đủ chỗ chứa, rơi đồ ra đất hoặc báo lỗi
    return remaining 
}

// --- Helper Functions (Wrapper) ---
// Giúp các Event Handler từ các chương trước giao tiếp dễ dàng với Inventory
add_item_to_inventory :: proc(player_entity: EntityID, item_id: int, amount: int) {
    // Trong môi trường ECS thực tế:
    // inv := &world.inventories[player_entity]
    // add_item(inv, item_id, .CROP, amount)
}

remove_item_from_inventory :: proc(player_entity: EntityID, item_id: int, amount: int) {
    // Logic vòng lặp tìm slot có item_id rồi trừ đi quantity, tương tự add_item
}
// ----------------------------------
```

## 3. Tương tác Swap (Kéo Thả Đổi Chỗ)

Trên giao diện, người chơi thường xuyên kéo vật phẩm từ Ô số 1 sang Ô số 5 để sắp xếp cho đẹp.
Thao tác Swap này cực kì nhạy cảm.

```odin
swap_slots :: proc(inv: ^Inventory, from_idx: int, to_idx: int) {
    if from_idx < 0 || from_idx >= 30 || to_idx < 0 || to_idx >= 30 do return
    
    // Dùng biến tạm để hoán đổi (Atomic-like operation)
    temp := inv.slots[from_idx]
    inv.slots[from_idx] = inv.slots[to_idx]
    inv.slots[to_idx] = temp
    
    // Ghi chú: Nếu Game Online, logic này KHÔNG ĐƯỢC chạy ở Client. 
    // Client phải gửi Request lên Server, Server chạy hàm swap_slots này,
    // rồi phản hồi kết quả về Client. (Xem Chương 13 của phần Online).
}
```

**Bảo mật tài sản:**
Trong mọi tựa game, `Inventory` không bao giờ được gửi qua lại toàn bộ giữa Client và Server.
Server giữ file gốc. Khi người chơi đăng nhập, Server nén 30 ô này lại và gửi 1 lần duy nhất (Sync). Sau đó, mọi thao tác (Thu hoạch, Bán đồ) chỉ gửi những **Lệnh (Commands)** nhỏ bé như: `Bán ô số 5`. Server tự xử lý và báo về: `Ô số 5 giờ trống, tiền của mày tăng 1000 xu`. Khép kín và chống hack 100%.
