# Chương 2: Tư duy Component hóa & Nguyên tắc SOLID trong React

Một trong những sai lầm lớn nhất của người mới học React là nhồi nhét mọi thứ vào một Component khổng lồ (God Component). Khi đi làm, code của bạn phải dễ đọc, dễ test và dễ tái sử dụng. Để làm được điều đó, hãy áp dụng nguyên lý SOLID vào việc thiết kế Component.

---

## 1. Single Responsibility Principle (SRP - Đơn trách nhiệm)

Một Component chỉ nên thực hiện **MỘT** nhiệm vụ duy nhất. 
Nếu một Component vừa fetch data, vừa render giao diện phức tạp, vừa xử lý validate form, thì nó đang vi phạm SRP.

**Sai (God Component):**
```tsx
function UserProfile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/user').then(res => res.json()).then(data => {
      setUser(data);
      setLoading(false);
    });
  }, []);

  if (loading) return <Spinner />;

  return (
    <div>
      {/* Vừa render Header, vừa render User Info, vừa render Settings form */}
      <h1>{user.name}</h1>
      <form onSubmit={/* ... */}>
         {/* Hàng chục dòng code form ở đây */}
      </form>
    </div>
  );
}
```

**Đúng (Enterprise Pattern - Smart vs Dumb Components):**
Chúng ta tách ra làm 2 phần: 
- `Container Component (Smart)`: Chỉ lo fetch data và truyền xuống.
- `Presentational Component (Dumb)`: Chỉ lo nhận data (props) và render UI.

```tsx
// 1. Dumb Component: Chỉ lo hiển thị UI
function UserInfoUI({ user, onUpdate }) {
  return (
    <div>
      <h1>{user.name}</h1>
      <UserUpdateForm onSubmit={onUpdate} /> 
    </div>
  );
}

// 2. Smart Component: Chỉ lo Data fetching & Logic
function UserProfileContainer() {
  // Logic fetch data được đưa ra custom hook riêng
  const { data: user, isLoading } = useFetchUser(); 

  const handleUpdate = (newData) => { /* gọi API update */ };

  if (isLoading) return <Spinner />;
  
  return <UserInfoUI user={user} onUpdate={handleUpdate} />;
}
```

---

## 2. Open/Closed Principle (OCP - Mở rộng thì dễ, Sửa đổi thì khó)

Component nên dễ dàng **mở rộng tính năng mới** (Open for extension) mà **không cần sửa lại code cũ** bên trong nó (Closed for modification).

Ví dụ: Bạn có một `Button`. Hôm nay sếp yêu cầu thêm icon bên trái, ngày mai sếp đòi thêm icon bên phải, ngày mốt đòi thêm loading state. Nếu bạn dùng hàng chục câu lệnh `if...else` trong ruột `Button`, nó sẽ rất nát.

**Cách giải quyết: Sử dụng `children` và `Composition` (Lắp ráp)**

```tsx
// Đúng: Thay vì truyền prop iconLeft, iconRight, hãy để người dùng tự quyết định qua children
type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  isLoading?: boolean;
};

function Button({ isLoading, children, className, ...props }: ButtonProps) {
  return (
    <button className={`btn-base ${className}`} disabled={isLoading} {...props}>
      {isLoading ? <SpinnerIcon /> : null}
      {children}
    </button>
  );
}

// Khi sử dụng: Rất linh hoạt mà không cần sửa ruột Button
<Button>Click me</Button>
<Button> <IconLeft /> Click me </Button>
<Button> Click me <IconRight /> </Button>
```

---

## 3. Liskov Substitution Principle (LSP) trong React

Trong React, LSP thường được hiểu là: Component con/mở rộng phải giữ nguyên hợp đồng (contract/props) của phần tử HTML gốc hoặc component cha.

**Ví dụ:** Nếu bạn tạo một Custom Input, nó phải nhận được mọi props mà thẻ `<input>` gốc nhận được (như `onChange`, `onFocus`, `placeholder`, `disabled`). Đừng tự phát minh ra các props khác thay thế.

**Sai:**
```tsx
// Bạn tự nghĩ ra 'onTextChange' thay vì dùng 'onChange' chuẩn
function CustomInput({ onTextChange, hint }) {
  return <input onChange={e => onTextChange(e.target.value)} />
}
```

**Đúng:**
```tsx
// Kế thừa toàn bộ Props của input chuẩn HTML
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  hint?: string;
}

// Dùng forwardRef để tương thích 100% với các thư viện như React Hook Form
const CustomInput = React.forwardRef<HTMLInputElement, InputProps>(
  ({ hint, ...props }, ref) => {
    return (
      <div>
        <input ref={ref} {...props} />
        {hint && <span>{hint}</span>}
      </div>
    );
  }
);
```

---

## 4. Tóm tắt Actionable cho người đi làm
1. **Rule of 3 (Quy tắc số 3):** Nếu một đoạn UI hoặc Logic bị lặp lại ở 3 nơi khác nhau, hãy biến nó thành 1 Custom Hook hoặc 1 UI Component dùng chung (`shared/ui`).
2. **Tách Logic khỏi UI:** Hãy viết **Custom Hooks** (`useUser`, `useCart`) để chứa logic nghiệp vụ, giữ cho file Component `.tsx` của bạn chỉ tập trung vào việc mô tả giao diện.
3. **Ưu tiên Composition hơn Inheritance:** Ở React không dùng Class Kế thừa (Inheritance). Mọi sự mở rộng UI đều thông qua việc truyền `children` hoặc truyền Component dưới dạng props.
