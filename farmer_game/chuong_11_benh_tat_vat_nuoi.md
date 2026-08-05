# Chương 11: Hệ Thống Bệnh Tật Ở Vật Nuôi (Sinh Lão Bệnh Tử)

Giống như cây cối bị sâu ăn lá, vật nuôi cũng có thể bị ốm. Nếu Gà rù hoặc Lợn bệnh, chúng sẽ ngừng sản xuất trứng/sữa, và nếu để lâu quá không chữa, chúng sẽ chết và người chơi mất trắng tiền đầu tư.

## 1. Thiết kế dữ liệu Bệnh tật

Vật nuôi có thể mắc nhiều loại bệnh. Dùng Bit-flag (Cờ nhị phân) là cách cực kì thông minh để một con vật có thể mắc CÙNG LÚC nhiều loại bệnh mà không tốn thêm byte bộ nhớ nào.

```odin
package ecs

DiseaseFlag :: enum u8 {
    NONE    = 0,
    FLU     = 1 << 0, // Cúm (Gà rù)
    FOOT    = 1 << 1, // Lở mồm long móng (Bò, Lợn)
    STARVE  = 1 << 2, // Đói lả (Do hết thức ăn)
}

LivestockComponent :: struct {
    // ... các trường cũ
    diseases: DiseaseFlag, // Sử dụng toán tử Bitwise
    sick_started_at: f64,  // Thời điểm bắt đầu bệnh để tính toán cái chết
}
```

## 2. Hệ thống Gieo rắc mầm bệnh (Disease System)

System này chạy định kỳ (Vd: Mỗi 5 phút) để xổ số xem con nào xui xẻo bị bệnh.
Đặc biệt, cơ chế lây nhiễm (Contagion): Nếu trong chuồng có 1 con bệnh, tỷ lệ những con khác dính bệnh sẽ tăng gấp 10 lần!

```odin
update_livestock_disease :: proc(world: ^World) {
    import "core:math/rand"
    
    // Đếm xem trong chuồng đang có bao nhiêu mầm bệnh
    sick_count := 0
    for i := 0; i < int(world.next_entity_id); i += 1 {
        if world.mask_livestock[i] {
            if world.livestock[i].diseases != .NONE {
                sick_count += 1
            }
        }
    }
    
    // Tỷ lệ lây nhiễm cơ bản 0.1%. Cộng thêm 1% cho mỗi con đang ốm.
    infection_chance := 0.001 + (f32(sick_count) * 0.01)
    
    // Xổ số cho những con đang khỏe
    for i := 0; i < int(world.next_entity_id); i += 1 {
        if world.mask_livestock[i] {
            animal := &world.livestock[i]
            if animal.diseases == .NONE {
                if rand.float32() < infection_chance {
                    animal.diseases |= .FLU // Gán cờ bệnh (Dùng phép OR |)
                    animal.sick_started_at = get_current_time()
                    
                    // Con vật lập tức ngừng đẻ trứng/sữa
                    animal.is_producing = false 
                }
            }
        }
    }
}
```

## 3. Án Tử Hình (Death System)

Nếu 24 giờ trôi qua (86400 giây) mà người chơi không chích thuốc, con vật sẽ chết.

```odin
update_livestock_death :: proc(world: ^World) {
    current_time := get_current_time()
    
    for i := 0; i < int(world.next_entity_id); i += 1 {
        if world.mask_livestock[i] {
            animal := &world.livestock[i]
            
            if animal.diseases != .NONE {
                if current_time - animal.sick_started_at > 86400 {
                    // Xóa sổ Entity khỏi thế giới
                    destroy_entity(world, EntityID(i))
                }
            }
        }
    }
}
```

## 4. Bơm Thuốc (Chữa Bệnh)

Khi người chơi cầm `TOOL_VACCINE` và tương tác với con vật bị ốm. Ta sử dụng toán tử Bitwise AND NOT (`&~`) để gỡ bỏ cờ bệnh.

```odin
// Đăng ký Handler Vắc-xin vào init_tool_handlers()
tool_handlers[.VACCINE] = proc(world: ^World, event: InteractEvent) {
    // Tìm Entity con vật nằm trong ô target_grid_x, y
    target_animal_id, found := find_livestock_at(world, event.target_grid_x, event.target_grid_y)
    if !found do return
    
    animal := &world.livestock[target_animal_id]
    
    // Kiểm tra xem nó có bị Cúm không
    if .FLU in animal.diseases {
        // Gỡ bỏ cờ Cúm
        animal.diseases &= ~.FLU
        
        // Reset thời gian bệnh nếu đã hết các bệnh khác
        if animal.diseases == .NONE {
            animal.sick_started_at = 0
            // Cho phép đẻ trứng lại
            animal.is_producing = true
            animal.last_fed_time = get_current_time()
        }
        
        remove_item_from_inventory(event.entity_id, ITEM_VACCINE, 1)
        play_sound("heal.wav")
    }
}
```

**Anti-pattern cần tránh:**
Nhiều bạn lưu 1 mảng các con vật vào `List<Animal>`. Khi 1 con vật chết đi, bạn xóa nó khỏi List bằng hàm `List.RemoveAt(i)`. Hành động này cực kỳ nguy hiểm vì nó làm xô lệch toàn bộ Index của các con vật phía sau, gây crash game.
Bằng cách dùng ECS (`destroy_entity`), ta chỉ đơn giản là lật cờ `world.mask_livestock[i] = false`, và ô bộ nhớ đó sẽ được tái sử dụng an toàn sau này. Đọc thêm về **Object Pooling** ở Tab Troubleshooting nhé!
