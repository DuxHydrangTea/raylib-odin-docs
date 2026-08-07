# Bài 4: Nhóm Hàm Toán Học Toàn Cục

Nhóm hàm này không thuộc về một Node nào cả. Ở GDScript, bạn có thể gọi chúng ở mọi nơi. Nhưng trong C#, chúng được sắp xếp cực kỳ quy củ vào hai lớp tĩnh là `Mathf` và `GD`.

## 1. `clamp(value, min, max)`

Chặn một biến không cho phép nó vọt ra khỏi một giới hạn Min/Max. Rất hay dùng để ép Thanh Máu không bị âm, hoặc Màn hình Camera không trôi quá bản đồ.

- **Trả về**: `float` hoặc `int` tùy vào dữ liệu truyền vào.

#### Song ngữ
```gdscript
# GDScript
hp = clamp(hp, 0, max_hp)
```
```csharp
// C# (Phải mượn hàm từ lớp Mathf)
_hp = Mathf.Clamp(_hp, 0, MaxHp);
```

## 2. `lerp(from, to, weight)`

Nội suy tuyến tính (Linear Interpolation). Chạy mượt mà từ số A sang số B dựa trên trọng số Weight (từ 0.0 đến 1.0). Nếu Weight = 0.5, hàm trả về điểm chính giữa của A và B.
Được dùng cực nhiều để làm hiệu ứng thanh máu tụt từ từ, hoặc Camera bám theo Player một cách êm ái.

#### Song ngữ
```gdscript
# GDScript
# Mỗi khung hình, Camera nhích 10% (0.1) quãng đường tới chỗ Player
camera_pos = lerp(camera_pos, player_pos, 0.1)
```
```csharp
// C# (Lưu ý: Mathf.Lerp áp dụng cho số float. Nếu là Vector2, dùng trực tiếp từ struct Vector2)
cameraPos = cameraPos.Lerp(playerPos, 0.1f);

float alpha = Mathf.Lerp(0.0f, 1.0f, 0.5f); // = 0.5f
```

## 3. Các hàm Ngẫu Nhiên (Random)

Làm game mà không có yếu tố Random thì không phải là game! 
- `randf()`: Random số thực từ 0.0 đến 1.0 (Dùng làm tỉ lệ % rớt đồ).
- `randf_range(min, max)`: Random số thực có giới hạn.
- `randi_range(min, max)`: Random số nguyên (VD: Từ 1 đến 5).

#### 🐍 GDScript
```gdscript
var ti_le = randf() # 0.73...
var damage = randf_range(10.5, 12.0)
var tien_vang = randi_range(1, 100)
```

#### 🔷 C#
Trong C#, các hàm này được nhét vào lớp lõi `GD`. Đặc biệt chú ý, hàm Range trong C# trả về kiểu `double`, nên khi làm game 2D bạn phải thường xuyên Ép kiểu (Cast) về `float`.

```csharp
using Godot;

float tiLe = GD.Randf();
// Phải ép kiểu (float) vì GD.RandRange trả ra double
float damage = (float)GD.RandRange(10.5, 12.0); 
int tienVang = GD.RandRange(1, 100); 
```

## 4. `wrapf(value, min, max)`

Cuộn vòng tròn giá trị. Ví dụ giới hạn là 0 đến 10, nếu value tăng lên 11, nó sẽ cuộn lại thành 1.
Cực kỳ hữu ích khi thao tác với Góc xoay (Độ). Góc xoay chỉ từ 0 đến 360 độ, nếu vật thể xoay liên tục tới 10.000 độ sẽ gây lỗi tràn bộ nhớ Toán học.

#### Song ngữ
```gdscript
# GDScript
rotation_degrees = wrapf(rotation_degrees, 0.0, 360.0)
```
```csharp
// C#
RotationDegrees = Mathf.Wrap(RotationDegrees, 0.0f, 360.0f);
```

> [!WARNING]
> GDScript có sẵn 2 hàm chuyển đổi góc quay rất tiện là `deg_to_rad()` và `rad_to_deg()`. Trong C#, bạn hãy tìm nó ở `Mathf.DegToRad()` nhé!
