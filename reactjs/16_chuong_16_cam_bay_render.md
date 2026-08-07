# Chương 16: Mổ xẻ Cạm bẫy Render và Rò rỉ bộ nhớ (Memory Leaks)

Hiệu năng của React phụ thuộc vào một triết lý vô cùng cốt lõi: **Khi State/Props thay đổi, Component sẽ chạy lại (Re-render).** 

Nhưng nếu không hiểu sâu sắc quá trình này, các Dev mới thường vô tình biến React thành "kẻ sát nhân" giết chết tốc độ trình duyệt vì Re-render dư thừa (Wasted Renders) và Rò rỉ bộ nhớ (Memory Leaks).

---

## 1. Bản chất của quá trình Re-render

Một component React bị Re-render khi một trong 3 điều kiện sau xảy ra:
1. **State bên trong nó thay đổi.**
2. **Props truyền từ component cha xuống thay đổi.**
3. **Component cha bị Re-render** (Lý do kinh điển nhất!).

Đúng vậy! Trừ khi bạn sử dụng `React.memo`, nếu Component Cha re-render, TOÀN BỘ Component Con bên trong nó sẽ bị re-render theo, bất chấp việc Props của component con có đổi hay không.

### 💀 Sai lầm 1: Component con bị re-render oan mạng
```jsx
// Kém tối ưu
function Parent() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Đếm: {count}</button>
      {/* HeavyChild bị re-render liên tục mỗi khi bấm nút đếm, dù nó chẳng liên quan gì đến count! */}
      <HeavyChild /> 
    </div>
  );
}
```

**✅ Giải pháp: Push State Down (Đẩy State xuống dưới)**
Tách phần hiển thị `count` ra thành một component riêng (`Counter`). Như vậy, khi bấm đếm, chỉ có `Counter` re-render, `Parent` và `HeavyChild` bình an vô sự.

```jsx
// Tối ưu
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>Đếm: {count}</button>;
}

function Parent() {
  return (
    <div>
      <Counter />
      <HeavyChild /> 
    </div>
  );
}
```

---

## 2. Lạm dụng Context API gây thảm họa hiệu năng

React Context là công cụ tuyệt vời để tránh Props Drilling. Nhưng nó đi kèm một hình phạt nặng:
**Bất kỳ component nào tiêu thụ (useContext) một Context, sẽ bị Re-render khi GIÁ TRỊ của Context đó thay đổi.**

Giả sử bạn có `GlobalContext` chứa `{ user, theme, cartItems }`. Nếu bạn dùng `useContext` ở Sidebar chỉ để đọc `theme` (Sáng/Tối), nhưng ở một nơi khác, ai đó thêm món hàng vào `cartItems`. Hậu quả? Context thay đổi -> **Sidebar bị re-render theo**, dù nó chả quan tâm gì tới giỏ hàng!

**✅ Giải pháp:** 
1. Tách Context ra làm nhiều Context nhỏ (VD: `ThemeContext`, `CartContext`, `AuthContext`).
2. Hoặc tốt nhất là chuyển sang dùng **Zustand** hoặc **Redux Toolkit** cho các state thay đổi liên tục. Zustand cho phép bạn chọn lọc (select) chính xác thuộc tính cần lấy, thuộc tính khác đổi thì component không bị re-render.

---

## 3. Quên dọn dẹp useEffect (Thủ phạm gây Memory Leaks)

`Memory Leak` (Rò rỉ bộ nhớ) xảy ra khi bạn tạo ra một tiến trình ngầm (như `setInterval`, `addEventListener`) nhưng khi Component biến mất (Unmount), bạn lại **quên xóa tiến trình đó đi**. Trình duyệt sẽ chạy tiến trình đó mãi mãi.

### 💀 Sai lầm 2: Lắng nghe sự kiện không xóa
```jsx
function MouseTracker() {
  useEffect(() => {
    const handleMouseMove = (e) => console.log(e.clientX, e.clientY);
    
    // Đăng ký event
    window.addEventListener('mousemove', handleMouseMove);
    
    // 💀 QUÊN XÓA (No Cleanup Function)
    // Nếu MouseTracker bị ẩn đi, window vẫn tiếp tục chạy console.log mãi mãi!
  }, []);

  return <div>Tracking...</div>;
}
```

**✅ Giải pháp: Trả về Cleanup Function trong useEffect**
```jsx
function MouseTracker() {
  useEffect(() => {
    const handleMouseMove = (e) => console.log(e.clientX, e.clientY);
    window.addEventListener('mousemove', handleMouseMove);
    
    // ✅ React sẽ gọi hàm này ngay trước khi MouseTracker bị Unmount
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);
  
  return <div>Tracking...</div>;
}
```

**Một số trường hợp phổ biến khác cần Cleanup:**
- `clearInterval`, `clearTimeout`.
- Hủy API Call đang dở dang bằng `AbortController` (Khi mạng chậm, user chuyển trang khác mà API cũ vẫn đang tải, về lý thuyết khi API tải xong nó sẽ cố gắng update State của một Component đã không còn tồn tại -> Lỗi React Memory Leak warning).

---

## 4. Bẫy Khởi tạo (Initialization Trap)

### 💀 Sai lầm 3: Object và Function bị tạo mới liên tục
Mỗi khi component re-render, mọi biến, mảng, object, và hàm bên trong nó đều **bị khởi tạo lại ở một địa chỉ ô nhớ mới**.

```jsx
function SearchUser() {
  const [query, setQuery] = useState("");

  // Mỗi lần gõ phím, mảng này được tạo mới hoàn toàn (Object Reference mới)
  const filters = { role: "admin", active: true }; 

  // Mỗi lần gõ phím, hàm này cũng bị tạo lại
  const handleSearch = () => { /* logic */ };

  return (
    <div>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      {/* ChildComponent sẽ thấy Props 'filters' và 'onSearch' luôn luôn LÀ ĐỒ MỚI 
          -> Dẫn đến ChildComponent tự Re-render vô tội vạ! */}
      <ChildComponent filters={filters} onSearch={handleSearch} />
    </div>
  );
}
```

**✅ Giải pháp: Đưa ra ngoài Component hoặc dùng `useMemo` / `useCallback`**

1. Nếu `filters` tĩnh (không đổi), hãy vứt nó ra ngoài hàm `SearchUser`.
```jsx
const filters = { role: "admin", active: true }; // Tĩnh vĩnh viễn
function SearchUser() { ... }
```

2. Nếu cần truyền hàm xuống Component con (đã bọc `React.memo`), hãy bọc hàm bằng `useCallback`.
```jsx
const handleSearch = useCallback(() => { /* logic */ }, []);
```

**Tóm lược Chương 16:**
- Hiểu rõ 3 nguyên lý gây Re-render của React.
- Chia nhỏ Component, hạ State xuống thấp nhất có thể.
- Đừng lạm dụng Context API cho dữ liệu thay đổi quá nhanh.
- Luôn luôn nhớ Cleanup `useEffect`.
- `useMemo` và `useCallback` không sinh ra để dùng bừa bãi, nó chỉ có tác dụng khi truyền Props xuống một Child Component đã được bọc `React.memo`.
