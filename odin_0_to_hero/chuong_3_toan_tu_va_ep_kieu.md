# Chương 3: Toán tử và Ép kiểu

Trong chương này, chúng ta sẽ tìm hiểu về các toán tử (Operators) để thao tác với biến và cách ép kiểu (Type Casting) giữa các kiểu dữ liệu khác nhau. Odin rất khắt khe về kiểu dữ liệu (Strict Typing), điều này giúp bạn tránh được vô số lỗi ngớ ngẩn (bugs) khi lập trình game.

## 1. Toán tử số học (Arithmetic Operators)

Dùng để thực hiện các phép tính toán cơ bản.

* `+` : Cộng
* `-` : Trừ
* `*` : Nhân
* `/` : Chia (Nếu chia 2 số nguyên, kết quả sẽ bị làm tròn xuống - cắt bỏ phần thập phân).
* `%` : Chia lấy phần dư (Modulo - cực kỳ hữu ích để giới hạn vòng lặp, ví dụ như tạo hoạt ảnh sprite sheet).

```odin
a, b := 10, 3
tong := a + b       // 13
chia_nguyen := a / b // 3 (vì a và b đều là int)
chia_du := a % b    // 1
```

## 2. Toán tử gán (Assignment Operators)

Dùng để gán giá trị mới cho một biến đã tồn tại (Nhớ là dùng `=`, không dùng `:=` nữa).

* `=` : Gán thông thường.
* `+=` : Cộng thêm vào biến hiện tại.
* `-=` : Trừ đi biến hiện tại.
* `*=` : Nhân thêm vào.
* `/=` : Chia đi.

```odin
mau_hien_tai := 100
mau_hien_tai -= 20  // Tương đương: mau_hien_tai = mau_hien_tai - 20
// Lúc này mau_hien_tai = 80
```

## 3. Toán tử so sánh (Comparison Operators)

Dùng để so sánh hai giá trị. Kết quả trả về luôn luôn là một giá trị `bool` (`true` hoặc `false`).

* `==` : Bằng nhau (Lưu ý: 2 dấu bằng, 1 dấu bằng là phép gán).
* `!=` : Khác nhau.
* `>` : Lớn hơn.
* `<` : Nhỏ hơn.
* `>=` : Lớn hơn hoặc bằng.
* `<=` : Nhỏ hơn hoặc bằng.

```odin
diem_nguoi_choi := 500
diem_ky_luc := 1000

pha_ky_luc := diem_nguoi_choi > diem_ky_luc // false
```

## 4. Toán tử logic (Logical Operators)

Dùng để kết hợp các điều kiện với nhau (rất hay dùng trong cấu trúc `if`).

* `&&` : AND (Và). Chỉ `true` khi cả hai vế đều `true`.
* `||` : OR (Hoặc). `true` nếu một trong hai vế `true`.
* `!` : NOT (Phủ định). Đảo ngược kết quả (Từ `true` thành `false` và ngược lại).

```odin
co_chia_khoa := true
cua_bi_khoa := true

// Bạn có thể mở cửa nếu bạn CÓ chìa khóa VÀ cửa BỊ khóa
co_the_mo_cua := co_chia_khoa && cua_bi_khoa // true
```

## 5. Ép kiểu (Type Casting)

Đây là phần **rất quan trọng** trong Odin. Khác với C hay C++, Odin **không bao giờ ép kiểu ngầm định (implicit casting)**. Bạn không thể cộng một số `int` và một số `f32` lại với nhau một cách trực tiếp. Compiler sẽ báo lỗi ngay lập tức. Điều này ép bạn phải rõ ràng về ý định của mình, giúp ngăn chặn lỗi do mất mát dữ liệu.

Cú pháp ép kiểu: `cast(KiểuDữLiệu)biến_cần_ép_kiểu`

```odin
so_nguyen: int = 10
so_thuc: f32 = 2.5

// SAI: Odin sẽ báo lỗi mismatch type
// ket_qua := so_nguyen + so_thuc 

// ĐÚNG: Bạn phải ép kiểu 1 trong 2 biến
ket_qua_f32 := cast(f32)so_nguyen + so_thuc // 12.5 (Kiểu f32)
ket_qua_int := so_nguyen + cast(int)so_thuc // 12 (Kiểu int, bị mất phần thập phân .5)
```
*Ghi chú:* Khi ép kiểu từ số thực (`f32`, `f64`) sang số nguyên (`int`), Odin sẽ luôn **cắt bỏ (truncate)** phần thập phân chứ không làm tròn. (Ví dụ 2.9 ép về int sẽ thành 2).

## 6. Code mẫu tổng hợp (Đã kiểm tra bằng Odin)

Bạn có thể chạy thử đoạn code sau để xem kết quả.

```odin
package main

import "core:fmt"

main :: proc() {
    // 1. Toán tử số học
    a, b := 10, 3
    fmt.println("Cộng:", a + b)
    fmt.println("Chia lấy nguyên:", a / b)
    fmt.println("Chia lấy dư:", a % b)
    
    // 2. Toán tử gán
    x := 5
    x += 2 // x = 7
    x *= 3 // x = 21
    fmt.println("Giá trị x:", x)
    
    // 3. Toán tử so sánh
    mau_nguoi_choi := 100
    mau_quai_vat := 150
    fmt.println("Nhiều máu hơn?", mau_nguoi_choi > mau_quai_vat) // false
    fmt.println("Bằng nhau?", mau_nguoi_choi == mau_quai_vat)    // false
    
    // 4. Toán tử logic
    co_chia_khoa := true
    cua_da_mo := false
    co_the_vao_phong := co_chia_khoa && !cua_da_mo
    fmt.println("Vào phòng được không?", co_the_vao_phong) // true

    // 5. Ép kiểu tường minh (Explicit Casting)
    so_nguyen: int = 10
    so_thuc: f32 = 2.5
    
    ket_qua := cast(f32)so_nguyen + so_thuc
    fmt.println("Kết quả ép kiểu (f32):", ket_qua) // 12.5
    
    ket_qua_int := so_nguyen + cast(int)so_thuc
    fmt.println("Kết quả ép kiểu (int):", ket_qua_int) // 12
}
```

## Tổng kết chương 3
Cú pháp `cast()` là người bạn đồng hành thường xuyên của bạn trong Odin. Sự khắt khe này có vẻ hơi "phiền" lúc đầu, nhưng nó chính là lá chắn bảo vệ bạn khỏi vô số lỗi khó nhằn. Ở chương tiếp theo, chúng sẽ đi sâu vào việc điều khiển luồng của chương trình với **Cấu trúc điều khiển (If, Switch, For)**.
