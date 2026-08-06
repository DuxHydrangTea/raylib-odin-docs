# Chương 4: Cấu trúc điều khiển (Control Flow)

Cấu trúc điều khiển giúp chúng ta đưa ra quyết định (nhánh rẽ) và thực hiện các hành động lặp đi lặp lại. Đây là phần cốt lõi để tạo nên "trí tuệ" cho game, từ logic AI của quái vật đến việc kiểm tra điều kiện thắng/thua.

Odin cung cấp 3 cấu trúc chính: `if / else`, `switch`, và `for`. Đáng chú ý là Odin không yêu cầu bạn phải bọc điều kiện trong dấu ngoặc đơn `()`, giúp code trông thoáng và sạch hơn rất nhiều.

## 1. Lệnh if / else

Lệnh `if` kiểm tra một điều kiện (phải trả về `bool`). Nếu đúng, khối lệnh bên trong sẽ được chạy.

```odin
mau_so := 30

if mau_so > 50 {
    fmt.println("An toàn!")
} else if mau_so > 20 {
    fmt.println("Cảnh báo!")
} else {
    fmt.println("Nguy hiểm!")
}
```

### Biến khởi tạo cục bộ trong lệnh `if`
Đây là một tính năng cực kỳ tuyệt vời của Odin. Bạn có thể khởi tạo một biến ngay bên trong dòng lệnh `if`. Biến này chỉ tồn tại bên trong khối lệnh `if` đó. Điều này giúp bộ nhớ gọn gàng và tránh khai báo quá nhiều biến toàn cục không cần thiết.

```odin
// Khởi tạo biến random_value, sau đó phẩy (;) và viết điều kiện kiểm tra
if random_value := 8; random_value > 5 {
    // Biến random_value chỉ được sử dụng trong cặp ngoặc nhọn này
    fmt.println("Giá trị lớn hơn 5:", random_value)
}
// Nếu gọi random_value ở ngoài này, chương trình sẽ báo lỗi
```

## 2. Lệnh switch

Khi bạn có quá nhiều `else if` kiểm tra cùng một biến, lệnh `switch` là lựa chọn thay thế hoàn hảo để code dễ đọc hơn.
Đặc biệt ở Odin, các khối `case` **không tự động chạy tuột xuống (no implicit fallthrough)** giống như C hay C++. Nghĩa là bạn không cần phải viết chữ `break` ở cuối mỗi case.

```odin
trang_thai := 2

switch trang_thai {
case 0:
    fmt.println("Đứng yên")
case 1:
    fmt.println("Đang chạy")
case 2, 3: // Bạn có thể gộp nhiều case lại với nhau bằng dấu phẩy
    fmt.println("Đang tấn công hoặc phòng thủ")
case: // Một case để trống tương đương với "default" trong C
    fmt.println("Không xác định")
}
```

## 3. Vòng lặp for

Ngược lại với nhiều ngôn ngữ có cả `while`, `do-while`, `for`..., Odin chỉ dùng **một từ khóa duy nhất** là `for` cho mọi loại vòng lặp.

### Vòng lặp kiểu C truyền thống
Rất quen thuộc, gồm 3 phần: Khởi tạo ; Điều kiện ; Bước nhảy.
```odin
for i := 0; i < 3; i += 1 {
    fmt.print(i, " ") // Kết quả: 0 1 2 
}
```

### Vòng lặp Range (Khoảng giá trị)
Đây là cách ngắn gọn và hiện đại nhất để lặp qua một khoảng số đếm.
* `..=` hoặc `=..` : Bao gồm điểm cuối (Inclusive).
* `..<` hoặc `<..` : Không bao gồm điểm cuối (Exclusive).

```odin
// Từ 0 đến 4 (không bao gồm 5)
for j in 0..<5 {
    fmt.print(j, " ") // Kết quả: 0 1 2 3 4
}

// Từ 1 đến 3 (bao gồm cả 3)
for k in 1..=3 {
    fmt.print(k, " ") // Kết quả: 1 2 3
}
```

### Vòng lặp vô hạn (Thay thế cho `while(true)`)
Chỉ cần viết `for` không kèm điều kiện. Rất hay dùng cho Vòng lặp Game (Game Loop) chính. Để thoát ra giữa chừng, ta dùng từ khóa `break`.
Để bỏ qua lần lặp hiện tại và đi tới lần lặp tiếp theo, ta dùng từ khóa `continue`.

```odin
dem := 0
for {
    dem += 1
    if dem == 3 {
        break // Thoát hoàn toàn khỏi vòng lặp
    }
}
```

## 4. Code mẫu tổng hợp (Đã kiểm tra bằng Odin)

Bạn có thể chạy thử đoạn code sau.

```odin
package main

import "core:fmt"

main :: proc() {
    // 1. Lệnh if / else
    mau_so := 30
    
    if mau_so > 50 {
        fmt.println("An toàn!")
    } else if mau_so > 20 {
        fmt.println("Cảnh báo!")
    } else {
        fmt.println("Nguy hiểm!")
    }

    // if với biến khởi tạo cục bộ
    if random_value := 8; random_value > 5 {
        fmt.println("Giá trị random lớn hơn 5:", random_value)
    }

    // 2. Lệnh switch
    trang_thai := 2
    
    switch trang_thai {
    case 0:
        fmt.println("Đứng yên")
    case 1:
        fmt.println("Đang chạy")
    case 2, 3:
        fmt.println("Đang tấn công hoặc phòng thủ")
    case:
        fmt.println("Không xác định")
    }

    // 3. Vòng lặp for
    fmt.println("Đếm từ 0 đến 2:")
    for i := 0; i < 3; i += 1 {
        fmt.print(i, " ")
    }
    fmt.println()

    // Vòng lặp range
    fmt.println("Vòng lặp range (0..<5):")
    for j in 0..<5 { 
        fmt.print(j, " ")
    }
    fmt.println()

    fmt.println("Vòng lặp range (1..=3):")
    for k in 1..=3 { 
        fmt.print(k, " ")
    }
    fmt.println()

    // Vòng lặp vô hạn
    dem := 0
    for {
        dem += 1
        if dem == 3 {
            fmt.println("Đã đếm đến 3, thoát vòng lặp!")
            break 
        }
    }
}
```

## Tổng kết phần 1
Chúc mừng bạn! Qua 4 chương đầu, bạn đã có đủ lượng kiến thức nền tảng (Biến, Toán tử, Cấu trúc điều khiển) để viết được các chương trình có logic xử lý phức tạp.
Ở phần 2, chúng ta sẽ bắt đầu làm việc với việc lưu trữ và tổ chức nhiều dữ liệu cùng lúc thông qua **Mảng tĩnh, Slice và Chuỗi**.
