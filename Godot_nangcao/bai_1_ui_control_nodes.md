# Bài 1: Làm Chủ Hệ Thống Giao Diện (Control Nodes)

Giao diện người dùng (UI) trong Godot được xây dựng hoàn toàn bằng **các Node màu xanh lá cây** (kế thừa từ lớp `Control`). Khác với Node2D (xanh dương) định vị bằng Tọa độ XY, Control Node định vị bằng **Hệ thống Neo (Anchors)** và **Vùng chứa (Containers)**.

## 1. Hệ thống Neo (Anchors & Presets)
Bạn muốn một Nút bấm (Button) luôn nằm ở góc trên bên phải màn hình dù cửa sổ game bị thu nhỏ hay phóng to?
- Thêm một `Button`.
- Nhìn lên thanh công cụ phía trên (hoặc trong phần Layout ở Inspector), chọn **Anchor Preset**.
- Chọn **Top Right**. Bất chấp độ phân giải màn hình, nút bấm sẽ luôn bám dính vào góc đó!

## 2. Các Node Container Tự động sắp xếp
Thay vì phải tính toán khoảng cách bằng tay, Godot cung cấp các Container tự động dàn trang:
- **VBoxContainer**: Xếp các Node con theo chiều **Dọc** (Vertical). Rất hợp để làm danh sách Menu (Play, Settings, Quit).
- **HBoxContainer**: Xếp theo chiều **Ngang** (Horizontal). Dùng làm thanh máu đứng cạnh icon nhân vật.
- **MarginContainer**: Tạo lề (Padding) để UI không bị dính sát vào viền màn hình.

## 3. Thực hành tạo Main Menu

1. Tạo `MarginContainer` lấp đầy màn hình (Anchor: Full Rect). Chỉnh Margin = 50.
2. Bên trong thêm `VBoxContainer` (Căn giữa).
3. Trong VBox, thêm 2 `Button` đặt tên là "Chơi" và "Thoát".

### Code bắt sự kiện cho Nút bấm

#### 🐍 GDScript
```gdscript
extends Control

func _on_play_button_pressed():
	# Hàm chuyển Scene (Mở màn chơi chính)
	get_tree().change_scene_to_file("res://MainLevel.tscn")

func _on_quit_button_pressed():
	# Thoát game
	get_tree().quit()
```

#### 🔷 C#
```csharp
using Godot;

public partial class MainMenu : Control
{
    private void OnPlayButtonPressed()
    {
        // Chuyển Scene
        GetTree().ChangeSceneToFile("res://MainLevel.tscn");
    }

    private void OnQuitButtonPressed()
    {
        // Thoát game
        GetTree().Quit();
    }
}
```

> [!TIP]
> **Tư duy đi làm:** Không bao giờ kéo thả Control Node tự do bằng tay để làm Menu! Hãy luốn bọc chúng trong các `Container` để giao diện của bạn hỗ trợ Responsive (hiển thị tốt trên cả Màn hình vuông lẫn Màn hình rộng).
