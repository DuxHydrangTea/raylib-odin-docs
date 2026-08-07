# Bài 9: Hệ thống Lưu & Tải Game (Save / Load)

Một trong những hệ thống "khoai" nhất của ngành làm game là Save/Load. Trong Stardew Valley, mỗi khi nhân vật lên giường đi ngủ, game sẽ tự động lưu lại toàn bộ (Tiền, Kho đồ, Trạng thái Cây cối).

Để làm việc này, chúng ta sẽ mã hóa mọi thứ thành định dạng chuỗi **JSON** và ghi ra một file trên ổ cứng.

## 1. Lưu Game (Save)

Tạo một script Autoload tên là `SaveManager.gd`.

### 🐍 GDScript
```gdscript
extends Node

const SAVE_PATH = "user://farm_save.json"

func save_game():
	# 1. Thu thập mọi dữ liệu cần lưu thành một cuốn từ điển (Dictionary)
	var player = get_tree().get_first_node_in_group("Player")
	
	var save_dict = {
		"gold": player.gold,
		"stamina": player.current_stamina,
		"day": TimeManager.current_day,
		"player_pos_x": player.global_position.x,
		"player_pos_y": player.global_position.y,
		# Giả sử Kho đồ có hàm trích xuất dữ liệu
		"inventory": player.inventory.get_save_data()
	}
	
	# 2. Mở file để Ghi (Write)
	var file = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	
	# 3. Ép kiểu Từ điển thành chuỗi JSON và ghi vào file
	var json_string = JSON.stringify(save_dict)
	file.store_line(json_string)
	
	print("Đã lưu Game thành công!")
```

### 🔷 C#
Trong C#, ta có thể dùng hệ thống JSON của Godot hoặc dùng luôn thư viện `System.Text.Json` vô cùng mạnh mẽ của .NET. Ở đây ta dùng cách của Godot.

```csharp
using Godot;

public partial class SaveManager : Node
{
    private const string SavePath = "user://farm_save.json";

    public void SaveGame()
    {
        Player player = GetTree().GetFirstNodeInGroup("Player") as Player;
        TimeManager timeMgr = GetNode<TimeManager>("/root/TimeManager");

        var saveDict = new Godot.Collections.Dictionary
        {
            { "gold", player.Gold },
            { "day", timeMgr.CurrentDay },
            { "player_pos_x", player.GlobalPosition.X },
            { "player_pos_y", player.GlobalPosition.Y }
        };

        using var file = FileAccess.Open(SavePath, FileAccess.ModeFlags.Write);
        string jsonString = Json.Stringify(saveDict);
        file.StoreLine(jsonString);

        GD.Print("Lưu game C# thành công!");
    }
}
```

## 2. Tải Game (Load)

Khi người chơi mở game và bấm nút "Continue", ta tiến hành đọc file.

### 🐍 GDScript
```gdscript
func load_game():
	# Kiểm tra file có tồn tại không
	if not FileAccess.file_exists(SAVE_PATH):
		print("Không có file save nào!")
		return
		
	# Mở file để Đọc (Read)
	var file = FileAccess.open(SAVE_PATH, FileAccess.READ)
	var json_string = file.get_as_text()
	
	# Dịch chuỗi JSON ngược lại thành Từ điển
	var json = JSON.new()
	var error = json.parse(json_string)
	
	if error == OK:
		var save_dict = json.get_data()
		
		# Khôi phục dữ liệu cho Player
		var player = get_tree().get_first_node_in_group("Player")
		player.gold = save_dict["gold"]
		player.global_position = Vector2(save_dict["player_pos_x"], save_dict["player_pos_y"])
		
		TimeManager.current_day = save_dict["day"]
		print("Tải game thành công!")
	else:
		print("File Save bị lỗi (Corrupted)!")
```

> [!IMPORTANT]
> **Đường dẫn `user://` là gì?**
> Godot chia ổ cứng làm 2 loại: `res://` (Nơi chứa file gốc của Project, dạng chỉ-đọc khi xuất file cài) và `user://` (Nơi lưu trữ dữ liệu cá nhân của người chơi như File Save, Cache). 
> - Trên Windows, `user://` thường nằm ở `C:\Users\[TênBạn]\AppData\Roaming\Godot\app_userdata\[TênGame]\`.
> - Tuyệt đối không dùng `res://` để lưu Save Game vì khi Build ra `.exe`, bạn sẽ không ghi đè vào file .exe được!
