# Chương 6: Xử lý Routing chuẩn xác với React Router v6+

Trong các ứng dụng SPA (Single Page Application), Router không chỉ làm nhiệm vụ "đổi URL hiển thị màn hình", mà nó còn đóng vai trò như một bộ xương sống điều khiển luồng dữ liệu. Bắt đầu từ bản v6.4 (Data Router API), **React Router** đã thay đổi hoàn toàn cách chúng ta nạp dữ liệu và xử lý lỗi.

---

## 1. Khai báo Router bằng Object (Data API) thay vì JSX

Ở bản cũ (v5), chúng ta dùng thẻ `<Switch>` và `<Route>` lồng nhau. Dù dễ nhìn nhưng nó không hỗ trợ tính năng nạp dữ liệu sớm (Early data fetching) của v6.4+.

**Chuẩn Enterprise hiện tại là `createBrowserRouter`:**

```tsx
// src/app/router/index.tsx
import { createBrowserRouter } from 'react-router-dom';
import { RootLayout } from '../layout/RootLayout';
import { ErrorPage } from '../pages/ErrorPage';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <ErrorPage />, // Bắt LỖI cho toàn bộ nhánh này!
    children: [
      {
        index: true,
        lazy: () => import('@/pages/Home') // Code-splitting: Chỉ tải JS khi vào trang
      },
      {
        path: 'users',
        lazy: () => import('@/pages/Users')
      },
      {
        path: 'users/:id',
        lazy: () => import('@/pages/UserDetail')
      }
    ]
  }
]);

// Trong main.tsx:
// <RouterProvider router={router} />
```

---

## 2. Loại bỏ nhấp nháy Loading với `loader`

Theo cách truyền thống, khi user bấm vào trang `UserDetail`:
1. Trình duyệt tải JS của `UserDetail`.
2. Chạy hàm render, hiển thị màn hình `Loading...`.
3. Chạy `useEffect`, gọi API tải user.
4. API trả về, render lại màn hình thật.
=> **UX bị giật, nhấp nháy.**

React Router v6 giới thiệu **`loader`**, cho phép gọi API *song song* với việc tải JS và chuyển trang. Chỉ khi data sẵn sàng, trang mới được hiển thị.

```tsx
// 1. Định nghĩa loader tại file UserDetail
export const userLoader = async ({ params }) => {
  const user = await fetch(`/api/users/${params.id}`).then(res => res.json());
  if (!user) {
    throw new Response("Not Found", { status: 404 }); // Đẩy thẳng vào ErrorBoundary
  }
  return user;
};

export function UserDetail() {
  // 2. Lấy data mà KHÔNG CẦN useEffect hay isLoading!
  const user = useLoaderData(); 
  
  return <div>{user.name}</div>;
}
```

```tsx
// 3. Gắn vào Router
{
  path: 'users/:id',
  loader: userLoader,
  element: <UserDetail />
}
```
*Ghi chú:* Khi kết hợp React Router `loader` với `React Query`, bạn có một hệ thống Prefetching vô địch (cực kì mượt mà).

---

## 3. Xử lý Form không dùng State với `action`

Xưa kia, để làm 1 form đăng nhập, bạn phải tạo 2 cái state (`email`, `password`), gắn `onChange`, gọi `e.preventDefault()` khi submit... Khá nhiều mã thừa (boilerplate).

React Router v6 có component `<Form>` (Lưu ý chữ F viết hoa). Nó hoạt động y như HTML Form truyền thống, thu thập dữ liệu và ném cho hàm **`action`** xử lý, không cần `useState`.

```tsx
// 1. Giao diện (Không cần State!)
import { Form, useActionData, useNavigation } from 'react-router-dom';

export function LoginForm() {
  const errors = useActionData(); // Lỗi từ action ném về (nếu có)
  const navigation = useNavigation();
  const isSubmitting = navigation.state === 'submitting';

  return (
    <Form method="post"> {/* Bấm submit nó sẽ gọi action ở dưới */}
      <input type="email" name="email" required />
      <input type="password" name="password" required />
      
      {errors?.message && <p className="error">{errors.message}</p>}
      
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Đang login...' : 'Login'}
      </button>
    </Form>
  );
}

// 2. Hàm Action xử lý logic
export const loginAction = async ({ request }) => {
  const formData = await request.formData();
  const email = formData.get('email');
  const password = formData.get('password');

  try {
    await api.login(email, password);
    return redirect('/dashboard'); // Chuyển trang nếu thành công
  } catch (error) {
    return { message: "Sai tài khoản hoặc mật khẩu" }; // Trả lỗi về UI
  }
};
```

---

## 4. Xử lý Lỗi Tinh Tế với `errorElement` (Error Boundary)

Trong React, nếu 1 biến bị `undefined` và bạn cố map() nó, **CẢ TRANG WEB SẼ TRẮNG XÓA (Crash)**.
React Router xử lý việc này bằng `errorElement`. Nếu trang `UserDetail` bị crash hoặc API lỗi, nó chỉ hiển thị lỗi ngay tại khu vực của `UserDetail`, còn `Header`, `Sidebar` ở `RootLayout` vẫn hiển thị bình thường.

```tsx
import { useRouteError } from 'react-router-dom';

export function ErrorPage() {
  const error = useRouteError(); // Lấy chi tiết lỗi
  
  return (
    <div className="error-container">
      <h2>Ôi không! Có lỗi xảy ra.</h2>
      <p>{error.statusText || error.message}</p>
      <button onClick={() => window.location.reload()}>Thử lại</button>
    </div>
  );
}
```

Hãy đảm bảo bạn thiết lập ít nhất một `errorElement` ở gốc root, và nếu cẩn thận, thiết lập thêm ở các trang quan trọng để "cách ly" lỗi.
