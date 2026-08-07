# Bài 2: Hitbox & Hurtbox Component

Trong game 2D, việc kiểm tra va chạm để trừ máu rất nhạy cảm. Thường người ta sẽ tách rời logic Sát thương ra khỏi Physics (Vật lý). 
- **HitboxComponent (Hộp Nhận Đòn)**: Node `Area2D` bao quanh cơ thể nhân vật. Nếu bị chém trúng, nó sẽ gọi `take_damage()` trên `HealthComponent`.
- **HurtboxComponent (Hộp Gây Đòn)**: Node `Area2D` gắn ở lưỡi kiếm hoặc viên đạn. Khi chạm vào Hitbox của kẻ địch, nó truyền sát thương sang.

## 1. HitboxComponent (Nhận Sát Thương)

Thêm một Node `Area2D` và đặt tên là `HitboxComponent`.

### 🐍 GDScript
```gdscript
extends Area2D
class_name HitboxComponent

# Gắn tham chiếu đến HealthComponent của thực thể này
@export var health_component: HealthComponent

func take_damage(amount: int):
	# Nhận sát thương và chuyển thẳng cho HealthComponent xử lý
	if health_component:
		health_component.take_damage(amount)
```

### 🔷 C#
```csharp
using Godot;

[GlobalClass]
public partial class HitboxComponent : Area2D
{
    [Export] public HealthComponent HealthComponent;

    public void TakeDamage(int amount)
    {
        if (HealthComponent != null)
        {
            HealthComponent.TakeDamage(amount);
        }
    }
}
```

## 2. HurtboxComponent (Gây Sát Thương)

Thêm một Node `Area2D` khác đặt tên là `HurtboxComponent`. Chúng ta sẽ kết nối signal `area_entered` của chính nó để phát hiện khi nó chém trúng một `HitboxComponent`.

### 🐍 GDScript
```gdscript
extends Area2D
class_name HurtboxComponent

@export var damage: int = 10

func _ready():
	# Lắng nghe khi có Area2D khác lọt vào khu vực sát thương
	area_entered.connect(_on_area_entered)

func _on_area_entered(area: Area2D):
	# Nếu cái Area bị chạm trúng là một HitboxComponent
	if area is HitboxComponent:
		# Gây sát thương!
		area.take_damage(damage)
```

### 🔷 C#
```csharp
using Godot;

[GlobalClass]
public partial class HurtboxComponent : Area2D
{
    [Export] public int Damage = 10;

    public override void _Ready()
    {
        AreaEntered += OnAreaEntered;
    }

    private void OnAreaEntered(Area2D area)
    {
        // Kiểm tra xem area lọt vào có phải Hitbox không
        if (area is HitboxComponent hitbox)
        {
            hitbox.TakeDamage(Damage);
        }
    }
}
```

## 3. Thiết lập Collision Layer & Mask (Cực kỳ quan trọng)

Nếu bạn không cài đặt Layer, lưỡi kiếm của Player có thể sẽ chém trúng... chính thân thể của Player (tự sát).

**Quy tắc:**
- **Layer**: "Tôi là ai?"
- **Mask**: "Tôi muốn va chạm với ai?"

**Cách thiết lập trong Project Settings -> 2D Physics:**
1. Đặt tên Layer 1: `Player_Hitbox`
2. Đặt tên Layer 2: `Player_Hurtbox`
3. Đặt tên Layer 3: `Enemy_Hitbox`
4. Đặt tên Layer 4: `Enemy_Hurtbox`

**Gán cho Node:**
- **Kiếm của Player (`HurtboxComponent`)**: 
  - Layer = 2 (`Player_Hurtbox`)
  - Mask = 3 (`Enemy_Hitbox`). (Nó chỉ có thể chém trúng Enemy).
- **Thân thể Enemy (`HitboxComponent`)**: 
  - Layer = 3 (`Enemy_Hitbox`)
  - Mask = Không tick gì cả (Mask chỉ dành cho người CHỦ ĐỘNG tìm kiếm va chạm, Hitbox là kẻ BỊ ĐỘNG).

> [!TIP]
> Việc thiết lập Layer & Mask chuẩn chỉnh là điểm mấu chốt khác biệt giữa "Dev Xịn" và "Gà mờ" khi làm game Godot!
