# Chương 13: Bảo mật Frontend & Chiến lược Quản lý Token

Nhiều lập trình viên lầm tưởng bảo mật là việc của Backend. Tuy nhiên, nếu Frontend lưu trữ Token sai cách hoặc hiển thị dữ liệu không an toàn, toàn bộ hệ thống vẫn có thể bị xâm nhập. Ở mức độ Enterprise, bạn phải nắm rõ các lỗ hổng phổ biến và cách phòng tránh.

---

## 1. Lưu trữ Access Token: LocalStorage vs HTTP-Only Cookies

Khi đăng nhập thành công, Server sẽ trả về một Access Token (thường là JWT). Frontend phải lưu Token này lại để đính kèm vào các Request tiếp theo.

### Sai lầm phổ biến: Lưu Token vào `localStorage`
Rất nhiều tutorial trên mạng dạy bạn làm như sau:
```javascript
localStorage.setItem('token', accessToken);
```
**Lý do không an toàn:** Bất kỳ đoạn mã JavaScript nào chạy trên trang web của bạn (kể cả mã độc từ một thư viện NPM dỏm bạn vô tình cài vào) đều có thể truy cập `localStorage` bằng lệnh `localStorage.getItem('token')` và gửi nó về server của hacker. Lỗ hổng này gọi là **XSS (Cross-Site Scripting)**.

### Chuẩn Enterprise: HTTP-Only Cookies
Cách bảo mật nhất hiện nay là Backend phải thiết lập Access Token (và Refresh Token) vào một Cookie có cờ `HttpOnly`. 
- **`HttpOnly`**: Cookie này sẽ KHÔNG THỂ bị đọc bởi bất kỳ mã JavaScript nào. Trình duyệt tự động đính kèm Cookie này vào mỗi request gửi lên đúng domain đó. Hacker có chạy được mã độc trên web của bạn cũng không thể ăn cắp được Token.
- **`Secure`**: Đảm bảo Cookie chỉ gửi qua mạng HTTPS.
- **`SameSite=Lax` hoặc `Strict`**: Giúp phòng chống tấn công **CSRF**.

*Trách nhiệm của Frontend trong kiến trúc này:* Rất nhàn! Bạn không cần lấy token và set Header `Authorization: Bearer ...` thủ công nữa, chỉ cần cấu hình thư viện fetch (vd Axios) gửi kèm thông tin xác thực (credentials).

```javascript
// Cấu hình Axios gửi kèm HttpOnly Cookie tự động
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.congty.com',
  withCredentials: true, // Quan trọng: Báo cho trình duyệt gửi kèm Cookie
});
```

---

## 2. Tấn công XSS (Cross-Site Scripting)

XSS xảy ra khi Hacker chèn được một đoạn mã JavaScript độc hại vào trang web của bạn.
Ví dụ: Ở một khung bình luận, hacker gõ `<script>alert('Bị hack')</script>`.

### May mắn thay: React tự động chống XSS
React sẽ tự động mã hóa (escape) tất cả các dữ liệu dạng text trước khi render ra màn hình. Đoạn script trên sẽ chỉ hiển thị dưới dạng chuỗi chữ bình thường, không bị thực thi.

```tsx
// React ĐÃ BẢO VỆ bạn ở đây
const comment = "<script>alert('Bị hack')</script>";
return <div>{comment}</div>; 
```

### Kẽ hở: Lạm dụng `dangerouslySetInnerHTML`
Nếu bạn bắt buộc phải render nội dung HTML phong phú (Rich Text) từ database (ví dụ bài viết từ CkEditor), bạn phải dùng `dangerouslySetInnerHTML`. Lúc này React SẼ KHÔNG bảo vệ bạn nữa.

```tsx
// ❌ CỰC KỲ NGUY HIỂM: Rất dễ dính XSS nếu bài viết chứa mã độc
return <div dangerouslySetInnerHTML={{ __html: articleContent }} />;
```

**Cách phòng vệ chuẩn:** Luôn dùng thư viện sanitize (làm sạch) như **DOMPurify** trước khi truyền vào `dangerouslySetInnerHTML`.

```tsx
import DOMPurify from 'dompurify';

export function Article({ content }) {
  // Loại bỏ mọi thẻ <script> và các thuộc tính nguy hiểm (onload, onerror)
  const safeContent = DOMPurify.sanitize(content);
  
  return <div dangerouslySetInnerHTML={{ __html: safeContent }} />;
}
```

---

## 3. Tấn công CSRF (Cross-Site Request Forgery)

Giả sử bạn vừa đăng nhập vào trang ngân hàng `bank.com` (trình duyệt đã lưu Cookie). Bạn mở một tab khác vào trang `web-phim-lau.com`. Trang web lậu đó ngầm gửi một request POST sang `bank.com/transfer` để chuyển tiền. Vì trình duyệt luôn tự đính kèm Cookie, ngân hàng tưởng đó là lệnh của bạn!

**Cách Frontend phối hợp Backend chống CSRF:**
1. **Dùng SameSite Cookie:** Backend set `SameSite=Lax` cho Token Cookie. Trình duyệt sẽ từ chối gửi Cookie nếu request xuất phát từ tên miền lạ (`web-phim-lau.com`).
2. **CSRF Token:** Backend trả về một chuỗi `csrf-token` ngẫu nhiên. Frontend phải lấy chuỗi này (thường nằm ở thẻ `<meta>` hoặc qua 1 endpoint GET) và gắn vào Header `X-CSRF-Token` ở mọi request POST/PUT/DELETE.

---

## Tóm tắt Actionable
1. Đừng bao giờ lưu Access Token / Refresh Token vào `localStorage` hay `sessionStorage`. Hãy thúc đẩy Backend chuyển sang dùng **HttpOnly Cookies**.
2. Nếu dự án bắt buộc phải lưu ở LocalStorage, hãy setup **Thời gian sống (TTL) của Access Token thật ngắn** (VD: 5-15 phút) và xoay vòng bằng Refresh Token.
3. Luôn bọc `DOMPurify` trước khi sử dụng `dangerouslySetInnerHTML`.
4. Không bao giờ chạy `eval()` hoặc gán trực tiếp dữ liệu từ API vào URL (ví dụ thẻ `<a href={userWebsite}>`) mà không kiểm tra (hacker có thể truyền vào `javascript:alert(1)`).
