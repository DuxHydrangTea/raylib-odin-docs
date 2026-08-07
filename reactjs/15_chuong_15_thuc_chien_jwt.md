# Chương 15: Thực chiến Xác thực & Phân quyền (JWT & OAuth)

Trong môi trường doanh nghiệp, bảo mật ứng dụng và quản lý luồng đăng nhập là yếu tố tối quan trọng. Chuẩn xác thực phổ biến nhất hiện nay khi kết nối Frontend với Backend API chính là **JWT (JSON Web Token)**.

Chương này sẽ hướng dẫn bạn cách triển khai JWT chuyên nghiệp, khắc phục các lỗ hổng bảo mật chết người mà các Newbie thường mắc phải, và thiết lập luồng Refresh Token tự động hoàn hảo.

---

## 1. Hiểu đúng về cơ chế JWT

Một luồng JWT chuẩn trong doanh nghiệp luôn bao gồm 2 loại token:

1. **Access Token (Token truy cập):**
   - Có thời hạn rất ngắn (ví dụ: 15 phút).
   - Được đính kèm vào Header (`Authorization: Bearer <token>`) của mỗi request gọi lên API.
   - Chứa thông tin cơ bản của user (ID, Role). Không nên lưu trữ thông tin nhạy cảm (như mật khẩu, số thẻ).

2. **Refresh Token (Token làm mới):**
   - Có thời hạn dài (ví dụ: 7 ngày, 30 ngày).
   - Chỉ dùng cho một mục đích duy nhất: Lấy Access Token mới khi Access Token cũ hết hạn.
   - Thường được Backend set tự động vào `httpOnly Cookie` để bảo vệ tối đa khỏi tấn công XSS.

---

## 2. Lưu trữ Token ở đâu an toàn nhất?

**Sai lầm phổ biến:** Lưu thẳng `Access Token` và `Refresh Token` vào `localStorage`.
**Hậu quả:** `localStorage` có thể bị đọc bởi bất kỳ đoạn mã JavaScript nào chạy trên trang web (kể cả mã độc từ các thư viện NPM bên thứ 3 hoặc CDN). Đây gọi là lỗ hổng **XSS (Cross-Site Scripting)**. Kẻ gian sẽ lấy token và chiếm quyền tài khoản hoàn toàn.

**Giải pháp chuẩn doanh nghiệp:**
- **Access Token:** Lưu trong `Memory` (Biến Zustand, Redux, hoặc Context). Nếu user F5 trang, Token sẽ mất, nhưng chúng ta sẽ tự động xin lại cái mới.
- **Refresh Token:** Backend bắt buộc phải trả về qua **httpOnly Cookie** và thiết lập thuộc tính `Secure`. Trình duyệt sẽ tự động quản lý Cookie này. Frontend không thể đọc được (chặn đứng XSS), nhưng mỗi khi Frontend gọi API tới Backend, trình duyệt sẽ tự động đính kèm Cookie này.

---

## 3. Triển khai Axios Interceptors (Tự động hóa luồng gọi API)

Để không phải viết đi viết lại đoạn code gắn `Bearer token` vào từng request, chúng ta dùng tính năng **Interceptors** của Axios.

```javascript
// src/api/axiosClient.js
import axios from 'axios';
import useAuthStore from '../store/useAuthStore'; // Giả sử bạn dùng Zustand

const axiosClient = axios.create({
  baseURL: 'https://api.yourdomain.com',
  // Nếu Backend cần đọc httpOnly Cookie (Refresh Token), bật cấu hình này lên
  withCredentials: true, 
});

// Đánh chặn trước khi GỬI request
axiosClient.interceptors.request.use(
  (config) => {
    // Lấy Access Token từ Memory (Zustand/Redux)
    const token = useAuthStore.getState().accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);
```

---

## 4. Xử lý "Refresh Token" tự động (Xử lý hàng đợi)

Đây là kỹ thuật phân loại Senior vs Junior Frontend. 

**Vấn đề:** Khi Access Token hết hạn, API trả về lỗi `401 Unauthorized`. Frontend phải âm thầm gọi API lấy Token mới (bằng Refresh Token Cookie), rồi **chạy lại (retry)** cái API vừa thất bại để user không hề hay biết sự cố. 

