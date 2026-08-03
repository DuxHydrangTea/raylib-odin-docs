# Chương 14: Bản đồ Tilemap và Tích hợp "Tiled"

Làm sao để vẽ một bản đồ rộng lớn (Platformer, RPG) mà không phải code tay tọa độ từng viên gạch? Kỹ thuật được sử dụng ở mọi game 2D chính là **Tilemap**.

Một Tilemap giống như 1 tấm lưới (Grid). Bạn có một bức ảnh chứa hàng trăm viên gạch (Tileset), và một ma trận số nguyên. Số `1` là gạch đất, `2` là cỏ, `0` là không khí.

---

## 1. Cơ bản về Tilemap

Dưới đây là một Tilemap tĩnh lưu thẳng vào code (Thường dùng cho game kiểu Bomberman hoặc Sokoban).

```odin
package game
import rl "vendor:raylib"

TILE_SIZE :: 32
MAP_COLS  :: 10
MAP_ROWS  :: 5

// 1 = Tường rắn, 0 = Lối đi
map_data := [MAP_ROWS][MAP_COLS]int{
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {1, 0, 0, 0, 1, 0, 0, 0, 0, 1},
    {1, 0, 1, 0, 1, 0, 1, 1, 0, 1},
    {1, 0, 0, 0, 0, 0, 0, 0, 0, 1},
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
}

draw_tilemap :: proc(tileset: rl.Texture2D) {
    for r in 0..<MAP_ROWS {
        for c in 0..<MAP_COLS {
            tile_id := map_data[r][c]
            
            if tile_id > 0 {
                // Tính toạ độ vẽ ra màn hình
                screen_x := c.int(c * TILE_SIZE)
                screen_y := c.int(r * TILE_SIZE)
                
                // Cắt ảnh viên gạch từ Tileset (Dùng DrawTextureRec)
                // (Giả sử tileset là dải gạch nằm ngang)
                source_rect := rl.Rectangle{f32((tile_id-1) * TILE_SIZE), 0, TILE_SIZE, TILE_SIZE}
                
                rl.DrawTextureRec(tileset, source_rect, {f32(screen_x), f32(screen_y)}, rl.WHITE)
            }
        }
    }
}
```

---

## 2. Kỹ thuật Culling (Vẽ tối ưu Camera)

Giả sử map của bạn là 10.000 x 10.000 ô (Terraria). Nếu bạn dùng 2 vòng lặp `for` duyệt 100 triệu ô gạch mỗi frame, game sẽ bị treo cứng.
**Culling** là kỹ thuật giải quyết: **"Chỉ vẽ những gì Camera nhìn thấy"**.

Bạn phải tính toán ô Bắt Đầu và ô Kết Thúc dựa vào tọa độ của Camera.

```odin
// (Ví dụ thuật toán Culling ngụy mã)
cam_x := camera.target.x - camera.offset.x
cam_y := camera.target.y - camera.offset.y

// Tìm cột/hàng ngoài cùng bên trái-trên mà camera chạm tới
start_col := max(0, int(cam_x / TILE_SIZE))
start_row := max(0, int(cam_y / TILE_SIZE))

// Tính số lượng ô gạch vừa đủ cho 1 màn hình
cols_per_screen := int(WINDOW_WIDTH / TILE_SIZE) + 2 // +2 dư ra để không bị khuyết góc khi di chuyển nửa ô
rows_per_screen := int(WINDOW_HEIGHT / TILE_SIZE) + 2

end_col := min(MAP_COLS, start_col + cols_per_screen)
end_row := min(MAP_ROWS, start_row + rows_per_screen)

// Giờ bạn chỉ cần lặp từ start_col đến end_col! (Rất ít)
for r in start_row..<end_row {
    for c in start_col..<end_col {
        // Vẽ gạch...
    }
}
```

---

## 3. Tích hợp phần mềm Tiled Map Editor

Thay vì tự gõ mảng số vào code, bạn hãy dùng phần mềm [Tiled](https://www.mapeditor.org/) (Miễn phí).
* Bạn thiết kế map bằng cách kéo thả hình ảnh.
* Xuất (Export) map đó ra đuôi `.json`.
* Dùng thư viện lõi của Odin là `core:encoding/json` để parse file JSON này vào Struct.
* Đọc mảng ma trận từ Struct đó và đổ vào hàm `draw_tilemap` ở trên.

Với Tiled, bạn có thể tạo nhiều Lớp (Layers) như: Lớp Nền (Background), Lớp Gạch Va chạm (Collision), và Lớp Quái vật để sinh quái vật vào đúng tọa độ định sẵn.
