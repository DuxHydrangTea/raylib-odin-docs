# Bài 5: Nhóm Tìm Đường (Navigation & AI)

Làm sao để một con Quái thú biết đường đi vòng qua bức tường để đuổi theo Player? Chào mừng đến với nghệ thuật Navigation (Điều hướng).

## 1. Trải thảm NavMesh (`NavigationRegion2D`)

Trước khi tìm đường, AI cần biết vùng nào CÓ THỂ đi được.
1. Thêm `NavigationRegion2D` vào màn chơi (thường làm Node cha của TileMapLayer).
2. Vẽ một Polygon2D bọc lại những khu vực mặt đất an toàn.
3. Trong Godot 4, bạn có thể tự động "Bake" (Nướng) NavMesh ngay trên TileMapLayer bằng cách cấu hình thuộc tính Navigation Layer ở trong bản thân viên Gạch (Tile).

## 2. Gắn AI Dẫn Đường (`NavigationAgent2D`)

Đây là cái GPS (Bản đồ điện tử) của quái vật. Kéo Node này thả làm con của con Quái (Enemy). 

Bạn cấp tọa độ của Player cho cái GPS này, nó sẽ trả về một chuỗi các "Điểm mốc" (Path) ngắn nhất uốn lượn né qua các bức tường.

## 3. Thực hành: AI Tự Động Rượt Đuổi

### 🐍 GDScript
Gắn vào `Enemy.gd` (Là một `CharacterBody2D`). Đảm bảo nó có con là `NavigationAgent2D`.

```gdscript
extends CharacterBody2D

@onready var nav_agent: NavigationAgent2D = $NavigationAgent2D
@export var speed: float = 150.0

# Biến lưu trữ mục tiêu (Player)
var target_node: Node2D

func _ready():
	# Giả sử Player có tên là "Player" nằm cùng nhóm cha
	target_node = get_parent().get_node("Player")

func _physics_process(delta):
	if target_node == null: return
	
	# Cập nhật mục tiêu liên tục cho GPS
	nav_agent.target_position = target_node.global_position
	
	# Đã đuổi tới nơi chưa?
	if nav_agent.is_navigation_finished():
		velocity = Vector2.ZERO
		move_and_slide()
		return
		
	# Lấy điểm mốc tiếp theo dọc theo con đường
	var next_path_position = nav_agent.get_next_path_position()
	
	# Tính hướng đi
	var direction = global_position.direction_to(next_path_position)
	
	# Di chuyển
	velocity = direction * speed
	move_and_slide()
```

### 🔷 C#
```csharp
using Godot;

public partial class AIEnemy : CharacterBody2D
{
    private NavigationAgent2D _navAgent;
    [Export] public float Speed = 150.0f;
    private Node2D _targetNode;

    public override void _Ready()
    {
        _navAgent = GetNode<NavigationAgent2D>("NavigationAgent2D");
        _targetNode = GetParent().GetNode<Node2D>("Player");
    }

    public override void _PhysicsProcess(double delta)
    {
        if (_targetNode == null) return;

        // Báo tọa độ đích
        _navAgent.TargetPosition = _targetNode.GlobalPosition;

        if (_navAgent.IsNavigationFinished())
        {
            Velocity = Vector2.Zero;
            MoveAndSlide();
            return;
        }

        Vector2 nextPathPos = _navAgent.GetNextPathPosition();
        Vector2 direction = GlobalPosition.DirectionTo(nextPathPos);

        Velocity = direction * Speed;
        MoveAndSlide();
    }
}
```

> [!NOTE]
> Khối lượng tính toán tìm đường (Pathfinding) là khá nặng. Hãy đặt một bộ định thời `Timer` để chỉ gọi `nav_agent.target_position = ...` khoảng **4 lần mỗi giây** (0.25s) thay vì liên tục 60 lần/giây ở `_physics_process`. Kẻ địch vẫn trông cực kỳ thông minh mà Game lại không bị tụt FPS!
