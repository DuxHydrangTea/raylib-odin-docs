# Chương 7: Xử lý Form chuẩn Enterprise (React Hook Form & Zod)

Trong React, thao tác với Form truyền thống (Controlled Components) yêu cầu bạn phải tạo một State cho mỗi Input và liên tục gọi `setState` mỗi khi người dùng gõ phím. Nếu Form có 20 trường, bạn sẽ có 20 lần Re-render trên MỖI LẦN GÕ PHÍM, cực kỳ lag.

Chuẩn mực của Enterprise là sử dụng **Uncontrolled Components** kết hợp với thư viện siêu nhẹ **React Hook Form (RHF)** và thư viện kiểm tra dữ liệu **Zod**.

---

## 1. Tại sao lại là React Hook Form?

- **Zero Re-render:** RHF lưu trữ giá trị của các input vào các `ref` đằng sau hậu trường. Khi bạn gõ phím, component KHÔNG hề bị re-render.
- **Rất nhẹ:** Nhẹ hơn Formik hay Redux Form rất nhiều.
- **Hỗ trợ tối đa:** Dễ dàng kết hợp với các thư viện giao diện như Material-UI, Ant Design (qua Component `<Controller />`).

### Ví dụ Form đơn giản nhất với RHF:

```tsx
import { useForm } from 'react-hook-form';

function SimpleForm() {
  // register: Dùng để gắn vào các thẻ input
  // handleSubmit: Bao bọc hàm xử lý của bạn
  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = (data) => {
    console.log("Dữ liệu form:", data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('username', { required: true })} />
      {errors.username && <span className="error">Tên là bắt buộc</span>}

      <input type="password" {...register('password')} />
      <button type="submit">Submit</button>
    </form>
  );
}
```

---

## 2. Nâng tầm với Zod (Schema Validation)

Validate dữ liệu bằng tay (viết `if (password.length < 8)`) rất dễ sai sót. **Zod** giúp bạn định nghĩa một "khuôn mẫu" (Schema), tự động báo lỗi và **tự động sinh ra kiểu dữ liệu TypeScript** (TypeScript Type Inference).

### Kết hợp RHF và Zod (Combo hoàn hảo):

Bạn cần cài đặt thêm `@hookform/resolvers`.

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

// 1. Định nghĩa Schema bằng Zod
const loginSchema = z.object({
  email: z.string().email({ message: "Email không hợp lệ" }),
  password: z.string().min(8, { message: "Mật khẩu phải từ 8 ký tự" })
});

// 2. Tự động nội suy kiểu dữ liệu cho TypeScript! (Cực hay)
// Type LoginFormValues sẽ có dạng { email: string; password: string }
type LoginFormValues = z.infer<typeof loginSchema>;

export function EnterpriseLoginForm() {
  const { 
    register, 
    handleSubmit, 
    formState: { errors, isSubmitting } 
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema) // Gắn Zod vào RHF
  });

  const onSubmit = async (data: LoginFormValues) => {
    // Lúc này data.email và data.password chắc chắn đã chuẩn 100%
    await api.login(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
      <div>
        <input placeholder="Email" {...register('email')} className="input" />
        {/* RHF tự động lấy câu thông báo lỗi từ Zod */}
        {errors.email && <p className="text-red-500">{errors.email.message}</p>}
      </div>

      <div>
        <input type="password" placeholder="Password" {...register('password')} className="input" />
        {errors.password && <p className="text-red-500">{errors.password.message}</p>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Loading...' : 'Đăng Nhập'}
      </button>
    </form>
  );
}
```

---

## 3. Tích hợp với Thư viện UI (MUI, Ant Design) - `Controller`

Các thư viện giao diện như Material-UI không trả về thẻ `<input>` gốc mà trả về Component ảo. `register` của RHF không cắm trực tiếp vào được. Lúc này bạn phải dùng `<Controller />`.

```tsx
import { useForm, Controller } from 'react-hook-form';
import Select from 'react-select'; // Một thư viện dropdown bên thứ 3

function SelectForm() {
  const { control, handleSubmit } = useForm();

  return (
    <form onSubmit={handleSubmit(data => console.log(data))}>
      <Controller
        name="country"
        control={control}
        rules={{ required: true }}
        render={({ field }) => (
          // field chứa { onChange, onBlur, value, ref }
          <Select 
            {...field} 
            options={[
              { value: 'vn', label: 'Việt Nam' },
              { value: 'us', label: 'Hoa Kỳ' }
            ]} 
          />
        )}
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

---

## Tóm tắt Actionable

1. **Rule of thumb (Quy tắc chung):** Code React chuyên nghiệp là 100% dùng thư viện form (RHF) + thư viện Schema Validation (Zod/Yup). **Tuyệt đối không dùng Controlled State cơ bản** (`useState`, `onChange`) cho form > 2 fields.
2. Zod giúp bạn chỉ phải viết định dạng dữ liệu đúng 1 lần, vừa dùng để Validate lúc gõ, vừa dùng để sinh kiểu (Type) cho TypeScript (SSOT - Single Source of Truth).
3. Nếu phải custom các input phức tạp (như date picker, rich text editor), hãy làm quen với `Controller` hoặc `useController`.
