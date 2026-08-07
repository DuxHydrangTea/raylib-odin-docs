# Bài 3: Quản lý Signals tập trung với Event Bus

Ở phần Cơ bản, bạn đã học cách dùng Signals. Tuy nhiên, nếu Hệ thống Giao diện (UI) muốn bắt tín hiệu của Hàng trăm con quái vật để hiển thị thanh máu, việc gọi `connect()` thủ công cho từng con quái là thảm họa.
Mẫu thiết kế **Event Bus** kết hợp Autoload sẽ cứu rỗi bạn.

## 1. Event Bus là gì?
Event Bus đơn giản là một Autoload/Singleton KHÔNG CHỨA LOGIC, nó **chỉ chứa các khai báo Signals**.
- Quái vật bị đánh -> Báo cho Event Bus.
- UI máu hiển thị -> Lắng nghe từ Event Bus.
-> Quái vật và UI hoàn toàn không biết đến sự tồn tại của nhau!

**Bước 1:** Tạo một script `EventBus` và cài làm Autoload.

## 2. Triển khai Event Bus

### 🐍 GDScript

```gdscript
# File: EventBus.gd (Autoload)
extends Node

signal enemy_damaged(enemy_name: String, remaining_hp: int)
signal player_leveled_up(new_level: int)
```

```gdscript
# File: Enemy.gd
extends CharacterBody2D

func take_damage(dmg: int):
	var hp -= dmg
	# Thay vì tự emit signal, ta dùng EventBus để phát loa thông báo toàn game
	EventBus.enemy_damaged.emit(self.name, hp)
```

```gdscript
# File: UIManager.gd
extends CanvasLayer

func _ready():
	# Đăng ký nghe kênh thông báo "enemy_damaged" từ loa phường EventBus
	EventBus.enemy_damaged.connect(_on_enemy_damaged)

func _on_enemy_damaged(enemy_name: String, hp: int):
	print("Kẻ thù ", enemy_name, " còn ", hp, " máu.")
```

### 🔷 C#
Trong C#, Godot hỗ trợ Signal rất tốt thông qua `[Signal]` attribute kết hợp với `delegate`.

```csharp
// File: EventBus.cs (Autoload)
using Godot;

public partial class EventBus : Node
{
    public static EventBus Instance { get; private set; }

    // C# Yêu cầu khai báo kiểu delegate trước
    [Signal]
    public delegate void EnemyDamagedEventHandler(string enemyName, int remainingHp);
    
    [Signal]
    public delegate void PlayerLeveledUpEventHandler(int newLevel);

    public override void _EnterTree()
    {
        if (Instance == null) Instance = this;
    }
}
```

```csharp
// File: Enemy.cs
using Godot;

public partial class Enemy : CharacterBody2D
{
    private int _hp = 100;

    public void TakeDamage(int dmg)
    {
        _hp -= dmg;
        // Phát tín hiệu qua EmitSignal
        EventBus.Instance.EmitSignal(EventBus.SignalName.EnemyDamaged, this.Name, _hp);
    }
}
```

```csharp
// File: UIManager.cs
using Godot;

public partial class UIManager : CanvasLayer
{
    public override void _Ready()
    {
        // Lắng nghe tín hiệu
        EventBus.Instance.EnemyDamaged += OnEnemyDamaged;
    }

    private void OnEnemyDamaged(string enemyName, int hp)
    {
        GD.Print($"Kẻ thù {enemyName} còn {hp} máu.");
    }
}
```

> [!TIP]
> Event Bus là mẫu thiết kế (pattern) được khuyên dùng nhiều nhất khi làm các game có hệ thống UI phức tạp trong Godot.
