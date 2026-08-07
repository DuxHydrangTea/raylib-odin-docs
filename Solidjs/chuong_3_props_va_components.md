# Chương 3: Components và Quy tắc xử lý Props

Việc chia nhỏ ứng dụng thành các Component là điều hiển nhiên trong các framework hiện đại. SolidJS cũng sử dụng Components, nhưng cách xử lý **Props** (tham số truyền vào component) thì có một quy tắc sống còn mà bạn phải nhớ.

## 1. Quy tắc vàng: KHÔNG ĐƯỢC Destructure Props

Ở React, chúng ta thường viết như sau:
```jsx
// REACT WAY - KHÔNG DÙNG TRONG SOLID!
function Greeting({ name, age }) {
  return <p>Hello {name}, you are {age}</p>;
}
```

Nếu bạn làm điều này ở SolidJS, **tính phản ứng (reactivity) sẽ bị mất hoàn toàn**.
Lý do: Hàm Component trong Solid chỉ chạy 1 lần. Khi bạn destructure (`{ name } = props`), bạn đang sao chép giá trị tại thời điểm khởi tạo vào một biến tĩnh cục bộ. Nó sẽ không bao giờ được cập nhật!

**Cách đúng trong SolidJS:** Luôn luôn truy cập thuộc tính thông qua biến `props`.

```jsx
import { createSignal } from "solid-js";

function Greeting(props) {
  // Đúng: Thuộc tính props.name sẽ được track tự động bên trong JSX
  return <p>Hello {props.name}!</p>;
}

function App() {
  const [name, setName] = createSignal("World");
  return (
    <div>
      <Greeting name={name()} />
      <button onClick={() => setName("Solid")}>Đổi Tên</button>
    </div>
  );
}
```

## 2. Gán giá trị mặc định: `mergeProps`

Nếu bạn muốn tạo giá trị mặc định cho Props, đừng dùng default parameters của JS (như `props = { name: "Guest" }`). Hãy dùng hàm tiện ích `mergeProps`.

```jsx
import { mergeProps } from "solid-js";

function Profile(rawProps) {
  // Gộp giá trị mặc định vào props một cách an toàn (giữ nguyên tính phản ứng)
  const props = mergeProps({ name: "Guest", role: "User" }, rawProps);

  return (
    <div>
      <h2>{props.name}</h2>
      <p>Chức vụ: {props.role}</p>
    </div>
  );
}
```

## 3. Tách Props: `splitProps`

Khi bạn xây dựng một UI Component (ví dụ một Button tự tạo) và muốn truyền phần lớn props gốc (như `onClick`, `class`, `style`) vào thẻ HTML bên trong, nhưng lại muốn giữ lại vài props riêng biệt để xử lý logic, hãy dùng `splitProps`.

```jsx
import { splitProps } from "solid-js";

function CustomButton(rawProps) {
  // Tách prop 'variant' và 'children' ra thành biến local, 
  // phần còn lại đưa vào biến 'others'.
  const [local, others] = splitProps(rawProps, ["variant", "children"]);

  return (
    <button 
      class={`btn btn-${local.variant || "primary"}`} 
      {...others} // Truyền tất cả các props còn lại (vd: onClick, id, ...)
    >
      {local.children}
    </button>
  );
}
```

## 4. Xử lý Children an toàn: `children()` helper

`props.children` trong Solid có thể là một chuỗi, một hàm, một Component, hoặc một mảng. Việc truy cập trực tiếp `props.children` nhiều lần có thể gây ra việc tạo DOM không mong muốn (nếu `children` là một hàm tạo DOM).

Để giải quyết một cách an toàn và tối ưu, Solid cung cấp helper `children`.

```jsx
import { children, createEffect } from "solid-js";

function Wrapper(props) {
  // Trả về một hàm getter đại diện cho các DOM nodes đã được phân giải (resolved)
  const resolved = children(() => props.children);

  createEffect(() => {
    console.log("Số lượng child nodes:", resolved.toArray().length);
  });

  return (
    <div style={{ border: "2px solid red", padding: "10px" }}>
      {resolved()}
    </div>
  );
}
```

**Tóm tắt Chương 3:**
1. Luôn dùng `props.name`, **tuyệt đối không** `{name}`.
2. Dùng `mergeProps` để đặt giá trị mặc định.
3. Dùng `splitProps` để trích xuất props riêng biệt.
4. Dùng helper `children` khi cần tương tác phức tạp với `props.children`.
