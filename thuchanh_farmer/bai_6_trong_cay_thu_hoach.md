# Bài 6: Trồng Cây & Hệ Thống Thời Gian (Time-based Growth)

Đây là chương đáng mong đợi nhất. Ta sẽ gieo hạt, dùng hàm `GetTime()` để tính số giây trôi qua, và làm cái cây lớn lên theo thời gian thực (Giống hệt Avatar 2D nhưng ở quy mô mini).

## 1. Thiết Kế Component Cây Trồng
Thay vì hardcode, ta sử dụng **Data-Driven Design** (Bảng dữ liệu) để dễ dàng thêm hàng chục loại hạt giống sau này mà không cần sửa logic.

```odin
// Cấu trúc dữ liệu cấu hình cho 1 loại hạt
SeedData :: struct {
    duration: f64,
    seed_tex: TextureID,
    grown_tex: TextureID,
    seed_color: rl.Color,
    grown_color: rl.Color,
}

// Từ điển (Map) lưu trữ thông tin mọi loại hạt trong game
seed_db: map[EquipTool]SeedData

// Khởi tạo ở đầu hàm main()
init_seed_db :: proc() {
    seed_db[.SEED_CARROT] = { 10.0, .SEED_CARROT, .GROWN_CARROT, rl.YELLOW, rl.ORANGE }
    seed_db[.SEED_TOMATO] = { 15.0, .SEED_TOMATO, .GROWN_TOMATO, rl.SKYBLUE, rl.RED }
}

// Component Cây trồng thực tế
Crop :: struct {
    type: EquipTool,       // Cây đang trồng là loại gì?
    planted_at: f64,       // Timestamp lúc gieo hạt
    phase: int,            // 0: Hạt mầm, 1: Cây trưởng thành
}

// Cập nhật Struct World
World :: struct {
    // ...
    crops: [100]Crop,
    mask_crop: [100]bool,
}
```

## 2. Gieo Hạt (Trồng cây)
Cập nhật hàm `farming_interaction_system` ở Bài 5. Ta sẽ kiểm tra `current_tool` có nằm trong `seed_db` hay không thay vì dùng if-else chuỗi:

```odin
    EquipTool :: enum { HAND, HOE, WATERING_CAN, SEED_CARROT, SEED_TOMATO }
    // ...
    
    // Nếu đang cầm một công cụ CÓ TRONG bảng hạt giống và ném vào Đất Ướt (2)
    } else if current_tool in seed_db {
        if tile_id == 2 {
            map_data[ty][tx] = 3
            
            id := world.next_entity_id
            world.next_entity_id += 1
            
            world.positions[id] = Position { grid_x = tx, grid_y = ty, pixel_x = f32(tx*TILE_SIZE), pixel_y = f32(ty*TILE_SIZE) }
            world.mask_position[id] = true
            
            // Lấy dữ liệu cấu hình hạt giống từ Map
            seed_data := seed_db[current_tool]

            world.crops[id] = Crop {
                type = current_tool,
                planted_at = rl.GetTime(), // Bấm đồng hồ!
                phase = 0,
            }
            world.mask_crop[id] = true
            
            // Gắn hình ảnh Mầm cây dựa trên dữ liệu tra cứu được
            world.renderables[id] = Renderable { tex_id = seed_data.seed_tex, color = seed_data.seed_color }
            world.mask_renderable[id] = true
            
            fmt.println("Da gieo hat!")
        }
    }
```
*(Lưu ý: Bạn nhớ gọi hàm `init_seed_db()` bên trong hàm `main()` nhé!)*

## 3. Hệ Thống Sinh Trưởng (Growth System)
Cây không tự lớn. Ta cần một System chạy mỗi khung hình, lấy Thời gian hiện tại trừ đi Thời gian gieo hạt để tính ra "Tuổi" của cây.

```odin
crop_growth_system :: proc(world: ^World) {
    current_time := rl.GetTime()
    
    for i := 0; i < world.next_entity_id; i += 1 {
        if world.mask_crop[i] {
            crop := &world.crops[i]
            
            // Nếu chưa chín (Chỉ có 2 phase: 0 và 1)
            if crop.phase == 0 {
                age := current_time - crop.planted_at
                
                // Tra cứu thông tin loại cây đang trồng
                seed_data := seed_db[crop.type]
                
                // Nếu tuổi thọ đã vượt quá thời gian sinh trưởng
                if age >= seed_data.duration {
                    crop.phase = 1 // Chín!
                    
                    // Nâng cấp hình ảnh lên cây trưởng thành tự động
                    world.renderables[i].tex_id = seed_data.grown_tex
                    world.renderables[i].color = seed_data.grown_color
                    
                    fmt.println("Cây đã chín!")
                }
            }
        }
    }
}
```

## 4. Thu Hoạch (Thu nhặt Nông sản)
Bây giờ, nếu cây đã chín (Phase = 1) và ta dùng Bàn Tay (Phím `HAND`) để thu hoạch. Cập nhật `farming_interaction_system`:

```odin
    } else if current_tool == .HAND {
        if tile_id == 3 {
            // Tìm thực thể Cây đang nằm ở ô này
            for i := 0; i < world.next_entity_id; i += 1 {
                if world.mask_crop[i] && world.positions[i].grid_x == tx && world.positions[i].grid_y == ty {
                    if world.crops[i].phase == 1 { // Nếu cây ĐÃ CHÍN
                        
                        // 1. Phá hủy Entity cây (Bằng cách tắt Mask)
                        world.mask_crop[i] = false
                        world.mask_renderable[i] = false
                        world.mask_position[i] = false
                        
                        // 2. Trả ô đất về trạng thái Tơi xốp (1)
                        map_data[ty][tx] = 1
                        
                        fmt.println("THU HOACH THANH CONG! +1 Nong san")
                    } else {
                        fmt.println("Cay chua chin, khong duoc hai!")
                    }
                }
            }
        }
    }
```

**Thử nghiệm thành quả:**
Bật Game -> Cuốc đất -> Tưới đất -> Lấy hạt giống ném xuống.
Một mầm cây màu Vàng xuất hiện. Đếm đúng 10 giây (hoặc đứng nhìn). PÓP! Cây đổi sang màu Cam.
Lấy tay (Bấm phím tương ứng `HAND`) bấm vào cái cây Cam. Cây biến mất và ô đất nâu tơi xốp hiện ra trở lại.
Chu kỳ Nông trại đã khép kín cực kì hoàn hảo và chặt chẽ bằng ECS!

Ở **Bài cuối**, ta sẽ làm một chút UI Kéo thả (Drag & Drop) và hạt bụi (Particle) để Game trông lung linh hơn nhé!
