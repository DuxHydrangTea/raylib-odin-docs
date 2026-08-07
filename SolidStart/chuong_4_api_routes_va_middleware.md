# Chương 4: API Routes và Middleware

Mặc dù `cache()` và `action()` giải quyết được 95% nhu cầu lấy/gửi dữ liệu trên giao diện (Frontend), bạn đôi khi vẫn cần viết các API REST truyền thống (ví dụ: cấp API cho một ứng dụng di động Mobile App, cung cấp Webhook cho Stripe/Paypal). SolidStart hỗ trợ việc này thông qua **API Routes**.

## 1. Khởi tạo API Routes

Cấu trúc thư mục của API Routes hoạt động giống hệt như UI Routes (File-based routing), ngoại trừ việc bạn không `export default` một Component giao diện, mà bạn `export` các hàm đại diện cho HTTP Methods: `GET`, `POST`, `PUT`, `DELETE`.

Theo quy ước, người ta thường đặt API vào thư mục `src/routes/api/`.

```ts
// src/routes/api/hello.ts (Đường dẫn: http://localhost:3000/api/hello)

import type { APIEvent } from "@solidjs/start/server";

// Xử lý request GET
export async function GET({ request }: APIEvent) {
  return new Response(JSON.stringify({ message: "Xin chào từ SolidStart API" }), {
    headers: { "Content-Type": "application/json" }
  });
}

// Xử lý request POST
export async function POST({ request }: APIEvent) {
  // Lấy dữ liệu gửi lên từ body
  const body = await request.json(); 
  
  return new Response(JSON.stringify({ received: body }), {
    status: 201, // Created
    headers: { "Content-Type": "application/json" }
  });
}
```

## 2. Dynamic API Routes (API động)

Tương tự như UI, bạn có thể tạo URL API động bằng ngoặc vuông.

```ts
// src/routes/api/users/[id].ts
import type { APIEvent } from "@solidjs/start/server";

export async function GET({ params, request }: APIEvent) {
  const userId = params.id;
  
  // Logic tìm kiếm user trong CSDL
  const user = { id: userId, name: "Nguyen Van A" };
  
  return new Response(JSON.stringify(user));
}
```

## 3. Middleware (Đánh chặn Request)

Middleware là một đoạn code luôn chạy TRƯỚC KHI request chạm đến Route cuối cùng. Bạn thường dùng Middleware để:
- Kiểm tra người dùng đã đăng nhập chưa (Authentication).
- Ghi log hệ thống.
- Redirect (chuyển hướng) nếu truy cập trái phép.

Để tạo Middleware trong SolidStart, bạn tạo một file tên là `middleware.ts` ở thư mục `src/`.

```ts
// src/middleware.ts
import { createMiddleware } from "@solidjs/start/middleware";

export default createMiddleware({
  onRequest: [
    async (event) => {
      const url = new URL(event.request.url);
      
      console.log(`[LOG] Ai đó đang truy cập vào: ${url.pathname}`);
      
      // Giả sử có một trang Admin yêu cầu quyền đặc biệt
      if (url.pathname.startsWith("/admin")) {
        // Kiểm tra cookie hoặc token (Ví dụ rút gọn)
        const token = event.request.headers.get("Authorization");
        
        if (!token) {
          // Trả về lỗi 401 hoặc dùng Response.redirect() để đuổi về trang Đăng nhập
          return new Response("Unauthorized", { status: 401 });
        }
      }
      
      // Nếu hợp lệ, cho phép request đi tiếp tới Route
    }
  ]
});
```
*Lưu ý quan trọng:* Middleware chạy ở mọi request, kể cả tải ảnh, tải file CSS. Hãy cẩn thận khi viết các logic tính toán nặng ở đây.

## Tổng kết Chương 4
- API Routes giúp SolidStart hoạt động như một Backend thực thụ (Node.js/Bun).
- Sử dụng hàm trùng tên với HTTP Methods (`GET`, `POST`, `PATCH`, `DELETE`).
- Middleware rất hữu ích để kiểm soát luồng truy cập và bảo mật.
