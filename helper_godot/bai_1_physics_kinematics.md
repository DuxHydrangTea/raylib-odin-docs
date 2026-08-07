# Bài 1: Nhóm Hàm Di chuyển Vật lý

Nhóm hàm này là "Linh hồn" của Node `CharacterBody2D`. Nó giải quyết mọi vấn đề về va chạm tường, trượt dốc và leo bậc thang mà không cần bạn phải tự tính toán.

## 1. `move_and_slide()`

Hàm quyền lực nhất của Godot. Nó sẽ đọc giá trị từ biến `velocity` (vận tốc) của CharacterBody2D và tự động di chuyển nhân vật. Nếu đụng tường, nó sẽ trượt dọc theo mặt tường thay vì bị khựng lại.

- **Tham số**: Không có.
- **Trả về**: `bool` (Đúng nếu có xảy ra va chạm, Sai nếu không đụng ai).

#### 🐍 GDScript
```gdscript
func _physics_process(delta):
	velocity = Vector2(100, 0)
	var has_collided = move_and_slide()
```

#### 🔷 C#
```csharp
public override void _PhysicsProcess(double delta)
{
    Velocity = new Vector2(100, 0);
    bool hasCollided = MoveAndSlide();
}
```

## 2. `move_and_collide(velocity * delta)`

Khác với trượt, hàm này sẽ **Dừng lại ngay lập tức** khi đụng vào bất kỳ vật thể nào. Rất hay dùng cho Viên Đạn (Đụng tường thì nổ luôn chứ không trượt).

- **Tham số**: Một `Vector2` chứa độ dời (Thường là `vận tốc * delta`).
- **Trả về**: `KinematicCollision2D` (Một Object chứa toàn bộ thông tin về vụ va chạm, hoặc `null` nếu không đụng ai).

#### 🐍 GDScript
```gdscript
func _physics_process(delta):
	var collision = move_and_collide(velocity * delta)
	if collision:
		print("Đụng trúng: ", collision.get_collider().name)
```

#### 🔷 C#
```csharp
public override void _PhysicsProcess(double delta)
{
    KinematicCollision2D collision = MoveAndCollide(Velocity * (float)delta);
    if (collision != null)
    {
        Node collider = (Node)collision.GetCollider();
        GD.Print("Đụng trúng: ", collider.Name);
    }
}
```

## 3. Các hàm Check Trạng Thái
*Lưu ý: Các hàm này chỉ có tác dụng NGAY SAU KHI bạn vừa gọi hàm `move_and_slide()`.*

- **`is_on_floor()`**: Trả về `bool`. Nhân vật có đang dẫm lên mặt đất không? Rất quan trọng để check xem có được bấm phím Nhảy (Jump) không.
- **`is_on_wall()`**: Trả về `bool`. Nhân vật có đang kẹp vào tường không? Dùng làm cơ chế Bám tường (Wall Slide) hoặc Leo tường.
- **`is_on_ceiling()`**: Trả về `bool`. Đầu nhân vật có đang kẹt vào trần nhà không?

#### 🐍 GDScript
```gdscript
func _physics_process(delta):
	move_and_slide()
	
	if is_on_floor() and Input.is_action_just_pressed("jump"):
		velocity.y = -400 # Nhảy lên!
```

#### 🔷 C#
```csharp
public override void _PhysicsProcess(double delta)
{
    MoveAndSlide();
    
    if (IsOnFloor() && Input.IsActionJustPressed("jump"))
    {
        Vector2 vel = Velocity;
        vel.Y = -400; // Nhảy lên
        Velocity = vel;
    }
}
```

> [!WARNING]
> Trong C#, biến `Velocity` là một Struct `Vector2`. Bạn không thể gán trực tiếp `Velocity.Y = -400` như GDScript. Bạn phải tạo một biến `Vector2 vel` tạm thời, sửa nó, rồi gán đè lại vào `Velocity`!
