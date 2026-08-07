# Chương 7: Giới thiệu về SolidStart

SolidJS bản chất là một Client-side Framework (hoạt động chủ yếu trên trình duyệt của người dùng). Tuy nhiên, khi xây dựng các ứng dụng thực tế đòi hỏi SEO tốt (như Blog, Trang bán hàng) hoặc tốc độ tải trang cực nhanh, bạn cần đến **Server-Side Rendering (SSR)**.

Đó là lý do **SolidStart** ra đời. SolidStart là Meta-Framework chính thức của SolidJS (giống như Next.js của React hay Nuxt của Vue).

## 1. Khởi tạo dự án SolidStart

Để bắt đầu một dự án SolidStart, bạn sử dụng lệnh CLI sau (không cần phải cài đặt thủ công rườm rà):

```bash
npm create solid@latest
```
*Lưu ý: Đoạn mã trên là lệnh chạy trong Terminal, không phải mã JavaScript.*

CLI sẽ hỏi bạn muốn sử dụng template nào (Basic, Bare, Hacking) và ngôn ngữ (TypeScript hay JavaScript). 

## 2. File-Based Routing (Định tuyến dựa trên thư mục)

Khác với Solid Router (nơi bạn khai báo `<Route path="..." component={...} />`), SolidStart sử dụng **File-Based Routing**. Nghĩa là cấu trúc thư mục của bạn sẽ quyết định đường dẫn URL.

Cấu trúc ví dụ trong thư mục `src/routes/`:
- `index.tsx` => Đường dẫn trang chủ `/`
- `about.tsx` => Đường dẫn `/about`
- `users/[id].tsx` => Đường dẫn động `/users/:id`

Ví dụ một file `src/routes/users/[id].tsx`:

```jsx
// src/routes/users/[id].jsx
import { useParams } from "@solidjs/router";
import { Title } from "@solidjs/meta";

export default function UserDetail() {
  const params = useParams();

  return (
    <main>
      {/* Thay đổi thẻ <title> trên trình duyệt dễ dàng với @solidjs/meta */}
      <Title>Hồ sơ của User {params.id}</Title>
      
      <h1>Trang chi tiết của người dùng: {params.id}</h1>
      <p>Nội dung này được tạo ra từ file-based routing của SolidStart.</p>
    </main>
  );
}
```

## 3. Chạy mã trên Server (Server Functions)

Trong SolidStart, bạn có thể viết một hàm thực thi trực tiếp trên Server (truy vấn Database, gọi API nội bộ, xử lý File) ngay bên trong file Frontend của bạn bằng từ khóa `"use server"`.

```jsx
// src/routes/index.jsx
import { createResource, Suspense } from "solid-js";

// Hàm này CHỈ CHẠY TRÊN SERVER. Không bao giờ lộ code xuống Client.
// Bạn có thể an toàn gọi Database ở đây.
const getSecretData = async () => {
  "use server";
  
  // Giả lập truy vấn DB tốn 1 giây
  await new Promise(r => setTimeout(r, 1000));
  
  return { secretMessage: "Đây là dữ liệu bí mật lấy từ Server" };
};

export default function Home() {
  // Lấy dữ liệu an toàn
  const [data] = createResource(getSecretData);

  return (
    <main>
      <h1>Trang chủ có SSR</h1>
      <Suspense fallback={<p>Đang tải dữ liệu từ máy chủ...</p>}>
        <p>Kết quả: {data()?.secretMessage}</p>
      </Suspense>
    </main>
  );
}
```
*Lưu ý: Khi người dùng truy cập trang, SolidStart sẽ chạy hàm `getSecretData` trên Node.js server, kết xuất ra HTML tĩnh kèm theo dữ liệu `secretMessage`, sau đó gửi HTML đã hoàn thiện xuống trình duyệt. Người dùng sẽ thấy nội dung ngay lập tức mà không cần chờ loading.*

## 4. Middleware & API Routes

Ngoài việc trả về giao diện HTML, SolidStart còn cho phép bạn tạo ra các API Endpoint (như REST API) bằng cách sử dụng thư mục `src/routes/api/`.

Ví dụ: Tạo file `src/routes/api/hello.js`:
```js
// API Endpoint đơn giản trả về JSON
export function GET() {
  return new Response(
    JSON.stringify({ message: "Xin chào từ API của SolidStart!" }), 
    {
      headers: { "Content-Type": "application/json" }
    }
  );
}
```
Bạn có thể gọi trực tiếp API này tại `http://localhost:3000/api/hello`.

## Tổng kết Chương 7
- **SolidStart** nâng tầm SolidJS lên mức độ production-ready với Server-Side Rendering.
- Tự động tạo Route dựa trên thư mục (`File-Based Routing`).
- **Server Functions (`"use server"`)** giúp trộn lẫn Backend logic vào Frontend một cách bảo mật và cực kỳ gọn gàng.
- Dễ dàng tạo API Endpoints bằng cách xuất các hàm `GET`, `POST`.
