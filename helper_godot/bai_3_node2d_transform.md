# Bài 3: Nhóm Hàm Tọa Độ Trực Quan (Node2D)

Đây là các hàm nằm ngay bên trong lớp `Node2D`, giúp bạn thao tác với Tọa độ (Position) và Không gian (Space) một cách trực quan nhất.

## 1. `look_at(point)`

Đây là phiên bản "tự động hóa" của hàm `angle_to_point()` ở bài trước. Thay vì tính góc rồi gán vào biến `rotation`, hàm này ép Node quay mặt chỉa thẳng vào Tọa độ đó ngay lập tức! (Mặc định trục X - mũi tên đỏ - được coi là mặt tiền).

- **Tham số**: Tọa độ cần nhìn `Vector2` (Phải là Tọa độ Toàn cục - Global Position).
- **Trả về**: Không có (`void`).

#### 🐍 GDScript
```gdscript
func _process(delta):
	# Tháp pháo quay nòng súng theo con trỏ chuột
	look_at(get_global_mouse_position())
```

#### 🔷 C#
```csharp
public override void _Process(double delta)
{
    LookAt(GetGlobalMousePosition());
}
```

## 2. `get_global_mouse_position()`

Lấy tọa độ thực tế của con trỏ chuột trên thế giới 2D. 
*Đừng bao giờ dùng `get_viewport().get_mouse_position()` cho game có màn hình cuộn theo Camera, vì hàm đó chỉ lấy vị trí chuột trên Màn hình máy tính chứ không tính đến việc Camera đã trôi đi bao xa!*

- **Tham số**: Không có.
- **Trả về**: `Vector2`.

## 3. Hệ Tọa Độ: `to_local()` và `to_global()`

Một trong những khái niệm nhức não nhất của Game Engine là Tọa độ Địa phương (Local) và Tọa độ Toàn cục (Global).
- **Global**: Tọa độ thật trên cả thế giới game.
- **Local**: Tọa độ tương đối so với Node Cha. Nếu Node cha ở vị trí (10, 10) và bạn đứng cách Node cha 2 bước, thì Local của bạn là (2,0) nhưng Global của bạn là (12, 10).

Hàm `to_local()` giúp dịch một Tọa độ Global về xem nó cách mình bao xa.

- **Tham số**: Tọa độ gốc `Vector2`.
- **Trả về**: `Vector2` tọa độ đã chuyển đổi.

#### 🐍 GDScript
```gdscript
func check_target(boss_global_pos: Vector2):
	# Tính xem Boss nằm ở đâu so với bản thân tôi
	var local_pos = to_local(boss_global_pos)
	
	if local_pos.x > 0:
		print("Boss đang ở bên Phải tôi!")
	else:
		print("Boss đang ở bên Trái tôi!")
```

#### 🔷 C#
```csharp
public void CheckTarget(Vector2 bossGlobalPos)
{
    Vector2 localPos = ToLocal(bossGlobalPos);
    
    if (localPos.X > 0) GD.Print("Phải");
    else GD.Print("Trái");
}
```

> [!TIP]
> Thuộc tính `global_position` là biến được dùng nhiều nhất. Mọi tính toán liên quan đến hướng đi, khoảng cách hay khởi tạo viên đạn, TẤT CẢ phải dùng `global_position`, tuyệt đối không dùng `position` (vì `position` chỉ là Local).
