# Bài 7: Nhóm Công Cụ Tiện Ích (Utilities)

Đây là những Node có công dụng rất đặc thù, hỗ trợ đắc lực cho lập trình viên giải quyết các tình huống khó nhằn.

## 1. `Marker2D` (Tọa độ Mốc)
Nó là một dấu chấm chữ thập tàng hình. Tác dụng duy nhất của nó là để lưu 1 tọa độ (Position).

**Ví dụ**: Khi nhân vật cầm súng bắn, bạn không biết tọa độ đầu nòng súng ở đâu. Bạn kéo 1 cái `Marker2D` đặt ngay đầu nòng súng.

```gdscript
@onready var muzzle_marker = $Weapon/MuzzleMarker

func fire():
	var bullet = bullet_scene.instantiate()
	
	# Đẻ viên đạn đúng chỗ nòng súng!
	bullet.global_position = muzzle_marker.global_position
	get_tree().current_scene.add_child(bullet)
```

## 2. `RemoteTransform2D` (Điều khiển từ xa)
Giả sử có một thanh Máu của Boss nằm ở giao diện UI (không liên quan gì đến Boss trên cây Node). Nếu muốn UI luôn trôi lơ lửng trên đầu Boss, ta dùng `RemoteTransform2D`.

- Thả `RemoteTransform2D` vào đầu Boss.
- Gắn biến Node Path trỏ thẳng tới thanh UI máu.
- Mặc kệ UI nằm ở đâu, khi Boss chạy, nó sẽ "ép" UI phải lấy tọa độ của nó! (Rất hữu ích để tránh việc Node con kế thừa sai tỉ lệ Scale của Node cha).

## 3. `VisibleOnScreenNotifier2D` (Cảm biến Màn hình)

Một khẩu súng liên thanh nhả ra 100 viên đạn. Viên đạn bay mãi bay mãi ra ngoài vũ trụ vô tận. Game của bạn sẽ hết RAM và sập (Crash). Ta cần xóa viên đạn khi nó rời khỏi Camera.

Thêm Node `VisibleOnScreenNotifier2D` vào viên đạn. Node này cung cấp Signal `screen_exited()`.

### 🐍 GDScript
```gdscript
extends Area2D

func _ready():
	# Nhớ nối dây tín hiệu từ Notifier sang script này
	$VisibleOnScreenNotifier2D.screen_exited.connect(_on_screen_exited)

func _on_screen_exited():
	# Ngay khi bay ra khỏi màn hình, tự sát để giải phóng RAM!
	queue_free()
```

### 🔷 C#
```csharp
using Godot;

public partial class Bullet : Area2D
{
    public override void _Ready()
    {
        var notifier = GetNode<VisibleOnScreenNotifier2D>("VisibleOnScreenNotifier2D");
        notifier.ScreenExited += OnScreenExited;
    }

    private void OnScreenExited()
    {
        // Giải phóng bộ nhớ
        QueueFree();
    }
}
```

---
**LỜI KẾT**
Vậy là bạn đã cầm trong tay "Từ điển" toàn tập về hệ sinh thái Node của Godot 2D!
Hãy nhớ: Đừng nhét tất cả vào code. Nếu Godot đã cung cấp sẵn một Node (như RayCast dò đường hay Timer đếm giờ), hãy dùng nó. Đó chính là triết lý Component của Godot!
