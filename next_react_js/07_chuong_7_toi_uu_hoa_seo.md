# Chương 7: Tối ưu hóa (Optimizations) & SEO - Bí quyết đạt 100 điểm Lighthouse

Một dự án đi làm thực tế không chỉ cần tính năng chạy đúng, mà còn phải chạy **nhanh** và **chuẩn SEO** để Marketing có thể quảng cáo được. Next.js cung cấp các công cụ tích hợp sẵn để tối ưu hóa hoàn toàn tự động.

---

## 1. Tối ưu Hình ảnh (Image Optimization)

Thẻ `<img>` truyền thống load ảnh với kích thước gốc (ví dụ ảnh 5MB), làm giảm trầm trọng tốc độ tải trang (chỉ số LCP - Largest Contentful Paint).

Thẻ `<Image>` của Next.js tự động:
- Chuyển đổi định dạng sang WebP hoặc AVIF (nhẹ hơn 30-50% so với JPEG/PNG).
- Tự động thay đổi kích thước ảnh (resize) dựa trên thiết bị (mobile, tablet, desktop).
- Tự động Lazy load (chỉ tải ảnh khi người dùng cuộn tới).

**Cách sử dụng chuẩn:**
```tsx
import Image from 'next/image';
import heroImg from '@/public/images/hero.jpg'; // Import trực tiếp ảnh local (Next.js tự tính toán width/height)

export default function HeroSection() {
  return (
    <div className="relative w-full h-[500px]">
      {/* 
        priority: Đặt ở banner đầu trang để tải NGAY LẬP TỨC (tối ưu LCP) 
        placeholder="blur": Hiển thị ảnh mờ trong lúc tải
      */}
      <Image 
        src={heroImg} 
        alt="Banner Quảng Cáo" 
        priority 
        placeholder="blur" 
        style={{ objectFit: 'cover' }} 
      />

      {/* Với ảnh lấy từ API (External URL), bạn BẮT BUỘC phải truyền width và height,
          Đồng thời cấu hình URL trong next.config.mjs */}
      <Image 
        src="https://s3.amazonaws.com/my-bucket/product-1.jpg" 
        alt="Sản phẩm"
        width={400} 
        height={300} 
      />
    </div>
  );
}
```

*Cấu hình file `next.config.mjs` cho ảnh ngoại (External Images):*
```js
const nextConfig = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 's3.amazonaws.com' }, // Cho phép load ảnh từ domain này
    ],
  },
};
export default nextConfig;
```

---

## 2. Tối ưu Font chữ (next/font)

Custom font (Google Fonts) thường gây ra lỗi **Cumulative Layout Shift (CLS)** (chữ bị giật/nhảy layout khi font tải xong). `next/font` sẽ tự tải font về server lúc build và nhúng thẳng vào HTML, xóa bỏ hoàn toàn CLS và không tốn thêm request mạng nào.

**Vị trí:** `app/layout.tsx`

```tsx
import { Inter, Roboto_Mono } from 'next/font/google';

const inter = Inter({ subsets: ['latin', 'vietnamese'], variable: '--font-inter' });
const roboto = Roboto_Mono({ subsets: ['latin'], variable: '--font-roboto' });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi" className={`${inter.variable} ${roboto.variable}`}>
      <body className="font-sans"> {/* Sử dụng CSS biến --font-inter được cấu hình trong tailwind */}
        {children}
      </body>
    </html>
  );
}
```

---

## 3. SEO chuyên nghiệp: Metadata API

Next.js App Router bỏ qua `<Head>` cũ và sử dụng API Metadata mạnh mẽ hơn nhiều.

### Static Metadata (Trang cố định)
**Vị trí:** `app/about/page.tsx`

```tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Về chúng tôi | Công ty ABC',
  description: 'Công ty công nghệ hàng đầu với 10 năm kinh nghiệm.',
  openGraph: {
    images: ['/og-image-about.jpg'], // Ảnh hiện khi share Facebook/Zalo
  },
};
```

### Dynamic Metadata (Trang thay đổi theo ID/Slug)
Đặc biệt quan trọng cho các trang Chi tiết sản phẩm/Bài viết. Next.js tự động loại bỏ các request API trùng lặp giữa hàm sinh Metadata và Component!

**Vị trí:** `app/products/[id]/page.tsx`

```tsx
import type { Metadata } from 'next';
import { getProductById } from '@/lib/api';

// Hàm generateMetadata sẽ chạy trước để sinh các thẻ <meta>
export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const product = await getProductById(params.id);
  
  if (!product) {
    return { title: 'Không tìm thấy sản phẩm' };
  }

  return {
    title: `${product.name} | Cửa hàng ABC`,
    description: product.summary,
    openGraph: {
      images: [product.imageUrl],
    },
  };
}

export default async function ProductPage({ params }: { params: { id: string } }) {
  // LƯU Ý: Lời gọi hàm này KHÔNG làm tăng số lượng request đến DB!
  // Next.js tự động cache (deduplicate) request getProductById() nếu nó giống ở generateMetadata
  const product = await getProductById(params.id); 
  
  return <div>{/* Nội dung sản phẩm */}</div>;
}
```

## 4. Tự động hóa Sitemap & Robots.txt

Bạn không cần viết file tĩnh nữa. Next.js hỗ trợ file `.ts` để sinh tự động.

**Vị trí:** `app/sitemap.ts`

```ts
import { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  // Thực tế: Lấy tất cả bài viết từ DB
  const posts = await getAllPosts(); 
  
  const postEntries = posts.map((post) => ({
    url: `https://my-domain.com/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }));

  return [
    {
      url: 'https://my-domain.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    ...postEntries,
  ];
}
```
Vào `https://localhost:3000/sitemap.xml`, bạn sẽ thấy một XML sitemap hoàn chỉnh cho Google Bot!
