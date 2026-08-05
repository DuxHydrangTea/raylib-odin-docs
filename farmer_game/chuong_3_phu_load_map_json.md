# Chương 3 (Phụ): Khởi tạo Bản Đồ bằng File JSON (Data-Driven Map)

Trong các bài học trước, chúng ta đã khởi tạo bản đồ bằng hai vòng lặp `for` lồng nhau. Điều này ổn để test game, nhưng trong thực tế sản xuất, không ai code cứng bản đồ bằng tay cả. Thay vào đó, ta sử dụng các phần mềm chuyên dụng (như **Tiled Map Editor**) để vẽ bản đồ trực quan bằng chuột, sau đó xuất ra file **JSON**. 

Chương này sẽ hướng dẫn bạn cách đọc file JSON đó vào game bằng thư viện có sẵn của Odin, đồng thời giải thích cách mà **Hệ thống xử lý vật thể không thể đi xuyên** sẽ tự động kích hoạt mà không cần bạn phải code thêm dòng nào!

---

## 0. Quy trình Làm Game thực tế (Từ Vẽ đến Code)

Vì bạn chưa từng tiếp xúc với công cụ vẽ map, hãy hình dung quy trình 5 bước cực kỳ đơn giản sau:

1. **Chuẩn bị Nguyên liệu (Tileset):** Bạn cần một tấm ảnh PNG lớn chứa tập hợp tất cả các hình ảnh viên gạch (cỏ, đất, cây, nước). Trong tấm ảnh này, mỗi loại gạch được đánh một số thứ tự (ID). Ví dụ: Cỏ là số 1, Đất là 2, Cây là 5.
2. **Vẽ Bản Đồ (Trên phần mềm Tiled):** Bạn nhập tấm ảnh PNG đó vào phần mềm Tiled. Sau đó, bạn dùng chuột chọn hình Cây (ID = 5) và click "bôi" lên màn hình y hệt như đang dùng cọ vẽ trong MS Paint.
3. **Lưu Trữ (Export):** Khi vẽ xong một ngôi làng lộng lẫy, bạn bấm nút **"Lưu thành file JSON"**.
4. **Phần mềm tự dịch ra Số:** Phần mềm sẽ tự động quét qua bức tranh bạn vừa vẽ, dịch từng nét cọ của bạn thành các con số ID tương ứng. Sau đó nó nhóm tất cả các con số này thành một hàng ngang thật dài và lưu vào mảng `"data"`.
5. **Nhiệm vụ của Code Game:** Code Odin của chúng ta không cần biết bạn đã vẽ đẹp thế nào. Nó chỉ việc mở file JSON kia lên, đọc mảng `"data"`, thấy số 1 thì in hình Cỏ ra màn hình, thấy số 5 thì in hình Cây ra màn hình ở đúng tọa độ đó. Mọi thứ hiện lên chính xác 100%!

---

## 1. Cấu trúc File JSON của một Bản Đồ (map.json)

Khi bạn xuất bản đồ từ Tiled ra định dạng JSON, một phiên bản đơn giản hóa của nó sẽ trông như sau:

```json
{
  "width": 50,
  "height": 50,
  "tilewidth": 32,
  "tileheight": 32,
  "layers": [
    {
      "name": "Background",
      "data": [1, 1, 1, 1, 4, 4, 1, 1, 1, "...(rút gọn 2491 phần tử nữa)..."] 
    },
    {
      "name": "Decoration",
      "data": [0, 0, 2, 0, 0, 0, 0, 0, 0, "...(rút gọn 2491 phần tử nữa)..."]
    },
    {
      "name": "Collision",
      "data": [0, 3, 3, 3, 0, 0, 0, 0, 0, "...(rút gọn 2491 phần tử nữa)..."]
    },
    {
      "name": "Canopy",
      "data": [0, 0, 0, 5, 5, 5, 0, 0, 0, "...(rút gọn 2491 phần tử nữa)..."]
    }
  ]
}
```

**Giải thích Cấu trúc JSON:**
- `width` và `height`: Số lượng ô lưới (Tile) theo chiều ngang và dọc (Ví dụ: Bản đồ rộng 50x50 ô).
- `tilewidth` và `tileheight`: Kích thước pixel của mỗi viên gạch (Ví dụ: 32x32 pixel).
- `layers`: Mảng chứa các Lớp đồ họa (Layer). Mỗi lớp tương đương với 1 mặt phẳng chồng lên nhau.
  - `name`: Tên của lớp để ta dễ phân biệt (Background, Decoration, Collision...).
  - `data`: Chứa dữ liệu định vị các viên gạch.

> [!NOTE]
> Mảng `data` trong JSON là **Mảng 1 Chiều** trải dài từ trái qua phải, từ trên xuống dưới. Nếu map có kích thước 50x50, mảng này sẽ có chính xác 2500 phần tử. Các con số bên trong đại diện cho ID của từng loại gạch (ánh xạ trực tiếp với Enum `TileType` của chúng ta):
> - `0`: Ô trống (.EMPTY)
> - `1`: Bãi cỏ (.GRASS)
> - `2`: Đất bùn (.DIRT)
> - `3`: Hàng rào (.FENCE)
> - `4`: Nước (.WATER)
> - `5`: Cây cối (.TREE)

---

## 2. Khai báo Struct để Ánh Xạ JSON (JSON Unmarshaling)

Odin có thư viện `core:encoding/json` hỗ trợ ánh xạ (đổ dữ liệu) cực mạnh. Bạn chỉ cần định nghĩa một Struct có cấu trúc y hệt file JSON, hệ thống sẽ tự động gán giá trị cho bạn.

