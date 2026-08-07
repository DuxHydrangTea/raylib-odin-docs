# Bài 5: Vectơ và Toán học trong Game 2D

Lập trình game gắn liền chặt chẽ với toán học, đặc biệt là **Đại số tuyến tính (Vectơ)**. Nhưng đừng lo, Godot đã cung cấp sẵn các hàm tiện ích để bạn không phải tự tính toán phức tạp.

## 1. Vector2 là gì?
Trong không gian 2D, một điểm hay một hướng được biểu diễn bằng `Vector2(x, y)`.
- Trục X: Dương là đi sang phải, Âm là đi sang trái.
- Trục Y: Dương là đi **XUỐNG DƯỚI**, Âm là đi **LÊN TRÊN**. (Hơi ngược với toán học cấp 3, nhưng đây là quy chuẩn của hầu hết game engine).

## 2. Vấn đề di chuyển chéo (Diagonal movement)
Ở Bài 3, chúng ta di chuyển bằng cách cộng dồn hướng `x` và `y`. Nhưng nếu bạn vừa bấm phím Phải và phím Xuống cùng lúc, Vector sẽ là `Vector2(1, 1)`.
Độ dài của vector này (theo định lý Pytago) là `1.414` (Căn bậc 2 của 2). Điều này khiến nhân vật đi chéo **nhanh hơn 41%** so với đi thẳng!

Để giải quyết, ta cần **Chuẩn hóa (Normalize)** vector, tức là đưa độ dài của nó về 1 mà vẫn giữ nguyên hướng.

```gdscript
extends Sprite2D

var speed: float = 300.0

func _process(delta: float):
	# Khởi tạo vector 0
	var direction := Vector2.ZERO 
	
	direction.x = Input.get_axis("ui_left", "ui_right")
	direction.y = Input.get_axis("ui_up", "ui_down")
	
	# CHUẨN HÓA: Nếu độ dài > 1 (đi chéo), ép độ dài về 1
	if direction.length() > 0:
		direction = direction.normalized()
		
	position += direction * speed * delta
```

## 3. Hàm Input.get_vector() (Cách siêu tốc trong Godot 4)
Godot 4 cung cấp một hàm làm sẵn TẤT CẢ những việc trên (lấy input 4 hướng và tự động normalize):

```gdscript
func _process(delta: float):
	# Tự động kết hợp 4 phím và trả về vector đã chuẩn hóa!
	var direction := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	
	position += direction * speed * delta
```

## 4. Nội suy tuyến tính (LERP)
LERP (Linear Interpolation) dùng để di chuyển mượt mà một giá trị từ A đến B. Rất hữu ích cho camera bám theo nhân vật hoặc trượt nhân vật trên mặt băng.

```gdscript
var current_pos = Vector2(0, 0)
var target_pos = Vector2(100, 100)

func _process(delta: float):
	# current_pos sẽ di chuyển dần về phía target_pos với tốc độ 10% mỗi frame
	current_pos = current_pos.lerp(target_pos, 0.1)
```
