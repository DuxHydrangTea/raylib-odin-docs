# Bài 10: Getters và Setters (Bảo vệ dữ liệu)

Tính năng cuối cùng làm nên đẳng cấp OOP của GDScript 4 chính là **Properties (Getter / Setter)**. Nó giúp bạn Đóng gói (Encapsulation) dữ liệu, ngăn không cho các Lớp khác gán giá trị "tào lao" làm hỏng game.

## 1. Vấn đề của biến thông thường
Giả sử bạn có biến `hp` (Máu):
```gdscript
var hp: int = 100
```
Nếu một file khác viết nhầm: `player.hp = -9999`, nhân vật của bạn sẽ bị lỗi logic. Chúng ta cần một "Người bảo vệ" đứng canh cửa mỗi khi ai đó muốn đọc (Get) hoặc thay đổi (Set) biến này.

## 2. Cú pháp Get/Set mới nhất của Godot 4

Từ Godot 4, cú pháp khai báo getter/setter đã được làm lại cực kỳ giống với ngôn ngữ Swift và C#, mang lại cảm giác vô cùng hiện đại.

```gdscript
extends Node
class_name Player

# Khai báo biến hp đi kèm với cặp set/get
var hp: int = 100:
	set(value):
		# value là giá trị mà người ta đang cố gán vào
		# Ta chặn đứng nếu họ gán máu < 0
		if value < 0:
			value = 0
			
		hp = value
		
		# Tự động cập nhật UI mỗi khi bị trừ máu!
		print("Máu vừa thay đổi thành: ", hp)
		
	get:
		# Chạy mỗi khi ai đó muốn đọc biến hp
		return hp
```

Bây giờ, nếu từ một file khác, bạn viết:
```gdscript
player.hp = -50
```
Thay vì bị gán bằng `-50`, hàm `set(value)` sẽ nhảy ra chặn lại, ép nó về `0`, và in ra dòng chữ `"Máu vừa thay đổi thành: 0"`. Code gọi thì vẫn y hệt `player.hp` (rất ngắn gọn) nhưng bên trong đã được bảo mật 100%!

## 3. Cú pháp rút gọn (Inline)

Nếu bạn chỉ muốn tạo một biến chỉ-đọc (Read-only), tức là người khác được quyền xem nhưng cấm sửa, bạn có thể viết ngắn gọn:

```gdscript
# Biến max_speed không có hàm set, nên chỉ đọc được!
var max_speed: float:
	get:
		return 300.0

# -----------------
# Hoặc gán thông qua các hàm có sẵn ở đâu đó:
var score: int = 0: set = update_score, get = read_score

func update_score(new_val):
	score = new_val
	
func read_score() -> int:
	return score
```

> [!TIP]
> Dùng Getter/Setter kết hợp với **Signals** (bài 4) là "Combo Hủy Diệt" của Godot. Bên trong hàm `set(value)`, bạn chỉ cần thêm dòng `health_changed.emit(value)`. Vậy là thanh máu UI sẽ tự động tụt xuống mỗi khi biến `hp` thay đổi, mà bạn không cần phải viết hàm update nào ở `_process()` cả!
