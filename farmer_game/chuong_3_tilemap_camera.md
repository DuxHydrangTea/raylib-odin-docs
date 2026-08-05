# Chương 3: Quản lý Tilemap và Camera trong Nông Trại

Bản đồ nông trại (như game Avatar) thường được xây dựng từ một tấm gạch (Tilemap) lớn. Gồm nhiều lớp (Layers): Lớp đất nền, Lớp trang trí (Cỏ, Rào), và Lớp Tương tác (Luống đất có thể trồng).

## 1. Dữ liệu Bản đồ (Map Data)

Tránh Anti-pattern: Đừng dùng biến toàn cục (Global Variable) `map_data[100][100]` rải rác khắp nơi. Hãy nhóm nó vào một Struct để sau này dễ dàng tải từ file (Ví dụ file `.tmj` xuất ra từ phần mềm Tiled).

```odin
package core

import rl "vendor:raylib"

MAP_WIDTH  :: 50
MAP_HEIGHT :: 50

TileType :: enum u8 {
    EMPTY = 0,   // Trống (Trong suốt)
    GRASS = 1,
    DIRT = 2,
    FENCE = 3,
    WATER = 4,
    TREE = 5,
}

GameMap :: struct {
    // Bản đồ Chuẩn 4 Lớp (Tạo chiều sâu cho Game 2D):
    // Lớp 0 (Ground): Nền đất dưới cùng (Cỏ, Đất tơi, Nước)
    // Lớp 1 (Decor): Trang trí nền không va chạm (Sỏi, viền cỏ, hoa)
    // Lớp 2 (Object): Vật cản (Hàng rào, Cây, Đá, Nhà)
    // Lớp 3 (Canopy): Mái che, tán lá (Sẽ được vẽ đè lên đầu nhân vật)
    tiles: [4][MAP_HEIGHT][MAP_WIDTH]TileType,
    tileset: rl.Texture2D,
}

// 2. Data-Driven: Bảng Dữ Liệu Đặc Tính (Tile Metadata)
// Giải quyết Anti-pattern: Không dùng "if tile == .WATER" hardcode trong logic.
TileProperties :: struct {
    is_walkable: bool,
}

// Bảng tra cứu (Lookup Table) được ánh xạ 1-1 với Enum TileType
TILE_DATA: [TileType]TileProperties = {
    .EMPTY = { is_walkable = true },
    .GRASS = { is_walkable = true },
    .DIRT  = { is_walkable = true },
    
    // Các vật cản
    .FENCE = { is_walkable = false },
    .WATER = { is_walkable = false },
    .TREE  = { is_walkable = false },
}

// Hàm kiểm tra Va chạm (Collision) cho Grid Movement
is_walkable :: proc(game_map: ^GameMap, grid_x, grid_y: int) -> bool {
    // 1. Chặn không cho đi ra ngoài bản đồ
    if grid_x < 0 || grid_x >= MAP_WIDTH || grid_y < 0 || grid_y >= MAP_HEIGHT {
        return false
    }
    
    // 2. Tra cứu cản trở ở các Lớp có khả năng va chạm (Lớp 0, 1, 2)
    // Ghi chú: Lớp 3 (Mái che) thường không cản đường nên không cần check
    tile_layer0 := game_map.tiles[0][grid_y][grid_x]
    tile_layer1 := game_map.tiles[1][grid_y][grid_x]
    tile_layer2 := game_map.tiles[2][grid_y][grid_x]
    
    // 3. Tra cứu thẳng vào Bảng dữ liệu (O(1) Cực nhanh)
    if !TILE_DATA[tile_layer0].is_walkable do return false
    if !TILE_DATA[tile_layer1].is_walkable do return false
    if !TILE_DATA[tile_layer2].is_walkable do return false
    
    return true
}
```

## 2. Hệ thống Camera theo dõi nhân vật (Camera Follow)

Camera trong Raylib 2D rất mạnh. Để Camera luôn bám theo nhân vật chính, nhưng KHÔNG ĐƯỢC trượt ra ngoài rìa màn hình (để lộ khoảng đen vô tận), chúng ta dùng kỹ thuật **Clamp** (Giới hạn).