Tuy nhiên, điều gì xảy ra nếu tại 1 thời điểm, trang web của bạn gọi **5 API cùng lúc** và cả 5 đều ăn lỗi 401? Bạn không thể gọi hàm Refresh Token 5 lần liên tiếp! Bạn phải chặn 4 request kia lại, đưa vào hàng đợi, chờ request đầu tiên lấy được token xong thì giải phóng cả 4.

```javascript
// src/api/axiosClient.js
let isRefreshing = false;
let failedQueue = [];

// Xử lý các request đang đợi
const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

axiosClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Bắt đúng lỗi 401 (Hết hạn Token) và đảm bảo request này chưa bị retry lần nào
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // Nếu ĐANG refresh token, nhét request này vào hàng đợi (Promise Queue)
        return new Promise(function(resolve, reject) {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers['Authorization'] = 'Bearer ' + token;
            return axiosClient(originalRequest); // Retry
          })
          .catch((err) => Promise.reject(err));
      }

      // Khóa cờ lại
      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // Gọi API lên Backend xin Access Token mới (Trình duyệt tự đính kèm httpOnly Cookie)
        const response = await axios.post('https://api.yourdomain.com/auth/refresh', {}, {
           withCredentials: true 
        });
        
        const newAccessToken = response.data.accessToken;

        // Lưu Token mới vào Memory
        useAuthStore.getState().setAccessToken(newAccessToken);

        // Giải phóng hàng đợi
        processQueue(null, newAccessToken);

        // Gắn token mới và chạy lại request đầu tiên
        originalRequest.headers['Authorization'] = 'Bearer ' + newAccessToken;
        return axiosClient(originalRequest);
      } catch (err) {
        // Refresh Token cũng hết hạn luôn -> Bắt user Login lại
        processQueue(err, null);
        useAuthStore.getState().logout(); 
        window.location.href = '/login';
        return Promise.reject(err);
      } finally {
        isRefreshing = false; // Mở khóa
      }
    }

    return Promise.reject(error);
  }
);
```

---

## 5. Phân quyền và Bảo vệ Routes (Private Route)

Sau khi có luồng Đăng nhập / Refresh chuẩn, bạn bọc các trang nhạy cảm (Admin, Dashboard) bằng một component `ProtectedRoute` để đá user ra ngoài nếu họ chưa đăng nhập hoặc không đủ quyền (Role-based).

```jsx
// src/components/ProtectedRoute.jsx
import { Navigate, Outlet } from 'react-router-dom';
import useAuthStore from '../store/useAuthStore';

const ProtectedRoute = ({ allowedRoles }) => {
  const { user, isAuth, isLoading } = useAuthStore();

  if (isLoading) return <div>Đang kiểm tra phiên đăng nhập...</div>;

  if (!isAuth) {
    // Chưa đăng nhập -> đá về Login
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    // Đã đăng nhập nhưng không có quyền -> đá về lỗi 403
    return <Navigate to="/403" replace />;
  }

  // Hợp lệ -> Cho phép truy cập vào component bên trong
  return <Outlet />;
};

export default ProtectedRoute;
```

Trong `App.jsx`, bạn bọc Route như sau:
```jsx
<Routes>
  {/* Public Route */}
  <Route path="/login" element={<Login />} />

  {/* Private Route: Bất kỳ User nào đã đăng nhập */}
  <Route element={<ProtectedRoute />}>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/profile" element={<Profile />} />
  </Route>

  {/* Admin Route: Chỉ dành cho Role ADMIN */}
  <Route element={<ProtectedRoute allowedRoles={['ADMIN']} />}>
    <Route path="/admin" element={<AdminPanel />} />
  </Route>
</Routes>
```

**Tóm lược Chương 15:** 
- JWT bảo mật tốt nhất khi kết hợp `Access Token (Memory)` và `Refresh Token (httpOnly Cookie)`.
- Kỹ thuật `Promise Queue` trong Axios Interceptor cứu cánh hệ thống khỏi bão "Refresh Token".
- Luôn kiểm tra phân quyền (Role) tại cả Frontend (UX) lẫn Backend (Bảo mật tuyệt đối).
