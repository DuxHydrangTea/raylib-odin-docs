# Vấn Đề 24: Kẹt trong vòng lặp vô tận (Async Hell / Dialogue)

**Vấn đề:**
Bạn muốn NPC nói chuyện với người chơi: Chữ hiện ra từ từ từng chữ cái một trong 2 giây. Bạn viết một vòng `for` + `sleep` để hiện chữ. BÙM! Game bị đơ (Not Responding) hoàn toàn, nhân vật đứng im trong 2 giây đó.

**Nguyên nhân:**
Vòng lặp chính của game cần phải liên tục quay (tối thiểu 60 lần/s) để làm mới hình ảnh. Nếu bạn dùng lệnh `sleep()` hoặc vòng `while` kẹt cứng, GPU sẽ bị bỏ đói và Hệ điều hành tưởng game đã bị treo.

**Giải pháp:**
Không bao giờ dùng vòng lặp chặn đứng (Blocking). Thay vào đó, dùng **Bộ đếm thời gian (Timers)**. Cứ mỗi khung hình, cộng dồn `dt`. Đủ thời gian thì hiện thêm 1 chữ cái.

```odin
dialogue_text := "Xin chào dũng sĩ!"
char_index: int = 0
timer: f32 = 0.0
char_delay: f32 = 0.1 // Hiện 1 chữ mất 0.1s

update_dialogue :: proc(dt: f32) {
    if char_index < len(dialogue_text) {
        timer += dt
        if timer >= char_delay {
            timer = 0
            char_index += 1
        }
    }
    
    // Lấy chuỗi con từ 0 đến char_index
    visible_text := dialogue_text[0:char_index]
    rl.DrawText(visible_text, 10, 10, 20, rl.WHITE)
}
// Vì không có while/sleep, Game Loop vẫn trôi chảy và nhạc nền vẫn chạy!
```
