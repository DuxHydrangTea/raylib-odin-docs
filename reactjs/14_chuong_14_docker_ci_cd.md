# Chương 14: Đóng gói và Triển khai (Docker, Nginx & CI/CD)

Code chạy ngon trên máy của bạn (localhost) không có nghĩa là nó sẽ chạy được trên Server Production. Các dự án Enterprise hiện đại luôn sử dụng cấu trúc Container hóa (Docker) và quy trình tự động CI/CD để đảm bảo tính nhất quán.

---

## 1. Bản chất của việc Deploy React App (Vite/CRA)

Khác với NodeJS backend, một dự án React thuần (không xài Next.js SSR) bản chất chỉ là **HTML, CSS và JavaScript Tĩnh (Static Files)**.
Bạn không cần Node.js để chạy React App trên Production. Bạn chỉ cần Node.js để **build** (biên dịch) code, sau đó lấy thư mục `dist` đẩy lên một Web Server nhẹ (như **Nginx**) để phục vụ người dùng tải về.

---

## 2. Dockerize React App (Multi-stage Build)

Sử dụng Docker Multi-stage giúp giữ cho dung lượng Image Production siêu nhỏ (chỉ vài chục MB thay vì hàng GB của NodeJS).

Tạo file `Dockerfile` ở thư mục gốc của dự án:

```dockerfile
# ==========================================
# GIAI ĐOẠN 1: BUILD (Sử dụng Node.js)
# ==========================================
FROM node:20-alpine AS builder

# Tạo thư mục làm việc
WORKDIR /app

# Copy package.json và cài đặt dependencies trước (Tận dụng Docker Cache)
COPY package.json package-lock.json ./
RUN npm ci

# Copy toàn bộ code và tiến hành build
COPY . .
RUN npm run build

# ==========================================
# GIAI ĐOẠN 2: PRODUCTION (Sử dụng Nginx)
# ==========================================
FROM nginx:alpine AS runner

# Xóa trang web mặc định của Nginx
RUN rm -rf /usr/share/nginx/html/*

# Copy thư mục build (thường là 'dist' của Vite, hoặc 'build' của CRA) từ Giai đoạn 1 sang
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy file cấu hình Nginx tùy chỉnh (Giải quyết lỗi React Router - 404 Not Found)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose cổng 80
EXPOSE 80

# Chạy Nginx ở chế độ background
CMD ["nginx", "-g", "daemon off;"]
```

---

## 3. Cấu hình Nginx chống lỗi 404 cho React Router

Khi bạn dùng React Router, người dùng truy cập `domain.com/dashboard`, Nginx sẽ cố tìm thư mục `dashboard/index.html` trong ổ cứng và báo lỗi 404. Giải pháp là bảo Nginx hãy trỏ mọi đường dẫn về `index.html` để React Router tự xử lý.

Tạo file `nginx.conf` ở thư mục gốc:

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Nén Gzip để thu nhỏ file JS, CSS tải nhanh hơn
    gzip on;
    gzip_types text/css application/javascript application/json image/svg+xml;
    gzip_comp_level 6;
    gzip_min_length 1000;

    location / {
        # ĐÂY LÀ DÒNG QUAN TRỌNG NHẤT: Trỏ mọi thứ về index.html
        try_files $uri $uri/ /index.html;
    }

    # Đảm bảo các file static (JS, CSS, Ảnh) được cache 1 năm ở trình duyệt
    location ~* \.(?:ico|css|js|gif|jpe?g|png|woff2?|eot|ttf|svg)$ {
        expires 1y;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }
}
```

---

## 4. Tự động hóa với CI/CD (GitHub Actions)

Mỗi lần gõ code xong lại phải tự gõ lệnh Docker build rồi tự đẩy lên server thì rất mất thời gian. **CI/CD** giúp tự động hóa quá trình này.

Tạo file `.github/workflows/deploy.yml`:

```yaml
name: Deploy React App

# Pipeline này sẽ chạy mỗi khi bạn PUSH code lên nhánh 'main'
on:
  push:
    branches: [ "main" ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Lấy code từ repo
        uses: actions/checkout@v4

      - name: Cài đặt Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Cài đặt Dependencies
        run: npm ci

      - name: Chạy kiểm tra Code (Linter & Type Check)
        run: |
          npm run lint
          npm run typecheck

      - name: Chạy Unit Tests
        run: npm run test

      # Tùy chọn: Build Docker Image và Push lên Docker Hub (Nếu dùng Docker)
      - name: Build Docker Image
        run: docker build -t my-react-app:latest .

  # Giai đoạn Deploy (Chỉ chạy nếu giai đoạn trên thành công)
  deploy:
    needs: build-and-test
    runs-on: ubuntu-latest
    steps:
      - name: SSH vào Server Production và cập nhật Code
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.SERVER_IP }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /var/www/my-react-app
            git pull origin main
            docker-compose up -d --build
```

---

## 5. Lời Kết Giáo Trình
Chúc mừng bạn đã hoàn thành giáo trình **ReactJS dành cho người đi làm**. Bạn đã đi từ những kiến trúc cơ bản (Feature Sliced Design), kiểm soát State (Zustand, React Query), tối ưu hóa hiệu năng, đến bảo vệ ứng dụng (Security) và triển khai tự động (Docker, CI/CD). 

Giờ đây, bạn hoàn toàn có thể tự tin tham gia hoặc thiết lập nền móng cho bất kỳ dự án Enterprise Frontend nào!
