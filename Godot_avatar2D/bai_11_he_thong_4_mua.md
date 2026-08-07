# Bài 11: Hệ thống 4 Mùa (Seasons) & Cây trồng héo úa

Mỗi Mùa trong game kéo dài 28 ngày. Khi chuyển mùa, khung cảnh thay đổi màu sắc và toàn bộ cây trồng của mùa cũ (nếu chưa thu hoạch) sẽ bị chết (Héo úa).

## 1. Định nghĩa Mùa (Enum)

Mở `TimeManager.gd` và bổ sung hệ thống Mùa màng.

### 🐍 GDScript
```gdscript
enum Season { SPRING, SUMMER, AUTUMN, WINTER }
var current_season: Season = Season.SPRING

signal season_changed(new_season)

func tick_day():
	current_day += 1
	if current_day > 28:
		current_day = 1
		advance_season()
		
func advance_season():
	current_season = (current_season + 1) % 4
	season_changed.emit(current_season)
	print("Đã chuyển sang mùa mới: ", current_season)
```

### 🔷 C#
```csharp
public enum Season { Spring, Summer, Autumn, Winter }
public Season CurrentSeason = Season.Spring;

[Signal] public delegate void SeasonChangedEventHandler(Season newSeason);

private void TickDay()
{
    CurrentDay++;
    if (CurrentDay > 28)
    {
        CurrentDay = 1;
        AdvanceSeason();
    }
}

private void AdvanceSeason()
{
    CurrentSeason = (Season)(((int)CurrentSeason + 1) % 4);
    EmitSignal(SignalName.SeasonChanged, (int)CurrentSeason);
}
```

## 2. Đổi màu Môi trường theo Mùa

Sử dụng lại Node `CanvasModulate` (hoặc tính năng Shader) để ám màu bản đồ.
- **Mùa Xuân**: Hơi ngả hồng (Hoa anh đào).
- **Mùa Hè**: Vàng chói rực rỡ.
- **Mùa Thu**: Cam sẫm (Lá đỏ).
- **Mùa Đông**: Xanh dương nhạt (Lạnh giá).

## 3. Cây trồng Héo Úa (Crop Death)

Mỗi Hạt giống sẽ được lưu một thuộc tính `allowed_seasons` (Mùa được phép sống). Ví dụ: Cà chua sống được mùa Hè và Thu.

Khi sự kiện `season_changed` kích hoạt, ta báo cho toàn bộ Cây trồng (Crop) đang trồng trên đất tự kiểm tra sinh mệnh của mình.

### 🐍 GDScript (`Crop.gd`)
```gdscript
extends Node2D

@export var crop_name: String = "Cà chua"
@export var allowed_seasons: Array[TimeManager.Season] = [TimeManager.Season.SUMMER, TimeManager.Season.AUTUMN]

@onready var sprite = $Sprite2D

func _ready():
	TimeManager.season_changed.connect(_on_season_changed)

func _on_season_changed(new_season):
	if not allowed_seasons.has(new_season):
		die()

func die():
	print(crop_name, " không chịu nổi thời tiết mùa này và đã héo úa!")
	# Đổi hình ảnh sang bụi cỏ khô màu nâu
	sprite.texture = preload("res://assets/dead_crop.png")
	
	# Xóa bỏ các tính năng tương tác thu hoạch
	if has_node("HarvestArea"):
		$HarvestArea.queue_free()
```

> [!WARNING]
> Đừng bao giờ gọi lệnh `queue_free()` thẳng thừng lên cây trồng khi nó chết. Người chơi cần NHÌN THẤY xác cây (Bụi cỏ khô) để biết mình đã tính toán sai ngày gieo hạt, và họ phải vác Liềm ra dọn dẹp đống rác đó. Đó mới là Game Nông trại chuẩn mực!
