# Chương 22: Bí kíp Tối Ưu Hiệu Năng (Performance Optimization)

Khi dự án game nông trại của bạn phát triển thành một tựa game MMO thực thụ với hàng ngàn người chơi và hàng chục vạn vật nuôi, các phương pháp lập trình cơ bản sẽ khiến CPU của bạn "bốc cháy" và GPU bị "nghẽn cổ chai". 

Đây là lúc chúng ta phải áp dụng **7 kỹ thuật tối ưu hóa (Optimization Techniques)** kinh điển, tận dụng tối đa sức mạnh của ngôn ngữ Odin và kiến trúc ECS.

---

## 1. Bit Sets & Bitwise Flags (Tối ưu Bộ Nhớ & Trạng Thái)

### Vấn đề:
Khi một con vật có thể mắc nhiều loại bệnh cùng lúc (Cúm, Nấm, Lở mồm long móng...), lập trình viên thường dùng Mảng (`[dynamic]Disease`) hoặc một đống biến Boolean (`is_flu: bool, is_fungus: bool`). Điều này làm lãng phí bộ nhớ và vòng lặp `for` để tìm kiếm rất tốn thời gian.

### Giải pháp trong Odin:
Odin có sẵn một cấu trúc dữ liệu tuyệt vời là `bit_set`. Mỗi loại bệnh sẽ tương ứng với 1 bit (0 hoặc 1) bên trong một biến số nguyên duy nhất. 1 biến số nguyên 32-bit có thể lưu trữ đến 32 loại bệnh khác nhau mà chỉ tốn đúng 4 bytes RAM!

```odin
package ecs

// Khai báo Enum các loại bệnh
Disease :: enum {
    Flu,            // Cúm
    FootAndMouth,   // Lở mồm
    Fungus,         // Nấm
    Rabies,         // Dại
}

// Khai báo Bit Set (chỉ chiếm 1 Byte nếu < 8 phần tử)
Diseases :: bit_set[Disease]

// Trong Component của động vật
AnimalComponent :: struct {
    type: AnimalType,
    diseases: Diseases,
}

// CÁCH SỬ DỤNG
system_disease :: proc() {
    cow := AnimalComponent{ type = .Cow }
    
    // 1. Thêm bệnh (Dùng toán tử +)
    cow.diseases += {.Flu, .Fungus} 
    
    // 2. Chữa khỏi bệnh (Dùng toán tử -)
    cow.diseases -= {.Fungus}
    
    // 3. Kiểm tra xem có đang bị Cúm không? (Dùng từ khóa "in")
    // Phép tính này thực chất là phép AND bitwise (CPU thực hiện trong 1 chu kỳ máy)
    if .Flu in cow.diseases {
        // Trừ máu con bò
    }
}
```

---

## 2. Data Locality & SoA (Tối ưu CPU Cache)

### Vấn đề:
Theo chuẩn OOP (Object-Oriented Programming), chúng ta thường gom tất cả dữ liệu vào 1 Object (`Array of Structs - AoS`). Ví dụ: class `Animal` chứa `Position, Health, Texture, AI_State`. Khi CPU duyệt qua mảng `Animals` chỉ để di chuyển (Position), nó bị bắt buộc phải tải cả `Health`, `Texture` vào CPU Cache L1, gây ra **Cache Miss** và làm chậm tốc độ vòng lặp cực kỳ khủng khiếp.

### Giải pháp ECS:
ECS là kiến trúc **Struct of Arrays (SoA)**. Dữ liệu được xẻ dọc.
Mọi Tọa độ (Position) của 10.000 con vật được xếp liền kề nhau trong thanh RAM thành 1 dải liên tục.
Trình biên dịch Odin còn cung cấp từ khóa `#soa` để bạn ép mảng thành dạng SoA tự động!

```odin
// Thay vì viết AoS:
entities: [10000]Entity

// Hãy dùng SoA để ép CPU chạy nhanh gấp 10 lần:
#soa entities: [10000]Entity
```
*Ghi chú: Việc tách rời `positions: [dynamic]Position` và `velocities: [dynamic]Velocity` mà chúng ta làm ở Chương 12 chính là SoA thủ công.*

---

## 3. Spatial Hashing (Tối ưu Va chạm & Tương tác)

### Vấn đề:
Khi bạn có 1.000 con gà, nếu dùng 2 vòng lặp lồng nhau `for i in 0..<1000` và `for j in 0..<1000` để cho chúng né nhau, bạn sẽ mất **$1.000 \times 1.000 = 1.000.000$** phép tính mỗi frame. Game sẽ tụt FPS thảm hại.

