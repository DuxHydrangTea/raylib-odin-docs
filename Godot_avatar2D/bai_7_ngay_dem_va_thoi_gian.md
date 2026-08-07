# Bài 7: Vòng lặp Ngày/Đêm (Day/Night Cycle)

Trồng trọt phải đi đôi với thời gian. Chúng ta sẽ tạo một hệ thống đếm giờ trong Game (ví dụ: 1 giây ngoài đời = 1 phút trong game). Màn hình sẽ dần tối lại khi về chiều và đen kịt lúc 12h đêm.

## 1. Hệ thống Đếm Thời Gian Toàn Cục (Autoload)

Quản lý thời gian phải nằm ở một script Toàn cục (Global) để mọi hệ thống (NPC, Cây cối) đều có thể truy cập mà không cần phải nối dây lằng nhằng.

1. Tạo một script tên là `TimeManager.gd`.
2. Vào **Project Settings -> Autoload**, thêm `TimeManager.gd` và đặt tên là `TimeManager`.

### 🐍 GDScript (`TimeManager.gd`)
```gdscript
extends Node

signal minute_changed(hour: int, minute: int)
signal day_changed(day: int)

var current_day: int = 1
var current_hour: int = 6 # Bắt đầu ngày mới lúc 6h sáng
var current_minute: int = 0

# Tốc độ thời gian (Ví dụ 1 giây ngoài đời = 10 phút trong game)
const REAL_SECONDS_PER_IN_GAME_MINUTE = 0.1 
var time_passed: float = 0.0

func _process(delta):
	time_passed += delta
	if time_passed >= REAL_SECONDS_PER_IN_GAME_MINUTE:
		time_passed = 0.0
		tick_minute()

func tick_minute():
	current_minute += 10 # Mỗi lần nhảy 10 phút
	
	if current_minute >= 60:
		current_minute = 0
		current_hour += 1
		
		if current_hour >= 24:
			current_hour = 0
			current_day += 1
			day_changed.emit(current_day)
			
	minute_changed.emit(current_hour, current_minute)
```

### 🔷 C# (`TimeManager.cs`)
Tương tự, tạo script C# và add vào Autoload.

```csharp
using Godot;

public partial class TimeManager : Node
{
    [Signal] public delegate void MinuteChangedEventHandler(int hour, int minute);
    [Signal] public delegate void DayChangedEventHandler(int day);

    public int CurrentDay = 1;
    public int CurrentHour = 6;
    public int CurrentMinute = 0;

    private const float RealSecPerGameMin = 0.1f;
    private float _timePassed = 0.0f;

    public override void _Process(double delta)
    {
        _timePassed += (float)delta;
        if (_timePassed >= RealSecPerGameMin)
        {
            _timePassed = 0.0f;
            TickMinute();
        }
    }

    private void TickMinute()
    {
        CurrentMinute += 10;
        if (CurrentMinute >= 60)
        {
            CurrentMinute = 0;
            CurrentHour += 1;

            if (CurrentHour >= 24)
            {
                CurrentHour = 0;
                CurrentDay += 1;
                EmitSignal(SignalName.DayChanged, CurrentDay);
            }
        }
        EmitSignal(SignalName.MinuteChanged, CurrentHour, CurrentMinute);
    }
}
```

## 2. Tạo Màn Đêm bằng CanvasModulate

Godot cung cấp một Node tên là `CanvasModulate` giúp phủ một lớp màu lên TÒAN BỘ các Node 2D bên dưới nó. (Hoạt động như Kính râm).

1. Mở Scene chính (`World.tscn`).
2. Thêm Node `CanvasModulate`.
3. Tạo script `DayNightCycle.gd` đính vào nó.

### 🐍 GDScript (`DayNightCycle.gd`)
```gdscript
extends CanvasModulate

# Định nghĩa các mốc màu
const DAY_COLOR = Color(1, 1, 1, 1) # Sáng trắng
const EVENING_COLOR = Color(0.8, 0.5, 0.3, 1) # Vàng cam hoàng hôn
const NIGHT_COLOR = Color(0.1, 0.1, 0.3, 1) # Xanh đen ban đêm

func _ready():
	# Lắng nghe thời gian từ Singleton
	TimeManager.minute_changed.connect(_on_time_changed)

func _on_time_changed(hour: int, minute: int):
	var time_float = hour + (minute / 60.0) # Tính ra số thập phân (Ví dụ 18h30 = 18.5)
	
	if time_float >= 6.0 and time_float < 17.0:
		# Ban ngày (6h - 17h)
		self.color = DAY_COLOR
	elif time_float >= 17.0 and time_float < 19.0:
		# Hoàng hôn (Từ 17h đến 19h, chuyển màu mượt bằng lerp)
		var weight = (time_float - 17.0) / 2.0 # Tỉ lệ từ 0 đến 1
		self.color = DAY_COLOR.lerp(EVENING_COLOR, weight)
	elif time_float >= 19.0 and time_float < 21.0:
		# Buổi tối (Từ 19h đến 21h)
		var weight = (time_float - 19.0) / 2.0
		self.color = EVENING_COLOR.lerp(NIGHT_COLOR, weight)
	else:
		# Đêm khuya
		self.color = NIGHT_COLOR
```

> [!NOTE]
> Mẹo nhỏ của hàm `lerp()` (Nội suy) giúp màn hình ngả màu từ từ sang Cam thay vì đột ngột chớp tắt. Điều này tạo cảm giác thời gian trôi vô cùng tự nhiên giống hệt Stardew Valley!
