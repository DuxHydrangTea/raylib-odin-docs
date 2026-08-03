# Vấn Đề 1: Y-Sorting (Sắp xếp theo trục Y)

**Vấn đề:** 
Nhân vật đứng phía sau cái cây, nhưng hình ảnh nhân vật lại bị vẽ đè lên trên ngọn cây. Điều này phá vỡ luật xa-gần trong không gian 2.5D.

**Nguyên nhân:**
Lệnh vẽ nào gọi sau sẽ đè lên lệnh vẽ gọi trước (Thuật toán họa sĩ - Painter's Algorithm). Nếu bạn vẽ cái cây trước, rồi mới vẽ nhân vật, nhân vật sẽ luôn đè lên cái cây bất kể tọa độ.

**Giải pháp:**
Không gọi lệnh vẽ (`DrawTexture`) ngay lập tức trong vòng lặp. 
Thay vào đó, tạo một danh sách (Array) chứa TẤT CẢ các vật thể cần vẽ (cây, đá, nhân vật, quái vật) kèm theo tọa độ Y của chúng (đáy của vật thể). Sau đó **sắp xếp (Sort)** mảng này theo tọa độ Y từ bé đến lớn. Cuối cùng mới lặp qua mảng đã sắp xếp để vẽ.

```odin
import "core:slice"

// Định nghĩa cấu trúc
RenderItem :: struct {
    tex: rl.Texture2D,
    pos: rl.Vector2,
    y_sort_anchor: f32, // Tọa độ Y ở dưới chân vật thể
}

// ... Trong Game Loop
items_to_draw: [dynamic]RenderItem
// Thêm nhân vật, cây cỏ vào items_to_draw...

// Sắp xếp mảng theo y_sort_anchor (Odin có sẵn hàm slice.sort_by)
slice.sort_by(items_to_draw[:], proc(i, j: RenderItem) -> bool {
    return i.y_sort_anchor < j.y_sort_anchor
})

// Tiến hành vẽ
for item in items_to_draw {
    rl.DrawTextureV(item.tex, item.pos, rl.WHITE)
}
```
