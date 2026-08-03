# Vấn Đề 10: Code Mì Ý (Spaghetti Code / State Management)

**Vấn đề:**
Khi game có thêm tính năng Tạm Dừng (Pause), bạn rải lệnh `if !is_paused` khắp 100 hàm khác nhau. Đến khi thêm màn hình Menu, Cửa hàng, Game Over... file `main` của bạn dài 5000 dòng đầy `if else` và rối như một tô mì Ý. Không dám sửa code vì sợ hỏng toàn cục.

**Nguyên nhân:**
Chưa sử dụng Máy Trạng Thái Hữu Hạn (Finite State Machine). Bạn xử lý luồng game dựa vào các biến boolean `is_playing`, `is_dead`, `is_paused` xếp chồng lên nhau.

**Giải pháp:**
Tạo một `enum` chứa TẤT CẢ các trạng thái game, và một cấu trúc dữ liệu `switch-case` sạch sẽ.
Khi ở trạng thái nào, chỉ gọi hàm Update/Draw của trạng thái đó. Các hàm này nên được tách riêng ra các file khác nhau.

```odin
GameState :: enum { MENU, PLAYING, PAUSED, SHOP, GAME_OVER }
current_state := GameState.MENU

for !rl.WindowShouldClose() {
    // UPDATE
    switch current_state {
        case .MENU:      update_menu(&current_state)
        case .PLAYING:   update_gameplay(&current_state)
        case .PAUSED:    update_paused(&current_state)
        case .SHOP:      update_shop(&current_state)
        case .GAME_OVER: update_game_over(&current_state)
    }
    
    // DRAW
    rl.BeginDrawing()
        rl.ClearBackground(rl.BLACK)
        switch current_state {
            case .MENU:      draw_menu()
            case .PLAYING:   draw_gameplay()
            case .PAUSED:    draw_gameplay(); draw_paused_overlay()
            // ...
        }
    rl.EndDrawing()
}
```
