# Bài 9: Kế Thừa (Inheritance) và Đa Hình (Polymorphism)

Khái niệm cốt lõi thứ hai của OOP là Kế thừa. Khi làm game, bạn sẽ nhận thấy "Quái vật Slime" và "Quái vật Orc" có 80% logic giống hệt nhau (đều có máu, đều biết đi, đều nhận sát thương). Thay vì copy-paste code, ta dùng Kế thừa!

## 1. Từ khóa `extends`

Ta tạo ra một class cha tên là `Enemy`.

```gdscript
# File: Enemy.gd
extends CharacterBody2D
class_name Enemy

var hp: int = 100
var speed: float = 50.0

func take_damage(amount: int):
	hp -= amount
	print(self.name, " bị trừ ", amount, " máu!")
	if hp <= 0:
		die()

func die():
	print(self.name, " đã chết!")
	queue_free()
```

Bây giờ, tạo một con Boss. Nó KẾ THỪA toàn bộ khả năng của `Enemy`.

```gdscript
# File: Boss.gd
extends Enemy # Trỏ về Class cha!
class_name Boss

func _ready():
	# Mặc dù file Boss.gd không có khai báo hp, nhưng nó được hưởng thừa kế từ Enemy
	hp = 5000 
	speed = 20.0
```

## 2. Ghi đè hàm (Overriding) và hàm `super()`

Giả sử Boss khi nhận sát thương thì được giảm 50% damage nhờ giáp dày. Ta sẽ "Ghi đè" (Override) lại hàm `take_damage()` của cha nó.

```gdscript
# File: Boss.gd
extends Enemy
class_name Boss

# Khai báo lại hàm take_damage để ghi đè (Override)
func take_damage(amount: int):
	var real_damage = amount / 2
	print("Boss dùng khiên chặn nửa sát thương!")
	
	# Gọi NGƯỢC LẠI hàm take_damage() của class Enemy (Lớp Cha)
	# Từ khóa super() giúp ta không phải viết lại logic trừ máu, báo tử vong...
	super(real_damage)
```

> [!WARNING]
> Việc gọi `super()` là chìa khóa vàng trong tính năng kế thừa. Nếu bạn không gọi `super()`, hàm `take_damage` của Lớp cha sẽ bị "bỏ quên" hoàn toàn và Boss sẽ không bao giờ chết!

## 3. Đa Hình (Polymorphism)

Đa hình hiểu đơn giản là: Cùng một lời gọi hàm, nhưng mỗi đối tượng con lại có cách phản ứng khác nhau.

```gdscript
# File: Main.gd
extends Node

var enemies: Array[Enemy] = []

func _ready():
	var normal_orc = Enemy.new()
	var final_boss = Boss.new()
	
	enemies.append(normal_orc)
	enemies.append(final_boss)
	
	# Đa hình ở đây:
	for e in enemies:
		e.take_damage(100)
		
	# - Đối với normal_orc, nó sẽ gọi take_damage() của lớp Enemy (mất 100 máu)
	# - Đối với final_boss, nó sẽ gọi take_damage() của lớp Boss (bị chia nửa, chỉ mất 50 máu)
```

Với Kế thừa và Đa hình, bạn có thể thiết kế một hệ thống cả trăm loại súng hoặc hàng chục loại phép thuật vô cùng dễ dàng mà không lo bị phình code (Code bloat).
