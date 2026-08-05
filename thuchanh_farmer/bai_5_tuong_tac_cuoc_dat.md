# Bài 5: Tương Tác Cuốc Đất & Tưới Nước

Bây giờ bạn đã đi lại được, tới lúc tác động lên môi trường xung quanh. Ở bài này, ta sẽ vẽ một ô Highlight (nhấp nháy màu vàng) trước mặt nhân vật, và khi bấm Space, ta sẽ cuốc đất nếu đó là đất.

## 1. Tìm ô đất đang được chỉ vào (Facing)
Ta viết một hàm phụ trợ nhỏ trả về tọa độ (Grid) của ô đang nằm ngay trước mặt nhân vật, dựa theo hướng quay đầu (Facing).

```odin
get_facing_tile :: proc(pos: Position, mov: Movement) -> (int, int) {
    tx, ty := pos.grid_x, pos.grid_y
    switch mov.facing {
    case .UP:    ty -= 1
    case .DOWN:  ty += 1
    case .LEFT:  tx -= 1
    case .RIGHT: tx += 1
    case .NONE:  break
    }
    return tx, ty
}
```

## 2. Vẽ Highlight màu Vàng
Trong hàm `render_system()`, sau khi vẽ xong nhân vật, ta dùng hàm `get_facing_tile` để tính và vẽ một cái khung rỗng.

```odin
// Thêm vào cuối hàm render_system
for i := 0; i < world.next_entity_id; i += 1 {
    if world.mask_player[i] { // Tìm thấy người chơi
        pos := world.positions[i]
        mov := world.movements[i]
        
        tx, ty := get_facing_tile(pos, mov)
        
        // Vẽ ô vàng (Highlight) nếu nó nằm trong bản đồ
        if tx >= 0 && tx < MAP_WIDTH && ty >= 0 && ty < MAP_HEIGHT {
            px := f32(tx * TILE_SIZE)
            py := f32(ty * TILE_SIZE)
            rect := rl.Rectangle{px, py, f32(TILE_SIZE), f32(TILE_SIZE)}
            
            // Vẽ viền dày 3 pixel
            rl.DrawRectangleLinesEx(rect, 3.0, rl.YELLOW)
        }
    }
}
```

## 3. Hệ Thống Tương Tác Nông Trại (Farming System)
Tạo thêm một Enum cho Công cụ người chơi đang cầm. Giả sử ta đang cầm cái Cuốc.

```odin
EquipTool :: enum { HAND, HOE, WATERING_CAN }
current_tool: EquipTool = .HOE // Tạm hardcode để test
```

Hệ thống xử lý nút `Space` sẽ can thiệp trực tiếp vào mảng 2D `map_data`. (Ở Bài 2 ta đã quy định: `0` là cỏ, `1` là đất).
Ta thêm luật mới: `2` là đất đã tưới (Màu nâu đậm).

```odin
farming_interaction_system :: proc(world: ^World) {
    if rl.IsKeyPressed(.SPACE) {
        // Tìm player
        for i := 0; i < world.next_entity_id; i += 1 {
            if world.mask_player[i] {
                pos := world.positions[i]
                mov := world.movements[i]
                
                // Lấy tọa độ đích
                tx, ty := get_facing_tile(pos, mov)
                
                // Nếu vượt ra khỏi bản đồ thì bỏ qua
                if tx < 0 || tx >= MAP_WIDTH || ty < 0 || ty >= MAP_HEIGHT do return
                
                tile_id := map_data[ty][tx] // Chú ý: map_data[Y][X] vì khai báo [Row][Col]
                
                // Máy trạng thái (State Machine) của đất
                if current_tool == .HOE {
                    // Cuốc cỏ (0) thành Đất tơi xốp (1)
                    if tile_id == 0 {
                        map_data[ty][tx] = 1 
                        fmt.println("Da cuoc dat!")
                    }
                } else if current_tool == .WATERING_CAN {
                    // Tưới Đất tơi (1) thành Đất ướt (2)
                    if tile_id == 1 {
                        map_data[ty][tx] = 2
                        fmt.println("Da tuoi nuoc!")
                    }
                }
            }
        }
    }
}
```

## 4. Tích hợp và Đổi màu vẽ
Sửa đoạn code Render bản đồ ở hàm `main()` (Bài 2) để hỗ trợ vẽ thêm Đất Ướt (2):

```odin
// ... (Render Map vòng lặp Row Col) ...
if tile_id == 0 { 
    rl.DrawTexture(textures[.GRASS], px, py, rl.WHITE)
} else if tile_id == 1 { 
    rl.DrawTexture(textures[.DIRT], px, py, rl.WHITE)
} else if tile_id == 2 { // CẬP NHẬT MỚI: Đất Ướt
    rl.DrawTexture(textures[.WATERED_DIRT], px, py, rl.WHITE)
}
```

Đừng quên thêm lệnh gọi `farming_interaction_system(&game_world)` vào Game Loop, nằm dưới phần gọi `player_input_system`.

**Test thử:**
- Bấm phím số `1` để đổi cuốc, bấm phím số `2` để đổi bình tưới (Tự gán thêm bằng lệnh `if rl.IsKeyPressed(.ONE) do current_tool = .HOE`).
- Chạy tới thảm cỏ màu xanh lá, quay mặt vào nó, bấm Space. Biến thành đất nâu!
- Đổi sang bình tưới, bấm Space lên đất màu nâu. Biến thành nâu sẫm!

Đã sẵn sàng để gieo hạt ở Bài 6!
