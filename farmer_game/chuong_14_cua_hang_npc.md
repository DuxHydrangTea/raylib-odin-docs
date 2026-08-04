# Chương 14: Cửa Hàng Nông Trại (NPC Lái Buôn)

Trồng lúa xong thì phải đem bán. Trong Avatar, khu trung tâm luôn có các NPC Lái buôn thu mua nông sản và bán hạt giống. Hệ thống Cửa hàng là nơi dòng tiền xu (Money Sink / Faucet) luân chuyển.

## 1. Dữ Liệu Cửa Hàng (Shop Config)

Tương tự hạt giống, các mặt hàng trong Shop phải được lưu ở file Data ngoài (JSON) để Game Designer dễ dàng cân bằng giá cả (Balancing) mà không cần can thiệp vào Source Code.

```odin
package core

ShopItem :: struct {
    item_id: int,
    item_type: ItemType,
    buy_price: int,    // Giá người chơi MUA TỪ NPC
    sell_price: int,   // Giá NPC THU MUA LẠI từ người chơi
}

// Danh sách các mặt hàng NPC đang bán
npc_shop_inventory: [dynamic]ShopItem
```

## 2. Giao Dịch Mua Hàng (Buy)

Khi người chơi ấn nút "Mua" 10 Hạt giống Cà chua. Logic phải cực kỳ cẩn trọng. Luôn kiểm tra Tiền TRƯỚC, và kiểm tra Chỗ Trống TRƯỚC khi thực hiện thay đổi.

**Anti-pattern:** Trừ tiền người chơi trước, sau đó phát hiện túi đồ họ đã đầy, thế là lỗi mất tiền oan.

```odin
buy_item_from_npc :: proc(inv: ^Inventory, shop_item: ShopItem, amount: int) -> bool {
    total_cost := shop_item.buy_price * amount
    
    // 1. Kiểm tra đủ tiền không
    if inv.money < total_cost {
        fmt.println("Lỗi: Không đủ tiền!")
        return false
    }
    
    // 2. Chạy thử hàm Add Item nhưng ở chế độ "Simulate" (Giả lập)
    // Để xem có đủ chỗ trống không.
    // Nếu bạn không có hàm simulate, thì làm bước 3:
    
    // 3. Thực hiện nhét đồ vào túi
    leftover := add_item(inv, shop_item.item_id, shop_item.item_type, amount)
    
    if leftover == amount {
        // Hoàn toàn không nhét được cái nào
        fmt.println("Lỗi: Túi đồ đã đầy!")
        return false
    }
    
    // Tính số lượng thực tế đã mua được (nếu túi bị đầy giữa chừng)
    actual_bought := amount - leftover
    actual_cost := actual_bought * shop_item.buy_price
    
    // 4. Trừ tiền CHÍNH XÁC
    inv.money -= actual_cost
    
    play_sound("cash_register.wav")
    return true
}
```

## 3. Giao Dịch Bán Hàng (Sell)

Người chơi muốn xả kho 50 quả Cà chua để lấy tiền nâng cấp đất.

```odin
sell_item_to_npc :: proc(inv: ^Inventory, slot_index: int, amount: int) {
    if slot_index < 0 || slot_index >= 30 do return
    
    slot := &inv.slots[slot_index]
    
    if slot.item_id == 0 || slot.quantity < amount {
        fmt.println("Lỗi: Không có vật phẩm để bán!")
        return
    }
    
    // Tra cứu giá bán của vật phẩm này từ Registry tổng
    price_per_unit := get_sell_price(slot.item_id)
    
    // 1. Xóa vật phẩm khỏi túi
    slot.quantity -= amount
    if slot.quantity <= 0 {
        slot.item_id = 0 // Dọn sạch ô nếu bán hết
    }
    
    // 2. Cộng tiền
    total_earned := price_per_unit * amount
    inv.money += total_earned
    
    play_sound("coins_drop.wav")
}
```

## 4. Quản Lý Dòng Tiền (Economy Balancing)
Trong một game nông trại có cày cuốc, Lạm phát (Inflation) là thứ đáng sợ nhất.
- Hạt giống mua `50 Xu`. 
- Cà chua thu hoạch bán được `100 Xu`. 
- Lợi nhuận `50 Xu` cho 2 tiếng chờ đợi.

Game cần tạo ra các **"Money Sinks" (Lỗ hổng hút tiền)** để người chơi có lý do tiêu tiền liên tục, tránh tiền đọng lại hàng tỷ Xu gây chán nản. Các Lỗ hổng này chính là: Mua đồ trang trí (Áo quần), Mua Phân bón ép xung thời gian, và đắt đỏ nhất: **Mua thêm Lô đất**. (Đón xem ở Chương 15).
