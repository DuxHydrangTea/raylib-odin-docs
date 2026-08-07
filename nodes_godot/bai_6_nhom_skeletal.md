# Bài 6: Nhóm Hoạt Hình Xương (Skeletal Animation)

Bên cạnh việc dùng SpriteSheet (Ảnh chớp tắt liên tục), Godot hỗ trợ làm Hoạt hình theo cấu trúc Xương bọc thịt (Skeletal), giống với phần mềm Spine 2D nổi tiếng. Điều này giúp game cực kỳ nhẹ vì bạn chỉ cần 1 bức ảnh duy nhất (tay, chân, thân rời rạc) thay vì phải vẽ 10 bức ảnh khác nhau.

## 1. Thành phần của Hoạt hình xương 2D

- **`Skeleton2D`**: Bộ khung xương tổng chỉ huy. Tất cả các chiếc xương con phải nằm bên trong nó.
- **`Bone2D`**: Đốt xương vô hình. Khớp tay nối vào khớp vai, cẳng tay nối vào bắp tay. Bạn thiết lập cây phả hệ (Parent-Child) cho các Bone2D để khi xoay Bắp tay, Cẳng tay sẽ xoay theo.
- **`Polygon2D` (Thịt)**: Thay vì dùng Sprite2D, bạn thả ảnh vào Polygon2D, sau đó "Gắn xương" (Weight) các điểm ảnh vào từng cục `Bone2D`. Nếu Bone cong lên, bức ảnh sẽ bị uốn lượn (Deform) theo, trông cực kỳ mềm mại.

## 2. Hệ thống IK (Inverse Kinematics)

Bình thường bạn phải xoay bắp tay, rồi xoay cẳng tay để cái Tay chạm được vào món đồ (Forward Kinematics - FK). 
Nhưng với IK (`SkeletonModification2D`), bạn chỉ cần cầm đúng bàn tay kéo tới món đồ, Godot sẽ tự động bẻ gập bắp tay và cẳng tay sao cho khớp!

Tính năng này là "Ma thuật" để làm cho đôi chân của Quái thú khổng lồ có thể tự động co gập tùy theo độ nhấp nhô của mặt đất (ngọn đồi gồ ghề).

## 3. Quy trình Rigging cơ bản

Bài này sẽ thiên về lý thuyết vì thao tác Rigging (Gắn xương) đòi hỏi giao diện trực quan. Các bước bao gồm:
1. Tạo một `Skeleton2D`.
2. Tạo các `Bone2D` theo cấu trúc con người (Hông -> Cột sống -> Ngực -> Cổ -> Đầu).
3. Đặt các `Sprite2D` (Ảnh cánh tay, cẳng chân) làm con của từng `Bone2D` tương ứng. (Lưu ý nhớ dời tâm Pivot của Sprite về đúng vị trí khớp nối).
4. Mở `AnimationPlayer`, lưu các mốc xoay (Rotation) của các cục Xương để tạo ra hoạt ảnh Chạy, Nhảy.

> [!TIP]
> Việc dùng Skeleton2D cho phép bạn thay đổi đồ (Cosmetics) cho nhân vật cực kỳ dễ. Muốn đổi kiếm? Chỉ việc đổi bức ảnh nằm dưới cục Xương Tay, toàn bộ hoạt ảnh vung kiếm vẫn giữ nguyên!
