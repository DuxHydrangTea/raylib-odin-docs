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
Tạo thêm một Enum cho Công cụ người chơi đang cầm. Đồng thời, thay vì hardcode việc công cụ nào tương tác với đất nào (ví dụ Cuốc thì đổi đất 0 thành 1), ta tạo một Bảng Quy Tắc (Data-Driven Rules) để dễ dàng thêm công cụ mới.

```odin
EquipTool :: enum { HAND, HOE, WATERING_CAN }
current_tool: EquipTool = .HOE // Tạm hardcode để test

// Quy tắc tương tác đất đai
ToolRule :: struct {
    req_tile: int,  // Yêu cầu ID đất đầu vào
    res_tile: int,  // Biến thành ID đất đầu ra
}

// Bảng từ điển quy luật
tool_rules: map[EquipTool]ToolRule

// Khởi tạo quy luật (gọi trong hàm main hoặc init)
init_tool_rules :: proc() {
    tool_rules[.HOE] = {0, 1}           // Cuốc: Cỏ (0) -> Đất tơi (1)
    tool_rules[.WATERING_CAN] = {1, 2}  // Bình tưới: Đất tơi (1) -> Đất ướt (2)
}
```

Hệ thống xử lý nút `Space` sẽ tra cứu quy tắc này để can thiệp vào `map_data`.

```odin
farming_interaction_system :: proc(world: ^World) {
    if rl.IsKeyPressed(.SPACE) {
        for i := 0; i < world.next_entity_id; i += 1 {
            if world.mask_player[i] {
                pos := world.positions[i]
                mov := world.movements[i]
                
                tx, ty := get_facing_tile(pos, mov)
                if tx < 0 || tx >= MAP_WIDTH || ty < 0 || ty >= MAP_HEIGHT do return
                
                tile_id := map_data[ty][tx] // Chú ý: map_data[Y][X] vì khai báo [Row][Col]
                
                // Tra cứu quy luật dựa trên công cụ đang cầm
                if rule, ok := tool_rules[current_tool]; ok {
                    // Nếu điều kiện ô đất khớp với luật
                    if tile_id == rule.req_tile {
                        map_data[ty][tx] = rule.res_tile // Đổi loại đất!
                        fmt.println("Tương tác thành công!")
                    }
                }
            }
        }
    }
}
```
*(Lưu ý: Đừng quên gọi hàm `init_tool_rules()` ở đầu hàm `main()` nhé)*

## 4. Tích hợp và Đổi màu vẽ
Sửa đoạn code Render bản đồ ở hàm `main()` (Bài 2) để hỗ trợ vẽ thêm Đất Ướt (2):

```odin
// ... Cập nhật mảng tile_textures (Thêm hỗ trợ đất ướt)
tile_textures := [4]TextureID{ .GRASS, .DIRT, .WATERED_DIRT, .WATERED_DIRT } // ID 3 dành cho Đất đang trồng cây ở bài sau

// ... Vòng lặp vẽ vẫn giữ nguyên 1 dòng cực kỳ ngắn gọn!
rl.DrawTexture(textures[tile_textures[tile_id]], px, py, rl.WHITE)
```

Đừng quên thêm lệnh gọi `farming_interaction_system(&game_world)` vào Game Loop, nằm dưới phần gọi `player_input_system`.

**Test thử:**
- Bấm phím số `1` để đổi cuốc, bấm phím số `2` để đổi bình tưới (Tự gán thêm bằng lệnh `if rl.IsKeyPressed(.ONE) do current_tool = .HOE`).
- Chạy tới thảm cỏ màu xanh lá, quay mặt vào nó, bấm Space. Biến thành đất nâu!
- Đổi sang bình tưới, bấm Space lên đất màu nâu. Biến thành nâu sẫm!

Đã sẵn sàng để gieo hạt ở Bài 6!
