# Chương 9: Giao diện UI Nâng cao (9-Patch & Scissor)

Khi phát triển game, hệ thống UI (Bảng cài đặt, Túi đồ, Hộp thoại NPC) thường ngốn nhiều thời gian code hơn cả gameplay chính. Nếu chỉ dùng `DrawTexture` thông thường, bạn sẽ gặp 2 vấn đề lớn:
1. Khi kéo giãn bảng UI cho chữ dài ra, 4 góc viền của bảng bị méo xệch.
2. Danh sách vật phẩm dài thò ra ngoài khung nền.

Chương này sẽ cung cấp 2 vũ khí tối thượng của Raylib để giải quyết triệt để vấn đề trên.

---

## 1. Vẽ UI chuẩn tỷ lệ: 9-Patch (NPatch)

9-Patch là kỹ thuật cắt một bức ảnh UI vuông (ví dụ: khung thoại bo góc) thành 9 mảng caro (như trò chơi Tic-Tac-Toe). 
* **4 góc** sẽ được giữ nguyên không bao giờ bị phóng to.
* **4 cạnh viền** sẽ chỉ bị kéo giãn theo 1 chiều ngang hoặc dọc.
* **Vùng ở giữa** sẽ được kéo dãn thoải mái.

Kết quả? Bạn có thể lấy một ảnh khung thoại kích thước 50x50 để vẽ thành một bảng cài đặt khổng lồ 500x300 mà các góc bo tròn vẫn sắc nét, không hề bị biến dạng!

### Cách sử dụng
* **`DrawTextureNPatch(texture: Texture2D, nPatchInfo: NPatchInfo, dest: Rectangle, origin: Vector2, rotation: f32, tint: Color)`**

Trước tiên bạn phải định nghĩa struct `NPatchInfo`:

```odin
// Khai báo cấu trúc lưới cắt (Thường làm 1 lần lúc nạp ảnh)
npatch_info := rl.NPatchInfo {
    source = rl.Rectangle{0, 0, f32(ui_tex.width), f32(ui_tex.height)}, // Lấy cả ảnh
    left   = 16, // Khoảng cách từ lề trái đến đường cắt dọc 1 (pixel)
    top    = 16, // Lề trên đến cắt ngang 1
    right  = 16, // Lề phải đến cắt dọc 2
    bottom = 16, // Lề dưới đến cắt ngang 2
    layout = .NINE_PATCH // Loại lưới 9 ô
}

// Bên trong vòng lặp Draw
// Vẽ một bảng thoại khổng lồ 400x200
dest_rec := rl.Rectangle{100, 100, 400, 200}
rl.DrawTextureNPatch(ui_tex, npatch_info, dest_rec, {0,0}, 0.0, rl.WHITE)
```

---

## 2. Kỹ thuật "Cắt xén" (Scissor Mode)

Khi làm Túi đồ (Inventory) chứa hàng chục món đồ, bạn sẽ phải làm **Thanh cuộn (Scroll View)**. 
Nếu chỉ đơn giản là đổi tọa độ Y của các món đồ khi cuộn chuột, chúng sẽ trượt ra ngoài nền của túi đồ và bay lơ lửng trên màn hình game.

Thuật toán giải quyết: Dùng "Kéo" (Scissor) để cắt bỏ mọi thứ vẽ bên ngoài vùng chữ nhật của túi đồ!

### Cách sử dụng
* **`BeginScissorMode(x, y, width, height: c.int)`**
* **`EndScissorMode()`**

Mọi lệnh Draw nằm giữa 2 hàm này, nếu toạ độ vẽ rơi ra ngoài vùng `(x, y, width, height)`, GPU sẽ thẳng tay loại bỏ, không thèm vẽ nó ra màn hình.

```odin
inventory_panel := rl.Rectangle{200, 100, 400, 500}

// Vẽ nền của túi đồ (Có thể dùng 9-Patch)
rl.DrawRectangleRec(inventory_panel, rl.DARKGRAY)

// --- BẬT CHẾ ĐỘ CẮT XÉN ---
rl.BeginScissorMode(
    c.int(inventory_panel.x), 
    c.int(inventory_panel.y), 
    c.int(inventory_panel.width), 
    c.int(inventory_panel.height)
)
    
    // Vẽ hàng trăm vật phẩm bên trong
    // Giả sử scroll_Y là biến cuộn chuột
    for i in 0..<50 {
        item_y := 120 + (i * 60) + scroll_Y
        
        // Vẽ icon vật phẩm. 
        // Đừng lo nếu item_y nằm tít dưới đáy màn hình, ScissorMode sẽ tự động "cắt" phần thừa!
        rl.DrawRectangle(220, c.int(item_y), 50, 50, rl.RED)
    }

// --- TẮT CHẾ ĐỘ CẮT XÉN ---
rl.EndScissorMode()

// Giờ bạn có thể vẽ trỏ chuột UI đè lên trên mà không sợ bị cắt xén
```

---

## Tổng kết
Chỉ với 2 công cụ **9-Patch** và **Scissor Mode**, kết hợp với hàm tính toán chiều dài chữ `MeasureTextEx` ở Chương 4, bạn hoàn toàn có thể tự xây dựng một thư viện UI đồ sộ cho riêng mình trong Raylib mà không cần phụ thuộc vào các công cụ bên ngoài!
