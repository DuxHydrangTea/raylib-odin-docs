# Vấn Đề 2: Tilemap Bleeding (Kẽ hở màn hình)

**Vấn đề:**
Khi Camera di chuyển, thi thoảng bạn sẽ thấy những đường viền đen mảnh khảnh hoặc kẽ hở xuất hiện giữa các ô gạch (Tiles) trên bản đồ.

**Nguyên nhân:**
Do sai số dấu phẩy động (Floating Point) khi tính toán tỷ lệ phóng to (Scaling) của Camera. GPU đôi khi làm tròn số tọa độ pixel dẫn đến việc lấy dư 1 pixel ngoài lề của file ảnh (Texture).

**Giải pháp:**
1. **Làm tròn tọa độ Camera:** Đảm bảo Camera luôn trỏ vào số nguyên thay vì số thực.
```odin
camera.target.x = f32(math.round(player_pos.x))
camera.target.y = f32(math.round(player_pos.y))
```
2. **Kỹ thuật Extrusion (Đùn viền ảnh):** Khi vẽ các ô Tile trên Tileset, lặp lại các pixel viền ngoài cùng thêm 1 pixel. Phần mềm như Tiled có plugin tự động làm việc này.
3. **Cài đặt Filter cho Texture:** Nếu làm game Pixel Art, luôn tắt bộ lọc chống răng cưa của ảnh.
```odin
rl.SetTextureFilter(tileset_tex, .POINT) // Quan trọng cho Pixel Art
```
