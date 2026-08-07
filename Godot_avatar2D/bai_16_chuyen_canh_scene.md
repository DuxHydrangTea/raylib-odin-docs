# Bài 16: Chuyển Cảnh Mượt Mà (Scene Transition)

Trong Game Nông Trại, việc đi từ ngoài vườn (Bản đồ World) vào trong Nhà (Bản đồ House) diễn ra liên tục. Nếu gọi lệnh `change_scene_to_file()` thẳng thừng, game sẽ chớp đen màn hình cực kỳ xấu.

Ta cần tạo một hệ thống **Chuyển cảnh mượt mà (Fade In/Out)** và tự động đặt Player vào đúng Cửa ra/vào.

## 1. Scene Chuyển Cảnh (TransitionLayer)

Tạo một `CanvasLayer` đặt tên `SceneManager` và cấu hình làm Autoload.
Bên trong Scene này có:
- Một `ColorRect` màu Đen (Kéo giãn full màn hình).
- Một `AnimationPlayer` để tạo hoạt ảnh `fade_in` (Đen -> Trong suốt) và `fade_out` (Trong suốt -> Đen).

### 🐍 GDScript (`SceneManager.gd`)
```gdscript
extends CanvasLayer

@onready var anim = $AnimationPlayer
@onready var color_rect = $ColorRect

var target_door_tag = ""

func _ready():
	color_rect.visible = false

# Hàm này được gọi bởi cái Cửa (Door)
func transition_to_scene(scene_path: String, door_tag: String):
	target_door_tag = door_tag
	
	# Bật màn đen lên và mờ dần
	color_rect.visible = true
	anim.play("fade_out")
	
	# Tạm dừng game để Player không chạy lung tung trong lúc màn hình đang đen
	get_tree().paused = true
	
	# Đợi Animation chạy xong
	await anim.animation_finished
	
	# Đổi Scene
	get_tree().change_scene_to_file(scene_path)
	
	# Sáng dần lên
	anim.play("fade_in")
	await anim.animation_finished
	
	get_tree().paused = false
	color_rect.visible = false
```

## 2. Gắn Cửa (Doorway)

Ở ngoài Bản đồ (World), ngay chỗ cửa Nhà, ta đặt một `Area2D` tên là `Door`.

### 🐍 GDScript (`Door.gd`)
```gdscript
extends Area2D

@export_file("*.tscn") var next_scene_path: String
@export var door_tag: String = "MainHouse"

func _ready():
	body_entered.connect(_on_body_entered)

func _on_body_entered(body):
	if body.name == "Player":
		# Gọi SceneManager (Singleton) để chuyển cảnh
		SceneManager.transition_to_scene(next_scene_path, door_tag)
```

## 3. Khởi tạo Vị trí Player (Spawn Point)

Khi Scene mới (House) tải lên, Player mặc định sẽ bị quăng ở tọa độ (0,0). Ta phải di chuyển Player đến đúng Cửa (SpawnPoint) tương ứng với cái Cửa mà họ vừa bước vào.

Bên trong Scene `House.tscn`, đặt một cái `Marker2D` ngay chỗ Cửa ra vào và đặt tên là `Spawn_MainHouse`.

### 🐍 GDScript (`HouseLevel.gd`)
Script gắn ở Gốc của Scene `House`.
```gdscript
extends Node2D

func _ready():
	var player = get_tree().get_first_node_in_group("Player")
	
	# Lấy cái Tag cửa từ SceneManager
	var tag = SceneManager.target_door_tag
	
	# Tìm Marker2D tương ứng
	var spawn_point = get_node_or_null("Spawn_" + tag)
	if spawn_point:
		player.global_position = spawn_point.global_position
```

> [!IMPORTANT]
> Cơ chế `door_tag` (Nhãn của Cửa) là cực kỳ quan trọng. Hãy tưởng tượng bản đồ World có Cửa đi vào Nhà, và Cửa đi vào Chuồng Gà. Nếu không có `door_tag`, khi Player từ Nhà bước ra ngoài World, Game sẽ không biết phải thả Player ở trước cửa Nhà hay thả ở trước Chuồng Gà!
