# Bài 17: Hệ thống Hội Thoại (Dialogue System)

Tương tác với dân làng là linh hồn của thể loại Nông trại. Chúng ta sẽ tạo một Hộp thoại (Dialogue Box) hiện lên chữ chạy từ từ (Typewriter effect) kèm theo hình đại diện (Portrait) của NPC.

## 1. Thiết kế Hộp thoại (UI)

Tạo một Scene `DialogueUI.tscn` (Kế thừa `CanvasLayer` để đè lên mọi thứ).
- Dùng `NinePatchRect` để làm khung hộp thoại có viền đẹp.
- Dùng `TextureRect` đặt bên trái làm Hình đại diện (Portrait).
- Dùng `RichTextLabel` để hiển thị chữ. Bật `bbcode_enabled = true` để tô màu từng chữ nếu muốn.

## 2. Code Hiệu ứng chữ chạy (Typewriter)

Để chữ hiện ra từng ký tự một, ta dùng thuộc tính `visible_characters` của `RichTextLabel`.

### 🐍 GDScript (`DialogueUI.gd`)
```gdscript
extends CanvasLayer

@onready var text_label = $NinePatchRect/RichTextLabel
@onready var portrait = $NinePatchRect/Portrait
@onready var timer = $LetterTimer # Timer với thời gian 0.05s, lặp vô hạn

var current_dialogues = []
var current_index = 0

func _ready():
	visible = false

# Hàm này được gọi bởi NPC khi Player bắt chuyện
func start_dialogue(lines: Array, npc_portrait: Texture2D):
	current_dialogues = lines
	current_index = 0
	portrait.texture = npc_portrait
	
	visible = true
	get_tree().paused = true # Dừng thời gian khi nói chuyện
	show_line()

func show_line():
	text_label.text = current_dialogues[current_index]
	text_label.visible_characters = 0
	timer.start() # Bắt đầu chạy chữ

# Khi người chơi bấm phím Tương tác
func _input(event):
	if not visible: return
	
	if event.is_action_pressed("interact"):
		if text_label.visible_characters < text_label.get_total_character_count():
			# Nếu chữ chưa hiện hết -> Bấm để hiện hết ngay lập tức
			text_label.visible_characters = text_label.get_total_character_count()
			timer.stop()
		else:
			# Đã hiện hết -> Chuyển sang câu tiếp theo
			current_index += 1
			if current_index < current_dialogues.size():
				show_line()
			else:
				# Hết hội thoại -> Đóng bảng
				visible = false
				get_tree().paused = false

# Mỗi 0.05s hiện thêm 1 chữ
func _on_letter_timer_timeout():
	if text_label.visible_characters < text_label.get_total_character_count():
		text_label.visible_characters += 1
	else:
		timer.stop()
```

## 3. Tạo NPC Tương tác

Tạo một `StaticBody2D` (NPC), gắn thêm `Area2D` để phát hiện Player.

### 🐍 GDScript (`NPC_Mayor.gd`)
```gdscript
extends StaticBody2D

@export var avatar: Texture2D
var lines = [
	"Chào cháu! Cháu là người mới chuyển đến trang trại cũ của ông nội đúng không?",
	"Ta là Thị trưởng Lewis. Chào mừng cháu đến với thung lũng Pelican!",
	"Hãy dọn dẹp đống cỏ dại và bắt đầu gieo hạt nhé."
]

var is_player_near = false

func _ready():
	$TalkArea.body_entered.connect(func(b): if b.name == "Player": is_player_near = true)
	$TalkArea.body_exited.connect(func(b): if b.name == "Player": is_player_near = false)

func _input(event):
	if is_player_near and event.is_action_pressed("interact"):
		# Giả sử DialogueUI được gắn làm Autoload tên là DialogueManager
		DialogueManager.start_dialogue(lines, avatar)
```

> [!TIP]
> Việc dùng `RichTextLabel` kết hợp `bbcode` cho phép bạn chèn màu sắc vào đoạn hội thoại. Ví dụ: `"Ta là [color=red]Thị trưởng Lewis[/color]"`. Tên ông trưởng làng sẽ nổi bần bật màu Đỏ!