```odin
package core

import rl "vendor:raylib"
import "core:math"
import "../ecs"

update_camera :: proc(cam: ^rl.Camera2D, player_pos: ^ecs.Position, screen_w, screen_h: int) {
    // 1. Gắn tâm camera vào giữa nhân vật
    cam.target = { player_pos.pixel_x, player_pos.pixel_y }
    cam.offset = { f32(screen_w) / 2.0, f32(screen_h) / 2.0 }
    
    // 2. Giới hạn không cho Camera lọt ra ngoài rìa bản đồ (Clamp)
    min_x := cam.offset.x
    max_x := f32(MAP_WIDTH * TILE_SIZE) - cam.offset.x
    
    min_y := cam.offset.y
    max_y := f32(MAP_HEIGHT * TILE_SIZE) - cam.offset.y
    
    // Ép giá trị target nằm trong vùng hợp lệ
    cam.target.x = math.clamp(cam.target.x, min_x, max_x)
    cam.target.y = math.clamp(cam.target.y, min_y, max_y)
}
```

## 3. Tối ưu Vẽ Bản đồ (Culling)

**Anti-pattern:** Dùng vòng lặp lồng nhau duyệt qua toàn bộ mảng `50x50` (2500 ô) và gọi lệnh `DrawTexture` mỗi frame. Dù ngoài màn hình cũng vẽ.
Điều này làm FPS tụt dốc không phanh.

**Giải pháp (View Culling):** Chỉ vẽ những ô (Tiles) nằm lọt trong tầm nhìn của Camera. Ngoài ra, ta phải chia việc vẽ bản đồ làm 2 đợt: Đợt 1 vẽ nền dưới chân nhân vật (Lớp 0,1,2). Đợt 2 vẽ tán cây/mái nhà đè lên đầu nhân vật (Lớp 3).

```odin
// Hàm render_map_layers nhận tham số start_layer và end_layer để tùy biến vẽ.
render_map_layers :: proc(game_map: ^GameMap, cam: ^rl.Camera2D, screen_w, screen_h: int, start_layer, end_layer: int) {
    // Tính toán góc trên bên trái của Camera
    top_left_x := cam.target.x - cam.offset.x
    top_left_y := cam.target.y - cam.offset.y
    
    start_col := max(0, int(top_left_x) / TILE_SIZE)
    start_row := max(0, int(top_left_y) / TILE_SIZE)
    // Chừa hao thêm 1-2 ô để khi di chuyển không bị nhấp nháy mép
    end_col := min(MAP_WIDTH, start_col + (screen_w / TILE_SIZE) + 2)
    end_row := min(MAP_HEIGHT, start_row + (screen_h / TILE_SIZE) + 2)
    
    // Lặp qua khoảng layer được yêu cầu
    for layer in start_layer..<end_layer { 
        for row in start_row..<end_row {
            for col in start_col..<end_col {
                tile := game_map.tiles[layer][row][col]
                
                // Bỏ qua tile trống
                if tile == .EMPTY do continue
                
                source_rect := rl.Rectangle{ f32(tile) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE }
                dest_rect := rl.Rectangle{ f32(col * TILE_SIZE), f32(row * TILE_SIZE), TILE_SIZE, TILE_SIZE }
                
                rl.DrawTexturePro(game_map.tileset, source_rect, dest_rect, {0,0}, 0, rl.WHITE)
            }
        }
    }
}

/* --- Cách lắp ráp thứ tự vẽ (Order of Drawing) vào Game Loop ---
rl.BeginDrawing()
    rl.ClearBackground(rl.BLACK)
    
    // 1. Vẽ Đất, Viền cỏ, Vật cản (Lớp 0, 1, 2)
    render_map_layers(&game_map, &camera, SCREEN_W, SCREEN_H, 0, 3)
    
    // 2. Vẽ Nhân vật và Thú cưng
    // (Bởi vì vẽ sau nên Nhân vật sẽ đi lên trên mặt đất và đè lên cỏ)
    render_player(&player)
    
    // 3. Vẽ Tán cây, Mái nhà (Lớp 3)
    // (Bởi vì vẽ cuối cùng, Tán cây sẽ che khuất nửa người nhân vật nếu nhân vật đi nấp sau cái cây)
    render_map_layers(&game_map, &camera, SCREEN_W, SCREEN_H, 3, 4)

rl.EndDrawing()
*/
```

Với Culling, dù bản đồ có rộng `1000x1000`, mỗi khung hình bạn cũng chỉ vẽ tối đa `~400 ô`. Kết hợp với Render 4 Lớp, game của bạn sẽ mang một vẻ đẹp 2.5D hệt như Stardew Valley.
