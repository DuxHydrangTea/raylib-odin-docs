# Chương 8: Backend trong Next.js (Route Handlers & Middleware)

Với Next.js, bạn hoàn toàn có thể xây dựng một Full-stack Application mà không cần tới Express hay Nest.js. Bạn có thể xây dựng RESTful APIs, Webhooks, và xử lý phân luồng request với Middleware ở Edge Network.

---

## 1. Route Handlers (`route.ts`) - Thay thế `/api`

Trong App Router, thay vì tạo file trong thư mục `pages/api`, bạn tạo thư mục bất kỳ bên trong `app/` và tạo file `route.ts`.
*(Lưu ý: Không thể đặt file `route.ts` và `page.tsx` trong cùng một thư mục ngang hàng vì nó sẽ gây xung đột cho cùng một URL).*

### Xây dựng một REST API hoàn chỉnh
**Vị trí:** `app/api/users/route.ts` (Sẽ tạo ra endpoint: `GET /api/users` và `POST /api/users`)

```ts
import { NextRequest, NextResponse } from 'next/server';
import { db } from '@/lib/db'; // Kết nối Database (Prisma/Drizzle)

// Xử lý GET request (Lấy danh sách User)
export async function GET(request: NextRequest) {
  try {
    // Lấy query param. Ví dụ: /api/users?role=admin
    const searchParams = request.nextUrl.searchParams;
    const role = searchParams.get('role');

    const users = await db.user.findMany({
      where: role ? { role } : undefined
    });

    return NextResponse.json(users, { status: 200 });
  } catch (error) {
    return NextResponse.json({ error: "Lỗi máy chủ nội bộ" }, { status: 500 });
  }
}

// Xử lý POST request (Tạo User mới)
export async function POST(request: NextRequest) {
  try {
    const body = await request.json(); // Đọc body JSON

    // Validate dữ liệu (Nên dùng thư viện Zod)
    if (!body.email || !body.name) {
      return NextResponse.json({ error: "Thiếu trường dữ liệu" }, { status: 400 });
    }

    const newUser = await db.user.create({ data: body });
    
    return NextResponse.json(newUser, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: "Lỗi khi tạo user" }, { status: 400 });
  }
}
```

---

## 2. Dynamic Route Handlers

Tương tự như UI, bạn có thể tạo API động bằng thư mục `[id]`.
**Vị trí:** `app/api/users/[id]/route.ts` (Tạo endpoint: `DELETE /api/users/123`)

```ts
import { NextRequest, NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function DELETE(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    await db.user.delete({ where: { id: params.id } });
    return NextResponse.json({ message: "Xóa thành công" });
  } catch (error) {
    return NextResponse.json({ error: "Không tìm thấy User" }, { status: 404 });
  }
}
```

---

## 3. Middleware - Người gác cổng (Gatekeeper)

Middleware cho phép bạn chạy mã **trước khi** một Request hoàn thành. Khác với Route Handlers chạy trên Node.js, Middleware thường chạy trên **Edge Runtime** (môi trường cực nhẹ, gần với người dùng nhất).

**Ứng dụng tuyệt vời của Middleware:**
- Kiểm tra JWT Token (Authentication).
- Trích xuất ngôn ngữ (i18n Localization).
- A/B Testing, Redirect (Chuyển hướng), Rewrite.

**Vị trí BẮT BUỘC:** File `middleware.ts` nằm ở thư mục GỐC của dự án (ngang hàng thư mục `app/`).

```ts
// /middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')?.value;
  const url = request.nextUrl.pathname;

  // 1. Chuyển hướng nếu chưa đăng nhập mà vào Dashboard
  if (url.startsWith('/dashboard') && !token) {
    // Chuyển về trang login, lưu kèm URL hiện tại để login xong quay lại
    return NextResponse.redirect(new URL(`/login?callbackUrl=${url}`, request.url));
  }

  // 2. Nếu đã đăng nhập mà lại vào trang Login -> Đẩy về trang chủ
  if (url.startsWith('/login') && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // 3. Cho phép đi tiếp nếu hợp lệ
  return NextResponse.next();
}

// Cực kỳ quan trọng: Định nghĩa những đường dẫn nào Middleware sẽ chạy qua
// Nếu không cấu hình, Middleware sẽ chạy với TẤT CẢ request (bao gồm ảnh tĩnh, css -> làm chậm web)
export const config = {
  matcher: [
    /*
     * Match tất cả đường dẫn ngoại trừ:
     * 1. /api/ (bỏ qua API routes, tự xử lý riêng)
     * 2. /_next/ (file build của Next.js)
     * 3. /_static, /favicon.ico (Tài nguyên tĩnh)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
```

**Tóm tắt chương 8:**
Bạn đã biết cách sử dụng Next.js như một backend server. Sử dụng `route.ts` cho các API công khai hoặc webhooks, và đặc biệt là `middleware.ts` để chặn / chuyển hướng / bảo vệ trang web ở cấp độ toàn cục trước khi request chạm vào code logic của bạn.
