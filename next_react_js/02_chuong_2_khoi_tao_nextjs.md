# Chương 2: Khởi tạo & Cấu trúc Dự án Next.js (Chuẩn Enterprise)

Khi làm việc trong môi trường doanh nghiệp hoặc làm việc nhóm, cách bạn setup dự án ban đầu quyết định 50% sự thành bại của việc bảo trì sau này. Chúng ta không chỉ `create-next-app` rồi code ngay, mà cần thiết lập quy chuẩn.

---

## 1. Khởi tạo dự án với thiết lập chuyên nghiệp

Mở Terminal và chạy lệnh:

```bash
npx create-next-app@latest enterprise-app
```

Khi các lựa chọn hiện ra, hãy chọn cấu hình khuyên dùng cho dự án lớn:

```text
Would you like to use TypeScript?  Yes      (BẮT BUỘC)
Would you like to use ESLint?  Yes          (Để giữ code chuẩn)
Would you like to use Tailwind CSS?  Yes    
Would you like to use `src/` directory?  Yes (LƯU Ý: Rất quan trọng để tách bạch source code với các file config)
Would you like to use App Router? (recommended)  Yes
Would you like to customize the default import alias (@/*)?  No
```

### Tại sao lại chọn thư mục `src/`?
Nếu không có `src/`, thư mục gốc của bạn sẽ chứa lẫn lộn: `app/`, `components/`, `package.json`, `next.config.mjs`, `docker-compose.yml`, `.eslintrc.json`, v.v... Rất rác!
Dùng `src/` giúp cách ly toàn bộ code logic (`src/app`, `src/components`, `src/lib`) khỏi các file cấu hình nằm ở ngoài cùng.

---

## 2. Absolute Imports (`@/...`) thay vì Relative Imports

Trong các dự án cũ, bạn hay thấy những đoạn import ác mộng như thế này:
```ts
// ❌ Rất khó bảo trì khi chuyển thư mục
import { Button } from '../../../../components/ui/Button'; 
```

Next.js đã tự cấu hình Absolute Import với tiền tố `@/` (trỏ thẳng vào thư mục `src/`).
```ts
// ✅ Chuẩn Enterprise
import { Button } from '@/components/ui/Button';
import { formatDate } from '@/lib/utils';
```

---

## 3. Cấu trúc thư mục (Folder Structure) đề xuất

Sau khi setup, hãy chủ động tạo thêm một số thư mục chuẩn mực bên trong `src/`:

```text
enterprise-app/
├── public/                 # Chứa logo, favicon, ảnh tĩnh
├── src/
│   ├── app/                # CHỈ CHỨA file định tuyến (page.tsx, layout.tsx, route.ts)
│   ├── components/         
│   │   ├── ui/             # Các component câm (Dumb UI: Button, Input, Modal)
│   │   └── shared/         # Các component chứa logic dùng chung (Navbar, Footer)
│   ├── lib/                # Các thư viện bên thứ 3 (prisma.ts, axios.ts)
│   ├── utils/              # Các hàm helper phụ trợ (formatDate.ts, math.ts)
│   ├── hooks/              # Custom React Hooks (useAuth.ts, useDebounce.ts)
│   ├── types/              # Định nghĩa Interface/Type TypeScript dùng chung
│   └── services/           # Chứa các hàm fetch data gọi API (user.service.ts)
├── .env.local              # File chứa biến môi trường (Database URL, Secret keys)
├── .prettierrc             # File cấu hình format code (bạn nên tự thêm)
└── package.json
```

---

## 4. Quản lý Biến Môi Trường (Environment Variables)

Biến môi trường giúp bạn giấu các khóa bí mật (Secret Keys). 
- Tạo file `.env.local` ở thư mục gốc (Ngang hàng package.json).
- **Lưu ý cực kỳ quan trọng:** File này ĐÃ ĐƯỢC tự động thêm vào `.gitignore`, tuyệt đối KHÔNG push nó lên GitHub.

```env
# .env.local
DATABASE_URL="postgres://admin:password@localhost:5432/mydb"
STRIPE_SECRET_KEY="sk_test_123456"

# CHÚ Ý: Bất kỳ biến nào muốn dùng được ở giao diện Client (trình duyệt)
# Bắt buộc phải có tiền tố NEXT_PUBLIC_
NEXT_PUBLIC_API_URL="https://api.my-domain.com"
```

Cách lấy biến trong Code:
```ts
// Trong Server Components hoặc API Routes
const dbUrl = process.env.DATABASE_URL;

// Trong Client Components (phải có NEXT_PUBLIC_)
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

---

## 5. Cấu hình Code Quality (Linting & Formatting)

Để làm việc nhóm không bị cãi nhau vì "thằng dùng nháy đơn, đứa dùng nháy kép", "người thụt 2 dấu cách, kẻ thụt 4 dấu", hãy ép khuôn dự án:

1. **Cài đặt Prettier:**
   ```bash
   npm install -D prettier eslint-config-prettier
   ```
2. **Tạo file `.prettierrc` ở thư mục gốc:**
   ```json
   {
     "semi": true,
     "singleQuote": true,
     "trailingComma": "es5",
     "tabWidth": 2
   }
   ```
3. *(Mở rộng)* Trong doanh nghiệp, người ta thường cài thêm **Husky** và **Lint-staged**. Mỗi khi ai đó gõ lệnh `git commit`, hệ thống sẽ tự động format và check lỗi toàn bộ code. Nếu có lỗi đỏ, sẽ block không cho commit!

---

**Kết luận:** 
Bạn đã có một khung sườn dự án Next.js vững chắc như lô cốt. Hãy luôn giữ thói quen sử dụng `src/`, `Absolute Imports`, và kiểm soát chặt chẽ `Environment Variables`. 

Ở chương sau (Chương 3), chúng ta sẽ bắt tay vào việc quan trọng nhất: **Định tuyến (Routing) nâng cao cho các luồng UX phức tạp**.
