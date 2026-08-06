# Chương 8: Tối Ưu Hiệu Năng (React.memo, useMemo, useCallback)

"Tránh tối ưu hóa sớm" (Premature optimization is the root of all evil) là một câu nói nổi tiếng. Trong React, việc lạm dụng `React.memo`, `useMemo`, `useCallback` ở khắp mọi nơi thực chất làm ứng dụng của bạn **chậm đi** chứ không phải nhanh lên, vì bản thân việc ghi nhớ (memoization) cũng tốn chi phí CPU.

Chương này sẽ giúp bạn hiểu rõ khi nào cần, và khi nào **tuyệt đối không** nên tối ưu.

---

## 1. Vòng đời Re-render trong React

Theo mặc định, khi một component cha bị re-render (do State hoặc Props thay đổi), **toàn bộ các component con bên trong nó sẽ bị re-render theo**, bất kể props của component con có đổi hay không.

```tsx
function Parent() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>Tăng count: {count}</button>
      {/* ⚠️ Child này cũng sẽ render lại mỗi khi bấm nút Tăng, dù nó chả liên quan gì đến count */}
      <Child /> 
    </div>
  );
}

function Child() {
  console.log("Child bị render lại!");
  return <div>Component Con</div>;
}
```

### Cách giải quyết đơn giản nhất: Đẩy State xuống dưới (Push State Down) hoặc Kéo component lên trên (Lift Component Up)

Thay vì xài công cụ phức tạp, hãy tách phần có State ra riêng:

```tsx
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>Tăng count: {count}</button>;
}

function Parent() {
  return (
    <div>
      <Counter /> {/* Khi Counter render lại, Parent không bị ảnh hưởng */}
      <Child />   {/* Do đó Child không bị render lại! */}
    </div>
  );
}
```

---

## 2. Dùng `React.memo` (Cần cẩn thận)

`React.memo` là một HOC (Higher Order Component) giúp ghi nhớ một component. Nó sẽ so sánh nông (shallow compare) Props cũ và Props mới. Nếu giống hệt nhau, nó bỏ qua việc re-render.

```tsx
const HeavyChart = React.memo(function HeavyChart(props) {
  // Tốn 1 giây để render biểu đồ
  return <div>...</div>;
});
```

**KHI NÀO DÙNG?**
- Khi component đó render rất nặng (như SVG Chart, danh sách dài hàng trăm item).
- Khi nó thường xuyên bị re-render bởi cha với cùng một prop y hệt.

**KHI NÀO KHÔNG DÙNG?**
- Những component nhẹ (như Button, Text, Div).
- Khi component thường xuyên nhận props mới (Lúc này thuật toán so sánh props sẽ chạy vô ích và làm app chậm thêm).

---

## 3. Cặp bài trùng `useMemo` và `useCallback`

### `useMemo` (Nhớ dữ liệu)
Dùng để ghi nhớ kết quả của một phép tính toán nặng (vd: filter một mảng lớn).

```tsx
// ❌ Xấu: filter sẽ chạy lại mỗi lần render
const filteredUsers = users.filter(u => u.name.includes(search));

// ✅ Tốt: filter chỉ chạy lại khi mảng users HOẶC biến search thay đổi
const filteredUsers = useMemo(() => {
  return users.filter(u => u.name.includes(search));
}, [users, search]);
```
*Lưu ý: Không dùng `useMemo` cho các phép tính cơ bản (`a + b`, gán biến bình thường).*

### `useCallback` (Nhớ hàm số)
Mỗi lần React render, một hàm mới sẽ được tạo ra trong bộ nhớ.
`useCallback` giữ lại hàm cũ (không tạo mới) giữa các lần render, TRỪ KHI mảng dependency thay đổi.

**ĐỪNG DÙNG `useCallback` bừa bãi**. Bạn chỉ nên dùng nó trong 2 trường hợp:
1. Hàm đó được truyền xuống một component con đang xài `React.memo` (để tránh phá vỡ chức năng so sánh props của memo).
2. Hàm đó là một dependency (nằm trong mảng `[]`) của một `useEffect` khác.

```tsx
function Parent() {
  const [text, setText] = useState('');

  // ✅ Bắt buộc xài useCallback vì hàm onSubmit được truyền xuống HeavyForm (đang dùng React.memo)
  const handleSubmit = useCallback((data) => {
    api.post(data);
  }, []); // Hàm này không phụ thuộc gì nên mảng rỗng

  return (
    <div>
      <input value={text} onChange={e => setText(e.target.value)} />
      {/* Nếu không có useCallback ở trên, mỗi lần gõ input, hàm handleSubmit mới 
          sẽ được tạo ra -> HeavyForm bị ép render lại -> Mất tác dụng của React.memo */}
      <HeavyForm onSubmit={handleSubmit} />
    </div>
  );
}

const HeavyForm = React.memo(function HeavyForm({ onSubmit }) { ... });
```

---

## Tóm tắt Actionable

1. **Đừng tối ưu hóa sớm.** Viết code bình thường, đo đạc bằng **React DevTools Profiler**, thấy chỗ nào bị render nhiều mà lag thì mới thêm `memo`.
2. Hầu hết các vấn đề re-render có thể được giải quyết thông qua việc cấu trúc lại Component (tách Component con ra riêng) thay vì dùng `useMemo`/`useCallback`.
3. Chỉ bọc `useCallback` khi hàm đó làm Prop cho một Component dùng `React.memo`, hoặc nằm trong mảng theo dõi của `useEffect`.
