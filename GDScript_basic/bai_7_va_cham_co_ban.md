# Bài 7: Các loại Node Vật lý và Va chạm (Physics)

Godot Engine đi kèm với một hệ thống vật lý 2D (Physics 2D) cực kỳ mạnh mẽ. Thay vì tự viết code kiểm tra tọa độ xem 2 vật có đè lên nhau không, bạn sẽ dùng các **PhysicsBody**.

## 1. Phân loại PhysicsBody2D
Godot cung cấp 3 loại thân vật lý chính, tùy vào mục đích sử dụng:

1. **StaticBody2D**: 
   - Vật tĩnh, không bị ảnh hưởng bởi trọng lực hay ngoại lực.
   - Dùng làm: Mặt đất, Bức tường, Chướng ngại vật.
2. **RigidBody2D**:
   - Vật chịu sự quản lý 100% của hệ thống Vật lý Godot (có trọng lượng, bị rơi, nảy lên khi va chạm, có ma sát).
   - Dùng làm: Thùng gỗ rơi, Bóng lăn, Chim Angry Birds. (Không nên tự thay đổi `position` của RigidBody bằng code).
3. **CharacterBody2D**:
   - Vật thể được bạn điều khiển hoàn toàn bằng code (`velocity`, `move_and_slide()`), nhưng nó vẫn biết tự dừng lại khi đụng tường (Không bị đi xuyên tường).
   - Dùng làm: Người chơi (Player), Kẻ thù (Enemy).

## 2. CollisionShape2D
Bất kỳ một Body nào cũng **BẮT BUỘC** phải có một Node con là `CollisionShape2D` hoặc `CollisionPolygon2D`. Nó định nghĩa hình dáng thật của vùng va chạm (Hình tròn, Hình chữ nhật).

*Lưu ý: Hình ảnh `Sprite2D` chỉ để mắt người nhìn thấy, máy tính dựa vào `CollisionShape2D` để tính va chạm!*

## 3. Area2D (Vùng Trigger)
`Area2D` không phải là một vật rắn. Nó giống như một tia laser hồng ngoại hoặc một vùng cảm biến. Khi có vật thể đi xuyên qua nó, nó không cản lại, mà nó sẽ **phát tín hiệu (Signal)**.

Cách dùng Area2D làm bẫy:
```gdscript
extends Area2D

func _ready():
	# Kết nối tín hiệu body_entered của Area2D
	body_entered.connect(_on_body_entered)

# Hàm này tự chạy khi có một PhysicsBody2D đi vào vùng Area2D
func _on_body_entered(body: Node2D):
	if body.name == "Player":
		print("Người chơi đã dẫm vào bẫy!")
		
		# Có thể gọi hàm take_damage của Player nếu Player có hàm đó
		if body.has_method("take_damage"):
			body.take_damage(50)
			
		# Hủy cái bẫy này đi
		queue_free()
```

---
**Chúc mừng bạn!** Bằng việc nắm vững 7 bài học cơ bản này, bạn đã có đủ 90% kiến thức nền tảng về GDScript để bắt tay vào làm các dự án game thực tế như game Nông Trại hay RPG.
