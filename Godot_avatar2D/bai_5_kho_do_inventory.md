# Bài 5: Thu Hoạch & Kho Đồ (Inventory)

Khi cây đã chín, người chơi nhấn phím tương tác để thu hoạch, cất vào túi và biến cây đó biến mất.

## 1. Lưu trữ Kho Đồ bằng Autoload
Giống như Bài 2 của phần Mẫu Thiết Kế, chúng ta tạo một Autoload `InventoryManager` để lưu số lượng nông sản. Dùng Cấu trúc **Dictionary** (Từ điển).

### 🐍 GDScript
```gdscript
# File: InventoryManager.gd (Autoload)
extends Node

var items: Dictionary = {} # VD: {"tomato": 5, "carrot": 2}
signal inventory_updated()

func add_item(item_name: String, amount: int = 1):
	if items.has(item_name):
		items[item_name] += amount
	else:
		items[item_name] = amount
		
	inventory_updated.emit()
	print("Đã thu hoạch! Túi đồ: ", items)
```

## 2. Refactor: Tính Đóng Gói (Encapsulation)

> [!TIP]
> **Tư duy đi làm (Professional):** Đừng bao giờ cho phép `Player` đọc trực tiếp một biến sâu bên trong `Crop` (như `if collider.stage == 2`). Hành động này phá vỡ **Tính Đóng Gói (Encapsulation)** của Lập trình Hướng đối tượng. 
> 
> Nếu sau này `Crop` đổi logic, bạn sẽ phải lùng sục khắp nơi để sửa file `Player`. Thay vào đó, hãy để `Crop` tự quyết định nó đã chín chưa và cung cấp hàm giao tiếp công khai (Public method).

### Cập nhật Script của Crop (Thêm hàm công khai)
Thêm đoạn code này vào file `Crop.gd` (hoặc `Crop.cs`):

```gdscript
# (Bên trong Crop.gd)
# Dùng export để mỗi cây tự quy định nó là cây gì (Cà chua, Cà rốt...) thay vì hardcode
@export var crop_name: String = "tomato" 

# Hàm công khai (Public method) để Player gọi
func can_harvest() -> bool:
	return current_stage == GrowthStage.MATURE

# Trả về tên nông sản khi thu hoạch thành công
func harvest() -> String:
	queue_free() # Xóa cây trồng đi
	return crop_name
```

### Logic Thu Hoạch từ Player
Giờ đây, logic bên trong `Player` sẽ cực kỳ "sạch" và "chuẩn":

#### 🐍 GDScript
```gdscript
# (Bên trong script Player.gd)
func harvest():
	var collider = interact_ray.get_collider()
	
	if collider and collider.is_in_group("Crop"):
		# Player không hề biết bên trong Crop dùng biến stage hay gì cả
		# Player chỉ cần hỏi: "Mày thu hoạch được chưa?"
		if collider.has_method("can_harvest") and collider.can_harvest():
			
			# Thu hoạch và xin cái tên cây
			var harvested_item = collider.harvest()
			
			# Nhét vào kho
			InventoryManager.add_item(harvested_item, 1)
```

#### 🔷 C#
```csharp
// (Bên trong Player.cs)
private void Harvest()
{
    var collider = _interactRay.GetCollider();

    // Dùng ép kiểu an toàn trong C# (Pattern matching)
    if (collider is Crop crop)
    {
        // Player giao tiếp qua hàm public của Crop
        if (crop.CanHarvest())
        {
            string harvestedItem = crop.Harvest();
            InventoryManager.Instance.AddItem(harvestedItem, 1);
        }
    }
}
```

---
**TỔNG KẾT KHÓA HỌC:**
Tuyệt vời! Bạn đã có một Mini-Project hoàn chỉnh với **Chất lượng Code chuẩn mực (Production-ready)**. Không có Magic Numbers, không có Hard-code, và tuân thủ chặt chẽ OOP Encapsulation.

Bạn hoàn toàn có thể tự mở rộng thêm tính năng **Tưới nước**, **Đổi công cụ (Cuốc, Bình tưới)** dựa vào bộ khung chất lượng cao này!
