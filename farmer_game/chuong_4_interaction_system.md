# Chương 4: Hệ Thống Tương Tác (Interaction System)

Trong Avatar 2D, khi nhân vật đi dạo quanh nông trại, sẽ luôn có một **Ô vuông nét đứt (Highlight Cursor)** xuất hiện ngay phía trước mặt nhân vật. Người chơi bấm nút (Phím Space hoặc Enter) để thao tác (Cuốc đất, Tưới nước, Nhổ củ cải) lên chính cái ô Highlight đó.

## 1. Tìm ô (Tile) trước mặt nhân vật

Dựa vào hướng mặt (Facing) của Component di chuyển (`MovementComponent`), ta dễ dàng tìm được tọa độ Grid phía trước.

```odin
package ecs

import rl "vendor:raylib"

get_facing_grid :: proc(pos: ^Position, mov: ^MovementComponent) -> (tx: int, ty: int) {
    tx, ty = pos.grid_x, pos.grid_y
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

## 2. Vẽ Highlight Cursor (Trải nghiệm người dùng)

Component này không ảnh hưởng vật lý, nó chỉ giúp người chơi biết họ chuẩn bị "Phá" nhầm luống cải của ai không.

```odin
// Trong system render
render_interaction_cursor :: proc(world: ^World, player_id: EntityID) {
    pos := &world.positions[player_id]
    mov := &world.movements[player_id]
    
    // Lấy ô trước mặt
    tx, ty := get_facing_grid(pos, mov)
    
    // Tính tọa độ pixel
    px := f32(tx * TILE_SIZE)
    py := f32(ty * TILE_SIZE)
    
    // Vẽ ô vuông màu vàng nhấp nháy hoặc nét đứt
    rect := rl.Rectangle{px, py, TILE_SIZE, TILE_SIZE}
    rl.DrawRectangleLinesEx(rect, 2.0, rl.YELLOW)
}
```

## 3. Hệ thống Gửi Lệnh (Command/Action System)

Khi người chơi bấm Phím Tương Tác, chúng ta **không nên** xử lý Logic Đất/Cây trồng trực tiếp ngay tại code Bắt phím (Input).

**Anti-pattern:**
```odin
if rl.IsKeyPressed(.SPACE) {
    if map[tx][ty] == DIRT {
        map[tx][ty] = PLOWED
    } else if map[tx][ty] == PLANT {
        harvest_plant(tx, ty)
    }
}
```
Làm như vậy code sẽ dài hàng ngàn dòng, cực kỳ rối rắm. Thêm vào đó, nếu làm Multiplayer, phím SPACE không gieo hạt ngay, mà phải bay lên Server trước.

**Kiến trúc đúng (Command Pattern / Event Queue):**
Nhân vật chỉ phát ra một "Yêu cầu (Request)" hoặc "Sự kiện (Event)".

```odin
// ecs/events.odin
package ecs

InteractEvent :: struct {
    entity_id: EntityID,
    target_grid_x: int,
    target_grid_y: int,
}

// Hàng đợi sự kiện
event_queue: [dynamic]InteractEvent
```

```odin
// Khi bắt phím (Input)
if rl.IsKeyPressed(.SPACE) {
    tx, ty := get_facing_grid(pos, mov)
    append(&event_queue, InteractEvent{ player_id, tx, ty })
}
```

Sau đó, một System chuyên biệt (Ví dụ: `FarmingSystem`) sẽ lặp qua hàng đợi `event_queue`, lấy công cụ người chơi đang cầm trên tay (Cuốc, Bình tưới, Hạt giống), đối chiếu với ô `tx, ty` xem có cuốc được không, nếu hợp lệ mới thực thi đổi trạng thái ô đất. Điều này tạo nền tảng cực tốt cho Chương 5!
