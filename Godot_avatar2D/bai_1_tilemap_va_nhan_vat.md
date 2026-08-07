# Bài 1: Khởi tạo Bản đồ (TileMap) và Nhân vật

Chào mừng bạn đến với dự án thực hành **Game Nông Trại (Avatar 2D)**. Để bắt đầu, chúng ta cần một mảnh đất để trồng trọt và một nhân vật nông dân.

## 1. Thiết lập Bản đồ (TileMapLayer)
Trong Godot 4.3, hệ thống TileMap đã được nâng cấp thành **TileMapLayer**, giúp vẽ bản đồ theo từng lớp (Layer) dễ dàng hơn rất nhiều.

**Các bước tạo nông trại:**
1. Tạo một Node `Node2D` làm gốc (đặt tên là `Main`).
2. Thêm một Node `TileMapLayer` vào `Main` (Đặt tên là `GroundLayer`).
3. Ở khung Inspector bên phải, tạo một `TileSet` mới.
4. Kéo thả bức ảnh chứa các ô đất (Tileset Texture) vào khung TileSet dưới cùng.
5. Godot sẽ hỏi bạn có muốn tự động cắt ảnh không -> Chọn **Yes**.
6. Sang tab **TileMap**, chọn các ô đất cỏ và vẽ kín màn hình.
7. Thêm một `TileMapLayer` thứ hai (Đặt tên là `FarmLayer`) để lát các ô đất có thể trồng trọt đè lên lớp cỏ.

## 2. Thiết lập Nhân Vật (Farmer)
Nhân vật trong game góc nhìn từ trên xuống (Top-down) thường sử dụng **CharacterBody2D**.

**Cấu trúc Node của Nhân vật:**
- `CharacterBody2D` (Tên: `Player`)
  - `Sprite2D` (Hình ảnh nhân vật)
  - `CollisionShape2D` (Hình chữ nhật ôm sát chân nhân vật để xét va chạm)
  - `AnimationPlayer` (Tạo hoạt ảnh đi lên, đi xuống, cuốc đất)

## 3. Khởi tạo Code Cơ Bản

### 🐍 GDScript
Gắn script này vào Node `Player`. Tạm thời ta chỉ khai báo các thông số cơ bản.
```gdscript
extends CharacterBody2D

# Kích thước của 1 ô Grid (Thường là 16x16 hoặc 32x32 pixels)
const GRID_SIZE: int = 32

# Tốc độ di chuyển
@export var speed: float = 150.0

func _ready():
	# Đảm bảo nhân vật luôn đứng vừa vặn vào giữa một ô Grid khi bắt đầu game
	position = position.snapped(Vector2(GRID_SIZE, GRID_SIZE))
```

### 🔷 C#
Gắn script này vào Node `Player`.
```csharp
using Godot;

public partial class Player : CharacterBody2D
{
    // Kích thước của 1 ô Grid
    public const int GridSize = 32;

    [Export]
    public float Speed = 150.0f;

    public override void _Ready()
    {
        // Căn chỉnh nhân vật vừa vặn vào lưới khi bắt đầu
        Position = Position.Snapped(new Vector2(GridSize, GridSize));
    }
}
```

> [!NOTE]
> Hàm `snapped()` là một hàm toán học cực kỳ hữu ích trong Godot giúp làm tròn tọa độ. Ví dụ: Nếu nhân vật đứng ở `(15, 40)` và Grid là `32`, `snapped` sẽ kéo nhân vật về ô `(0, 32)` gần nhất!

Ở bài sau, chúng ta sẽ lập trình thuật toán di chuyển nhân vật nhảy theo từng ô vuông (Grid-based movement).
