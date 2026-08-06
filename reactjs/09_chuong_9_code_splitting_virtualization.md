# Chương 9: Xử Lý Lượng Dữ Liệu Khổng Lồ (Code Splitting & Virtualization)

Khi ứng dụng của bạn scale lên, có hai vấn đề lớn về dung lượng và hiển thị:
1. **Dung lượng gói JavaScript (Bundle Size) quá lớn**, người dùng phải đợi hàng chục giây mới tải xong trang web.
2. **DOM Nodes (Thẻ HTML) quá nhiều**, trình duyệt bị "treo" khi cố gắng hiển thị 10,000 dòng dữ liệu trên màn hình cùng lúc.

Chương này sẽ hướng dẫn bạn giải quyết triệt để 2 vấn đề trên.

---

## 1. Code Splitting & Lazy Loading (Chia nhỏ file JS)

Mặc định, các bundler như Webpack/Vite sẽ gộp (bundle) tất cả các file React của bạn vào một file khổng lồ tên là `main.js`. Điều này khiến trang Login ban đầu tải cực chậm, dù người dùng chưa hề đăng nhập vào Dashboard.

**Giải pháp:** Chỉ tải file JavaScript của Dashboard **KHI VÀ CHỈ KHI** người dùng truy cập vào nó.

### Cách 1: Dùng hàm `lazy()` của React Router v6 (Khuyên dùng)
Như đã học ở Chương 6, React Router v6.4+ hỗ trợ Lazy Loading nguyên bản trên cấp độ Route.

```tsx
// src/app/router/index.tsx
import { createBrowserRouter } from 'react-router-dom';

export const router = createBrowserRouter([
  {
    path: '/',
    // Component Home đã được import tĩnh, luôn có sẵn
    element: <Home />, 
  },
  {
    path: 'dashboard',
    // Chỉ khi click vào /dashboard, trình duyệt mới tải file Dashboard.tsx về
    lazy: () => import('@/pages/Dashboard')
  }
]);
```

### Cách 2: Dùng `React.lazy()` và `<Suspense>` (Cho Component con)
Nếu bạn có một Component rất nặng (ví dụ: một thư viện Vẽ Đồ Thị Chart.js) nằm TRONG một trang, bạn không muốn tải nó ngay lúc đầu.

```tsx
import React, { Suspense, useState } from 'react';

// Dùng React.lazy để import động
const HeavyChart = React.lazy(() => import('@/components/HeavyChart'));

export function Dashboard() {
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <button onClick={() => setShowChart(true)}>Hiển thị Biểu đồ</button>

      {/* Phải bọc trong Suspense để hiển thị Loading trong lúc tải file JS của HeavyChart */}
      {showChart && (
        <Suspense fallback={<div>Đang tải biểu đồ...</div>}>
          <HeavyChart />
        </Suspense>
      )}
    </div>
  );
}
```

---

## 2. Virtualization (Ảo hóa danh sách)

Trình duyệt xử lý logic JavaScript rất nhanh, nhưng việc vẽ các thẻ HTML (DOM Rendering) lại rất chậm. Nếu bạn map() một mảng 10,000 dòng `<tr>` ra Table, trình duyệt sẽ sập.

**Giải pháp (Virtualization):** Chỉ vẽ đúng những dòng ĐANG HIỂN THỊ TRÊN MÀN HÌNH (Ví dụ màn hình chỉ hiển thị được 20 dòng). Khi người dùng cuộn (scroll), ta tái sử dụng lại các thẻ HTML cũ và thay thế dữ liệu mới vào. Bằng cách này, dù có 10,000 dữ liệu, DOM cũng chỉ có vỏn vẹn 20 thẻ HTML.

### Thư viện khuyên dùng: `@tanstack/react-virtual` hoặc `react-virtuoso`
Đây là giải pháp hiện đại thay thế cho thư viện cũ kỹ `react-window` / `react-virtualized`.

**Ví dụ với `@tanstack/react-virtual`:**

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';
import { useRef } from 'react';

function VirtualizedList({ items }) {
  // Ref gắn vào thẻ bọc ngoài (chứa thanh scroll)
  const parentRef = useRef<HTMLDivElement>(null);

  // Cấu hình máy ảo (virtualizer)
  const rowVirtualizer = useVirtualizer({
    count: items.length, // Tổng số phần tử: 10,000
    getScrollElement: () => parentRef.current, // Vị trí thanh cuộn
    estimateSize: () => 50, // Chiều cao ước tính của 1 dòng: 50px
  });

  return (
    // Khung nhìn cố định chiều cao, có thanh cuộn (overflow-auto)
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      
      {/* Khung chứa tổng có chiều cao bằng: tổng số phần tử x chiều cao 1 phần tử */}
      <div style={{ height: `${rowVirtualizer.getTotalSize()}px`, position: 'relative' }}>
        
        {/* Chỉ lấy các phần tử ĐANG HIỂN THỊ để render */}
        {rowVirtualizer.getVirtualItems().map((virtualItem) => (
          
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualItem.size}px`, // Chiều cao thực tế
              // Dịch chuyển phần tử (TranslateY) xuống đúng vị trí cuộn
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            {/* Nội dung thực sự của 1 dòng */}
            Dòng số {virtualItem.index}: {items[virtualItem.index].name}
          </div>

        ))}
      </div>
    </div>
  );
}
```
Khi chạy đoạn code trên, nếu bạn inspect (F12), bạn sẽ thấy số lượng thẻ `<div>` bên trong luôn cố định ở con số 15-20 thẻ dù mảng dữ liệu có lên tới 1 triệu phần tử.

---

## Tóm tắt Actionable

1. **Lazy Loading theo Route:** Luôn bật tính năng Lazy Loading cho các Route phụ (vd: Trang Setting, Profile) để làm giảm file `main.js` tải lần đầu, giúp đạt điểm xanh Google PageSpeed.
2. Đừng lạm dụng `React.lazy()` cho mọi Component con. Nó có "độ trễ" (network delay). Chỉ dùng cho Component rất nặng hoặc ít khi user bấm vào.
3. Khi nhận API có trả về hơn **200 phần tử**, hãy nghĩ ngay đến giải pháp **Pagination (Phân trang)** (Ở phía Backend), hoặc **Virtualization** (Nếu bắt buộc phải Scroll liên tục ở phía Frontend). Tuyệt đối không dùng `.map()` thẳng.
