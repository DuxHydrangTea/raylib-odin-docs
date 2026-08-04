# Chương 15: Hệ Thống Nâng Cấp Nông Trại (Progression)

Để người chơi có động lực cày cuốc (Grinding) liên tục từ ngày này qua tháng nọ, Nông trại khởi đầu của họ phải cực kỳ chật chội và nghèo nàn. Việc "Mở khóa ô đất mới" là phần thưởng vinh quang nhất đối với một nông dân ảo.

## 1. Dữ liệu Bản đồ Động (Dynamic Tilemap)

Ở Chương 3, mảng `tiles: [MAP_HEIGHT][MAP_WIDTH]TileType` của chúng ta là tĩnh. Bây giờ ta thêm khái niệm `LOCKED_PLOT` (Ô đất bị khóa) và `MAX_UNLOCK_LEVEL`.

```odin
package core

TileType :: enum u8 {
    GRASS = 0,
    DIRT = 1,
    FENCE = 2,
    LOCKED_PLOT = 3, // Hình một cái bảng gỗ cắm trên đất ghi "Bán"
}

FarmUpgradeConfig :: struct {
    plots_unlocked: int,  // Cấp 1 mở 10 ô, cấp 2 mở 15 ô...
    upgrade_cost: int,    // Cấp 2 tốn 10,000 Xu, Cấp 3 tốn 50,000 Xu
}
```

## 2. Nâng Cấp Mở Rộng Đất (Expand Farm)

Người chơi đi ra Khu ngoại ô (Town) gặp NPC "Trưởng Làng" để nộp tiền nâng cấp sổ đỏ.

```odin
upgrade_farm_size :: proc(player_id: EntityID, inv: ^Inventory) {
    player_data := &world.players[player_id]
    current_level := player_data.farm_level
    
    // Kiểm tra xem đã max level chưa
    if current_level >= MAX_FARM_LEVEL {
        fmt.println("Nông trại của bạn đã đạt cấp tối đa!")
        return
    }
    
    next_level_cfg := get_upgrade_config(current_level + 1)
    
    // Rút tiền từ túi (Áp dụng logic kiểm tra từ Chương 14)
    if inv.money < next_level_cfg.upgrade_cost {
        fmt.println("Thiếu tiền nâng cấp! Yêu cầu:", next_level_cfg.upgrade_cost)
        return
    }
    
    inv.money -= next_level_cfg.upgrade_cost
    player_data.farm_level += 1
    
    // Gửi Event hoặc gọi hàm mở khóa Đất trực tiếp
    unlock_new_plots(player_id, next_level_cfg.plots_unlocked)
    
    play_sound("fanfare_level_up.wav")
}
```

## 3. Thuật toán Mở Khóa Đất (Unlock Logic)

Làm sao Game biết ô đất nào sẽ được mở khóa?
Có hai cách thiết kế:
1. **Thiết kế Cứng (Pre-defined):** Trên file Tiled Map, bạn cắm sẵn 100 bảng gỗ. Và đánh số cho chúng từ 1 đến 100. Khi người chơi nâng cấp, bạn xóa bỏ bảng gỗ mang số thứ tự tương ứng.
2. **Thuật toán loang (Flood Fill):** Cực kỳ linh hoạt, ô nào nằm cạnh các ô đã mở khóa thì sẽ được ưu tiên mở dần ra ngoài viền.

Cách 1 (Pre-defined) dễ kiểm soát và được chuộng nhất:

```odin
unlock_new_plots :: proc(player_id: EntityID, total_plots_to_unlock: int) {
    // 1. Duyệt qua mảng bản đồ cá nhân của Player này (Nếu là Game Online, load từ DB)
    farm_map := get_player_farm_map(player_id)
    
    // Biến đếm số lượng đất đang mở
    current_unlocked := 0
    
    // 2. Chuyển đổi các Tile từ LOCKED_PLOT sang DIRT
    for r := 0; r < MAP_HEIGHT; r += 1 {
        for c := 0; c < MAP_WIDTH; c += 1 {
            if farm_map.tiles[r][c] == .DIRT {
                current_unlocked += 1
            }
        }
    }
    
    plots_needed := total_plots_to_unlock - current_unlocked
    
    if plots_needed > 0 {
        // Tìm các ô bị khóa và mở chúng (Theo thứ tự ưu tiên hoặc tọa độ)
        for r := 0; r < MAP_HEIGHT && plots_needed > 0; r += 1 {
            for c := 0; c < MAP_WIDTH && plots_needed > 0; c += 1 {
                if farm_map.tiles[r][c] == .LOCKED_PLOT {
                    farm_map.tiles[r][c] = .DIRT
                    
                    // Sinh ra Component FarmPlot (Chương 5) cho ô này để có thể trồng trọt
                    spawn_farm_plot_entity(c, r)
                    
                    plots_needed -= 1
                }
            }
        }
    }
}
```

Và thế là người chơi của chúng ta đã cạn kiệt tiền túi, tiếp tục quay lại chuỗi ngày cày cuốc, gieo hạt, bón phân để dành tiền cho đợt mở đất tiếp theo! Khái niệm Game Loop hoàn hảo khép lại. Mời bạn tiến tới **Phân hệ 5: Mạng Xã Hội Online!**
