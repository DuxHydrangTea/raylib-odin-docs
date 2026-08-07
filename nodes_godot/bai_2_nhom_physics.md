# Bài 2: Nhóm Vật Lý & Va Chạm (Physics)

Godot tích hợp sẵn Physics Engine 2D vô cùng mạnh mẽ, xử lý ma sát, trọng lực và dội ngược (Bouncing).

## 1. 3 Anh em nhà Body

- **`StaticBody2D` (Tĩnh)**: Vật thể không bao giờ nhúc nhích dù bị ai đâm vào. Dùng làm mặt đất, tường, vách núi. Tốc độ xử lý của nó là nhanh nhất.
- **`RigidBody2D` (Cứng)**: Vật thể hoàn toàn giao phó sinh mạng cho Vật lý. Bạn không code `position` cho nó, mà bạn ném nó bằng lệnh `apply_central_impulse()`. Rất hợp làm Thùng gỗ bị đẩy, Viên bi lăn hay game Angry Birds.
- **`CharacterBody2D` (Động)**: Do con người (hoặc AI) điều khiển. Nó có hàm `move_and_slide()` thần thánh tự động trượt dọc theo mặt tường khi đâm vào mà không bị kẹt.

## 2. Area2D & CollisionShapes

- **`Area2D`**: Vùng không gian "tàng hình". Nó không cản đường ai cả, nó chỉ la lên (phát Signal) khi có người đi xuyên qua nó. Dùng làm Bẫy, Trạm dịch chuyển, Vùng rớt đồ.
- **`CollisionShape2D`**: Đây là cái lõi (cục xương) BẮT BUỘC phải có bên trong Body hoặc Area2D để xác định hình dáng (Vuông, Tròn, Capsule).

## 3. Thực hành: Bắn tia Laser bằng RayCast2D

`RayCast2D` bắn ra một tia laser để dò xem có đụng ai không. Nó sinh ra để làm cơ chế bắn súng (Hitscan) hoặc Mắt của quái vật.

### 🐍 GDScript
```gdscript
extends RayCast2D

func _physics_process(_delta):
	# Dùng phím Space để bắn laser
	if Input.is_action_just_pressed("ui_accept"):
		# Ép tia laser cập nhật kết quả ngay lập tức
		force_raycast_update()
		
		# Kiểm tra xem tia laser có đụng vật cản nào không
		if is_colliding():
			var target = get_collider()
			print("Laser trúng vào: ", target.name)
			
			# Lấy Tọa độ va chạm
			var hit_point = get_collision_point()
			print("Tọa độ nổ đốm lửa: ", hit_point)
			
			# Nếu vật đó có hàm take_damage thì gọi
			if target.has_method("take_damage"):
				target.take_damage(10)
```

### 🔷 C#
```csharp
using Godot;

public partial class LaserRaycast : RayCast2D
{
    public override void _PhysicsProcess(double delta)
    {
        if (Input.IsActionJustPressed("ui_accept"))
        {
            ForceRaycastUpdate();

            if (IsColliding())
            {
                Node target = (Node)GetCollider();
                GD.Print("Laser trúng vào: ", target.Name);

                Vector2 hitPoint = GetCollisionPoint();
                GD.Print("Tọa độ nổ đốm lửa: ", hitPoint);

                if (target.HasMethod("take_damage"))
                {
                    target.Call("take_damage", 10);
                }
            }
        }
    }
}
```

> [!WARNING]
> Luôn nhớ gọi `force_raycast_update()` trước khi kiểm tra `is_colliding()`. Vì mặc định RayCast2D chỉ tự động update 1 lần sau mỗi khung hình Vật lý, nếu không ép cập nhật, tia laser có thể bị chậm đi 1 frame gây ra lỗi "bắn hụt ảo".
