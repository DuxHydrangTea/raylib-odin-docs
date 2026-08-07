# Bài 5: Nhóm Hàm Dò Tìm (RayCast2D & Area2D)

Đây là các giác quan (Mắt, Xúc giác) của thực thể. 

## 1. Dò tìm diện rộng (Area2D)

Area2D là một cái máy quét radar.

- **`get_overlapping_bodies()`**: Mở lưới quét, chộp lấy toàn bộ các Node Body đang dẫm lên Area2D.
- **Trả về**: Mảng `Array` (GDScript) hoặc `Godot.Collections.Array<Node2D>` (C#).

#### 🐍 GDScript
```gdscript
@onready var bom_area = $BombArea2D

func no_bom():
	var nan_nhan = bom_area.get_overlapping_bodies()
	for muc_tieu in nan_nhan:
		if muc_tieu.has_method("take_damage"):
			muc_tieu.take_damage(50)
```

#### 🔷 C#
```csharp
using Godot;

public void NoBom()
{
    var nanNhan = _bombArea2D.GetOverlappingBodies();
    foreach (Node2D mucTieu in nanNhan)
    {
        if (mucTieu.HasMethod("take_damage"))
        {
            mucTieu.Call("take_damage", 50);
        }
    }
}
```

## 2. Dò tìm Laze chỉ hướng (RayCast2D)

- **`force_raycast_update()`**: Mặc định tia laze chỉ cập nhật 1 lần mỗi khung hình (frame). Nếu bạn xoay nòng súng và muốn check kết quả ngay-lập-tức trong dòng code kế tiếp, BẮT BUỘC phải gọi hàm này.
- **`is_colliding()`**: Tia laze có bị vật gì chặn lại không? (Trả về `bool`).
- **`get_collider()`**: Lấy cái Node (thực thể) vừa chặn tia laze lại (Để gọi hàm trừ máu). Trả về `Object`.
- **`get_collision_point()`**: Lấy vị trí Không gian (Global Position) chính xác tại điểm laser đập vào tường. Dùng để dán tấm decal Vết Đạn lên tường.

#### 🐍 GDScript
```gdscript
@onready var raycast = $RayCast2D

func ban_sung():
	raycast.force_raycast_update()
	
	if raycast.is_colliding():
		var ke_dich = raycast.get_collider()
		print("Trúng: ", ke_dich.name)
		
		# Nổ hiệu ứng tia lửa tại điểm va chạm
		var toa_do_trung = raycast.get_collision_point()
		spawn_spark(toa_do_trung)
```

#### 🔷 C#
```csharp
using Godot;

public void BanSung()
{
    _raycast.ForceRaycastUpdate();
    
    if (_raycast.IsColliding())
    {
        Node keDich = (Node)_raycast.GetCollider();
        GD.Print("Trúng: ", keDich.Name);
        
        Vector2 toaDoTrung = _raycast.GetCollisionPoint();
        SpawnSpark(toaDoTrung);
    }
}
```

> [!TIP]
> Kết hợp `RayCast2D` với hàm `look_at(player.global_position)`, bạn sẽ tạo ra một tháp pháo trụ (Turret) tự động quay nòng theo Player và bắn ra những tia laze chết chóc!
