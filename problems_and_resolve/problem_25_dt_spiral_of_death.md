# Vấn Đề 25: Vòng Xoáy Tử Thần (Spiral of Death)

**Vấn đề:**
Vào một màn chơi có quá nhiều hiệu ứng vụ nổ, game bị lag khiến FPS tụt xuống 10 (mất 0.1s mỗi khung hình). Đột nhiên, đạn bắt đầu bay xiên qua tường, nhân vật rơi xuyên qua sàn đất lọt ra khỏi bản đồ, mọi thứ hỗn loạn hoàn toàn.

**Nguyên nhân:**
Do FPS tụt, `Delta Time (dt)` trở nên rất lớn (0.1 giây hoặc hơn). 
Các công thức vật lý tính toán: Vị trí Mới = Vận tốc * `dt`.
Vì `dt` quá lớn, quãng đường nhân vật nhảy cóc trong 1 khung hình trở nên khổng lồ, bỏ qua mọi kiểm tra va chạm (Collision Tunneling). Quái vật đè lên nhau, vật lý đẩy chúng ra xa bằng một lực cực lớn, càng làm CPU quá tải -> FPS lại càng tụt sâu hơn nữa. Đó là "Spiral of Death".

**Giải pháp:**
Giới hạn mức tối đa (Clamp) cho Delta Time. Nếu máy tính bị khựng hoặc Tab game bị đưa xuống nền, tuyệt đối không cho `dt` vượt qua ngưỡng an toàn.

```odin
dt := rl.GetFrameTime()

// Kỹ thuật Cứu mạng (Clamp Delta Time)
MAX_DT :: 0.1 // Không cho dt lớn hơn 0.1 giây (tương đương 10 FPS)
if dt > MAX_DT {
    dt = MAX_DT
}

// Chấp nhận game chạy bị CHẬM ĐI (như slow-motion) khi quá lag,
// còn hơn là để Vật lý bay tứ tung và hỏng hoàn toàn.
update_physics(dt)
```
