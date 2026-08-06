# Chương 4: Quản Lý Global State (Zustand & Redux Toolkit)

Trong các dự án lớn, việc truyền dữ liệu qua nhiều lớp Component (Prop Drilling) là một "cơn ác mộng". Để giải quyết vấn đề này, chúng ta cần một **Global Store**. Hiện nay, hai công cụ phổ biến nhất và được khuyên dùng ở môi trường Enterprise là **Zustand** (nhẹ, nhanh, linh hoạt) và **Redux Toolkit** (chặt chẽ, chuẩn mực cho dự án siêu lớn).

*Lưu ý: Không nên dùng Context API cho các state thay đổi liên tục, vì Context API sẽ làm toàn bộ các Component tiêu thụ (consumer) bị re-render ngay cả khi giá trị chúng cần không đổi.*

---

## 1. Zustand - Kẻ thống trị mới của Global State

Zustand là một thư viện siêu nhẹ (chỉ ~1kb), không cần setup Provider (như Redux hay Context), và chống re-render thừa rất tốt.

### Cách setup chuẩn Enterprise:
Thay vì nhét mọi state vào 1 store duy nhất, hãy tách store theo các miền nghiệp vụ (slices).

```tsx
// src/shared/store/useAuthStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware'; // Hỗ trợ lưu LocalStorage

interface User {
  id: string;
  name: string;
  role: 'admin' | 'user';
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  login: (user: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      login: (user) => set({ user, isAuthenticated: true }),
      logout: () => set({ user: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage', // Tên key trong localStorage
    }
  )
);
```

### Tuyệt chiêu tối ưu Re-render với Zustand
Đừng bao giờ lấy toàn bộ store ra dùng nếu không thực sự cần.

**Sai (Sẽ bị re-render nếu bất kỳ giá trị nào trong store thay đổi):**
```tsx
const store = useAuthStore();
return <div>{store.user.name}</div>;
```

**Đúng (Chỉ re-render khi đúng biến user thay đổi):**
```tsx
const user = useAuthStore((state) => state.user);
return <div>{user.name}</div>;
```

---

## 2. Redux Toolkit (RTK) - Lựa chọn cho dự án khổng lồ

Nếu team của bạn > 20 người, nghiệp vụ cực kỳ phức tạp (như ứng dụng Trading, Figma clone), Redux Toolkit (RTK) mang lại cấu trúc chặt chẽ và công cụ Debugging (Redux DevTools) không thể đánh bại.

### Tại sao RTK thay thế Redux cũ?
- Không cần viết boilerplate (action, reducer riêng lẻ).
- Tích hợp sẵn Immer (viết code mutate state một cách an toàn).
- Tích hợp sẵn Redux Thunk cho async.

### Cấu trúc 1 Slice trong RTK:
```tsx
// src/features/cart/model/cartSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CartState {
  items: Array<{ id: string; qty: number }>;
  total: number;
}

const initialState: CartState = { items: [], total: 0 };

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    // Nhờ có Immer, bạn được phép "sửa" trực tiếp state thay vì phải return {...state}
    addItem: (state, action: PayloadAction<{ id: string }>) => {
      const existing = state.items.find(i => i.id === action.payload.id);
      if (existing) {
        existing.qty += 1;
      } else {
        state.items.push({ id: action.payload.id, qty: 1 });
      }
    },
    removeItem: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter(i => i.id !== action.payload);
    }
  }
});

export const { addItem, removeItem } = cartSlice.actions;
export default cartSlice.reducer;
```

### Tối ưu Selector với Reselect (Quan trọng)
Trong Redux, khi bạn thực hiện các phép tính toán dựa trên State (Derived State), nếu không cẩn thận Component sẽ re-render vô tội vạ. RTK tích hợp sẵn `createSelector` để giải quyết việc này (Memoized Selector).

```tsx
import { createSelector } from '@reduxjs/toolkit';

// Chỉ lấy mảng items gốc
const selectCartItems = (state: RootState) => state.cart.items;

// Selector tính tổng số lượng - CHỈ CHẠY LẠI khi items thay đổi
export const selectTotalQuantity = createSelector(
  [selectCartItems],
  (items) => items.reduce((total, item) => total + item.qty, 0)
);

// Ở Component:
// useSelector sẽ biết tự chặn re-render nếu kết quả không đổi
const totalQty = useSelector(selectTotalQuantity); 
```

---

## Tóm tắt Actionable

1. **Dự án mới, quy mô vừa và lớn vừa:** Hãy mạnh dạn chọn **Zustand**. Code sạch, nhẹ, dễ refactor.
2. **Dự án enterprise khổng lồ, team dev đông đảo:** Chọn **Redux Toolkit**. Sự chặt chẽ của nó giúp quản trị rủi ro tốt hơn.
3. Luôn luôn extract State chi tiết nhất có thể ra khỏi Store, **không lấy toàn bộ state object** (dù dùng Zustand hay Redux). Mọi tính toán từ State (Derived state) phải được **Memoize** (bằng `useStore(selector)` hoặc `createSelector`).
