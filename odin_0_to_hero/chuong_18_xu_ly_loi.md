# Chương 18: Xử lý lỗi (Error Handling)

Trong quá trình làm game, lỗi là không thể tránh khỏi: File save bị thiếu, Load ảnh thất bại, Không kết nối được server... Odin xử lý lỗi theo một cách cực kỳ rõ ràng, không mập mờ bằng Exceptions (như C# hay Java).

## 1. Không có Try/Catch!

Odin không có Exceptions. Cách Odin xử lý lỗi giống hệt ngôn ngữ Go (Golang) và C: **Lỗi được trả về như một giá trị thông thường**.

Điều này buộc lập trình viên phải "nhìn thẳng vào sự thật" và xử lý lỗi ngay lập tức, thay vì bọc nó trong một đống `try/catch` có thể phá vỡ luồng (control flow) của chương trình bất cứ lúc nào.

## 2. Pattern: Trả về Đa giá trị (Multiple Returns)

Để báo lỗi, một hàm sẽ trả về giá trị thực sự của nó kèm theo một mã lỗi (thường là một `Enum`).

```odin
// 1. Định nghĩa các kiểu lỗi có thể xảy ra
FileError :: enum {
    None,              // Không có lỗi
    File_Not_Found,    // Không tìm thấy file
    Permission_Denied, // Bị chặn quyền truy cập
}

// 2. Hàm trả về cặp (Giá trị, Lỗi)
doc_file_save :: proc(ten_file: string) -> (data: string, err: FileError) {
    if ten_file == "" {
        return "", .File_Not_Found // Trả về lỗi
    }
    
    // Giả lập đọc thành công
    return "Dữ liệu...", .None
}
```

Khi gọi hàm, bạn chỉ việc dùng lệnh `if` để kiểm tra biến `err` có khác `.None` hay không.

```odin
data, err := doc_file_save("save1.dat")
    
if err != .None {
    fmt.println("Có lỗi xảy ra:", err)
} else {
    fmt.println("Đọc thành công:", data)
}
```

## 3. Lệnh `or_return` (Phép thuật rút gọn)

Đôi khi hàm `A` gọi hàm `B`, hàm `B` gọi hàm `C`. Nếu `C` bị lỗi, `B` phải nhận lỗi rồi truyền lại cho `A`. Việc viết hàng loạt câu `if err != .None` sẽ rất mệt mỏi.
Odin có từ khóa `or_return`. Nó tự động kiểm tra xem có lỗi hay không. Nếu có lỗi, nó sẽ **return cái lỗi đó ngay lập tức ra khỏi hàm hiện tại**.

```odin
ham_A :: proc() -> (string, FileError) {
    // Nếu doc_file_save có lỗi, ham_A sẽ tự động ngắt và return lỗi đó!
    data := doc_file_save("save_game.dat") or_return
    
    // Nếu chạy được tới đây nghĩa là không có lỗi
    return data, .None
}
```

## Tổng kết chương 18
Tuyệt đối không có chuyện Game bị Crash bất tử vì một cái lỗi vớ vẩn nào đó bị ném ra (Throw exception) mà bạn quên bắt (Catch). Mọi luồng xử lý lỗi đều hiện rành rành trên màn hình. Đó chính là Triết lý "Không ẩn ý" của Odin.
