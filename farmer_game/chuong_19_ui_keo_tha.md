# Chương 19: Hệ Thống UI Kéo Thả (Drag & Drop)

Làm game Nông trại mà không có UI kéo thả phân bón từ túi đồ ra gieo lên ruộng thì vứt đi. 
Giao diện người dùng (UI) trong Raylib khá thô sơ (RayGUI), nên chúng ta sẽ tự viết cơ chế Kéo Thả (Drag & Drop) bằng Toán Học Hình Học cơ bản (AABB).

## 1. Trạng Thái Của Chuột (Mouse State)

Để làm Kéo thả, ta cần theo dõi 3 trạng thái của chuột:
1. Đang không cầm gì.
2. Vừa bấm chuột trái vào 1 vật phẩm (Bắt đầu kéo - Drag Start).
3. Đang giữ chuột và di chuyển (Đang kéo - Dragging).
4. Thả chuột trái (Kết thúc kéo - Drop).

```odin
package core

import rl "vendor:raylib"

DragState :: struct {
    is_dragging: bool,
    dragged_item_id: int, // Đang cầm hạt giống gì
    source_slot_index: int, // Cầm từ ô túi đồ số mấy
    offset_x, offset_y: f32, // Điểm lệch giữa con trỏ chuột và tâm hình
}

current_drag: DragState
```

## 2. Bắt Sự Kiện Bấm (Mouse Press)

Hàng khung hình, ta lặp qua giao diện Túi đồ (Inventory UI). Nếu chuột nằm đè lên 1 ô, và người chơi BẤM, ta bắt đầu hành trình.

```odin
update_ui_drag :: proc(inv: ^Inventory) {
    mouse_pos := rl.GetMousePosition()
    
    // 1. Kiểm tra Bắt đầu Kéo (Drag Start)
    if !current_drag.is_dragging && rl.IsMouseButtonPressed(.LEFT) {
        
        // Duyệt qua 30 ô túi đồ trên UI
        for i := 0; i < 30; i += 1 {
            slot_rect := get_slot_rect(i) // Hàm trả về tọa độ của ô thứ i trên màn hình
            
            // Nếu chuột đè lên ô và ô đó có đồ
            if rl.CheckCollisionPointRec(mouse_pos, slot_rect) && inv.slots[i].item_id != 0 {
                current_drag.is_dragging = true
                current_drag.dragged_item_id = inv.slots[i].item_id
                current_drag.source_slot_index = i
                
                // Tránh việc ảnh bị giật cục khi nhấp vào mép, ta lưu độ lệch
                current_drag.offset_x = mouse_pos.x - slot_rect.x
                current_drag.offset_y = mouse_pos.y - slot_rect.y
                break
            }
        }
    }
}
```

## 3. Vẽ Vật Phẩm Lơ Lửng (Floating Item)

Khi đang kéo, vật phẩm không nằm trong túi nữa, mà nó dính chặt vào con trỏ chuột. Chú ý: Phải vẽ túi đồ xong, sau đó mới vẽ vật phẩm kéo để nó nằm lớp trên cùng (Z-index cao nhất).

```odin
render_ui_drag :: proc() {
    if current_drag.is_dragging {
        mouse_pos := rl.GetMousePosition()
        
        // Vẽ icon vật phẩm tại tọa độ chuột trừ đi độ lệch
        draw_x := mouse_pos.x - current_drag.offset_x
        draw_y := mouse_pos.y - current_drag.offset_y
        
        // Hàm vẽ mờ đi 1 xíu (Alpha = 200) để tạo cảm giác đang cầm lơ lửng
        draw_item_icon(current_drag.dragged_item_id, draw_x, draw_y, 200)
    }
}
```

## 4. Xử Lý Khi Nhả Chuột (Drop)

Khâu phức tạp nhất là Nhả chuột.
Khi nhả, ta phải kiểm tra xem chuột đang thả ở đâu:
- Thả vào 1 ô trống khác trong túi đồ: Chuyển vật phẩm sang ô mới (Tính năng Sắp xếp - Swap).
- Thả ra ngoài bản đồ chơi (World Space) và trúng 1 Luống đất: Gieo hạt/Bón phân!
- Thả ra ngoài luân thường đạo lý (Không trúng đâu cả): Văng vật phẩm trả lại ô cũ.

```odin
    // 2. Kiểm tra Kết thúc kéo (Drop)
    if current_drag.is_dragging && rl.IsMouseButtonReleased(.LEFT) {
        
        dropped_on_slot := false
        // Lặp kiểm tra xem có thả trúng ô túi đồ nào khác không
        for i := 0; i < 30; i += 1 {
            slot_rect := get_slot_rect(i)
            if rl.CheckCollisionPointRec(mouse_pos, slot_rect) {
                // Đổi chỗ (Swap)
                swap_slots(inv, current_drag.source_slot_index, i)
                dropped_on_slot = true
                break
            }
        }
        
        // Nếu không thả vào túi đồ, mà thả ra Bản Đồ
        if !dropped_on_slot {
            // Chuyển tọa độ Chuột trên màn hình (Screen) thành tọa độ Bản đồ (World) thông qua Camera
            world_pos := rl.GetScreenToWorld2D(mouse_pos, camera)
            
            // Đổi tọa độ Pixel sang tọa độ Grid
            grid_x := int(world_pos.x) / TILE_SIZE
            grid_y := int(world_pos.y) / TILE_SIZE
            
            // Gửi một Yêu cầu Tương tác (Gieo hạt) vào Ô Grid này
            // Giống hệt như cách nhân vật bấm Space ở Chương 4!
            append(&event_queue, InteractEvent{ 
                entity_id: player_id, 
                target_grid_x: grid_x, 
                target_grid_y: grid_y, 
                tool_id: current_drag.dragged_item_id 
            })
        }
        
        // Reset trạng thái
        current_drag.is_dragging = false
    }
```

Bằng cách tái sử dụng `InteractEvent` của phần Lõi (Core Framework), UI Kéo thả hoạt động một cách mượt mà và an toàn. Giao diện trở nên vô cùng thân thiện!
