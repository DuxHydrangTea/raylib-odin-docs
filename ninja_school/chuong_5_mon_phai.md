# Chương 5: Thiết kế 6 Môn Phái Huyền Thoại (Class System)

Ninja School Online có 3 trường học (Haruna, Hirosaki, Ookaza), tương ứng đào tạo 6 loại vũ khí (Môn phái) với bộ kỹ năng và chỉ số hoàn toàn khác biệt. 

Thay vì hard-code các câu lệnh `if class == .Kiem { HP = 100 } else if class == .Tieu { HP = 50 }`, chúng ta sẽ sử dụng kiến trúc Data-Driven (Định hướng Dữ liệu) để quản lý, giúp bạn dễ dàng cân bằng game (Balance) sau này.

---

## 1. Phân loại Môn Phái & Hệ Thuộc Tính

Mỗi môn phái trong NSO đều mang một hệ ngũ hành (Băng, Hỏa, Phong). Hệ này cực kỳ quan trọng vì nó quyết định **Trạng thái dị thường** áp lên quái vật khi đánh trúng.

Mở `ecs/components.odin` và thêm:

```odin
package ecs

// Hệ Ngũ Hành (Elements)
Element :: enum {
    None,
    Fire, // Hỏa (Gây Bỏng)
    Ice,  // Băng (Đóng băng)
    Wind, // Phong (Độc/Làm chậm)
}

// 6 Môn Phái
NinjaClass :: enum {
    Sword,  // Kiếm (Hệ Hỏa - Cận chiến)
    Dart,   // Tiêu (Hệ Hỏa - Đánh xa)
    Kunai,  // Kunai (Hệ Băng - Cận chiến)
    Bow,    // Cung (Hệ Băng - Đánh xa)
    Fan,    // Quạt (Hệ Phong - Đánh xa)
    Dagger, // Đao (Hệ Phong - Cận chiến)
}

// Kiểu Tấn Công
AttackType :: enum {
    Melee, // Cận chiến (Chém ra Hitbox ngay trước mặt)
    Range, // Xa (Bắn ra Ám khí - Projectile)
}
```

## 2. Bảng Cấu Hình Môn Phái (Data-Driven)

Tiếp theo, ta tạo một Struct định nghĩa "Khuôn mẫu" của 1 phái, và 1 Bảng Tra Cứu (Lookup Table / Map) để lưu toàn bộ thông số mặc định của 6 phái.

```odin
// Struct chứa khuôn mẫu của 1 Class
ClassConfig :: struct {
    name:         string,
    base_hp:      int,
    base_mp:      int,
    base_damage:  int,
    attack_type:  AttackType,
    element:      Element,
    attack_range: f32, // Tầm đánh (Pixel)
}

// Bảng tra cứu (Lookup Table) tĩnh
// Khi khởi tạo Ninja, chỉ cần lấy dữ liệu từ bảng này đắp vào Component
g_class_configs: map[NinjaClass]ClassConfig = {
    .Sword = {
        name = "Kiem Khach",
        base_hp = 120,
        base_mp = 50,
        base_damage = 25,
        attack_type = .Melee,
        element = .Fire,
        attack_range = 50.0,
    },
    .Dart = {
        name = "Phi Tieu",
        base_hp = 70,
        base_mp = 80,
        base_damage = 35,
        attack_type = .Range,
        element = .Fire,
        attack_range = 300.0, // Bắn rất xa
    },
    .Kunai = {
        name = "Kunai",
        base_hp = 150, // Trâu bò nhất
        base_mp = 40,
        base_damage = 20,
        attack_type = .Melee,
        element = .Ice,
        attack_range = 60.0,
    },
    // ... Thêm Cung, Quạt, Đao tương tự ...
}
```

## 3. Hàm Tạo Ninja Chuyên Nghiệp

Bây giờ chúng ta sẽ viết một hàm `spawn_ninja` thực thụ. Truyền vào Hệ phái mà người chơi chọn, hàm sẽ tự động bốc dữ liệu từ `g_class_configs` để sinh ra Nhân vật.

Mở `ecs/entities.odin`:

```odin
spawn_ninja :: proc(start_x, start_y: f32, class_type: NinjaClass) -> EntityID {
    id := create_entity() // Hàm Pool ID ở Chương 4
    
    // Lấy config từ bảng
    cfg := g_class_configs[class_type]
    
    // 1. Khởi tạo Tọa độ
    transforms[id] = TransformComponent{
        position = {start_x, start_y},
        size = {32, 64}, // Người cao 64px
    }
    
    // 2. Khởi tạo Vận tốc
    velocities[id] = VelocityComponent{}
    
    // 3. Khởi tạo Chỉ số theo Class
    stats[id] = StatsComponent{
        hp = cfg.base_hp,
        max_hp = cfg.base_hp,
        mp = cfg.base_mp,
        max_mp = cfg.base_mp,
        damage = cfg.base_damage,
        defense = 5,
        speed = 200.0,
    }
    
    // 4. Khởi tạo Thông số Chiến đấu
    combats[id] = CombatComponent{
        entity_type = .Player,
        attack_speed = 1.0, // 1 giây chém 1 nhát
        attack_range = cfg.attack_range,
        is_attacking = false,
        attack_timer = 0.0,
    }
    
    return id
}
```

> [!TIP]
> Việc thiết kế **Bảng tra cứu (Lookup Table)** như trên giúp game của bạn cực kỳ linh hoạt. Sau này khi làm tính năng Cập nhật Game (Patch), bạn chỉ cần đọc dữ liệu của bảng `g_class_configs` từ một file `.json` bên ngoài là có thể cân bằng sức mạnh môn phái mà không cần phải biên dịch lại mã nguồn (Re-compile).

Thế là xong! Hệ thống Class đã cực kỳ gọn gàng. Ở Chương 6, chúng ta sẽ bắt đầu xử lý logic Vung kiếm (Melee Hitbox) và Bắn cung (Projectile) dựa vào biến `AttackType` mà chúng ta vừa định nghĩa.
