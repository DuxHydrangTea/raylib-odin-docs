# Bài 4: Hệ thống Tín hiệu (Signals)

Khi trò chơi phức tạp lên, việc các Node chọc trực tiếp vào code của nhau sẽ làm hỏng cấu trúc game (Spaghetti code). Godot giải quyết việc này bằng **Signals** (Tín hiệu - hay còn gọi là mẫu thiết kế Observer).

## 1. Signal là gì?
Tưởng tượng Signal giống như một cái đài phát thanh.
- Node A phát ra một tín hiệu (Ví dụ: "Tôi vừa chết!"). Node A không cần quan tâm ai đang nghe.
- Node B, Node C (Giao diện máu, Hệ thống điểm) đăng ký "nghe" tín hiệu đó. Khi tín hiệu được phát, các Node B, C sẽ tự động chạy một hàm tương ứng.

## 2. Cách kết nối Signal thông qua giao diện (Editor)
Bất kỳ Node nào cũng có các Signal mặc định. 
Ví dụ một `Button` có signal `pressed()`.
- Chọn Button, nhìn sang cột bên phải (Inspector), chọn tab **Node**.
- Nhấp đúp vào `pressed()`, chọn một script để kết nối. Godot sẽ tự động tạo một hàm `_on_button_pressed()` cho bạn.

## 3. Cách kết nối Signal bằng Code (GDScript)
Trong Godot 4, cú pháp kết nối signal bằng code cực kỳ trong sáng và sạch sẽ.

```gdscript
extends Node2D

# 1. Khai báo một tín hiệu (Signal) tùy chỉnh của riêng bạn
signal player_died(final_score: int)

func _ready():
	# 2. Kết nối tín hiệu bằng code (Godot 4 syntax)
	# Cú pháp: ten_signal.connect(ham_xu_ly)
	player_died.connect(_on_player_died)

func take_damage(amount: int):
	var hp = 100 - amount
	if hp <= 0:
		# 3. Phát tín hiệu (Emit signal) và truyền kèm dữ liệu
		player_died.emit(500)

# 4. Hàm nhận tín hiệu (sẽ tự động chạy khi signal được emit)
func _on_player_died(score: int):
	print("Người chơi đã chết. Điểm số: ", score)
```

## 4. Tại sao phải dùng Signal?
Signal giúp **Decoupling** (Giảm phụ thuộc). Player không cần biết hệ thống Giao diện người dùng (UI) hoạt động ra sao. Player chỉ việc hét lên "Tôi bị đánh trúng", còn UI tự nhận tín hiệu để trừ máu trên màn hình. Điều này giúp dễ dàng tái sử dụng code và gỡ lỗi!
