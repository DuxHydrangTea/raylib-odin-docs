# Bài 13: AI Động vật (Chăn nuôi Gà)

Sau khi Gà con nở ra, nó phải biết tự đi loanh quanh, đòi ăn và đẻ trứng. Chúng ta sẽ viết một State Machine (Máy trạng thái) đơn giản để quản lý AI của bầy Gà.

## 1. State Machine của Gà

Con Gà có 3 trạng thái chính:
1. **IDLE** (Đứng im thở, kêu lắt nhắt).
2. **WANDER** (Tự động chọn 1 hướng và đi dạo trong 2 giây).
3. **EAT** (Phát hiện thức ăn và cúi mổ).

### 🐍 GDScript (`Chicken.gd`)
Sử dụng `CharacterBody2D` kết hợp với `Timer` để quyết định khi nào đổi trạng thái.

```gdscript
extends CharacterBody2D

enum State { IDLE, WANDER, EAT }
var current_state = State.IDLE

@export var speed: float = 20.0
var move_direction = Vector2.ZERO

@onready var state_timer = $StateTimer # Hẹn giờ chuyển trạng thái
@onready var anim = $AnimatedSprite2D

func _ready():
	pick_new_state()

func pick_new_state():
	# Random giữa IDLE và WANDER
	if randf() > 0.5:
		current_state = State.WANDER
		# Random một hướng đi bất kỳ (Hàm rotated xoay ngẫu nhiên 360 độ)
		move_direction = Vector2.RIGHT.rotated(randf() * TAU)
		anim.play("walk")
	else:
		current_state = State.IDLE
		move_direction = Vector2.ZERO
		anim.play("idle")
		
	# Random thời gian duy trì trạng thái này (từ 1 đến 3 giây)
	state_timer.start(randf_range(1.0, 3.0))

# Hàm này gọi khi StateTimer đếm ngược xong
func _on_state_timer_timeout():
	pick_new_state()

func _physics_process(_delta):
	if current_state == State.WANDER:
		velocity = move_direction * speed
		move_and_slide()
		
		# Lật ảnh Gà quay trái/phải
		if velocity.x > 0: anim.flip_h = false
		elif velocity.x < 0: anim.flip_h = true
```

## 2. Hệ thống Đẻ trứng & Tình cảm (Happiness)

Mỗi ngày, con Gà chỉ đẻ trứng NẾU nó được ăn cỏ vào ngày hôm trước. 

1. Cấp cho con Gà một biến `is_fed = false`.
2. Khi Gà chạm vào "Khay thức ăn" (RayCast2D hoặc Area2D), nó sẽ chuyển state sang `EAT` và đánh dấu `is_fed = true`.
3. Lắng nghe `day_changed`:

```gdscript
func _ready():
	TimeManager.day_changed.connect(_on_day_changed)
	
func _on_day_changed(_day):
	if is_fed:
		lay_egg()
		is_fed = false # Reset bụng đói cho ngày mới
	else:
		# Giảm thanh tình cảm (Trái tim) nếu bị bỏ đói
		happiness -= 1

func lay_egg():
	var egg = preload("res://Egg.tscn").instantiate()
	egg.global_position = global_position # Rớt ngay dưới chân
	get_parent().add_child(egg)
```

### 🔷 C#
Code C# cho AI WANDER:
```csharp
using Godot;

public partial class Chicken : CharacterBody2D
{
    private enum State { Idle, Wander, Eat }
    private State _currentState = State.Idle;
    
    private Vector2 _moveDirection = Vector2.Zero;
    [Export] public float Speed = 20.0f;

    public void PickNewState()
    {
        if (GD.Randf() > 0.5f)
        {
            _currentState = State.Wander;
            // Xoay vector bằng toán học
            float randomAngle = (float)GD.Randf() * Mathf.Tau;
            _moveDirection = Vector2.Right.Rotated(randomAngle);
        }
        else
        {
            _currentState = State.Idle;
            _moveDirection = Vector2.Zero;
        }
    }

    public override void _PhysicsProcess(double delta)
    {
        if (_currentState == State.Wander)
        {
            Velocity = _moveDirection * Speed;
            MoveAndSlide();
        }
    }
}
```

> [!NOTE]
> Hàm `Vector2.RIGHT.rotated(randf() * TAU)` là kỹ thuật cực kỳ điêu luyện trong 2D. `TAU` chính là 360 độ (2 PI). Nó lấy một mũi tên chỉ về bên phải, và quay mũi tên đó ngẫu nhiên tạo thành góc đi 360 độ cực mượt.
