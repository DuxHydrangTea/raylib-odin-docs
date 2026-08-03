# Dự Án Tốt Nghiệp: Sinh Tồn
## Phần 4: Thanh Máu, Lên Cấp (9-Patch) & State Machine

Game không thể chỉ bắn nhau mãi, người chơi phải có ĐIỂM KINH NGHIỆM, được chọn kỹ năng, có lúc CHẾT và trở về MENU.

*(Kỹ năng áp dụng: Chương 9, Chương 10)*

---

### 1. Kiến trúc Máy Trạng Thái (State Machine)

Cấu trúc lại hàm `main()` để game có Menu đàng hoàng.

```odin
GameState :: enum { MENU, PLAYING, LEVEL_UP, GAME_OVER }
current_state := GameState.MENU

// Game Loop
for !rl.WindowShouldClose() {
    // A. UPDATE LOGIC
    switch current_state {
        case .MENU:
            if rl.IsKeyPressed(.ENTER) {
                reset_game() // Hồi máu, xóa quái, xóa đạn
                current_state = .PLAYING
            }
        case .PLAYING:
            // Update Player, Enemies, Bullets...
            if player_xp >= xp_to_next_level { current_state = .LEVEL_UP }
            if player_hp <= 0 { current_state = .GAME_OVER }
        case .LEVEL_UP:
            if rl.IsKeyPressed(.ONE) { /* Nâng cấp Đạn */ current_state = .PLAYING }
        case .GAME_OVER:
            if rl.IsKeyPressed(.ENTER) { current_state = .MENU }
    }

    // B. DRAW
    rl.BeginDrawing()
        rl.ClearBackground(rl.BLACK)
        // ... switch tương tự để Draw
    rl.EndDrawing()
}
```

### 2. Giao diện 9-Patch UI (Bảng Nâng Cấp)

Khi State là `.LEVEL_UP`, game sẽ dừng thời gian (không gọi `update_enemies`). Lúc này, hiện ra một bảng chọn kỹ năng thật đẹp không bị móp méo các góc.

```odin
// Khai báo lúc đầu (Chương 9)
ui_panel_tex := rl.LoadTexture("assets/panel.png")
npatch := rl.NPatchInfo {
    source = {0, 0, f32(ui_panel_tex.width), f32(ui_panel_tex.height)},
    left = 16, top = 16, right = 16, bottom = 16,
    layout = .NINE_PATCH
}

// Bên trong Draw -> case .LEVEL_UP:
// Vẽ nền tối phủ mờ toàn bộ màn hình
rl.DrawRectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, rl.Color{0, 0, 0, 150})

// Vẽ bảng 9-Patch to đùng ở giữa màn hình
panel_rect := rl.Rectangle{WINDOW_WIDTH/2 - 200, WINDOW_HEIGHT/2 - 250, 400, 500}
rl.DrawTextureNPatch(ui_panel_tex, npatch, panel_rect, {0,0}, 0.0, rl.WHITE)

// Ghi chữ lên bảng
rl.DrawText("LÊN CẤP!", i32(panel_rect.x + 100), i32(panel_rect.y + 40), 40, rl.GOLD)
rl.DrawText("[1] Tăng tốc độ bắn", i32(panel_rect.x + 50), i32(panel_rect.y + 150), 20, rl.WHITE)
```

### 3. Vẽ Thanh Máu (HP Bar) và Thanh XP

Không cần 9-Patch, chỉ cần xếp chồng 2 `DrawRectangle` lên nhau ngoài Camera (Cố định vào UI màn hình).

```odin
// Thanh Máu
hp_ratio := player_hp / max_hp
bar_width: i32 = 300

// Đáy đỏ thẫm
rl.DrawRectangle(20, 20, bar_width, 25, rl.MAROON)
// Lõi đỏ tươi
rl.DrawRectangle(20, 20, i32(f32(bar_width) * hp_ratio), 25, rl.RED)

// Viền trắng
rl.DrawRectangleLines(20, 20, bar_width, 25, rl.WHITE)
```

**Thành quả:** Bây giờ game của bạn đã có một vòng lặp Gameplay Loop chuẩn chỉnh của một tựa game Roguelite thực sự. Đánh quái -> Lên cấp -> Nâng sức mạnh -> Quái mạnh hơn -> Chết -> Menu!
