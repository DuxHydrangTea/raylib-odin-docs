# Bài 14: Hệ thống Thời tiết & Hiệu ứng Hạt (Particles)

Không phải ngày nào trời cũng nắng đẹp. Việc thêm những ngày Mưa hoặc Tuyết rơi sẽ khiến nông trại sống động hơn, đồng thời hệ thống Mưa cũng tự động tưới nước hộ người chơi!

## 1. Thiết lập Hạt Mưa bằng `GPUParticles2D`

1. Khởi tạo một Node `GPUParticles2D` đặt tên là `RainParticles`. Đặt nó làm con của `Camera2D` (Để hạt mưa luôn rơi trước mặt người chơi dù họ đi đâu).
2. Tạo một **ParticleProcessMaterial**.
3. Cấu hình các thông số cơ bản:
   - **Emission Shape**: Box (Kéo dài hình hộp ra cho bằng chiều ngang màn hình).
   - **Particle Flag**: Align Y (Để hạt mưa dọc theo chiều rơi).
   - **Direction**: Y = 1 (Rơi xuống).
   - **Gravity**: Y = 98 (Trọng lực kéo xuống).
   - **Initial Velocity**: Tăng tốc độ ban đầu để mưa rơi xéo xéo (như có gió thổi).

## 2. Kết nối Thời tiết vào TimeManager

Mỗi sáng thức dậy, `TimeManager` sẽ quay xổ số (Random) để quyết định thời tiết ngày hôm đó.

### 🐍 GDScript (`TimeManager.gd`)
```gdscript
enum Weather { SUNNY, RAINY, SNOWY }
var current_weather = Weather.SUNNY

signal weather_changed(new_weather)

func tick_day():
	current_day += 1
	# Random thời tiết mới
	roll_weather()
	
func roll_weather():
	var chance = randf()
	
	if current_season == Season.WINTER:
		# Mùa đông thì chỉ có Nắng hoặc Tuyết
		if chance > 0.5: current_weather = Weather.SNOWY
		else: current_weather = Weather.SUNNY
	else:
		# Các mùa khác có Nắng hoặc Mưa
		if chance > 0.7: current_weather = Weather.RAINY # 30% Mưa
		else: current_weather = Weather.SUNNY
		
	weather_changed.emit(current_weather)
```

## 3. Mưa tự động tưới nước

Đây là cơ chế quan trọng giúp người chơi "xả hơi" vào những ngày mưa.

Vào lúc bắt đầu ngày mới (khi vừa gọi `weather_changed`), nếu trời mưa, ta quét qua toàn bộ TileMap và biến Đất khô thành Đất ướt.

### 🐍 GDScript (`TileManager.gd`)
```gdscript
func _ready():
	TimeManager.weather_changed.connect(_on_weather_changed)

func _on_weather_changed(weather):
	if weather == TimeManager.Weather.RAINY:
		print("Trời mưa! Tự động tưới toàn bộ nông trại!")
		
		# Quét toàn bộ các ô đang được sử dụng trong TileMap
		var used_cells = soil_layer.get_used_cells()
		for cell in used_cells:
			var tile_id = soil_layer.get_cell_source_id(cell)
			if tile_id == TILE_HOED:
				# Biến thành đất ướt
				soil_layer.set_cell(cell, TILE_WATERED, Vector2i(0,0))
				FarmData.add_watered_tile(cell)
```

> [!TIP]
> Bạn có thể kết hợp Node `CanvasModulate` ở Bài 7 để làm màn hình tối sầm lại và ngả sang màu xám xịt vào những ngày có Mưa hoặc Bão, cảm giác Game Feel sẽ tuyệt vời hơn rất nhiều!
