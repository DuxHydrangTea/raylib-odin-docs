# Bài 3: Xử lý Input & Sự kiện

Để trò chơi có tính tương tác, bạn cần biết cách nhận các lệnh điều khiển từ người chơi (Bàn phím, Chuột, Gamepad). Trong Godot, hệ thống **Input** lo việc này.

## 1. Input Map (Bản đồ phím)
Thay vì hard-code (viết cứng) phím cụ thể như "Phím mũi tên phải", Godot cho phép bạn định nghĩa các **Action** (hành động).
- Mở **Project -> Project Settings -> Input Map**.
- Thêm một action mới, ví dụ `move_right`.
- Gán phím `D` và phím `Mũi tên phải` cho action `move_right`.

## 2. Bắt sự kiện bằng code (Polling)
Bạn có thể kiểm tra trạng thái phím liên tục trong hàm `_process()` bằng `Input.is_action_pressed()`.

```gdscript
extends Sprite2D

var speed: float = 400.0

func _process(delta: float):
	var direction := Vector2.ZERO # Vector2(0, 0)
	
	# Godot có sẵn các action "ui_right", "ui_left"... mặc định
	if Input.is_action_pressed("ui_right"):
		direction.x += 1
	if Input.is_action_pressed("ui_left"):
		direction.x -= 1
	if Input.is_action_pressed("ui_down"):
		direction.y += 1
	if Input.is_action_pressed("ui_up"):
		direction.y -= 1
		
	# Cập nhật vị trí
	position += direction * speed * delta
```

## 3. Phân biệt các loại Pressed
- `is_action_pressed(action)`: Trả về `true` **LIÊN TỤC** miễn là bạn đang giữ phím (Dùng để di chuyển).
- `is_action_just_pressed(action)`: Trả về `true` **MỘT LẦN DUY NHẤT** ở khung hình mà phím vừa được nhấn xuống (Dùng để nhảy, bắn súng).
- `is_action_just_released(action)`: Trả về `true` khi vừa thả phím ra.

## 4. Bắt tọa độ Chuột
```gdscript
func _process(delta: float):
	# Nếu bấm chuột trái
	if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		# Lấy tọa độ thế giới (global) của chuột
		var mouse_pos = get_global_mouse_position()
		print("Chuột đang ở: ", mouse_pos)
```

Ở bài sau, chúng ta sẽ học cách để các Node giao tiếp với nhau mà không làm mã nguồn bị rối, thông qua **Hệ thống Signals**!
