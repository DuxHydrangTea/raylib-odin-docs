# Bài 4: Gieo Hạt và Quản Lý Thời Gian Cây Lớn

Sau khi có đất đã cuốc, người chơi cần gieo hạt. Cây sẽ trải qua 3 giai đoạn: Mầm -> Cây nhỏ -> Có thể thu hoạch (Fruit).

## 1. Sinh Node Cây Trồng (Crop Scene)
Thay vì đổi TileMap, khi trồng cây, ta nên `instantiate()` một Scene riêng tên là `Crop.tscn`. Scene này chứa `Sprite2D` và `Timer`.

## 2. Refactor: Tránh Hard-code và Magic Numbers

> [!TIP]
> **Tư duy đi làm (Professional):** 
> 1. Không dùng số `0, 1, 2` để đánh dấu giai đoạn phát triển. Hãy dùng `Enum`.
> 2. Đừng gán chết (hard-code) đường dẫn ảnh `"res://assets/seed.png"` thẳng vào file Script. Điều này khiến Game Designer hoặc Họa sĩ không thể tự thay ảnh bằng giao diện Godot mà cứ phải mở code ra sửa. Thay vào đó, hãy dùng `@export var`.

### Script cho Crop.tscn

#### 🐍 GDScript
```gdscript
extends Node2D

# Khai báo Enum thay cho Magic Numbers (0, 1, 2)
enum GrowthStage { SEED, SPROUT, MATURE }
var current_stage: GrowthStage = GrowthStage.SEED

# Dùng @export để cho phép Designer kéo thả ảnh tùy thích từ Inspector
@export var seed_texture: Texture2D
@export var sprout_texture: Texture2D
@export var mature_texture: Texture2D

@onready var timer = $GrowthTimer
@onready var sprite = $Sprite2D

func _ready():
	timer.wait_time = 5.0 
	timer.timeout.connect(_on_timer_timeout)
	timer.start()
	update_sprite()

func _on_timer_timeout():
	if current_stage != GrowthStage.MATURE:
		current_stage += 1
		update_sprite()
		
		if current_stage != GrowthStage.MATURE:
			timer.start()

func update_sprite():
	match current_stage:
		GrowthStage.SEED:
			sprite.texture = seed_texture
		GrowthStage.SPROUT:
			sprite.texture = sprout_texture
		GrowthStage.MATURE:
			sprite.texture = mature_texture
```

#### 🔷 C#
```csharp
using Godot;

public partial class Crop : Node2D
{
    // Khai báo Enum
    public enum GrowthStage { Seed, Sprout, Mature }
    private GrowthStage _currentStage = GrowthStage.Seed;

    // Dùng [Export] để lộ biến ra Inspector
    [Export] public Texture2D SeedTexture;
    [Export] public Texture2D SproutTexture;
    [Export] public Texture2D MatureTexture;

    private Timer _timer;
    private Sprite2D _sprite;

    public override void _Ready()
    {
        _timer = GetNode<Timer>("GrowthTimer");
        _sprite = GetNode<Sprite2D>("Sprite2D");

        _timer.WaitTime = 5.0f;
        _timer.Timeout += OnTimerTimeout;
        _timer.Start();
        
        UpdateSprite();
    }

    private void OnTimerTimeout()
    {
        if (_currentStage != GrowthStage.Mature)
        {
            _currentStage++;
            UpdateSprite();
            
            if (_currentStage != GrowthStage.Mature)
                _timer.Start();
        }
    }

    private void UpdateSprite()
    {
        switch (_currentStage)
        {
            case GrowthStage.Seed: _sprite.Texture = SeedTexture; break;
            case GrowthStage.Sprout: _sprite.Texture = SproutTexture; break;
            case GrowthStage.Mature: _sprite.Texture = MatureTexture; break;
        }
    }
}
```

Với cách viết này, code cực kỳ "Clean", dễ đọc, và Họa sĩ có thể thay đổi giao diện/hình ảnh cây trồng thông qua Godot Editor mà không sợ làm hỏng logic của Lập trình viên!
