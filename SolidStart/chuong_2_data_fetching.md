# Chương 2: Data Fetching (Tải dữ liệu) trên Server

Một trong những lý do lớn nhất để sử dụng SolidStart là khả năng **tải dữ liệu trực tiếp trên Server** trước khi HTML được gửi về trình duyệt. Điều này giúp:
1. SEO (Search Engine Optimization) cực kỳ tốt vì Bot của Google có thể đọc được dữ liệu ngay lập tức.
2. Tốc độ tải trang nhanh hơn đối với người dùng cuối vì họ không cần chờ JavaScript tải xong mới bắt đầu đi lấy data.

## 1. Dùng `cache()` và `createAsync()`

Solid Router (nay được tích hợp sâu vào SolidStart) cung cấp một mô hình lấy dữ liệu rất thanh lịch sử dụng hàm `cache` kết hợp với `createAsync`.

Hàm `cache` làm 2 việc:
1. Đảm bảo hàm lấy dữ liệu chạy ở Server (nếu là trang SSR) hoặc Client (nếu là điều hướng nội bộ).
2. Tự động lưu cache kết quả vào bộ nhớ để không phải gọi API lại nhiều lần nếu dữ liệu chưa hết hạn hoặc người dùng quay lại trang.

```jsx
import { cache, createAsync } from "@solidjs/router";
import { Suspense, For } from "solid-js";

// 1. Tạo hàm lấy dữ liệu và bọc nó trong `cache()`
// Hàm này có tên là "getUsers" làm định danh cho việc lưu cache
const getUsers = cache(async () => {
  const response = await fetch("https://jsonplaceholder.typicode.com/users");
  if (!response.ok) throw new Error("Fetch failed");
  const data = await response.json();
  
  // Bạn thậm chí có thể console.log ở đây. 
  // Nếu tải trang lần đầu, log này sẽ in ra ở Terminal (Server), không phải Browser!
  return data;
}, "users-key"); // "users-key" là khoá để lưu vào cache

export default function UsersPage() {
  // 2. Kích hoạt việc lấy dữ liệu bằng createAsync
  // `users()` sẽ trở thành một Signal (Accessor) chứa dữ liệu khi tải xong.
  const users = createAsync(() => getUsers());

  return (
    <main>
      <h1>Danh sách Người Dùng (SSR)</h1>
      
      {/* 3. Dùng Suspense để hiển thị Loading State trong khi chờ API */}
      <Suspense fallback={<p>Đang tải dữ liệu từ Server...</p>}>
        <ul>
          <For each={users()}>
            {(user) => (
              <li>
                {user.name} - {user.email}
              </li>
            )}
          </For>
        </ul>
      </Suspense>
    </main>
  );
}
```

## 2. Truyền tham số vào hàm tải dữ liệu

Rất thường xuyên, bạn cần lấy thông tin của MỘT người dùng cụ thể dựa vào URL (ví dụ: `/users/123`). Bạn có thể truyền giá trị từ URL thẳng vào hàm `cache()`.

```jsx
// src/routes/users/[id].jsx
import { cache, createAsync, useParams } from "@solidjs/router";
import { Suspense } from "solid-js";

// Hàm lấy data nhận tham số ID
const getUserDetail = cache(async (id) => {
  const response = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
  return response.json();
}, "user-detail-key"); // key cache có thể giống nhau, Solid tự kết hợp với args để phân biệt

export default function UserDetail() {
  const params = useParams(); // Lấy ID từ thanh địa chỉ URL

  // Gọi hàm và truyền tham số `params.id`
  const user = createAsync(() => getUserDetail(params.id));

  return (
    <main>
      <Suspense fallback={<p>Đang tải thông tin chi tiết...</p>}>
        {/* Phải kiểm tra user() tồn tại trước khi render nếu API có thể trả về rỗng */}
        {user() ? (
          <div>
            <h1>{user().name}</h1>
            <p>Điện thoại: {user().phone}</p>
            <p>Website: {user().website}</p>
          </div>
        ) : (
          <p>Không tìm thấy người dùng.</p>
        )}
      </Suspense>
    </main>
  );
}
```

## 3. Server Functions (Lưu ý bảo mật)

Khi bạn dùng hàm `fetch()` trong ví dụ trên, URL là public API. Nhưng nếu bạn phải kết nối trực tiếp vào Database (như MySQL, PostgreSQL) thì sao?
Đừng lo, trong SolidStart bạn có thể dùng từ khóa `"use server"`. Nó đảm bảo một khối code LUÔN LUÔN chỉ chạy trên Server. Bạn có thể an toàn viết mật khẩu CSDL ở đây mà không sợ bị rò rỉ xuống Client. (Chúng ta sẽ nói kỹ hơn ở chương sau).

## Tổng kết Chương 2
- Đừng dùng `onMount` và `fetch` thông thường nếu bạn muốn làm SEO.
- Dùng `cache()` kết hợp với `createAsync()` để tải dữ liệu, SolidStart sẽ tự động xử lý toàn bộ logic SSR và Hydration.
- Bọc giao diện trong thẻ `<Suspense>` để có trải nghiệm UI mượt mà.
