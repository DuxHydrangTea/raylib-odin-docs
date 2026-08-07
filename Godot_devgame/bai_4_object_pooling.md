# Bài 4: Object Pooling (Tối ưu Bộ nhớ)

Một trong những sai lầm phổ biến nhất khiến game của người mới bị giật lag (stutter/FPS drop) là liên tục sử dụng hàm `instantiate()` và `queue_free()` (Sinh đạn và Xóa đạn liên tục). Việc xin cấp phát và giải phóng RAM liên tục là một thao tác rất tốn kém (Garbage Collection).

Kỹ thuật **Object Pooling (Hồ chứa Object)** sẽ giải quyết triệt để vấn đề này.

## 1. Nguyên lý Object Pooling
- Khi khởi động game, bạn dùng `instantiate()` để tạo sẵn một mảng gồm **50 viên đạn**. Ban đầu, ẩn tất cả đi (`hide()`) và tắt va chạm.
- Khi bắn, bạn lấy 1 viên đạn bị ẩn ra, bật nó lên (`show()`) và đặt vị trí ở nòng súng.
- Khi viên đạn trúng đích hoặc bay ra khỏi màn hình, **KHÔNG ĐƯỢC DÙNG `queue_free()`**. Bạn chỉ việc ẩn nó đi và đưa nó về lại "hồ chứa" để chờ lần bắn tiếp theo tái sử dụng.

## 2. Triển khai Cơ bản

### 🐍 GDScript
```gdscript
extends Node2D

var bullet_scene = preload("res://Bullet.tscn")
var pool_size: int = 50
var bullets_pool: Array = []

func _ready():
	# Khởi tạo Pool
	for i in range(pool_size):
		var b = bullet_scene.instantiate()
		b.hide() # Ẩn đi
		b.set_process(false) # Tắt process để tối ưu
		add_child(b)
		bullets_pool.append(b)

func get_bullet() -> Node2D:
	for b in bullets_pool:
		if not b.visible: # Tìm viên đạn nào đang nghỉ ngơi
			b.show()
			b.set_process(true)
			return b
	return null # Hết đạn trong hồ

# Khi bắn
func shoot():
	var b = get_bullet()
	if b:
		b.global_position = $GunPosition.global_position
```

### 🔷 C#
Trong C#, ta có thể dùng cấu trúc `Queue` (Hàng đợi) hoặc `List` để quản lý Pool chuyên nghiệp và an toàn kiểu dữ liệu hơn.

```csharp
using Godot;
using System.Collections.Generic;

public partial class BulletPool : Node2D
{
    private PackedScene _bulletScene = GD.Load<PackedScene>("res://Bullet.tscn");
    private List<Node2D> _bulletsPool = new List<Node2D>();
    private int _poolSize = 50;

    public override void _Ready()
    {
        for (int i = 0; i < _poolSize; i++)
        {
            Node2D b = _bulletScene.Instantiate<Node2D>();
            b.Hide();
            b.SetProcess(false);
            AddChild(b);
            _bulletsPool.Add(b);
        }
    }

    public Node2D GetBullet()
    {
        foreach (var b in _bulletsPool)
        {
            if (!b.Visible)
            {
                b.Show();
                b.SetProcess(true);
                return b;
            }
        }
        return null;
    }
}
```

> [!IMPORTANT]
> Lưu ý trong Script của viên đạn (`Bullet.gd`), khi trúng tường hoặc hết thời gian sống, bạn phải gọi `hide()` và `set_process(false)` THAY VÌ gọi `queue_free()`!
