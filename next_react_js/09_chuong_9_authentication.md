# Chương 9: Authentication & Authorization (Xác thực và Phân quyền)

Bảo mật là ưu tiên số một của hệ thống Enterprise. Trong Next.js, cách chuẩn mực và an toàn nhất hiện tại là sử dụng **Auth.js** (Phiên bản nâng cấp của NextAuth.js v4). 

Auth.js hỗ trợ đăng nhập qua OAuth (Google, Facebook, Github...), Magic Links (Gửi email), và Credentials (Tài khoản/Mật khẩu truyền thống).

---

## 1. Cài đặt Auth.js (NextAuth v5)

Vì là tài liệu đi làm, chúng ta sẽ hướng dẫn kiến trúc của phiên bản V5 - phiên bản tích hợp sâu nhất với App Router.

Cài đặt thư viện: `npm install next-auth@beta` (V5 đang trong quá trình final release).

---

## 2. Cấu hình Cốt lõi (The Core Config)

Tạo một file trung tâm quản lý toàn bộ Auth.
**Vị trí:** `auth.ts` (Tại thư mục gốc, ngang hàng `app/`)

```ts
// auth.ts
import NextAuth from 'next-auth';
import GitHubProvider from 'next-auth/providers/github';
import CredentialsProvider from 'next-auth/providers/credentials';

export const { 
  handlers: { GET, POST }, // Dùng để expose API routes
  auth, // Hàm kiểm tra session (dùng ở Server Components/Server Actions)
  signIn, // Hàm gọi đăng nhập
  signOut // Hàm gọi đăng xuất
} = NextAuth({
  providers: [
    GitHubProvider({
      clientId: process.env.GITHUB_ID,
      clientSecret: process.env.GITHUB_SECRET,
    }),
    // Ví dụ đăng nhập bằng username/password (Thực tế phải hash bcrypt/argon2)
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        // Gọi DB kiểm tra password ở đây
        if (credentials.email === "admin@test.com" && credentials.password === "123456") {
          // Trả về Object User
          return { id: "1", name: "Admin", email: "admin@test.com", role: "ADMIN" };
        }
        return null;
      }
    })
  ],
  callbacks: {
    // Ép role vào JWT Token (Để Middleware có thể đọc được)
    async jwt({ token, user }) {
      if (user) {
        token.role = user.role; // Lấy role từ DB gán vào token
      }
      return token;
    },
    // Trích xuất từ Token ra Session (Để UI hiển thị)
    async session({ session, token }) {
      if (session.user && token.role) {
        // Mở rộng kiểu dữ liệu Session mặc định cần khai báo TypeScript (module augmentation)
        (session.user as any).role = token.role; 
      }
      return session;
    }
  },
  pages: {
    signIn: '/login', // Đường dẫn trang login custom của bạn
  }
});
```

---

## 3. Tạo Route Handler cho Auth (Bắt buộc)

Auth.js cần một API route để tự động xử lý các callback OAuth và callbacks đăng nhập.

**Vị trí:** `app/api/auth/[...nextauth]/route.ts`

```ts
import { GET, POST } from '@/auth'; // Lấy từ file auth.ts ở bước 2

export { GET, POST };
```

---

## 4. Bảo vệ Trang và API (Authorization & RBAC)

Giờ đây bạn đã có Auth. Bạn cần bảo vệ ứng dụng của mình. Có 3 cách bảo vệ ở 3 tầng khác nhau:

### Cách 1: Bảo vệ tại Middleware (Cửa ngõ ngoài cùng)
Mở lại file `middleware.ts` ở chương trước và viết lại bằng Auth.js.

```ts
// /middleware.ts
import { auth } from '@/auth';

export default auth((req) => {
  const isLoggedIn = !!req.auth;
  const { pathname } = req.nextUrl;

  // Phân quyền Role-based Access Control (RBAC)
  if (pathname.startsWith('/admin')) {
    const role = (req.auth?.user as any)?.role;
    if (role !== 'ADMIN') {
      return Response.redirect(new URL('/unauthorized', req.url));
    }
  }

  if (pathname.startsWith('/dashboard') && !isLoggedIn) {
    return Response.redirect(new URL('/login', req.url));
  }
});

export const config = { matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'] };
```

### Cách 2: Bảo vệ tại Server Components / Server Actions
Dùng khi bạn cần truy xuất DB an toàn.

**Vị trí:** `app/dashboard/page.tsx`
```tsx
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export default async function Dashboard() {
  // Hàm auth() chạy cực nhanh trên server
  const session = await auth();

  if (!session?.user) {
    redirect('/login'); // Đá văng ra ngoài nếu chưa đăng nhập
  }

  return <div>Chào mừng {session.user.name} đến với Dashboard bí mật!</div>;
}
```

### Cách 3: Ở Client Components (Hiển thị UI theo user)
Chỉ hiển thị nút Logout nếu đã đăng nhập.

**Vị trí:** `components/Navbar.tsx`
```tsx
'use client';
import { useSession, signOut } from 'next-auth/react'; // Cần bọc <SessionProvider> ở layout
import Link from 'next/link';

export default function Navbar() {
  const { data: session, status } = useSession();

  if (status === "loading") return <div>Đang kiểm tra bảo mật...</div>;

  return (
    <nav>
      {session ? (
        <div className="flex gap-4 items-center">
          <span>Xin chào, {session.user?.name}</span>
          <button onClick={() => signOut()} className="bg-red-500 text-white px-2 py-1 rounded">
            Thoát
          </button>
        </div>
      ) : (
        <Link href="/login" className="bg-blue-500 text-white px-4 py-2 rounded">
          Đăng Nhập
        </Link>
      )}
    </nav>
  );
}
```

**Lưu ý khi dùng Client Component:**
Bạn phải mở file `app/layout.tsx` và bọc toàn bộ app bằng `<SessionProvider>` của `next-auth/react` thì hàm `useSession` mới hoạt động.
