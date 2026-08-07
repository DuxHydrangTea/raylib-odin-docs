# Bài 12: Chăn nuôi (Xây Chuồng & Ấp Trứng)

Trồng trọt đã xong, giờ là lúc sắm sửa một bầy Gà con. Việc mua Gà không giống mua Hạt giống, Gà cần Chuồng và cần thời gian Ấp.

## 1. Mua và Đặt Chuồng Gà (Coop)

Chuồng Gà là một `StaticBody2D` (chiếm diện tích, không đi xuyên được). Khi mua Chuồng, ta chuyển sang "Chế độ Xây dựng" (Build Mode), con trỏ chuột sẽ biến thành hình Chuồng gà màu xanh trong suốt để chọn vị trí.

### 🐍 GDScript (Chế độ Xây dựng)
```gdscript
extends Node2D

var is_building = false
var building_preview_sprite: Sprite2D
var coop_scene = preload("res://Coop.tscn")

func start_building():
	is_building = true
	building_preview_sprite.modulate = Color(0, 1, 0, 0.5) # Xanh lá trong suốt
	building_preview_sprite.visible = true

func _process(_delta):
	if not is_building: return
	
	# Bám theo con trỏ chuột (Snap vào Grid)
	var mouse_pos = get_global_mouse_position()
	# Dùng phép chia lấy dư để làm tròn tọa độ theo ô lưới 16x16
	var snapped_pos = mouse_pos.snapped(Vector2(16, 16)) 
	building_preview_sprite.global_position = snapped_pos
	
	# Nhấn chuột trái để Đặt chuồng
	if Input.is_action_just_pressed("mouse_click"):
		place_coop(snapped_pos)

func place_coop(pos: Vector2):
	is_building = false
	building_preview_sprite.visible = false
	
	var coop = coop_scene.instantiate()
	coop.global_position = pos
	get_tree().current_scene.add_child(coop)
	print("Đã xây Chuồng Gà!")
```

## 2. Máy Ấp Trứng (Incubator)

Trong Chuồng Gà sẽ có một cái Máy ấp. Khi người chơi cầm quả trứng tương tác với Máy ấp, nó sẽ bắt đầu đếm ngược thời gian (Đếm theo Ngày).

### 🐍 GDScript (`Incubator.gd`)
```gdscript
extends Area2D

var has_egg = false
var days_left = 0

func _ready():
	TimeManager.day_changed.connect(_on_day_changed)

func interact(player):
	if has_egg: return
	
	# Nếu người chơi đang cầm Quả Trứng
	if player.inventory.get_equipped_item() == "egg":
		player.inventory.remove_item("egg", 1)
		has_egg = true
		days_left = 3 # 3 ngày để nở
		print("Đã ném trứng vào máy ấp. Chờ 3 ngày nhé!")
		$EggSprite.visible = true

func _on_day_changed(_day):
	if not has_egg: return
	
	days_left -= 1
	if days_left <= 0:
		hatch_chicken()

func hatch_chicken():
	has_egg = false
	$EggSprite.visible = false
	print("Tèn Tén Ten! Trứng đã nở thành Gà Con!")
	
	var chicken = preload("res://Chicken.tscn").instantiate()
	# Đẻ con Gà ngay trước mặt máy ấp
	chicken.global_position = global_position + Vector2(0, 20)
	get_tree().current_scene.add_child(chicken)
```

> [!TIP]
> Việc lắng nghe `day_changed` từ `TimeManager` ở khắp mọi nơi (Cây trồng, Máy ấp, Hợp đồng nhiệm vụ) chứng minh sức mạnh của hệ thống Event Bus & Autoload. Các object hoạt động độc lập nhưng liên kết vô cùng chặt chẽ.
