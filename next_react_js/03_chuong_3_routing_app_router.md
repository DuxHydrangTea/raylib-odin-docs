# Chương 3: Routing (Điều hướng) - Tư duy cho Dự án Thực tế

Trong Next.js App Router, **Routing là linh hồn của ứng dụng**. Hệ thống routing dựa trên file-system (`File-system based routing`), nghĩa là cách bạn sắp xếp thư mục sẽ quyết định URL của trang web.

Tuy nhiên, khi làm dự án thực tế ở môi trường doanh nghiệp, chúng ta không chỉ tạo các file `page.tsx` rời rạc, mà cần quản lý layout, trạng thái loading, xử lý lỗi (error handling) và cấu trúc thư mục sao cho dễ mở rộng (scalable).

---

## 1. Nguyên lý cơ bản & Cấu trúc thư mục chuẩn Doanh nghiệp

Trong thư mục `app/`, **chỉ những thư mục nào chứa file `page.tsx` (hoặc `route.ts`) mới trở thành một đường dẫn (URL) công khai.** 

Các file đặc biệt khác:
- `layout.tsx`: Giao diện dùng chung cho các route con (Không re-render khi chuyển trang).
- `template.tsx`: Giống layout nhưng re-render (tạo lại instance) mỗi khi chuyển trang (Dùng khi cần trigger lại animation hoặc reset state).
- `loading.tsx`: UI hiển thị trong lúc chờ tải dữ liệu (sử dụng React Suspense ngầm).
- `error.tsx`: Bắt lỗi (Error Boundary) để không làm crash toàn bộ app.
- `not-found.tsx`: Trang 404 tùy chỉnh.

### 💡 Best Practice: Cấu trúc thư mục (Colocation)
Trong thực tế, đừng nhét mọi thứ vào root `components/`. Hãy đặt các component, util, style chỉ dành riêng cho một trang *ngay bên trong* thư mục của trang đó. Next.js hoàn toàn cho phép điều này vì URL chỉ được tạo khi có `page.tsx`.

```text
app/
├── (marketing)/             # Route Group: Nhóm các trang lại nhưng KHÔNG đổi URL
│   ├── about/
│   │   ├── page.tsx         # URL: /about
│   │   └── AboutHero.tsx    # Component chỉ dùng cho trang About
│   └── layout.tsx           # Layout riêng cho nhóm Marketing (vd: Header kiểu A)
│
├── (dashboard)/             # Route Group khác
│   ├── layout.tsx           # Layout riêng cho Dashboard (vd: có Sidebar)
│   ├── dashboard/
│   │   ├── page.tsx         # URL: /dashboard
│   │   ├── loading.tsx      # Loading skeleton cho dashboard
│   │   └── DashboardChart.tsx 
│   └── settings/
│       └── page.tsx         # URL: /settings
│
└── components/              # Thư mục cho các Shared Components (Button, Input, Modal...)
```

---

## 2. Dynamic Routing (Route Động)

Khi bạn làm trang chi tiết sản phẩm, chi tiết bài viết, bạn không thể hardcode từng thư mục. Hãy dùng ngoặc vuông `[param]`.

### A. Route Động Cơ Bản: `app/blog/[slug]/page.tsx`
**URL khớp:** `/blog/hello-world`, `/blog/react-18`

```tsx
// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation';

type Props = {
  params: { slug: string };
};

// Lưu ý: Trong Next.js 14+, params là một Promise trong một số trường hợp nhất định nếu bạn dùng các API mới, nhưng ở bản ổn định hiện tại nó là Object.
export default function BlogPost({ params }: Props) {
  // Lấy giá trị slug từ URL
  const { slug } = params;

  // Thực tế: Lấy dữ liệu từ DB dựa vào slug
  // Nếu không tìm thấy, ép Next.js trả về trang 404
  if (slug === 'khong-ton-tai') {
    notFound(); 
  }

  return (
    <article className="prose lg:prose-xl mx-auto py-10">
      <h1>Chi tiết bài viết: {slug}</h1>
      <p>Nội dung bài viết sẽ được fetch từ Database hoặc CMS...</p>
    </article>
  );
}
```

### B. Catch-all Routes: `[...slug]` và Optional Catch-all `[[...slug]]`
Thường dùng cho trang danh mục sản phẩm có nhiều bộ lọc (category, brand, price).
- `app/shop/[...slug]/page.tsx` khớp `/shop/a`, `/shop/a/b`, `/shop/a/b/c`.
- `app/shop/[[...slug]]/page.tsx` khớp luôn cả root là `/shop`.

---

## 3. Xử lý Trạng thái Thực tế: Loading & Error

Khi người dùng click chuyển trang, nếu trang đó mất 2s để fetch dữ liệu DB, màn hình sẽ bị "đơ" nếu không xử lý.

### File `loading.tsx` (Tạo Skeleton chuyên nghiệp)
**Vị trí:** `app/dashboard/loading.tsx`

```tsx
// app/dashboard/loading.tsx
export default function DashboardLoading() {
  // Trả về một Skeleton UI thay vì text "Loading..." đơn điệu
  return (
    <div className="p-8 space-y-4 animate-pulse">
      <div className="h-8 bg-gray-300 rounded w-1/4"></div>
      <div className="grid grid-cols-3 gap-4">
        <div className="h-32 bg-gray-200 rounded"></div>
        <div className="h-32 bg-gray-200 rounded"></div>
        <div className="h-32 bg-gray-200 rounded"></div>
      </div>
    </div>
  );
}
```

