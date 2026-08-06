# Chương 2: Biến, Hằng số và Kiểu dữ liệu cơ bản

Trong bất kỳ ngôn ngữ lập trình nào, biến và hằng số là nền tảng để lưu trữ dữ liệu. Odin cung cấp một hệ thống kiểu dữ liệu rất rõ ràng, an toàn (type-safe) và thân thiện với lập trình viên.

## 1. Biến (Variables)

Biến là một vùng nhớ dùng để lưu trữ dữ liệu có thể thay đổi được trong quá trình chạy chương trình.

### Khai báo tường minh (Explicit Type)
Cú pháp chuẩn trong Odin là `tên_biến: kiểu_dữ_liệu = giá_trị`. Chú ý dấu hai chấm `:` được sử dụng để phân cách tên biến và kiểu dữ liệu.

```odin
tuoi: int = 25
```

### Khai báo nội suy (Type Inference)
Odin rất thông minh, nó có thể tự đoán kiểu dữ liệu dựa trên giá trị bạn gán. Bạn có thể bỏ qua kiểu dữ liệu và dùng toán tử `:=`.

```odin
ten := "Nguyen Van A" // Odin tự hiểu đây là kiểu string
diem_so := 9.5        // Odin tự hiểu đây là kiểu f64 (số thực)
```
*Lưu ý: Toán tử `:=` chỉ dùng khi khởi tạo biến lần đầu tiên. Khi muốn thay đổi giá trị sau này, bạn chỉ dùng dấu `=`.*

### Khai báo nhiều biến cùng lúc
Bạn có thể khai báo và gán giá trị cho nhiều biến trên cùng một dòng.

```odin
x, y, z: f32 = 1.5, 2.5, 3.5
```

### Khai báo giá trị mặc định (Zero Value)
Nếu bạn khai báo một biến nhưng không gán giá trị khởi tạo, Odin sẽ tự động gán giá trị mặc định (Zero Value) cho nó thay vì để rác trong bộ nhớ (garbage value) như ngôn ngữ C.
* Số nguyên / Số thực sẽ là `0`
* Boolean sẽ là `false`
* Chuỗi sẽ là `""` (chuỗi rỗng)

```odin
mau_sac_mac_dinh: int // Tự động có giá trị là 0
```

## 2. Hằng số (Constants)

Hằng số là những giá trị không bao giờ thay đổi trong suốt quá trình chạy của chương trình. Hằng số trong Odin được xử lý ngay lúc biên dịch (compile-time), giúp tăng tốc độ chạy.

Cú pháp khai báo hằng số sử dụng `::`.

```odin
PI :: 3.14159
MAX_ENEMIES :: 100
GAME_TITLE :: "Siêu Phẩm Odin"
```
Hằng số trong Odin không bị giới hạn về kích thước bộ nhớ lúc biên dịch (Untyped Constants). Nghĩa là `MAX_ENEMIES` ở trên có thể được gán cho một biến `int` (32 bit) hoặc `u8` (8 bit) đều hợp lệ, miễn là giá trị của nó vừa vặn.

## 3. Các Kiểu dữ liệu cơ bản (Basic Types)

Odin có rất nhiều kiểu dữ liệu để bạn tinh chỉnh hiệu năng bộ nhớ (đặc biệt hữu ích khi làm game).

### Số nguyên (Integers)
* **Có dấu (Signed):** `i8`, `i16`, `i32`, `i64`, `i128`. Thường dùng nhất là `int` (kích thước phụ thuộc vào hệ điều hành 32-bit hay 64-bit).
* **Không dấu (Unsigned):** `u8`, `u16`, `u32`, `u64`, `u128`. Thường dùng nhất là `uint`. Chỉ chứa số dương (từ 0 trở lên).
  * Trong game, `u8` thường dùng để biểu diễn giá trị màu sắc (0-255).

```odin
so_nguyen_thuong: int = -100
so_nguyen_8bit: i8 = -128
mau_do: u8 = 255
```

### Số thực (Floating-Point)
Dùng cho tọa độ, tính toán vật lý, v.v.
* `f32`: Số thực 32-bit (Thường dùng nhất trong game).
* `f64`: Số thực 64-bit (Chính xác hơn, thường dùng làm giá trị nội suy mặc định khi gán `:=`).

```odin
trong_luc: f32 = 9.81
```

### Boolean (Đúng / Sai)
Chỉ nhận hai giá trị `true` hoặc `false`. Khai báo là `bool`.

```odin
is_game_over: bool = false
```

### Ký tự và Chuỗi (Rune & String)
* `rune`: Đại diện cho một ký tự Unicode (UTF-8) duy nhất. Dùng dấu nháy đơn `' '`.
* `string`: Đại diện cho một chuỗi các ký tự. Dùng dấu nháy kép `" "`.

```odin
ky_tu_trai_tim: rune = '♥'
loi_chao: string = "Học Odin rất vui!"
```

## 4. Code mẫu tổng hợp

Đoạn code dưới đây tổng hợp tất cả các kiến thức ở trên. Đoạn code này đã được kiểm tra (check syntax) bằng trình biên dịch Odin để đảm bảo tính chính xác tuyệt đối.

```odin
package main

import "core:fmt"

main :: proc() {
    // 1. Biến (Variables)
    tuoi: int = 25
    ten := "Nguyen Van A"
    x, y, z: f32 = 1.5, 2.5, 3.5
    diem_so: int 
    
    fmt.println("Tên:", ten, "- Tuổi:", tuoi, "- Điểm:", diem_so)
    fmt.println("Tọa độ:", x, y, z)

    // 2. Hằng số (Constants)
    PI :: 3.14159
    MAX_ENEMIES :: 100
    
    fmt.println("Số PI:", PI)
    fmt.println("Số lượng kẻ địch tối đa:", MAX_ENEMIES)

    // 3. Kiểu dữ liệu cơ bản (Basic Types)
    so_nguyen_8bit: i8 = -128
    so_nguyen_khong_dau_16bit: u16 = 65535
    so_thuc_32bit: f32 = 3.14
    is_game_over: bool = false
    ky_tu: rune = '🔥'
    chuoi_ky_tu: string = "Học Odin rất vui!"

    fmt.println(so_nguyen_8bit, so_nguyen_khong_dau_16bit, so_thuc_32bit)
    fmt.println("Game over?", is_game_over)
    fmt.println("Ký tự:", ky_tu)
    fmt.println("Chuỗi:", chuoi_ky_tu)
}
```

## Tổng kết chương 2
Bạn đã nắm được cách khai báo biến (`:` và `:=`), hằng số (`::`) và các kiểu dữ liệu nền tảng nhất trong Odin. Đây là những "viên gạch" đầu tiên để xây dựng bất kỳ logic game nào. Ở chương tiếp theo, chúng ta sẽ học cách thao tác với các biến này thông qua các **Toán tử và Ép kiểu**.
