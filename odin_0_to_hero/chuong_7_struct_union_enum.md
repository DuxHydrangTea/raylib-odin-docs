# Chương 7: Struct, Union, Enum và Bit_Set

Khi lập trình game, một nhân vật (`Player`) không chỉ là một số nguyên hay một chuỗi. Nó bao gồm Tọa độ (X, Y), Máu (HP), Tên, v.v. Để quản lý những dữ liệu phức tạp như vậy, chúng ta cần tự định nghĩa các kiểu dữ liệu mới.

## 1. Struct (Cấu trúc dữ liệu)

Struct giúp bạn đóng gói nhiều biến khác nhau thành một thực thể duy nhất. Đây là "xương sống" của việc mô hình hóa thế giới game.

```odin
// Khai báo một Struct
Vector2 :: struct {
    x: f32,
    y: f32,
}

Player :: struct {
    name: string,
    pos:  Vector2, // Struct có thể nằm bên trong Struct khác!
    hp:   int,
}
```

**Khởi tạo Struct:**
```odin
// Cách 1: Khởi tạo với tên biến (rõ ràng, khuyên dùng)
p1 := Player{
    name = "Hero",
    pos = {10.5, 20.0}, // Khởi tạo lồng nhau rất dễ dàng
    hp = 100,
}

// Lấy thông tin bằng dấu chấm (.)
toa_do_x := p1.pos.x
```

## 2. Enum (Kiểu liệt kê)

Trong game, nhân vật của bạn sẽ có các trạng thái: Đứng yên, Chạy, Nhảy, Đánh... Nếu dùng số nguyên (`0`, `1`, `2`) để đánh dấu thì code sẽ rất khó đọc. Enum sinh ra để đặt tên cho các con số này.

```odin
GameState :: enum {
    Menu,      // Mặc định là 0
    Playing,   // 1
    Paused,    // 2
    GameOver,  // 3
}
```

Odin rất thông minh, khi bạn gán hoặc so sánh enum, bạn có thể bỏ qua tên kiểu (GameState) và chỉ cần dùng dấu chấm `.`.

```odin
state := GameState.Playing

// Thay vì viết state == GameState.Playing, bạn chỉ cần:
if state == .Playing {
    fmt.println("Game đang chơi")
}
```

Bạn cũng có thể ép kích thước bộ nhớ cho Enum (ví dụ dùng `u8` để tiết kiệm RAM) và chỉ định giá trị cụ thể.

```odin
ItemType :: enum u8 {
    Weapon = 1,
    Potion = 2,
}
```

## 3. Bit_Set (Tập hợp Bit - Tính năng "sát thủ" của Odin)

Đây là tính năng độc nhất và vô cùng mạnh mẽ của Odin, đặc biệt phù hợp cho lập trình game. 
Thử tưởng tượng nhân vật của bạn có thể vừa Bị trúng độc, vừa Đang tàng hình. Làm sao để lưu 2 trạng thái này cùng lúc một cách hiệu quả? Dùng `bit_set`!

Bên dưới vỏ bọc, nó lưu trữ dữ liệu dưới dạng các bit `0` và `1` (cực kỳ nhanh và nhẹ), nhưng cú pháp lại giống như đang thao tác với một tập hợp trong toán học.

```odin
// 1. Tạo một enum các cờ (flags)
EntityFlag :: enum {
    Is_Dead,
    Is_Flying,
    Is_Invisible,
}

// 2. Tạo một bit_set từ enum trên
EntityFlags :: bit_set[EntityFlag]
```

**Cách sử dụng Bit_Set:**
```odin
// Khởi tạo nhân vật Đang bay và Đang tàng hình
flags: EntityFlags = {.Is_Flying, .Is_Invisible}

// Thêm trạng thái Bị chết
flags += {.Is_Dead}

// Hết tàng hình (Xóa trạng thái)
flags -= {.Is_Invisible}

// Kiểm tra nhân vật có đang bay không (dùng từ khóa `in`)
if .Is_Flying in flags {
    fmt.println("Nhân vật đang trên không trung!")
}
```

## 4. Union (Kiểu hỗn hợp / Đa hình)

`Union` trong Odin là **Tagged Union** (giống `std::variant` trong C++). Nó cho phép một biến có thể chứa MỘT trong NHIỀU kiểu dữ liệu khác nhau một cách an toàn.

Rất phù hợp để làm hệ thống ECS (Entity Component System) hoặc trả về các sự kiện đa dạng.

```odin
Enemy :: struct { damage: int }
NPC   :: struct { dialogue: string }

// Một thực thể EntityData có thể LÀ quái vật, HOẶC là NPC
EntityData :: union {
    Enemy,
    NPC,
}
```

Để biết lúc chạy thực sự nó đang chứa cái gì, ta dùng `switch` kết hợp từ khóa `in`.

```odin
data: EntityData = Enemy{damage = 50}
    
switch v in data {
case Enemy:
    fmt.println("Đây là quái vật, nó đánh mất", v.damage, "HP")
case NPC:
    fmt.println("Đây là NPC, nó nói:", v.dialogue)
}
```

## 5. Code mẫu (Đã kiểm tra bằng Odin)

```odin
package main

import "core:fmt"

Vector2 :: struct { x, y: f32 }
Player :: struct { name: string, pos: Vector2 }

GameState :: enum { Menu, Playing, GameOver }

EntityFlag :: enum { Is_Poisoned, Is_Flying }
EntityFlags :: bit_set[EntityFlag]

EntityData :: union { Player, string }

main :: proc() {
    // 1. Struct
    p1 := Player{name = "Hero", pos = {10.5, 20.0}}
    
    // 2. Enum
    state := GameState.Playing
    if state == .Playing { fmt.println("Đang chơi!") }
    
    // 3. Bit_Set
    flags: EntityFlags = {.Is_Poisoned}
    flags += {.Is_Flying}
    
    if .Is_Flying in flags { fmt.println("Nhân vật đang bay và bị trúng độc!") }
    
    // 4. Union
    data: EntityData = p1
    switch v in data {
    case Player:
        fmt.println("Đây là người chơi:", v.name)
    case string:
        fmt.println("Đây là chuỗi")
    }
}
```

## Tổng kết chương 7
Bạn đã học cách tạo ra các kiểu dữ liệu phong phú để mô phỏng thế giới game. Điểm nhấn lớn nhất là `bit_set`, hãy tận dụng nó để xử lý các trạng thái phức tạp. Tới đây, bạn đã hoàn thành **Phần 2: Cấu trúc dữ liệu và Hàm**. Bạn đã đủ sức để mô hình hóa mọi đối tượng trong game của mình.
