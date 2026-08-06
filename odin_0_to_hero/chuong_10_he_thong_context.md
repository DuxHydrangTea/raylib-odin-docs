# Chương 10: Hệ thống Context (Ngữ cảnh ngầm định)

Hệ thống Context (Ngữ cảnh) là một trong những tính năng độc đáo, mang tính cách mạng nhất của Odin. Nó giải quyết một vấn đề nhức nhối trong C/C++: Làm sao để truyền các biến môi trường (như Logger, Bộ cấp phát bộ nhớ - Allocator) đi khắp mọi nơi mà không phải khai báo chúng vào *tất cả* các tham số của *tất cả* các hàm?

## 1. Context là gì?

Trong Odin, **MỌI HÀM** (procedure) khi được thực thi đều âm thầm mang theo một biến tên là `context`. Biến này giống như một "cái balo" vô hình chứa những công cụ thiết yếu:
* `context.allocator`: Công cụ cấp phát bộ nhớ mặc định (khi bạn gọi lệnh `new`, thực chất nó đang nhờ cái allocator này lấy vùng nhớ).
* `context.logger`: Công cụ ghi log mặc định.
* `context.user_index`: Một con số nguyên bạn có thể tùy ý sử dụng để đánh dấu.

```odin
in_ra_thong_tin :: proc() {
    // Dù không truyền tham số nào, ta vẫn lấy được context
    fmt.println("ID từ context ngầm định:", context.user_index)
}
```

## 2. Sức mạnh của việc "Ghi đè Context" (Overriding Context)

Sức mạnh thực sự của Context là bạn có thể tạo ra một cái balo mới (chứa công cụ mới), và **ép toàn bộ các hàm được gọi bên dưới** phải dùng cái balo mới này!

Ví dụ, bạn muốn một hàm cụ thể không dùng bộ nhớ RAM tiêu chuẩn (Heap) nữa, mà dùng bộ nhớ siêu tốc (Arena Allocator - ta sẽ học ở chương 12). Thay vì phải sửa code của hàng trăm hàm bên trong, bạn chỉ cần ghi đè `context.allocator` ở lớp ngoài cùng. Mọi hàm `new` ở bên trong sẽ ngoan ngoãn nghe theo.

```odin
main :: proc() {
    in_ra_thong_tin() // In ra 0 (Mặc định)

    {
        // 1. Sao chép cái balo hiện tại
        new_context := context 
        
        // 2. Sửa thông số trong balo mới
        new_context.user_index = 999
        
        // 3. Ép toàn bộ khối lệnh này dùng balo mới
        context = new_context
        
        in_ra_thong_tin() // Lúc này hàm sẽ tự động in ra 999!
    } // Hết khối này, balo cũ (context cũ) tự động được phục hồi!
    
    in_ra_thong_tin() // Lại in ra 0
}
```

## 3. Lợi ích khổng lồ khi làm Game

Nhờ có Context, khi bạn muốn chuyển từ việc In log ra màn hình Console sang việc Ghi log ra File (để kiểm tra lỗi sau khi game crash), bạn **không cần sửa một dòng code game logic nào cả**. Bạn chỉ cần ghi đè `context.logger` ở đầu hàm `main()` là xong.

## 4. Code mẫu (Đã kiểm tra bằng Odin)

```odin
package main

import "core:fmt"

in_ra_thong_tin :: proc() {
    fmt.println("ID người dùng từ context:", context.user_index)
}

main :: proc() {
    in_ra_thong_tin() // Dùng context gốc

    {
        new_context := context
        new_context.user_index = 999
        
        // Ghi đè context cục bộ
        context = new_context
        
        in_ra_thong_tin() 
    }
    
    // Tự động khôi phục context gốc
    in_ra_thong_tin() 
}
```
