# Chương 5: Bất đồng bộ (Async) và Gói Dữ Liệu

Khi làm việc với các framework frontend, việc gọi API và quản lý trạng thái loading, lỗi (error), hiển thị dữ liệu là một công việc lặp đi lặp lại. SolidJS đã tích hợp sẵn các Primitives vô cùng mạnh mẽ cho việc này.

## 1. Tìm nạp dữ liệu với `createResource`

`createResource` là một primitive đặc biệt dùng để kết nối dữ liệu bất đồng bộ (ví dụ: fetch API) với hệ thống Reactivity của Solid.

Hàm này trả về mảng gồm `[data, { mutate, refetch }]`. Biến `data` không chỉ chứa dữ liệu trả về, mà còn mang theo các trạng thái (loading, error) như những thuộc tính (properties).

```jsx
import { createResource, Switch, Match } from "solid-js";

// Một hàm fetch thông thường trả về Promise
const fetchUser = async (id) => {
  const response = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
  if (!response.ok) throw new Error("Không thể tải dữ liệu");
  return response.json();
};

function UserProfile(props) {
  // createResource nhận vào tham số ban đầu (props.userId) 
  // và một hàm fetch. Hàm fetch sẽ TỰ ĐỘNG được gọi lại khi props.userId thay đổi.
  const [user] = createResource(() => props.userId, fetchUser);

  return (
    <div>
      <Switch>
        {/* user.error sẽ có giá trị nếu Promise bị reject */}
        <Match when={user.error}>
          <p style={{ color: "red" }}>Lỗi: {user.error.message}</p>
        </Match>

        {/* user.loading sẽ là true khi Promise đang chạy */}
        <Match when={user.loading}>
          <p>Đang tải dữ liệu người dùng...</p>
        </Match>

        {/* Khi thành công, gọi user() để lấy dữ liệu */}
        <Match when={user()}>
          <div>
            <h2>{user().name}</h2>
            <p>Email: {user().email}</p>
          </div>
        </Match>
      </Switch>
    </div>
  );
}
```

## 2. Xử lý UI đồng bộ với `<Suspense>`

Mặc dù `user.loading` rất hữu ích, việc viết các câu lệnh `Switch / Match` liên tục ở nhiều cấp Component khác nhau có thể gây rườm rà. SolidJS cung cấp thẻ `<Suspense>` để tạm dừng hiển thị toàn bộ một khu vực giao diện cho đến khi mọi `Resource` bên trong nó hoàn thành.

```jsx
import { createResource, Suspense, createSignal } from "solid-js";

const fetchQuote = async () => {
  const response = await fetch("https://api.quotable.io/random");
  return response.json();
};

function Quote() {
  const [quote] = createResource(fetchQuote);
  return <blockquote>"{quote()?.content}" - {quote()?.author}</blockquote>;
}

function App() {
  const [tab, setTab] = createSignal("quote");

  return (
    <div>
      <h1>Ứng dụng trích dẫn</h1>
      
      {/* Bọc component cần nạp dữ liệu vào Suspense */}
      <Suspense fallback={<div class="spinner">Đang lấy trích dẫn hay nhất...</div>}>
        <Quote />
      </Suspense>
    </div>
  );
}
```

## 3. Quản lý Lỗi với `<ErrorBoundary>`

Tương tự như `<Suspense>` quản lý trạng thái chờ, `<ErrorBoundary>` quản lý trạng thái lỗi. Nếu bất kỳ Component con nào văng ra lỗi (throw Error) hoặc `Resource` bị reject mà không xử lý thủ công, `<ErrorBoundary>` sẽ bắt lấy nó và hiển thị một fallback UI thay vì làm sập toàn bộ ứng dụng.

```jsx
import { ErrorBoundary } from "solid-js";
import { render } from "solid-js/web";

function BrokenComponent() {
  // Cố tình ném ra một lỗi
  throw new Error("Lỗi kết nối cơ sở dữ liệu!");
  return <p>Đoạn text này không bao giờ hiển thị</p>;
}

function Main() {
  return (
    <div>
      <h2>Hệ thống cốt lõi</h2>
      
      <ErrorBoundary fallback={(err, reset) => (
        <div style={{ padding: "10px", border: "1px solid red" }}>
          <p>Có lỗi nghiêm trọng: {err.message}</p>
          {/* Bạn có thể gọi hàm reset để render lại UI bên trong nếu cần */}
          <button onClick={reset}>Thử lại</button>
        </div>
      )}>
        {/* Nếu BrokenComponent lỗi, nó sẽ bị thay thế bởi fallback ở trên */}
        <BrokenComponent />
      </ErrorBoundary>
      
      <p>Ứng dụng chính vẫn hoạt động bình thường, không bị sập.</p>
    </div>
  );
}

// render(() => <Main />, document.getElementById("app"));
```

## Tổng kết Chương 5
- **`createResource`**: Công cụ tối thượng để liên kết Promise với Reactivity.
- **`<Suspense>`**: Khung chứa hiển thị trạng thái `Loading` thanh lịch.
- **`<ErrorBoundary>`**: Màng chắn bảo vệ ứng dụng khỏi các cú `throw Error`.
