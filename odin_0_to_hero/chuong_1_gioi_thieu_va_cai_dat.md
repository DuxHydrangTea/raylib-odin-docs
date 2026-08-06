# Chương 1: Giới thiệu Odin, Cài đặt và Hello World

Chào mừng bạn đến với ngôn ngữ lập trình Odin! Trong chương này, chúng ta sẽ tìm hiểu lý do tại sao Odin lại đặc biệt, triết lý thiết kế của nó, cách cài đặt và viết chương trình đầu tiên.

## 1. Ngôn ngữ Odin là gì? Tại sao lại chọn Odin?

Odin là một ngôn ngữ lập trình đa năng, được thiết kế với mục tiêu cốt lõi là tạo ra một công cụ **nhanh, gọn, dễ đọc, thực tế** và **mã nguồn mở**. Được sáng lập bởi Ginger Bill, Odin nhắm đến việc thay thế C với tư cách là một ngôn ngữ lập trình hệ thống (system programming) nhưng hiện đại hơn và ít rườm rà hơn C++.

**Triết lý của Odin:**
* **Niềm vui lập trình (Joy of Programming):** Odin muốn mang lại cảm giác vui vẻ khi code.
* **Tính thực dụng (Pragmatism):** Giải quyết vấn đề thực tế, không bị trói buộc bởi lý thuyết giáo điều.
* **Đơn giản hóa (Simplicity):** Cú pháp dễ đọc, ít ẩn ý (no hidden control flow). Odin không có operator overloading hay các class phức tạp như C++.
* **Hiệu suất cao (High Performance):** Biên dịch nhanh, chạy nhanh, kiểm soát bộ nhớ hoàn toàn.
* **Data-Oriented Design (DOD):** Odin được thiết kế tự nhiên để hỗ trợ DOD (rất quan trọng trong làm game).

**Tại sao Odin lại tuyệt vời cho Lập trình Game (đặc biệt với Raylib)?**
1. **Liên kết C (C Interoperability) mượt mà:** Odin gọi hàm C cực kỳ tự nhiên. Raylib được viết bằng C, nên sự kết hợp này là hoàn hảo.
2. **Quản lý bộ nhớ linh hoạt:** Hệ thống Allocator và Context tích hợp sẵn giúp bạn dễ dàng theo dõi bộ nhớ, tạo các Custom Allocator (như Arena) chuyên dụng cho game để tối ưu tốc độ.
3. **Cú pháp rõ ràng:** Code dài nhưng đọc rất dễ hiểu, giúp bạn duy trì các dự án lớn (như game) mà không bị "lạc lối".
4. **Không có Garbage Collector (GC):** Game cần tốc độ khung hình (FPS) ổn định. GC của các ngôn ngữ khác (C#, Java) thường gây ra hiện tượng khựng hình (lag spike). Odin cho bạn toàn quyền kiểm soát thời điểm giải phóng bộ nhớ.

## 2. Cài đặt môi trường Odin

### Bước 1: Cài đặt Odin Compiler
Odin có thể chạy trên Windows, macOS và Linux. 

**Đối với Windows:**
1. Tải bản release mới nhất (`.zip`) từ trang chủ hoặc Github của Odin: [Odin Github Releases](https://github.com/odin-lang/Odin/releases).
2. Giải nén vào một thư mục cố định (ví dụ: `C:\Odin`).
3. Thêm đường dẫn `C:\Odin` vào biến môi trường `PATH` của Windows (để có thể gọi lệnh `odin` từ mọi nơi trong Terminal).

**Đối với Linux / macOS:**
Bạn có thể tự build từ mã nguồn hoặc dùng brew (macOS):
```bash
# Clone mã nguồn
git clone https://github.com/odin-lang/Odin
cd Odin

# Chạy script build
make release-native
```
Sau đó thêm thư mục Odin vào biến môi trường `$PATH` trong file `~/.bashrc` hoặc `~/.zshrc`.

*Kiểm tra cài đặt:* Mở terminal / command prompt và gõ:
```bash
odin version
```
Nếu màn hình hiển thị phiên bản Odin, chúc mừng bạn đã cài đặt thành công!

### Bước 2: Trình soạn thảo mã (Code Editor)
Mặc dù bạn có thể dùng bất kỳ editor nào, nhưng **Visual Studio Code (VS Code)** hoặc **Sublime Text** được khuyến nghị.
* **VS Code:** Cài đặt extension `Odin` (bởi ols - Odin Language Server) để có tính năng tự động hoàn thành code (autocomplete), highlight cú pháp và đi tới định nghĩa.
* **Sublime Text:** Cài gói `Odin` thông qua Package Control.

## 3. Hello, World! - Chương trình đầu tiên

Hãy bắt đầu viết dòng code đầu tiên. Tạo một file tên là `main.odin` (trong thư mục học tập của bạn) và nhập đoạn code sau:

```odin
package main

import "core:fmt"

main :: proc() {
    fmt.println("Xin chào, Odin from Zero to Hero!")
}
```

### Phân tích chương trình:
1. `package main`: Bắt buộc ở đầu mỗi file. Khai báo file này thuộc gói (package) `main`. Hàm thực thi chính luôn nằm trong package `main`.
2. `import "core:fmt"`: Nhập (import) package `fmt` (format) từ thư viện cốt lõi (`core`) của Odin. Package này chứa các hàm in dữ liệu ra màn hình.
3. `main :: proc() { ... }`: Định nghĩa hàm chính của chương trình. 
   * `::` là cú pháp định nghĩa một hằng số. Ở đây, ta định nghĩa `main` là một thủ tục (procedure) không đổi.
   * `proc()` khai báo đây là một procedure (trong Odin, function được gọi là procedure).
4. `fmt.println(...)`: Gọi hàm in ra màn hình và xuống dòng từ package `fmt`.

## 4. Biên dịch và chạy chương trình

Odin cung cấp nhiều cách để chạy file. Mở terminal tại thư mục chứa file `main.odin` và chạy các lệnh sau:

**Cách 1: Chạy trực tiếp (Build & Run)**
Lệnh này sẽ biên dịch code ra một file thực thi tạm thời và tự động chạy nó. Thường dùng khi đang phát triển (develop).
```bash
odin run main.odin -file
```
*Kết quả:*
`Xin chào, Odin from Zero to Hero!`

*Lưu ý: Flag `-file` báo cho compiler biết ta chỉ muốn build một file duy nhất. Nếu build toàn bộ thư mục, ta bỏ `-file` đi.*

**Cách 2: Build ra file thực thi (Executable)**
Lệnh này sẽ tạo ra một file `.exe` (trên Windows) hoặc một file nhị phân (trên Linux/macOS) để bạn có thể gửi cho người khác chạy.
```bash
odin build main.odin -file
```
Sau đó bạn có thể chạy file thực thi vừa được tạo:
* Trên Windows: `main.exe`
* Trên Linux/macOS: `./main`

## Tổng kết chương 1
Trong chương này, bạn đã làm quen với triết lý của Odin, cài đặt thành công compiler và viết chương trình đầu tiên. 
Hãy đảm bảo bạn đã cài đặt thành công và chạy được lệnh `odin run` trước khi bước sang chương 2, nơi chúng ta sẽ tìm hiểu về các nền tảng xây dựng ngôn ngữ: Biến và Kiểu dữ liệu.
