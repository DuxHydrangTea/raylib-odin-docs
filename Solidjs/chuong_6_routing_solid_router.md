# Chương 6: Định tuyến với Solid Router

Khi xây dựng ứng dụng Một Trang (Single Page Application - SPA), bạn cần điều hướng giữa các trang mà không làm mới lại trình duyệt. `@solidjs/router` là thư viện chính thức để làm việc này trong SolidJS, tương tự như `react-router-dom` trong hệ sinh thái React.

## 1. Cài đặt và Thiết lập cơ bản

Trước hết, bạn cần bọc toàn bộ ứng dụng bằng `<Router>`.

```jsx
import { render } from "solid-js/web";
import { Router, Route } from "@solidjs/router";

// Các trang mẫu
function Home() {
  return <h1>Trang Chủ</h1>;
}

function About() {
  return <h1>Về Chúng Tôi</h1>;
}

function App() {
  return (
    <Router>
      <Route path="/" component={Home} />
      <Route path="/about" component={About} />
    </Router>
  );
}

// render(() => <App />, document.getElementById("app"));
```

## 2. Truyền tham số đường dẫn (Dynamic Routing)

Bạn có thể tạo các đường dẫn động bằng cách sử dụng dấu hai chấm `:` trước tên tham số. Để lấy tham số đó ra trong Component, ta dùng hook `useParams`.

```jsx
import { Router, Route, useParams, A } from "@solidjs/router";

function UserProfile() {
  // Lấy tham số 'id' từ URL (ví dụ: /users/123 -> id là "123")
  const params = useParams();

  return (
    <div>
      <h2>Hồ sơ người dùng: {params.id}</h2>
      <A href="/users">Quay lại danh sách</A>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Route path="/users/:id" component={UserProfile} />
    </Router>
  );
}
```

*Lưu ý: Thay vì thẻ `<a>` thông thường, bạn nên dùng thẻ `<A>` (viết hoa) từ `@solidjs/router` để chuyển trang mượt mà không bị reload lại (tương đương với `<Link>` bên React Router).*

## 3. Lồng ghép Route (Nested Routing) và Layouts

Solid Router cho phép lồng các Route vào nhau. Route cha có thể đóng vai trò làm Layout (chứa Navbar, Sidebar...) và truyền component con vào thuộc tính `props.children`.

```jsx
import { Router, Route, A } from "@solidjs/router";

// Layout Component
function DashboardLayout(props) {
  return (
    <div style={{ display: "flex" }}>
      <aside style={{ width: "200px", background: "#f4f4f4", padding: "10px" }}>
        <h3>Menu</h3>
        <ul>
          <li><A href="/dashboard">Tổng quan</A></li>
          <li><A href="/dashboard/settings">Cài đặt</A></li>
        </ul>
      </aside>
      
      <main style={{ padding: "20px", flex: 1 }}>
        {/* Nơi hiển thị nội dung của các Route con */}
        {props.children}
      </main>
    </div>
  );
}

function Overview() { return <h2>Trang Tổng Quan</h2>; }
function Settings() { return <h2>Trang Cài Đặt</h2>; }

function App() {
  return (
    <Router>
      {/* Route Cha */}
      <Route path="/dashboard" component={DashboardLayout}>
        {/* Route Con: Đường dẫn sẽ ghép vào cha */}
        <Route path="/" component={Overview} />
        <Route path="/settings" component={Settings} />
      </Route>
    </Router>
  );
}
```

## 4. Lazy Loading Components

Để tối ưu hóa thời gian tải trang đầu tiên (Initial Load Time), thay vì import toàn bộ trang web vào 1 file JS khổng lồ, bạn có thể trì hoãn việc tải các trang chưa dùng tới bằng hàm `lazy`.

```jsx
import { lazy, Suspense } from "solid-js";
import { Router, Route } from "@solidjs/router";

// Chỉ tải component Admin khi user truy cập vào /admin
const AdminPage = lazy(() => import("./pages/Admin"));

function App() {
  return (
    <Router root={(props) => (
      // Khi component Lazy đang được tải qua mạng, hiển thị Fallback
      <Suspense fallback={<div>Đang tải trang...</div>}>
        {props.children}
      </Suspense>
    )}>
      <Route path="/admin" component={AdminPage} />
    </Router>
  );
}
```

## Tổng kết Chương 6
- **`<Router>`**: Khởi tạo hệ thống định tuyến.
- **`<Route>`**: Liên kết đường dẫn (`path`) với Component. Hỗ trợ tham số động (`:id`) và lồng ghép (Nested).
- **`<A>`**: Dùng thay thế `<a>` để ngăn chặn reload trang.
- **`useParams`**: Lấy các tham số động từ URL.
- **`lazy`**: Phân tách code (Code splitting) theo Route để cải thiện tốc độ.
