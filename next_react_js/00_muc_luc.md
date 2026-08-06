# Lộ trình học Next.js từ Zero đến Hero (App Router)

Đây là lộ trình chi tiết để bạn có thể nắm vững Next.js từ những khái niệm cơ bản nhất cho đến khi xây dựng được các ứng dụng thực tế, chuyên nghiệp. Lộ trình này tập trung vào **App Router** (kiến trúc hiện đại và mặc định của Next.js).

---

## 📚 Phần 1: Nền tảng (Ôn tập React)
*Trước khi học Next.js, bạn cần có nền tảng vững chắc về React.*

- [ ] **Chương 1.1:** React Cơ bản & JSX (Components, Props)
- [ ] **Chương 1.2:** Quản lý State & Lifecycle (useState, useEffect)
- [ ] **Chương 1.3:** React Hooks chuyên sâu (useMemo, useCallback, useRef, useContext)
- [ ] **Chương 1.4:** Sự khác biệt giữa Client-Side Rendering (CSR) và Server-Side Rendering (SSR) cơ bản.

## 🚀 Phần 2: Bắt đầu với Next.js
*Hiểu Next.js là gì và cấu trúc của một dự án Next.js.*

- [ ] **Chương 2.1:** Next.js là gì? Tại sao nên dùng Next.js? (Các tính năng nổi bật)
- [ ] **Chương 2.2:** Khởi tạo dự án (`create-next-app`) và Cấu trúc thư mục chuẩn.
- [ ] **Chương 2.3:** Tổng quan về App Router vs Pages Router.

## 🗺️ Phần 3: Routing (Điều hướng)
*Trái tim của App Router trong Next.js.*

- [ ] **Chương 3.1:** Routing cơ bản (File-system based routing: `page.tsx`, `layout.tsx`).
- [ ] **Chương 3.2:** Điều hướng (Navigation) với `<Link>` và `useRouter`.
- [ ] **Chương 3.3:** Dynamic Routes (Route động: `[id]`, `[...slug]`).
- [ ] **Chương 3.4:** Xử lý trạng thái UI: Loading (`loading.tsx`), Error (`error.tsx`), Not Found (`not-found.tsx`).
- [ ] **Chương 3.5:** Route Groups (`(folder)`) và Parallel Routes (`@folder`), Intercepting Routes (`(..)folder`).

## ⚙️ Phần 4: Kiến trúc Rendering
*Hiểu rõ cách Next.js render trang là chìa khóa để tối ưu hiệu suất.*

- [ ] **Chương 4.1:** React Server Components (RSC) vs Client Components. Khi nào nên dùng loại nào?
- [ ] **Chương 4.2:** Các mô hình Rendering:
  - Static Rendering (SSG - Mặc định)
  - Dynamic Rendering (SSR)
- [ ] **Chương 4.3:** Edge và Node.js Runtimes.

## 💾 Phần 5: Data Fetching & Đột biến dữ liệu (Mutations)
*Cách lấy dữ liệu và tương tác với Database.*

- [ ] **Chương 5.1:** Lấy dữ liệu trên Server với `fetch()` (Server Components).
- [ ] **Chương 5.2:** Data Caching & Revalidating (Time-based, On-demand revalidation: `revalidatePath`, `revalidateTag`).
- [ ] **Chương 5.3:** Lấy dữ liệu trên Client (SWR, React Query).
- [ ] **Chương 5.4:** **Server Actions:** Xử lý Form và đột biến dữ liệu không cần API Route.
- [ ] **Chương 5.5:** Xử lý trạng thái Form (useFormStatus, useFormState).

## 🎨 Phần 6: Styling (Giao diện)
*Làm đẹp ứng dụng Next.js.*

- [ ] **Chương 6.1:** Global CSS và CSS Modules.
- [ ] **Chương 6.2:** Tích hợp Tailwind CSS (Cách cài đặt và cấu hình tối ưu).
- [ ] **Chương 6.3:** Sử dụng CSS-in-JS (Styled-components, Emotion) với App Router (Lưu ý về Server Components).

## ⚡ Phần 7: Tối ưu hóa (Optimizations) & SEO
*Làm cho ứng dụng chạy siêu nhanh và thân thiện với bộ máy tìm kiếm.*

- [ ] **Chương 7.1:** Tối ưu hóa Hình ảnh với `<Image>`.
- [ ] **Chương 7.2:** Tối ưu hóa Font chữ (`next/font`) và Scripts (`next/script`).
- [ ] **Chương 7.3:** Metadata API (Static và Dynamic Metadata cho SEO).
- [ ] **Chương 7.4:** Sitemap (`sitemap.ts`) và Robots (`robots.ts`).

## 🔌 Phần 8: Backend trong Next.js
*Biến Next.js thành một Full-stack framework.*

- [ ] **Chương 8.1:** Route Handlers (`route.ts` - Xây dựng REST/GraphQL APIs).
- [ ] **Chương 8.2:** Middleware: Xử lý request trước khi đến route (Authentication, Redirect, Rewrite).
- [ ] **Chương 8.3:** Kết nối cơ sở dữ liệu (Prisma, Drizzle ORM, Mongoose).

## 🔐 Phần 9: Authentication & Authorization (Xác thực & Phân quyền)
*Bảo mật ứng dụng của bạn.*

- [ ] **Chương 9.1:** Xác thực cơ bản với JWT/Cookies bằng Middleware & Route Handlers.
- [ ] **Chương 9.2:** Sử dụng NextAuth.js (Auth.js) cho OAuth (Google, GitHub) và Credentials.
- [ ] **Chương 9.3:** Phân quyền (Role-based Access Control - RBAC) bảo vệ trang và API.

## 🚀 Phần 10: Triển khai (Deployment)
*Đưa dự án của bạn lên Internet.*

- [ ] **Chương 10.1:** Triển khai siêu mượt lên Vercel.
- [ ] **Chương 10.2:** Đóng gói (Dockerizing) ứng dụng Next.js.
- [ ] **Chương 10.3:** Triển khai lên VPS truyền thống (AWS EC2, DigitalOcean) với Docker/PM2.

## 🛠️ Phần 11: Dự án thực hành (Capstone Projects)
*Thực hành để biến kiến thức thành kỹ năng.*

- [ ] **Dự án 1:** Blog cá nhân với Markdown/MDX (Tập trung: SSG, Routing, SEO).
- [ ] **Dự án 2:** Ứng dụng Quản lý công việc (Todo/Kanban) (Tập trung: Server Actions, Database, Authentication).
- [ ] **Dự án 3:** E-commerce cơ bản (Trang sản phẩm, Giỏ hàng, Tích hợp Stripe) (Tập trung: Full-stack, Caching, API).
