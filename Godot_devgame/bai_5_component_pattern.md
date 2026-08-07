# Bài 5: Kiến trúc Component-based (Thành phần hóa)

Cách thiết kế truyền thống (Kế thừa - Inheritance) thường gặp vấn đề: Nếu Player có máu (Health), Enemy cũng có máu, Boss cũng có máu. Vậy ta viết code xử lý Máu ở đâu? Viết lại 3 lần? Hay tạo một class `LivingEntity` rồi bắt 3 thằng kia kế thừa? Dùng Kế thừa nhiều sẽ dẫn đến "Cây gia phả" cực kỳ phức tạp (Diamond problem).

Xu hướng hiện đại (ECS / Component-based) là dùng **Thành phần (Composition)**: Cái gì cần thì ráp vào!

## 1. Nguyên lý Component trong Godot
Một Component trong Godot đơn thuần là một Node con.
Thay vì Player tự quản lý Máu, ta tạo một Node riêng tên là `HealthComponent.tscn` chuyên lo việc tăng/giảm máu, phát tín hiệu tử vong. Ráp Node này vào Player, ráp vào Enemy, ráp vào Thùng Gỗ -> Bùm! Cả 3 đều có máu mà không cần viết lại 1 dòng code nào!

## 2. Triển khai Component (HealthComponent)

### 🐍 GDScript

**Tạo script cho HealthComponent (Kế thừa Node thông thường):**
```gdscript
# File: HealthComponent.gd
extends Node
class_name HealthComponent

@export var max_health: int = 100
var current_health: int

signal died()
signal health_changed(current: int, max_h: int)

func _ready():
	current_health = max_health

func take_damage(amount: int):
	current_health -= amount
	health_changed.emit(current_health, max_health)
	
	if current_health <= 0:
		died.emit()
```

**Sử dụng trong Player:**
Kéo thả `HealthComponent` làm con của `Player`.
```gdscript
# File: Player.gd
extends CharacterBody2D

# Tham chiếu đến Component
@onready var health_component: HealthComponent = $HealthComponent

func _ready():
	health_component.died.connect(_on_died)

# Hàm này bị gọi khi trúng đạn
func hit_by_bullet(damage: int):
	health_component.take_damage(damage)

func _on_died():
	print("Player dead!")
	queue_free()
```

### 🔷 C#

**HealthComponent.cs:**
```csharp
using Godot;

// Khai báo GlobalClass để hiển thị trong mục Add Node
[GlobalClass]
public partial class HealthComponent : Node
{
    [Export] public int MaxHealth = 100;
    public int CurrentHealth;

    [Signal] public delegate void DiedEventHandler();
    [Signal] public delegate void HealthChangedEventHandler(int current, int max);

    public override void _Ready()
    {
        CurrentHealth = MaxHealth;
    }

    public void TakeDamage(int amount)
    {
        CurrentHealth -= amount;
        EmitSignal(SignalName.HealthChanged, CurrentHealth, MaxHealth);
        
        if (CurrentHealth <= 0)
        {
            EmitSignal(SignalName.Died);
        }
    }
}
```

**Player.cs:**
```csharp
using Godot;

public partial class Player : CharacterBody2D
{
    private HealthComponent _healthComponent;

    public override void _Ready()
    {
        // Lấy tham chiếu đến Node con
        _healthComponent = GetNode<HealthComponent>("HealthComponent");
        
        // Kết nối tín hiệu
        _healthComponent.Died += OnDied;
    }

    public void HitByBullet(int damage)
    {
        _healthComponent.TakeDamage(damage);
    }

    private void OnDied()
    {
        GD.Print("Player dead!");
        QueueFree();
    }
}
```

> [!TIP]
> Bạn có thể tạo thêm `HitboxComponent` (Vùng nhận sát thương) và `HurtboxComponent` (Vùng gây sát thương) và kết nối chúng bằng Signal. Đây là cấu trúc đỉnh cao được dùng trong mọi game lớn làm bằng Godot!
