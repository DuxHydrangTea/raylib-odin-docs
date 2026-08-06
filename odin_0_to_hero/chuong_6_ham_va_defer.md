# Chương 6: Hàm (Functions) và Defer

Khi chương trình game lớn dần, việc nhét tất cả code vào hàm `main()` sẽ biến nó thành một đống bùng nhùng (spaghetti code). Chúng ta cần chia nhỏ code ra thành các khối logic có thể tái sử dụng, gọi là **Hàm (Functions)** - mà trong Odin được gọi là **Procedures** (`proc`).

## 1. Khai báo Hàm cơ bản

Một hàm trong Odin được khai báo với từ khóa `proc`. Nó nhận các tham số (parameters) đầu vào và có thể trả về một kết quả đầu ra.

Cú pháp:
`tên_hàm :: proc(tham_số: kiểu) -> kiểu_trả_về { ... }`

```odin
// Hàm nhận 2 số nguyên và trả về 1 số nguyên
tinh_tong :: proc(a: int, b: int) -> int {
    return a + b
}
```

Và bạn có thể gọi nó từ hàm `main`:
```odin
ket_qua := tinh_tong(5, 10) // 15
```

## 2. Hàm trả về nhiều giá trị (Multiple Return Values)

Đây là một tính năng cực kỳ tiện lợi mà C/C++ không có một cách tự nhiên. Trong game, bạn thường cần trả về nhiều thông tin cùng lúc, ví dụ: Tọa độ x và y mới sau khi di chuyển. Odin hỗ trợ điều này rất thanh lịch.

```odin
// Hàm này trả về 2 số nguyên
chia_lay_nguyen_va_du :: proc(a: int, b: int) -> (int, int) {
    if b == 0 { 
        return 0, 0 // Tránh lỗi chia cho 0
    }
    return a / b, a % b
}
```
Để nhận kết quả, bạn dùng dấu phẩy để gán cho nhiều biến:
```odin
nguyen, du := chia_lay_nguyen_va_du(10, 3)
```

### Đặt tên cho biến trả về (Named Return Values)
Bạn có thể đặt tên luôn cho các biến trả về ngay trên chữ ký của hàm. Điều này có 2 lợi ích:
1. Làm code dễ đọc hơn (Documentation).
2. Các biến này tự động được khởi tạo giá trị mặc định (Zero value).
3. Chỉ cần gọi `return` trơn, Odin tự động hiểu và gom các biến đã đặt tên trả về.

```odin
tinh_tong_hieu :: proc(a: int, b: int) -> (tong: int, hieu: int) {
    tong = a + b // Không cần dùng := vì biến đã được khai báo ở trên
    hieu = a - b
    return // Tự động trả về giá trị hiện tại của 'tong' và 'hieu'
}
```

## 3. Siêu năng lực "Defer"

`defer` là một từ khóa kỳ diệu. Khi bạn dùng `defer` kèm một dòng lệnh, dòng lệnh đó sẽ **BỊ TRÌ HOÃN (hoãn lại)** và chỉ được chạy **NGAY TRƯỚC KHI** thoát khỏi phạm vi hiện tại (thường là trước dấu ngoặc nhọn đóng `}`).

Tại sao nó lại quan trọng? Khi làm game, bạn mở một file lưu trữ, bạn phải nhớ đóng nó. Bạn cấp phát một vùng nhớ, bạn phải nhớ giải phóng nó. Nếu bạn có quá nhiều nhánh `return` trong hàm, bạn rất dễ quên đóng file, dẫn đến rò rỉ bộ nhớ (Memory Leak). `defer` sinh ra để giải quyết việc này.

```odin
doc_file_config :: proc() {
    fmt.println("1. Mở file cấu hình")
    
    // Ngay sau khi mở thành công, ta dùng defer để đảm bảo file sẽ luôn được đóng
    defer fmt.println("3. Đóng file (Tự động chạy cuối hàm)")
    
    fmt.println("2. Đang đọc dữ liệu...")
    
    // Dù bạn có return ở đâu, lệnh defer cũng sẽ được chạy trước khi thoát!
    return 
}
```
*Kết quả in ra sẽ là: 1 -> 2 -> 3.*

Bạn không bao giờ phải lo lắng về việc quên dọn dẹp "bãi chiến trường" nữa. 

## 4. Code mẫu (Đã kiểm tra bằng Odin)

```odin
package main

import "core:fmt"

tinh_tong_hieu :: proc(a: int, b: int) -> (tong: int, hieu: int) {
    tong = a + b
    hieu = a - b
    return 
}

chia_lay_nguyen_va_du :: proc(a: int, b: int) -> (int, int) {
    if b == 0 { return 0, 0 }
    return a / b, a % b
}

main :: proc() {
    // 1. Trả về nhiều giá trị
    t, h := tinh_tong_hieu(20, 5)
    fmt.println("Tổng:", t, "Hiệu:", h)
    
    nguyen, du := chia_lay_nguyen_va_du(10, 3)
    fmt.println("Chia nguyên:", nguyen, "Chia dư:", du)
    
    // 2. Demo Defer
    {
        fmt.println("A. Mở một cái gì đó")
        defer fmt.println("C. Tự động dọn dẹp")
        
        fmt.println("B. Làm việc với nó")
    } // Lệnh ở defer sẽ chạy ngay tại đây
}
```

## Tổng kết chương 6
Hàm giúp bạn tái sử dụng logic, còn `defer` giúp code của bạn an toàn và sạch sẽ. Bước tiếp theo, chúng ta sẽ bước vào Chương 7: **Kiểu dữ liệu tùy chỉnh**, nơi bạn sẽ học cách nhóm nhiều biến lại thành một thực thể như `Player` hoặc `Enemy`.
