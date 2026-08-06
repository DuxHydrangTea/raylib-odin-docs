# Chương 19: Viết Test (Testing) cơ bản

Bước cuối cùng để trở thành một lập trình viên "Hero": Bạn phải biết viết Test (Kiểm thử). Test giúp đảm bảo khi bạn thêm tính năng mới vào game, tính năng cũ không bị hỏng (Regression bug).

Thật may mắn, Odin đã tích hợp sẵn một framework Test tuyệt vời ngay trong lõi (package `core:testing`), bạn không cần cài đặt thêm bất kỳ công cụ nào cả.

## 1. Cách viết một Test Case

Để định nghĩa một hàm là hàm test (chỉ chạy khi test, không chạy khi build game thật), bạn dùng "Annotation" (Chú thích) `@(test)` đặt ngay trên đầu hàm.
Hàm test bắt buộc phải nhận một tham số là con trỏ `^testing.T`.

```odin
import "core:testing"

// Đây là logic bạn muốn test
tinh_sat_thuong :: proc(tan_cong: int, phong_thu: int) -> int {
    sat_thuong := tan_cong - phong_thu
    if sat_thuong < 0 { return 0 }
    return sat_thuong
}

// 1. Tạo hàm Test với tiền tố @(test)
@(test)
test_tinh_sat_thuong_am :: proc(t: ^testing.T) {
    ket_qua := tinh_sat_thuong(5, 10)
    
    // 2. Dùng hàm expect để "kỳ vọng" kết quả là đúng
    testing.expect(t, ket_qua == 0, "Sát thương không được âm, phải là 0")
}
```

## 2. Cách chạy Test

Đừng chạy lệnh `odin run` hay `odin build`. Bạn hãy mở terminal và chạy lệnh `test`:

```bash
odin test <tên_file_hoặc_thư_mục>
```
Ví dụ:
```bash
odin test chuong19_test.odin -file
```

Hệ thống sẽ chạy tất cả các hàm `@(test)`, tự động kiểm tra rò rỉ bộ nhớ (Memory Tracking), và báo cáo kết quả (Pass/Fail) cùng thời gian chạy. 
Bạn có thể thử cố tình sửa hàm `tinh_sat_thuong` thành kết quả sai, sau đó chạy lại lệnh test để xem Odin báo màu đỏ lỗi như thế nào.

## 3. Code mẫu (Đã kiểm tra bằng Odin)

```odin
package main

import "core:testing"
import "core:fmt"

tinh_sat_thuong :: proc(tan_cong: int, phong_thu: int) -> int {
    sat_thuong := tan_cong - phong_thu
    if sat_thuong < 0 { return 0 }
    return sat_thuong
}

@(test)
test_tinh_sat_thuong_co_ban :: proc(t: ^testing.T) {
    ket_qua := tinh_sat_thuong(10, 5)
    testing.expect(t, ket_qua == 5, "Sát thương phải là 5")
}

@(test)
test_tinh_sat_thuong_am :: proc(t: ^testing.T) {
    ket_qua := tinh_sat_thuong(5, 10)
    testing.expect(t, ket_qua == 0, "Sát thương không được âm, phải là 0")
}

main :: proc() {
    fmt.println("Hãy mở Terminal và chạy lệnh: odin test chuong_19.odin -file")
}
```

## LỜI KẾT KHÓA HỌC
Chúc mừng bạn! Bạn đã hoàn thành xuất sắc chặng đường **"Odin: Zero to Hero"**.
Từ những biến số cơ bản, vòng lặp, cho tới con trỏ bộ nhớ, Arena Allocator và DOD. Khối kiến thức bạn đang sở hữu lúc này đủ sức để đối đầu với mọi rào cản kỹ thuật khi làm Game với Raylib hay bất kỳ framework nào khác. 

Hãy bắt tay ngay vào những dự án như "Farmer Game" hay "Ninja School" mà bạn đang ấp ủ nhé. Chúc bạn code vui vẻ!
