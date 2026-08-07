# Bài 3: Nhóm Ánh Sáng & Hiệu Ứng (VFX & Lighting)

Đồ họa 2D thường mang cảm giác "phẳng". Để game có chiều sâu và huyền ảo (Game AAA), hệ thống Ánh sáng 2D và Hạt (Particles) của Godot là vô giá.

## 1. Particle Systems (Hệ thống Hạt)

- **`GPUParticles2D`**: Xử lý bằng Card màn hình. Dùng khi bạn cần hàng ngàn hạt bay lung tung (Mưa, Bão tuyết). Vô cùng mượt.
- **`CPUParticles2D`**: Xử lý bằng Chip máy tính. Ít sức mạnh hơn nhưng hỗ trợ trên các dòng điện thoại cổ hoặc thiết bị cũ không có GPU xịn.
- *Thiết lập*: Gắn `ParticleProcessMaterial` vào ô Process Material. Chỉnh `Gravity`, `Scale`, `Color Ramp` (Đổi màu theo thời gian để làm lửa cháy từ Cam sang Khói đen).

## 2. Hệ thống Đánh Sáng 2D (Lighting)

- **`DirectionalLight2D`**: Ánh sáng song song (Mặt trời/Mặt trăng). Gắn 1 cái là sáng cả màn hình.
- **`PointLight2D`**: Ánh sáng tụ điểm (Đèn pin, ngọn đuốc). Cần cung cấp một bức ảnh Gradient (sáng ở tâm, mờ dần ra rìa) vào mục `Texture`.
- **`LightOccluder2D`**: Bóng đen cản sáng. Đặt nó ở bức tường. Khi PointLight2D đi ngang qua bức tường, bức tường sẽ đổ bóng dài ra đằng sau cực kỳ chân thực.

## 3. Thực hành: Làm hiệu ứng Đèn Pin chớp tắt

### 🐍 GDScript
```gdscript
extends PointLight2D

func _process(_delta):
	# Nhấn phím F để bật tắt đèn pin
	if Input.is_action_just_pressed("ui_focus_next"): # ui_focus_next thường là phím Tab hoặc gán phím F
		self.enabled = !self.enabled
		
	# Giả lập đèn pin bị chập điện (nháy sáng)
	if self.enabled:
		if randf() < 0.05: # 5% cơ hội bị nháy ở mỗi khung hình
			self.energy = randf_range(0.2, 1.5) # Độ sáng chập chờn
		else:
			self.energy = 1.0 # Sáng bình thường
```

### 🔷 C#
```csharp
using Godot;

public partial class Flashlight : PointLight2D
{
    public override void _Process(double delta)
    {
        // Bật tắt
        if (Input.IsActionJustPressed("ui_focus_next"))
        {
            Enabled = !Enabled;
        }

        // Chập điện chớp nháy
        if (Enabled)
        {
            if (GD.Randf() < 0.05f)
            {
                Energy = (float)GD.RandRange(0.2, 1.5);
            }
            else
            {
                Energy = 1.0f;
            }
        }
    }
}
```

> [!TIP]
> Việc dùng `PointLight2D` đi kèm với thuộc tính `energy` hoặc thuật toán Noise (Perlin Noise) sẽ tạo ra hiệu ứng ngọn lửa đang bập bùng vô cùng chân thực.
