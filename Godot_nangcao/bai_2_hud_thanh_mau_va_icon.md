# Bài 2: Tạo HUD In-game (Thanh Máu & Icon)

HUD (Heads-Up Display) là các thông số luôn hiển thị trên màn hình khi bạn đang chơi game, ví dụ: Thanh máu (HP Bar) và Số lượng vật phẩm trong kho.

## 1. Chế tạo Thanh Máu bằng TextureProgressBar
Node `ProgressBar` mặc định khá xấu. Để làm thanh máu đẹp có hình khung đồ họa, ta dùng **TextureProgressBar**.

1. Thêm Node `TextureProgressBar`.
2. Ở phần Textures trong Inspector, bạn cần 2 bức ảnh:
   - **Under**: Ảnh nền tối màu (cái vỏ thanh máu).
   - **Progress**: Ảnh phần máu (màu đỏ hoặc xanh lá).
3. Chỉnh thông số **Max Value** = 100, **Value** = 100.
4. Kéo thử thanh `Value`, bạn sẽ thấy máu tụt xuống cực kỳ mượt mà!

## 2. Kết nối HUD với Event Bus (Đã học ở phần Devgame)

Thay vì Player tự đi tìm thanh máu để trừ, ta để UI tự lắng nghe tín hiệu `health_changed` từ EventBus.

### 🐍 GDScript
```gdscript
extends Control

@onready var hp_bar: TextureProgressBar = $MarginContainer/HPBar
@onready var tomato_label: Label = $MarginContainer/Inventory/TomatoCount

func _ready():
	# Lắng nghe sự kiện từ Event Bus
	EventBus.player_health_changed.connect(update_hp_bar)
	InventoryManager.inventory_updated.connect(update_inventory)

func update_hp_bar(current_hp: int):
	# Code rất xịn: Dùng Tween để thanh máu tụt từ từ (Game Feel) thay vì giật cục
	var tween = create_tween()
	tween.tween_property(hp_bar, "value", current_hp, 0.3)

func update_inventory():
	# Cập nhật số cà chua đang có
	var count = InventoryManager.items.get("tomato", 0)
	tomato_label.text = "x " + str(count)
```

### 🔷 C#
```csharp
using Godot;

public partial class HUD : Control
{
    private TextureProgressBar _hpBar;
    private Label _tomatoLabel;

    public override void _Ready()
    {
        _hpBar = GetNode<TextureProgressBar>("MarginContainer/HPBar");
        _tomatoLabel = GetNode<Label>("MarginContainer/Inventory/TomatoCount");

        // Lắng nghe sự kiện
        EventBus.Instance.PlayerHealthChanged += UpdateHpBar;
        InventoryManager.Instance.InventoryUpdated += UpdateInventory;
    }

    private void UpdateHpBar(int currentHp)
    {
        // Hiệu ứng Tween mượt mà
        Tween tween = CreateTween();
        tween.TweenProperty(_hpBar, "value", currentHp, 0.3f);
    }

    private void UpdateInventory()
    {
        int count = 0;
        if (InventoryManager.Instance.Items.ContainsKey("tomato"))
        {
            count = InventoryManager.Instance.Items["tomato"];
        }
        _tomatoLabel.Text = "x " + count.ToString();
    }
}
```

> [!NOTE]
> Hàm `create_tween()` là "ma thuật" của Godot. Nó giúp bạn làm mọi hiệu ứng chuyển động mượt mà (animating code) mà không cần dùng đến Node AnimationPlayer.
