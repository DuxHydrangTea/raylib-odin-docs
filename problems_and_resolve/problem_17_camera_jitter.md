# Vấn Đề 17: Rung giật Camera (Camera Jitter / Lerp Stutter)

**Vấn đề:**
Bạn áp dụng hàm nội suy (`Lerp`) để Camera bám theo người chơi một cách mượt mà. Tuy nhiên khi nhân vật chạy, cảnh vật nền xung quanh (Background) cứ giật cục từng nhịp nhỏ, rất nhức mắt.

**Nguyên nhân:**
Có 2 nguyên nhân chính:
1. **Cập nhật sai thứ tự:** Hàm Cập nhật Camera chạy TRƯỚC hàm Cập nhật Vị trí người chơi. Kết quả là Camera luôn trỏ về vị trí cũ của người chơi ở frame trước.
2. **Pixel Snapping:** Nhân vật di chuyển với tọa độ thập phân (10.5, 10.7), nhưng màn hình chỉ vẽ được pixel nguyên (10, 11). Khi Camera di chuyển không đồng bộ với độ lẻ của điểm ảnh, hình ảnh bị răng cưa giật cục.

**Giải pháp:**
1. Luôn luôn cập nhật Camera ở **CUỐI CÙNG** của vùng Update, ngay trước lệnh Draw. Đảm bảo mọi vật thể đã hoàn thành chuyển động.
2. Ép Camera Target làm tròn về số nguyên, và dùng Sub-pixel rendering (nếu hỗ trợ).

```odin
// 1. Cập nhật nhân vật trước
player.pos += vel * dt

// 2. Nội suy mượt mà (Lerp)
target_cam_pos = rl.Vector2Lerp(target_cam_pos, player.pos, 5.0 * dt)

// 3. Ép làm tròn (Rất quan trọng cho Pixel Art!)
camera.target.x = math.round(target_cam_pos.x)
camera.target.y = math.round(target_cam_pos.y)
```
