# Chương 17: Tính Năng Qua Nhà Hàng Xóm (Social Visit)

Avatar 2D không chỉ là game tự kỷ trồng trọt, nó là Mạng Xã Hội (MXH). Việc sang nhà người yêu ngắm cảnh hoặc lén sang nhà kẻ thù dòm ngó là tính năng cốt lõi.

## 1. Thiết Kế Cơ Chế Dịch Chuyển (Warping)

Làm sao để một người chơi A (đang ở nông trại của mình) có thể "nhảy" sang nông trại của người chơi B?

**Quy trình chuyển Room phía Server:**
```odin
// Khi Client gửi yêu cầu: "Tôi muốn sang thăm nhà thằng ID = 456"
handle_warp_request :: proc(player_id: u32, target_farm_id: u32) {
    
    // 1. Gỡ Player khỏi căn phòng hiện tại
    current_room_id := get_player_current_room(player_id)
    if current_room_id != 0 {
        remove_player_from_room(player_id, current_room_id)
        broadcast_player_leave(current_room_id, player_id)
    }
    
    // 2. Load Nông trại của B lên RAM nếu nó chưa có (Lazy load)
    if !(target_farm_id in active_rooms) {
        // Truy vấn DB và nạp vào active_rooms (Xem Chương 16)
        load_farm_into_memory(target_farm_id)
    }
    
    // 3. Đưa Player A vào căn phòng của B
    add_player_to_room(player_id, target_farm_id)
    
    // 4. Báo cho A biết: "Đây là toàn bộ bản đồ nhà thằng B, vẽ ra màn hình đi"
    send_map_snapshot(player_id, target_farm_id)
    
    // 5. Báo cho tất cả những người đang ở nhà thằng B (kể cả B) biết: "Thằng A vừa bước vào cửa"
    broadcast_player_enter(target_farm_id, player_id)
}
```

## 2. Render Đa Người Chơi ở Client (Multiplayer Culling)

Tại Client, trong mảng `World` của ECS, chúng ta không chỉ có 1 `Player`. Chúng ta sẽ có danh sách các Network Players. 
Mỗi khi nhận gói tin `PlayerEnter` từ Server, Client sẽ rớt ra (Spawn) một hình nộm (Dummy) đại diện cho người chơi kia. Khi nhận gói tin `PlayerMove`, hình nộm đó sẽ trượt (Lerp) sang vị trí mới (Sử dụng kỹ thuật nội suy như đã giải thích ở khóa Lỗi Online).

## 3. Hệ Thống Trò Chuyện (Chat Bong Bóng)

MXH thì phải có Chat. Đặc trưng của Avatar là bong bóng chat nổi bồng bềnh trên đầu nhân vật.

```odin
// Client-side: Xử lý hiển thị
ChatBubble :: struct {
    text: string,
    time_to_live: f32, // Tồn tại 5 giây rồi biến mất
}

// Gắn Component này vào Player
render_chat_bubbles :: proc(world: ^World, cam: ^rl.Camera2D) {
    for i := 0; i < int(world.next_entity_id); i += 1 {
        if world.mask_player[i] && world.mask_chat[i] {
            pos := &world.positions[i]
            chat := &world.chats[i]
            
            // Vẽ hộp thoại lùi lên phía trên đầu nhân vật (Y - 40px)
            box_rect := rl.Rectangle{ pos.pixel_x - 20, pos.pixel_y - 40, 100, 30 }
            rl.DrawRectangleRounded(box_rect, 0.5, 4, rl.WHITE)
            rl.DrawText(fmt.ctprintf("%s", chat.text), i32(box_rect.x + 5), i32(box_rect.y + 5), 10, rl.BLACK)
        }
    }
}
```

Khi Player A gõ phím và Enter, gói tin `ChatPacket("Chào B")` bay lên Server. Server Broadcast nó cho những ai đang đứng cùng nông trại. Các Client sẽ móc tin nhắn này vào `ChatBubble` của hình nộm A.

Bây giờ bạn có thể đi vào nhà hàng xóm, chào hỏi họ, và sau đó... chuẩn bị cho chương đen tối nhất: Ăn Trộm!