### Giải pháp: Phân vùng lưới (Grid Hashing)
Thay vì bắt gà A kiểm tra với 999 con còn lại, chúng ta sử dụng chính hệ tọa độ Grid của game nông trại.
Gà A đang đứng ở ô Grid `(5, 5)`, nó chỉ cần kiểm tra xem trong ô `(5, 5)` và 8 ô xung quanh có con gà nào khác không. Số phép tính giảm từ 1 triệu xuống còn... vài chục!

```odin
package ecs

// Key của Map (Tọa độ Grid)
GridPos :: struct {
    x, y: int,
}

// Bảng Băm (Spatial Hash)
// Mỗi ô đất sẽ lưu 1 danh sách các Entity đang dẫm lên nó
spatial_hash: map[GridPos][dynamic]EntityID

// Đầu mỗi Frame, làm sạch bảng băm
clear(&spatial_hash)

// Đăng ký vị trí của vạn vật vào bảng băm
for id, pos in positions {
    grid := GridPos{ int(pos.x / TILE_SIZE), int(pos.y / TILE_SIZE) }
    append(&spatial_hash[grid], id)
}

// Lúc kiểm tra va chạm:
// Chỉ cần lấy danh sách thực thể ở cùng ô Grid!
neighbors := spatial_hash[my_grid_pos]
```

---

## 4. Memory Arena & Temporary Allocator (Tối ưu Dọn Rác RAM)

### Vấn đề:
Hiệu ứng (Particles) như lá rơi, máu chảy, hạt nước... sinh ra và biến mất liên tục. Nếu bạn dùng lệnh `new` và `free` (cấp phát động trên Heap) liên tục mỗi frame, Game sẽ bị khựng (Stuttering) vì hệ điều hành phải đi xin xỏ bộ nhớ.

### Giải pháp:
Sử dụng `context.temp_allocator` của Odin. Đây là một bộ nhớ dạng Arena (khuôn viên khép kín). Bạn cứ tha hồ xả rác vào đó, rồi đến cuối Frame, bạn chỉ cần 1 dòng `free_all(context.temp_allocator)` để quét sạch mọi thứ trong O(1). Tuyệt đối không bao giờ rò rỉ bộ nhớ (Memory Leak)!

```odin
import "core:mem"

// Ở đầu hàm Update mỗi Frame
temp_arena: mem.Arena
mem.arena_init(&temp_arena, make([]byte, 1 * mem.Megabyte)) // Cấp 1MB
context.allocator = mem.arena_allocator(&temp_arena)

// Cứ thoải mái xả rác sinh hạt (Particle)
for i in 0..<1000 {
    p := new(Particle) 
}

// Cuối Frame: Dọn dẹp SẠCH BÁCH 1000 HẠT chỉ với 1 lệnh, nhanh gấp vạn lần "free" từng cái
mem.free_all(context.allocator)
```

---

## 5. Viewport Culling (Tối ưu Cạc Đồ Họa - GPU)

### Vấn đề:
Có 5000 cây lúa trên nông trại khổng lồ 2D. Nhưng màn hình người chơi (Camera) chỉ nhìn thấy được khoảng 100 cây lúa ở trung tâm. Nếu bạn vẫn cố gọi hàm `rl.DrawTexture` cho cả 5000 cây, GPU sẽ bị quá tải (Overdraw).

### Giải pháp: 
Lọc ra (Culling) những cây lúa nằm ngoài khung hình Camera để không gửi lệnh vẽ xuống Card đồ họa.

```odin
render_system :: proc(camera: rl.Camera2D) {
    // 1. Tính toán ranh giới khung hình Camera đang nhìn thấy
    screen_width := f32(rl.GetScreenWidth())
    screen_height := f32(rl.GetScreenHeight())
    
    view_left   := camera.target.x - (screen_width / 2.0) * camera.zoom
    view_right  := camera.target.x + (screen_width / 2.0) * camera.zoom
    view_top    := camera.target.y - (screen_height / 2.0) * camera.zoom
    view_bottom := camera.target.y + (screen_height / 2.0) * camera.zoom

    // 2. Lặp qua các thực thể
    for id, pos in ecs.positions {
        // Chỉ vẽ nếu thực thể nằm TRONG tầm nhìn của Camera
        if pos.x >= view_left && pos.x <= view_right &&
           pos.y >= view_top && pos.y <= view_bottom {
           
            rl.DrawTexture(...)
        }
    }
}
```

