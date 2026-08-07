# Chương 9: Custom Directives (Từ khóa `use:___`)

Một trong những tính năng thú vị và mạnh mẽ nhất của SolidJS là **Custom Directives**. Tính năng này cho phép bạn viết các hàm JavaScript thuần tuý để tương tác trực tiếp với DOM Element tại thời điểm Element đó được render. Nó giúp giữ cho Component của bạn cực kỳ sạch sẽ.

## 1. Directive là gì?

Directive là một hàm bình thường nhận vào 2 tham số:
1. `element`: DOM Element thực tế mà nó được gắn vào.
2. `accessor`: Hàm trả về giá trị mà bạn truyền vào từ khóa `use:` trên thẻ JSX.

Cách sử dụng trong JSX là dùng cú pháp: `use:tên_hàm={giá_trị}`.

## 2. Ví dụ thực tế: Tự động Focus vào Input

Thay vì phải tạo `ref` rồi dùng `onMount` để gọi `ref.focus()` như trong React, với SolidJS bạn có thể làm điều này cực kỳ tinh tế.

```jsx
import { createSignal } from "solid-js";

// Khai báo Directive (chỉ là một hàm bình thường)
function autofocus(el) {
  // Thực thi ngay khi Element được render
  el.focus();
}

function SearchBox() {
  return (
    <div>
      {/* 
        Sử dụng Directive bằng từ khoá 'use:'. 
        (Cần phải khai báo // @ts-ignore hoặc khai báo module Solid nếu dùng TypeScript) 
      */}
      <input type="text" placeholder="Tìm kiếm..." use:autofocus />
    </div>
  );
}
```

## 3. Ví dụ Nâng cao: Click Outside

Một kịch bản rất phổ biến là tắt Dropdown/Popup khi người dùng click ra ngoài phần tử đó. Ta có thể viết một Directive tái sử dụng được ở khắp mọi nơi.

```jsx
import { createSignal, onCleanup, Show } from "solid-js";

// Viết hàm Click Outside Directive
function clickOutside(el, accessor) {
  const onClick = (e) => {
    // Nếu click không nằm trong Element, thì gọi hàm callback từ accessor()
    if (!el.contains(e.target)) {
      accessor()();
    }
  };

  // Lắng nghe sự kiện click trên toàn bộ trình duyệt
  document.body.addEventListener("click", onClick);

  // Quan trọng: Dọn dẹp event listener khi Element bị unmount
  onCleanup(() => {
    document.body.removeEventListener("click", onClick);
  });
}

function UserMenu() {
  const [isOpen, setIsOpen] = createSignal(false);

  return (
    <div style={{ position: "relative" }}>
      {/* Nút bấm không bị dính clickOutside do event sủi bọt (bubbling) có thể cần stopPropagation */}
      <button onClick={(e) => { e.stopPropagation(); setIsOpen(!isOpen()) }}>
        Tài khoản
      </button>

      <Show when={isOpen()}>
        <div 
          use:clickOutside={() => setIsOpen(false)} // Truyền callback đóng Menu
          style={{ position: "absolute", background: "white", border: "1px solid #ccc" }}
        >
          <ul>
            <li>Hồ sơ</li>
            <li>Cài đặt</li>
            <li>Đăng xuất</li>
          </ul>
        </div>
      </Show>
    </div>
  );
}
```

## Tổng kết Chương 9
- Từ khóa `use:directive` giúp đính kèm các hàm xử lý DOM trực tiếp vào thẻ JSX.
- Giảm thiểu việc lạm dụng `ref` và các hiệu ứng `onMount` lằng nhằng trong Component.
- Tuyệt vời cho việc kết hợp với các thư viện JavaScript thuần (Vanilla JS) của bên thứ 3 (ví dụ: đính kèm biểu đồ D3.js hoặc thư viện kéo-thả).
