# Bài 1: Health Component (Quản lý Máu & I-Frames)

Trong Godot, thay vì mỗi Entity (Player, Enemy, Boss) tự chứa một mớ hỗn độn các biến `hp`, `max_hp`, và `is_invincible`, chúng ta sẽ gói gọn tất cả vào một Node duy nhất tên là `HealthComponent`.

Bất kỳ Object nào cần có máu, bạn chỉ việc thêm `HealthComponent` làm con của Object đó.

## 1. Thiết kế HealthComponent
Component này kế thừa từ `Node` thông thường và có các tính năng:
- Máu tối đa (`max_health`).
- Thời gian bất tử sau khi dính đòn (I-Frames - Invincibility Frames).
- Phát tín hiệu `died` khi hết máu.

## 2. Triển khai Code (Production-ready)

### 🐍 GDScript
Tạo file `HealthComponent.gd` và gắn vào một Node cơ bản.

```gdscript
extends Node
class_name HealthComponent

signal health_changed(current_health: int, max_health: int)
signal died()
signal took_damage(amount: int)

@export var max_health: int = 100
@export var invincibility_time: float = 0.5 # Thời gian bất tử (giây)

var current_health: int:
	set(value):
		# Không cho phép máu vượt quá max_health hoặc rớt xuống dưới 0
		current_health = clamp(value, 0, max_health)
		health_changed.emit(current_health, max_health)
		
		if current_health == 0:
			died.emit()

var is_invincible: bool = false
var _invincibility_timer: Timer

func _ready():
	current_health = max_health
	
	# Khởi tạo Timer bằng code để xử lý I-Frames
	_invincibility_timer = Timer.new()
	_invincibility_timer.one_shot = true
	_invincibility_timer.wait_time = invincibility_time
	_invincibility_timer.timeout.connect(_on_invincibility_ended)
	add_child(_invincibility_timer)

func take_damage(amount: int):
	# Nếu đang trong thời gian bất tử hoặc đã chết, bỏ qua sát thương
	if is_invincible or current_health == 0:
		return
		
	current_health -= amount
	took_damage.emit(amount)
	
	if current_health > 0:
		start_invincibility()

func start_invincibility():
	is_invincible = true
	_invincibility_timer.start()

func _on_invincibility_ended():
	is_invincible = false

# Hàm công khai cho phép uống bình máu
func heal(amount: int):
	if current_health > 0: # Không cho phép cứu sống kẻ đã chết
		current_health += amount
```

### 🔷 C#
Tạo file `HealthComponent.cs`. Dùng `[GlobalClass]` để nó xuất hiện trong menu Add Node.

```csharp
using Godot;

[GlobalClass]
public partial class HealthComponent : Node
{
    [Signal] public delegate void HealthChangedEventHandler(int currentHealth, int maxHealth);
    [Signal] public delegate void DiedEventHandler();
    [Signal] public delegate void TookDamageEventHandler(int amount);

    [Export] public int MaxHealth = 100;
    [Export] public float InvincibilityTime = 0.5f;

    private int _currentHealth;
    public int CurrentHealth
    {
        get => _currentHealth;
        private set
        {
            _currentHealth = Mathf.Clamp(value, 0, MaxHealth);
            EmitSignal(SignalName.HealthChanged, _currentHealth, MaxHealth);
            
            if (_currentHealth == 0) EmitSignal(SignalName.Died);
        }
    }

    private bool _isInvincible = false;
    private Timer _invincibilityTimer;

    public override void _Ready()
    {
        CurrentHealth = MaxHealth;
        
        _invincibilityTimer = new Timer();
        _invincibilityTimer.OneShot = true;
        _invincibilityTimer.WaitTime = InvincibilityTime;
        _invincibilityTimer.Timeout += OnInvincibilityEnded;
        AddChild(_invincibilityTimer);
    }

    public void TakeDamage(int amount)
    {
        if (_isInvincible || CurrentHealth == 0) return;
        
        CurrentHealth -= amount;
        EmitSignal(SignalName.TookDamage, amount);
        
        if (CurrentHealth > 0)
        {
            StartInvincibility();
        }
    }

    private void StartInvincibility()
    {
        _isInvincible = true;
        _invincibilityTimer.Start();
    }

    private void OnInvincibilityEnded()
    {
        _isInvincible = false;
    }

    public void Heal(int amount)
    {
        if (CurrentHealth > 0) CurrentHealth += amount;
    }
}
```

> [!TIP]
> **I-Frames** (Invincibility Frames) là tính năng vô cùng quan trọng. Nếu không có Timer chặn lại, khi một viên đạn bay xuyên qua nhân vật, nó có thể kích hoạt hàm `take_damage()` 60 lần trong 1 giây (do `_process` chạy 60FPS) khiến nhân vật đột tử ngay lập tức!
