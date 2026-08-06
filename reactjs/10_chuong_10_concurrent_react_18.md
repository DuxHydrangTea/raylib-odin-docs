# Chương 10: Sức mạnh của Concurrent React 18 

Trước React 18, quá trình Render là một khối (block) đồng bộ và không thể bị ngắt ngang. Nếu bạn gõ phím vào một input và React phải mất 2 giây để tính toán (ví dụ: filter một danh sách khổng lồ), toàn bộ trình duyệt sẽ bị "đơ" trong 2 giây đó. Người dùng không thể click, không thể cuộn trang.

**React 18 Concurrent Mode** ra đời để giải quyết vấn đề này. Nó cho phép React có thể **ngắt ngang** việc render những thứ kém quan trọng (danh sách) để ưu tiên render những thứ quan trọng ngay lập tức (phím gõ của người dùng).

---

## 1. `useTransition`: Chuyển đổi trạng thái mượt mà

Ví dụ bạn có một nút "Chuyển sang Tab Thống Kê". Tab Thống Kê phải render hàng ngàn điểm dữ liệu, mất khoảng 1 giây.
Nếu dùng `useState` bình thường, khi bấm nút, nút sẽ bị đơ trong 1 giây, trông như ứng dụng bị treo.

Với `useTransition`, bạn có thể "đánh dấu" việc chuyển tab là một tác vụ có mức độ ưu tiên thấp (low-priority).

```tsx
import { useState, useTransition } from 'react';

function TabContainer() {
  const [isPending, startTransition] = useTransition();
  const [tab, setTab] = useState('about');

  function selectTab(nextTab) {
    // startTransition báo cho React biết việc setTab này 
    // không cần gấp, có thể thực hiện từ từ ở background.
    startTransition(() => {
      setTab(nextTab);
    });
  }

  return (
    <div>
      <div className="flex gap-4">
        <button onClick={() => selectTab('about')}>Về chúng tôi</button>
        <button onClick={() => selectTab('stats')}>Thống kê nặng</button>
      </div>

      {/* Hiển thị thanh loading mờ mờ thay vì treo cứng giao diện */}
      {isPending && <div className="spinner">Đang chuẩn bị dữ liệu...</div>}
      
      <div style={{ opacity: isPending ? 0.5 : 1 }}>
        {tab === 'about' ? <AboutTab /> : <HeavyStatsTab />}
      </div>
    </div>
  );
}
```

---

## 2. `useDeferredValue`: Trì hoãn việc render giá trị

Nếu `useTransition` bọc xung quanh một LỆNH thay đổi state (`setState`), thì `useDeferredValue` bọc xung quanh một GIÁ TRỊ (Value).

Trường hợp sử dụng phổ biến nhất là **Ô Tìm Kiếm (Search Input)**.
Khi bạn gõ "A", bạn muốn input hiện chữ "A" ngay lập tức (Ưu tiên cao). Việc lọc danh sách hàng nghìn sản phẩm bắt đầu bằng chữ "A" có thể làm sau (Ưu tiên thấp).

```tsx
import { useState, useDeferredValue, useMemo } from 'react';

function SearchPage({ products }) {
  const [query, setQuery] = useState('');
  
  // React sẽ cố gắng giữ giá trị deferredQuery ở phiên bản cũ 
  // cho đến khi nó rảnh rỗi mới cập nhật lên bằng với query hiện tại.
  const deferredQuery = useDeferredValue(query);

  // Danh sách chỉ tính toán lại khi deferredQuery thay đổi (lúc rảnh)
  const filteredProducts = useMemo(() => {
    return products.filter(p => p.name.includes(deferredQuery));
  }, [products, deferredQuery]);

  // Cờ báo hiệu giao diện danh sách đang bị "cũ" (chưa update kịp với input)
  const isStale = query !== deferredQuery;

  return (
    <div>
      {/* Input luôn mượt mà vì nó phản hồi ngay theo state 'query' */}
      <input 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
        placeholder="Tìm kiếm..."
      />

      <div style={{ opacity: isStale ? 0.5 : 1 }}>
        <ul>
          {filteredProducts.map(p => <li key={p.id}>{p.name}</li>)}
        </ul>
      </div>
    </div>
  );
}
```

---

## 3. Khi nào Dùng gì? Debounce vs Concurrent Features

Nhiều lập trình viên lâu năm thắc mắc: *"Tính năng này có khác gì việc dùng `setTimeout` (Debounce/Throttle) để trì hoãn việc search đâu?"*

Sự khác biệt là **khổng lồ**:
- **Debounce:** Luôn bắt bạn đợi 1 khoảng thời gian cố định (vd: 500ms). Dù máy tính người dùng mạnh đến đâu, họ vẫn phải đợi 500ms danh sách mới được lọc.
- **Concurrent React:** Không có thời gian chờ cố định. Nó sẽ bắt đầu việc lọc ngay lập tức ở background. Nếu máy của user xịn, họ thấy kết quả ngay lập tức (0ms). Nếu máy user yếu, nó sẽ tốn thời gian hơn, nhưng quan trọng nhất là **bàn phím gõ vẫn không bị khựng**.

### Tóm tắt Actionable
1. Đừng bỏ quên Debounce hoàn toàn. Nếu bạn cần hạn chế số lần **GỌI API LÊN SERVER**, hãy dùng **Debounce**.
2. Nếu bạn đang xử lý và lọc dữ liệu **Ở PHÍA CLIENT (Trình duyệt)**, hãy dùng **`useDeferredValue`** hoặc **`useTransition`**.
3. Cập nhật React lên v18 và gọi `createRoot()` (thay vì `ReactDOM.render()`) để tự động được hưởng lợi ích Batching State của Concurrent Mode.
