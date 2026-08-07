# Bài 2: Quản lý Global State với Autoload (Singleton)

Trong game, có những dữ liệu bạn muốn giữ lại khi người chơi chuyển từ Màn 1 (Scene 1) sang Màn 2 (Scene 2), ví dụ như **Điểm số (Score)**, **Máu (HP)**, hoặc **Cài đặt âm lượng**.
Vì khi chuyển Scene, Scene cũ sẽ bị xóa hoàn toàn khỏi bộ nhớ. Giải pháp của Godot là **Autoload**.

## 1. Autoload là gì?
Autoload là một Node được Godot tự động khởi tạo khi game vừa chạy, và nó sẽ tồn tại vĩnh viễn không bao giờ bị xóa khi bạn đổi Scene. Ở các ngôn ngữ khác, mẫu thiết kế này gọi là **Singleton**.

**Cách tạo Autoload:**
1. Tạo một script có tên `GameManager.gd` hoặc `GameManager.cs`.
2. Vào **Project -> Project Settings -> Autoload**.
3. Chọn script đó và thêm vào danh sách với tên `GameManager`.

## 2. Truy cập Autoload từ mọi nơi

### 🐍 GDScript
Với GDScript, Godot biến tên Autoload thành một biến toàn cục (Global variable). Bạn có thể gọi nó từ bất kỳ script nào.

```gdscript
# File: GameManager.gd
extends Node

var score: int = 0
var player_hp: int = 100

func add_score(amount: int):
	score += amount
```

```gdscript
# File: Player.gd (Nằm ở một Scene khác)
extends CharacterBody2D

func _on_coin_collected():
	# Gọi trực tiếp GameManager từ bất kỳ đâu!
	GameManager.add_score(10)
	print("Điểm hiện tại: ", GameManager.score)
```

### 🔷 C#
Với C#, vì bản chất nó là ngôn ngữ hướng đối tượng tĩnh, cách triển khai chuẩn nhất là sử dụng mẫu thiết kế Singleton bằng một biến `static`.

```csharp
// File: GameManager.cs
using Godot;

public partial class GameManager : Node
{
    // Biến static để lưu bản thể duy nhất (Singleton Instance)
    public static GameManager Instance { get; private set; }

    public int Score = 0;
    public int PlayerHp = 100;

    public override void _EnterTree()
    {
        // Gán chính bản thân Node này vào biến static khi vừa khởi tạo
        if (Instance == null)
            Instance = this;
        else
            QueueFree(); // Xóa nếu bị trùng lặp
    }

    public void AddScore(int amount)
    {
        Score += amount;
    }
}
```

```csharp
// File: Player.cs (Nằm ở một Scene khác)
using Godot;

public partial class Player : CharacterBody2D
{
    private void OnCoinCollected()
    {
        // Truy cập thông qua GameManager.Instance
        GameManager.Instance.AddScore(10);
        GD.Print("Điểm hiện tại: " + GameManager.Instance.Score);
    }
}
```

> [!WARNING]
> Đừng lạm dụng Autoload để chứa quá nhiều thứ (kẻ thù, đạn). Chỉ dùng nó cho các dữ liệu thực sự mang tính "toàn cầu" (Global).
