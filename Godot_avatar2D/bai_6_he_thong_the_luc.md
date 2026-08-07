# Bài 6: Hệ thống Thể lực (Stamina) & Sự Kiệt sức

Một game Nông trại đúng nghĩa không thể cho phép người chơi cuốc đất cả ngày mà không biết mệt. Chúng ta sẽ xây dựng hệ thống **Thể lực (Stamina)**. Mỗi khi cuốc đất hoặc chặt cây, thể lực sẽ giảm. Khi thể lực về 0, nhân vật sẽ "Kiệt sức" (Ngất xỉu) và game sẽ cưỡng ép chuyển sang ngày hôm sau.

## 1. Thiết kế UI Thanh Thể Lực

1. Khởi tạo một Node `CanvasLayer` đặt tên là `HUD`.
2. Thêm một `TextureProgressBar` vào trong HUD.
   - Đặt `Texture Under` là một cái khung rỗng.
   - Đặt `Texture Progress` là một thanh màu xanh lá cây.
3. Trong script của `Player`, ta sẽ tạo một Signal để thông báo cho HUD cập nhật thanh Stamina.

## 2. Triển khai Code (Player)

Chúng ta cần giới hạn hàm `_input` (hoặc nơi gọi hành động cuốc đất) để kiểm tra xem nhân vật có đủ sức không.

### 🐍 GDScript (`Player.gd`)
```gdscript
extends CharacterBody2D

signal stamina_changed(current_stamina, max_stamina)
signal player_fainted() # Signal phát ra khi ngất xỉu

@export var max_stamina: int = 100
var current_stamina: int

func _ready():
	current_stamina = max_stamina
	# Cập nhật UI ngay lúc bắt đầu
	stamina_changed.emit(current_stamina, max_stamina)

func _process(_delta):
	if Input.is_action_just_pressed("action_hoe"):
		# Kiểm tra xem có đủ sức không (Mỗi lần cuốc tốn 10 sức)
		if current_stamina >= 10:
			perform_hoe_action()
			reduce_stamina(10)
		else:
			print("Không đủ thể lực!")
			# Có thể chạy Animation nhân vật thở dốc ở đây

func reduce_stamina(amount: int):
	current_stamina -= amount
	current_stamina = max(current_stamina, 0) # Không cho âm
	
	stamina_changed.emit(current_stamina, max_stamina)
	
	if current_stamina == 0:
		faint()

func faint():
	print("Nhân vật đã ngất xỉu!")
	player_fainted.emit()
	# Disable input để nhân vật nằm im
	set_process(false)
	set_physics_process(false)
	# Play animation ngã gục...
```

### 🔷 C# (`Player.cs`)
```csharp
using Godot;

public partial class Player : CharacterBody2D
{
    [Signal] public delegate void StaminaChangedEventHandler(int currentStamina, int maxStamina);
    [Signal] public delegate void PlayerFaintedEventHandler();

    [Export] public int MaxStamina = 100;
    private int _currentStamina;

    public override void _Ready()
    {
        _currentStamina = MaxStamina;
        EmitSignal(SignalName.StaminaChanged, _currentStamina, MaxStamina);
    }

    public override void _Process(double delta)
    {
        if (Input.IsActionJustPressed("action_hoe"))
        {
            if (_currentStamina >= 10)
            {
                PerformHoeAction();
                ReduceStamina(10);
            }
            else
            {
                GD.Print("Không đủ thể lực!");
            }
        }
    }

    private void PerformHoeAction() { /* Code cuốc đất */ }

    private void ReduceStamina(int amount)
    {
        _currentStamina -= amount;
        _currentStamina = Mathf.Max(_currentStamina, 0);

        EmitSignal(SignalName.StaminaChanged, _currentStamina, MaxStamina);

        if (_currentStamina == 0)
        {
            Faint();
        }
    }

    private void Faint()
    {
        GD.Print("Ngất xỉu!");
        EmitSignal(SignalName.PlayerFainted);
        SetProcess(false);
        SetPhysicsProcess(false);
    }
}
```

## 3. Cập nhật UI (HUD)

Tạo script `HUD.gd` đính kèm vào `CanvasLayer` để lắng nghe tín hiệu `stamina_changed` từ Player.

### 🐍 GDScript (`HUD.gd`)
```gdscript
extends CanvasLayer

@onready var stamina_bar = $TextureProgressBar

func update_stamina_ui(current: int, max_val: int):
	stamina_bar.max_value = max_val
	# Dùng Tween để thanh thể lực tụt mượt mà thay vì giật cục
	var tween = create_tween()
	tween.tween_property(stamina_bar, "value", current, 0.2)
```

> [!TIP]
> **Game Feel**: Thay vì gán `stamina_bar.value = current` khiến thanh máu tụt giật cục, việc sử dụng `create_tween()` sẽ giúp thanh máu chạy lùi từ từ cực kỳ mượt mắt, đem lại cảm giác Game AAA.
