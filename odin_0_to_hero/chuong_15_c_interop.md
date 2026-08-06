# Chương 15: Giao tiếp với ngôn ngữ C (C Interoperability)

Một ngôn ngữ không thể sống sót nếu không thể kế thừa di sản đồ sộ của thế giới C/C++. 
Odin tỏa sáng ở điểm này: **Việc gọi một hàm C trong Odin tự nhiên đến mức bạn không nhận ra sự khác biệt.** Đây là lý do binding (gắn kết) thư viện Raylib (viết bằng C) cho Odin lại hoàn hảo đến vậy.

## 1. Import hàm C bằng `foreign`

Cú pháp để định nghĩa một liên kết đến thư viện C cực kỳ đơn giản.

```odin
import "core:c"

// Khai báo liên kết với thư viện hệ thống của C (libc)
foreign import libc_lib "system:c"

// Báo cho Odin biết chúng ta đang xài tiêu chuẩn gọi hàm của C
@(default_calling_convention="c")
foreign libc_lib {
    // Khai báo chữ ký hàm (giống file header .h trong C)
    // --- nghĩa là hàm này không có logic ở file này, hãy tìm nó trong thư viện C
    puts :: proc(s: cstring) -> c.int --- 
    abs  :: proc(j: c.int) -> c.int ---
}
```

## 2. Chuỗi C (cstring) vs Chuỗi Odin (string)

Cần lưu ý sự khác biệt lớn nhất giữa C và Odin là Chuỗi:
* `string` (Odin): Là một slice có chứa độ dài (length). An toàn tuyệt đối.
* `cstring` (C): Là con trỏ trỏ tới vùng nhớ ký tự, kết thúc bằng một ký tự Null `\0`. Không an toàn.

Khi gọi hàm C từ Odin, bạn PHẢI truyền `cstring`.

```odin
// Khai báo cstring trực tiếp (Odin tự động thêm Null terminator ở cuối)
chuoi_c: cstring = "Hello từ hàm puts của C!"

// Gọi hàm C vừa import ở trên
puts(chuoi_c)
```

## 3. Kiểu dữ liệu của C

Để đảm bảo tương thích 100%, bạn nên dùng các kiểu dữ liệu từ package `core:c` khi giao tiếp với C.
* `c.int` (Tương đương `int` trong C).
* `c.float` (Tương đương `float`).
* `c.bool`...

```odin
so_am: c.int = -42
gia_tri_tuyet_doi := abs(so_am)
```

## Tổng kết chương 15
Nếu bạn muốn dùng một thư viện vật lý hay thư viện âm thanh nào đó được viết bằng C, Odin sẵn sàng "mở cửa đón khách" chỉ với vài dòng `foreign import`. Sức mạnh của Cộng đồng C giờ đây đã thuộc về bạn!
