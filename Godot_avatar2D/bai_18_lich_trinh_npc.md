# Bài 18: Lịch Trình NPC (NPC Schedule)

Dân làng trong game nông trại không đứng im một chỗ như tượng gỗ. Họ có thời gian biểu (Schedule). Ví dụ:
- 8h00: Đi từ Nhà ra Quảng trường.
- 13h00: Đi từ Quảng trường ra Bãi biển.
- 18h00: Về nhà ngủ.

## 1. Thiết lập Điểm đến (Waypoints)

Ở trên Bản đồ, ta rải các `Marker2D` và đặt tên cho chúng: `Point_Square` (Quảng trường), `Point_Beach` (Bãi biển), `Point_Home` (Nhà).

Cung cấp cho NPC một cái **Từ điển Thời gian biểu (Dictionary)**.

### 🐍 GDScript (`NPC_Schedule.gd`)
```gdscript
extends CharacterBody2D

# GPS để tìm đường né chướng ngại vật
@onready var nav_agent = $NavigationAgent2D

# Khai báo Lịch trình: Khóa (Key) là Giờ, Giá trị (Value) là Tên điểm đến
var schedule = {
	8: "Point_Square",
	13: "Point_Beach",
	18: "Point_Home"
}

var current_target_node: Node2D = null
var speed = 80.0

func _ready():
	# Lắng nghe thời gian trôi qua mỗi giờ
	TimeManager.minute_changed.connect(_on_time_changed)

func _on_time_changed(hour: int, _minute: int):
	# Nếu giờ hiện tại có trong Lịch trình
	if schedule.has(hour):
		var target_name = schedule[hour]
		
		# Tìm Node Marker2D trên bản đồ thông qua Group "Waypoints"
		var waypoints = get_tree().get_nodes_in_group("Waypoints")
		for wp in waypoints:
			if wp.name == target_name:
				current_target_node = wp
				nav_agent.target_position = current_target_node.global_position
				print(name, " đang đi đến: ", target_name)
				break
```

## 2. Xử lý Di chuyển Bằng NavigationAgent2D

Bây giờ NPC đã biết Tọa độ đích, ta chỉ việc dùng hàm Tìm đường để nó tự đi đến đó.

### 🐍 GDScript
```gdscript
func _physics_process(_delta):
	# Nếu chưa có đích đến, đứng im
	if current_target_node == null: return
	
	# Nếu đã đến nơi
	if nav_agent.is_navigation_finished():
		current_target_node = null # Ngừng đi
		$AnimatedSprite2D.play("idle")
		return
		
	# Lấy tọa độ tiếp theo trên con đường
	var next_path_pos = nav_agent.get_next_path_position()
	var direction = global_position.direction_to(next_path_pos)
	
	velocity = direction * speed
	move_and_slide()
	
	# Phát hoạt ảnh đi bộ
	$AnimatedSprite2D.play("walk")
	if velocity.x > 0: $AnimatedSprite2D.flip_h = false
	elif velocity.x < 0: $AnimatedSprite2D.flip_h = true
```

### 🔷 C#
Code C# kiểm tra lịch trình (Giả sử bạn dùng Dictionary của C#):
```csharp
using Godot;
using System.Collections.Generic;

public partial class NPCSchedule : CharacterBody2D
{
    private NavigationAgent2D _navAgent;
    private Node2D _currentTargetNode = null;
    public float Speed = 80.0f;

    private Dictionary<int, string> _schedule = new Dictionary<int, string>()
    {
        { 8, "Point_Square" },
        { 13, "Point_Beach" },
        { 18, "Point_Home" }
    };

    public void OnTimeChanged(int hour, int minute)
    {
        if (_schedule.ContainsKey(hour))
        {
            string targetName = _schedule[hour];
            var waypoints = GetTree().GetNodesInGroup("Waypoints");
            foreach (Node2D wp in waypoints)
            {
                if (wp.Name == targetName)
                {
                    _currentTargetNode = wp;
                    _navAgent.TargetPosition = _currentTargetNode.GlobalPosition;
                    break;
                }
            }
        }
    }
}
```

> [!WARNING]
> Bản đồ (TileMap) của bạn BẮT BUỘC phải được cấu hình `Navigation Layer` cho các phần Đất trống thì `NavigationAgent2D` mới có thể dò đường đi được. Nếu không có NavigationMesh, NPC sẽ đứng im hoặc đâm đầu vào tường!
