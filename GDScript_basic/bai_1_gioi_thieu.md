# Bài 1: Giới thiệu & Cú pháp cơ bản GDScript

Chào mừng bạn đến với khóa học **Godot 2D & GDScript**! Trong phần này, chúng ta sẽ làm quen với GDScript - ngôn ngữ kịch bản mạnh mẽ, dễ học và được tối ưu hóa đặc biệt cho Godot Engine.

## GDScript là gì?
GDScript là ngôn ngữ định kiểu động (dynamic typed) nhưng có hỗ trợ định kiểu tĩnh (static typing), cú pháp của nó lấy cảm hứng rất nhiều từ **Python**. Nếu bạn đã từng học Python, bạn sẽ thấy GDScript cực kỳ quen thuộc.

## Cú pháp cơ bản

### 1. Khai báo biến (Variables)
Trong Godot 4, chúng ta sử dụng từ khóa `var` để khai báo biến. Bạn nên sử dụng định kiểu tĩnh (thêm dấu `:` và tên kiểu) để Godot tối ưu tốc độ và gợi ý code tốt hơn.

```gdscript
# Khai báo không định kiểu (dynamic typing)
var player_name = "Hero"
var score = 100

# Khai báo CÓ định kiểu (static typing - Khuyên dùng)
var hp: int = 100
var speed: float = 300.5
var is_alive: bool = true
var weapon_name: String = "Sword"

# Ép kiểu tự động (inferred typing)
var damage := 50 # Godot tự hiểu damage là int vì 50 là số nguyên
```

### 2. Hàm (Functions)
Sử dụng từ khóa `func` để khai báo hàm.

```gdscript
# Hàm cơ bản không trả về giá trị
func say_hello():
    print("Xin chào Godot!")

# Hàm có tham số và định kiểu trả về
func calculate_damage(base_dmg: int, multiplier: float) -> int:
    var final_dmg: int = int(base_dmg * multiplier)
    return final_dmg
```

### 3. Vòng lặp và Điều kiện
Giống như Python, GDScript sử dụng thụt lề (indentation) để phân biệt các khối lệnh thay vì dùng dấu ngoặc nhọn `{}`.

```gdscript
func check_health(current_hp: int):
    if current_hp <= 0:
        print("Player died!")
    elif current_hp < 20:
        print("Warning: Low Health!")
    else:
        print("Player is healthy.")

func count_to_five():
    for i in range(1, 6):
        print(i) # In ra từ 1 đến 5
```

## Tổng kết
Bạn đã nắm được các cú pháp cơ bản nhất của GDScript. Trong bài tiếp theo, chúng ta sẽ tìm hiểu về các khái niệm cốt lõi của Godot như **Node**, **Scene**, và cách gắn một script vào một Node để điều khiển nó!
