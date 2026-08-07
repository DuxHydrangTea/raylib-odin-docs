# Bài 5: State Machine trong AnimationTree

Ở bài trước, ta đã giải quyết vấn đề "Đi 4 hướng" bằng BlendSpace2D. Nhưng còn các hành động khác thì sao? Ví dụ: Đứng im (Idle), Cuốc đất (Hoe).
Làm sao để khi Đứng im bấm Space thì chuyển sang Cuốc đất, cuốc xong thì TỰ ĐỘNG quay về Đứng im?

Godot cung cấp sẵn **AnimationNodeStateMachine** ngay bên trong AnimationTree.

## 1. Thiết lập State Machine (FSM)
1. Ở Node `AnimationTree`, mục Tree Root, thay vì chọn `BlendSpace2D` luôn, hãy chọn `New AnimationNodeStateMachine`.
2. Mở cửa sổ đồ thị (graph) ra. Ở đây giống hệt một sơ đồ tư duy.
3. Chuột phải -> Add BlendSpace2D -> Đặt tên là `Idle`. Xếp 4 hướng đứng im vào (như bài 4).
4. Chuột phải -> Add BlendSpace2D -> Đặt tên là `Walk`. Xếp 4 hướng đi bộ vào.
5. Chuột phải -> Add BlendSpace2D -> Đặt tên là `Hoe`. Xếp 4 hướng cuốc đất vào.

## 2. Nối dây Chuyển đổi (Transitions)
- Dùng công cụ "Connect" (Nút nối dây) trên menu. Nối một mũi tên từ `Idle` sang `Walk`.
- Nối mũi tên từ `Walk` về `Idle`.
- Ở menu Inspector bên tay phải, khi nhấp vào mũi tên, bạn cài đặt điều kiện chuyển đổi (Ví dụ: Advance Condition). Nhưng cách dễ nhất là kích hoạt bằng Code thông qua lệnh **Travel**.

## 3. Điều khiển máy trạng thái bằng Travel

Lệnh `travel("TênTrạngThái")` sẽ bảo máy tự động tìm đường chạy từ trạng thái hiện tại sang trạng thái đích cực kỳ mượt mà.

### 🐍 GDScript
```gdscript
extends CharacterBody2D

@onready var anim_tree: AnimationTree = $AnimationTree
# Lấy ra công cụ điều khiển State Machine
@onready var state_machine = anim_tree.get("parameters/playback")

func _process(delta):
	var direction = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	
	if Input.is_action_just_pressed("ui_accept"):
		# Điểm hay nhất của Travel: Nó sẽ chạy hết animation Cuốc, sau đó 
		# (nếu bạn thiết lập nối dây Auto Advance về Idle) nó sẽ tự quay về Đứng im!
		state_machine.travel("Hoe")
		return
		
	if direction != Vector2.ZERO:
		# Gán hướng đi cho CẢ 3 BlendSpace
		anim_tree.set("parameters/Idle/blend_position", direction)
		anim_tree.set("parameters/Walk/blend_position", direction)
		anim_tree.set("parameters/Hoe/blend_position", direction)
		
		state_machine.travel("Walk")
	else:
		state_machine.travel("Idle")
```

### 🔷 C#
```csharp
using Godot;

public partial class Player : CharacterBody2D
{
    private AnimationTree _animTree;
    private AnimationNodeStateMachinePlayback _stateMachine;

    public override void _Ready()
    {
        _animTree = GetNode<AnimationTree>("AnimationTree");
        // Lấy bộ điều khiển Playback
        _stateMachine = (AnimationNodeStateMachinePlayback)_animTree.Get("parameters/playback");
    }

    public override void _Process(double delta)
    {
        Vector2 direction = Input.GetVector("ui_left", "ui_right", "ui_up", "ui_down");

        if (Input.IsActionJustPressed("ui_accept"))
        {
            _stateMachine.Travel("Hoe");
            return;
        }

        if (direction != Vector2.Zero)
        {
            _animTree.Set("parameters/Idle/blend_position", direction);
            _animTree.Set("parameters/Walk/blend_position", direction);
            _animTree.Set("parameters/Hoe/blend_position", direction);

            _stateMachine.Travel("Walk");
        }
        else
        {
            _stateMachine.Travel("Idle");
        }
    }
}
```

---
**LỜI KẾT**
Đến đây, bạn đã cầm trong tay một "Kho vũ khí" hoàn chỉnh để tạo ra bất kỳ tựa game 2D nào: Từ Cấu trúc code vững chắc, Hệ thống Quản lý Vòng đời, Vật lý, cho tới Hệ thống Giao diện và Hoạt ảnh nâng cao bậc nhất của Godot! Chúc bạn sớm ra mắt con game triệu đô của riêng mình!
