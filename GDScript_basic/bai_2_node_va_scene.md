# Bài 2: Khái niệm cốt lõi - Node và Scene

Trong phần trước, chúng ta đã học về cú pháp GDScript. Tuy nhiên, để làm game trong Godot, bạn phải hiểu được hai khái niệm nền tảng nhất: **Node** và **Scene**.

## 1. Node (Nút) là gì?
**Node** là "viên gạch" cơ bản nhất trong Godot. Mọi thứ trong game của bạn, từ nhân vật, âm thanh, ánh sáng, hình ảnh nền, cho đến camera đều là một Node.

Một Node có các đặc điểm:
- Có một tên gọi (ví dụ: `Player`, `Enemy`).
- Có các thuộc tính (properties) có thể thay đổi (ví dụ: Tọa độ X/Y, màu sắc).
- Có thể có các Node con (Children), tạo thành một cấu trúc cây (Tree).
- Có thể gắn một đoạn code **GDScript** vào để điều khiển nó!

## 2. Scene (Cảnh) là gì?
Khi bạn ghép nhiều Node lại với nhau và lưu thành một nhóm, nhóm đó được gọi là một **Scene**.
Ví dụ:
- Bạn ghép một `Sprite2D` (hình ảnh), một `CollisionShape2D` (vùng va chạm), và một `CharacterBody2D` (vật lý) lại. Bạn lưu chúng thành Scene có tên là `Player.tscn`.
- Scene `Player` này có thể được sử dụng lại (tạo ra nhiều bản sao - Instantiate) trong toàn bộ trò chơi!
- Ngay cả toàn bộ một Màn chơi (Level 1) cũng là một Scene lớn chứa các Scene nhỏ hơn (như Player, Enemy, Vàng).

## 3. Vòng đời của một Node qua GDScript
Khi bạn gắn một Script vào một Node, bạn có thể "móc" (hook) vào vòng đời của nó thông qua các hàm có sẵn của Godot (thường bắt đầu bằng dấu gạch dưới `_`).

Dưới đây là hai hàm quan trọng nhất bạn sẽ dùng liên tục:

```gdscript
extends Sprite2D

# Biến lưu tốc độ di chuyển
var speed: float = 400.0

# Hàm _ready() được gọi MỘT LẦN DUY NHẤT ngay khi Node vừa xuất hiện
# (tức là khi nó được thêm vào Scene Tree)
func _ready():
	print("Hello từ Node: ", name)
	
	# Đặt vị trí ban đầu của Node này
	position = Vector2(100, 100)

# Hàm _process(delta) được gọi LIÊN TỤC ở mỗi khung hình (frame)
# Thường là 60 lần 1 giây. Dùng để cập nhật di chuyển, trạng thái...
func _process(delta: float):
	# delta là khoảng thời gian (giây) trôi qua kể từ khung hình trước.
	# Nhân với delta giúp game chạy đều đặn trên cả máy yếu và máy mạnh!
	position.x += speed * delta
```

## 4. Tóm tắt
- **Node**: Thành phần nhỏ nhất cấu tạo nên game.
- **Scene**: Một cụm các Node ghép lại để tạo thành một đối tượng hoàn chỉnh.
- **_ready()**: Hàm chạy 1 lần khi bắt đầu.
- **_process(delta)**: Hàm chạy liên tục mỗi khung hình.

Ở bài tiếp theo, chúng ta sẽ bắt đầu sử dụng GDScript để bắt các tín hiệu Input từ người chơi (Bấm phím, Click chuột) nhé!
