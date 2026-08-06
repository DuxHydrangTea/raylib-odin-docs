# Chương 5: Xử lý Server State với TanStack Query (React Query)

Hơn 80% state trong các ứng dụng web thực chất là **Server State** (Dữ liệu fetch từ database/API). Quản lý Server State bằng `useEffect` và `useState` thủ công là một thiết kế tồi vì bạn phải tự xử lý loading, error, caching, deduplication (hủy request trùng), re-validation.

**TanStack Query (React Query)** là thư viện tiêu chuẩn của ngành để giải quyết bài toán này.

---

## 1. Vấn đề của cách làm cũ (fetch trong useEffect)

Khi bạn tự viết logic fetch data bằng `useEffect`:
- **Không có Cache:** Mỗi lần Component mount, nó lại gọi API, bất chấp dữ liệu cũ vẫn còn xài được.
- **Race conditions:** Nếu người dùng click liên tục, request gửi sau có thể trả về trước request gửi trước, gây lỗi hiển thị.
- **Trùng lặp API:** Nếu có 3 component cùng gọi 1 API, trình duyệt sẽ gửi đi 3 request giống hệt nhau.

---

## 2. Giải pháp với TanStack Query: `useQuery`

React Query quản lý dữ liệu dựa trên **QueryKey** (một mảng khóa). Bất cứ lúc nào QueryKey giống nhau được gọi, React Query sẽ trả về dữ liệu cache ngay lập tức nếu có, và tự động gọi ngầm API để lấy dữ liệu mới (Stale-while-revalidate).

### Cách sử dụng chuẩn xác (Đưa ra Custom Hook):

Đừng viết trực tiếp `useQuery` trong file giao diện. Hãy gom nó vào một Custom Hook ở layer `features` hoặc `api`.

```tsx
// src/features/users/api/useUsers.ts
import { useQuery } from '@tanstack/react-query';
import { api } from '@/shared/api';

const fetchUsers = async (page: number) => {
  const { data } = await api.get(`/users?page=${page}`);
  return data;
};

// Đóng gói logic thành Custom Hook
export const useUsers = (page: number) => {
  return useQuery({
    queryKey: ['users', { page }], // Phải bao gồm cả biến số vào mảng key
    queryFn: () => fetchUsers(page),
    staleTime: 5 * 60 * 1000, // Dữ liệu sẽ "tươi" trong 5 phút, không gọi lại API vô ích
  });
};
```

**Ở Component:**
```tsx
function UserList({ page }) {
  // Rất gọn gàng!
  const { data, isLoading, isError } = useUsers(page);

  if (isLoading) return <SkeletonList />;
  if (isError) return <ErrorMessage />;

  return <ul>{data.map(user => <li key={user.id}>{user.name}</li>)}</ul>;
}
```

---

## 3. Thực hiện thay đổi dữ liệu: `useMutation`

Nếu `useQuery` dùng để **LẤY** dữ liệu (GET), thì `useMutation` dùng để **THAY ĐỔI** dữ liệu (POST, PUT, DELETE).

### Mutation cơ bản + Tự động làm mới dữ liệu
Khi tạo mới user thành công, bạn muốn danh sách user tự động tải lại? Rất dễ dàng với `invalidateQueries`.

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/shared/api';

export const useCreateUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newUser: { name: string }) => api.post('/users', newUser),
    onSuccess: () => {
      // Khi thành công, báo cho React Query biết data của key ['users'] đã cũ (stale)
      // React Query sẽ tự động gọi lại API để fetch list user mới ngay lập tức!
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
    onError: (error) => {
      // Show thông báo lỗi
      toast.error(error.message);
    }
  });
};
```

### Optimistic Updates (Cập nhật lạc quan - Nâng cao)
Khi người dùng bấm "Like" một bài viết, họ muốn thấy biểu tượng chuyển sang màu đỏ NGAY LẬP TỨC chứ không phải đợi API báo thành công (delay 500ms). Đây gọi là Optimistic Update.

```tsx
useMutation({
  mutationFn: (postId: string) => api.post(`/posts/${postId}/like`),
  
  // Chạy ngay khi hàm mutationFn được gọi (chưa biết API trả về gì)
  onMutate: async (postId) => {
    // 1. Dừng ngay các fetch khác đang chạy về bài viết này để tránh ghi đè
    await queryClient.cancelQueries({ queryKey: ['posts', postId] });

    // 2. Lưu lại data cũ để fallback
    const previousPost = queryClient.getQueryData(['posts', postId]);

    // 3. Cập nhật thẳng vào cache React Query, UI sẽ đổi ngay lập tức
    queryClient.setQueryData(['posts', postId], (old: any) => ({
      ...old,
      likes: old.likes + 1,
      hasLiked: true
    }));

    // 4. Trả về data cũ để dùng nếu lỡ API bị lỗi
    return { previousPost };
  },
  
  // Nếu API bị lỗi (Mất mạng, v.v...)
  onError: (err, postId, context) => {
    // Rollback lại data cũ trước khi Like
    queryClient.setQueryData(['posts', postId], context?.previousPost);
  },
  
  // Bất kể thành công hay thất bại, fetch lại cho chắc chắn
  onSettled: (data, error, postId) => {
    queryClient.invalidateQueries({ queryKey: ['posts', postId] });
  }
});
```

---

## Tóm tắt Actionable
1. Bỏ ngay việc dùng `useEffect` để fetch data trong các dự án mới.
2. Quản lý chặt chẽ **QueryKey**. QueryKey là mảng, nên các giá trị phụ thuộc (id, page, filter...) phải được đưa vào mảng này.
3. Phân biệt rõ `staleTime` (thời gian dữ liệu được coi là mới, không cần gọi lại API) và `gcTime/cacheTime` (thời gian giữ rác trong bộ nhớ sau khi component bị hủy). Thường set `staleTime` > 0 (vd: 1 phút) để tiết kiệm băng thông.
