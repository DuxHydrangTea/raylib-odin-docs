# Bài 8: Lập trình Hướng Đối Tượng (OOP) - Lớp và Khởi tạo

GDScript không chỉ là một ngôn ngữ kịch bản để viết các hàm rời rạc. Kể từ Godot 4, nó đã trở thành một ngôn ngữ Lập trình Hướng Đối Tượng (OOP) đích thực. Ở bài này, chúng ta sẽ học cách tạo ra các bản thiết kế (Class) và sinh ra đối tượng từ chúng.

## 1. Định nghĩa một Lớp bằng `class_name`

Mặc định, mỗi file `.gd` là một Lớp ẩn danh. Để biến nó thành một Lớp công khai (Global Class) mà mọi script khác đều có thể nhận diện, ta dùng từ khóa `class_name` ở ngay đầu file.

```gdscript
# File: Weapon.gd
extends Node
class_name Weapon

var damage: int = 10
var ammo: int = 30

func shoot():
	print("Bắn ra ", damage, " sát thương!")
	ammo -= 1
```

> [!TIP]
> Nhờ có `class_name Weapon`, giờ đây Godot Editor sẽ hiển thị `Weapon` trong danh sách Add Node! Đồng thời bạn có thể dùng nó làm kiểu dữ liệu (Data Type) ở các file khác. VD: `var my_gun: Weapon`.

## 2. Hàm Khởi Tạo (Constructor - `_init`)

Trong C# hay Java, bạn dùng Constructor để gán giá trị mặc định khi tạo mới một Object. Trong GDScript, hàm đó là `_init()`.

```gdscript
# File: Character.gd
class_name Character

var name: String
var hp: int

# Hàm này tự động chạy ngay khi Object được tạo ra bằng lệnh .new()
func _init(char_name: String, starting_hp: int):
	name = char_name
	hp = starting_hp
	print("Đã tạo nhân vật: ", name)
```

## 3. Khởi tạo Đối tượng bằng Code (`.new()`)

Với những Lớp thuần túy chứa dữ liệu (không cần kéo thả vào Scene làm Node), bạn có thể tạo thẳng đối tượng bằng code thông qua hàm `new()`.

```gdscript
# File: Main.gd
extends Node

func _ready():
	# Gọi hàm .new() sẽ kích hoạt hàm _init() bên trong class
	var hero = Character.new("Arthur", 100)
	var boss = Character.new("Dragon", 5000)
	
	print(hero.hp) # In ra: 100
```

## 4. Lớp Nội Bộ (Inner Classes)

Nếu bạn có một class quá nhỏ và chỉ dùng tạm thời, bạn không cần phải tạo file `.gd` mới. Bạn có thể định nghĩa nó ngay bên trong file hiện tại.

```gdscript
# File: Inventory.gd
extends Node

# Định nghĩa một Class con nằm ngay bên trong Inventory
class Item:
	var id: int
	var count: int
	
	func _init(i_id: int, i_count: int):
		id = i_id
		count = i_count

# Sử dụng Inner Class
var my_bag: Array[Item] = []

func _ready():
	my_bag.append(Item.new(1, 50)) # Thêm 50 Bình máu
```

Tính năng OOP này giúp code của bạn gọn gàng, có tổ chức và đậm chất "kỹ sư phần mềm" hơn rất nhiều!
