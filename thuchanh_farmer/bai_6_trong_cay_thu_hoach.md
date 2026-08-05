# Bài 6: Trồng Cây & Hệ Thống Thời Gian (Time-based Growth)

Đây là chương đáng mong đợi nhất. Ta sẽ gieo hạt, dùng hàm `GetTime()` để tính số giây trôi qua, và làm cái cây lớn lên theo thời gian thực (Giống hệt Avatar 2D nhưng ở quy mô mini).

## 1. Thiết Kế Component Cây Trồng
Một cái cây cần lưu trữ: Thời điểm gieo hạt (Timestamp), nó lớn mất bao lâu, và nó đang ở giai đoạn (Phase) nào.

```odin
// Thêm vào khối Khai báo Component ở Bài 3
Crop :: struct {
    planted_at: f64,       // Số giây tính từ lúc game bật lên
    growth_duration: f64,  // Mất 10 giây để chín hoàn toàn
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
Ta thêm một phím mới để đổi sang công cụ Hạt Giống (Seed). Cập nhật hàm `farming_interaction_system` ở Bài 5:

```odin
    EquipTool :: enum { HAND, HOE, WATERING_CAN, SEED }
    // ...
    
    // Đang cầm hạt giống và ném vào ô Đất Ướt (2)
    } else if current_tool == .SEED {
        if tile_id == 2 {
            // Tạm thời đánh dấu ô đất này có cây bằng ID = 3
            map_data[ty][tx] = 3
            
            // Sinh ra Thực thể Cây Trồng (Entity)
            id := world.next_entity_id
            world.next_entity_id += 1
            
            // Tọa độ của cây chính là tọa độ ô lưới (tx, ty)
            world.positions[id] = Position { grid_x = tx, grid_y = ty, pixel_x = f32(tx*TILE_SIZE), pixel_y = f32(ty*TILE_SIZE) }
            world.mask_position[id] = true
            
            // Component Cây
            world.crops[id] = Crop {
                planted_at = rl.GetTime(), // Bấm đồng hồ!
                growth_duration = 10.0,    // Trồng 10 giây là chín
                phase = 0,
            }
            world.mask_crop[id] = true
            
            // Gắn hình ảnh Mầm cây (Giả lập bằng màu Vàng ở Bài 2)
            world.renderables[id] = Renderable { tex_id = .PLANT_SEED, color = rl.YELLOW }
            world.mask_renderable[id] = true
            
            fmt.println("Da gieo hat!")
        }
    }
```
*(Lưu ý: Mở hàm `init_dummy_textures()` ở Bài 2, sinh thêm ảnh `.PLANT_SEED` (Vàng) và `.PLANT_GROWN` (Đỏ cam) bằng `rl.GenImageColor(TILE_SIZE, TILE_SIZE, rl.YELLOW)` nhé!)*

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
                
                // Nếu tuổi thọ đã vượt quá thời gian sinh trưởng
                if age >= crop.growth_duration {
                    crop.phase = 1 // Chín!
                    
                    // Nâng cấp hình ảnh lên cây trưởng thành
                    world.renderables[i].tex_id = .PLANT_GROWN
                    world.renderables[i].color = rl.ORANGE
                    
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
