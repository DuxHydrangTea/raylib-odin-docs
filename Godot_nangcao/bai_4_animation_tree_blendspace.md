# Bài 4: Đỉnh cao AnimationTree (BlendSpace2D)

Để lập trình chuyển động cho game Top-down (Nông trại, Zelda, Pokemon...), nơi nhân vật có thể đi theo 4 hoặc 8 hướng, thay vì code một nùi `if/else`, các kỹ sư chuyên nghiệp sử dụng **BlendSpace2D** bên trong `AnimationTree`.

## 1. Khởi tạo AnimationTree
1. Đảm bảo bạn đã có sẵn 4 hoạt ảnh (walk_left, walk_right, walk_up, walk_down) trong `AnimationPlayer`.
2. Thêm Node `AnimationTree` làm con của Player.
3. Trong Inspector của AnimationTree, gán mục **Anim Player** trỏ về Node `AnimationPlayer`.
4. Mục **Tree Root**, chọn `New AnimationNodeBlendSpace2D`. Kích hoạt nút **Active** (On).

## 2. Thiết lập Biểu Đồ Không Gian (BlendSpace2D)
Bấm vào mục AnimationTree ở thanh dưới cùng:
- Bạn sẽ thấy một trục tọa độ XY giống môn Toán (X ngang, Y dọc).
- Trục X đại diện cho `Left (-1)` và `Right (1)`. Trục Y đại diện cho `Up (-1)` và `Down (1)`.
- Dùng công cụ Cây bút 🖊️ chấm 1 điểm ở vị trí `(1, 0)` -> Chọn hoạt ảnh `"walk_right"`.
- Chấm ở `(-1, 0)` -> Chọn `"walk_left"`.
- Chấm ở `(0, 1)` -> Chọn `"walk_down"`.
- Chấm ở `(0, -1)` -> Chọn `"walk_up"`.

Bây giờ, thay vì gọi `play("tên_hoạt_ảnh")`, ta chỉ cần gán **Vectơ di chuyển** vào hệ tọa độ này, cái cây (Tree) sẽ tự động chọn hoạt ảnh đúng hướng!

## 3. Code cực ngắn nhờ AnimationTree

### 🐍 GDScript
```gdscript
extends CharacterBody2D

@onready var anim_tree: AnimationTree = $AnimationTree

func _process(delta):
	# Lấy Vectơ hướng đi (ví dụ: (1,0) là đi sang phải)
	var direction = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	
	if direction != Vector2.ZERO:
		# TRUYỀN HƯỚNG VÀO TRONG BLENDSPACE
		# Cú pháp truy cập biến bên trong AnimationTree của Godot 4:
		anim_tree.set("parameters/blend_position", direction)
```

### 🔷 C#
```csharp
using Godot;

public partial class Player : CharacterBody2D
{
    private AnimationTree _animTree;

    public override void _Ready()
    {
        _animTree = GetNode<AnimationTree>("AnimationTree");
    }

    public override void _Process(double delta)
    {
        Vector2 direction = Input.GetVector("ui_left", "ui_right", "ui_up", "ui_down");
        
        if (direction != Vector2.Zero)
        {
            // Truyền Vector hướng vào BlendSpace
            _animTree.Set("parameters/blend_position", direction);
        }
    }
}
```

> [!TIP]
> Bạn thấy sự kỳ diệu chưa? Hàng chục dòng `if/else` giờ được gói gọn vào ĐÚNG MỘT DÒNG CODE DUY NHẤT `anim_tree.set()`. Đây chính là quyền năng của AnimationTree khiến Godot vượt trội hoàn toàn so với các engine 2D khác!
