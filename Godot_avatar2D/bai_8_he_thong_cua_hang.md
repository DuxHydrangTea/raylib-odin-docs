# Bài 8: Xây dựng Cửa Hàng (Shop UI)

Kinh tế là huyết mạch của Nông trại. Chúng ta cần thiết lập Vàng (Gold) và Giao diện Cửa hàng để người chơi mua Cà chua, Bắp cải và bán Nông sản.

## 1. Quản lý Vàng (Gold)

Thêm biến `gold` vào `Player.gd` hoặc một Autoload `InventoryManager`.

### 🐍 GDScript
```gdscript
var gold: int = 500

signal gold_changed(new_amount)

func add_gold(amount: int):
	gold += amount
	gold_changed.emit(gold)

func spend_gold(amount: int) -> bool:
	if gold >= amount:
		gold -= amount
		gold_changed.emit(gold)
		return true
	return false # Không đủ tiền
```

## 2. Giao diện Cửa Hàng (Control Nodes)

Tạo một Scene mới tên là `ShopUI.tscn` (Kế thừa từ `Control`).
- Dùng `ColorRect` làm nền (Làm mờ màn hình game).
- Dùng `PanelContainer` làm bảng menu cửa hàng.
- Dùng `GridContainer` chứa danh sách các Nút (Button) mua vật phẩm.

### Thiết lập Nút Mua (Buy Button)
Tạo script gắn vào một Nút mua Hạt giống Cà chua:

#### 🐍 GDScript
```gdscript
extends Button

@export var item_id: String = "tomato_seed"
@export var price: int = 50

func _pressed():
	# Giả sử ta lấy tham chiếu tới Player (hoặc gọi qua Autoload)
	var player = get_tree().get_first_node_in_group("Player")
	
	if player.spend_gold(price):
		# Nếu trừ tiền thành công, ném hạt giống vào kho đồ
		player.inventory.add_item(item_id, 1)
		print("Mua thành công 1 hạt giống Cà chua!")
	else:
		print("Nghèo quá, không đủ tiền!")
		# Play hiệu ứng rung màn hình chữ Đỏ
```

#### 🔷 C#
```csharp
using Godot;

public partial class BuyButton : Button
{
    [Export] public string ItemId = "tomato_seed";
    [Export] public int Price = 50;

    public override void _Pressed()
    {
        // Giả sử lấy tham chiếu Player qua Group
        Player player = GetTree().GetFirstNodeInGroup("Player") as Player;

        if (player.SpendGold(Price))
        {
            player.Inventory.AddItem(ItemId, 1);
            GD.Print("Mua thành công!");
        }
        else
        {
            GD.Print("Không đủ tiền!");
        }
    }
}
```

## 3. Tương tác với Cửa hàng (NPC Pier)

Ở bản đồ ngoài thế giới (World), ta đặt một cái quầy hàng (Node `StaticBody2D` kết hợp `Area2D` làm vùng tương tác).

### 🐍 GDScript (`ShopCounter.gd`)
```gdscript
extends Area2D

# Gán file ShopUI.tscn vào đây từ Inspector
@export var shop_ui_scene: PackedScene
var is_player_near = false

func _ready():
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)

func _on_body_entered(body):
	if body.name == "Player":
		is_player_near = true

func _on_body_exited(body):
	if body.name == "Player":
		is_player_near = false

func _input(event):
	# Nếu Player đứng gần và bấm phím Tương tác (Space / E)
	if is_player_near and event.is_action_pressed("interact"):
		open_shop()

func open_shop():
	# Đẻ cái Menu UI ra
	var shop = shop_ui_scene.instantiate()
	# Gắn nó lên CanvasLayer cao nhất để đè lên mọi thứ
	get_tree().root.add_child(shop)
	
	# Tạm dừng vật lý của Game (Tùy chọn)
	get_tree().paused = true
```

> [!TIP]
> **Tạm dừng Game (Pause)**: Khi mở UI cửa hàng, thường ta sẽ set `get_tree().paused = true` để thời gian ngừng trôi và bọn quái vật không cắn lén chúng ta. Nhớ chỉnh thuộc tính `Process Mode` của Scene ShopUI thành **"Always"** để bản thân cái Cửa hàng không bị đứng hình theo!
