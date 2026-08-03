# Chương 8: Ánh sáng, Hoà trộn màu và Shaders

Trong chương này, chúng ta sẽ vượt ra khỏi ranh giới của những mảng màu đơn điệu để bước vào thế giới xử lý hình ảnh GPU. Đây là bí quyết đằng sau những thanh gươm laser rực rỡ, vòng phép thuật phát sáng và các bộ lọc màu (Instagram-like filters) trong game.

---

## 1. Chế độ Hoà trộn (Blend Mode)

Thông thường, khi bạn vẽ đè hình A lên hình B, GPU sẽ dùng thông số Alpha (độ trong suốt) của hình A để che đi một phần hình B. Chế độ đó gọi là **Alpha Blend** (mặc định).

Tuy nhiên, có một chế độ hòa trộn rất kỳ diệu là **Additive Blend** (Cộng gộp màu sắc). Khi 2 màu cộng lại với nhau, chúng sẽ có xu hướng tiến về màu Trắng (cháy sáng).

### Ứng dụng: Tạo ánh sáng, Lửa, Tia Laser, Hạt nổ (Particles)

* **`BeginBlendMode(mode: BlendMode)`**
* **`EndBlendMode()`**

```odin
rl.BeginDrawing()
    rl.ClearBackground(rl.BLACK) // Bầu trời đêm

    // 1. Vẽ các vật thể bình thường
    rl.DrawRectangle(50, 50, 100, 100, rl.BLUE)

    // 2. Bật Additive Blend để vẽ hiệu ứng cháy sáng
    rl.BeginBlendMode(.ADDITIVE)
        // Vẽ nhiều vòng tròn mờ xếp chồng lên nhau
        // Khi cộng gộp lại, vùng tâm sẽ phát sáng chói lọi!
        rl.DrawCircle(100, 100, 40, rl.Color{255, 100, 0, 50}) // Cam nhạt
        rl.DrawCircle(100, 100, 20, rl.Color{255, 200, 0, 100}) // Vàng
        rl.DrawCircle(100, 100, 5, rl.WHITE) // Lõi trắng
    rl.EndBlendMode()

rl.EndDrawing()
```

---

## 2. Viết Shaders (GLSL)

Shader là những đoạn mã nhỏ xíu nhưng cực kỳ mạnh mẽ, chạy trên hàng ngàn luồng (threads) của GPU cùng một lúc. Nó được viết bằng ngôn ngữ GLSL (OpenGL Shading Language).
Ở game 2D, chúng ta chủ yếu dùng **Fragment Shader** (Xử lý từng điểm ảnh/pixel).

### 2.1. Tải Shader
* **`LoadShader(vsFileName, fsFileName: cstring) -> Shader`**
  * Tác dụng: Tải Vertex Shader và Fragment Shader. Thường thì làm game 2D bạn chỉ cần Fragment Shader, nên tham số đầu tiên cứ truyền `nil`.
  ```odin
  my_shader := rl.LoadShader(nil, "assets/grayscale.fs")
  defer rl.UnloadShader(my_shader)
  ```

### 2.2. Áp dụng Shader
Bạn sẽ bọc lệnh vẽ (thường là vẽ cái RenderTexture ở Chương 7 ra màn hình) vào giữa `BeginShaderMode` và `EndShaderMode`.

```odin
rl.BeginShaderMode(my_shader)
    // Toàn bộ hình ảnh vẽ trong này sẽ bị biến đổi bởi Shader!
    rl.DrawTexturePro(canvas_tex, source, dest, {0,0}, 0, rl.WHITE)
rl.EndShaderMode()
```

### 2.3. Ví dụ một File Fragment Shader (`grayscale.fs`)
Shader dưới đây biến toàn bộ màn hình thành màu xám (rất hay dùng khi nhân vật cạn máu hoặc Pause game).
```glsl
#version 330
in vec2 fragTexCoord;
in vec4 fragColor;
out vec4 finalColor;
uniform sampler2D texture0; // Ảnh gốc được Raylib tự động truyền vào

void main()
{
    // Lấy màu gốc của pixel hiện tại
    vec4 texelColor = texture(texture0, fragTexCoord);
    
    // Tính toán độ sáng (Luminance) bằng công thức tiêu chuẩn
    float gray = dot(texelColor.rgb, vec3(0.299, 0.587, 0.114));
    
    // Gán lại màu xám
    finalColor = vec4(gray, gray, gray, texelColor.a);
}
```

---

## 3. Truyền biến số (Uniforms) vào Shader

Giả sử bạn muốn màn hình bị mờ dần thành màu đỏ tùy thuộc vào Lượng máu của người chơi. Bạn phải truyền biến `HP` từ mã Odin vào trong mã GLSL Shader. Biến đó gọi là **Uniform**.

* **`GetShaderLocation(shader: Shader, uniformName: cstring) -> c.int`**: Tìm vị trí của biến trong Shader.
* **`SetShaderValue(shader: Shader, locIndex: c.int, value: rawptr, uniformType: ShaderUniformDataType)`**: Gửi giá trị vào Shader.

```odin
// Lấy vị trí của biến "hp_ratio" trong Shader
hp_loc := rl.GetShaderLocation(my_shader, "hp_ratio")

// Gửi giá trị máu (từ 0.0 đến 1.0) vào Shader
hp_val: f32 = current_hp / max_hp
rl.SetShaderValue(my_shader, hp_loc, &hp_val, .FLOAT)
```

---

## Tổng kết
Kết hợp **RenderTexture (Chương 7)** và **Shader/BlendMode (Chương 8)** là cách các Engine chuyên nghiệp như Unity, Godot tạo ra hệ thống **Post-Processing (Xử lý hậu kỳ)**. Bạn có thể tự viết bộ lọc Bloom, Chromatic Aberration hay CRT Scanline cho tựa game Raylib của mình.
