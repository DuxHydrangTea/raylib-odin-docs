# Bài 7: Kéo Thả Kho Đồ (Inventory) & Game Feel

Để thay thế việc dùng các phím số (1, 2, 3) để đổi công cụ khô khan, ta sẽ vẽ một thanh Kho đồ (Inventory) 5 ô ở dưới cùng màn hình. Người chơi có thể dùng Chuột kéo công cụ từ Kho thả vào ô Đất để thao tác.

## 1. Dữ liệu Kho Đồ (Inventory)
Khai báo kho đồ đơn giản với 5 ô, lưu trữ ID của Công cụ (`EquipTool` ở Bài 5).

```odin
INVENTORY_SIZE :: 5

InventorySlot :: struct {
    tool: EquipTool,
    amount: int,
}

inventory: [INVENTORY_SIZE]InventorySlot

// Khởi tạo đồ có sẵn
init_inventory :: proc() {
    inventory[0] = { .HOE, 1 }
    inventory[1] = { .WATERING_CAN, 1 }
    inventory[2] = { .SEED, 10 }
    inventory[3] = { .HAND, 1 } // Bàn tay trống
    inventory[4] = { .HAND, 0 } // Ô trống
}
```

## 2. Hệ Thống Drag & Drop (Kéo Thả Chuột)
Ta cần biết người chơi đang Kéo cái gì.

```odin
DragState :: struct {
    is_dragging: bool,
    slot_index: int, // Đang cầm từ ô số mấy
    tool_id: EquipTool,
}
drag_state: DragState
```

**Cập nhật Chuột (Mouse Update):**
Kiểm tra xem khi click chuột, tọa độ chuột có va chạm (Collision) với giao diện các ô vuông dưới màn hình không.

```odin
update_inventory_ui :: proc() {
    mouse_pos := rl.GetMousePosition()
    
    // Khởi tạo tọa độ gốc của thanh Inventory (Giữa màn hình, dưới đáy)
    start_x := f32(SCREEN_WIDTH/2 - (INVENTORY_SIZE*60)/2)
    start_y := f32(SCREEN_HEIGHT - 70)
    
    // 1. Nhấp Chuột (Kéo)
    if rl.IsMouseButtonPressed(.LEFT) && !drag_state.is_dragging {
        for i := 0; i < INVENTORY_SIZE; i += 1 {
            rect := rl.Rectangle{start_x + f32(i*60), start_y, 50, 50}
            if rl.CheckCollisionPointRec(mouse_pos, rect) {
                if inventory[i].tool != .HAND { // Chỉ kéo nếu có đồ
                    drag_state.is_dragging = true
                    drag_state.slot_index = i
                    drag_state.tool_id = inventory[i].tool
                }
            }
        }
    }
    
    // 2. Nhả Chuột (Thả)
    if rl.IsMouseButtonReleased(.LEFT) && drag_state.is_dragging {
        drag_state.is_dragging = false // Ngừng kéo
        
        // Chuyển tọa độ chuột trên màn hình thành tọa độ Grid (Lưới)
        grid_x := int(mouse_pos.x) / TILE_SIZE
        grid_y := int(mouse_pos.y) / TILE_SIZE
        
        // Gắn công cụ đang kéo làm Tool hiện tại và KÍCH HOẠT tương tác lên Grid
        // (Đoạn này ta gọi lại logic check Tile ở Bài 5 nhưng thay vì xét ô trước mặt nhân vật, ta xét ô ngay con trỏ chuột)
        execute_farming_tool_at(drag_state.tool_id, grid_x, grid_y) 
    }
}
```
*(Lưu ý: Bạn tách logic ở hàm `farming_interaction_system` Bài 5 ra thành hàm `execute_farming_tool_at(tool, tx, ty)` để tái sử dụng).*

## 3. Vẽ UI (Render Inventory)
Hàm này được gọi **CUỐI CÙNG** trong khối Render để đè lên mọi thứ.