---

## 6. Texture Atlasing (Tối ưu Draw Calls)

### Vấn đề:
Mỗi lần đổi Texture (từ Ảnh cây cải sang Ảnh cây cà rốt), GPU phải đổi trạng thái (State Change) làm tốn 1 lệnh Draw Call. Càng nhiều Draw Call, Game càng giật.

### Giải pháp:
Gom tất cả ảnh của mọi loại cây trồng, vật nuôi vào **1 bức ảnh PNG khổng lồ (Sprite Sheet / Texture Atlas)**. Bạn chỉ cần Load ảnh đó 1 lần duy nhất, và dùng hàm `rl.DrawTextureRec` để "cắt" đúng ô hình chữ nhật chứa hình dáng cần thiết.
Từ 10.000 Draw Call sẽ giảm xuống còn **1 Draw Call duy nhất**.

```odin
// Vẽ từ Atlas (Chỉ dùng 1 biến tex_atlas duy nhất)
source_rect := rl.Rectangle{
    x = 32.0, // Tọa độ X trên tấm ảnh lớn
    y = 0.0,  // Tọa độ Y trên tấm ảnh lớn
    width = 32.0,
    height = 32.0,
}
rl.DrawTextureRec(tex_atlas, source_rect, rl.Vector2{pos.x, pos.y}, rl.WHITE)
```

---

## 7. Inline & Unroll (Ép trình biên dịch tối ưu Code)

### Vấn đề:
Các hàm toán học (như tính khoảng cách `rl.Vector2Distance`) được gọi hàng chục ngàn lần. Chi phí "nhảy vọt" (jump) trong CPU khi gọi hàm (Overhead Function Call) sẽ làm chậm game.

### Giải pháp:
Ngôn ngữ Odin cung cấp từ khóa ép trình biên dịch (Compiler Directives) `#force_inline` để copy-paste mã nguồn của hàm đó thẳng vào vòng lặp, bỏ qua chi phí gọi hàm. Và từ khóa `@(unroll)` để giải nén các vòng lặp for nhỏ.

```odin
// Ép trình biên dịch nhúng thẳng code tính khoảng cách
@force_inline
distance_sq :: proc(a, b: rl.Vector2) -> f32 {
    dx := a.x - b.x
    dy := a.y - b.y
    return dx*dx + dy*dy
}

// Ép trình biên dịch trải phẳng vòng lặp (Unroll)
@(unroll)
for i in 0..<4 {
    check_direction(i)
}
```

> (Bản cập nhật Bổ sung 13 Kỹ thuật Tối ưu Nâng cao)

---

## 8. Dirty Flags (Lazy Evaluation - Tối Ưu Tính Toán)

### Vấn đề:
Một số phép toán rất nặng (ví dụ: tính lại ma trận xoay Transform, hoặc tính toán Layout của UI). Nếu bạn đặt nó trong vòng lặp `Update` và chạy 60 lần/giây dù nhân vật đang đứng im, bạn đang lãng phí CPU.

### Giải pháp:
Sử dụng cờ `is_dirty`. Chỉ khi nào thực thể thực sự thay đổi vị trí hoặc thông số, cờ này mới bật lên `true`. Hệ thống sẽ kiểm tra cờ này, nếu `true` thì mới tính toán lại và trả cờ về `false`.

```odin
TransformComponent :: struct {
    position: rl.Vector2,
    rotation: f32,
    world_matrix: rl.Matrix,
    is_dirty: bool, // Cờ báo hiệu cần tính lại
}

// Khi di chuyển nhân vật
move_entity :: proc(t: ^TransformComponent, dx, dy: f32) {
    t.position.x += dx
    t.position.y += dy
    t.is_dirty = true // Bật cờ!
}

// Hệ thống tính toán (Chạy mỗi frame)
system_transform :: proc() {
    for t in transforms {
        if t.is_dirty {
            t.world_matrix = calculate_heavy_matrix(t.position, t.rotation)
            t.is_dirty = false // Tắt cờ sau khi tính xong
        }
    }
}
```

---

## 9. Tránh Branch Prediction Failure (Tối ưu Hot Loop)

### Vấn đề:
CPU hiện đại có tính năng "Đoán trước rẽ nhánh" (Branch Prediction). Nếu trong một vòng lặp 10.000 phần tử (Hot Loop) chứa quá nhiều lệnh `if - else` không có quy luật, CPU sẽ đoán sai liên tục, phải hủy toàn bộ công việc đang làm dở (Pipeline Flush), làm chậm game cực độ.

