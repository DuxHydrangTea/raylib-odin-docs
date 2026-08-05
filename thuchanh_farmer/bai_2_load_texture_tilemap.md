# Bài 2: Tải Ảnh Giả Lập & Xây Bản Đồ Lưới (Tilemap)

Để có một Nông trại, ta cần hình ảnh vạt cỏ, luống đất và nhân vật. Vì đây là bài thực hành code, ta sẽ không cần thiết kế một file ảnh `.png` thật. Ta sẽ **sinh ảnh giả lập** (Dummy Textures) bằng tính năng tạo ảnh từ màu sắc (Image generation) của Raylib. Cách này giúp bạn copy code chạy được ngay lập tức mà không lo bị lỗi "File not found"!

## 1. Khai báo hằng số và tạo Ảnh giả lập
Kế thừa file `main.odin` ở Bài 1, hãy thêm kích thước lưới (Tile) và định nghĩa các ID ảnh.

```odin
// Thêm lên trên cùng, ngay dưới SCREEN_HEIGHT
TILE_SIZE :: 64 // Mỗi ô đất có cạnh 64 pixel

TextureID :: enum {
    PLAYER,
    GRASS,
    DIRT,
    WATERED_DIRT,
    PLANT_SEED,
    PLANT_GROWN,
}

// Bảng từ điển lưu trữ toàn bộ hình ảnh của game
textures: map[TextureID]rl.Texture2D

// Hàm sinh ảnh giả (Chỉ dùng cho mục đích học code)
init_dummy_textures :: proc() {
    // Nhân vật: Hình vuông màu Đỏ
    img_player := rl.GenImageColor(48, 48, rl.RED)
    textures[.PLAYER] = rl.LoadTextureFromImage(img_player)
    rl.UnloadImage(img_player)

    // Cỏ xanh lá
    img_grass := rl.GenImageColor(TILE_SIZE, TILE_SIZE, rl.LIME)
    textures[.GRASS] = rl.LoadTextureFromImage(img_grass)
    rl.UnloadImage(img_grass)

    // Đất tơi xốp (Màu nâu sáng)
    img_dirt := rl.GenImageColor(TILE_SIZE, TILE_SIZE, rl.BROWN)
    textures[.DIRT] = rl.LoadTextureFromImage(img_dirt)
    rl.UnloadImage(img_dirt)
    
    // Đất đã tưới nước (Nâu sẫm)
    img_watered := rl.GenImageColor(TILE_SIZE, TILE_SIZE, rl.DARKBROWN)
    textures[.WATERED_DIRT] = rl.LoadTextureFromImage(img_watered)
    rl.UnloadImage(img_watered)
}
```

## 2. Thiết kế Bản Đồ (Tilemap)
Thay vì load file Tiled phức tạp, ta tạo một bản đồ tĩnh `10x10` dạng mảng 2D cho dễ quản lý.

```odin
MAP_WIDTH  :: 10
MAP_HEIGHT :: 10

// 0 là cỏ, 1 là đất trống (có thể cuốc)
map_data: [MAP_HEIGHT][MAP_WIDTH]int = {
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 1, 1, 1, 0, 0, 1, 1, 1, 0},
    {0, 1, 1, 1, 0, 0, 1, 1, 1, 0},
    {0, 1, 1, 1, 0, 0, 1, 1, 1, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 1, 1, 1, 1, 1, 1, 1, 1, 0},
    {0, 1, 1, 1, 1, 1, 1, 1, 1, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
}
```

## 3. Tích hợp vào main()
Giờ ta nhúng 2 hàm trên vào Vòng lặp.

```odin
main :: proc() {
    rl.InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Nông Trại 2D")
    defer rl.CloseWindow()
    rl.SetTargetFPS(60)

    // Khởi tạo Textures ngay sau khi InitWindow
    init_dummy_textures()

    for !rl.WindowShouldClose() {
        
        // ... (phần Update State giữ nguyên như bài 1) ...

        rl.BeginDrawing()
        
        switch current_state {
        case .TITLE_SCREEN:
            rl.ClearBackground(rl.DARKBLUE)
            rl.DrawText("Nhan ENTER de bat dau", 250, 300, 20, rl.WHITE)
            
        case .PLAYING:
            rl.ClearBackground(rl.BLACK) // Xóa phông

            // --- VẼ BẢN ĐỒ ---
            for row := 0; row < MAP_HEIGHT; row += 1 {
                for col := 0; col < MAP_WIDTH; col += 1 {
                    tile_id := map_data[row][col]
                    
                    // Tính tọa độ pixel X, Y trên màn hình
                    px := i32(col * TILE_SIZE)
                    py := i32(row * TILE_SIZE)
                    
                    if tile_id == 0 { // Cỏ
                        rl.DrawTexture(textures[.GRASS], px, py, rl.WHITE)
                    } else if tile_id == 1 { // Đất có thể trồng
                        rl.DrawTexture(textures[.DIRT], px, py, rl.WHITE)
                    }
                }
            }
            // ------------------

            rl.DrawText("Nhan B de ra Menu", 10, 10, 20, rl.BLACK)
        }

        rl.EndDrawing()
    }
}
```

Chạy lệnh `odin run .` rồi bấm Enter vào game. Bạn sẽ thấy một màn hình tuyệt đẹp với các luống đất màu nâu sếp hàng ngay ngắn giữa thảm cỏ xanh. 

Bước tiếp theo ở **Bài 3**: Ta sẽ ném Nhân vật màu đỏ vào màn hình bằng cấu trúc dữ liệu xịn xò có tên là ECS!
