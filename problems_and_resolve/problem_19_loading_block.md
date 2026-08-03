# Vấn Đề 19: Đứng hình khi Load tài nguyên (Loading Block)

**Vấn đề:**
Giữa lúc chơi game, nhân vật bước sang khu vực mới (Zone 2). Game đột ngột đứng hình toàn tập, âm thanh bị kẹt, chuột đơ mất 2 giây trong khi đợi màn hình tải ảnh nền của Zone 2.

**Nguyên nhân:**
Bạn gọi lệnh `rl.LoadTexture("huge_map.png")` ngay giữa Vòng Lặp Game (Main Thread). Lệnh đọc ổ cứng là lệnh đồng bộ (Synchronous), nó sẽ bắt CPU ngừng làm mọi việc khác để chờ ổ cứng trả file.

**Giải pháp:**
Sử dụng Đa luồng (Multi-threading - Chương 15) hoặc Tải trước (Pre-loading).
1. **Pre-loading:** Tải TOÀN BỘ file của mọi khu vực ở Màn hình chờ (Loading Screen) đầu tiên. 
2. **Multi-threading:** Dùng một luồng phụ (Background thread) tải dữ liệu thô (RAM) và chỉ đẩy lên VRAM bằng Luồng chính vào giây phút cuối cùng.
3. **Màn hình che (Fade Screen):** Để giấu việc giật lag 1 giây, hãy cho màn hình mờ đen dần (Fade to Black). Khi đen xì, tiến hành load nặng (người chơi không thấy bị lag ảnh). Sau khi load xong, cho sáng dần lên lại.

```odin
if zone_changed {
    // Thay vì đơ ảnh cũ, vẽ bọc màu đen lên trước
    rl.DrawRectangle(0,0,1280,720, rl.BLACK)
    rl.DrawText("Đang tải khu vực mới...", 500, 360, 20, rl.WHITE)
    rl.EndDrawing() // Ép GPU vẽ xong màn đen
    
    // TIẾN HÀNH LOAD NẶNG Ở ĐÂY (Lag giấu mặt sau màn đen)
    load_heavy_assets() 
}
```
