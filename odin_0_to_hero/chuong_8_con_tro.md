# Chương 8: Con trỏ, Tham chiếu và Số học con trỏ

Chào mừng bạn đến với Phần 3! Ở phần này, chúng ta sẽ làm quen với những khái niệm làm nên sức mạnh tuyệt đối của ngôn ngữ hướng hệ thống như Odin: Con trỏ và Bộ nhớ. Nếu bạn nắm vững phần này, hiệu năng game của bạn sẽ không có đối thủ.

## 1. Con trỏ (Pointers) là gì?

Mỗi khi bạn tạo ra một biến, máy tính sẽ cấp cho biến đó một **địa chỉ bộ nhớ** (giống như địa chỉ nhà) và cất dữ liệu vào đó. 
**Con trỏ** đơn giản chỉ là một biến, nhưng thay vì chứa dữ liệu (như số `10`, chữ `"A"`), nó lại **chứa địa chỉ nhà** của biến khác.

* Dấu `^` đứng trước kiểu dữ liệu dùng để khai báo kiểu con trỏ: `^int` (Con trỏ trỏ đến một số int).
* Dấu `&` đứng trước tên biến dùng để **Lấy địa chỉ (Tham chiếu - Reference)**.
* Dấu `^` đứng *sau* con trỏ dùng để **Truy xuất dữ liệu (Giải tham chiếu - Dereference)**.

```odin
so_nguyen := 42

// 1. Tham chiếu: Lấy địa chỉ của 'so_nguyen' gán cho 'con_tro'
con_tro: ^int = &so_nguyen

// 2. Giải tham chiếu: Đi tới địa chỉ đó và sửa dữ liệu thành 100
con_tro^ = 100

// Lúc này biến 'so_nguyen' ban đầu đã mang giá trị 100!
```

## 2. Số học con trỏ (Pointer Arithmetic)

Đôi khi bạn muốn "nhích" địa chỉ đi một chút để đọc dữ liệu tiếp theo trong bộ nhớ (điều này rất hay dùng khi xử lý mảng dữ liệu đồ họa).
Tuy nhiên, khác với C/C++ cho phép bạn cộng trừ con trỏ loạn xạ (`ptr + 1`), Odin **nghiêm cấm** việc cộng trực tiếp con trỏ với số nguyên nhằm đảm bảo an toàn.

Thay vào đó, để di chuyển con trỏ một cách an toàn, bạn phải sử dụng hàm `ptr_offset` từ package `core:mem`.

```odin
import "core:mem"

mang := [3]int{10, 20, 30}
ptr := &mang[0] // Trỏ vào phần tử đầu tiên (số 10)

// Di chuyển con trỏ tiến lên 1 phần tử (sẽ trỏ vào số 20)
ptr_next := mem.ptr_offset(ptr, 1)
```
*Ghi chú:* Thực tế trong Odin, bạn nên dùng **Slice** để thao tác với mảng sẽ an toàn và dễ dàng hơn dùng Số học con trỏ rất nhiều. Chỉ dùng số học con trỏ khi bạn thực sự phải giao tiếp với thư viện C bên ngoài.

## 3. Code mẫu (Đã kiểm tra bằng Odin)

```odin
package main

import "core:fmt"
import "core:mem"

main :: proc() {
    // Demo con trỏ
    so_nguyen := 42
    con_tro: ^int = &so_nguyen
    
    fmt.println("Giá trị ban đầu:", so_nguyen)
    fmt.println("Địa chỉ bộ nhớ:", con_tro)
    
    con_tro^ = 100 // Đổi dữ liệu thông qua con trỏ
    fmt.println("Giá trị sau khi sửa:", so_nguyen)

    // Demo di chuyển con trỏ
    mang := [3]int{10, 20, 30}
    ptr := &mang[0]
    
    ptr_next := mem.ptr_offset(ptr, 1)
    fmt.println("Giá trị tại phần tử thứ 2:", ptr_next^) // In ra 20
}
```
