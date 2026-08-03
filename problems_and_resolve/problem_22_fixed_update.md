# Vấn Đề 22: Vật lý giật cục (Fixed Update vs Variable Update)

**Vấn đề:**
Nhân vật rơi tự do xuống đất. Dù FPS game của bạn đang rất cao (144FPS), chuyển động rơi của nhân vật nhìn vẫn cứ giật giật, không đều đặn mượt mà.

**Nguyên nhân:**
Khung hình hiển thị (FPS) không bao giờ ổn định tuyệt đối (lúc 144, lúc 140, lúc 145). `Delta Time` luôn biến động. 
Nhưng các công thức Vật lý (Ma sát, Gia tốc, Trọng lực) cực kỳ nhạy cảm với sự biến động này. Nếu tính Vật lý bằng `dt` biến động, sai số cộng dồn sẽ tạo ra sự rung giật.

**Giải pháp (Fixed Timestep):**
Tách biệt `UpdateLogic` (Vật lý) ra khỏi vòng lặp `Draw` (Hình ảnh).
Ép `UpdateLogic` chạy cố định với 1 khoảng thời gian không đổi (Ví dụ: 0.016s = 60 lần/giây), bất kể máy mạnh hay yếu. Nếu máy mạnh vẽ được 144 khung hình, nó cứ việc vẽ nội suy (Lerp) giữa 2 khung vật lý.

```odin
FIXED_DT :: 1.0 / 60.0
accumulator: f32 = 0.0

for !rl.WindowShouldClose() {
    dt := rl.GetFrameTime()
    accumulator += dt
    
    // Nếu máy yếu (dt lớn), vòng lặp này sẽ chạy nhiều lần để Vật lý đuổi kịp thời gian thực
    for accumulator >= FIXED_DT {
        update_physics(FIXED_DT)
        accumulator -= FIXED_DT
    }
    
    // Máy mạnh cứ việc vẽ thoải mái
    rl.BeginDrawing()
        draw_game()
    rl.EndDrawing()
}
```
