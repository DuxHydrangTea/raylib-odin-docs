# Chương 7: Hệ Thống Sức Khỏe Cây (Cỏ Dại & Sâu Bệnh)

Nếu người chơi chỉ cần gieo hạt rồi tắt máy, 5 tiếng sau quay lại thu hoạch thì game sẽ quá nhàm chán. Để níu chân người chơi liên tục vào game, Avatar 2D áp dụng cơ chế Cỏ Dại và Sâu Bệnh ngẫu nhiên làm đình trệ sự phát triển của cây.

## 1. Mở rộng CropComponent

Chúng ta cần thêm các biến theo dõi tình trạng sinh bệnh và bù trừ thời gian.

```odin
package ecs

CropComponent :: struct {
    config_id: int,       
    planted_at: f64,      
    
    // Hệ thống Sức khỏe
    has_bugs: bool,       // Bị sâu ăn lá
    has_weeds: bool,      // Bị cỏ dại hút chất dinh dưỡng
    
    // Hình phạt thời gian
    sick_started_at: f64, // Thời điểm bắt đầu dính bệnh
    total_sick_time: f64, // Tổng thời gian đã bị bệnh (Bị trừ khỏi tuổi của cây)
    
    current_phase: int,
    is_dead: bool,
}
```

## 2. Sinh Bệnh Ngẫu Nhiên (Random Events)

Hệ thống sẽ chạy ngầm và dựa vào Random (RNG) để ném cỏ dại/sâu bọ lên cây.

```odin
update_crop_health_system :: proc(world: ^World, dt: f32) {
    for i := 0; i < int(world.next_entity_id); i += 1 {
        if world.mask_crop[i] {
            crop := &world.crops[i]
            if crop.is_dead || crop.current_phase == get_max_phase(crop.config_id) do continue
            
            // Xổ số ngẫu nhiên: Tỷ lệ sinh bệnh là 1% mỗi phút (kiểm tra theo Tick)
            if !crop.has_bugs && !crop.has_weeds {
                if rand_percentage() < 0.001 {
                    // Random bị sâu hay bị cỏ
                    if rand_int(2) == 0 {
                        crop.has_bugs = true
                    } else {
                        crop.has_weeds = true
                    }
                    crop.sick_started_at = get_current_time()
                }
            }
        }
    }
}
```

## 3. Chỉnh sửa Lại Thời Gian Phát Triển (Đình trệ)

Đây là chỗ hóc búa nhất. Nếu cây bị sâu ăn, thời gian phát triển bị đứng im. Khi tính toán `current_phase` ở Chương 6, ta phải TRỪ ĐI tổng thời gian cây đã bị bệnh.

```odin
// (Bên trong hàm update_crop_growth của Chương 6)

// Tính tổng thời gian cây bị bệnh (Từ lúc dính tới hiện tại)
current_sick_penalty: f64 = 0
if crop.has_bugs || crop.has_weeds {
    current_sick_penalty = current_time - crop.sick_started_at
}

// Tuổi thực sự của cây (Đã trừ đi những khoảng thời gian ốm đau)
effective_age := (current_time - crop.planted_at) - crop.total_sick_time - current_sick_penalty

// Sử dụng effective_age để tính Phase thay vì age thông thường...
```

**Ví dụ thực tế:** 
1. Cây Cà chua cần 2 tiếng để chín. Trồng lúc `8:00`. Lẽ ra `10:00` chín.
2. Lúc `9:00`, cây dính Cỏ Dại. 
3. Bạn đi học. Lúc `11:00` bạn vào game.
4. Cây vẫn đang ở `Phase Mầm` (Vì tuổi thực của cây = `11 - 8 - (11 - 9)` = 1 tiếng). 
5. Bạn nhổ cỏ. Lúc này `total_sick_time` được cộng thêm 2 tiếng. Cây bắt đầu lớn lại bình thường, và sẽ chín vào lúc `12:00`.

## 4. Chữa Bệnh (Cứu Cây)

Người chơi cầm cuốc (Nhổ cỏ) hoặc Bình xịt sâu (Xịt sâu) bấm vào cây.

```odin
if tool == .HOE && crop.has_weeds {
    // Chữa khỏi
    crop.has_weeds = false
    
    // Chốt sổ thời gian bị bệnh và cộng dồn vào total_sick_time
    crop.total_sick_time += (get_current_time() - crop.sick_started_at)
    crop.sick_started_at = 0
    
    play_sound("weed_pull.wav")
    // Tương tự cho xịt sâu với tool == BUG_SPRAY
}
```

Kiến trúc này đảm bảo Cây cối của bạn phát triển (hoặc bị thui chột) một cách 100% Deterministic (tất định) dựa trên lịch sử Timestamp, bất chấp việc máy chủ online hay offline.
