# Chương 14: Thao tác bit và Tư duy Data-Oriented Design (DOD)

Chương này sẽ giới thiệu cho bạn hai thứ làm nên "đẳng cấp" của một lập trình viên Engine Game: Hiểu về Bit và hiểu về Kiến trúc Dữ liệu hướng Data.

## 1. Thao tác Bit (Bitwise Operations)

Mọi dữ liệu tận cùng đều là số 0 và 1. Thao tác bit cho phép bạn xử lý trực tiếp các con số nhị phân này với tốc độ ánh sáng (chỉ tốn đúng 1 chu kỳ của CPU).

Các toán tử bit cơ bản:
* `&` (AND): Trả về 1 nếu CẢ HAI bit là 1.
* `|` (OR): Trả về 1 nếu MỘT TRONG HAI bit là 1.
* `~` (XOR): Trả về 1 nếu 2 bit KHÁC NHAU.
* `<<` (Dịch trái): Dịch tất cả các bit sang trái n vị trí (Tương đương nhân 2 mũ n).
* `>>` (Dịch phải): Dịch tất cả các bit sang phải n vị trí (Tương đương chia lấy nguyên cho 2 mũ n).

```odin
a: u8 = 0b0000_1010 // Số 10
b: u8 = 0b0000_1100 // Số 12

ket_qua := a & b // 0b0000_1000 (Số 8)
```
*Lưu ý: Mặc dù thao tác bit rất ngầu, nhưng trong Odin bạn CÓ THỂ sử dụng `bit_set` (đã học ở Chương 7) để code sạch đẹp hơn rất nhiều mà vẫn giữ nguyên tốc độ.*

## 2. Tư duy Data-Oriented Design (DOD)

DOD là thứ tạo nên sức mạnh của các Game Engine hiện đại (như Unity DOTS). 
Triết lý của DOD: **CPU hiện đại không chậm ở việc tính toán, nó chậm ở việc chờ Dữ liệu được nạp vào Cache (Bộ đệm).**

### Mô hình OOP Truyền thống: Array of Structures (AOS)
Trong lập trình hướng đối tượng, ta thường gom mọi thứ của 1 con quái vật thành 1 cục (Struct), rồi cho vào mảng.
```odin
Entity :: struct {
    pos_x, pos_y: f32,
    hp: int,
    name: string,
}
danh_sach_quai: [dynamic]Entity
```
Vấn đề: Nếu Hệ thống Vật lý chỉ muốn lặp qua mảng để cập nhật `pos_x` và `pos_y`, nó vô tình "phải" tải luôn cả `hp` và `name` (rất bự) vào CPU Cache. Dẫn đến CPU bị "sặc" dữ liệu rác (Cache Miss), làm giảm FPS thê thảm nếu có 10.000 quái vật.

### Mô hình DOD: Structure of Arrays (SOA)
DOD phá vỡ cấu trúc đó. Ta tách từng thuộc tính ra thành từng mảng riêng biệt.
```odin
EntityManager :: struct {
    pos_x: [dynamic]f32,
    pos_y: [dynamic]f32,
    hps:   [dynamic]int,
}
manager: EntityManager
```
Giờ đây, khi Hệ thống Vật lý cần cập nhật Tọa độ, nó chỉ lặp trên mảng `pos_x` và `pos_y`. Tất cả các con số kiểu `f32` được nạp liên tiếp vào CPU Cache (Cache Hit 100%). Tốc độ xử lý có thể tăng **gấp 5 đến 10 lần** so với mô hình OOP!

Odin là một ngôn ngữ được thiết kế cực kỳ phù hợp để viết code theo chuẩn SOA. Hãy nhớ: **Tách biệt Dữ liệu (Data) ra khỏi Logic tính toán.**
