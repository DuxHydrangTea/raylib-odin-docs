# Chương 17: Hệ thống Packages, Imports và Phạm vi (Scope)

Phần 5 cuối cùng này sẽ chỉ cho bạn cách sắp xếp và tổ chức code khi dự án Game của bạn phình to ra với hàng chục file và hàng ngàn dòng code.

## 1. Package là gì?

Package (Gói) đơn giản là một **thư mục** chứa các file `.odin`. Khác với C++ phải dùng file `.h` và `.cpp` lằng nhằng, trong Odin, mọi file nằm chung một thư mục tự động thuộc về cùng một Package và có thể nhìn thấy toàn bộ biến, hàm của nhau mà không cần `#include`.

Ở dòng đầu tiên của mỗi file `.odin`, bạn phải khai báo tên package:
```odin
package main
```
Tên package `main` là bắt buộc đối với thư mục chứa hàm `main()`. Các thư mục con khác bạn có thể đặt tên tùy ý (ví dụ: `package vat_ly`, `package am_thanh`).

## 2. Lệnh Import

Để sử dụng code từ một Package khác, ta dùng từ khóa `import`. 

```odin
// Import các thư viện lõi (Core Library) của Odin
import "core:fmt"
import "core:math"

// Import một package do bạn tự viết (nằm trong thư mục phu_tro/toan_hoc)
import toan "phu_tro/toan_hoc"
```
Khi import một package của riêng bạn, bạn có thể đặt một **tên định danh (alias)** cho nó (ví dụ ở trên là `toan`). Sau đó bạn gọi hàm bằng cách gõ `toan.tinh_toan_gi_do()`.

## 3. Phạm vi (Scope) và Truy cập

Trong một file, bạn có thể khai báo biến ở bên trong hàm, hoặc ở bên ngoài hàm (toàn cục - global).

```odin
diem_cao_nhat := 1000 // Biến toàn cục (Global)

main :: proc() {
    mau_hien_tai := 50 // Biến cục bộ (Local)
}
```

**Quy tắc truy cập (Visibility):**
* **Mặc định:** Bất kỳ biến, hằng số, struct hay hàm nào được khai báo ở dạng Global đều có thể được nhìn thấy và sử dụng bởi **bất kỳ file nào khác** nằm trong **cùng một package**.
* **Xuất ra ngoài (Export):** Tương tự, nếu một package khác import package của bạn, họ mặc định cũng được xài toàn bộ các thành phần Global đó.
* **Che giấu (Private):** Nếu bạn muốn viết một hàm ẩn chỉ dùng nội bộ trong file đó, không cho file khác (kể cả cùng package) gọi được, hãy thêm cờ `@(private)` trước hàm.

```odin
@(private)
tinh_toan_bi_mat :: proc() {
    // Không ai ở ngoài file này gọi được hàm này
}
```

## 4. Code mẫu (Đã kiểm tra bằng Odin)

```odin
package main

import "core:fmt"
import "core:math"

diem_cao_nhat := 1000

main :: proc() {
    // Phải ép kiểu 16.0 thành f32 hoặc f64 vì math.sqrt không nhận untyped float
    can_bac_hai := math.sqrt(f32(16.0)) 
    fmt.println("Căn bậc 2 của 16 là:", can_bac_hai)

    mau_hien_tai := 50
    fmt.println("Điểm cao nhất (Global):", diem_cao_nhat)
    fmt.println("Máu (Local):", mau_hien_tai)
}
```
