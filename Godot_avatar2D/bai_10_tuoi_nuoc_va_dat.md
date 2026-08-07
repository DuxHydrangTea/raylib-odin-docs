# Bài 10: Cơ chế Tưới Nước & Hệ thống Đất

Trong Stardew Valley, cây chỉ lớn lên vào sáng hôm sau NẾU ngày hôm trước nó được tưới nước. Chúng ta sẽ mở rộng TileMap để hỗ trợ Đất Khô và Đất Ướt.

## 1. Thiết lập TileMap Mới

Thay vì chỉ có Tile "Đất đã cuốc" (Hoed Dirt), ta tạo thêm một Tile "Đất ướt" (Watered Dirt) với màu đất sẫm hơn.

- Nguồn Tile ID (Giả sử): 
  - `0`: Đất thường (Chưa cuốc)
  - `1`: Đất đã cuốc (Khô)
  - `2`: Đất đã cuốc (Ướt)

## 2. Dụng cụ Bình tưới nước (Watering Can)

Khi Player cầm bình tưới và bấm hành động, ta sẽ lấy tọa độ ô lưới (Cell) trước mặt Player. Nếu ô đó đang là Đất cuốc (Khô), ta biến nó thành Đất Ướt.

### 🐍 GDScript (`TileManager.gd` - Autoload)
```gdscript
extends Node

@onready var soil_layer = get_tree().get_first_node_in_group("SoilLayer") as TileMapLayer

const TILE_HOED = 1
const TILE_WATERED = 2

func water_soil(global_pos: Vector2):
	# 1. Chuyển Tọa độ thế giới thành Tọa độ ô lưới (Grid)
	var cell_pos = soil_layer.local_to_map(global_pos)
	
	# 2. Lấy dữ liệu của ô đất hiện tại
	var current_tile = soil_layer.get_cell_source_id(cell_pos)
	
	if current_tile == TILE_HOED:
		# 3. Thay bằng Đất Ướt
		soil_layer.set_cell(cell_pos, TILE_WATERED, Vector2i(0, 0))
		print("Đã tưới nước ô: ", cell_pos)
		
		# (Tùy chọn) Lưu vào mảng dữ liệu để sang ngày hôm sau xử lý
		FarmData.add_watered_tile(cell_pos)
	else:
		print("Chỉ được tưới lên đất đã cuốc!")
```

### 🔷 C#
```csharp
using Godot;

public partial class TileManager : Node
{
    private TileMapLayer _soilLayer;
    private const int TileHoed = 1;
    private const int TileWatered = 2;

    public override void _Ready()
    {
        _soilLayer = GetTree().GetFirstNodeInGroup("SoilLayer") as TileMapLayer;
    }

    public void WaterSoil(Vector2 globalPos)
    {
        Vector2I cellPos = _soilLayer.LocalToMap(globalPos);
        int currentTile = _soilLayer.GetCellSourceId(cellPos);

        if (currentTile == TileHoed)
        {
            _soilLayer.SetCell(cellPos, TileWatered, new Vector2I(0, 0));
            GD.Print("Đã tưới nước ô: ", cellPos);
            // Cập nhật Database
            FarmData.AddWateredTile(cellPos);
        }
    }
}
```

## 3. Chuyển ngày (Reset Đất Ướt về Khô)

Khi nhân vật đi ngủ, sự kiện `day_changed` sẽ được kích hoạt. Ta duyệt qua toàn bộ danh sách các ô đất đã tưới, giúp Cây ở trên ô đó Lớn Lên 1 giai đoạn, sau đó biến Đất Ướt trở lại thành Đất Khô.

### 🐍 GDScript
```gdscript
func _on_day_changed(new_day):
	for cell_pos in FarmData.get_watered_tiles():
		# Cây trồng lớn lên
		grow_crop_at(cell_pos)
		
		# Trả lại đất khô
		soil_layer.set_cell(cell_pos, TILE_HOED, Vector2i(0,0))
		
	# Xóa danh sách đất ướt
	FarmData.clear_watered_tiles()
	print("Chào buổi sáng! Mọi mảnh đất đã khô lại.")
```

> [!TIP]
> Việc lưu Tọa độ ô lưới (Vector2i) vào một mảng toàn cục `FarmData` giúp chúng ta dễ dàng quản lý hàng nghìn ô đất mà không bắt Game Engine phải quét lại toàn bộ TileMap mỗi ngày!
