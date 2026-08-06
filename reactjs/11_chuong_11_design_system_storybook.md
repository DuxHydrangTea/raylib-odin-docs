# Chương 11: Xây dựng Design System (Tailwind, Radix & Storybook)

Trong một team đông người, nếu mỗi lập trình viên tự viết CSS cho cái Nút bấm (Button) của mình theo một kiểu, giao diện sẽ trở thành một mớ hỗn độn (Frankenstein UI). Enterprise Frontend đòi hỏi phải có một **Design System** (Hệ thống thiết kế) nhất quán.

Gần đây, kiến trúc Headless UI đang chiếm ưu thế tuyệt đối so với các thư viện cũ (như Bootstrap).

---

## 1. Headless UI là gì? (Radix UI)

Các thư viện cũ như Material-UI (MUI) hay Ant Design cung cấp sẵn Component cực đẹp. Nhưng khi Designer của công ty bạn vẽ một cái Select Dropdown khác hoàn toàn với Ant Design, bạn sẽ phải dùng CSS `!important` để ghi đè, tốn hàng giờ đồng hồ vật lộn.

**Headless UI (như Radix UI Primitives, Headless UI)** đi theo một hướng khác: 
- Chúng cung cấp 100% logic phức tạp (focus bằng bàn phím phím mũi tên, đóng khi click ra ngoài, hỗ trợ máy đọc màn hình Accessibility).
- Nhưng chúng **KHÔNG HỀ CÓ CSS**. Bạn tự do style chúng trông như thế nào tùy thích.

### Ví dụ về Radix UI Dialog (Modal)
Nó bao bọc sẵn toàn bộ chuẩn W3C, việc của bạn chỉ là sơn màu lên nó bằng Tailwind:

```tsx
import * as Dialog from '@radix-ui/react-dialog';

export function CustomModal() {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <button className="bg-blue-500 text-white p-2 rounded">Mở Modal</button>
      </Dialog.Trigger>
      
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50 backdrop-blur-sm" />
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-xl shadow-lg">
          <Dialog.Title className="text-xl font-bold">Xác nhận xóa?</Dialog.Title>
          <Dialog.Description className="mt-2 text-gray-500">
            Hành động này không thể hoàn tác.
          </Dialog.Description>
          
          <div className="mt-4 flex justify-end gap-2">
            <Dialog.Close asChild>
              <button className="bg-gray-200 p-2 rounded">Hủy</button>
            </Dialog.Close>
            <button className="bg-red-500 text-white p-2 rounded">Xóa ngay</button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

---

## 2. Tiện ích hóa với Tailwind CSS và CVA

Để dễ dàng quản lý các biến thể (variants) của Component (Button to, Button nhỏ, Button màu đỏ, Button màu xanh), ta sử dụng công cụ `class-variance-authority` (CVA). Đây là cách mà thư viện nổi tiếng **shadcn/ui** đang sử dụng.

```tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/shared/utils'; // Tiện ích gộp class (clsx + tailwind-merge)

const buttonVariants = cva(
  // Base classes: Luôn luôn có
  "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:opacity-50",
  {
    variants: {
      intent: {
        primary: "bg-blue-600 text-white hover:bg-blue-700",
        destructive: "bg-red-500 text-white hover:bg-red-600",
        outline: "border border-gray-300 bg-transparent hover:bg-gray-100",
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4 py-2",
        lg: "h-12 px-8 text-lg",
      }
    },
    defaultVariants: {
      intent: "primary",
      size: "md",
    },
  }
);

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {}

export function Button({ className, intent, size, ...props }: ButtonProps) {
  return (
    <button className={cn(buttonVariants({ intent, size, className }))} {...props} />
  );
}

// Khi dùng: 
// <Button intent="destructive" size="lg">Xóa tài khoản</Button>
```

---

## 3. Storybook - Danh mục Component độc lập

Khi team của bạn làm ra 50 cái Component (Button, Table, Card...), làm sao để người mới vào dự án biết dự án có những Component nào để tái sử dụng?

**Storybook** là một môi trường phát triển UI độc lập. Nó chạy trên một cổng riêng (VD: localhost:6006) liệt kê toàn bộ các Component của dự án dưới dạng một quyển Catalog. Lập trình viên có thể click thử, thay đổi Props và xem component thay đổi ra sao mà không cần phải nhúng Component đó vào trang App chính.

### File `Button.stories.tsx`:
```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'UI/Button',
  component: Button,
};
export default meta;

type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    intent: 'primary',
    children: 'Button Chính',
  },
};

export const Destructive: Story = {
  args: {
    intent: 'destructive',
    children: 'Xóa Ngay',
  },
};
```

---

## Tóm tắt Actionable
1. **Muốn làm web đẹp chuẩn chỉnh và nhanh?** Đừng cài Bootstrap hay viết CSS thuần. Hãy học **Tailwind CSS**.
2. **Không muốn tự làm Modal, Dropdown vì sợ lỗi Accessibility?** Hãy cài **Radix UI** (hoặc dùng thẳng **shadcn/ui** - bộ template copy/paste dựa trên Tailwind + Radix UI cực kỳ nổi tiếng hiện nay).
3. Sử dụng **CVA** để quản lý các Variant của Component thay vì viết hằng hà sa số các câu lệnh `if...else` rườm rà.
