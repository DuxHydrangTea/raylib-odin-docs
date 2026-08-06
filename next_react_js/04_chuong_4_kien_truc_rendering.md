# Chương 4: Kiến trúc Rendering - React Server Components (RSC)

Hiểu sai về Rendering là nguyên nhân số một khiến các ứng dụng Next.js chạy chậm, tốn băng thông và mất lợi thế SEO. Ở Next.js App Router, mọi thứ mặc định là **Server Components**. 

Là một kỹ sư phần mềm, bạn cần kiểm soát chính xác code nào chạy ở Server và code nào chạy ở trình duyệt (Client).

---

## 1. Mặc định: React Server Components (RSC)

Trong thư mục `app/`, nếu bạn tạo một component, nó sẽ là **Server Component** (trừ khi bạn gắn `"use client"`).

### Đặc điểm của Server Component:
- **Chạy duy nhất trên Server:** Trình duyệt sẽ nhận kết quả là mã HTML tĩnh đã được render, không phải tải JavaScript chứa logic của component đó.
- **Có quyền truy cập tài nguyên backend:** Bạn có thể kết nối Database (Prisma/Drizzle), đọc file hệ thống, sử dụng biến môi trường (Environment Variables) chứa Secret Keys một cách an toàn tuyệt đối.
- **KHÔNG thể tương tác trực tiếp:** Không dùng được `useState`, `useEffect`, `onClick`, `onChange`. Trình duyệt không biết các hàm này.

### Code mẫu chuẩn Server Component
**Vị trí:** `app/users/page.tsx`

```tsx
import { db } from '@/lib/db'; // Giả lập thư viện DB an toàn trên server

export default async function UsersPage() {
  // 🚀 CỰC KỲ AN TOÀN: Query DB trực tiếp mà không lộ thông tin kết nối ra client
  const users = await db.user.findMany(); 

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold">Danh sách người dùng</h1>
      <ul className="mt-4 space-y-2">
        {users.map(user => (
          <li key={user.id} className="p-4 bg-white shadow rounded">
            {user.name} - {user.email}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

## 2. Client Components: Bổ sung "Tương tác"

Khi bạn cần xử lý thao tác người dùng (click, gõ phím) hoặc dùng state/effect, bạn phải dùng **Client Component** bằng cách đặt `"use client"` ở dòng đầu tiên của file.

Nhưng **LƯU Ý LỚN**: Client Component ở Next.js không có nghĩa là nó chỉ render ở Client. Nó **vẫn được Pre-render thành HTML ở Server** để tăng tốc First Load và SEO, sau đó gửi về trình duyệt cùng với cục JavaScript để "Hydrate" (gắn sự kiện tương tác vào HTML).

### Code mẫu: Client Component chuẩn
**Vị trí:** `components/SearchBox.tsx`

```tsx
'use client'; // Kích hoạt Hydration ở Client

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function SearchBox() {
  const [query, setQuery] = useState('');
  const router = useRouter();

  const handleSearch = () => {
    // Tương tác phía Client: thay đổi URL
    if (query.trim()) router.push(`/search?q=${query}`);
  };

  return (
    <div className="flex gap-2">
      <input 
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
        className="border rounded p-2 text-black"
        placeholder="Tìm kiếm..."
      />
      <button onClick={handleSearch} className="bg-blue-600 text-white px-4 py-2 rounded">
        Tìm
      </button>
    </div>
  );
}
```

---

## 3. Tư duy tối ưu (Pro-tips cho Enterprise)

Để ứng dụng siêu nhanh, hãy tuân thủ nguyên tắc: **Đẩy "use client" xuống mức thấp nhất có thể ở cây component (Push Client Components to the Leaves).**

❌ **Sai lầm phổ biến (Bad Pattern):** Gắn `"use client"` ở layout hoặc page gốc. Điều này biến toàn bộ children thành Client Component, phá hỏng mục đích dùng Next.js.

✅ **Chuẩn Enterprise (Good Pattern):**

```tsx
// app/blog/page.tsx (MẶC ĐỊNH LÀ SERVER COMPONENT)
import BlogPostContent from './BlogPostContent'; // Server Component
import ShareButton from './ShareButton';         // Client Component (có nút click)

export default async function BlogPostPage({ params }: { params: { slug: string } }) {
  // Lấy dữ liệu nhanh và an toàn trên server
  const post = await fetchPost(params.slug);

  return (
    <article className="max-w-2xl mx-auto">
      {/* Phần lớn HTML được render trên server, 0 byte JS tải về client */}
      <h1 className="text-3xl font-bold">{post.title}</h1>
      <BlogPostContent content={post.content} /> 
      
      {/* 
        Chỉ truyền những data có thể serialize (string, number, object đơn giản) 
        từ Server xuống Client Component.
      */}
      <div className="mt-8 border-t pt-4">
        <ShareButton url={`https://domain.com/blog/${params.slug}`} />
      </div>
    </article>
  );
}
```

### Một quy tắc vàng nữa: Interleaving (Lồng Component)
Bạn **KHÔNG THỂ** import một Server Component vào bên trong một Client Component một cách trực tiếp.
Nhưng bạn **CÓ THỂ** truyền Server Component vào Client Component thông qua `props` (thường là `children`).

```tsx
// components/ClientLayoutWrapper.tsx
'use client'
export default function ClientLayoutWrapper({ children }: { children: React.ReactNode }) {
  return <div className="client-wrapper" onClick={() => console.log('click')}>{children}</div>;
}

// app/page.tsx (Server)
export default function Page() {
  return (
    <ClientLayoutWrapper>
      <ServerComponent /> {/* Hoạt động hoàn hảo! Server render cái này rồi nhét vào lỗ 'children' */}
    </ClientLayoutWrapper>
  )
}
```

Chương 4 kết thúc! Nắm được RSC là bạn đã nắm được 70% sức mạnh Next.js. Chuyển sang Chương 5, chúng ta sẽ học cách Fetch Data và thao tác Caching xịn xò.
