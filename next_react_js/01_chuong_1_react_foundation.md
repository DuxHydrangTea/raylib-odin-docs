# Chương 1: Nền tảng React cơ bản & Quản lý State (Chuẩn Enterprise)

Để làm việc tốt với Next.js, chúng ta cần nắm vững React. Trong môi trường doanh nghiệp, viết code "chạy được" là chưa đủ, code phải dễ bảo trì, strict type (TypeScript), và hiệu năng cao.

*(Lưu ý: Bạn có thể đọc trước phần này. Ở Chương 2, chúng ta sẽ tạo dự án Next.js và bạn có thể copy các code này vào để chạy thử).*

---

## 1. Component, JSX & Tư duy chia tách Types

Trong các dự án lớn, chúng ta không viết lẫn lộn Component và Type definitions. Bạn nên tách Type/Interface riêng biệt hoặc định nghĩa rõ ràng.

### Code mẫu: Định nghĩa Component chuẩn mực
**Vị trí file:** `types/user.ts` (Thư mục chuyên chứa Type)
```ts
export interface UserData {
  id: string;
  name: string;
  role: 'ADMIN' | 'USER';
  isActive: boolean;
}
```

**Vị trí file:** `components/UserCard.tsx`
```tsx
import React from 'react';
import type { UserData } from '@/types/user'; // Import type từ file dùng chung

// Khai báo rõ ràng Props nhận vào
interface UserCardProps {
  user: UserData;
  onEdit?: (id: string) => void; // Optional function prop
}

export default function UserCard({ user, onEdit }: UserCardProps) {
  return (
    <div className="border p-4 rounded-lg my-2 flex justify-between items-center">
      <div>
        <h2 className="text-xl font-semibold">{user.name}</h2>
        <p className="text-gray-600">Vai trò: {user.role}</p>
      </div>
      
      {/* Cẩn thận với thẻ Button: Luôn định nghĩa type="button" để tránh submit nhầm form */}
      {onEdit && (
        <button 
          type="button" 
          onClick={() => onEdit(user.id)}
          className="text-blue-500 hover:underline"
        >
          Chỉnh sửa
        </button>
      )}
    </div>
  );
}
```

---

## 2. Quản lý trạng thái (State) tránh Rác (Anti-patterns)

Rất nhiều người mới lạm dụng `useState` cho mọi thứ. 
**Quy tắc đi làm:**
- Nếu một giá trị có thể tính toán được từ state khác -> Đừng tạo state mới.
- Tránh state lồng nhau quá sâu (deeply nested object).

> **Lưu ý trong Next.js App Router:** 
> Các component dùng state/effect BẮT BUỘC phải thêm dòng `"use client";` ở trên cùng.

### Code mẫu: Quản lý Form State chuyên nghiệp
```tsx
"use client";

import React, { useState } from 'react';

export default function UserProfileForm() {
  // Thay vì dùng 3 state riêng lẻ, hãy gộp thành 1 object state
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: ''
  });

  // Derived state (Tự tính toán, không cần lưu vào useState)
  const fullName = `${formData.firstName} ${formData.lastName}`.trim();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    // Cập nhật an toàn với spread operator
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <form className="p-4">
      <input 
        name="firstName" 
        value={formData.firstName} 
        onChange={handleChange} 
        placeholder="Họ"
      />
      <p>Họ tên đầy đủ của bạn: {fullName}</p>
    </form>
  );
}
```

---

## 3. Tách biệt Logic & UI với Custom Hooks

Đừng nhồi nhét gọi API, tính toán logic và UI vào chung một file Component. Hãy viết **Custom Hooks** để tái sử dụng logic.

**Vị trí file:** `hooks/useWindowSize.ts`
```ts
"use client";
import { useState, useEffect } from 'react';

// Custom hook chuyên nghiệp tái sử dụng ở mọi component
export function useWindowSize() {
  const [windowSize, setWindowSize] = useState({
    width: typeof window !== 'undefined' ? window.innerWidth : 0,
    height: typeof window !== 'undefined' ? window.innerHeight : 0,
  });

  useEffect(() => {
    // Chỉ chạy trên client
    if (typeof window === 'undefined') return;

    const handleResize = () => {
      setWindowSize({ width: window.innerWidth, height: window.innerHeight });
    };

    window.addEventListener('resize', handleResize);
    // BẮT BUỘC: Cleanup function để tránh memory leak
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
}
```

Và ở Component, bạn chỉ cần gọi:
```tsx
const { width } = useWindowSize();
```

---

## 4. Tối ưu hiệu năng (useMemo & useCallback)

Khi app lớn lên, re-render là vấn đề lớn nhất của React.

- **useMemo:** Ghi nhớ một giá trị tính toán nặng.
- **useCallback:** Ghi nhớ một hàm (tránh tạo lại reference mới mỗi lần render, giúp các component con bọc trong `React.memo` không bị re-render vô ích).

```tsx
import React, { useMemo, useCallback, useState } from 'react';

export default function Dashboard({ rawData }) {
  const [filter, setFilter] = useState('ALL');

  // Chỉ tính toán lại khi rawData hoặc filter thay đổi (Tránh lag vòng lặp)
  const processedData = useMemo(() => {
    return rawData.filter(item => filter === 'ALL' || item.type === filter);
  }, [rawData, filter]);

  // Giữ lại hàm này, không tạo reference mới
  const handleExport = useCallback(() => {
    console.log("Exporting...", processedData);
  }, [processedData]);

  return (
    <div>
       {/* UI code */}
    </div>
  );
}
```

---
**Tóm tắt Chương 1:**
- Hãy luôn viết TypeScript interface rõ ràng.
- Đừng lạm dụng `useState`, hãy tính toán từ props (derived state) nếu có thể.
- Đóng gói logic phức tạp (Side Effects) vào **Custom Hooks**.
- Biết cách chống memory leak trong `useEffect` (dùng cleanup function).
- Dùng `useMemo` và `useCallback` cho các tác vụ nặng.

Tiếp theo, hãy sang **Chương 2** để khởi tạo dự án với cấu trúc chuyên nghiệp!
