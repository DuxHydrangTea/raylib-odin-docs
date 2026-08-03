# Chương 6: Âm thanh và Lưu trữ (Save/Load)

Chúc mừng bạn đã đến với chương cuối cùng! Một tựa game không thể thiếu tiếng động (hiệu ứng, nhạc nền) và khả năng lưu lại thành quả chơi (Save game).

---

## 1. Hệ thống Âm thanh (Audio)

Trước khi gọi bất kỳ hàm âm thanh nào, bạn **BẮT BUỘC** phải đánh thức card âm thanh bằng hàm khởi tạo (thường để dưới `InitWindow`). Nếu bạn tải nhạc mà chưa gọi hàm này, game sẽ bị crash ngay lập tức.

```odin
rl.InitAudioDevice()
defer rl.CloseAudioDevice()
```

Raylib chia âm thanh ra làm 2 loại để tối ưu RAM: `Sound` (Hiệu ứng động ngắn) và `Music` (Nhạc nền dài).

### 1.1. Tiếng động ngắn (Sound)
Dùng cho tiếng nhảy, tiếng bắn súng, tiếng nhặt tiền.
* **`LoadSound(fileName: cstring) -> Sound`**: Tải file `.wav` hoặc `.ogg` vào RAM. Gọi ngoài vòng lặp. Nhớ `defer rl.UnloadSound(fx)`.
* **`PlaySound(sound: Sound)`**: Phát âm thanh một lần. Bạn có thể gọi liên tục, âm thanh sẽ tự trộn đè lên nhau.

```odin
if rl.IsKeyPressed(.SPACE) {
    rl.PlaySound(jump_sfx) // Tiếng nhảy
}
```

### 1.2. Nhạc nền (Music)
Dùng cho nhạc game vòng lặp dài. Thay vì tải toàn bộ bài nhạc 10MB vào RAM, Raylib sẽ "stream" (vừa đọc ổ cứng vừa phát).
* **`LoadMusicStream(fileName: cstring) -> Music`**: Tải nhạc dạng luồng (thường là file `.mp3` hoặc `.ogg`). Nhớ `defer rl.UnloadMusicStream(bgm)`.
* **`PlayMusicStream(music: Music)`**: Bắt đầu phát nhạc.
* **`UpdateMusicStream(music: Music)`**: **CỰC KỲ QUAN TRỌNG!** Bạn phải gọi hàm này TẠI MỖI KHUNG HÌNH (trong vòng lặp Update) để game liên tục nạp dữ liệu nhạc mới vào loa. Nếu thiếu hàm này, nhạc sẽ im lặng.

```odin
// (Bên ngoài vòng lặp)
bg_music := rl.LoadMusicStream("assets/music.mp3")
rl.PlayMusicStream(bg_music)
defer rl.UnloadMusicStream(bg_music)

// (Bên trong vòng lặp Game Loop)
for !rl.WindowShouldClose() {
    rl.UpdateMusicStream(bg_music) // <--- Phải có hàm này!
    // ...
}
```

---

## 2. Lưu trữ Hệ thống (Save / Load)

Để người chơi không phải chơi lại từ đầu mỗi khi tắt game, chúng ta cần ghi dữ liệu ra ổ cứng (file Save).

Raylib hỗ trợ các hàm đọc/ghi chuỗi C-String rất tiện lợi. Bạn có thể lưu dữ liệu dưới định dạng JSON, hoặc đơn giản nhất là 1 file `.txt`.

### 2.1. Đọc và Ghi File Text
* **`SaveFileText(fileName, text: cstring) -> bool`**
  * Tác dụng: Tạo file mới hoặc ghi đè lên file cũ toàn bộ chuỗi text bạn truyền vào.
* **`LoadFileText(fileName: cstring) -> cstring`**
  * Tác dụng: Đọc toàn bộ nội dung file `.txt` hoặc `.json` vào một C-String.
  * **Lưu ý:** Raylib đã cấp phát vùng nhớ cho chuỗi này. Khi dùng xong, bạn PHẢI tự gọi `rl.UnloadFileText(loaded_str)` để giải phóng RAM.

### 2.2. Kiểm tra File Tồn tại
* **`FileExists(fileName: cstring) -> bool`**
  * Tác dụng: Trước khi Load, hãy dùng hàm này kiểm tra xem người chơi đã có file Save chưa. Tránh lỗi đọc nhầm file không tồn tại.

### Ví dụ mô phỏng Lưu / Tải điểm số:
```odin
import "core:fmt"

save_path : cstring = "save_data.txt"

// LƯU GAME (Khi bấm phím S)
if rl.IsKeyPressed(.S) {
    // Ép kiểu điểm số thành chuỗi tạm thời
    save_str := fmt.ctprintf("%d", score) 
    if rl.SaveFileText(save_path, save_str) {
        rl.TraceLog(.INFO, "Đã lưu game thành công!")
    }
}

// TẢI GAME (Khi bấm phím L)
if rl.IsKeyPressed(.L) {
    if rl.FileExists(save_path) {
        // Đọc dữ liệu lên RAM
        loaded_str := rl.LoadFileText(save_path)
        defer rl.UnloadFileText(loaded_str) // Đừng quên dòng này
        
        // (Trong thực tế, bạn sẽ dùng thư viện strconv để chuyển chuỗi "1500" thành số integer)
        rl.TraceLog(.INFO, loaded_str)
    } else {
        rl.TraceLog(.WARNING, "Không tìm thấy file save!")
    }
}
```

*(Mẹo: Ngôn ngữ Odin hỗ trợ module `core:encoding/json` cực kì mạnh mẽ. Bạn có thể dùng module đó biến 1 Struct của Odin thành chuỗi JSON, sau đó ném cho `SaveFileText` của Raylib để ghi ra file một cách hoàn hảo).*

---

## Lời Kết & Bài tập thực hành Chương 6

1. Hãy tìm 1 file âm thanh tiếng bùm hoặc ting (`.wav`) và 1 bài nhạc nền (`.mp3`).
2. Khởi tạo `InitAudioDevice`.
3. Bật nhạc nền chạy liên tục trong vòng lặp bằng `PlayMusicStream` và `UpdateMusicStream`.
4. Viết code: Mỗi lần bấm chuột trái, phát tiếng `.wav` 1 lần (Dùng `PlaySound`).
5. (Thử thách cuối) Viết chức năng Tạm Dừng Game (Pause): Khi bấm phím `ESC` (nhớ đổi phím thoát mặc định bằng `rl.SetExitKey(.NONE)`), vòng lặp Update ngừng cập nhật di chuyển, đồng thời gọi `rl.PauseMusicStream()` để tạm dừng nhạc!

**Chúc mừng bạn đã hoàn thành khóa học 6 chương làm game 2D với Raylib và Odin! Bạn đã nắm giữ toàn bộ những công cụ mạnh mẽ nhất. Giờ là lúc thỏa sức sáng tạo và tạo ra tựa game của riêng mình!**
