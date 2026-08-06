# Chương 3: Quản Lý Trạng Thái (State Management) Hiện Đại

Hệ sinh thái React năm 2024+ đã thay đổi rất nhiều so với thời kỳ hoàng kim của Redux (2018-2020). Việc đặt tất cả dữ liệu vào chung một "Global Store" khổng lồ không còn là best practice nữa. 

Ngày nay, ở tầm Enterprise, người ta phân loại State thành **3 loại riêng biệt** và dùng công cụ chuyên dụng cho từng loại.

---

## 1. Local State (Trạng thái cục bộ)

Là dữ liệu chỉ thuộc về một Component hoặc một cụm Component nhỏ. **Nếu component đó bị unmount (gỡ khỏi màn hình), dữ liệu này cũng nên biến mất.**

- **Ví dụ:** Trạng thái mở/đóng của một Modal, giá trị đang gõ trong một input text, trạng thái active của một tab.
- **Công cụ:** `useState`, `useReducer`, hoặc lưu tạm vào `ref` (bằng `useRef`) nếu không cần re-render.

**Enterprise Tip:** 
Đừng lạm dụng `useState` cho dữ liệu có thể tính toán được từ state khác (Derived State). 
```tsx
// ❌ BAD: Dùng thêm state thừa thãi, dễ bị lỗi đồng bộ
const [items, setItems] = useState([1, 2, 3]);
const [count, setCount] = useState(3); 

// ✅ GOOD: Dữ liệu suy xuất (Derived State)
const [items, setItems] = useState([1, 2, 3]);
const count = items.length; // Luôn luôn đúng, không cần setState
```

---

## 2. Server State (Trạng thái từ máy chủ)

Đây là thay đổi lớn nhất trong kiến trúc Frontend hiện đại. Server State là dữ liệu được tải từ backend API (VD: Danh sách bài viết, Thông tin User).
Đặc điểm của nó là:
- Nó không thuộc quyền kiểm soát hoàn toàn của Frontend (Backend có thể thay đổi nó bất cứ lúc nào).
- Cần cơ chế Cache (Lưu tạm), Tái xác thực (Revalidation), Xử lý lỗi (Error handling), Trạng thái tải (Loading state).

**Công cụ tiêu chuẩn hiện nay:** **TanStack Query (React Query)** hoặc **SWR**.

**❌ Cách cũ (Dùng `useEffect` + Global State / Local State):**
Quá nhiều code Boilerplate (viết đi viết lại `loading`, `error`, `data`), không có cache.
```tsx
const [data, setData] = useState(null);
const [loading, setLoading] = useState(true);

useEffect(() => {
  fetch('/api/user')
    .then(res => res.json())
    .then(setData)
    .finally(() => setLoading(false));
}, []);
```

**✅ Cách mới (React Query):**
Chuẩn mực của Enterprise: Tự động cache, tự động fetch lại khi người dùng quay lại tab, tự động gộp các request trùng lặp (Deduping).
```tsx
import { useQuery } from '@tanstack/react-query';

function UserProfile() {
  const { data: user, isLoading, isError } = useQuery({
    queryKey: ['user', 'profile'],
    queryFn: () => fetch('/api/user').then(res => res.json())
  });

  if (isLoading) return <Spinner />;
  if (isError) return <div>Lỗi tải dữ liệu</div>;

  return <div>{user.name}</div>;
}
```
*Lưu ý: Chúng ta sẽ đi sâu vào React Query ở Chương 5.*

---

## 3. Global Client State (Trạng thái toàn cục phía Client)

Là dữ liệu **được tạo ra bởi người dùng ở Client**, cần được chia sẻ qua nhiều màn hình/component khác nhau, ở các nhánh cách xa nhau trong cây Component.
- **Ví dụ:** Trạng thái Dark/Light Mode, Giỏ hàng (Cart) khi chưa đồng bộ lên server, Thông báo Toast.
- **Công cụ:** **Zustand** (Rất nhẹ, dễ dùng - Khuyên dùng hiện nay) hoặc **Redux Toolkit** (Cho dự án siêu lớn, có team size > 20 frontend devs). Không nên dùng `Context API` cho dữ liệu thay đổi liên tục vì nó gây ra hiện tượng Re-render toàn bộ app (Performance issue).

**Ví dụ dùng Zustand cho Giỏ hàng:**
```tsx
import { create } from 'zustand';

// 1. Tạo Store độc lập bên ngoài Component
type CartStore = {
  count: number;
  increment: () => void;
};

export const useCartStore = create<CartStore>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));

// 2. Sử dụng ở bất kỳ Component nào (Chỉ component nào gọi hook này mới bị re-render)
function Header() {
  const count = useCartStore((state) => state.count);
  return <div>Giỏ hàng: {count}</div>;
}

function AddToCartButton() {
  const increment = useCartStore((state) => state.increment);
  return <button onClick={increment}>Thêm vào giỏ</button>;
}
```

---

## 4. Tóm tắt Actionable cho người đi làm

Khi bạn định lưu một biến vào state, hãy tự hỏi:
1. **Dữ liệu này từ API về?** -> Bỏ ngay suy nghĩ dùng `useState` hay Redux. Dùng **React Query**.
2. **Dữ liệu này chỉ mình component này xài?** -> Dùng **`useState` / `useReducer`**.
3. **Dữ liệu này phải share cho cả cái Header và Sidebar xài chung?** -> Dùng **Zustand** (hoặc Redux Toolkit). 
4. **Dữ liệu này có thể suy ra từ url (ví dụ: filter, search tab)?** -> Đừng dùng state, hãy đẩy nó lên **URL parameters** (Bằng React Router). Nó giúp user copy link gửi cho bạn bè mà vẫn giữ nguyên trạng thái filter!
