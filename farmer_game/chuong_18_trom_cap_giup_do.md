# Chương 18: Trộm Cắp, Giúp Đỡ & Race Condition

Avatar 2D sống nhờ tính năng này. Chủ nhà đi ngủ quên thu hoạch, sáng dậy thấy vườn cà chua trụi lủi. Chó cắn khách tới tấp. Tình bạn rạn nứt.

## 1. Cơ Chế Giúp Đỡ (Help System)

Trước khi tính tới chuyện xấu, hãy làm chuyện tốt. Nếu bạn sang nhà B và thấy cây của B bị cỏ dại (như Chương 7 đã mô tả). Bạn cầm cuốc gỡ cỏ giùm B.
- Logic gỡ cỏ chạy Y HỆT như hồi bạn tự nhổ cỏ vườn mình. Bấm phím -> Bay lên Server -> Server tìm ô đất.
- NHƯNG Server phải check quyền: "Ai đang nhổ cỏ?". Của A. "Nhà ai?". Nhà B.
- Nếu khác chủ, Server cộng điểm danh vọng/Thân thiện cho A. Không cộng tiền.

```odin
if room.owner_id != packet.client_id {
    // Không phải chủ nhà, hành động này là "Giúp đỡ"
    add_friendship_points(packet.client_id, 10)
    broadcast_chat_message("Hệ thống", fmt.tprintf("Người chơi %d vừa giúp tưới nước!", packet.client_id))
}
```

## 2. Kỹ Thuật Trộm Cắp (Stealing Logic)

Nếu Cây đã chín (Phase cuối cùng), và Khách vươn tay hái. Đây là hành vi Trộm Cắp!

**Quy tắc cân bằng của Game:** 
- Khách không bao giờ hái được 100% sản lượng. Mỗi cây chỉ cho phép bị trộm tối đa 1 hoặc 2 quả (tức 20%). 
- Chủ nhà ngủ dậy hái vẫn còn 80%. Tránh việc chủ nhà bỏ game vì mất sạch.

```odin
// Server-side
handle_harvest_request :: proc(packet: InteractPlotPacket) {
    room := active_rooms[packet.room_id]
    plot := room.farm_map.get_plot_at(packet.grid_x, packet.grid_y)
    
    if plot.has_plant && is_crop_ready(plot.crop_entity) {
        
        is_thief := (packet.client_id != room.owner_id)
        
        if is_thief {
            // Kiểm tra xem cây này đã bị trộm tới mức giới hạn chưa
            if plot.crop.stolen_count >= MAX_STOLEN_PER_CROP {
                send_error_to_client(packet.client_id, "Cây này đã bị vặt trụi, tha cho chủ nhà đi!")
                return
            }
            
            // Tăng biến đếm số lần bị trộm
            plot.crop.stolen_count += 1
            
            // Trộm thì được ít tiền/sản phẩm hơn
            add_item_to_inventory(packet.client_id, plot.crop.config_id, 1)
            
            // CHÚ Ý: Cây KHÔNG biến mất (Trái với Chương 6). 
            // Cây vẫn đứng đó chờ chủ nhà về thu hoạch mớ còn lại.
            broadcast_plot_update(packet.room_id, packet.grid_x, packet.grid_y)
            
        } else {
            // Là chủ nhà, hái nốt chỗ còn lại
            yield := MAX_YIELD - plot.crop.stolen_count
            add_item_to_inventory(packet.client_id, plot.crop.config_id, yield)
            
            // Bây giờ cây mới bị tiêu hủy
            destroy_crop(plot.crop_entity)
            plot.has_plant = false
            plot.state = .PLOWED
            broadcast_plot_update(packet.room_id, packet.grid_x, packet.grid_y)
        }
    }
}
```

## 3. Khóa Bất Đồng Bộ (Race Condition) khi Trộm

**Bài Toán Khét Lẹt:**
Quả cà chua của nhà Cường. 
Thằng A và thằng B cùng canh giờ Cà chua chín, đứng kế bên. Cả hai cùng spam nút Space 10 lần một giây.
Gói tin của A và B bay tới Server GẦN NHƯ CÙNG LÚC.

Nếu code của bạn đọc dữ liệu vào, rồi lưu xuống như bình thường, A lấy 1 quả, B lấy 1 quả, Quả Cà Chua rớt âm quả.
=> Giải quyết bằng **Mutex Lock** hoặc xử lý Hàng đợi đơn luồng (Single-thread Event Loop) ở phía Server (Xem chi tiết kỹ thuật này tại *Phụ lục Lỗi Online Chương 13*). Đảm bảo một khi Gói của A đang chạy vào khu vực check cây chín, Gói của B phải bị gạt ra hoặc chờ A xử lý xong, lúc B nhảy vào check sẽ thấy `stolen_count` đã max, báo lỗi thất bại.

## 4. Chó Cắn Trộm

Nếu Khách hái đồ, Server sẽ âm thầm đánh thức AI Chó Canh (Chương 12) ở máy chủ.
Chó bắt đầu kích hoạt State `.ALERT` và phi tới cắn. Khách bị trừ tiền và rơi đồ vừa trộm ra đất! Cảm giác chạy trối chết khỏi đàn chó trong Avatar chính là tuyệt tác thiết kế tâm lý người chơi.
