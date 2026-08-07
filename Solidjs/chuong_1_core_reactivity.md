# Chương 1: Kiến trúc Cốt lõi & Reactivity (Tính Phản Ứng)

> **Thông tin Tài liệu:**
> - Viết ngày: 07/08/2026
> - Phiên bản Node.js: v24.16.0
> - Phiên bản npm: v11.13.0
> - Phiên bản SolidJS: v1.9.14

SolidJS thoạt nhìn có cú pháp rất giống ReactJS (cũng sử dụng JSX), nhưng bên dưới lớp vỏ đó là một cơ chế hoạt động hoàn toàn khác biệt. SolidJS **không sử dụng Virtual DOM (VDOM)**.

Thay vì chạy lại toàn bộ Component mỗi khi State thay đổi, SolidJS biên dịch JSX trực tiếp thành các thao tác cập nhật DOM nguyên thủy (native DOM updates). Component của SolidJS thực chất chỉ là một hàm chạy duy nhất một lần để khởi tạo giao diện.

## 1. Mảnh ghép đầu tiên: Signals (`createSignal`)

`Signal` là nền tảng cốt lõi của tính phản ứng trong Solid. Nó chứa một giá trị và có khả năng thông báo cho hệ thống mỗi khi giá trị đó thay đổi.

```jsx
import { createSignal } from "solid-js";
import { render } from "solid-js/web";

function Counter() {
  // createSignal trả về mảng 2 phần tử: [getter, setter]
  const [count, setCount] = createSignal(0);

  // Component này chỉ được gọi (chạy) ĐÚNG 1 LẦN.
  console.log("Component Counter khởi tạo!");

  return (
    <div>
      {/* Để lấy giá trị, ta phải GỌI HÀM getter: count() */}
      <p>Số lần click: {count()}</p>
      
      {/* Khi click, chỉ duy nhất text của thẻ <p> ở trên được cập nhật */}
      <button onClick={() => setCount(count() + 1)}>
        Tăng giá trị
      </button>
    </div>
  );
}

// render(() => <Counter />, document.getElementById("app"));
```

**Sự khác biệt với React `useState`:**
- Ở React, `count` là một biến (variable). Mỗi khi cập nhật, React gọi lại *toàn bộ* function `Counter`.
- Ở Solid, `count` là một HÀM (function getter). Khi bạn gọi `count()`, Solid sẽ tự động "theo dõi" (track) xem `count` đang được dùng ở đâu (trong trường hợp này là bên trong thẻ `<p>`). Khi `setCount` được gọi, Solid chỉ cập nhật đúng cái `<p>` đó, function `Counter` không bao giờ chạy lại!

## 2. Derived State: Memos (`createMemo`)

Đôi khi bạn cần tính toán một giá trị dựa trên các Signal khác. Thay vì tính toán lại mỗi khi render (dù không cần thiết), Solid cung cấp `createMemo` để lưu trữ bộ đệm (cache) giá trị tính toán. Memo chỉ chạy lại khi Signal phụ thuộc của nó thay đổi.

```jsx
import { createSignal, createMemo } from "solid-js";

function FibonacciCalculator() {
  const [num, setNum] = createSignal(10);

  // Tính toán tốn kém, chỉ chạy lại khi num() thay đổi
  const fib = createMemo(() => {
    console.log("Đang tính toán Fibonacci...");
    const calculate = (n) => (n <= 1 ? n : calculate(n - 1) + calculate(n - 2));
    return calculate(num());
  });

  return (
    <div>
      <input 
        type="number" 
        value={num()} 
        onInput={(e) => setNum(parseInt(e.target.value, 10))} 
      />
      {/* Gọi memo như một hàm getter thông thường */}
      <p>Giá trị Fibonacci: {fib()}</p>
    </div>
  );
}
```
*Ghi chú: Memo bản chất cũng là một Signal (read-only), do đó bạn cũng cần gọi nó bằng dấu ngoặc đơn `fib()`.*

## 3. Side Effects (`createEffect`)

`createEffect` được dùng để thực hiện các tác vụ phụ (như gọi API, thao tác DOM thủ công, hay in log) khi dữ liệu thay đổi. 

SolidJS tự động theo dõi (auto-track) các Signal bên trong `createEffect`. Bạn không cần phải khai báo "dependency array" như trong React `useEffect`.

```jsx
import { createSignal, createEffect } from "solid-js";

function AutoTracker() {
  const [firstName, setFirstName] = createSignal("John");
  const [lastName, setLastName] = createSignal("Doe");

  // Effect sẽ TỰ ĐỘNG chạy lại mỗi khi firstName() hoặc lastName() thay đổi
  createEffect(() => {
    console.log(`Tên đầy đủ hiện tại là: ${firstName()} ${lastName()}`);
  });

  return (
    <div>
      <input value={firstName()} onInput={(e) => setFirstName(e.target.value)} />
      <input value={lastName()} onInput={(e) => setLastName(e.target.value)} />
    </div>
  );
}
```

## Tổng kết Chương 1
- **Component chạy 1 lần:** Không bao giờ lo lắng về những lần re-render dư thừa.
- **Signal (`createSignal`):** Hàm chứa dữ liệu `[get, set]`. Phải dùng dấu `()` để lấy giá trị.
- **Memo (`createMemo`):** Dùng cho dữ liệu phát sinh cần tính toán nặng.
- **Effect (`createEffect`):** Phản ứng tự động không cần mảng phụ thuộc (dependency array).
