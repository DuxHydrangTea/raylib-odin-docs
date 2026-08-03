# Hướng dẫn Khởi động Dự án - 5 Bước Hoàn thiện

Tiếp nối 3 bước cấu hình ban đầu, chúng ta sẽ đi vào 5 bước còn lại để game thực sự chạy được, hiển thị hình ảnh và có vòng lặp sống. Đây là phần cốt lõi của mọi dự án!

---

## 4. Thiết lập FPS (Frames Per Second)

Nếu không khóa tốc độ khung hình, game sẽ chạy hết tốc lực làm CPU và GPU nóng lên không cần thiết.

* **`SetTargetFPS(60)`**: Giới hạn game chạy tối đa 60 khung hình/giây. Hàm này nên được gọi ngay sau khi khởi tạo Window và Audio.

```odin
// 4. Thiết lập FPS (rất quan trọng)
rl.SetTargetFPS(60)
```

---

## 5. Tải Tài nguyên (Load Resources)

Game không thể hấp dẫn nếu thiếu hình ảnh và âm thanh. Bước này là nơi bạn "mua nguyên vật liệu" trước khi xây nhà.

* Luôn gọi lệnh tải (`LoadTexture`, `LoadSound`) ở **ngoài** vòng lặp chính.
* **QUAN TRỌNG:** Phải có lệnh `defer rl.Unload...` đi liền ngay sau đó để giải phóng VRAM/RAM khi tắt game.

```odin
// 5. Tải Tài nguyên (Texture, Font, Sound)
// player_tex := rl.LoadTexture("assets/player.png")
// defer rl.UnloadTexture(player_tex)

// bg_music := rl.LoadMusicStream("assets/bgm.mp3")
// defer rl.UnloadMusicStream(bg_music)
```

---

## 6. Khởi tạo Biến Game (Game State)

Đây là nơi bạn khai báo máu, điểm số, và toạ độ ban đầu của nhân vật trước khi vòng lặp bắt đầu đếm.

```odin
// 6. Khởi tạo Biến Game
player_pos := rl.Vector2{WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2}
player_speed: f32 = 250.0
score: int = 0
```

---

## 7. Vòng lặp Game Chính (Game Loop)

Vòng lặp này sẽ chạy hàng chục lần mỗi giây cho đến khi người dùng nhấn nút tắt cửa sổ (`!rl.WindowShouldClose()`). Nó luôn được chia làm 2 giai đoạn tách biệt rõ ràng: **Cập nhật (Update)** và **Hiển thị (Draw)**.

```odin
// 7. Vòng lặp Game
for !rl.WindowShouldClose() {
    
    // ==========================================
    // A. GIAI ĐOẠN UPDATE (Cập nhật Logic)
    // ==========================================
    dt := rl.GetFrameTime() // Lấy thời gian Delta Time
    
    // (Xử lý input bàn phím, va chạm, chạy logic kẻ địch ở đây...)
    // rl.UpdateMusicStream(bg_music) // Nhớ update nhạc nếu có

    // ==========================================
    // B. GIAI ĐOẠN DRAW (Vẽ ra màn hình)
    // ==========================================
    rl.BeginDrawing()
        rl.ClearBackground(rl.RAYWHITE) // Quét sơn trắng xoá sạch hình cũ của frame trước
        
        // Vẽ nhân vật, bản đồ ở đây...
        rl.DrawRectangleV(player_pos, {50, 50}, rl.BLUE)
        
        // Vẽ chữ (UI)
        rl.DrawFPS(10, 10)
    rl.EndDrawing()
    
    // ... (Bước 8 sẽ nằm ở dưới EndDrawing)
}
```

---

## 8. Dọn dẹp bộ nhớ tạm (Đặc thù của Odin)

Trong Odin, để ghép các chuỗi chữ và số lại với nhau (ví dụ: in ra `"Điểm: 100"`), chúng ta thường dùng hàm `fmt.ctprintf` (hàm này cấp phát một chuỗi mới trên vùng nhớ tạm `temp_allocator`). 
Nếu không giải phóng vùng nhớ tạm này, sau khoảng vài giây hoặc vài phút chơi game, RAM của bạn sẽ bị "phình to" và game bị văng (Memory Leak)!

```odin
    // ... (Tiếp nối phía dưới rl.EndDrawing() của bước 7) ...
    
    // 8. Dọn dẹp bộ nhớ tạm của vòng lặp hiện tại
    free_all(context.temp_allocator)
    
} // Kết thúc vòng lặp for
```

---

## Bài Tập Thực Hành Cuối Cùng

Bây giờ bạn hãy ghép toàn bộ 5 bước này vào bên dưới 3 bước mà bạn đã gõ ở file `main.odin` trước đó (Bạn có thể xóa vòng lặp tạm thời ở file cũ đi và thay bằng vòng lặp chuẩn chỉnh này). 

Sau khi ghép xong:
1. Chạy lệnh `odin run .` trong terminal.
2. Bạn sẽ thấy một cửa sổ màu trắng hiện ra, có bộ đếm FPS ổn định ở 60 góc trên cùng bên trái, và một hình vuông màu xanh lam ở giữa màn hình.
3. Mọi thứ vận hành trơn tru và không bị giật lag hay văng game.

**Chúc mừng bạn đã sở hữu 1 bộ khung (boilerplate) hoàn chỉnh, mạnh mẽ và an toàn nhất để bắt đầu lập trình bất kì dự án Game 2D nào bằng Raylib + Odin!**
