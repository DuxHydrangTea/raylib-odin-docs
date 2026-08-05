# Chương 17: Chuyển Cảnh Bản Đồ (Portal) & Lưu Game (Save/Load)

Game MMORPG phải có các Vòng sáng để chuyển bản đồ. Khi Ninja bước vào một Vòng sáng nằm ở mép phải bản đồ Tonek, họ sẽ được tải dữ liệu Bản đồ tiếp theo (Trường Haruna) và xuất hiện ở mép trái của bản đồ đó.

---

## 1. Cấu trúc Điểm Dịch Chuyển (Portal)

Bản chất Portal cũng là một Entity! Thay vì có Máu, có Vận tốc, nó chỉ có Tọa độ, Kích thước (Hitbox) và một Component lưu ID của Bản đồ đích.

Thêm vào `ecs/components.odin`:

```odin
PortalComponent :: struct {
    target_map_id: int, // ID của map sẽ chuyển đến (VD: 2 = Trường Haruna)
    spawn_x: f32,       // Tọa độ X khi nhảy sang map mới
    spawn_y: f32,
}

portals: map[EntityID]PortalComponent
```

## 2. Hàm Khởi tạo Map

Trong thực tế, người ta thường dùng File Tiled (đuôi `.tmx` hoặc `.json`) để thiết kế Map. 
Tuy nhiên ở đây ta giả lập một hàm LoadMap đơn giản:

```odin
// core/game.odin

current_map_id: int = 1

load_map :: proc(map_id: int, start_x, start_y: f32) {
    // 1. Dọn dẹp SẠCH SẼ toàn bộ Quái vật, Portal, và Đạn của Map cũ
    // LƯU Ý TỐI QUAN TRỌNG: Không được xóa Entity Ninja (Player)!
    for id in ecs.entities {
        if id == 0 do continue // Giữ lại Ninja
        ecs.destroy_entity(id)
    }
    
    // 2. Gán ID Map mới
    current_map_id = map_id
    
    // 3. Setup dữ liệu theo ID
    if map_id == 1 {
        // Load mảng Map Tonek (Như Chương 2)
        // Tạo vài con quái
        ecs.spawn_monster(400, 300)
        
        // Tạo Vòng sáng (Portal) đi sang Map 2 ở cuối đường
        p_id := ecs.create_entity()
        ecs.transforms[p_id] = ecs.TransformComponent{position = {800, 360}, size = {32, 64}}
        ecs.portals[p_id] = ecs.PortalComponent{target_map_id = 2, spawn_x = 50, spawn_y = 360}
        
    } else if map_id == 2 {
        // Load mảng Map Haruna
        // Tạo Vòng sáng đi ngược về Map 1
        p_id := ecs.create_entity()
        ecs.transforms[p_id] = ecs.TransformComponent{position = {0, 360}, size = {32, 64}}
        ecs.portals[p_id] = ecs.PortalComponent{target_map_id = 1, spawn_x = 750, spawn_y = 360}
    }
    
    // 4. Bốc Ninja ném xuống tọa độ điểm đến
    ecs.transforms[0].position.x = start_x
    ecs.transforms[0].position.y = start_y
    ecs.velocities[0].vel.x = 0 // Xóa trớn chạy
    ecs.velocities[0].vel.y = 0
}
```

## 3. System Kiểm tra Dẫm Vòng Sáng

Trong `ecs/systems.odin`, thêm `system_portals`:

```odin
system_portals :: proc() {
    if len(entities) == 0 do return
    player_id := entities[0]
    if player_id not_in transforms do return
    
    p_rect := rl.Rectangle{transforms[player_id].position.x, transforms[player_id].position.y, transforms[player_id].size.x, transforms[player_id].size.y}
    
    for id in entities {
        if id not_in portals do continue
        if id not_in transforms do continue
        
        portal := portals[id]
        t_rect := rl.Rectangle{transforms[id].position.x, transforms[id].position.y, transforms[id].size.x, transforms[id].size.y}
        
        // Nếu Ninja dẫm vào vòng sáng
        if rl.CheckCollisionRecs(p_rect, t_rect) {
            // Khi thao tác xóa quái/load map, tốt nhất nên đặt 1 cờ (Flag) rồi xử lý ở cuối Frame
            // Ở đây ta gọi trực tiếp để dễ hiểu (nhưng cẩn thận lỗi con trỏ)
            
            core.load_map(portal.target_map_id, portal.spawn_x, portal.spawn_y)
            break // Chuyển map rồi thì thoát vòng lặp ngay!
        }
    }
}
```

---

## 4. Save Game (Ghi Dữ Liệu Nhân Vật)

Trò chơi Offline cần lưu lại Tiến trình. Chúng ta sẽ lưu các Component của Entity `0` (Ninja) ra một chuỗi JSON và ghi xuống file.
Với Odin, thư viện `core:encoding/json` hỗ trợ Serialize Struct cực mạnh.

```odin
import "core:os"
import "core:encoding/json"

SaveData :: struct {
    map_id: int,
    x: f32,
    y: f32,
    hp: int,
    mp: int,
    level: int,
    // Chứa thêm mảng Inventory (Hành trang)
}

save_game :: proc() {
    if len(ecs.entities) == 0 do return
    p_id := ecs.entities[0]
    
    data := SaveData{
        map_id = current_map_id,
        x = ecs.transforms[p_id].position.x,
        y = ecs.transforms[p_id].position.y,
        hp = ecs.stats[p_id].hp,
        mp = ecs.stats[p_id].mp,
    }
    
    // Biến struct thành chuỗi JSON
    json_bytes, err := json.marshal(data)
    if err == nil {
        // Ghi xuống file
        os.write_entire_file("ninja_save.json", json_bytes)
    }
}

load_save_game :: proc() {
    json_bytes, ok := os.read_entire_file("ninja_save.json")
    if ok {
        data: SaveData
        err := json.unmarshal(json_bytes, &data)
        if err == nil {
            // Đổ dữ liệu vào Component
            load_map(data.map_id, data.x, data.y)
            ecs.stats[0].hp = data.hp
            ecs.stats[0].mp = data.mp
        }
    }
}
```

Nhét hàm `save_game()` vào phím Tắt (VD: F5) trong vòng lặp Game. Nhét `load_save_game()` vào nút "Continue" ngoài Menu chính.

Tuyệt vời! Game của bạn đã có cả chu kỳ Vòng Đời hoàn chỉnh! Chương 18 (Cuối) sẽ là món quà tri ân: Bộ Code tổng hợp để bạn cắm vào và chạy!
