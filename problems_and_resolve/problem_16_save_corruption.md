# Vấn Đề 16: Hỏng file lưu game (Save Data Corruption)

**Vấn đề:**
Người chơi đã cày game của bạn được 100 giờ. Bạn tung ra bản Update mới (Bản 1.1), thêm biến `mana: int` vào hệ thống nhân vật. 
Người chơi cập nhật game, mở lên, Load save cũ -> BÙM! Game crash và xóa sạch 100 giờ chơi của họ do file JSON không khớp cấu trúc mới. Bạn bị review 1 sao tơi bời.

**Nguyên nhân:**
Bạn parse thẳng JSON hoặc Byte code từ ổ cứng vào Struct của phiên bản hiện tại mà không có lớp bảo vệ (Version control) hoặc kiểm tra tương thích ngược.

**Giải pháp:**
Luôn đính kèm `version` vào file Save. Nếu version cũ, phải viết code phiên dịch (Migrate) nó sang chuẩn mới trước khi Load.

```odin
SaveData :: struct {
    version: int,
    hp: int,
    // V1.1 thêm biến mana
    mana: int, 
}

load_game :: proc() {
    // ... Đọc json ...
    if json_data.version == 1 {
        // Người chơi từ bản cũ! Gán giá trị mặc định cho các trường mới
        player.hp = json_data.hp
        player.mana = 100 // Giá trị mặc định
        // Bắt buộc update file save lên bản mới ngay lập tức
        save_game_v2() 
    }
}
```
