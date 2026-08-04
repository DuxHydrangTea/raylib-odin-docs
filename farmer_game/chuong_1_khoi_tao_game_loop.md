# Chương 1: Khởi tạo Kiến trúc Dự án & Game Loop

Để làm một game nông trại với quy mô hàng trăm thực thể (cây, con vật) và tương tác mạng, nếu sử dụng phương pháp Lập trình Hướng đối tượng (OOP) truyền thống với hàng loạt kế thừa (`Entity -> Plant -> Tomato`) sẽ dễ dẫn đến **Mì Ý Code (Spaghetti Code)**. 

Thay vào đó, chúng ta sẽ áp dụng **ECS (Entity Component System)** tối giản bằng `Data-Oriented Design` (DOD) đặc trưng của Odin, kết hợp với kiến trúc Cập nhật Trạng thái tách rời.

## 1. Cấu trúc thư mục chuẩn (Tránh Anti-pattern)

Một dự án lộn xộn sẽ giết chết khả năng mở rộng. Hãy sắp xếp theo kiến trúc:

```text
farmer_game/
├── core/
│   ├── game.odin         // Quản lý Game Loop, State
│   ├── renderer.odin     // Chịu trách nhiệm gọi lệnh vẽ của Raylib
│   └── network.odin      // Kết nối và đồng bộ Server
├── ecs/
│   ├── components.odin   // Khai báo struct dữ liệu thuần (Position, Sprite, CropData)
│   └── systems.odin      // Chứa các proc xử lý dữ liệu (MovementSystem, GrowthSystem)
├── data/
│   └── config.json       // Chỉ số cây trồng (Thay vì hardcode)
└── main.odin             // Điểm khởi đầu chương trình
```

## 2. Thiết kế ECS Tối Giản trong Odin

Trong Odin, chúng ta sử dụng `SoA (Structure of Arrays)` hoặc `Mảng cấp phát sẵn (Pool)` để quản lý Thực thể (Entities). Giúp CPU Cache Hit cao nhất có thể.

```odin
// ecs/components.odin
package ecs

import rl "vendor:raylib"

EntityID :: distinct u32

// Component dữ liệu thuần
Position :: struct {
    grid_x, grid_y: int,
    pixel_x, pixel_y: f32,
}

CropData :: struct {
    seed_id: int,
    planted_at: f64, // Thời gian (Unix timestamp)
    stage: int,      // Mầm, Lớn, Ra quả
    watered: bool,
}

// Thế giới chứa tất cả Component
World :: struct {
    positions: [10000]Position,
    crops:     [10000]CropData,
    
    // Bitset để đánh dấu Entity nào sở hữu Component nào
    mask_position: [10000]bool,
    mask_crop:     [10000]bool,
    
    next_entity_id: EntityID,
}
```

**Tại sao không dùng Kế thừa (Inheritance)?**
- **Anti-pattern OOP:** Nếu `Con Chó` vừa biết đi (`Movable`), vừa biết sủa (`Soundable`), vừa là vật nuôi (`Livestock`). Bạn sẽ rất khó phân cấp kế thừa.
- **Giải pháp ECS:** Tạo 1 Entity, nhét 3 Component `Position`, `SoundEmitter`, `Livestock` vào. Vô cùng linh hoạt.

## 3. Quản lý Game Loop tách biệt Logic và Render

Trong `main.odin`, vòng lặp game không được trộn lẫn code Tính toán (`x += speed`) với code Vẽ (`DrawTexture`).

```odin
// main.odin
package main

import rl "vendor:raylib"
import "core/game"
import "ecs"

main :: proc() {
    rl.InitWindow(800, 600, "Avatar Farm Clone")
    rl.SetTargetFPS(60)
    
    // Khởi tạo World
    world: ecs.World
    
    // Khởi tạo Logic
    game.init(&world)

    for !rl.WindowShouldClose() {
        dt := rl.GetFrameTime()
        
        // 1. Cập nhật hệ thống (Logic)
        game.update(&world, dt)
        
        // 2. Render hệ thống (Đồ họa)
        rl.BeginDrawing()
        rl.ClearBackground(rl.RAYWHITE)
        
        game.render(&world)
        
        rl.EndDrawing()
    }
    
    rl.CloseWindow()
}
```

Với cấu trúc này, khi bạn chuyển game thành Game Online nhiều người, phần `game.update()` hoàn toàn có thể được chạy ngầm trên Server (không cần thư viện đồ họa Raylib) để giả lập nông trại!
