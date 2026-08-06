# Chương 13: Đa luồng (Threading) và Đồng bộ hóa

CPU hiện đại có rất nhiều nhân (cores). Mặc định, game của bạn chỉ chạy trên 1 nhân duy nhất (Luồng chính - Main Thread). Để tận dụng hết sức mạnh của CPU (ví dụ: vừa vẽ hình, vừa load tài nguyên mạng, vừa tính toán AI AI), bạn cần dùng đến Đa luồng (Threading).

## 1. Tạo Luồng (Thread)

Odin hỗ trợ đa luồng trực tiếp thông qua package `core:thread`.

```odin
import "core:thread"

// Hàm này sẽ được chạy trên một luồng hoàn toàn độc lập
cong_viec_cua_luong :: proc(t: ^thread.Thread) {
    fmt.println("Luồng phụ đang chạy!")
}

main :: proc() {
    // Tạo luồng
    luong_phu := thread.create(cong_viec_cua_luong)
    
    if luong_phu != nil {
        // Bắt đầu chạy
        thread.start(luong_phu)
        
        // ... Hàm main vẫn tiếp tục chạy song song ...
        
        // Bắt hàm main chờ cho đến khi luồng phụ chạy xong
        thread.join(luong_phu) 
        
        // Dọn dẹp
        thread.destroy(luong_phu) 
    }
}
```

## 2. Vấn đề "Xung đột dữ liệu" (Data Race)

Chuyện gì xảy ra nếu cả **Luồng chính** và **Luồng phụ** cùng lao vào thay đổi một biến `tong_so_tien` cùng một lúc (Mili giây)? Dữ liệu sẽ bị hỏng hoàn toàn (Data Race). Máy tính sẽ không biết phải nghe ai.

## 3. Đồng bộ hóa với Mutex (Mutual Exclusion)

Để giải quyết Data Race, ta dùng cái Khóa (Mutex) từ package `core:sync`. Quy tắc rất đơn giản:
* Ai lấy được chìa khóa (`lock`) thì mới được sửa dữ liệu.
* Người kia đến sau, thấy khóa rồi thì phải đứng đợi (bị block).
* Sửa xong thì trả chìa khóa (`unlock`) cho người kia vào.

```odin
import "core:sync"

tien_mutex: sync.Mutex // Cấu trúc Khóa
tong_so_tien := 0

cong_viec_cua_luong :: proc(t: ^thread.Thread) {
    // 1. Khóa cửa (Nếu luồng khác đang khóa, luồng này sẽ tự động đứng chờ)
    sync.mutex_lock(&tien_mutex)
    
    // 2. An tâm sửa dữ liệu
    tong_so_tien += 1000
    
    // 3. Mở cửa cho người khác
    sync.mutex_unlock(&tien_mutex)
}
```

## 4. Code mẫu (Đã kiểm tra bằng Odin)

```odin
package main

import "core:fmt"
import "core:thread"
import "core:sync"

tong_so_tien := 0
tien_mutex: sync.Mutex

cong_viec_cua_luong :: proc(t: ^thread.Thread) {
    fmt.println("Luồng phụ đang chạy...")
    sync.mutex_lock(&tien_mutex)
    tong_so_tien += 1000
    sync.mutex_unlock(&tien_mutex)
}

main :: proc() {
    luong_phu := thread.create(cong_viec_cua_luong)
    
    if luong_phu != nil {
        thread.start(luong_phu)
        fmt.println("Luồng chính đang làm việc khác...")
        
        thread.join(luong_phu)
        thread.destroy(luong_phu)
        
        fmt.println("Tổng số tiền an toàn:", tong_so_tien)
    }
}
```

## Tổng kết chương 13
Đa luồng là một con dao hai lưỡi. Nó giúp game chạy siêu mượt, nhưng nếu quên dùng Mutex (Lock/Unlock), nó sẽ sinh ra những lỗi cực kỳ khó tìm. Lời khuyên: Hãy thiết kế luồng thật cẩn thận, hạn chế để các luồng dùng chung biến với nhau.
