# Bài 19: Quản lý Âm Thanh (AudioManager)

Âm thanh (Nhạc nền và Tiếng động) chiếm đến 50% cảm xúc của trò chơi. Nếu bạn rải các cục `AudioStreamPlayer` bừa bãi khắp các Scene, bạn sẽ không thể làm tính năng "Tắt Nhạc / Tắt Tiếng Động" trong menu Cài Đặt (Settings).

Đó là lý do ta cần một **AudioManager** (Autoload).

## 1. Thiết lập AudioManager

Tạo một Node cơ bản đặt tên là `AudioManager` và thêm vào Autoload.
Bên trong nó, tạo 2 Node con:
- `BGM_Player` (AudioStreamPlayer - Phát nhạc nền).
- `SFX_Player` (AudioStreamPlayer - Phát tiếng động).

### 🐍 GDScript (`AudioManager.gd`)
```gdscript
extends Node

@onready var bgm_player = $BGM_Player
@onready var sfx_player = $SFX_Player

# Các bài nhạc nền theo Mùa
var spring_bgm = preload("res://audio/spring_theme.ogg")
var summer_bgm = preload("res://audio/summer_theme.ogg")

func play_bgm(season: TimeManager.Season):
	if season == TimeManager.Season.SPRING:
		bgm_player.stream = spring_bgm
	elif season == TimeManager.Season.SUMMER:
		bgm_player.stream = summer_bgm
		
	bgm_player.play()

# Hàm phát tiếng động chung
func play_sfx(sound: AudioStream):
	sfx_player.stream = sound
	sfx_player.play()
```

## 2. Tiếng bước chân (Footsteps)

Tiếng bước chân giúp Game Feel tăng lên gấp bội. Cách đơn giản nhất là dựa vào Animation.

Mở `AnimationPlayer` của Player.
Trong Animation `walk` (đi bộ), ta thêm một rãnh (Track) mới gọi là **Call Method Track**.
Chỉ định Track này gọi vào chính cái Node Player.

Đặt một điểm Keyframe (Chìa khóa) vào giây thứ `0.1` và `0.3` (Lúc 2 chân chạm đất). Ở điểm Keyframe đó, điền tên hàm `play_footstep()`.

### 🐍 GDScript (`Player.gd`)
```gdscript
var dirt_step_sound = preload("res://audio/step_dirt.wav")

func play_footstep():
	# Gọi AudioManager phát tiếng bước chân
	AudioManager.play_sfx(dirt_step_sound)
```

## 3. Audio Bus (Kênh Âm Thanh)

Để làm tính năng Chỉnh Âm lượng trong Cài đặt, Godot hỗ trợ **Audio Bus**.
Mở tab Audio (Gần tab Animation dưới đáy màn hình).
- Add Bus mới tên là `Music`.
- Add Bus mới tên là `SFX`.

Trong `AudioManager`:
- Click vào `BGM_Player`, sửa thuộc tính **Bus** thành `Music`.
- Click vào `SFX_Player`, sửa thuộc tính **Bus** thành `SFX`.

Để code thanh Trượt Âm Lượng (Slider) chỉnh to nhỏ nhạc nền:

### 🐍 GDScript (Thanh trượt Music Volume)
```gdscript
extends HSlider

var music_bus_index = AudioServer.get_bus_index("Music")

func _on_value_changed(value: float):
	# Chuyển đổi % (từ 0.0 đến 1.0) sang decibel (dB)
	var db = linear_to_db(value)
	AudioServer.set_bus_volume_db(music_bus_index, db)
```

> [!TIP]
> Việc dùng `linear_to_db` là bắt buộc vì thính giác của con người cảm nhận âm lượng theo hàm Logarit chứ không phải tuyến tính. Nếu bạn để Slider 50% thì âm thanh phải giảm ở mức decibel tương ứng mới nghe ra được sự thay đổi.
