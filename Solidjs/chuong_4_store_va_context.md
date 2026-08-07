# Chương 4: Quản lý State Nâng Cao (Store & Context)

Nếu bạn xây dựng một ứng dụng phức tạp, việc dùng quá nhiều `createSignal` đơn lẻ sẽ khiến code trở nên lộn xộn. SolidJS cung cấp **Store** để quản lý các Object/Array phức tạp, và **Context** để truyền dữ liệu toàn cục.

## 1. Tìm hiểu về Store (`createStore`)

`createStore` trả về một mảng chứa State Object và một hàm Setter (giống như `createSignal`). Tuy nhiên, hàm Setter của Store cực kỳ mạnh mẽ, cho phép bạn cập nhật chính xác từng trường (field) lồng sâu bên trong object mà không cần phải "copy-paste" lại toàn bộ object như React.

```jsx
import { createStore } from "solid-js/store";

function UserProfile() {
  const [user, setUser] = createStore({
    id: 1,
    name: "John Doe",
    address: {
      city: "Hanoi",
      street: "Le Loi"
    }
  });

  const updateCity = () => {
    // Cập nhật lồng sâu cực kỳ đơn giản!
    // Trỏ đường dẫn: "address" -> "city" -> Giá trị mới
    setUser("address", "city", "Ho Chi Minh");
  };

  return (
    <div>
      <p>Name: {user.name}</p>
      <p>City: {user.address.city}</p>
      <button onClick={updateCity}>Chuyển thành phố</button>
    </div>
  );
}
```
*Lưu ý: Bạn KHÔNG CẦN dùng hàm (như `user()`) để lấy dữ liệu từ Store. Bạn truy cập trực tiếp bằng `user.name`. Việc tracking vẫn tự động diễn ra nhờ vào cơ chế Proxy của Solid.*

## 2. Thay đổi mảng với Store

Nếu State của bạn là một mảng Todo, bạn có thể cập nhật cực kỳ nhanh gọn.

```jsx
import { createStore } from "solid-js/store";
import { For } from "solid-js";

function TodoApp() {
  const [todos, setTodos] = createStore([
    { id: 1, text: "Học HTML", done: true },
    { id: 2, text: "Học SolidJS", done: false }
  ]);

  const toggleTodo = (id) => {
    // 1. Tìm điều kiện (id match)
    // 2. Tên field muốn update ("done")
    // 3. Hàm callback để lấy giá trị cũ và đảo ngược nó
    setTodos(
      todo => todo.id === id, 
      "done", 
      done => !done
    );
  };

  return (
    <ul>
      <For each={todos}>
        {todo => (
          <li>
            <input 
              type="checkbox" 
              checked={todo.done} 
              onChange={() => toggleTodo(todo.id)} 
            />
            <span style={{ "text-decoration": todo.done ? "line-through" : "none" }}>
              {todo.text}
            </span>
          </li>
        )}
      </For>
    </ul>
  );
}
```

## 3. Cập nhật dạng Mutable với `produce`

Nếu bạn thích viết code theo phong cách cập nhật trực tiếp (mutate) giống như Immer trong React, Solid cung cấp tiện ích `produce`.

```jsx
import { createStore, produce } from "solid-js/store";

function CounterWithProduce() {
  const [state, setState] = createStore({ count: 0, clicks: 0 });

  const handleClick = () => {
    // Thay đổi trực tiếp trên bản sao (draft)
    setState(produce((draft) => {
      draft.count += 5;
      draft.clicks += 1;
    }));
  };

  return <button onClick={handleClick}>Điểm: {state.count} (Click: {state.clicks})</button>;
}
```

## 4. Truyền dữ liệu toàn cục với Context

Để tránh việc truyền Props quá nhiều lớp (Props Drilling), Solid hỗ trợ Context API tương tự React, nhưng nhờ tính phản ứng nguyên thủy, Context trong Solid không bao giờ bị re-render toàn bộ cây component!

```jsx
import { createContext, useContext, createSignal } from "solid-js";

// 1. Khởi tạo Context
const ThemeContext = createContext();

export function ThemeProvider(props) {
  const [theme, setTheme] = createSignal("light");

  const value = {
    theme,
    toggleTheme: () => setTheme(t => t === "light" ? "dark" : "light")
  };

  return (
    <ThemeContext.Provider value={value}>
      {props.children}
    </ThemeContext.Provider>
  );
}

// 2. Sử dụng Context ở component con
export function ThemeToggleButton() {
  const { theme, toggleTheme } = useContext(ThemeContext);

  return (
    <button onClick={toggleTheme}>
      Chủ đề hiện tại: {theme()}
    </button>
  );
}
```
*Bạn có thể bọc `<ThemeProvider>` ở file `index.jsx` gốc để sử dụng cho toàn ứng dụng.*
