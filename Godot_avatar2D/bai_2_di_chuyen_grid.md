# Bài 2: Di chuyển theo Ô (Grid-based Movement)

Game nông trại cổ điển (như Avatar 2D, Harvest Moon) thường có cơ chế di chuyển đặc trưng: Nhân vật không lướt tự do mà sẽ **bước từng bước vừa khít vào các ô đất (Grid)**. 

## 1. Thuật toán Di chuyển Grid-based
- Nếu nhân vật đang đứng im, và người chơi bấm phím mũi tên.
- Tính toán tọa độ đích (Đích = Tọa độ hiện tại + Kích thước 1 ô).
- Bắt đầu trượt nhân vật về hướng Đích.
- TRONG QUÁ TRÌNH TRƯỢT, KHÔNG NHẬN THÊM LỆNH PHÍM (để tránh đi lệch ô).

## 2. Triển khai Code (Player Script)

### 🐍 GDScript
```gdscript
extends CharacterBody2D

const GRID_SIZE: int = 32
@export var speed: float = 150.0

var target_position: Vector2
var is_moving: bool = false

func _ready():
	position = position.snapped(Vector2(GRID_SIZE, GRID_SIZE))
	target_position = position

func _process(delta: float):
	if is_moving:
		# Lướt từ từ đến đích
		position = position.move_toward(target_position, speed * delta)
		
		# Đã đến đích chưa?
		if position == target_position:
			is_moving = false
	else:
		# Đang đứng im, chờ lệnh phím mới
		var direction := Vector2.ZERO
		
		if Input.is_action_pressed("ui_right"):
			direction = Vector2.RIGHT
		elif Input.is_action_pressed("ui_left"):
			direction = Vector2.LEFT
		elif Input.is_action_pressed("ui_down"):
			direction = Vector2.DOWN
		elif Input.is_action_pressed("ui_up"):
			direction = Vector2.UP
			
		# Nếu có bấm phím, tính toán đích đến mới
		if direction != Vector2.ZERO:
			target_position = position + (direction * GRID_SIZE)
			is_moving = true
```

### 🔷 C#
```csharp
using Godot;

public partial class Player : CharacterBody2D
{
    public const int GridSize = 32;
    [Export] public float Speed = 150.0f;

    private Vector2 _targetPosition;
    private bool _isMoving = false;

    public override void _Ready()
    {
        Position = Position.Snapped(new Vector2(GridSize, GridSize));
        _targetPosition = Position;
    }

    public override void _Process(double delta)
    {
        if (_isMoving)
        {
            // Lướt từ từ đến đích
            Position = Position.MoveToward(_targetPosition, (float)(Speed * delta));

            // Đã đến nơi
            if (Position == _targetPosition)
            {
                _isMoving = false;
            }
        }
        else
        {
            Vector2 direction = Vector2.Zero;

            if (Input.IsActionPressed("ui_right")) direction = Vector2.Right;
            else if (Input.IsActionPressed("ui_left")) direction = Vector2.Left;
            else if (Input.IsActionPressed("ui_down")) direction = Vector2.Down;
            else if (Input.IsActionPressed("ui_up")) direction = Vector2.Up;

            if (direction != Vector2.Zero)
            {
                _targetPosition = Position + (direction * GridSize);
                _isMoving = true;
            }
        }
    }
}
```

> [!TIP]
> Hàm `move_toward()` cực kỳ an toàn. Nó đảm bảo nhân vật sẽ dừng LẠI CHÍNH XÁC ở tọa độ đích mà không bao giờ bị trượt quá đà (overshoot). 

Tuyệt vời! Giờ nhân vật của bạn đã di chuyển giật cục từng ô vuông y hệt Avatar 2D!
