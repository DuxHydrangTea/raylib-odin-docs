# Bài 3: Tương tác Cuốc đất (Thay đổi TileMap bằng Code)

Khi nhân vật đứng trước một ô đất, bấm phím `Space` (Cuốc đất), làm sao để ô cỏ biến thành ô đất trồng trọt?
Chúng ta cần 2 công cụ:
1. **RayCast2D**: Đóng vai trò làm "mắt nhìn" để kiểm tra ô phía trước.
2. **TileMapLayer API**: Dùng hàm `set_cell()` để đổi hình ảnh viên gạch.

## 1. Mắt nhìn RayCast2D
- Chọn Node `Player`, thêm một con tên là `RayCast2D` (Tên: `InteractRaycast`).
- Kéo độ dài tia ray (Target Position) ngắn thôi, bằng đúng 1 ô (vd: `X: 0, Y: 32`).
- Mỗi khi nhân vật quay hướng nào, ta dùng code xoay tia RayCast về hướng đó.

## 2. Viết hàm Tương tác (Cuốc đất) - Chuẩn Clean Code

> [!TIP]
> **Tư duy đi làm (Professional):** Tránh xa **Magic Numbers** (Những con số vô tri). Khi gọi hàm `set_cell(grid_coords, 0, Vector2i(1, 0))`, số `0` và `Vector2i(1, 0)` là Magic Numbers. 6 tháng sau đọc lại code, bạn sẽ không nhớ `0` là cái gì. Thay vào đó, hãy khai báo chúng thành Hằng số (Constants).

### 🐍 GDScript
Giả sử chúng ta có 1 biến trỏ đến TileMap tên là `farm_layer`.

```gdscript
extends CharacterBody2D

# Khai báo Hằng số thay vì dùng Magic Numbers
const DIRT_TILE_ID: int = 0
const DIRT_ATLAS_COORD := Vector2i(1, 0)

# Tham chiếu tới tia nhìn và Bản đồ đất
@onready var interact_ray: RayCast2D = $InteractRaycast
@onready var farm_layer: TileMapLayer = get_node("/root/Main/FarmLayer")

# ... (Giữ nguyên code di chuyển ở Bài 2) ...
func _process(delta: float):
	# ... Logic di chuyển ...
	
	if Input.is_action_just_pressed("ui_accept"): # Phím Space
		hoe_ground()

func hoe_ground():
	var target_world_pos = position + interact_ray.target_position
	var grid_coords: Vector2i = farm_layer.local_to_map(target_world_pos)
	
	# Code rất dễ đọc: Đặt vào tọa độ grid_coords, dùng DIRT_TILE_ID và DIRT_ATLAS_COORD
	farm_layer.set_cell(grid_coords, DIRT_TILE_ID, DIRT_ATLAS_COORD)
```

### 🔷 C#

```csharp
using Godot;

public partial class Player : CharacterBody2D
{
    // Khai báo Hằng số (Clean Code)
    private const int DirtTileId = 0;
    private readonly Vector2I _dirtAtlasCoord = new Vector2I(1, 0);

    private RayCast2D _interactRay;
    private TileMapLayer _farmLayer;

    public override void _Ready()
    {
        // ... Logic bài 2 ...
        _interactRay = GetNode<RayCast2D>("InteractRaycast");
        _farmLayer = GetNode<TileMapLayer>("/root/Main/FarmLayer"); 
    }

    public override void _Process(double delta)
    {
        // ... Logic di chuyển ...
        if (Input.IsActionJustPressed("ui_accept"))
        {
            HoeGround();
        }
    }

    private void HoeGround()
    {
        Vector2 targetWorldPos = Position + _interactRay.TargetPosition;
        Vector2I gridCoords = _farmLayer.LocalToMap(targetWorldPos);

        // Gọi hàm với biến hằng số, cực kỳ an toàn và dễ bảo trì
        _farmLayer.SetCell(gridCoords, DirtTileId, _dirtAtlasCoord);
    }
}
```

> [!WARNING]
> Hàm `local_to_map` là một trong những hàm quan trọng bậc nhất khi làm game với TileMap. Nó giúp bạn quy đổi chính xác từ Tọa độ người chơi đang đứng (ví dụ 300, 450) sang Ô số mấy trên bản đồ cờ caro (ví dụ ô 10, 15).
