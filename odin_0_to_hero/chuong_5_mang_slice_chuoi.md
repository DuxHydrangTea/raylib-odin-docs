# Chương 5: Mảng tĩnh, Slice và Chuỗi

Trong quá trình làm game, bạn hiếm khi chỉ cần xử lý một biến đơn lẻ. Bạn sẽ cần quản lý danh sách máu của nhiều quái vật, một chuỗi tọa độ để vẽ đường đạn, hoặc đơn giản là hiển thị chữ lên màn hình. Đó là lúc chúng ta cần đến các cấu trúc dữ liệu cơ bản.

## 1. Mảng tĩnh (Static Arrays)

Mảng tĩnh là một tập hợp các phần tử có cùng kiểu dữ liệu, được sắp xếp liền kề nhau trong bộ nhớ. Đặc điểm quan trọng nhất của nó là **kích thước được cố định ngay lúc biên dịch (compile-time)** và không thể thay đổi khi chương trình đang chạy.

Cú pháp khai báo: `[kích_thước]Kiểu_dữ_liệu`

```odin
// Khai báo một mảng chứa 3 số nguyên
diem_so: [3]int = {10, 8, 9}

// Nếu bạn lười đếm, hãy dùng [?] và Odin sẽ tự đếm số phần tử
toa_do := [?]f32{1.5, 2.0, -3.14}
```

Để truy cập vào một phần tử, bạn dùng chỉ số (index) nằm trong ngoặc vuông `[]`. Lưu ý: Index trong Odin (và hầu hết ngôn ngữ khác) bắt đầu từ `0`.

```odin
toa_do_x := toa_do[0] // 1.5
toa_do_y := toa_do[1] // 2.0
```

## 2. Slice (Mảng cắt)

Slice là một trong những tính năng mạnh mẽ nhất của Odin. Nó không tự lưu trữ dữ liệu, mà nó chỉ là một **"khung nhìn" (view)** trỏ vào một mảng đã có sẵn. Bên dưới vỏ bọc, một Slice chứa 2 thông tin:
1. Một con trỏ (pointer) trỏ đến phần tử đầu tiên nó quản lý.
2. Độ dài (length) của nó.

Vì sao lại cần Slice? Khi bạn muốn truyền một mảng có 1 triệu phần tử vào một hàm, nếu bạn copy toàn bộ mảng đó sẽ cực kỳ tốn bộ nhớ và chậm. Thay vào đó, bạn chỉ truyền một Slice (rất nhẹ, chỉ gồm pointer và length).

Cú pháp tạo Slice: `mảng[vị_trí_bắt_đầu : vị_trí_kết_thúc]` (Lưu ý: Không bao gồm vị_trí_kết_thúc).

```odin
mang_goc := [5]int{10, 20, 30, 40, 50}

// Tạo một slice lấy 2 phần tử đầu
slice_dau := mang_goc[0:2] // Lấy index 0 và 1 -> [10, 20]

// Có thể bỏ qua số 0 nếu lấy từ đầu
slice_dau_cach_2 := mang_goc[:2] 

// Lấy toàn bộ mảng gốc thành dạng slice
toan_bo_slice := mang_goc[:]
```

**Quan trọng:** Vì Slice chỉ là khung nhìn, nên nếu bạn thay đổi giá trị thông qua Slice, dữ liệu trên mảng gốc cũng sẽ thay đổi theo.

```odin
slice_dau[0] = 999 
// Lúc này mang_goc sẽ trở thành [999, 20, 30, 40, 50]
```

## 3. Chuỗi (String)

Trong Odin, `string` thực chất là một **Slice của các bytes (chứ không phải rune)** và nó là **Bất biến (Immutable)** - nghĩa là bạn không thể sửa trực tiếp nội dung của một chuỗi sau khi đã tạo nó.

```odin
loi_chao := "Xin chào Odin!"
```

Nếu bạn cố gắng sửa nó: `loi_chao[0] = 'a'` -> Trình biên dịch sẽ báo lỗi!

### Ký tự Byte vs Ký tự Unicode (Rune)
Odin mặc định chuỗi được mã hóa bằng UTF-8. 
* Nếu bạn truy cập bằng index `loi_chao[0]`, bạn sẽ nhận được một **byte**, không phải là một ký tự nếu ký tự đó có dấu (như tiếng Việt).
* Độ dài `len(loi_chao)` sẽ trả về số lượng bytes, không phải số ký tự.

### Nối chuỗi
Vì `string` là bất biến, để nối chuỗi bạn không thể đơn giản dùng `+` như các ngôn ngữ cấp cao khác (C#, Java). Bạn cần sử dụng các hàm cấp phát để tạo ra một chuỗi mới. Hàm `fmt.tprintf` rất tiện dụng cho việc này.

```odin
chuoi_1 := "Xin chào"
chuoi_2 := "Odin"
chuoi_moi := fmt.tprintf("%s - %s", chuoi_1, chuoi_2)
```

## 4. Code mẫu (Đã kiểm tra bằng Odin)

```odin
package main

import "core:fmt"

main :: proc() {
    // 1. Mảng tĩnh
    toa_do := [?]f32{1.5, 2.0, -3.14}
    fmt.println("Mảng tọa độ:", toa_do)
    fmt.println("Phần tử đầu tiên:", toa_do[0])
    
    // 2. Slice
    hai_toa_do_dau := toa_do[0:2] 
    fmt.println("Slice 2 phần tử đầu:", hai_toa_do_dau)
    
    hai_toa_do_dau[0] = 99.9 // Thay đổi qua slice
    fmt.println("Mảng gốc bị ảnh hưởng:", toa_do)
    
    // 3. Chuỗi
    loi_chao := "Xin chào Odin!"
    fmt.println("Độ dài (số byte) của chuỗi:", len(loi_chao))
    
    chuoi_moi := fmt.tprintf("%s - %s", loi_chao, "Rất vui được gặp bạn")
    fmt.println("Chuỗi đã nối:", chuoi_moi)
}
```

## Tổng kết chương 5
Mảng và Slice là công cụ cốt lõi khi làm việc với tập hợp dữ liệu. Bạn hãy nhớ quy tắc vàng: "Mảng lưu trữ thật, Slice chỉ là góc nhìn". Ở chương 6, chúng ta sẽ học cách module hóa code bằng cách định nghĩa **Hàm (Functions)** và tìm hiểu về siêu năng lực **Defer**.
