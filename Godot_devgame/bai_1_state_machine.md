# Bài 1: State Machine Cơ Bản (FSM)

Khi lập trình nhân vật (Player), người mới thường dùng một nùi lệnh `if/else` để kiểm tra: "Nếu đang ở trên mặt đất thì được nhảy, nếu đang chạy thì không được tấn công...". Cách này sẽ biến code thành "Spaghetti" (rối rắm) rất nhanh. Giải pháp tốt nhất là dùng **Finite State Machine (FSM - Máy trạng thái hữu hạn)**.

## 1. Ý tưởng của FSM
Nhân vật tại một thời điểm chỉ có thể ở MỘT trạng thái duy nhất:
- `IDLE` (Đứng im)
- `RUN` (Chạy)
- `JUMP` (Nhảy)

Ta dùng một biến `state` để lưu trạng thái hiện tại. Tùy vào trạng thái mà ta cho phép người chơi làm gì.

## 2. Triển khai bằng Enum và Match/Switch

### 🐍 GDScript
Trong GDScript, ta dùng `enum` và lệnh `match` (giống switch trong các ngôn ngữ khác).

```gdscript
extends CharacterBody2D

enum State { IDLE, RUN, JUMP }
var current_state: State = State.IDLE

func _process(delta: float):
	match current_state:
		State.IDLE:
			# Chỉ cho phép đổi sang RUN nếu bấm nút di chuyển
			if Input.get_axis("ui_left", "ui_right") != 0:
				current_state = State.RUN
			elif Input.is_action_just_pressed("ui_up"):
				current_state = State.JUMP
				
		State.RUN:
			# Xử lý logic chạy
			if Input.get_axis("ui_left", "ui_right") == 0:
				current_state = State.IDLE
				
		State.JUMP:
			# Logic nhảy (rơi xuống thì chuyển về IDLE)
			pass
```

### 🔷 C#
Trong C#, ta sử dụng `enum` chuẩn và lệnh `switch`.

```csharp
using Godot;

public partial class Player : CharacterBody2D
{
    public enum State { Idle, Run, Jump }
    private State _currentState = State.Idle;

    public override void _Process(double delta)
    {
        switch (_currentState)
        {
            case State.Idle:
                if (Input.GetAxis("ui_left", "ui_right") != 0)
                    _currentState = State.Run;
                else if (Input.IsActionJustPressed("ui_up"))
                    _currentState = State.Jump;
                break;

            case State.Run:
                if (Input.GetAxis("ui_left", "ui_right") == 0)
                    _currentState = State.Idle;
                break;

            case State.Jump:
                // Logic nhảy
                break;
        }
    }
}
```

> [!TIP]
> Đây là cách FSM đơn giản nhất. Với dự án lớn, mỗi State nên được tách ra thành một Script riêng biệt (State Pattern thực thụ) để dễ quản lý hơn!
