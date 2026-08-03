# Vấn Đề 9: Giật lag ngẫu nhiên (Garbage Collection Spikes)

**Vấn đề:**
Game chạy mượt 60FPS. Cứ cách 5-10 giây, game lại khựng (đứng hình) mất 0.5 giây. 

**Nguyên nhân:**
Bạn khởi tạo (cấp phát động) quá nhiều dữ liệu rác trong Vòng Lặp.
Ví dụ: `append(&dynamic_array, bullet)` hoặc ghép chuỗi `fmt.tprintf` để vẽ UI mà quên xóa.
Khi RAM bị đầy rác, hệ điều hành hoặc Garbage Collector (C# / Java) sẽ dừng ứng dụng của bạn lại để chạy đi nhặt rác.

**Giải pháp (Odin / C / C++):**
Nguyên tắc vàng: **Không gọi hàm cấp phát động bên trong Game Loop.**
1. Sử dụng mảng tĩnh (Static Arrays) giới hạn dung lượng (vd: `bullets: [1000]Bullet`) thay cho mảng động (Dynamic).
2. Tái sử dụng đối tượng (Object Pooling) thay vì tạo mới.
3. Dùng `context.temp_allocator` cho các chuỗi chữ UI, và GỌI `free_all(context.temp_allocator)` MỖI CUỐI KHUNG HÌNH (Rất quan trọng trong ngôn ngữ Odin).

```odin
for !rl.WindowShouldClose() {
    // ... update ...
    
    // Tạo chuỗi tốn ram
    text := fmt.ctprintf("Điểm số: %d", score) 
    rl.DrawText(text, 10, 10, 20, rl.WHITE)
    
    // Dọn ngay mẻ rác trong frame này (O(1) tốn 0 giây)
    free_all(context.temp_allocator) 
}
```