```odin
package core

import "core:encoding/json"
import "core:os"
import "core:fmt"

// Khai báo struct ánh xạ với Layer trong JSON
JsonLayer :: struct {
    name: string,
    data: []int, // Odin tự động cấp phát mảng 1 chiều chứa dữ liệu
}

// Khai báo struct gốc chứa toàn bộ File
JsonMapData :: struct {
    width: int,
    height: int,
    tilewidth: int,
    tileheight: int,
    layers: []JsonLayer,
}
```

---

## 3. Thuật toán Đọc JSON và Bơm vào `GameMap`

Bây giờ ta viết một hàm `load_map_from_json()`. Nhiệm vụ của nó là đọc mảng 1 chiều từ Struct JSON, dùng phép chia `(/)` và phép chia lấy dư `(%)` để tách nó thành tọa độ 3 Chiều `[layer][row][col]` trong GameMap.

```odin
load_map_from_json :: proc(filepath: string) -> ^GameMap {
    // Đọc nội dung file thành chuỗi byte
    data, ok := os.read_entire_file_from_filename(filepath)
    if !ok {
        fmt.eprintfln("Lỗi: Không thể tìm thấy file %s", filepath)
        return nil
    }
    defer delete(data) // Giải phóng bộ nhớ tạm sau khi đọc xong

    // Chuẩn bị Struct rỗng để Odin tự động đổ dữ liệu vào
    parsed_json: JsonMapData
    err := json.unmarshal(data, &parsed_json)
    if err != nil {
        fmt.eprintfln("Lỗi parse JSON: %v", err)
        return nil
    }
    defer json.destroy_value(parsed_json) // Xóa dữ liệu rác sau khi parse

    // Tạo GameMap thực sự để Game sử dụng
    game_map := new(GameMap)
    
    // Thuật toán ánh xạ từ 1 Chiều -> 3 Chiều
    map_w := parsed_json.width
    
    for layer_idx := 0; layer_idx < len(parsed_json.layers); layer_idx += 1 {
        // Tránh bị Crash nếu JSON có nhiều hơn 4 Lớp
        if layer_idx >= 4 do break 
        
        layer_data := parsed_json.layers[layer_idx].data
        
        for i := 0; i < len(layer_data); i += 1 {
            tile_id := layer_data[i]
            if tile_id == 0 do continue // Bỏ qua ô trống
            
            row := i / map_w // Tìm Tọa độ Y
            col := i % map_w // Tìm Tọa độ X
            
            // Ép kiểu từ Int (JSON) sang TileType (Enum)
            game_map.tiles[layer_idx][row][col] = TileType(tile_id)
        }
    }
    
    return game_map
}
```

Bạn chỉ việc gọi hàm này trong `init_game()`:
```odin
g_ctx.game_map = load_map_from_json("assets/map.json")
```

---

## 4. Tại sao Ta Không Cần Viết Thêm Code Check Va Chạm?

Câu hỏi lớn: **"Làm sao để đánh dấu và xử lý các vật thể không thể đi xuyên từ file JSON?"**

Trái với cách code OOP thông thường (Bạn phải duyệt qua map JSON, thấy số 3 thì tạo ra đối tượng `FenceObject`, gắn `Collider`, v.v...), nhờ kiến trúc **Data-Oriented Design**, chúng ta... **không cần làm gì cả!**

Bạn còn nhớ mảng Cấu Hình Tính Chất (`TILE_DATA`) mà ta tạo ra ở Chương 3 chứ?

```odin
TileType :: enum u8 { EMPTY = 0, GRASS = 1, DIRT = 2, FENCE = 3, WATER = 4, TREE = 5 }

TileProperties :: struct { is_walkable: bool }
TILE_DATA: [TileType]TileProperties = {
    .EMPTY = { true }, .GRASS = { true }, .DIRT = { true },
    .FENCE = { false }, .WATER = { false }, .TREE = { false }, // <--- Chặn đường!
}
```

Khi bạn load file JSON, nếu ở tọa độ `(X=10, Y=5)` người vẽ map đặt Gốc Cây (ID = 5) vào Lớp số 2 (Layer Vật cản). Mảng `game_map.tiles[2][5][10]` sẽ tự động mang giá trị là `.TREE`.

Đến khi người chơi bấm nút sang phải tiến vào ô `(10, 5)`. Hàm `is_walkable()` của chúng ta sẽ quét qua các lớp như sau:

```odin
is_walkable :: proc(game_map: ^GameMap, grid_x, grid_y: int) -> bool {
    // Quét Lớp 0 (Đất)
    if !TILE_DATA[game_map.tiles[0][grid_y][grid_x]].is_walkable do return false
    
    // Quét Lớp 1 (Trang trí)
    if !TILE_DATA[game_map.tiles[1][grid_y][grid_x]].is_walkable do return false
    
    // Quét Lớp 2 (Vật cản) ---> Gặp .TREE!
    // TILE_DATA[.TREE].is_walkable == false!
    if !TILE_DATA[game_map.tiles[2][grid_y][grid_x]].is_walkable do return false
    
    return true
}
```

Ngay lập tức nó trả về `false`. Nhân vật bị chặn đứng!

### Tổng kết

Đó chính là sức mạnh của **Data-Driven Architecture**. Bạn tách biệt hoàn toàn giữa **Dữ liệu Hình ảnh** (Từ file JSON) và **Dữ liệu Logic** (`TILE_DATA`). Dù Designer có vẽ thêm 10 bản đồ mới, quăng cả hồ nước hay vách đá vào, Programmer (là bạn) cũng không phải sửa dù chỉ một dòng code Logic va chạm nào. Hệ thống tự động trơn tru dựa trên bảng tra cứu Lookup Table!
