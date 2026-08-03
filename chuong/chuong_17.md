# Chương 17: Hoạt ảnh Xương (Skeletal Animation 2D)

SpriteSheet là cách làm truyền thống: Mỗi khung hình của nhân vật là một bức ảnh vẽ sẵn. 
* Nhược điểm: Nếu nhân vật có 20 động tác, bạn phải vẽ hàng trăm bức ảnh. Rất tốn công họa sĩ và cực kỳ tốn RAM để load đống ảnh đó. Bạn cũng không thể thay đổi vũ khí trên tay nhân vật (vì ảnh vũ khí dính liền với ảnh tay).

Giải pháp hiện đại: **Skeletal Animation (Hoạt ảnh xương)**.

---

## 1. Nguyên lý hoạt động

Thay vì vẽ nguyên con nhân vật, bạn yêu cầu họa sĩ vẽ rời từng bộ phận: 1 cái đầu, 1 thân mình, 2 bắp tay, 2 cẳng tay, 2 bàn chân... thành các file `.png` nhỏ xíu.
Sau đó, bạn đưa chúng vào phần mềm chuyên dụng như **Spine 2D** hoặc **DragonBones (Miễn phí)**.
Bạn gắn các mảnh ảnh này vào một "khung xương ảo", và tạo chuyển động bằng cách xoay các khớp xương.

Khi xuất file, phần mềm chỉ trả về:
1. Một file ảnh nén nhỏ xíu (Atlas) chứa các bộ phận rời rạc.
2. Một file `.json` chứa toán học (Tọa độ, góc xoay của từng cục xương ở từng khung hình).

## 2. Ưu điểm vượt trội

* **Siêu nhẹ:** Game giảm dung lượng ảnh từ 100MB xuống còn 5MB.
* **Siêu mượt:** Nhờ việc tính toán góc xoay liên tục (Interpolation), hoạt ảnh có thể chạy ở 60FPS hoặc 144FPS mượt mà (SpriteSheet thường chỉ có 12-24 FPS).
* **Đổi đồ dễ dàng (Attachments):** Vì thanh kiếm là một mảnh `.png` rời dính vào "khớp tay", bạn có thể dễ dàng thay file ảnh thanh kiếm gỗ bằng kiếm sáng rực bằng đúng 1 dòng code.
* **Inverse Kinematics (IK):** Nhân vật có thể tự động bẻ cong đầu gối để chân luôn đặt đúng mặt đất dốc (không bị lơ lửng).

## 3. Tích hợp vào Raylib + Odin

Để chạy file Spine, bạn không dùng `DrawTexture` nữa. Bạn cần tìm một thư viện đọc Spine (Spine Runtime) hỗ trợ ngôn ngữ C, sau đó gọi nó thông qua tính năng C-binding của Odin.

Khi đó, code của bạn sẽ trông như thế này:

```odin
// (Ví dụ mã giả định)
skeleton := spine.load_skeleton("hero.json", "hero.atlas")

// Đổi hiệu ứng
spine.set_animation(skeleton, "run", loop = true)

for !rl.WindowShouldClose() {
    dt := rl.GetFrameTime()
    
    // Cập nhật toán học các khớp xương
    spine.update(skeleton, dt)
    
    rl.BeginDrawing()
        // Hàm vẽ chuyên dụng của thư viện sẽ duyệt qua từng mảnh xương
        // và gọi rl.DrawTexturePro() để vẽ ráp lại thành nhân vật
        spine.draw(skeleton)
    rl.EndDrawing()
}
```

Đây là công nghệ bắt buộc phải biết nếu bạn muốn xin việc vào các công ty sản xuất game 2D chuyên nghiệp!
