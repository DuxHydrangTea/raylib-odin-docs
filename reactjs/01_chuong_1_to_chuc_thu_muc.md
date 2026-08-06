# Chương 1: Kiến trúc & Tổ chức thư mục chuẩn Enterprise

Trong các dự án nhỏ, bạn có thể để tất cả Component vào thư mục `components/`, các hook vào `hooks/`. Nhưng khi dự án phình to (Enterprise level), cách tổ chức phẳng (Flat structure) này sẽ dẫn đến việc **không thể bảo trì**, khó khăn trong việc tìm kiếm và refactor code. 

Dưới đây là 2 kiến trúc phổ biến nhất được sử dụng trong các dự án React lớn.

---

## 1. Feature-Sliced Design (FSD) - Kiến trúc ưu tiên theo tính năng

Thay vì chia theo *loại file* (components, hooks, utils), chúng ta chia theo **tính năng (feature)**. Mỗi tính năng hoạt động như một module độc lập, đóng gói UI, logic và trạng thái của riêng nó.

### Cấu trúc tiêu chuẩn:
```text
src/
├── app/               # Nơi khởi tạo ứng dụng (Store, Global Styles, Providers, Router setup)
├── processes/         # (Tùy chọn) Quy trình liên quan đến nhiều trang (VD: Checkout process)
├── pages/             # Layout cấu trúc của các trang (Chỉ gọi các Widget/Features, ít logic)
├── widgets/           # Các khối UI lớn kết hợp nhiều feature (VD: Header, Sidebar, UserProfileWidget)
├── features/          # Các tính năng cụ thể mang giá trị nghiệp vụ (VD: auth, cart, posts)
│   ├── auth/
│   │   ├── api/       # Gọi API (login, register)
│   │   ├── model/     # State management (Zustand/Redux store)
│   │   ├── ui/        # Các component UI nội bộ (LoginForm, RegisterForm)
│   │   └── index.ts   # Public API (Export những gì bên ngoài được phép dùng)
├── entities/          # Các thực thể nghiệp vụ (VD: User, Product)
└── shared/            # Code dùng chung toàn dự án (UI kit, hooks, utils, config)
    ├── ui/            # Button, Input, Modal...
    ├── api/           # Axios instance, API base
    └── utils/         # formatTime, calculatePrice...
```

### Tại sao lại dùng FSD?
- **Tính đóng gói cao (Encapsulation):** Feature `auth` sẽ không biết gì về Feature `cart`. Nếu bạn xóa tính năng `cart`, bạn chỉ cần xóa đúng 1 thư mục `features/cart`, không cần đi tìm rải rác trong `components/`, `hooks/`, `api/`.
- **Dễ dàng Scale:** Khi team đông lên, mỗi team có thể handle một hoặc nhiều feature độc lập, ít bị conflict (merge conflict) code.

---

## 2. Quy tắc Public API (index.ts)

Đây là quy tắc **sống còn** khi làm việc trong team lớn. Một module (hoặc thư mục) **chỉ được phép export ra ngoài những gì cần thiết** thông qua file `index.ts`. Các component/module khác khi muốn dùng, bắt buộc phải import thông qua `index.ts` này.

**Sai (Bad Practice):** Import trực tiếp vào ruột của tính năng khác
```typescript
// KHÔNG ĐƯỢC LÀM NHƯ NÀY
import { loginApi } from '@/features/auth/api/login';
import { LoginForm } from '@/features/auth/ui/LoginForm';
```

**Đúng (Enterprise Practice):**
```typescript
// Trong thư mục features/auth/index.ts
export { LoginForm } from './ui/LoginForm';
export { useAuthStore } from './model/store';
// Các hàm api nội bộ sẽ KHÔNG được export

// Ở file cần dùng:
import { LoginForm, useAuthStore } from '@/features/auth';
```
> Việc che giấu các thành phần nội bộ giúp bạn thoải mái thay đổi logic bên trong thư mục `auth` mà không lo làm chết app ở những chỗ khác.

---

## 3. Atomic Design (Dành riêng cho thư mục `shared/ui`)

Đối với các UI Component dùng chung (UI Kit), chúng ta thường áp dụng Atomic Design để tái sử dụng tối đa:
- **Atoms (Nguyên tử):** Các thành phần cơ bản nhất không thể chia nhỏ hơn (Button, Input, Label, Icon).
- **Molecules (Phân tử):** Kết hợp nhiều Atom (VD: SearchBar = Input + Button).
- **Organisms (Sinh vật):** Kết hợp các Molecule tạo thành khối UI lớn (VD: Header, Footer).

```text
src/shared/ui/
├── atoms/
│   ├── Button.tsx
│   └── Input.tsx
├── molecules/
│   ├── FormField.tsx      (Label + Input + ErrorText)
│   └── SearchInput.tsx    (Input + IconSearch)
└── organisms/
    └── TopNavigationBar.tsx
```

---

## 4. Tóm tắt Actionable cho người đi làm
1. **Luôn dùng Alias (`@/`)**: Cấu hình `tsconfig.json` và `vite.config.ts` để dùng `import ... from '@/...'` thay vì `../../../../`.
2. **Tuân thủ ranh giới Import (Import Boundaries)**: Các layer bên trên được quyền import layer bên dưới (app -> pages -> widgets -> features -> entities -> shared), nhưng **không được ngược lại**. (VD: `shared` không được phép import bất kỳ thứ gì từ `features`). Lỗi này nên được bắt bằng `eslint-plugin-boundaries`.
3. **Thống nhất Naming Convention**: 
   - Component: `PascalCase` (`UserProfile.tsx`).
   - Hook: `camelCase` có tiền tố `use` (`useToggle.ts`).
   - Helper/Util: `camelCase` (`formatDate.ts`).
   - Hằng số (Constants): `UPPER_SNAKE_CASE` (`MAX_RETRY_COUNT`).
