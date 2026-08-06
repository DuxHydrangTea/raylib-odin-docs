# Chương 9: Quản lý bộ nhớ cốt lõi (Stack vs Heap)

Một trong những lý do khiến Odin được yêu thích để lập trình game là nó **KHÔNG CÓ Garbage Collector (Trình thu gom rác tự động)**. Việc dọn rác tự động thỉnh thoảng sẽ làm game bị khựng (lag spike) vì CPU phải đột ngột dừng mọi việc lại để đi dọn bộ nhớ.
Với Odin, bạn là người làm chủ 100% bộ nhớ. Để làm chủ, bạn cần hiểu hai vùng nhớ quan trọng: Stack và Heap.

## 1. Stack (Ngăn xếp) - Nhanh, Tự động dọn dẹp

Stack là một vùng nhớ rất nhanh, hoạt động theo nguyên tắc LIFO (vào sau ra trước).
Mỗi khi một hàm được gọi, hệ điều hành cấp cho nó một khối trên Stack. Tất cả các biến thông thường (int, float, mảng tĩnh tĩnh, struct...) khai báo trong hàm đều nằm ở đây.

**Đặc điểm của Stack:**
* **Cực kỳ nhanh.**
* Kích thước nhỏ (thường chỉ vài MB).
* **Tự động dọn dẹp:** Ngay khi hàm chạy xong (thoát khỏi cặp ngoặc `{}`), mọi biến trên Stack bị xóa sạch sành sanh ngay lập tức. Không bao giờ rò rỉ bộ nhớ.

```odin
tao_vu_khi :: proc() {
    sat_thuong := 50 // Biến này nằm trên Stack
    // Khi thoát khỏi hàm này, 'sat_thuong' biến mất hoàn toàn
}
```

## 2. Heap (Đống) - Rộng lớn, Cấp phát động

Chuyện gì xảy ra nếu bạn muốn tạo ra một con quái vật trong hàm `tao_quai_vat`, nhưng muốn con quái vật đó VẪN TỒN TẠI sau khi hàm đó đã kết thúc để cho vào mảng hiển thị lên màn hình?
Stack không làm được chuyện này vì nó sẽ xóa sạch khi hết hàm. Bạn phải dùng **Heap**.

Heap là vùng nhớ khổng lồ (vài GB RAM), dùng để lưu trữ dữ liệu "sống sót" vượt ra ngoài phạm vi hàm tạo ra nó. Để xin cấp phát vùng nhớ trên Heap, ta dùng từ khóa `new`. Hàm `new(KiểuDữLiệu)` sẽ trả về **con trỏ** trỏ đến vùng nhớ vừa được cấp phát.

```odin
tao_quai_vat :: proc() -> ^int {
    // Cấp phát động trên Heap
    quai_vat_hp := new(int) 
    quai_vat_hp^ = 100
    
    return quai_vat_hp // Trả về con trỏ, biến này vẫn sống nhăn răng!
}
```

**Mặt trái của Heap:**
* Truy xuất chậm hơn Stack một chút.
* **KHÔNG BAO GIỜ tự dọn dẹp!** Nếu bạn gọi `new`, bạn PHẢI tự gọi `free(con trỏ)` để xóa nó đi. Nếu không, bộ nhớ RAM sẽ bị ngốn dần cho đến khi văng game (Hiện tượng rò rỉ bộ nhớ - Memory Leak).

Đây là lúc siêu năng lực `defer` (học ở chương 6) tỏa sáng rực rỡ!

```odin
main :: proc() {
    quai_vat_ptr := tao_quai_vat()
    
    // Đảm bảo cuối hàm biến này sẽ được dọn dẹp
    defer free(quai_vat_ptr) 
    
    // Làm gì đó với con quái vật...
}
```

## 3. Code mẫu (Đã kiểm tra bằng Odin)

```odin
package main

import "core:fmt"

tao_quai_vat :: proc() -> ^int {
    quai_vat_hp := new(int)
    quai_vat_hp^ = 100
    return quai_vat_hp
}

main :: proc() {
    mau_nguoi_choi := 100 // Tự động nằm trên Stack, tự động giải phóng
    
    quai_vat_ptr := tao_quai_vat()
    fmt.println("Máu quái vật:", quai_vat_ptr^) // In ra 100
    
    // BẮT BUỘC: Giải phóng vùng nhớ Heap
    free(quai_vat_ptr) 
    fmt.println("Đã giải phóng quái vật khỏi bộ nhớ.")
}
```

## Tổng kết chương 9
Quy tắc ngón tay cái khi code Odin: **Hãy dùng Stack bất cứ khi nào có thể.** Chỉ dùng `new` (Heap) khi dữ liệu quá lớn, hoặc bạn thực sự cần nó sống vượt khỏi phạm vi của hàm. Ở chương sau, chúng ta sẽ xem cách Odin khiến việc quản lý Heap trở nên thanh lịch hơn nhờ vào **Hệ thống Context**.
