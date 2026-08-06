# Chương 5: Data Fetching, Caching & Server Actions

Ở các framework truyền thống (React thuần), bạn dùng `useEffect` và `axios` để lấy data. Việc này gây ra tình trạng "thác nước" (waterfall), giật lag do loading spinner liên tục và SEO bằng 0.

Với Next.js, chúng ta lấy dữ liệu trực tiếp trên Server và điều khiển được cả bộ nhớ đệm (Cache).

---

## 1. Fetching Data trên Server (Mặc định)

Next.js đã mở rộng hàm `fetch` mặc định của trình duyệt để có thể hoạt động mạnh mẽ trên Node.js (Server).

### Mô hình Cache Data (Cực kỳ quan trọng)

**Vị trí:** `app/dashboard/stats/page.tsx`

```tsx
export default async function StatsPage() {
  // Next.js TỰ ĐỘNG CACHE request này vĩnh viễn (force-cache mặc định)
  // Phù hợp cho dữ liệu tĩnh: Bài viết blog, danh sách danh mục...
  const staticData = await fetch('https://api.example.com/categories');
  
  // TẮT CACHE (Tương đương SSR - Server Side Rendering)
  // Request chạy lại mỗi khi có người dùng truy cập. Dùng cho dữ liệu biến động cao.
  const dynamicData = await fetch('https://api.example.com/realtime-stats', { 
    cache: 'no-store' 
  });

  // ISR - Incremental Static Regeneration (Tối ưu nhất cho Performance)
  // Cache dữ liệu lại, nhưng cứ sau 60 giây nếu có người truy cập thì fetch ngầm lại data mới.
  const revalidatingData = await fetch('https://api.example.com/prices', { 
    next: { revalidate: 60 } 
  });

  const stats = await dynamicData.json();

  return (
    <div>
      <h2>Thống kê hiện tại: {stats.users} user online</h2>
    </div>
  );
}
```

---

## 2. Revalidate On-Demand (Làm mới Cache theo ý muốn)

Thay vì chờ hết thời gian, trong thực tế khi Admin vừa nhấn nút "Sửa bài viết", chúng ta muốn bài viết được cập nhật mới trên website ngay lập tức. Ta dùng `revalidateTag`.

```tsx
// 1. Khi lấy data, ta gắn cho nó cái "mác" (tag)
const res = await fetch('https://api.example.com/articles', { 
  next: { tags: ['articles'] } 
});

// 2. Ở chỗ khác (ví dụ một API Route webhook từ CMS trả về khi Admin lưu bài)
import { revalidateTag } from 'next/cache';

export async function POST() {
  // Xóa toàn bộ cache của các request có mang tag 'articles'
  revalidateTag('articles');
  return Response.json({ message: "Đã làm mới dữ liệu" });
}
```

---

## 3. Server Actions (Đột biến dữ liệu không cần API)

Đây là tính năng "sát thủ" của Next.js 14+. 
Thay vì phải tạo form, tạo state loading, tạo một thư mục `/api/submit`, lấy dữ liệu form rồi fetch... Server Actions cho phép gọi một hàm chạy ngầm trên Server *ngay từ Client Component*.

### Code mẫu chuẩn Enterprise cho Form xử lý dữ liệu
**Vị trí Logic (Server):** `app/actions/user.ts` (Tách riêng file action để code gọn gàng)

```ts
'use server'; // Khai báo file này chứa Server Actions

import { db } from '@/lib/db';
import { revalidatePath } from 'next/cache';

export async function updateUserProfile(formData: FormData) {
  // Giả lập kiểm tra Auth (Thực tế bạn dùng thư viện session như auth())
  const userId = formData.get('id') as string;
  const name = formData.get('name') as string;

  try {
    // Cập nhật Database trực tiếp
    await db.user.update({ where: { id: userId }, data: { name } });
    
    // Xóa cache của trang cá nhân để user thấy tên mới ngay lập tức
    revalidatePath(`/profile`);
    return { success: true, message: "Cập nhật thành công!" };
  } catch (error) {
    return { success: false, message: "Lỗi hệ thống." };
  }
}
```

**Vị trí UI (Client):** `components/ProfileForm.tsx`

```tsx
'use client';

// useFormStatus đang nằm trong thư viện react-dom (React 19) 
// Nó lấy trạng thái (đang submit hay không) từ cái <form> bọc ngoài
import { useFormStatus } from 'react-dom'; 
import { updateUserProfile } from '@/app/actions/user';
import toast from 'react-hot-toast'; // Thư viện hiển thị thông báo

// Component con xử lý nút bấm (BẮT BUỘC TÁCH RIÊNG ra con để useFormStatus hoạt động)
function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <button 
      type="submit" 
      disabled={pending}
      className={`px-4 py-2 text-white rounded ${pending ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'}`}
    >
      {pending ? 'Đang lưu...' : 'Lưu Thay Đổi'}
    </button>
  );
}

export default function ProfileForm({ userId, currentName }: { userId: string, currentName: string }) {
  // Hàm trung gian để gọi Server Action và xử lý UI (toast/alert)
  const clientAction = async (formData: FormData) => {
    // formData.append('id', userId); // Hoặc bạn dùng input type hidden bên dưới
    const res = await updateUserProfile(formData);
    
    if (res.success) toast.success(res.message);
    else toast.error(res.message);
  };

  return (
    // Form action nay sẽ tự động gọi clientAction
    <form action={clientAction} className="flex flex-col gap-4 max-w-sm">
      <input type="hidden" name="id" value={userId} />
      
      <div>
        <label className="block text-sm font-medium">Họ tên</label>
        <input 
          type="text" 
          name="name" 
          defaultValue={currentName} 
          required 
          className="mt-1 w-full border rounded p-2"
        />
      </div>

      <SubmitButton />
    </form>
  );
}
```

**Tóm tắt chương 5:**
Với `fetch` ở Server, bạn kiểm soát toàn diện Caching.
Với `Server Actions` và `useFormStatus`, việc submit Form giờ đây an toàn, bảo mật, code siêu ngắn gọn và Không Cần Viết API Endpoints riêng.
