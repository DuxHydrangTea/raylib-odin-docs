# Vấn Đề 13: Âm thanh bị chồng chéo (Audio Overlapping)

**Vấn đề:**
Người chơi ném một quả lựu đạn tiêu diệt cùng lúc 10 con quái vật. Tiếng quái vật chết (`Oargh!`) phát lên 10 lần cùng một mili-giây, âm lượng khuếch đại gấp 10 lần làm vỡ màng nhĩ người chơi và làm rè loa (Audio Clipping).

**Nguyên nhân:**
Mỗi tiếng động là một sóng âm (Wave). Khi nhiều sóng âm giống hệt nhau phát đồng thời, biên độ của chúng cộng gộp lại (Tăng Volume đột biến), vượt qua mức giới hạn xử lý của thiết bị âm thanh.

**Giải pháp:**
Giới hạn số lượng âm thanh cùng loại được phép phát lên cùng lúc (Audio Throttling) hoặc thay đổi Pitch (Độ cao).

```odin
last_death_sound_time: f32 = 0.0

play_death_sound :: proc() {
    current_time := f32(rl.GetTime())
    
    // Giải pháp 1: Nếu tiếng chết vừa phát cách đây chưa tới 0.1 giây, bỏ qua!
    if current_time - last_death_sound_time < 0.1 {
        return 
    }
    
    // Giải pháp 2: Thay đổi độ cao (Pitch) ngẫu nhiên để các sóng âm không trùng khớp hoàn toàn
    rl.SetSoundPitch(death_snd, f32(rl.GetRandomValue(80, 120)) / 100.0) 
    
    rl.PlaySound(death_snd)
    last_death_sound_time = current_time
}
```
