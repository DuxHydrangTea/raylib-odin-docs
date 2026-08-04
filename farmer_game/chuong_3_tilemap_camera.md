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
    GRASS = 0,
    DIRT = 1,
    FENCE = 2,
    WATER = 3,
}

GameMap :: struct {
    tiles: [MAP_HEIGHT][MAP_WIDTH]TileType,
    tileset: rl.Texture2D,
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

**Giải pháp (View Culling):** Chỉ vẽ những ô (Tiles) nằm lọt trong tầm nhìn của Camera.

```odin
render_map :: proc(game_map: ^GameMap, cam: ^rl.Camera2D, screen_w, screen_h: int) {
    // Tính toán góc trên bên trái và góc dưới bên phải của Camera trên hệ tọa độ Pixel
    top_left_x := cam.target.x - cam.offset.x
    top_left_y := cam.target.y - cam.offset.y
    
    // Chuyển từ hệ Pixel sang tọa độ Grid (ô)
    start_col := max(0, int(top_left_x) / TILE_SIZE)
    start_row := max(0, int(top_left_y) / TILE_SIZE)
    
    // Chừa hao thêm 1-2 ô để khi di chuyển không bị nhấp nháy mép
    end_col := min(MAP_WIDTH, start_col + (screen_w / TILE_SIZE) + 2)
    end_row := min(MAP_HEIGHT, start_row + (screen_h / TILE_SIZE) + 2)
    
    // Chỉ lặp qua vùng cắt được (Culling Rect)
    for row in start_row..<end_row {
        for col in start_col..<end_col {
            tile := game_map.tiles[row][col]
            
            // Vẽ tile dựa trên tileset
            source_rect := rl.Rectangle{ f32(tile) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE }
            dest_rect := rl.Rectangle{ f32(col * TILE_SIZE), f32(row * TILE_SIZE), TILE_SIZE, TILE_SIZE }
            
            rl.DrawTexturePro(game_map.tileset, source_rect, dest_rect, {0,0}, 0, rl.WHITE)
        }
    }
}
```

Với Culling, dù bản đồ có rộng `1000x1000`, mỗi khung hình bạn cũng chỉ vẽ tối đa `~400 ô`. Game sẽ luôn duy trì ở 60+ FPS ngay cả trên web (WASM).