### Giải pháp:
Thay thế lệnh `if` bằng các phép toán hoặc lệnh bitwise để ép CPU tính toán trơn tru không rẽ nhánh (Branchless Programming). Hoặc gom các thực thể có cùng trạng thái (ví dụ: Đang ngủ) vào chung một mảng để chạy 1 vòng lặp không `if`.

---

## 10. Precomputed Look-Up Tables (LUT)

### Vấn đề:
Hàm lượng giác `math.sin()`, `math.cos()` hay `math.sqrt()` rất nặng. Nếu bạn có 10.000 hạt mưa rơi chéo góc, việc gọi hàm lượng giác cho từng hạt sẽ làm bốc khói CPU.

### Giải pháp:
Chỉ có 360 độ trong đường tròn. Hãy tính sẵn kết quả của 360 góc đó ngay khi mở game và lưu vào mảng `sin_table[360]`. Lúc vào game, tính toán chuyển thành phép lấy giá trị từ mảng O(1).

```odin
sin_table: [360]f32

init_math :: proc() {
    for i in 0..<360 {
        rad := f32(i) * rl.DEG2RAD
        sin_table[i] = math.sin(rad)
    }
}

// Lúc sử dụng (O(1) cực nhanh)
angle := 45
y_velocity := speed * sin_table[angle]
```

---

## 11. SIMD (Đơn Lệnh - Đa Dữ Liệu)

### Vấn đề:
CPU thông thường xử lý từng phép tính một (Scalar). Nếu bạn cần tính khoảng cách từ Player đến 4 con quái vật, CPU phải chạy 4 lần phép tính bình phương.

### Giải pháp:
Sử dụng các thanh ghi Vector của CPU (SSE, AVX) qua thư viện `core:simd` của Odin. Bạn nhét tọa độ của cả 4 con quái vật vào 1 thanh ghi 128-bit, và CPU sẽ tính ra kết quả cho cả 4 con CÙNG MỘT LÚC (Vectorization) trong đúng 1 chu kỳ máy.

---

## 12. Entity Object Pooling (Tái Sử Dụng ID)

### Vấn đề:
Hệ thống cấp phát bộ nhớ rất tốn kém. Việc tạo mới (`append`) và xóa (`ordered_remove`) Entity liên tục sẽ gây phân mảnh bộ nhớ và làm thay đổi vị trí của các phần tử khác trong mảng.

### Giải pháp:
Khi một thực thể "chết", đừng xóa nó khỏi bộ nhớ. Hãy đưa ID của nó vào một mảng `free_list`. Khi cần tạo thực thể mới, ưu tiên bốc ID từ `free_list` ra để xài lại (Tái sinh).

```odin
free_entities: [dynamic]EntityID

kill_entity :: proc(id: EntityID) {
    components[id].is_active = false
    append(&free_entities, id) // Cho vào kho đồ cũ
}

spawn_entity :: proc() -> EntityID {
    if len(free_entities) > 0 {
        return pop(&free_entities) // Tái sử dụng!
    }
    // Chỉ tạo mới nếu kho đã cạn
    return new_entity()
}
```

---

## 13. String Interning (Băm Chuỗi Số Nguyên)

### Vấn đề:
So sánh hai chuỗi ký tự `if name == "Cabbage"` tốn thời gian vì CPU phải duyệt từng chữ cái C-a-b-b-a-g-e.

### Giải pháp:
Trong các Game Engine, chuỗi được Băm (Hash) thành một số nguyên (ID) ngay từ lúc khởi tạo. Suốt quá trình game chạy, ta chỉ so sánh `if id == 1005`, tốc độ so sánh số nguyên là cực đỉnh.

---

## 14. Custom Context Allocator per System

### Vấn đề:
Việc cả Game dùng chung 1 bộ nhớ (Global Allocator) sẽ dẫn đến xung đột, phân mảnh khi hệ thống Âm thanh, Hình ảnh, Vật lý tranh nhau xin cấp phát RAM.

### Giải pháp:
Odin cho phép đổi `context.allocator` bất cứ lúc nào. Mỗi System sẽ có 1 Arena riêng. System Vật lý xài xong Arena của Vật lý thì xóa trắng, không ảnh hưởng gì đến Arena của Render.

---

## 15. Y-Sort bằng Insertion Sort (Tối ưu Vẽ Chồng)

