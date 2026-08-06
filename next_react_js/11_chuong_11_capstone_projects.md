# Chương 11: Dự án thực hành (Capstone Projects) - Áp dụng kiến thức

Không có cách nào học lập trình tốt hơn là tự tay làm các dự án thực tế. Dưới đây là kiến trúc đề xuất cho 3 dự án lớn, giúp bạn ôn lại toàn bộ 10 chương trước và bổ sung hoàn chỉnh vào Portfolio của mình.

---

## 1. Dự án: DevBlog (Blog cá nhân tối ưu hóa cực đỉnh)

**Mục tiêu:** Áp dụng SEO, MDX (Markdown) và Static Site Generation (SSG) để tạo một blog tải nhanh như chớp.

**Kiến trúc đề xuất:**
- **Routing:** `/blog`, `/blog/[slug]`.
- **Data Fetching:** Đọc các file `.md` từ thư mục local trong quá trình build (sử dụng thư viện `gray-matter` và `next-mdx-remote`). Dữ liệu này tĩnh 100%.
- **Tối ưu hóa:** 
  - Sử dụng `<Image>` tối ưu ảnh bìa (Thumbnail) các bài viết.
  - Sử dụng `generateMetadata` linh động sinh thẻ `<meta>` dựa vào tên bài viết.
  - Sinh file `sitemap.ts` tự động.
- **Styling:** Tailwind CSS kết hợp với plugin `@tailwindcss/typography` (`prose`) để format các thẻ HTML sinh ra từ Markdown một cách đẹp mắt nhất.

---

## 2. Dự án: TaskFlow (Ứng dụng quản lý công việc SaaS)

**Mục tiêu:** Xây dựng ứng dụng dạng Dashboard với tương tác dày đặc, Caching phức tạp và Database thực.

**Kiến trúc đề xuất:**
- **Authentication:** Tích hợp Auth.js v5 (Đăng nhập bằng Google GitHub). Bảo vệ toàn bộ Route `/dashboard/...` qua Middleware.
- **Database:** PostgreSQL kết nối qua ORM Prisma hoặc Drizzle.
- **Routing nâng cao:**
  - `(dashboard)/layout.tsx`: Giao diện Sidebar Sidebar điều hướng, không bị giật khi chuyển trang.
  - `@modal/(..)task/[id]/page.tsx`: Ứng dụng **Intercepting & Parallel Routes**. Bấm vào 1 task sẽ hiện lên Popup chi tiết Task mà URL đổi thành `/task/123`, hệt như Trello!
- **Data Mutations:** Toàn bộ thao tác Thêm/Sửa/Xóa Task dùng **Server Actions** (`'use server'`). Gắn kèm hàm `revalidatePath('/dashboard')` để giao diện cập nhật ngay lập tức mà không cần tạo state phức tạp. Dùng `useOptimistic` để tạo cảm giác thao tác tức thời.

---

## 3. Dự án: NextCommerce (E-commerce cơ bản)

**Mục tiêu:** Dự án thử thách kỹ năng Full-stack nặng đô nhất. Xử lý logic giỏ hàng (Cart) và thanh toán (Payment).

**Kiến trúc đề xuất:**
- **Product Display:** Sử dụng ISR (Incremental Static Regeneration) cho các trang danh mục `/category/[slug]`. Lấy dữ liệu siêu tốc nhưng vẫn cập nhật khi có hàng mới.
- **State Management (Giỏ hàng):** Vì giỏ hàng cần truy cập liên tục, lưu trữ nó ở **Zustand** (Global State trên Client) kết hợp lưu localStorage để không bị mất khi F5.
- **Backend API (`route.ts`):** 
  - Tạo một Webhook endpoint: `/api/stripe-webhook` để nhận thông báo thanh toán thành công từ cổng thanh toán Stripe.
- **Error Handling & Loading:** Phủ kín các trang bằng các file `loading.tsx` (Skeleton của sản phẩm) và `error.tsx` (Trường hợp API mất kết nối).

---
**🏆 Lời kết:**

Chúc mừng bạn đã hoàn thành trọn bộ 11 chương bí kíp Next.js App Router chuẩn đi làm. Bất cứ khi nào quên cú pháp, quên tư duy kiến trúc, hãy quay lại thư mục `next_react_js` này để tra cứu. 

Sự khác biệt giữa một Junior và Senior đôi khi không nằm ở số lượng thư viện họ biết, mà nằm ở chỗ họ biết cách tổ chức CodeBase mở rộng được, bảo mật tốt, bảo trì dễ dàng. **Bây giờ, hãy chọn một dự án, gõ `npx create-next-app` và bắt đầu thôi!**
