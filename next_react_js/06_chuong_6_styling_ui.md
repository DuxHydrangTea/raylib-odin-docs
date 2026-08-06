# Chương 6: Styling (Giao diện) Chuẩn Doanh Nghiệp

Styling trong Next.js không có một quy chuẩn duy nhất bắt buộc, bạn có thể dùng CSS thuần, SCSS, Tailwind, CSS Modules, hay CSS-in-JS (như styled-components). 

Tuy nhiên, **Tailwind CSS + CSS Modules** là bộ đôi được giới công nghệ ưa chuộng nhất hiện nay vì hiệu suất sinh file CSS cực nhỏ, không bị đụng độ class và tương thích 100% với Server Components.

*(Lưu ý: Các thư viện CSS-in-JS cũ như styled-components yêu cầu thẻ `<style>` sinh ra bằng JS ở Client, cấu hình phức tạp với App Router và có thể làm mất lợi thế tĩnh của RSC. Hạn chế sử dụng ở dự án mới).*

---

## 1. Tailwind CSS - Tiêu chuẩn ngành

Khi chúng ta khởi tạo dự án với tùy chọn `--tailwind`, Next.js đã cấu hình sẵn file `tailwind.config.ts` và `globals.css`.

**Best Practice cho Tailwind:** Không viết inline-class dài lê thê lặp đi lặp lại. Hãy dùng thư viện `clsx` và `tailwind-merge` (thường được gói gọn thành file `cn.ts`).

### Mẹo chuyên nghiệp: Hàm ghép Class động (Conditional Classes)
Trong dự án đi làm, bạn rất hay phải đổi class dựa theo state hoặc props (ví dụ Nút màu xanh khi thành công, xám khi bị vô hiệu hóa).

**Tạo file Utils:** `lib/utils.ts` (cần cài đặt `npm install clsx tailwind-merge`)

```ts
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  // clsx xử lý việc gộp các object/array điều kiện thành chuỗi
  // twMerge xử lý conflict (ví dụ: 'p-4 p-8' -> nó sẽ giữ lại 'p-8')
  return twMerge(clsx(inputs));
}
```

**Sử dụng để tạo một UI Component cực kỳ xịn xò (Reusable Component):**
**Vị trí:** `components/ui/Button.tsx`

```tsx
import { ButtonHTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

// Khai báo Props mở rộng từ button mặc định của HTML
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
}

export default function Button({ 
  className, 
  variant = 'primary', 
  size = 'md', 
  ...props 
}: ButtonProps) {
  return (
    <button
      className={cn(
        // Base classes (Lúc nào cũng có)
        "inline-flex items-center justify-center rounded-md font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none",
        
        // Classes tùy theo 'variant'
        variant === 'primary' && "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500",
        variant === 'secondary' && "bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500",
        variant === 'danger' && "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500",
        
        // Classes tùy theo 'size'
        size === 'sm' && "h-8 px-3 text-xs",
        size === 'md' && "h-10 px-4 py-2",
        size === 'lg' && "h-12 px-8 text-lg",
        
        // Cho phép user ghi đè (override) class từ bên ngoài truyền vào thông qua props 'className'
        className
      )}
      {...props}
    />
  );
}
```

Cách dùng Component trên:
```tsx
<Button variant="danger" size="lg" className="w-full mt-4" disabled>
  Xóa tài khoản
</Button>
```

---

## 2. CSS Modules - Khi Tailwind không đủ (hoặc quá rối)

Trong những trường hợp bạn cần animation siêu phức tạp hoặc một component có quá nhiều cấu trúc CSS giả (pseudo-elements như `::before`, `::after`), Tailwind có thể biến mã JSX thành bãi rác. Đó là lúc dùng CSS Modules.

CSS Modules tự động mã hóa tên class (hash), bảo đảm class "card" ở component A không bao giờ đụng độ class "card" ở component B.

**Tạo file CSS (bắt buộc đuôi `.module.css`):**
**Vị trí:** `components/AnimatedCard/styles.module.css`

```css
/* Chỉ ảnh hưởng bên trong module này */
.cardContainer {
  background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0));
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255,255,255,0.18);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
  transition: transform 0.3s ease;
}

.cardContainer:hover {
  transform: translateY(-10px) scale(1.02);
}

.title {
  color: #fff;
  font-weight: 700;
  text-shadow: 0px 2px 4px rgba(0,0,0,0.5);
}
```

**Sử dụng vào JSX:**
**Vị trí:** `components/AnimatedCard/index.tsx`

```tsx
import styles from './styles.module.css'; // Import như một object
import { cn } from '@/lib/utils'; // Vẫn có thể dùng chung với tailwind

export default function AnimatedCard({ title, desc }: { title: string, desc: string }) {
  return (
    // Kết hợp class sinh ra từ Module và class của Tailwind
    <div className={cn(styles.cardContainer, "p-8 max-w-sm mx-auto mt-10")}>
      <h2 className={cn(styles.title, "text-2xl mb-4")}>{title}</h2>
      <p className="text-gray-200">{desc}</p>
    </div>
  );
}
```

**Tóm tắt Chương 6:**
Trong dự án Next.js nghiêm túc, hãy lấy Tailwind làm nền tảng chính trị vì nó giúp code siêu nhanh và bundle siêu nhỏ. Luôn dùng hàm `cn()` (clsx + tailwind-merge) để viết các UI components linh hoạt. Chỉ fallback về CSS Modules khi bạn phải đối phó với CSS animation / layout mang tính đặc thù cao.
