# Bài 4: Grid-based Movement - Di Chuyển Từng Ô

Nếu bạn chỉ cộng `X += tốc độ`, nhân vật sẽ chạy xuyên qua các đường chỉ của Grid và trượt ra ngoài mép. Để di chuyển chuẩn phong cách Nông Trại, nhân vật phải bị "khóa" lại khi đang trượt từ tâm ô này sang tâm ô kế tiếp.

## 1. Mở Rộng Dữ Liệu
Thêm 1 Component di chuyển và 1 Enum định hướng.

```odin
// Khai báo Enum (Thêm vào phần đầu file)
Direction :: enum { DOWN, UP, LEFT, RIGHT, NONE }

// Component Di chuyển
Movement :: struct {
    is_moving: bool,
    target_x, target_y: int, // Ô lưới đích đến
    facing: Direction,
    speed: f32, // Số pixel đi được mỗi giây
}

// Cập nhật struct World
World :: struct {
    // ... các mảng cũ
    movements: [100]Movement,
    mask_movement: [100]bool,
}

// Cập nhật hàm create_player
create_player :: proc(world: ^World, start_grid_x: int, start_grid_y: int) {
    // ... code cũ
    
    // Thêm mask movement
    world.movements[id] = Movement {
        is_moving = false,
        facing = .DOWN,
        speed = 200.0, // Trượt 200 pixel / giây
    }
    world.mask_movement[id] = true
}
```

## 2. Hệ thống Nhận Phím (Input System)
Chỉ cho phép nhận phím khi nhân vật đang đứng im ở giữa một ô.

```odin
player_input_system :: proc(world: ^World) {
    for i := 0; i < world.next_entity_id; i += 1 {
        if world.mask_player[i] && world.mask_movement[i] {
            pos := &world.positions[i]
            mov := &world.movements[i]
            
            // Đang đi thì không cho nhận phím bẻ lái nửa chừng!
            if mov.is_moving do continue
            
            dx, dy := 0, 0
            if rl.IsKeyDown(.RIGHT) {
                dx = 1
                mov.facing = .RIGHT
            } else if rl.IsKeyDown(.LEFT) {
                dx = -1
                mov.facing = .LEFT
            } else if rl.IsKeyDown(.DOWN) {
                dy = 1
                mov.facing = .DOWN
            } else if rl.IsKeyDown(.UP) {
                dy = -1
                mov.facing = .UP
            }
            
            if dx != 0 || dy != 0 {
                // Kiểm tra biên giới bản đồ (Không cho đi ra ngoài mép)
                next_x := pos.grid_x + dx
                next_y := pos.grid_y + dy
                
                if next_x >= 0 && next_x < MAP_WIDTH && next_y >= 0 && next_y < MAP_HEIGHT {
                    // Chốt đơn đích đến, Khóa di chuyển
                    mov.target_x = next_x
                    mov.target_y = next_y
                    mov.is_moving = true
                }
            }
        }
    }
}
```

## 3. Hệ thống Trượt Pixel (Movement System)
Hệ thống này ép nhân vật trượt từ từ về hướng cái đích `target_x, y`.

```odin
movement_system :: proc(world: ^World, dt: f32) {
    for i := 0; i < world.next_entity_id; i += 1 {
        if world.mask_position[i] && world.mask_movement[i] {
            pos := &world.positions[i]
            mov := &world.movements[i]
            
            if mov.is_moving {
                // Tính tọa độ pixel của ô đích
                target_px := f32(mov.target_x * TILE_SIZE)
                target_py := f32(mov.target_y * TILE_SIZE)
                
                // Trượt theo trục X
                if pos.pixel_x < target_px {
                    pos.pixel_x += mov.speed * dt
                    if pos.pixel_x > target_px do pos.pixel_x = target_px // Chống đi lố
                } else if pos.pixel_x > target_px {
                    pos.pixel_x -= mov.speed * dt
                    if pos.pixel_x < target_px do pos.pixel_x = target_px
                }
                
                // Trượt theo trục Y
                if pos.pixel_y < target_py {
                    pos.pixel_y += mov.speed * dt
                    if pos.pixel_y > target_py do pos.pixel_y = target_py
                } else if pos.pixel_y > target_py {
                    pos.pixel_y -= mov.speed * dt
                    if pos.pixel_y < target_py do pos.pixel_y = target_py
                }
                
                // Nếu đã trượt đến chính xác tâm ô đích, Mở Khóa!
                if pos.pixel_x == target_px && pos.pixel_y == target_py {
                    pos.grid_x = mov.target_x
                    pos.grid_y = mov.target_y
                    mov.is_moving = false
                }
            }
        }
    }
}
```

## 4. Gắn vào Game Loop
```odin
main :: proc() {
    // ...
    for !rl.WindowShouldClose() {
        dt := rl.GetFrameTime()
        // ...
        case .PLAYING:
            // 1. Nhận Phím
            player_input_system(&game_world)
            // 2. Tính toán vật lý trượt
            movement_system(&game_world, dt)
            // ...
            // (Đoạn mã Render cũ bên dưới)
```

Chạy `odin run .` nào! Bấm mũi tên di chuyển, bạn sẽ thấy nhân vật không đi tự do mà nhảy lướt (glide) từng ô từng ô một rất ngay ngắn. Đây chính là "Game Feel" chuẩn mực của mọi game 2D nông trại (Kể cả Pokemon Red/Blue trên Gameboy ngày xưa cũng y hệt thế này).
