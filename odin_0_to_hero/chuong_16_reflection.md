# Chương 16: Polymorphism (Đa hình), kiểu `any` và Reflection

Ở chương cuối cùng của Phần 4, chúng ta sẽ tìm hiểu về cách Odin có thể làm việc với các kiểu dữ liệu không xác định trước.

## 1. Kiểu `any` (Bất kỳ thứ gì)

Odin là ngôn ngữ gõ tĩnh khắt khe (Strict Static Typing). Tuy nhiên, thi thoảng bạn muốn viết một hàm có thể nhận VÀO MỌI THỨ (chẳng hạn như hàm `fmt.println()`).
Đó là lúc kiểu `any` xuất hiện.

Bên dưới vỏ bọc, một biến `any` chứa 2 con trỏ:
1. Con trỏ trỏ tới Dữ liệu thực sự.
2. ID của Kiểu dữ liệu (TypeID).

```odin
// Hàm nhận mọi thứ trên đời
in_thong_tin :: proc(tham_so: any) {
    // Sử dụng switch type (có chữ `in`) để bóc tách kiểu thực sự
    switch v in tham_so {
    case int:
        fmt.println("Đây là một số nguyên:", v)
    case string:
        fmt.println("Đây là một chuỗi:", v)
    case:
        fmt.println("Kiểu lạ quá!")
    }
}
```

## 2. Reflection (Sự phản chiếu)

Reflection là khả năng Chương trình "tự soi gương" và phân tích cấu trúc của chính nó khi ĐANG CHẠY. 
Ứng dụng thực tế lớn nhất trong Game: **Hệ thống Save/Load tự động hoặc Tạo bảng Inspector (UI).** Bạn quăng một Struct `Player` vào, Reflection sẽ tự phân tích nó có những biến gì bên trong, và tự động lưu ra file JSON!

Sử dụng package `core:reflect` và từ khóa `type_info_of`.

```odin
import "core:reflect"

NguoiChoi :: struct {
    ten: string,
    cap_do: int,
}

// Lấy thông tin về cấu trúc NguoiChoi khi ĐANG CHẠY
thong_tin_kieu := type_info_of(NguoiChoi)

fmt.println("Kích thước (bytes):", thong_tin_kieu.size)

// Nếu bạn muốn đào sâu vào để biết nó có 2 trường 'ten' và 'cap_do'
// Bạn có thể xem source code của package core:reflect
```

## Tổng kết phần 4
Chính thức chúc mừng bạn đã tốt nghiệp trường phái "Odin Advanced"! Bạn đã nắm giữ trong tay những bí kíp tối thượng: Tối ưu bộ nhớ với Arena, Multi-threading, Kiến trúc DOD tối cao và khả năng cấy ghép nội tạng thư viện C.
Bạn đã sẵn sàng để viết ra bất kỳ Game Engine nào bằng Odin! Phần 5 cuối cùng sẽ chỉ cho bạn cách Tổ chức và Kiến trúc lại toàn bộ các dự án khổng lồ.
