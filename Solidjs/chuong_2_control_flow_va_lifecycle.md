# Chương 2: Luồng Điều Khiển (Control Flow) & Lifecycle

Ở React, chúng ta dùng các cú pháp JavaScript thuần túy như `.map()` để render danh sách, hay dùng `if...else` / `&&` / `? :` để render theo điều kiện. Tuy nhiên, ở SolidJS, do component chỉ chạy duy nhất 1 lần, nếu chúng ta dùng `.map()` thuần túy, những phần tử DOM bên trong sẽ không tự cập nhật một cách tối ưu.

Để giải quyết vấn đề này, Solid cung cấp các Component **Control Flow** chuyên biệt.

## 1. Hiển thị theo điều kiện: `<Show>`

Thay vì dùng `&&` hay `? :`, bạn nên dùng thẻ `<Show>`. Thẻ này nhận vào một `when` (thường là một giá trị phản ứng - signal), và nó sẽ chỉ mount/unmount component bên trong khi giá trị `when` thay đổi, mà không cần phải render lại phần DOM bên ngoài.

```jsx
import { createSignal, Show } from "solid-js";

function LoginStatus() {
  const [isLoggedIn, setIsLoggedIn] = createSignal(false);

  return (
    <div>
      <Show 
        when={isLoggedIn()} 
        fallback={<button onClick={() => setIsLoggedIn(true)}>Đăng nhập</button>}
      >
        <p>Chào mừng bạn đã trở lại!</p>
        <button onClick={() => setIsLoggedIn(false)}>Đăng xuất</button>
      </Show>
    </div>
  );
}
```

## 2. Render danh sách: `<For>` và `<Index>`

Khi render một mảng dữ liệu có thể thay đổi, **tuyệt đối không dùng `.map()`**. Hãy dùng `<For>`.
`<For>` sẽ tự động ánh xạ dữ liệu và **chỉ tạo mới hoặc xóa đi DOM của phần tử bị thay đổi**, giữ nguyên các phần tử khác. Khác với React, SolidJS KHÔNG cần thuộc tính `key`.

```jsx
import { createSignal, For } from "solid-js";

function TodoList() {
  const [todos, setTodos] = createSignal([
    { id: 1, text: "Học SolidJS" },
    { id: 2, text: "Làm project thực tế" }
  ]);

  return (
    <ul>
      <For each={todos()}>
        {(todo, index) => (
          <li>
            #{index() + 1}: {todo.text}
          </li>
        )}
      </For>
    </ul>
  );
}
```
*Lưu ý: Tham số thứ 2 của hàm callback trong `<For>` là `index`. Nó là một Signal! Do đó phải gọi `index()`.*

Nếu mảng của bạn là một mảng các kiểu dữ liệu nguyên thủy (như số hoặc chuỗi), bạn nên dùng `<Index>` thay vì `<For>` để tối ưu hóa việc so sánh.

## 3. Rẽ nhánh nhiều điều kiện: `<Switch>` và `<Match>`

Tương tự như cấu trúc `switch-case` trong JavaScript.

```jsx
import { createSignal, Switch, Match } from "solid-js";

function TrafficLight() {
  const [color, setColor] = createSignal("red");

  return (
    <div>
      <Switch fallback={<p>Đèn hỏng!</p>}>
        <Match when={color() === "red"}>
          <p style={{ color: "red" }}>Dừng lại!</p>
        </Match>
        <Match when={color() === "yellow"}>
          <p style={{ color: "orange" }}>Chậm lại!</p>
        </Match>
        <Match when={color() === "green"}>
          <p style={{ color: "green" }}>Đi tiếp!</p>
        </Match>
      </Switch>
    </div>
  );
}
```

## 4. Vòng đời (Lifecycle) của Component

Vì Component trong Solid chỉ chạy đúng 1 lần, vòng đời của nó cực kỳ đơn giản: **Khởi tạo** (khi hàm chạy) -> **Mount** (khi gắn vào DOM) -> **Unmount** (khi bị gỡ khỏi DOM).

Solid cung cấp 2 hàm chính: `onMount` và `onCleanup`.

```jsx
import { createSignal, onMount, onCleanup } from "solid-js";

function Timer() {
  const [time, setTime] = createSignal(0);

  onMount(() => {
    // Chạy MỘT LẦN duy nhất khi component được gắn vào DOM
    const interval = setInterval(() => {
      setTime(t => t + 1);
    }, 1000);

    // Dọn dẹp khi component bị xóa khỏi DOM
    onCleanup(() => {
      clearInterval(interval);
      console.log("Timer đã được dọn dẹp!");
    });
  });

  return <p>Thời gian: {time()}s</p>;
}
```
Khác với `useEffect` của React (vừa xử lý side effect, vừa dọn dẹp, vừa chạy lại khi deps đổi), trong SolidJS, `onMount` thực chất là một `createEffect` không tự động tracking signal nào cả. Còn `onCleanup` có thể gọi ở bất kỳ đâu (kể cả bên trong `createEffect` thông thường để dọn dẹp effect cũ trước khi chạy effect mới).
