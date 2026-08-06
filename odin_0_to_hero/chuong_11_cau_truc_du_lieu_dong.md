# Chương 11: Cấu trúc dữ liệu động (Dynamic Array & Map)

Đến lúc này, bạn đã biết mảng tĩnh `[3]int` có một nhược điểm chí mạng: Nó không thể co giãn. Nhưng trong game, số lượng đạn bay trên màn hình luôn thay đổi, số lượng item trong rương đồ cũng liên tục biến động. Chúng ta cần Cấu trúc dữ liệu Động.

Bởi vì kích thước của chúng không được biết trước, nên chúng **luôn được lưu trên Heap** (thông qua `context.allocator`). Đồng nghĩa với việc: **Bạn phải nhớ dọn rác (delete) chúng!**

## 1. Dynamic Array (Mảng động)

Mảng động trong Odin tương tự như `std::vector` trong C++ hay `List` trong C#. Bạn có thể thêm, bớt phần tử tùy ý.

Cú pháp khai báo: `[dynamic]Kiểu_dữ_liệu`. Để tạo nó, ta dùng hàm `make`.

```odin
// Tạo mảng động chứa điểm số
danh_sach_diem := make([dynamic]int)

// DÙNG DEFER LUÔN NGAY SAU MAKE ĐỂ KHÔNG BAO GIỜ QUÊN XÓA!
defer delete(danh_sach_diem)

// Thêm phần tử vào cuối (Push back)
append(&danh_sach_diem, 10)
append(&danh_sach_diem, 20)

// Lấy ra (xóa bỏ) phần tử ở cuối (Pop back)
pop(&danh_sach_diem) // Xóa số 20 đi
```

## 2. Map (Từ điển / Bảng băm)

Nếu Mảng động dùng index `0, 1, 2` để tìm dữ liệu, thì Map cho phép bạn dùng một "Khóa" (Key - ví dụ như Tên quái vật bằng string) để tìm ra một "Giá trị" (Value - lượng HP). Tốc độ tra cứu của Map là cực kỳ khủng khiếp (O(1)).

Cú pháp: `map[Kiểu_Khóa]Kiểu_Giá_Trị`. Cấp phát bằng hàm `make`.

```odin
// Tạo một cuốn từ điển, tra Tên (string) ra Máu (int)
tu_dien_quai_vat := make(map[string]int)
defer delete(tu_dien_quai_vat)

// Thêm dữ liệu
tu_dien_quai_vat["Goblin"] = 50
tu_dien_quai_vat["Dragon"] = 5000

// Kiểm tra xem một Key có tồn tại không
// Hàm này trả về 2 giá trị: Giá trị thật sự, và biến boolean xem nó có tồn tại không
hp, ton_tai := tu_dien_quai_vat["Slime"]

if ton_tai {
    fmt.println("Slime có máu:", hp)
} else {
    fmt.println("Chưa từng ghi nhận Slime trong từ điển!")
}

// Xóa một dữ liệu khỏi từ điển
delete_key(&tu_dien_quai_vat, "Goblin")
```

## 3. Code mẫu (Đã kiểm tra bằng Odin)

```odin
package main

import "core:fmt"

main :: proc() {
    // 1. Mảng động
    danh_sach_diem := make([dynamic]int)
    defer delete(danh_sach_diem)
    
    append(&danh_sach_diem, 10, 20, 30) // Có thể append nhiều giá trị một lúc
    fmt.println("Mảng động:", danh_sach_diem)
    
    pop(&danh_sach_diem)
    fmt.println("Sau khi pop:", danh_sach_diem)
    
    // 2. Map
    tu_dien_quai_vat := make(map[string]int)
    defer delete(tu_dien_quai_vat)
    
    tu_dien_quai_vat["Goblin"] = 50
    tu_dien_quai_vat["Dragon"] = 5000
    
    hp, ton_tai := tu_dien_quai_vat["Slime"]
    if ton_tai {
        fmt.println("Máu Slime:", hp)
    } else {
        fmt.println("Quái vật Slime không tồn tại.")
    }
    
    delete_key(&tu_dien_quai_vat, "Goblin")
}
```

## Tổng kết phần 3
Bạn vừa hoàn tất khóa huấn luyện "cử tạ" với những tạ nặng nhất: Con trỏ, Quản lý bộ nhớ Stack/Heap, Context và cấu trúc động `make/delete`. Xin chúc mừng! 
Ở Phần 4, chúng ta sẽ học kỹ thuật tối ưu hóa bộ nhớ thực sự để làm game AAA bằng **Custom Allocators (Arena)** và khai mở một chân trời tư duy mới mang tên **Data-Oriented Design (DOD)**.