### Vấn đề:
Trong game 2D góc nhìn từ trên xuống, nhân vật đứng dưới phải che khuất nhân vật đứng trên (Z-Ordering theo trục Y). Ta phải `sort` mảng thực thể mỗi frame. Dùng hàm Sort thông thường (QuickSort O(N log N)) cho 10.000 phần tử là quá dư thừa.

### Giải pháp:
Trong game, tọa độ Y của các thực thể gần như giống hệt Frame trước đó, mảng đã "gần như được sắp xếp sẵn". Thuật toán **Insertion Sort** là nhà vô địch tuyệt đối cho mảng đã sắp xếp sẵn (tiệm cận O(N)). 

---

## 16. Level of Detail (LOD) & Animation Skipping

### Vấn đề:
Vẽ quái vật ở xa thì đã có Viewport Culling lo (Không gửi lệnh Draw). Thế nhưng Hệ thống Animation (tính toán đổi khung hình) và AI vẫn đang chạy ngầm cho con quái đó!

### Giải pháp:
Nếu khoảng cách từ Quái đến Camera quá xa (VD: > 2000 pixels):
- Dừng chạy Animation Update.
- Giảm tần suất chạy AI (Thay vì update mỗi frame, chỉ cho phép AI nghĩ 1 lần mỗi giây).
Đây là cách các game MMO giữ cho server không bị cháy.

---

## 17. Broad-phase & Narrow-phase Collision

### Vấn đề:
Kiểm tra va chạm (Collision) chính xác đến từng pixel (Narrow-phase) bằng các thuật toán phức tạp như SAT hoặc check AABB tốn rất nhiều toán học.

### Giải pháp:
Luôn chia va chạm làm 2 bước:
- **Broad-phase (Thô):** Dùng Spatial Hash (Kỹ thuật số 3) để tìm ra 5 con quái vật gần nhất.
- **Narrow-phase (Tinh):** Lúc này mới dùng hàm tính va chạm hình tròn/chữ nhật cho 5 con đó. 

---

## 18. Event Bus (Giao Tiếp Không Chờ)

### Vấn đề:
Một con bò gọi hàm `UI.ShowText("-10 HP")`, rồi gọi hàm `Audio.Play("moo.wav")`. Con bò bị dính chặt (Coupled) với UI và Audio. Nếu Audio bị lỗi chờ load ổ cứng, cả con bò (và cả Game) bị đứng hình!

### Giải pháp:
Sử dụng kiến trúc Message Queue (Hàng đợi Sự kiện). Con bò chỉ cần đẩy 1 thẻ lệnh `Event{type = .Damage, id = 5}` vào Queue rồi chạy tiếp. Cuối frame, các System UI và Audio tự lấy thẻ lệnh ra xử lý sau.

---

## 19. Fixed Timestep (Chống Vòng Xoáy Tử Thần)

### Vấn đề:
Nếu đưa lệnh `x += speed * rl.GetFrameTime()` vào vòng lặp Render, khi game giật (FPS tụt còn 10), `GetFrameTime()` sẽ biến thành số rất to. Kết quả là nhân vật bước 1 bước xuyên thẳng qua tường (Collision lỗi).

### Giải pháp:
Tách rời Logic Vật Lý và Render. Ép Logic Vật lý luôn luôn chạy ở `1/60` giây không đổi (Fixed Timestep). Render có thể tụt FPS, nhưng Vật lý thì tuyệt đối phải ổn định.

---

## 20. Job System & Thread Pool (Đa Luồng Thực Sự)

### Vấn đề:
Thuật toán tìm đường (A* Pathfinding) cho nông dân tốn quá nhiều CPU. Nếu chạy trực tiếp trong Main Thread, game sẽ bị giật (Lag Spike) mỗi khi click chuột ra lệnh di chuyển xa.

### Giải pháp:
Sử dụng `core:thread` của Odin để đẩy tác vụ dò đường sang một lõi CPU khác (Worker Thread). Main Thread vẫn vẽ đồ họa mượt mà ở 60FPS. Khi Thread kia dò đường xong, nó trả kết quả về qua biến an toàn (Mutex/Atomic), nông dân bắt đầu chạy!

---

> Bằng việc kết hợp nhuần nhuyễn **20 công phu Tối Ưu Tối Thượng** kể trên, sếp hoàn toàn có thể tự tin thiết kế Game Engine riêng của mình và đẩy quy mô Nông Trại lên **giới hạn 100.000 thực thể chạy mượt mà 60FPS** trên một chiếc Laptop cùi bắp!
