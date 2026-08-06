# Chương 12: Allocators cơ bản và Custom Allocators (Arena)

Chào mừng bạn đến với **Phần 4: Odin Nâng cao**. Nếu Bộ nhớ là thanh kiếm, thì Allocator chính là nghệ thuật múa kiếm. Khả năng tùy biến Allocator là vũ khí tối thượng giúp game viết bằng Odin vượt mặt các ngôn ngữ khác về hiệu năng.

## 1. Allocator là gì?

Allocator (Bộ cấp phát) là một đoạn code chịu trách nhiệm đi xin RAM từ hệ điều hành và phân phát cho bạn mỗi khi bạn gọi `new` hoặc `make`.
Theo mặc định, Odin sử dụng **General Purpose Allocator (GPA)** - giống hàm `malloc` trong C. Nó tốt cho mọi trường hợp, nhưng vì phải xử lý nhiều thứ nên tốc độ của nó không phải là nhanh nhất.

## 2. Vấn đề "Phân mảnh bộ nhớ" (Memory Fragmentation)

Hãy tưởng tượng RAM của bạn là một bãi gửi xe. Game liên tục tạo và xóa quái vật, đạn, hiệu ứng... (giống xe ra vào liên tục). Dần dần, bãi xe sẽ lởm chởm những khoảng trống nhỏ lẻ. Khi bạn cần xin một khoảng trống LỚN (vd: Load một hình ảnh to), bãi xe không còn chỗ nào liền mạch đủ to nữa, dẫn đến văng game! C/C++ thường xuyên bị lỗi này.

Giải pháp hoàn hảo: **Arena Allocator**.

## 3. Arena Allocator (Vị cứu tinh của Game)

Arena (Đấu trường) hoạt động như sau:
1. Bạn xin hệ điều hành một cục RAM khổng lồ **ngay từ đầu** (Ví dụ: 100 Megabyte).
2. Khi game chạy, mỗi khi bạn cần cấp phát (`new`), Arena chỉ đơn giản là cắt một mẩu nhỏ từ cục 100MB đó cho bạn (Phép tính này cực kỳ nhanh, chỉ là dịch chuyển một con trỏ).
3. **Cái hay nhất:** Bạn KHÔNG CẦN phải xóa (free) từng thứ một. Khi chuyển cảnh, hoặc kết thúc một Frame, bạn chỉ cần gọi 1 lệnh duy nhất để dọn SẠCH SÀNH SANH toàn bộ 100MB đó chỉ trong nháy mắt (O(1)). Không bao giờ lo Memory Leak hay Phân mảnh bộ nhớ!

```odin
import "core:mem"

// 1. Khai báo Arena
arena: mem.Arena

// 2. Cấp phát vùng đệm khổng lồ (Ví dụ 1 Megabyte)
// Lưu ý: Đưa biến này ra global (toàn cục) hoặc cấp phát động để tránh tràn Stack
arena_buffer: [mem.Megabyte]byte 

// 3. Khởi tạo Arena
mem.arena_init(&arena, arena_buffer[:])

// 4. Ép tất cả code bên dưới dùng Arena thay vì dùng Mặc định
context.allocator = mem.arena_allocator(&arena)

// TỪ ĐÂY TRỞ XUỐNG, BẠN CỨ KHAI BÁO THẢI MÁI
quai_vat := new(int) // Sẽ lấy từ Arena (Cực nhanh)

// 5. Cuối vòng lặp Game Loop, chỉ cần 1 lệnh này là dọn sạch mọi thứ!
free_all(context.allocator)
```

## 4. Code mẫu (Đã kiểm tra bằng Odin)

```odin
package main

import "core:fmt"
import "core:mem"

main :: proc() {
    arena_buffer: [mem.Megabyte]byte
    
    arena: mem.Arena
    mem.arena_init(&arena, arena_buffer[:])
    
    arena_allocator := mem.arena_allocator(&arena)
    context.allocator = arena_allocator
    
    // Test
    quai_vat := new(int)
    quai_vat^ = 100
    
    danh_sach := make([dynamic]int)
    append(&danh_sach, 1, 2, 3)
    
    fmt.println("Quái vật:", quai_vat^)
    fmt.println("Danh sách:", danh_sach)
    
    free_all(context.allocator)
    fmt.println("Đã dọn dẹp xong 100% bộ nhớ của Arena!")
}
```
*Lưu ý từ Compiler:* Biến `arena_buffer` kích thước 1MB đặt trong hàm `main` có thể gây cảnh báo Stack Overflow. Trong thực tế, bạn nên dùng `virtual_allocator` để lấy bộ nhớ ảo lớn cho Arena, hoặc biến nó thành biến toàn cục.

## Tổng kết chương 12
Arena Allocator kết hợp cùng hệ thống Context của Odin chính là bộ đôi hoàn hảo để làm game. Thay vì đau đầu nhớ `free` từng biến, bạn gom chúng vào Arena và "xả" một lần ở cuối mỗi khung hình (End of Frame). Game của bạn sẽ chạy với tốc độ bàn thờ mà không bao giờ bị rò rỉ RAM!
