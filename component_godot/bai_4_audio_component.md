# Bài 4: Audio Component (Random Pitch)

Trong Game Feel (Cảm giác Game), nếu nhân vật cuốc đất 10 lần và cả 10 lần đều phát ra âm thanh tần số `1.0` y hệt nhau, người chơi sẽ cảm thấy não bộ bị "khó chịu" vì âm thanh bị máy móc lặp lại.

Bí quyết của dân làm game là: Mọi hiệu ứng âm thanh (SFX) đều phải được **thay đổi ngẫu nhiên cao độ (Random Pitch)** một chút xíu (ví dụ từ `0.9` đến `1.1`). Ta sẽ dùng một Component tên là `AudioComponent` (hoặc `RandomAudioPlayer2D`) để tự động hóa việc này.

## 1. Thiết kế AudioComponent

Component này KẾ THỪA từ `AudioStreamPlayer2D` thay vì `Node` cơ bản. 

### 🐍 GDScript
Tạo file `RandomAudioPlayer2D.gd`.

```gdscript
extends AudioStreamPlayer2D
class_name RandomAudioPlayer2D

@export var min_pitch: float = 0.9
@export var max_pitch: float = 1.1

# Ghi đè (Override) hàm play() mặc định của AudioStreamPlayer2D
func play_random():
	# Dùng hàm randf_range để sinh ra số ngẫu nhiên
	pitch_scale = randf_range(min_pitch, max_pitch)
	
	# Gọi hàm play() gốc của AudioStreamPlayer2D
	play()
```

### 🔷 C#
Tạo file `RandomAudioPlayer2D.cs`. 

```csharp
using Godot;

[GlobalClass]
public partial class RandomAudioPlayer2D : AudioStreamPlayer2D
{
    [Export] public float MinPitch = 0.9f;
    [Export] public float MaxPitch = 1.1f;

    public void PlayRandom()
    {
        // Sinh số ngẫu nhiên cho cao độ (Pitch)
        PitchScale = (float)GD.RandRange(MinPitch, MaxPitch);
        
        // Phát nhạc
        Play();
    }
}
```

## 2. Cách Sử dụng

1. Thay vì thêm `AudioStreamPlayer2D` vào Player, bạn kéo file `RandomAudioPlayer2D.gd` thả vào Player (Godot sẽ tự tạo Node với icon âm thanh do nó có tính kế thừa).
2. Kéo thả file âm thanh `hoe_hit.wav` vào mục **Stream**. Đặt tên Node là `HoeAudio`.
3. Trong code `Player`:

```gdscript
@onready var hoe_audio: RandomAudioPlayer2D = $HoeAudio

func hoe_ground():
	# Gọi hàm thay vì gọi play()
	hoe_audio.play_random()
```

Mỗi lần bạn cuốc đất, tiếng chát chúa sẽ lúc trầm lúc bổng vô cùng đã tai.

> [!NOTE]
> Bạn có thể cải tiến Component này xịn hơn bằng cách gán cho nó một Mảng (Array) chứa 5-6 âm thanh cuốc đất khác nhau. Trong hàm `play_random()`, code sẽ random chọn 1 trong 5 âm thanh đó, rồi tiếp tục random Pitch. Game của bạn sẽ có âm thanh AAA!
