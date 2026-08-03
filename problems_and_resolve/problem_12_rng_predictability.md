# Vấn Đề 12: Đồ thị sinh số ngẫu nhiên lặp lại (RNG Predictability)

**Vấn đề:**
Game của bạn là một tựa game thả xúc xắc (Dice). Lạ lùng thay, mỗi khi tắt game mở lại, xúc xắc luôn ra thứ tự: 5, 2, 6, 1, 3. Chơi ván nào cũng vậy.

**Nguyên nhân:**
Máy tính không thể tự nghĩ ra số ngẫu nhiên. Nó dùng một phương trình toán học gọi là PRNG (Pseudo-Random Number Generator). Phương trình này bắt đầu từ một điểm gọi là "Hạt giống" (Seed). Nếu bạn không gieo hạt (Set Seed), máy sẽ mặc định lấy Seed = 0 (hoặc 1), dẫn đến chuỗi số ngẫu nhiên sinh ra luôn giống hệt nhau.

**Giải pháp:**
Gieo hạt bằng đồng hồ thời gian thực của máy tính (vì thời gian luôn thay đổi từng mili-giây). Chỉ gọi hàm Set Seed đúng 1 lần khi khởi tạo game.

```odin
import "core:math/rand"
import "core:time"

main :: proc() {
    // 1. Lấy thời gian hiện tại làm Seed
    unix_time := time.to_unix_nanoseconds(time.now())
    
    // 2. Gieo hạt (Odin)
    rand.reset(u64(unix_time))
    
    // Giờ thì mỗi lần chạy game, chuỗi số sinh ra sẽ hoàn toàn khác biệt!
    a := rand.int31_max(10) 
}
```
*(Lưu ý: Nếu bạn làm game như Minecraft, bạn CẦN gán cứng Seed (Ví dụ Seed = 12345) để mọi người chơi tạo ra cùng một thế giới giống nhau).*
