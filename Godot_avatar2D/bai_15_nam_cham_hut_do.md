# Bài 15: Cơ chế Rớt đồ & Nam châm hút (Magnet)

Khi chặt đổ một cái cây, thay vì Gỗ nhảy thẳng vào túi đồ (rất nhàm chán), ta sẽ làm cho miếng Gỗ văng ra ngoài bãi cỏ. Sau đó, nếu người chơi bước lại gần, miếng Gỗ sẽ tự động bay vèo về phía người chơi như bị Nam châm hút.

## 1. Thiết kế Item rơi (Dropped Item)

Tạo một Scene mới `DroppedItem.tscn` (Kế thừa từ `RigidBody2D` hoặc `CharacterBody2D`).
Ở đây ta dùng `CharacterBody2D` để dễ dàng điều khiển quỹ đạo bay tự chế bằng code.

Node gồm:
- `Sprite2D` (Hình ảnh miếng gỗ).
- `CollisionShape2D` (Vùng va chạm vật lý).
- `Area2D` tên là `MagnetArea` (Bán kính cảm biến, nếu Player lọt vào vùng này thì bắt đầu bị hút).

## 2. Hiệu ứng Văng ra lúc chặt (Pop-out)

Khi Cây bị chặt, nó đẻ ra `DroppedItem` và ném nhẹ nó lên trời.

### 🐍 GDScript (`Tree.gd`)
```gdscript
func chop_down():
	var wood = preload("res://DroppedItem.tscn").instantiate()
	wood.global_position = global_position
	
	# Cung cấp một lực văng ngẫu nhiên
	var random_x = randf_range(-100, 100)
	var random_y = randf_range(-150, -50) # Văng lên trên
	wood.velocity = Vector2(random_x, random_y)
	
	get_tree().current_scene.add_child(wood)
	queue_free() # Cây biến mất
```

## 3. Lực hút Nam châm (Magnet)

Bên trong script của `DroppedItem`, ta xử lý 2 việc:
- Chịu lực hấp dẫn rơi xuống đất.
- Hút về phía Player khi Player lọt vào `MagnetArea`.

### 🐍 GDScript (`DroppedItem.gd`)
```gdscript
extends CharacterBody2D

var gravity = 400
var is_magnetized = false
var target_player: Node2D

func _ready():
	$MagnetArea.body_entered.connect(_on_magnet_entered)
	$PickupArea.body_entered.connect(_on_pickup)

func _on_magnet_entered(body):
	if body.name == "Player":
		is_magnetized = true
		target_player = body

func _physics_process(delta):
	if is_magnetized and target_player:
		# Bay vèo vèo về phía Player (Hàm move_toward thần thánh)
		var direction = global_position.direction_to(target_player.global_position)
		# Càng gần bay càng nhanh (Tăng tốc)
		velocity = velocity.move_toward(direction * 400, 800 * delta)
	else:
		# Rơi tự do xuống đất và ma sát dừng lại
		if velocity.y < 0: # Đang văng lên
			velocity.y += gravity * delta
		else:
			# Rớt xuống đất thì dừng lại
			velocity = velocity.move_toward(Vector2.ZERO, 300 * delta)
			
	move_and_slide()

# Khi miếng Gỗ chạm hẳn vào bụng Player
func _on_pickup(body):
	if body.name == "Player":
		body.inventory.add_item("wood", 1)
		queue_free() # Biến mất
```

### 🔷 C#
Code C# cho hiệu ứng văng (Pop-out) của Cây:
```csharp
using Godot;

public partial class TreeObj : StaticBody2D
{
    private PackedScene _woodScene = GD.Load<PackedScene>("res://DroppedItem.tscn");

    public void ChopDown()
    {
        CharacterBody2D wood = _woodScene.Instantiate<CharacterBody2D>();
        wood.GlobalPosition = GlobalPosition;

        float randX = (float)GD.RandRange(-100, 100);
        float randY = (float)GD.RandRange(-150, -50);
        wood.Velocity = new Vector2(randX, randY);

        GetTree().CurrentScene.AddChild(wood);
        QueueFree();
    }
}
```

> [!NOTE]
> Hiệu ứng hút Nam châm này là bí quyết để giải phóng cảm giác "Thỏa mãn" (Satisfaction) của người chơi khi họ làm việc mệt mỏi và thu hoạch được một đống trái ngọt văng rải rác.
