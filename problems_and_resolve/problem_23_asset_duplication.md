# Vấn Đề 23: Tràn VRAM vì trùng lặp Asset (Asset Duplication)

**Vấn đề:**
Bạn sinh ra 50 con Goblin trong rừng. Game đột ngột ngốn tới 2GB Card màn hình (VRAM) và FPS rớt thảm hại.

**Nguyên nhân:**
Mỗi con Goblin, bạn lại chạy lệnh `rl.LoadTexture("goblin.png")`. 
Tấm ảnh Goblin nặng 10MB, nhân cho 50 con là 500MB VRAM bị chiếm dụng lãng phí cho cùng một nội dung. Thẻ đồ họa phải load từng tấm ảnh một rất cồng kềnh.

**Giải pháp (Asset Manager / Flyweight Pattern):**
Chỉ tải tấm ảnh **một lần duy nhất** và chia sẻ (Share) biến `Texture2D` đó cho cả 50 con quái vật.

```odin
// Tải vào kho 1 lần duy nhất
AssetManager :: struct {
    goblin_tex: rl.Texture2D,
}
assets.goblin_tex = rl.LoadTexture("goblin.png")

// 50 con Goblin chỉ việc LẤY THAM CHIẾU (Pointer) từ kho
Goblin :: struct {
    pos: rl.Vector2,
    tex: ^rl.Texture2D, // Trỏ về bản gốc
}

for i in 0..<50 {
    spawn_goblin(x, y, &assets.goblin_tex)
}
```
*Lúc này, dù bạn đẻ ra 1 triệu con Goblin, VRAM bị tốn vẫn chỉ là 10MB.*
