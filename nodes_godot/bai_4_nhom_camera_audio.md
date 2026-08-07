# Bài 4: Nhóm Nghe - Nhìn (Camera & Audio)

Nhóm này kiểm soát những gì người chơi trực tiếp Nghe và Nhìn thấy trong game.

## 1. `Camera2D` (Khung máy quay)

Trong Godot, Camera cực kỳ dễ dùng. Bạn kéo nó làm con của `Player`, thế là màn hình tự động bám theo Player.
- **Drag Margin**: Mặc định Camera sẽ ghim Player cứng ngắc ở giữa màn. Bật Drag Margin lên, Player có thể chạy vòng vòng trong một khu vực nhỏ ở giữa mà Camera không bị di chuyển, giúp đỡ chóng mặt.
- **Position Smoothing**: Camera không đuổi theo Player ngay lập tức, mà trượt (slide) từ từ tới vị trí của Player. Mắt người sẽ thấy mượt hơn nhiều.
- **Limit**: Giới hạn tọa độ X, Y của Camera (Ví dụ: `Limit Left = 0`). Để Camera không bao giờ lia ra khỏi rìa bản đồ (lộ mảng đen).

## 2. `AudioStreamPlayer2D` (Âm thanh Không gian)

Khác với `AudioStreamPlayer` (thường dùng làm Nhạc nền BGM đập thẳng vào lỗ tai), con số `2D` ở đuôi có nghĩa là nó bị ảnh hưởng bởi Khoảng cách.
- **Max Distance**: Nếu Player đứng cách xa cái loa quá mức này, âm lượng = 0.
- Nó sẽ tự động tính toán Panning (Cân bằng loa Trái/Phải) dựa trên vị trí của Player so với cái Loa.

## 3. Thực hành: Thuật toán Rung Màn Hình (Camera Shake)

Khi có bom nổ hoặc Player dính đòn, làm rung màn hình là bí quyết tạo Game Feel.

### 🐍 GDScript
Tạo file `ShakeCamera.gd` gắn vào Camera2D.

```gdscript
extends Camera2D

var shake_strength: float = 0.0
var shake_fade: float = 5.0

func apply_shake(strength: float = 10.0):
	# Nhận lực rung (Càng to rung càng giật)
	shake_strength = strength

func _process(delta):
	if shake_strength > 0:
		# Giảm dần lực rung theo thời gian để màn hình êm trở lại
		shake_strength = lerp(shake_strength, 0.0, shake_fade * delta)
		
		# Tính độ lệch tọa độ (offset) ngẫu nhiên bằng randf_range
		var offset_x = randf_range(-shake_strength, shake_strength)
		var offset_y = randf_range(-shake_strength, shake_strength)
		
		self.offset = Vector2(offset_x, offset_y)
```

### 🔷 C#
```csharp
using Godot;

public partial class ShakeCamera : Camera2D
{
    private float _shakeStrength = 0.0f;
    private float _shakeFade = 5.0f;

    public void ApplyShake(float strength = 10.0f)
    {
        _shakeStrength = strength;
    }

    public override void _Process(double delta)
    {
        if (_shakeStrength > 0)
        {
            // Lerp giảm dần lực rung
            _shakeStrength = Mathf.Lerp(_shakeStrength, 0.0f, _shakeFade * (float)delta);

            // Tính Offset
            float offsetX = (float)GD.RandRange(-_shakeStrength, _shakeStrength);
            float offsetY = (float)GD.RandRange(-_shakeStrength, _shakeStrength);

            Offset = new Vector2(offsetX, offsetY);
        }
    }
}
```

Để sử dụng, khi Boss dậm chân ngầm, bạn gọi `camera.apply_shake(20.0)`. Màn hình sẽ rung bần bật và êm dần sau nửa giây.
