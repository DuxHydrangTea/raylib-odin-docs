# Bài 1: Nhóm Hình Ảnh (Visuals)

Nhóm Hình ảnh chịu trách nhiệm vẽ mọi thứ bạn nhìn thấy lên màn hình. Đứng đầu là `Sprite2D`.

## 1. Các Node Quan Trọng

- **`Sprite2D`**: Node cơ bản nhất để hiển thị một bức ảnh tĩnh.
- **`AnimatedSprite2D`**: Dùng cho tờ ảnh SpriteSheet. Khác với việc kết hợp `Sprite2D` + `AnimationPlayer` (thích hợp làm các chuyển động phức tạp kèm va chạm), `AnimatedSprite2D` rất nhẹ và dễ cài đặt, thường dùng cho các vật thể nền như Ngọn lửa đang cháy, Đồng xu lấp lánh.
- **`Line2D`**: Vẽ đường thẳng/đường cong nối tiếp nhau thông qua mảng tọa độ `points`. Rất thích hợp làm dây thừng hoặc quỹ đạo đạn.
- **`Parallax2D`**: (Godot 4.3) Tạo phông nền cuộn. Bằng cách điều chỉnh thông số `scroll_scale`, bạn có thể làm mây trôi chậm hơn mặt đất, tạo ảo giác 3D.

## 2. Thực hành: Đổi màu Sprite ngẫu nhiên

Đôi khi bạn muốn tái sử dụng một bức ảnh con Slime màu xanh lá, nhưng muốn đẻ ra cả Slime Đỏ và Vàng. Ta dùng thuộc tính `modulate`.

### 🐍 GDScript
```gdscript
extends Sprite2D

func _ready():
	# Hàm randomize() đảm bảo hạt giống (seed) ngẫu nhiên mỗi lần chạy game
	randomize()
	
	# Tạo một màu ngẫu nhiên (R, G, B) từ 0.0 đến 1.0
	var random_color = Color(randf(), randf(), randf())
	
	# Đổi màu (Modulate) đè lên ảnh gốc
	self.modulate = random_color
```

### 🔷 C#
```csharp
using Godot;

public partial class RandomColorSprite : Sprite2D
{
    public override void _Ready()
    {
        // Khởi tạo màu ngẫu nhiên (RGB)
        float r = (float)GD.Randf();
        float g = (float)GD.Randf();
        float b = (float)GD.Randf();
        
        // Gán màu vào Modulate
        Modulate = new Color(r, g, b);
    }
}
```

> [!TIP]
> Thuộc tính `modulate` sẽ áp dụng màu đè lên toàn bộ Node con của nó. Nếu bạn chỉ muốn đổi màu riêng Node này mà không ảnh hưởng Node con, hãy dùng `self_modulate`.
