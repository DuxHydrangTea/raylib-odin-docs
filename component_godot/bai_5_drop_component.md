# Bài 5: Drop Component (Loot rớt đồ)

Khi một con Slime chết, ta muốn nó rớt ra 1 Đồng Vàng, hoặc đôi khi may mắn rớt ra 1 Lọ Máu. Thuật toán để chọn ngẫu nhiên này được gọi là **Loot Table** hay hiểu nôm na là Cò quay Gacha. Ta gói nó vào `DropComponent`.

## 1. Dữ liệu Gacha (Export Array)
`DropComponent` cần chứa một danh sách (Mảng) các Scene vật phẩm (Vàng, Máu). Nó sẽ lắng nghe tín hiệu `died` từ `HealthComponent` và tự động đẻ (Instantiate) vật phẩm ra ngoài màn hình.

### 🐍 GDScript
```gdscript
extends Node
class_name DropComponent

# Mảng chứa các Scene vật phẩm có thể rớt
@export var item_scenes: Array[PackedScene] = []
# Tỉ lệ rớt đồ (0.0 đến 1.0)
@export var drop_chance: float = 0.5 

@export var health_component: HealthComponent

func _ready():
	if health_component:
		health_component.died.connect(_on_died)

func _on_died():
	# Kiểm tra nhân phẩm (Ví dụ drop_chance = 0.5 tức là 50% rớt đồ)
	if randf() > drop_chance:
		return
		
	if item_scenes.size() == 0:
		return
		
	# Chọn ngẫu nhiên 1 món đồ trong mảng
	var random_index = randi() % item_scenes.size()
	var item_to_drop = item_scenes[random_index].instantiate()
	
	# Lấy Node cha (Ví dụ: con Slime) để biết tọa độ rớt
	var owner_node = get_parent() as Node2D
	
	# Để vật phẩm rớt lại trên bản đồ thay vì bị xóa theo con Slime, 
	# ta phải ném nó ra ngoài hệ thống quản lý của Enemy, thường là thả vào Main root.
	item_to_drop.global_position = owner_node.global_position
	get_tree().current_scene.add_child.call_deferred(item_to_drop)
```

### 🔷 C#
```csharp
using Godot;

[GlobalClass]
public partial class DropComponent : Node
{
    [Export] public Godot.Collections.Array<PackedScene> ItemScenes = new();
    [Export] public float DropChance = 0.5f;
    [Export] public HealthComponent HealthComponent;

    public override void _Ready()
    {
        if (HealthComponent != null)
        {
            HealthComponent.Died += OnDied;
        }
    }

    private void OnDied()
    {
        if (GD.Randf() > DropChance || ItemScenes.Count == 0)
        {
            return;
        }

        int randomIndex = GD.RandRange(0, ItemScenes.Count - 1);
        Node2D itemToDrop = ItemScenes[randomIndex].Instantiate<Node2D>();

        Node2D ownerNode = GetParent<Node2D>();
        itemToDrop.GlobalPosition = ownerNode.GlobalPosition;

        // Thả vật phẩm vào root của Scene thay vì giữ trong con quái
        GetTree().CurrentScene.CallDeferred(Node.MethodName.AddChild, itemToDrop);
    }
}
```

> [!WARNING]
> Hàm `call_deferred` ("Gọi Trì Hoãn") rất quan trọng khi xử lý chết chóc. Khi `health_component.died` được gọi, Engine vật lý (Physics) có thể vẫn đang bận dọn dẹp bộ nhớ của con Slime. Dùng `call_deferred` để báo cho Godot biết: "Khi nào dọn dẹp xong xuôi thì hẵng AddChild cái Item này vào nhé", tránh gây lỗi Crash Game.

**TỔNG KẾT**: Thư viện Component của chúng ta đã có 5 mảnh ghép (Health, Hit/Hurtbox, Velocity, Audio, Drop). Bạn có thể tái sử dụng chúng mãi mãi về sau cho mọi dự án!
