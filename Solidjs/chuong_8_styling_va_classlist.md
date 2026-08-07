# Chương 8: Nghệ thuật Styling (CSS và classList)

SolidJS cung cấp các cách tiếp cận cực kỳ thông minh để xử lý giao diện (Styling), đặc biệt là việc tối ưu hóa cách gán các class động (Dynamic classes).

## 1. Sử dụng thuộc tính `style`
Tương tự như React, bạn có thể truyền một Object vào thuộc tính `style`. Khác biệt là SolidJS không bắt buộc bạn phải viết thuộc tính CSS dạng camelCase (như `backgroundColor`). Bạn có thể viết đúng chuẩn CSS (`background-color`).

```jsx
import { createSignal } from "solid-js";

function StyledBox() {
  const [isActive, setIsActive] = createSignal(false);

  return (
    <div
      style={{
        "background-color": isActive() ? "green" : "gray", // Viết chuẩn CSS gốc
        padding: "20px",
        "border-radius": "8px",
        color: "white",
        cursor: "pointer"
      }}
      onClick={() => setIsActive(!isActive())}
    >
      Click để đổi màu
    </div>
  );
}
```

## 2. Dynamic Classes với `classList`
Ở React, khi muốn thêm/bớt class dựa trên biến State, ta thường dùng Template Literals (chuỗi) hoặc thư viện `clsx`.
Ở Solid, bạn có **thuộc tính `classList` được tích hợp sẵn**. Thuộc tính này nhận vào một Object, trong đó keys là tên class, còn values là điều kiện boolean để hiển thị class đó.

```jsx
import { createSignal } from "solid-js";
import "./Button.css"; // Giả sử có chứa các class: .btn, .btn-primary, .disabled

function SmartButton() {
  const [isLoading, setIsLoading] = createSignal(false);

  // classList tự động thêm class "loading" và "disabled" nếu isLoading() là true
  return (
    <button
      class="btn btn-primary" // Class tĩnh dùng "class" (không dùng className)
      classList={{
        "loading": isLoading(),
        "disabled": isLoading()
      }}
      onClick={() => setIsLoading(true)}
    >
      {isLoading() ? "Đang xử lý..." : "Bắt đầu"}
    </button>
  );
}
```
*Lưu ý quan trọng: Solid dùng `class` thay vì `className` như React!*

## 3. Tích hợp CSS Modules
Nếu bạn muốn đóng gói CSS để không bị xung đột tên class, SolidJS hỗ trợ sẵn CSS Modules khi dùng chung với Vite.

Tạo file `Header.module.css`:
```css
.container {
  display: flex;
  justify-content: space-between;
  background: #333;
}
.title {
  color: #fff;
  font-size: 24px;
}
```

Sử dụng trong Component:
```jsx
import styles from "./Header.module.css";

function Header() {
  return (
    <header class={styles.container}>
      <h1 class={styles.title}>Ứng dụng của tôi</h1>
    </header>
  );
}
```

## Tổng kết Chương 8
- Dùng `class` (không dùng `className`).
- Dùng `classList` với object điều kiện để tối ưu các CSS Class động thay vì phải nối chuỗi dài ngoằng.
- CSS Modules được hỗ trợ mặc định. Tên thuộc tính trong thẻ `style` có thể viết chuẩn dấu gạch ngang (`-`) của CSS.
