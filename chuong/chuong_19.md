# Chương 19: Đóng gói & Phát hành (Deployment & WASM)

Game hay đến mấy mà không đến được tay người chơi thì cũng vứt. Chương này hướng dẫn bạn đóng gói game thành sản phẩm hoàn chỉnh để đưa lên Steam hoặc Itch.io.

---

## 1. Biên dịch tối ưu tốc độ (Release Build)

Lệnh `odin run .` mà bạn hay dùng là **Debug Build**. Nó chứa rất nhiều mã kiểm tra lỗi (bounds checking, nil pointer), làm game chạy chậm đi một chút.

Khi đóng gói cho người chơi, bạn phải dùng cờ tối ưu hóa của Odin (`-o:speed`).

Mở Terminal và gõ:
```bash
odin build . -out:MyAwesomeGame.exe -o:speed
```
Lệnh này sẽ biên dịch ra một file `.exe` cực kỳ nhỏ gọn, chạy ở tốc độ bàn thờ (nhanh hơn từ 2x đến 5x so với lúc debug). Hơn nữa, nó tắt luôn cửa sổ Console đen ngòm phiền phức phía sau game (nếu bạn chạy trên Windows, thêm cờ `-subsystem:windows`).

## 2. Quản lý Tài sản (Asset Management)

Người chơi có thói quen tò mò. Nếu bạn để file `player.png` trong thư mục `assets/`, họ sẽ dễ dàng thay ảnh chế vào và làm hỏng game.

* **Giải pháp 1:** Nén toàn bộ thư mục `assets/` thành một file `.zip` (hoặc định dạng `.pak` tự chế). Bạn code một module đọc file trực tiếp từ trong file Zip đó đổ lên RAM (Raylib có hỗ trợ hàm `LoadFileData`).
* **Giải pháp 2 (Bá đạo hơn):** Ngôn ngữ Odin hỗ trợ lệnh `#load("assets/player.png")`. Lệnh này sẽ **nhúng thẳng** file ảnh vào bên trong file `.exe` dưới dạng mảng byte. Khi đó, game của bạn chỉ có ĐÚNG 1 FILE `.exe` duy nhất, không cần đính kèm thư mục nào cả!

## 3. Xuất xưởng lên Trình duyệt web (WebAssembly - WASM)

Hành vi người chơi hiện đại rất lười tải file `.exe`. Nếu game của bạn chơi được ngay trên web (trên nền tảng Itch.io chẳng hạn), lượt chơi sẽ tăng gấp 10 lần.

Sự kỳ diệu của Odin và Raylib là chúng đều hỗ trợ biên dịch thẳng ra **WASM**. Trình duyệt web (Chrome, Firefox) có thể chạy thẳng code biên dịch của bạn ở tốc độ gần tương đương với chạy app trên máy tính.

**Các bước khái quát:**
1. Cài đặt Emscripten SDK (Công cụ biên dịch C sang Web).
2. Tinh chỉnh lại Vòng lặp Game: Trình duyệt không cho phép bạn dùng `for !rl.WindowShouldClose()`. Bạn phải bóc phần thân của vòng lặp ra thành một hàm `UpdateDrawFrame()`, sau đó giao hàm này cho Emscripten tự động gọi thông qua `emscripten_set_main_loop`.
3. Biên dịch Odin với `target` là `freestanding_wasm32`.
4. Kết quả sẽ sinh ra file `game.wasm`, `game.js` và `index.html`. 
5. Đưa 3 file này lên Web Host và gửi link cho bạn bè thưởng thức!
