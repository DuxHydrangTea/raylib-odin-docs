# Bài 6: Sinh ra Scene bằng Code (Instancing)

Trong game, bạn thường xuyên phải tạo ra các đối tượng mới khi game đang chạy. Ví dụ: Người chơi bắn ra viên đạn, hệ thống spawn ra quái vật mới. Kỹ thuật này gọi là **Instancing** (Sinh bản sao).

## 1. Nạp (Load) Scene vào bộ nhớ
Trước khi có thể sinh ra bản sao, bạn cần báo cho Godot biết phải lấy "bản gốc" (Scene file `.tscn`) từ đâu. Chúng ta dùng `preload()`.

```gdscript
extends Node2D

# preload() sẽ tải Scene vào RAM ngay khi game bắt đầu
# Giúp việc sinh đạn sau này không bị lag
var bullet_scene: PackedScene = preload("res://bullet.tscn")
```

## 2. Quy trình 3 bước để Instancing
Để tạo một viên đạn bằng code, bạn **LUÔN LUÔN** phải làm đủ 3 bước sau:

```gdscript
extends Node2D

var bullet_scene: PackedScene = preload("res://bullet.tscn")

func _process(delta: float):
	# Nếu vừa nhấn phím cách (Space)
	if Input.is_action_just_pressed("ui_accept"): 
		shoot()

func shoot():
	# BƯỚC 1: Tạo một bản sao (instance) từ PackedScene
	var bullet_instance = bullet_scene.instantiate()
	
	# BƯỚC 2: Thiết lập vị trí (hoặc hướng đi) cho bản sao
	# Ví dụ: đặt viên đạn xuất phát từ đúng vị trí của súng (Node hiện tại)
	bullet_instance.global_position = global_position
	
	# BƯỚC 3: Thêm bản sao đó vào Scene Tree để nó thực sự xuất hiện trong game!
	# (Nếu quên bước này, viên đạn chỉ nằm trong bộ nhớ RAM chứ không hiện ra)
	get_tree().current_scene.add_child(bullet_instance)
```

## 3. Hủy bỏ Node (Xóa khỏi game)
Nếu bạn sinh ra viên đạn liên tục mà không xóa chúng đi khi bay ra ngoài màn hình, máy tính sẽ đầy RAM và giật lag (Memory Leak).

Để xóa một Node an toàn vào cuối khung hình hiện tại, hãy gọi hàm:
```gdscript
queue_free()
```
*Lưu ý: Đừng bao giờ dùng `free()`, luôn luôn dùng `queue_free()` để Godot dọn dẹp an toàn.*
