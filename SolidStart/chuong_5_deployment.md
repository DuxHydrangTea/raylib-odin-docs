# Chương 5: Triển khai (Deployment) với SolidStart

Xây dựng xong ứng dụng chỉ là một nửa chặng đường. Bạn cần đưa nó lên không gian mạng (Internet) để mọi người có thể sử dụng. SolidStart sử dụng công nghệ nội bộ mang tên **Vinxi** và **Nitro**, giúp nó có thể biên dịch ra code chạy trên vô số nền tảng khác nhau: từ Node.js server truyền thống, cho đến Vercel, Netlify, Cloudflare Workers, Deno, hay Bun.

## 1. Cơ chế Adapter

Để deploy lên một môi trường cụ thể, SolidStart sử dụng thứ gọi là "Adapter" (Bộ chuyển đổi). Mặc định, nếu bạn không cài gì cả, nó sẽ build ra một Node.js server.

### Build và chạy trên Node.js (Mặc định)

1. Mở Terminal và chạy lệnh build:
```bash
npm run build
```
Lệnh này sẽ tạo ra thư mục `.output`. Trong đó chứa code đã được nén và tối ưu hoá.

2. Khởi chạy Server Production:
```bash
npm run start
```
Lúc này ứng dụng của bạn sẽ chạy cực kỳ mượt mà trên môi trường Production (Không còn hot-reload hay các công cụ debug làm chậm máy).

## 2. Deploy lên Vercel

Vercel là một trong những nền tảng Host cực kỳ tuyệt vời cho các ứng dụng Serverless và Edge Functions.

**Bước 1: Cài đặt Vercel Preset**

Mở file `app.config.ts` (hoặc `vite.config.ts` tuỳ phiên bản) ở thư mục gốc của dự án. 
Thêm thuộc tính `preset` vào plugin `solid`.

```ts
import { defineConfig } from "@solidjs/start/config";

export default defineConfig({
  server: {
    // Chỉ định preset Vercel để Nitro biết cách tối ưu code cho nền tảng này
    preset: "vercel" 
  }
});
```

**Bước 2: Push code lên GitHub**

1. Tạo một Repository trên GitHub.
2. Push source code SolidStart của bạn lên đó.

**Bước 3: Deploy trên Vercel Dashboard**

1. Đăng nhập vào [Vercel.com](https://vercel.com).
2. Chọn "Add New Project" và import cái GitHub Repo bạn vừa tạo.
3. Vercel sẽ tự động nhận diện đây là dự án SolidStart. (Các lệnh như `npm run build` đã được điền sẵn).
4. Bấm "Deploy" và chờ vài chục giây.

Boom! Bạn đã có một trang web SolidStart xịn xò chạy với tốc độ tên lửa, hỗ trợ SSR, API Routes đầy đủ.

## 3. Deploy lên Cloudflare Pages

Cloudflare nổi tiếng với mạng lưới CDN toàn cầu, chạy app siêu nhanh ngay gần vị trí của người dùng cuối (Edge Computing).

**Bước 1: Sửa config sang Cloudflare**

```ts
import { defineConfig } from "@solidjs/start/config";

export default defineConfig({
  server: {
    preset: "cloudflare-pages" 
  }
});
```

**Bước 2: Sử dụng Wrangler CLI**

Bạn cần có tài khoản Cloudflare và cài đặt `wrangler`.
```bash
npm i -g wrangler
npm run build
```

**Bước 3: Tải lên Cloudflare**
```bash
npx wrangler pages deploy .output/public
```

## Tổng kết SolidStart
Chúc mừng bạn đã hoàn thành bộ bí kíp SolidStart! Qua 5 chương, bạn đã biết:
1. Routing cực nhàn với File-Based Routing (Chương 1).
2. Tải dữ liệu an toàn trên Server để làm SEO (Chương 2).
3. Viết Form Submit với Server Actions xịn xò (Chương 3).
4. Tự viết API / Middleware (Chương 4).
5. Build và Deploy linh hoạt bằng Adapter (Chương 5).

Bạn đã chính thức làm chủ hệ sinh thái SolidJS rồi đấy! Chúc bạn xây dựng được những siêu phẩm công nghệ nhanh, nhẹ và mượt mà nhất.
