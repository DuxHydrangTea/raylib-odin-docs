# Bài 2: Nhóm Hàm Toán học Vector2

Game 2D là bản lề của Toán Vector. Nếu bạn không giỏi Toán, đừng lo, các hàm Helper của struct `Vector2` sẽ tính Cosin, Sin và Pytago thay cho bạn!

## 1. `distance_to(to)`
Tính khoảng cách ngắn nhất (đường thẳng) giữa 2 tọa độ.

- **Tham số**: Tọa độ đích `Vector2`.
- **Trả về**: `float` (Khoảng cách tính bằng Pixel).

#### Song ngữ
```gdscript
# GDScript
var dist = player_pos.distance_to(boss_pos)
```
```csharp
// C#
float dist = playerPos.DistanceTo(bossPos);
```

## 2. `direction_to(to)`
Lấy vectơ hướng chỉ thẳng từ Điểm A tới Điểm B. Vectơ này đã được "Chuẩn hóa" (Độ dài ép về đúng 1.0). Cực kỳ quan trọng để tính hướng bay của viên đạn.

- **Tham số**: Tọa độ đích `Vector2`.
- **Trả về**: `Vector2` (Hướng đi).

#### Song ngữ
```gdscript
# GDScript
var dir = global_position.direction_to(mouse_pos)
velocity = dir * speed
```
```csharp
// C#
Vector2 dir = GlobalPosition.DirectionTo(mousePos);
Velocity = dir * speed;
```

## 3. `move_toward(to, delta)`
Tiến dần đều từ Tọa độ hiện tại tới Tọa độ đích bằng một bước nhảy (delta). Đây là thuật toán tuyệt đỉnh để làm **Gia tốc (Acceleration)** và **Ma sát (Friction)**.

- **Tham số 1**: Tọa độ đích `Vector2`.
- **Tham số 2**: Bước nhảy tối đa `float`.
- **Trả về**: `Vector2` (Tọa độ mới sau khi đã nhích lên một chút).

#### Song ngữ
```gdscript
# GDScript: Dùng để phanh xe (Ma sát)
velocity = velocity.move_toward(Vector2.ZERO, friction * delta)
```
```csharp
// C#: Phanh xe
Velocity = Velocity.MoveToward(Vector2.Zero, friction * (float)delta);
```

## 4. `angle_to_point(to)`
Tính góc xoay để cái nòng súng chỉa thẳng vào mặt mục tiêu.

- **Tham số**: Tọa độ đích `Vector2`.
- **Trả về**: `float` (Góc quay tính bằng Radian).

#### Song ngữ
```gdscript
# GDScript
rotation = global_position.angle_to_point(mouse_pos)
```
```csharp
// C#
Rotation = GlobalPosition.AngleToPoint(mousePos);
```

## 5. `bounce(normal)`
Nảy bật (phản xạ). Khi viên bi đập vào tường, nó sẽ dội ra theo góc nào? Bạn đưa cho nó Vector vuông góc (Normal) của mặt tường, nó sẽ trả ra hướng dội ngược lại.

- **Tham số**: Vectơ pháp tuyến mặt phẳng `Vector2`.
- **Trả về**: `Vector2` (Hướng đi mới sau khi dội tường).

#### Song ngữ
```gdscript
# GDScript (Dùng chung với hàm move_and_collide ở Bài 1)
var collision = move_and_collide(velocity * delta)
if collision:
	# Lấy Vectơ vuông góc của mặt tường
	var wall_normal = collision.get_normal()
	# Tính hướng nảy bóng
	velocity = velocity.bounce(wall_normal)
```
```csharp
// C#
KinematicCollision2D collision = MoveAndCollide(Velocity * (float)delta);
if (collision != null)
{
    Vector2 wallNormal = collision.GetNormal();
    Velocity = Velocity.Bounce(wallNormal);
}
```
