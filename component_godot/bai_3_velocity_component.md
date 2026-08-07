# Bài 3: Velocity Component (Thành phần Vật lý)

Việc viết tính toán Gia tốc (Acceleration) và Lực ma sát (Friction) vào thẳng script của Player khiến file đó dài ngoằng. Hơn nữa, con quái (Enemy) cũng cần đi bộ giống y hệt, nên ta sẽ tách toàn bộ mảng Vật lý này ra thành `VelocityComponent`.

## 1. Thiết kế VelocityComponent
Component này sẽ nhận **Vectơ hướng (Input Direction)** từ Player, sau đó tự động nội suy dần dần để đạt Vận tốc tối đa (Gia tốc), và trượt dần về 0 khi ngừng bấm phím (Ma sát). Cuối cùng nó gọi hàm `move_and_slide()` cho CharacterBody2D.

## 2. Triển khai Code

### 🐍 GDScript
Tạo `VelocityComponent.gd` kế thừa `Node`.

```gdscript
extends Node
class_name VelocityComponent

@export var max_speed: float = 200.0
@export var acceleration: float = 800.0
@export var friction: float = 1000.0

# Node cha (CharacterBody2D) mà Component này sẽ di chuyển
var body: CharacterBody2D

func _ready():
	# Lấy cha của Node này
	body = get_parent() as CharacterBody2D
	assert(body != null, "VelocityComponent phải là con của CharacterBody2D!")

# Hàm này sẽ được Player gọi trong _physics_process
func accelerate_to_velocity(direction: Vector2, delta: float):
	if direction != Vector2.ZERO:
		# Có hướng đi -> Tăng tốc
		body.velocity = body.velocity.move_toward(direction * max_speed, acceleration * delta)
	else:
		# Không bấm phím -> Ma sát kéo về 0
		body.velocity = body.velocity.move_toward(Vector2.ZERO, friction * delta)
		
	# Di chuyển thực thể
	body.move_and_slide()
```

### 🔷 C#
Tạo `VelocityComponent.cs`.

```csharp
using Godot;

[GlobalClass]
public partial class VelocityComponent : Node
{
    [Export] public float MaxSpeed = 200.0f;
    [Export] public float Acceleration = 800.0f;
    [Export] public float Friction = 1000.0f;

    private CharacterBody2D _body;

    public override void _Ready()
    {
        _body = GetParent() as CharacterBody2D;
        if (_body == null)
        {
            GD.PrintErr("VelocityComponent must be a child of CharacterBody2D!");
        }
    }

    public void AccelerateToVelocity(Vector2 direction, double delta)
    {
        float fDelta = (float)delta;
        
        if (direction != Vector2.Zero)
        {
            _body.Velocity = _body.Velocity.MoveToward(direction * MaxSpeed, Acceleration * fDelta);
        }
        else
        {
            _body.Velocity = _body.Velocity.MoveToward(Vector2.Zero, Friction * fDelta);
        }

        _body.MoveAndSlide();
    }
}
```

## 3. Cách sử dụng bên trong Player

Bây giờ script của `Player` sẽ ngắn và sạch đẹp đến không ngờ!

```gdscript
extends CharacterBody2D

@onready var velocity_component: VelocityComponent = $VelocityComponent

func _physics_process(delta):
	# Chỉ quan tâm đến việc lấy Input
	var direction = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	
	# Đẩy việc xử lý vật lý nặng nhọc cho Component lo!
	velocity_component.accelerate_to_velocity(direction, delta)
```

> [!TIP]
> Đây là kiến trúc **Component-based** đích thực. `Player.gd` giờ đây chỉ đóng vai trò như "Bộ não" đưa ra quyết định (Input). Còn "Đôi chân" thực hiện lệnh di chuyển chính là `VelocityComponent`.
