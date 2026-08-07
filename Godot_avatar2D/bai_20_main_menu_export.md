# Bài 20: Main Menu & Xuất Game (Export)

Xin chúc mừng! Bạn đã đi đến chặng cuối của Dự án Nông Trại. Giờ là lúc tạo Màn hình chính (Main Menu) đẹp mắt và đóng gói game thành file `.exe` để gửi cho bạn bè chơi thử.

## 1. Thiết kế Main Menu

Tạo Scene `MainMenu.tscn` (Kế thừa từ `Control`).
- Đặt một `TextureRect` chứa hình nền Nông trại lấp lánh (Background).
- Một `Label` chứa Tên Game (Ví dụ: "Pixel Farm").
- Một `VBoxContainer` chứa các Nút bấm:
  - `BtnStart` (Chơi mới)
  - `BtnLoad` (Tiếp tục - Nếu có file Save)
  - `BtnQuit` (Thoát Game)

### 🐍 GDScript (`MainMenu.gd`)
```gdscript
extends Control

@onready var btn_load = $VBoxContainer/BtnLoad

func _ready():
	# Kiểm tra xem có File Save không để vô hiệu hóa nút Load
	if not FileAccess.file_exists(SaveManager.SAVE_PATH):
		btn_load.disabled = true

func _on_btn_start_pressed():
	# Xóa file save cũ (nếu muốn) và chuyển vào game
	get_tree().change_scene_to_file("res://World.tscn")

func _on_btn_load_pressed():
	# Load game
	SaveManager.load_game()
	get_tree().change_scene_to_file("res://World.tscn")

func _on_btn_quit_pressed():
	get_tree().quit()
```

## 2. Thiết lập Main Scene

Để khi bật Game lên, nó tự động nhảy vào Main Menu chứ không phải văng thẳng vào trang trại:
1. Mở Project Settings.
2. Mục **Application -> Run -> Main Scene**.
3. Chọn file `MainMenu.tscn`.

## 3. Đóng gói Game (Export)

Quá trình "Build" (Biên dịch) game ra file chạy độc lập (.exe trên Windows, .apk trên Android).

1. Ở thanh menu trên cùng, chọn **Project -> Export...**
2. Cửa sổ Export hiện ra, bấm `Add...` ở góc trên cùng bên trái.
3. Chọn Nền tảng muốn xuất (Ví dụ: **Windows Desktop**).
   - *Lưu ý*: Nếu Godot báo lỗi thiếu "Export Templates", bạn chỉ cần nhấp vào nút "Manage Export Templates" và bấm Download (Godot sẽ tự tải bộ biên dịch về, nặng khoảng 400MB).
4. Ở cột bên phải, bạn có thể chỉnh sửa:
   - Tên File `.exe`.
   - File Icon (`.ico` hoặc `.png`).
   - Tên công ty/Tên nhà phát triển.
5. Bấm nút **Export Project...** ở dưới đáy, chọn thư mục lưu (Nên tạo một thư mục mới ngoài Desktop).

> [!WARNING]
> Đừng bao giờ Export đè trực tiếp vào bên trong thư mục chứa Source Code của bạn. Hãy tạo một folder riêng (VD: `Build/Windows/`) để chứa file `.exe` và file `.pck` (gói dữ liệu game).

---

**LỜI KẾT**

Vậy là Series **20 Bài Học Làm Game Nông Trại** (Godot 2D) đã chính thức khép lại. Từ một bãi đất trống rỗng, chúng ta đã xây dựng nên một hệ sinh thái hoàn chỉnh với Cây trồng, Vật nuôi, Cửa hàng mua bán, AI dân làng, Hệ thống 4 Mùa và Lưu/Tải game. 

Hy vọng rằng "Mảnh vườn" này sẽ là nền tảng vững chắc để bạn tự tin sải cánh tạo ra siêu phẩm Stardew Valley của riêng mình trong tương lai! Hẹn gặp lại! 🚀
