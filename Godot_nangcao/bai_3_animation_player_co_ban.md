# Bài 3: Nhập Môn AnimationPlayer

Trong các bài trước, chúng ta chỉ thay ảnh tĩnh cho nhân vật. Để nhân vật vung cuốc hay đi bộ, chúng ta cần một tờ ảnh lớn chứa nhiều khung hình (SpriteSheet) và một "đạo diễn" là `AnimationPlayer`.

## 1. Thiết lập SpriteSheet
1. Bấm vào `Sprite2D` của Player, kéo tờ ảnh SpriteSheet vào mục Texture.
2. Ở mục **Animation** trong Inspector, đếm số cột (Hframes) và số dòng (Vframes) của tờ ảnh và điền vào. (Ví dụ: tờ ảnh 6 cột, 4 dòng).
3. Kéo thử mục `frame` từ 0 đến 23, bạn sẽ thấy nhân vật cử động!

## 2. Tạo Hoạt Ảnh (Animation)
1. Thêm Node `AnimationPlayer` vào làm con của Player.
2. Dưới cùng màn hình (khung Animation), ấn `Animation -> New` và đặt tên là `"walk_right"`.
3. Bấm hình chìa khóa 🔑 kế bên mục `frame` của Sprite2D để lưu khung hình số 0 ở giây 0.
4. Kéo thanh thời gian lên 0.1s, sửa `frame` thành 1, bấm 🔑 lưu lại. Cứ thế tạo thành một chuỗi hành động.
5. Đừng quên bấm biểu tượng **Vòng lặp (Looping)** để hoạt ảnh đi bộ được lặp lại mãi mãi!

## 3. Điều khiển bằng Code

Làm sao để gọi hoạt ảnh đi bộ khi nhấn phím mũi tên phải?

### 🐍 GDScript
```gdscript
extends CharacterBody2D

@onready var anim_player: AnimationPlayer = $AnimationPlayer

func _process(delta):
	# ... logic di chuyển (bỏ qua để code gọn) ...
	var velocity = Vector2.RIGHT # Giả sử đang đi sang phải
	
	if velocity.x > 0:
		anim_player.play("walk_right")
	elif velocity.x < 0:
		anim_player.play("walk_left")
	elif velocity.y > 0:
		anim_player.play("walk_down")
	elif velocity.y < 0:
		anim_player.play("walk_up")
	else:
		anim_player.play("idle")
```

### 🔷 C#
```csharp
using Godot;

public partial class Player : CharacterBody2D
{
    private AnimationPlayer _animPlayer;

    public override void _Ready()
    {
        _animPlayer = GetNode<AnimationPlayer>("AnimationPlayer");
    }

    public override void _Process(double delta)
    {
        Vector2 velocity = Vector2.Right; // Lấy từ input

        if (velocity.X > 0) _animPlayer.Play("walk_right");
        else if (velocity.X < 0) _animPlayer.Play("walk_left");
        else if (velocity.Y > 0) _animPlayer.Play("walk_down");
        else if (velocity.Y < 0) _animPlayer.Play("walk_up");
        else _animPlayer.Play("idle");
    }
}
```

> [!WARNING]
> Nhìn đoạn `if / else` 4 hướng bên trên bạn có thấy mệt mỏi không? Nếu thêm hoạt ảnh chạy (run_left, run_right) và tấn công (attack_up, attack_down) thì mớ `if/else` này sẽ phình to thành một thảm họa! 
> Ở bài tiếp theo, chúng ta sẽ làm quen với `AnimationTree` để giải quyết triệt để cục tạ này.
