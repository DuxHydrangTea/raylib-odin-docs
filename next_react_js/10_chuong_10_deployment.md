# Chương 10: Triển khai (Deployment) - Đưa sản phẩm ra Thế Giới

Đã làm xong dự án chuẩn Enterprise thì phải biết cách Deploy chuẩn. Với Next.js, có hai trường phái chính: **Triển khai lên Vercel (PaaS - Dễ nhất, Tối ưu nhất)** và **Triển khai bằng Docker lên VPS tự quản lý (Kinh tế, Bảo mật cục bộ)**.

---

## 1. Triển khai siêu tốc lên Vercel (Mặc định)

Vercel là công ty tạo ra Next.js. Deploy lên Vercel giống như "đo ni đóng giày" cho Next.js, hệ thống tự động phân bổ Serverless Functions cho các Route Handlers, phân bổ tĩnh trên CDN toàn cầu (Edge Network) cho các file SSG/Tĩnh.

### Các bước thực hiện:
1. Đẩy code của bạn lên GitHub/GitLab.
2. Đăng nhập vào [Vercel.com](https://vercel.com/) bằng tài khoản GitHub.
3. Bấm **"Add New Project"**, chọn kho lưu trữ (repository) của bạn.
4. Ở phần Environment Variables, điền các biến cấu hình (VD: `DATABASE_URL`, `NEXTAUTH_SECRET`).
5. Bấm **Deploy**. Chờ 2 phút. Xong!

**Ưu điểm:** CI/CD tự động toàn bộ. Mỗi lần bạn `git push` nhánh main, Vercel tự build và deploy. Tốc độ trang web siêu nhanh nhờ hạ tầng CDN toàn cầu.

---

## 2. Triển khai bằng Docker (Doanh nghiệp tự host - Tối quan trọng)

Rất nhiều công ty lớn không muốn mã nguồn và dữ liệu rời khỏi máy chủ nội bộ (On-premise) hoặc AWS/Google Cloud riêng của họ. Khi đó, bạn phải biết build Next.js thành một **Docker Container**.

### Bước 1: Bật chế độ Standalone
Mặc định Next.js build ra rất nhiều file phụ thuộc vào `node_modules` khổng lồ. Để build Docker nhẹ nhất, ta bảo Next.js chỉ gói gọn đúng những gì nó cần chạy.

Mở file `next.config.mjs` và thêm dòng này:
```js
const nextConfig = {
  output: 'standalone', // <--- CỰC KỲ QUAN TRỌNG
};
export default nextConfig;
```

### Bước 2: Viết file `Dockerfile` chuẩn Next.js
Tạo file tên `Dockerfile` (không có đuôi) ở thư mục gốc:

```dockerfile
# Sử dụng base image Node.js nhẹ nhất
FROM node:18-alpine AS base

# 1. Khôi phục packages (Install dependencies)
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# 2. Build ứng dụng
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Tạo biến môi trường tại thời điểm build nếu cần (Next.js đôi khi cần lúc build)
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# 3. Môi trường Production (Chạy server)
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

# Bỏ quyền root để bảo mật
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy thư mục public (tài nguyên tĩnh)
COPY --from=builder /app/public ./public

# Copy thư mục standalone đã được tối ưu siêu nhẹ
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
# Khởi chạy ứng dụng (server.js sinh ra từ chế độ standalone)
CMD ["node", "server.js"]
```

### Bước 3: Build và Chạy trên VPS (Sử dụng PM2 hệ Docker)

Ở máy chủ, bạn clone code về và chạy:
```bash
# Build thành image (tốn vài phút)
docker build -t my-next-app .

# Chạy app ở cổng 80 (mapping vào 3000 của docker), tự động restart khi crash
docker run -d -p 80:3000 --name next-production-app --restart always my-next-app
```

### Lưu ý cho người đi làm về CI/CD
Trong thực tế, bạn sẽ kết hợp viết **GitHub Actions** hoặc **GitLab CI**. Khi có commit mới, hệ thống CI tự động chạy lệnh docker build, sau đó dùng lệnh ssh để login vào VPS của công ty, stop container cũ và khởi động container mới.

**Tóm tắt:** Bạn đã là một chuyên gia. Bạn không chỉ viết code giao diện đẹp, gọi API mượt, bảo mật tốt mà còn biết cách tự tay đóng gói toàn bộ server của mình bằng Docker để deploy lên bất kỳ hạ tầng nào thế giới yêu cầu. 
Hãy tiến tới Chương 11 để nhận ý tưởng các dự án cuối khóa!
