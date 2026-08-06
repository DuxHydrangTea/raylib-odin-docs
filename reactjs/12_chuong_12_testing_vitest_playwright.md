# Chương 12: Chiến lược Testing (Kiểm thử) cho React App

Trong các startup nhỏ chạy đua với deadline, người ta thường bỏ qua viết Test. Nhưng ở quy mô Enterprise, khi số lượng dòng code lên tới hàng trăm ngàn, việc bạn sửa một file Component A có thể làm hỏng Component B (gọi là Bug Regression). 

Để ban đêm có thể ngủ ngon sau mỗi lần Deploy, dự án của bạn BẮT BUỘC phải có Testing.

---

## 1. Kim tự tháp Testing (Testing Pyramid)

Không phải cái gì cũng cần test giống nhau. Chúng ta tuân theo kim tự tháp:
- **Unit Testing (Test Đơn vị - 70%):** Chạy cực nhanh (chưa tới 1 giây), test từng hàm logic nhỏ (Ví dụ: Hàm format tiền tệ).
- **Integration Testing (Test Tích hợp - 20%):** Kiểm tra xem Component UI và hàm Fetch API có hoạt động ăn ý với nhau không.
- **E2E Testing (End-to-End - 10%):** Máy tính sẽ tự bật trình duyệt Chrome lên, click chuột, gõ phím y như người dùng thật. Chạy rất chậm (vài phút) nhưng là thứ chân thực nhất.

---

## 2. Unit Test & Integration Test với Vitest + React Testing Library

Hiện nay, **Vitest** đang thay thế dần Jest vì tốc độ cấu hình và thực thi cực nhanh (nhất là trong dự án dùng Vite). 
Để test UI component, chúng ta dùng **React Testing Library (RTL)**.

RTL khuyến khích chúng ta test ứng dụng theo cách người dùng nhìn thấy nó (Test Hành Vi), chứ không phải test theo code bên trong (State, Class name).

### Ví dụ Integration Test (Button thay đổi giá trị)
```tsx
// Counter.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Counter } from './Counter';

describe('Counter Component', () => {
  it('nên hiển thị giá trị 0 ban đầu', () => {
    // 1. Render Component ra màn hình ảo
    render(<Counter />);
    
    // 2. Tìm kiếm phần tử chứa chữ '0'
    const countElement = screen.getByText('0');
    
    // 3. Khẳng định (Expect) phần tử đó phải tồn tại
    expect(countElement).toBeInTheDocument();
  });

  it('nên tăng lên 1 khi người dùng bấm nút Tăng', () => {
    render(<Counter />);
    
    // 1. Tìm nút dựa theo Text mà người dùng nhìn thấy
    const button = screen.getByRole('button', { name: /Tăng/i });
    
    // 2. Giả lập hành động bấm chuột
    fireEvent.click(button);
    
    // 3. Khẳng định số 1 hiện ra màn hình
    expect(screen.getByText('1')).toBeInTheDocument();
  });
});
```

*Triết lý của RTL:* "The more your tests resemble the way your software is used, the more confidence they can give you." (Test càng giống cách phần mềm được sử dụng, độ tin cậy càng cao).

---

## 3. End-to-End (E2E) Test với Playwright

**Playwright** (Của Microsoft) đang nổi lên mạnh mẽ và đánh bại Cypress nhờ hỗ trợ đa trình duyệt cực tốt và tốc độ thực thi song song (Parallel) đáng nể.

E2E Test không quan tâm bạn viết React, Vue hay HTML thuần. Nó chỉ quan tâm kết quả cuối cùng.

### Ví dụ Test Luồng Đăng nhập:
```typescript
// tests/login.spec.ts
import { test, expect } from '@playwright/test';

test('Người dùng đăng nhập thành công', async ({ page }) => {
  // 1. Điều hướng trình duyệt thật đến trang login
  await page.goto('http://localhost:3000/login');

  // 2. Gõ tài khoản và mật khẩu
  await page.fill('input[name="email"]', 'admin@congty.com');
  await page.fill('input[name="password"]', 'matkhau123');

  // 3. Bấm nút Submit
  await page.click('button[type="submit"]');

  // 4. Đợi trình duyệt chuyển hướng và xác nhận xem đã vào Dashboard chưa
  await expect(page).toHaveURL('http://localhost:3000/dashboard');
  
  // 5. Kiểm tra có chữ "Chào mừng admin" không
  await expect(page.locator('h1')).toContainText('Chào mừng admin');
});
```
*Lưu ý: E2E thường được gắn vào hệ thống CI/CD (GitHub Actions) để chạy tự động mỗi khi có ai đó Push code lên nhánh `main`.*

---

## 4. Tóm tắt Actionable cho người đi làm

1. Đừng cố gắng đạt **100% Code Coverage** (Tỷ lệ bao phủ code). Điều đó rất tốn thời gian và vô nghĩa. Hãy đặt mục tiêu 70-80% cho các logic nghiệp vụ quan trọng (Tính tiền, Phân quyền, Các hàm tiện ích dùng chung).
2. Khi test UI bằng React Testing Library, hãy luôn tìm phần tử (element) thông qua thuộc tính **`aria-role`** (vd: `getByRole('button')`) hoặc **Label** thay vì dùng class name (`.btn-red`). Nếu sau này bạn đổi class sang màu xanh, Test của bạn sẽ không bị fail oan uổng.
3. Nếu nguồn lực team hạn hẹp, hãy ưu tiên viết một vài kịch bản **E2E Test (Playwright)** cho các luồng sống còn (Happy Path) như Đăng nhập, Thanh toán. Nó mang lại giá trị bảo vệ cao nhất với công sức bỏ ra ít nhất.