### File `error.tsx` (Bảo vệ ứng dụng không bị Crash)
Bắt buộc phải là Client Component (`"use client"`).

**Vị trí:** `app/dashboard/error.tsx`

```tsx
// app/dashboard/error.tsx
'use client'; // Error components must be Client Components

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log lỗi hệ thống ra Sentry, Datadog hoặc hệ thống tracking của công ty
    console.error("Dashboard Error:", error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center p-12 text-center border border-red-200 bg-red-50 rounded-lg mt-8">
      <h2 className="text-xl font-bold text-red-600 mb-2">Đã xảy ra lỗi hệ thống!</h2>
      <p className="text-gray-700 mb-4">{error.message || "Không thể tải dữ liệu dashboard."}</p>
      <button
        onClick={() => reset()} // Cố gắng render lại nội dung
        className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
      >
        Thử lại
      </button>
    </div>
  );
}
```

---

## 4. Kỹ thuật Nâng cao: Parallel & Intercepting Routes (Tạo Modal)

Ở các ứng dụng lớn (như Instagram, Reddit, Trello), khi bạn bấm vào 1 bài viết/ảnh, nó hiện lên dưới dạng **Modal (Popup)**. Nhưng nếu copy URL đó gửi cho người khác, họ mở ra sẽ thấy **Trang Chi Tiết (Full Page)**.

Next.js làm điều này qua sự kết hợp của:
1. **Parallel Routes (`@folder`)**: Cho phép render nhiều page độc lập trên cùng 1 layout (vd: layout chứa page chính và page modal).
2. **Intercepting Routes (`(..)folder`)**: "Bắt cóc" URL khi người dùng chuyển hướng bên trong app.

### Mô phỏng cấu trúc Modal xem ảnh (như Instagram):
```text
app/
├── feed/
│   ├── layout.tsx         # Sẽ render children và @modal
│   ├── page.tsx           # Danh sách ảnh (/feed)
│   └── @modal/            # Parallel Route
│       ├── default.tsx    # Bắt buộc có khi URL không match (trả về null)
│       └── (..)photo/     # Intercepting Route (bắt URL /photo/[id] từ bên trong feed)
│           └── [id]/
│               └── page.tsx # Hiện Modal thay vì nhảy sang trang /photo/[id] full
└── photo/                 
    └── [id]/
        └── page.tsx       # Trang chi tiết full (Sẽ hiện khi F5 hoặc user vào trực tiếp bằng link)
```

*(Chúng ta sẽ đi sâu vào code thực hành phần Modal này ở chương sau khi tích hợp chung với UI Library. Đây là một mẫu design pattern cực kỳ phổ biến trong Enterprise).*

---

## 5. Navigation: `<Link>` vs `useRouter`

### Dùng thẻ `<Link>` (Mặc định và Khuyên dùng)
- Tự động `prefetch` ngầm trang đích khi người dùng cuộn chuột thấy link, giúp chuyển trang dường như ngay lập tức (Instant routing).
- Tốt cho SEO (thẻ `<a>`).

```tsx
import Link from 'next/link';

export default function Sidebar() {
  return (
    <nav>
      {/* Tối ưu: Dùng prefetch={false} nếu trang đích quá nặng hoặc ít ai click (tiết kiệm băng thông) */}
      <Link href="/dashboard/settings" prefetch={false} className="block p-2 hover:bg-gray-100">
        Cài đặt (Settings)
      </Link>
    </nav>
  );
}
```

### Dùng `useRouter` (Khi phải thao tác bằng logic)
Thường dùng sau khi submit Form hoặc xử lý thanh toán xong.

```tsx
'use client';
import { useRouter } from 'next/navigation'; // Chú ý: import từ next/navigation, KHÔNG PHẢI next/router (của bản cũ)
import { useState } from 'react';

export default function CheckoutForm() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleCheckout = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Giả lập gọi API thanh toán
    await new Promise(r => setTimeout(r, 1000)); 

    // Chuyển hướng người dùng sau khi thành công
    router.push('/checkout/success'); 
    
    // Một số hàm khác của router:
    // router.replace('/path') -> Đổi trang nhưng không lưu vào history (người dùng bấm Back không về trang cũ)
    // router.back() -> Về trang trước
    // router.refresh() -> Fetch lại dữ liệu (RSC) của trang hiện tại mà không mất state
  };

  return (
    <form onSubmit={handleCheckout}>
      <button disabled={isSubmitting} type="submit" className="bg-blue-600 text-white px-6 py-2 rounded">
        {isSubmitting ? 'Đang xử lý...' : 'Thanh toán ngay'}
      </button>
    </form>
  );
}
```

---
**Tóm tắt Chương 3:**
Với người đi làm, việc setup Routing không chỉ là "chạy được". Bạn cần bố trí cấu trúc Route Groups `(folder)` cho gọn, xử lý `loading.tsx` dạng skeleton, bắt `error.tsx` để log lên Sentry, và nắm vững `Parallel/Intercepting Routes` để xử lý các logic UX phức tạp.

Ở Chương 4, chúng ta sẽ đào sâu vào khái niệm "hack não" nhất của Next.js: **Kiến trúc Rendering (RSC vs Client Components)**. Đây là phần quyết định hiệu năng app của bạn có đạt chuẩn Enterprise hay không!
