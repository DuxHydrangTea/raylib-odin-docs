# Bài 3: Lắp Ráp ECS (Entity Component System) Cơ Bản

Trong OOP (Hướng đối tượng), bạn tạo class `class Player { x, y, hp, move() }`. Nhược điểm là khi game có 100 thực thể (Cây, Gà, Phân bón), mọi thứ kế thừa chằng chịt rắc rối.

Odin hỗ trợ tuyệt vời **Data-Oriented Design (DOD)**. Ở bài này, ta sẽ ráp một hệ thống ECS siêu đơn giản để quản lý Nhân vật.

## 1. Định nghĩa Component
Component chỉ chứa **DỮ LIỆU THUẦN (Biến)**, tuyệt đối không chứa Hàm chức năng (Function).

```odin
// (Thêm vào trên hàm main)

// Component Vị Trí
Position :: struct {
    grid_x, grid_y: int, // Tọa độ trên lưới
    pixel_x, pixel_y: f32, // Tọa độ thật trên màn hình để vẽ
}

// Component Vẻ Ngoài (Để vẽ)
Renderable :: struct {
    tex_id: TextureID,
    color: rl.Color,
}

// Thế giới chứa mọi thứ (World)
World :: struct {
    positions:   [100]Position,     // Chứa tối đa 100 cái vị trí
    renderables: [100]Renderable,   // Chứa tối đa 100 cái hình ảnh
    
    // Cờ đánh dấu Entity nào có component nào
    mask_position:   [100]bool, 
    mask_renderable: [100]bool,
    
    // Đánh dấu đây là Người chơi (để nhận phím)
    mask_player:     [100]bool, 
    
    next_entity_id:  int,
}
```

## 2. Tạo Thực Thể (Entity)
Thực thể (Entity) chỉ là một con số ID. Khi bạn nhét `Position` vào ID số 0, nó thành một vật có tọa độ. Nhét thêm `Renderable` vào ID số 0, nó thành một vật có hình dáng!

```odin
create_player :: proc(world: ^World, start_grid_x: int, start_grid_y: int) {
    id := world.next_entity_id
    world.next_entity_id += 1
    
    // Gắn Component Position
    world.positions[id] = Position {
        grid_x = start_grid_x, 
        grid_y = start_grid_y,
        // Dịch tọa độ lưới sang tọa độ pixel
        pixel_x = f32(start_grid_x * TILE_SIZE), 
        pixel_y = f32(start_grid_y * TILE_SIZE),
    }
    world.mask_position[id] = true
    
    // Gắn Component Vẽ (Hình vuông đỏ)
    world.renderables[id] = Renderable {
        tex_id = .PLAYER,
        color = rl.WHITE,
    }
    world.mask_renderable[id] = true
    
    // Đánh dấu đây là nhân vật điều khiển được
    world.mask_player[id] = true
}
```

## 3. Hệ Thống Vẽ (Render System)
System (Hệ thống) là các **HÀM (Functions)** chuyên đi quét mảng dữ liệu để xử lý.

```odin
render_system :: proc(world: ^World) {
    for i := 0; i < world.next_entity_id; i += 1 {
        // Nếu Thực thể số [i] có cả Vị trí VÀ Hình ảnh, ta mới vẽ nó
        if world.mask_position[i] && world.mask_renderable[i] {
            pos := world.positions[i]
            ren := world.renderables[i]
            
            // Vẽ ở vị trí pixel_x, pixel_y. 
            // Cộng thêm offset (TILE_SIZE-48)/2 để nhân vật đứng chính giữa ô đất.
            offset := f32(TILE_SIZE - 48) / 2.0
            rl.DrawTexture(textures[ren.tex_id], i32(pos.pixel_x + offset), i32(pos.pixel_y + offset), ren.color)
        }
    }
}
```

## 4. Ráp vào main()

```odin
main :: proc() {
    // ... Khởi tạo Window và Texture ...
    
    // Khởi tạo World
    game_world := World{}
    create_player(&game_world, 2, 2) // Sinh người chơi ở ô (x=2, y=2)
    
    for !rl.WindowShouldClose() {
        dt := rl.GetFrameTime()
        // ... (Update Menu)
        
        rl.BeginDrawing()
        
        switch current_state {
        case .TITLE_SCREEN:
            // ...
        case .PLAYING:
            rl.ClearBackground(rl.BLACK)
            
            // 1. Vẽ Tilemap (Đã viết ở bài 2)
            // ... (Vòng lặp for vẽ map_data) ...
            
            // 2. Gọi Hệ thống Vẽ Nhân vật
            render_system(&game_world)
            
        }
        rl.EndDrawing()
    }
}
```

Chạy thử `odin run .`. Bạn sẽ thấy một hình vuông màu Đỏ (Nhân vật) đứng chễm chệ ngay ngắn trên luống đất số `(2,2)`. 

ECS thật ra rất đơn giản đúng không? Dữ liệu riêng, Hàm xử lý riêng. Giờ ta chuẩn bị cấp quyền Di Chuyển cho nó ở **Bài 4**.