```odin
render_inventory_ui :: proc() {
    start_x := i32(SCREEN_WIDTH/2 - (INVENTORY_SIZE*60)/2)
    start_y := i32(SCREEN_HEIGHT - 70)
    
    // Vẽ 5 ô vuông
    for i := 0; i < INVENTORY_SIZE; i += 1 {
        rl.DrawRectangle(start_x + i32(i*60), start_y, 50, 50, rl.LIGHTGRAY)
        rl.DrawRectangleLines(start_x + i32(i*60), start_y, 50, 50, rl.DARKGRAY)
        
        // Vẽ chữ thay cho Icon
        tool_name := "Trong"
        if inventory[i].tool == .HOE do tool_name = "Cuoc"
        if inventory[i].tool == .WATERING_CAN do tool_name = "Tuoi"
        if inventory[i].tool == .SEED do tool_name = "Hat"
        
        rl.DrawText(fmt.ctprintf("%s", tool_name), start_x + i32(i*60) + 5, start_y + 15, 10, rl.BLACK)
    }
    
    // Nếu đang Kéo (Drag), vẽ biểu tượng đang lơ lửng ngay con trỏ chuột
    if drag_state.is_dragging {
        mouse_pos := rl.GetMousePosition()
        rl.DrawRectangle(i32(mouse_pos.x - 25), i32(mouse_pos.y - 25), 50, 50, rl.Color{255, 255, 255, 120})
        rl.DrawText("Kéo...", i32(mouse_pos.x - 15), i32(mouse_pos.y - 5), 10, rl.BLACK)
    }
}
```

## 4. Game Feel (Hiệu Ứng Bụi - Particles)
Để kết thúc dự án một cách hoành tráng, mỗi khi cuốc đất trúng đích, ta văng lên một đống hột bụi.

```odin
// (Khai báo mảng Particle đơn giản)
Particle :: struct {
    x, y, vx, vy, life: f32
}
particles: [100]Particle

// Viết hàm Spawn Bụi
spawn_dust :: proc(px, py: f32) {
    import "core:math/rand"
    for i := 0; i < 100; i += 1 {
        if particles[i].life <= 0 { // Tìm hạt đã chết để tái sử dụng
            particles[i].x = px
            particles[i].y = py
            particles[i].vx = (rand.float32() - 0.5) * 200.0
            particles[i].vy = (rand.float32() - 0.5) * 200.0
            particles[i].life = 0.5 // Sống nửa giây
            break // Mỗi lần cuốc văng 1 hạt (bỏ vòng lặp để văng 1 chùm)
        }
    }
}

// Cập nhật và Vẽ
update_particles :: proc(dt: f32) {
    for i := 0; i < 100; i += 1 {
        if particles[i].life > 0 {
            particles[i].x += particles[i].vx * dt
            particles[i].y += particles[i].vy * dt
            particles[i].life -= dt
        }
    }
}
render_particles :: proc() {
    for i := 0; i < 100; i += 1 {
        if particles[i].life > 0 {
            rl.DrawCircle(i32(particles[i].x), i32(particles[i].y), 3.0, rl.BROWN)
        }
    }
}
```
Nhớ gọi `spawn_dust` vào trong đoạn code Cuốc Đất ở Bài 5 nhé!

---

**TỔNG KẾT KHÓA HỌC:**
Tuyệt vời! Bạn vừa tự tay xây dựng một Game Nông Trại bằng Raylib Odin từ 1 file trống không. Bắt đầu từ lưới Grid, sang Data-oriented ECS, tới Hệ thống Sinh trưởng bằng Thời gian, và UI kéo thả hệt như Game chuyên nghiệp.
Hãy tự tin tải thư mục này lên GitHub Portfolio của bạn! Mọi thắc mắc về Multiplayer hay Bug hãy quay về mục **Lỗi Game** và **K.T Online** trên trang chủ nhé. Cảm ơn bạn!
