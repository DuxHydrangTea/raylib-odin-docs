# Vấn Đề 18: Bấm xuyên giao diện (UI Click-Through)

**Vấn đề:**
Người chơi nhấp chuột vào nút "Mở kho đồ" trên UI. Khổ nỗi, ngay bên dưới nút đó trong không gian 2D lại có một con quái vật. Kết quả: Kho đồ được mở ra, đồng thời súng cũng nã đạn luôn vào con quái vật.

**Nguyên nhân:**
Hệ thống UI và Hệ thống Gameplay cùng bắt (Listen) sự kiện `IsMousePressed(.LEFT)`. Không có thứ tự ưu tiên nào giữa chúng.

**Giải pháp:**
Cần xây dựng một hệ thống **Tiêu thụ Sự kiện (Event Consumption)** hoặc ưu tiên xử lý luồng từ UI xuống Gameplay.
Nếu chuột đang nằm trên UI (Hovering), chặn đứng không cho phép code Gameplay nhận lệnh bắn.

```odin
// Vùng kiểm tra UI
is_mouse_over_ui := false
if rl.CheckCollisionPointRec(rl.GetMousePosition(), btn_rect) {
    is_mouse_over_ui = true
    if rl.IsMouseButtonPressed(.LEFT) {
        open_inventory()
    }
}

// Vùng xử lý Gameplay (Phải check điều kiện UI trước!)
if !is_mouse_over_ui {
    // Chỉ cho phép bắn súng nếu chuột không bấm vào bất kỳ UI nào
    if rl.IsMouseButtonPressed(.LEFT) {
        fire_weapon()
    }
}
```
*(Trong các hệ thống lớn, người ta thiết kế `Event.handled = true` để nổi bọt (Bubble up) nhằm triệt tiêu sự kiện).*
