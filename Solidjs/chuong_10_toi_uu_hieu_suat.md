# Chương 10: Tối ưu Hiệu suất và Các "Cạm bẫy" (Gotchas)

SolidJS vốn dĩ đã cực kỳ nhanh vì nó không sử dụng Virtual DOM, nhưng nếu viết code không đúng cách, bạn vẫn có thể vô tình kích hoạt các chuỗi cập nhật DOM dư thừa hoặc làm mất tính phản ứng.

## 1. Mất tính phản ứng (Reactivity Loss)

Đây là cạm bẫy lớn nhất của các lập trình viên chuyển từ React sang.

❌ **Sai lầm 1: Destructure Props**
Như đã nói ở Chương 3, việc destructure `props` sẽ tách rời giá trị ra khỏi hệ thống theo dõi của Solid. Hãy luôn dùng `props.name`.

❌ **Sai lầm 2: Destructure Signal trả về Object/Array**
Nếu State của bạn là một Object, bạn không thể destructure nó và hy vọng từng trường bên trong giữ được tính phản ứng.
```jsx
// SAI: 
const [user, setUser] = createSignal({ name: "A", age: 10 });
// Việc gọi user() tại đây và lấy ra name, age sẽ tạo ra biến tĩnh.
const { name, age } = user(); 
// <p>{name}</p> sẽ không bao giờ được cập nhật!

// ĐÚNG:
// Trong JSX, hãy viết: <p>{user().name}</p>
```

## 2. Dừng theo dõi với `untrack`

Trong một vài trường hợp (thường là trong `createEffect`), bạn muốn đọc một giá trị của Signal A, nhưng bạn KHÔNG MUỐN `createEffect` đó chạy lại khi Signal A thay đổi (ví dụ: bạn chỉ muốn nó chạy lại khi Signal B thay đổi). 

Lúc này, hãy bọc Signal A vào hàm `untrack`.

```jsx
import { createSignal, createEffect, untrack } from "solid-js";

function Logger() {
  const [a, setA] = createSignal(1);
  const [b, setB] = createSignal(1);

  createEffect(() => {
    // Đọc b() nhưng bọc trong untrack
    const currentB = untrack(() => b());
    
    // Effect này CHỈ chạy lại khi a() thay đổi. Nó mặc kệ sự thay đổi của b().
    console.log(`A vừa thay đổi thành: ${a()}. Giá trị của B hiện tại là: ${currentB}`);
  });

  return (
    <div>
      <button onClick={() => setA(a() + 1)}>Tăng A</button>
      <button onClick={() => setB(b() + 1)}>Tăng B</button>
    </div>
  );
}
```

## 3. Gộp các bản cập nhật bằng `batch`

Khi bạn gọi liên tiếp nhiều hàm `setSignal` khác nhau, SolidJS sẽ ngay lập tức tính toán lại mọi thứ cho TỪNG hàm `set`. Điều này đôi khi làm DOM phải render lại nhiều lần cho cùng một tác vụ. 

Hàm `batch` giúp bạn trì hoãn việc cập nhật DOM cho đến khi tất cả các logic gán giá trị kết thúc.

```jsx
import { createSignal, batch } from "solid-js";

function ResetGame() {
  const [score, setScore] = createSignal(100);
  const [level, setLevel] = createSignal(5);
  const [isGameOver, setIsGameOver] = createSignal(true);

  const reset = () => {
    // Gộp cả 3 thao tác update này thành 1 chu kỳ cập nhật duy nhất!
    batch(() => {
      setScore(0);
      setLevel(1);
      setIsGameOver(false);
    });
  };

  return <button onClick={reset}>Chơi lại từ đầu</button>;
}
```
*Lưu ý: SolidJS đã tự động `batch` các hành động diễn ra bên trong các DOM Events (như `onClick`), nên trong ví dụ trên, dù bạn không dùng `batch` thì nó vẫn gộp. Tuy nhiên, `batch` cực kỳ hữu ích khi bạn gọi các hàm `set` từ các nguồn không đồng bộ như `setTimeout` hoặc Websocket.*

## Tổng kết Khóa Học SolidJS
Chúc mừng bạn đã hoàn thành bộ tài liệu SolidJS Toàn Tập! Bạn đã nắm vững:
1. Cơ chế không dùng Virtual DOM (Chương 1)
2. Control Flow & Component Lifecycle (Chương 2, 3)
3. Advanced State (Chương 4)
4. Fetching & Routing (Chương 5, 6, 7)
5. Styling & Tối ưu hiệu suất (Chương 8, 9, 10)

Giờ là lúc bắt tay vào code các dự án thực tế!
