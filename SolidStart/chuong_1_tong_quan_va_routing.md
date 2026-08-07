# Chương 1: Tổng quan và Định tuyến (Routing)

Trong các dự án web quy mô lớn, việc tự cấu hình Webpack, Vite, SSR, hay API server tốn rất nhiều công sức. **SolidStart** là một framework cung cấp mọi thứ bạn cần "out of the box", giống như cách Next.js làm cho thế giới React.

## 1. Khởi tạo một dự án SolidStart

Để bắt đầu, mở Terminal và chạy lệnh:
```bash
npm create solid@latest
```
Hệ thống sẽ cung cấp một số tùy chọn template (khuyên dùng `Basic` + `TypeScript`). Sau đó, bạn chạy lệnh `npm install` và `npm run dev`. Trình duyệt sẽ mở ứng dụng SolidStart chạy trên cổng `3000`.

## 2. Cấu trúc Thư mục Chuẩn

Một dự án SolidStart điển hình có cấu trúc như sau:

```text
my-solid-app/
├── public/              # Chứa tài nguyên tĩnh (ảnh, favicon...)
├── src/
│   ├── components/      # Các component dùng chung (Nút bấm, Header...)
│   ├── routes/          # Thư mục cốt lõi của File-Based Routing
│   ├── entry-client.tsx # Điểm vào (entry) cho trình duyệt
│   ├── entry-server.tsx # Điểm vào cho Server (để SSR)
│   └── app.tsx          # Component Root chứa thẻ <html> và <Router>
├── vite.config.ts       # Cấu hình Vite & SolidStart plugins
└── package.json
```

## 3. File-Based Routing Cơ bản

Trong SolidStart, bạn **không cần** phải import các component vào file router trung tâm. Thay vào đó, bạn chỉ cần tạo file trong thư mục `src/routes`. Đường dẫn của file sẽ trở thành đường dẫn trên trình duyệt.

- `src/routes/index.tsx` => `http://localhost:3000/` (Trang chủ)
- `src/routes/about.tsx` => `http://localhost:3000/about` (Trang giới thiệu)
- `src/routes/blog/index.tsx` => `http://localhost:3000/blog`

```jsx
// src/routes/about.jsx
import { Title } from "@solidjs/meta";

export default function About() {
  return (
    <main>
      <Title>Về chúng tôi</Title>
      <h1>Công ty ABC</h1>
      <p>Chúng tôi chuyên làm về công nghệ.</p>
    </main>
  );
}
```
*Lưu ý: Bạn bắt buộc phải `export default` Component chính ở trong file route.*

## 4. Định tuyến động (Dynamic Routing)

Bạn có thể truyền các biến (như ID sản phẩm, tên người dùng) trực tiếp lên URL bằng cách đặt tên file trong cặp dấu ngoặc vuông `[ ]`.

- Cấu trúc: `src/routes/users/[id].tsx`
- URL hợp lệ: `/users/123`, `/users/john_doe`

Để lấy ra giá trị `id` này trong code, ta dùng hook `useParams`.

```jsx
// src/routes/users/[id].jsx
import { useParams } from "@solidjs/router";

export default function UserProfile() {
  const params = useParams();

  return (
    <div>
      {/* Tương ứng với tên file [id] */}
      <h2>Chào mừng bạn, người dùng số: {params.id}</h2>
    </div>
  );
}
```

## 5. Catch-all Routes (Bắt mọi đường dẫn)

Nếu bạn muốn một file duy nhất xử lý vô số đường dẫn (thường dùng cho trang lỗi 404 hoặc CMS), bạn có thể dùng cú pháp `[...tên_biến]`.

- Cấu trúc: `src/routes/[...404].tsx`
- URL hợp lệ: TẤT CẢ các URL nào chưa được định nghĩa trước đó.

```jsx
// src/routes/[...404].jsx
import { HttpStatusCode } from "@solidjs/start";

export default function NotFound() {
  return (
    <main>
      {/* Set mã lỗi 404 cho Server hiểu để làm SEO cho đúng */}
      <HttpStatusCode code={404} />
      <h1>Lỗi 404 - Không tìm thấy trang</h1>
      <p>URL bạn vừa truy cập không tồn tại.</p>
    </main>
  );
}
```

## Tổng kết Chương 1
- **SolidStart** loại bỏ việc cấu hình Router thủ công nhờ `File-Based Routing`.
- Thư mục `src/routes/` là "trái tim" của việc chuyển trang.
- Dùng `[id].tsx` cho tham số động và `[...404].tsx` để xử lý các trang không tồn tại.
