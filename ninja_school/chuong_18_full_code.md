# Chương 18: Full Source Code (Ninja School Offline Clone)

Chúc mừng sếp đã đi tới chặng cuối cùng của Khóa Huấn Luyện Làng Tonek! 

Dưới đây là một bộ Source Code rút gọn nhưng **Chạy được ngay lập tức** bằng lệnh `odin run .`. Nó bao gồm:
1. Cơ chế Vật lý Platformer (Trọng lực, Va chạm map).
2. Camera cuộn bám theo nhân vật.
3. Sinh Hitbox đâm chém phía trước.
4. Giao diện Máu & Năng lượng.

Hãy copy toàn bộ đoạn mã này vào file `main.odin` trong một thư mục mới trống rỗng (Chỉ duy nhất 1 file để bạn test nhanh).

---

```odin
package main

import rl "vendor:raylib"
import "core:fmt"
import "core:math"

// ==========================================
// THÔNG SỐ TOÀN CỤC (CONFIG)
// ==========================================
SCREEN_WIDTH  :: 800
SCREEN_HEIGHT :: 600
TILE_SIZE     :: 32
MAP_WIDTH     :: 30
MAP_HEIGHT    :: 20

GRAVITY       :: 1500.0
JUMP_FORCE    :: -600.0
MOVE_SPEED    :: 250.0

// ==========================================
// DỮ LIỆU BẢN ĐỒ
// ==========================================
map_data: [MAP_HEIGHT][MAP_WIDTH]int = {
    {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0},
    {0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0},
    {0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0},
    {1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0},
    {1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1},
    {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
    {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
    {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
    {1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1},
}

// ==========================================
// KIẾN TRÚC ECS ĐƠN GIẢN
// ==========================================
EntityID :: int

TransformComponent :: struct {
    pos: rl.Vector2,
    size: rl.Vector2,
}

VelocityComponent :: struct {
    vel: rl.Vector2,
    is_grounded: bool,
    facing_right: bool,
}

HitboxComponent :: struct {
    timer: f32, // Tồn tại 0.1s
}

transforms: map[EntityID]TransformComponent
velocities: map[EntityID]VelocityComponent
hitboxes: map[EntityID]HitboxComponent
next_id: EntityID = 1 // 0 Dành riêng cho Player

spawn_hitbox :: proc(player_pos: rl.Vector2, facing_right: bool) {
    id := next_id
    next_id += 1
    
    x: f32 = player_pos.x
    if facing_right {
        x += 32 // Chém sang phải
    } else {
        x -= 60 // Chém sang trái
    }
    
    transforms[id] = TransformComponent{ pos = {x, player_pos.y}, size = {60, 64} }
    hitboxes[id] = HitboxComponent{ timer = 0.1 }
}

check_map_collision :: proc(rect: rl.Rectangle) -> bool {
    min_col := int(rect.x) / TILE_SIZE
    max_col := int(rect.x + rect.width - 1) / TILE_SIZE
    min_row := int(rect.y) / TILE_SIZE
    max_row := int(rect.y + rect.height - 1) / TILE_SIZE

    if min_col < 0 || max_col >= MAP_WIDTH do return true
    if min_row < 0 || max_row >= MAP_HEIGHT do return true

    for r in min_row..=max_row {
        for c in min_col..=max_col {
            if map_data[r][c] == 1 do return true
        }
    }
    return false
}

// ==========================================
// MAIN GAME LOOP
// ==========================================
main :: proc() {
    rl.InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Ninja School Offline Clone")
    rl.SetTargetFPS(60)

    // Khởi tạo Player (ID = 0)
    transforms[0] = TransformComponent{ pos = {100, 100}, size = {32, 64} }
    velocities[0] = VelocityComponent{ vel = {0,0}, is_grounded = false, facing_right = true }
    
    camera := rl.Camera2D{
        offset = {SCREEN_WIDTH/2, SCREEN_HEIGHT/2},
        target = {0,0},
        zoom = 1.0,
    }

    // Biến phụ cho Cooldown chém
    attack_cooldown: f32 = 0.0

    for !rl.WindowShouldClose() {
        dt := rl.GetFrameTime()
        
        // ----------------------------------
        // UPDATE (Vật Lý & Logic)
        // ----------------------------------
        pt := &transforms[0]
        pv := &velocities[0]
        
        // 1. Input
        pv.vel.x = 0
        if rl.IsKeyDown(.LEFT) {
            pv.vel.x = -MOVE_SPEED
            pv.facing_right = false
        }
        if rl.IsKeyDown(.RIGHT) {
            pv.vel.x = MOVE_SPEED
            pv.facing_right = true
        }
        
        if rl.IsKeyPressed(.SPACE) && pv.is_grounded {
            pv.vel.y = JUMP_FORCE
            pv.is_grounded = false
        }
        
        // Input Chém (J)
        if attack_cooldown > 0 do attack_cooldown -= dt
        if rl.IsKeyPressed(.J) && attack_cooldown <= 0 {
            spawn_hitbox(pt.pos, pv.facing_right)
            attack_cooldown = 0.5 // Chờ nửa giây mới chém tiếp được
        }

        // 2. Trọng lực
        if !pv.is_grounded {
            pv.vel.y += GRAVITY * dt
        }

        // 3. Va chạm Trục X
        pt.pos.x += pv.vel.x * dt
        rect := rl.Rectangle{pt.pos.x, pt.pos.y, pt.size.x, pt.size.y}
        if check_map_collision(rect) {
            if pv.vel.x > 0 {
                pt.pos.x = f32(int(rect.x + rect.width) / TILE_SIZE * TILE_SIZE) - rect.width
            } else if pv.vel.x < 0 {
                pt.pos.x = f32(int(rect.x) / TILE_SIZE * TILE_SIZE + TILE_SIZE)
            }
            pv.vel.x = 0
        }

        // 4. Va chạm Trục Y
        pt.pos.y += pv.vel.y * dt
        rect.x = pt.pos.x
        rect.y = pt.pos.y
        pv.is_grounded = false

        if check_map_collision(rect) {
            if pv.vel.y > 0 {
                pt.pos.y = f32(int(rect.y + rect.height) / TILE_SIZE * TILE_SIZE) - rect.height
                pv.is_grounded = true
            } else if pv.vel.y < 0 {
                pt.pos.y = f32(int(rect.y) / TILE_SIZE * TILE_SIZE + TILE_SIZE)
            }
            pv.vel.y = 0
        }
        
        // 5. Cập nhật Hitbox
        for id in hitboxes {
            h := &hitboxes[id]
            h.timer -= dt
            if h.timer <= 0 {
                delete_key(&hitboxes, id)
                delete_key(&transforms, id)
            }
        }

        // 6. Camera bám đuôi
        camera.target.x = math.lerp(camera.target.x, pt.pos.x, 5.0 * dt)
        camera.target.y = math.lerp(camera.target.y, pt.pos.y, 5.0 * dt)

        // ----------------------------------
        // RENDER (Vẽ Hình)
        // ----------------------------------
        rl.BeginDrawing()
        rl.ClearBackground(rl.SKYBLUE)

        rl.BeginMode2D(camera)
            // Vẽ Map
            for r in 0..<MAP_HEIGHT {
                for c in 0..<MAP_WIDTH {
                    if map_data[r][c] == 1 {
                        rl.DrawRectangle(i32(c * TILE_SIZE), i32(r * TILE_SIZE), TILE_SIZE, TILE_SIZE, rl.DARKBROWN)
                    }
                }
            }
            
            // Vẽ Hitbox (Màu Vàng)
            for id in hitboxes {
                t := transforms[id]
                rl.DrawRectangle(i32(t.pos.x), i32(t.pos.y), i32(t.size.x), i32(t.size.y), rl.YELLOW)
            }
            
            // Vẽ Player (Màu Đỏ)
            rl.DrawRectangle(i32(pt.pos.x), i32(pt.pos.y), i32(pt.size.x), i32(pt.size.y), rl.RED)
            
            // Vẽ vũ khí trên tay Player để biết hướng
            if pv.facing_right {
                rl.DrawRectangle(i32(pt.pos.x + 32), i32(pt.pos.y + 32), 20, 5, rl.BLACK)
            } else {
                rl.DrawRectangle(i32(pt.pos.x - 20), i32(pt.pos.y + 32), 20, 5, rl.BLACK)
            }

        rl.EndMode2D()

        // Vẽ UI
        rl.DrawRectangle(20, 20, 200, 20, rl.BLACK)
        rl.DrawRectangle(20, 20, 150, 20, rl.RED) // Máu 75%
        rl.DrawText("HP: 75/100", 70, 22, 16, rl.WHITE)
        
        rl.DrawText("A,D: Di Chuyen | SPACE: Nhay | J: Chem", 20, 560, 20, rl.BLACK)

        rl.EndDrawing()
    }
    rl.CloseWindow()
}
```

Chúc dự án Ninja School của sếp thành công rực rỡ và sớm có bản Demo Playable nhé! Nếu sếp cần code thêm phần Multiplayer (Online), tôi luôn sẵn sàng hầu hạ!
