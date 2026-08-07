# Chương 3: Server Actions và Xử lý Form

Khi xây dựng trang web, việc xử lý Form (Đăng nhập, Đăng ký, Thêm dữ liệu) luôn chiếm phần lớn thời gian. Trong quá khứ (với React hoặc Solid thuần), bạn phải viết hàm `onSubmit`, gọi `e.preventDefault()`, sau đó dùng `fetch` để POST dữ liệu lên server, tự quản lý state `isLoading`, `isError`.

Với SolidStart, mọi thứ dễ dàng hơn gấp 10 lần nhờ tính năng **Server Actions**. Bạn có thể gọi thẳng một hàm trên Server ngay từ thẻ `<form>` của HTML! Đặc biệt hơn, Form này vẫn hoạt động ngay cả khi người dùng tắt JavaScript trên trình duyệt (Progressive Enhancement).

## 1. Khai báo Server Action (Hành động trên Server)

Sử dụng hàm `action` từ thư viện `@solidjs/router`. Quan trọng nhất là chuỗi `"use server"`. Nó báo cho trình biên dịch biết: Khối code này không bao giờ được tải xuống trình duyệt của người dùng.

```jsx
import { action } from "@solidjs/router";

// Khai báo một Server Action
const handleLogin = action(async (formData) => {
  "use server"; // Cực kỳ quan trọng: Code này chỉ chạy ở Node.js Server
  
  // Dữ liệu nhận được là đối tượng FormData chuẩn của HTML
  const email = formData.get("email");
  const password = formData.get("password");

  // Giả lập việc query vào Database... (Bạn có thể dùng Prisma/Drizzle ở đây một cách an toàn)
  if (email === "admin@gmail.com" && password === "123456") {
    console.log("Đăng nhập thành công trên Server!");
    // Có thể set Cookie, Redirect người dùng tại đây
    return { success: true, message: "Chào mừng admin" };
  }
  
  // Ném ra lỗi nếu sai mật khẩu
  throw new Error("Sai email hoặc mật khẩu");
}, "login-action"); // Tên định danh cho action
```

## 2. Gắn Action vào HTML Form

Bây giờ bạn lấy `handleLogin` vừa tạo và truyền thẳng nó vào thuộc tính `action` của thẻ `<form>`. (SolidJS sẽ tự động tạo ra một endpoint API ngầm đằng sau để kết nối form này với server).

```jsx
import { action, useSubmission } from "@solidjs/router";
import { Show } from "solid-js";

// Khai báo action (như phần 1)
const handleLogin = action(async (formData) => {
  "use server";
  const email = formData.get("email");
  await new Promise(r => setTimeout(r, 1000)); // Giả lập delay 1s
  if(email !== "admin") throw new Error("Thất bại!");
  return "Thành công!";
});

export default function LoginPage() {
  // Hook useSubmission cho phép theo dõi trạng thái của Form (Đang gửi, Đã xong, Bị lỗi)
  const submission = useSubmission(handleLogin);

  return (
    <main>
      <h1>Đăng nhập (Server Actions)</h1>

      {/* Truyền biến action vào đây */}
      <form action={handleLogin} method="post">
        <div>
          <label>Email:</label>
          <input type="text" name="email" required />
        </div>
        <div>
          <label>Mật khẩu:</label>
          <input type="password" name="password" required />
        </div>

        {/* Vô hiệu hóa nút khi đang loading */}
        <button type="submit" disabled={submission.pending}>
          {submission.pending ? "Đang xử lý..." : "Đăng nhập"}
        </button>
      </form>

      {/* Hiển thị lỗi nếu có */}
      <Show when={submission.error}>
        <p style={{ color: "red" }}>Lỗi: {submission.error.message}</p>
      </Show>

      {/* Hiển thị kết quả thành công */}
      <Show when={submission.result}>
        <p style={{ color: "green" }}>{submission.result}</p>
      </Show>
    </main>
  );
}
```

## 3. Lợi ích khổng lồ
- **Bảo mật tuyệt đối**: Code truy vấn Database hoặc Secret API Keys nằm trọn trong `"use server"`, không bao giờ lộ cho Client.
- **Tự động Loading State**: Thay vì tự tạo `[isLoading, setIsLoading]`, bạn chỉ cần gọi `useSubmission().pending`.
- **Hoạt động không cần JS**: Nếu JS bị lỗi chưa kịp tải, thẻ `<form>` HTML gốc tự động gửi một POST request chuẩn lên Server. App của bạn sẽ không bao giờ bị "liệt".

## Tổng kết Chương 3
- `action()` kết hợp với `"use server"` là cách tiêu chuẩn để cập nhật dữ liệu.
- `useSubmission()` giúp bạn dễ dàng làm UI Loading / Xử lý thông báo lỗi.
- Không cần tự viết REST API (GET/POST endpoints), SolidStart tự lo việc kết nối Frontend và Backend.
