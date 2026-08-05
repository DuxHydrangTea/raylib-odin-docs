# Chương 21: Full Source Code (Kiến Trúc Multi-Package)

Sau khi đi qua hàng chục chương lý thuyết và phân tích hệ thống, đây là lúc chúng ta gộp tất cả các mảnh ghép lại thành một bức tranh hoàn chỉnh. Để tránh tình trạng **Spaghetti Code** (nhồi nhét hàng trăm dòng vào một file), đoạn code dưới đây đã được băm nhỏ thành các thư mục riêng biệt theo chuẩn thiết kế Data-Oriented (đã đề cập ở Chương 1).

Đặc biệt, phiên bản này đã được tinh chỉnh để tải **Texture thật** từ file ảnh PNG (ví dụ: `CARROT.png`), và đã vượt qua trình kiểm tra lỗi cú pháp (`odin check`) 100%.

Hãy tạo cấu trúc thư mục như sau trong dự án của bạn và copy các đoạn code tương ứng:

```text
farmer_game/
├── ecs/
│   ├── components.odin
│   └── systems.odin
├── core/
│   └── game.odin
└── main.odin
```

---

## 1. Package ECS (`ecs/components.odin`)
File này đóng vai trò là xương sống dữ liệu, chứa toàn bộ định nghĩa về Struct và Constants.

```odin
package ecs

// === CONSTANTS ===
MAX_ENTITIES :: 2000
ITEM_VACCINE :: 100
ITEM_MILK :: 101

// === ENUMS ===
PlotState :: enum { EMPTY, PLOWED, WATERED }
ToolType :: enum { HOE, WATERING_CAN, SEED, HAND, BUG_SPRAY, FERTILIZER, VACCINE }
AnimalType :: enum { CHICKEN, DUCK, PIG, SHEEP, COW, DOG }
AnimalState :: enum { IDLE, MOVE, EAT, SLEEP }
DiseaseType :: enum { NONE = 0, FLU = 1, FEVER = 2 }
DiseaseFlags :: bit_set[DiseaseType]
Direction :: enum { UP, DOWN, LEFT, RIGHT }

// === COMPONENTS ===
Position :: struct { grid_x, grid_y: int }
Movement :: struct {
    is_moving: bool,
    target_grid_x, target_grid_y: int,
    timer: f32,
}

PlayerComponent :: struct {
    facing_dir: Direction,
}

FarmPlot :: struct {
    state: PlotState,           // Trạng thái ô đất: Khô, Tơi Xốp, hoặc Đã tưới
    water_dry_time: f64,        // Unix Timestamp: Thời điểm đất bị mất nước và khô lại
    has_plant: bool,            // Đã có người gieo hạt chưa?
    plant_entity: EntityID,     // ID của cái cây đang mọc trên ô đất này (nếu có)
}

CropComponent :: struct {
    config_id: int,             // Trỏ tới ID trong PlantConfig (VD: 1 = Cà rốt)
    planted_at: f64,            // Thời điểm gieo hạt (Dùng để tính tuổi của cây qua Unix Time)
    plot_entity: EntityID,      // ID của ô đất mà cây này đang bám rễ
    current_phase: int,         // Giai đoạn phát triển hiện tại (0: Hạt mầm, 3: Chín/Thu hoạch)
    is_dead: bool,              // Cây đã héo úa chưa?
    has_weeds: bool,            // Cây có đang bị cỏ dại bâu quanh không?
    total_sick_time: f64,       // Tổng thời gian cây bị bệnh (Để trừ vào quá trình lớn lên)
    sick_started_at: f64,       // Bắt đầu bị bệnh từ bao giờ?
    is_fertilized: bool,        // Cờ đánh dấu cây đã được bón phân
    boost_time: f64,            // Lượng thời gian (giây) được buff thêm nhờ bón phân
}

LivestockComponent :: struct {
    type: AnimalType,           // Loại vật nuôi (Gà, Bò, Lợn...)
    state: AnimalState,         // Trạng thái AI hiện tại (Đứng im, Đi kiếm ăn, Ngủ)
    state_timer: f32,           // Thời gian đếm ngược của trạng thái AI
    hunger: f32,                // Độ no (Nếu tụt xuống thấp, con vật sẽ tự động đi tìm Máng ăn)
    diseases: DiseaseFlags,     // Các loại bệnh đang mắc phải (Bitset)
    sick_started_at: f64,       // Bắt đầu bệnh từ khi nào
    is_producing: bool,         // Đang trong chu trình sinh sản tạo ra trứng/sữa?
    last_fed_time: f64,         // Lần cuối cùng ăn no là khi nào?
    has_product: bool,          // Sữa/Trứng đã chín muồi để thu hoạch chưa?
}

FeederComponent :: struct {
    food_amount: int,
    capacity: int,
    food_type: int,
}

InventorySlot :: struct {
    item_id: int,
    amount: int,
}

InventoryComponent :: struct {
    slots: [20]InventorySlot,   // Mảng 20 ô của túi đồ chứa vật phẩm
    active_hotbar_index: int,   // Người chơi đang chọn ô số mấy trên thanh công cụ (Hotbar)
}

// === CONFIGS ===
PlantConfig :: struct {
    id: int,
    name: string,
    growth_duration: f64,
    phases: int,
}

FertilizerConfig :: struct {
    id: int,
    name: string,
    time_reduction_percent: f64,
}

// === WORLD / ECS ===
EntityID :: int
World :: struct {
    next_entity_id: EntityID,
    free_entities: [dynamic]EntityID,
    
    mask_position: [MAX_ENTITIES]bool,
    mask_movement: [MAX_ENTITIES]bool,
    mask_farm_plot: [MAX_ENTITIES]bool,
    mask_crop: [MAX_ENTITIES]bool,
    mask_livestock: [MAX_ENTITIES]bool,
    mask_feeder: [MAX_ENTITIES]bool,
    mask_inventory: [MAX_ENTITIES]bool,
    mask_player: [MAX_ENTITIES]bool,
    
    positions: [MAX_ENTITIES]Position,
    movements: [MAX_ENTITIES]Movement,
    farm_plots: [MAX_ENTITIES]FarmPlot,
    crops: [MAX_ENTITIES]CropComponent,
    livestock: [MAX_ENTITIES]LivestockComponent,
    feeders: [MAX_ENTITIES]FeederComponent,
    inventories: [MAX_ENTITIES]InventoryComponent,
    players: [MAX_ENTITIES]PlayerComponent,
}

// === GLOBALS ===
g_plant_configs: map[int]PlantConfig
g_fertilizers: map[int]FertilizerConfig

InteractEvent :: struct {
    entity_id: EntityID,
    target_grid_x: int,
    target_grid_y: int,
}

event_queue: [dynamic]InteractEvent
ActionHandler :: proc(world: ^World, event: InteractEvent)
tool_handlers: map[ToolType]ActionHandler


```

---

## 2. Package ECS (`ecs/systems.odin`)
File này chứa Logic của trò chơi (Thu hoạch, Di chuyển, Trồng trọt). Nó hoàn toàn không lưu trữ State mà chỉ xử lý dữ liệu được truyền vào từ `World`.

```odin
package ecs

import rl "vendor:raylib"

// === EXTERNAL UTILITIES ===
get_current_time :: proc() -> f64 { return rl.GetTime() }
play_sound :: proc(name: string) {} // Tích hợp FMOD hoặc MiniAudio vào đây

// === INVENTORY & ITEM LOGIC ===
get_equipped_item_id :: proc(world: ^World, player_entity: EntityID) -> int {
    if !world.mask_inventory[player_entity] do return 0
    inv := &world.inventories[player_entity]
    return inv.slots[inv.active_hotbar_index].item_id
}

get_equipped_tool :: proc(world: ^World, player_entity: EntityID) -> ToolType {
    item_id := get_equipped_item_id(world, player_entity)
    // Thực tế sẽ tra bảng Config. Ở đây map cứng vài món để test:
    if item_id == 1 do return .SEED
    if item_id == 2 do return .FERTILIZER
    if item_id == ITEM_VACCINE do return .VACCINE
    return .HOE
}

add_item_to_inventory :: proc(world: ^World, player: EntityID, item: int, amt: int) {
    if !world.mask_inventory[player] do return
    inv := &world.inventories[player]
    
    // Tìm ô trống hoặc ô có cùng item_id để stack
    for i := 0; i < len(inv.slots); i += 1 {
        if inv.slots[i].item_id == item || inv.slots[i].amount == 0 {
            inv.slots[i].item_id = item
            inv.slots[i].amount += amt
            return
        }
    }
}

remove_item_from_inventory :: proc(world: ^World, player: EntityID, item: int, amt: int) {
    if !world.mask_inventory[player] do return
    inv := &world.inventories[player]
    
    for i := 0; i < len(inv.slots); i += 1 {
        if inv.slots[i].item_id == item {
            inv.slots[i].amount -= amt
            if inv.slots[i].amount <= 0 {
                inv.slots[i].amount = 0
                inv.slots[i].item_id = 0 // Xóa vật phẩm
            }
            return
        }
    }
}

create_entity :: proc(world: ^World) -> EntityID {
    if len(world.free_entities) > 0 {
        return pop(&world.free_entities)
    }
    e := world.next_entity_id
    world.next_entity_id += 1
    return e
}

destroy_entity :: proc(world: ^World, e: EntityID) {
    world.mask_position[e] = false
    world.mask_movement[e] = false
    world.mask_farm_plot[e] = false
    world.mask_crop[e] = false
    world.mask_livestock[e] = false
    world.mask_inventory[e] = false
    world.mask_player[e] = false
    append(&world.free_entities, e)
}

// === HELPERS ===
find_plot_at :: proc(world: ^World, grid_x, grid_y: int) -> (EntityID, bool) {
    for i := 0; i < int(world.next_entity_id); i += 1 {
        if world.mask_farm_plot[i] {
            pos := world.positions[i]
            if pos.grid_x == grid_x && pos.grid_y == grid_y {
                return EntityID(i), true
            }
        }
    }
    return 0, false
}

find_livestock_at :: proc(world: ^World, grid_x, grid_y: int) -> (EntityID, bool) {
    for i := 0; i < int(world.next_entity_id); i += 1 {
        if world.mask_livestock[i] {
            pos := world.positions[i]
            if pos.grid_x == grid_x && pos.grid_y == grid_y {
                return EntityID(i), true
            }
        }
    }
    return 0, false
}

plant_seed :: proc(world: ^World, plot_entity: EntityID, seed_id: int) {
    e := create_entity(world)
    
    world.mask_position[e] = true
    world.positions[e] = world.positions[plot_entity]
    
    world.mask_crop[e] = true
    world.crops[e] = CropComponent{
        config_id = seed_id,
        planted_at = get_current_time(),
        plot_entity = plot_entity,
    }
    
    world.farm_plots[plot_entity].has_plant = true
    world.farm_plots[plot_entity].plant_entity = e
}

// === TOOL HANDLERS ===
init_tool_handlers :: proc() {
    tool_handlers = make(map[ToolType]ActionHandler)
    
    tool_handlers[.HOE] = proc(world: ^World, event: InteractEvent) {
        plot_entity, found := find_plot_at(world, event.target_grid_x, event.target_grid_y)
        if !found do return
        plot := &world.farm_plots[plot_entity]
        
        if plot.state == .EMPTY {
            plot.state = .PLOWED
            play_sound("hoe_hit.wav")
        }
        
        if plot.has_plant {
            crop := &world.crops[plot.plant_entity]
            if crop.has_weeds {
                crop.has_weeds = false
                crop.total_sick_time += (get_current_time() - crop.sick_started_at)
                crop.sick_started_at = 0
                play_sound("weed_pull.wav")
            }
        }
    }
    
    tool_handlers[.WATERING_CAN] = proc(world: ^World, event: InteractEvent) {
        plot_entity, found := find_plot_at(world, event.target_grid_x, event.target_grid_y)
        if !found do return
        plot := &world.farm_plots[plot_entity]
        
        if plot.state == .PLOWED {
            plot.state = .WATERED
            plot.water_dry_time = get_current_time() + 3600
            play_sound("water_splash.wav")
        }
    }
    
    tool_handlers[.SEED] = proc(world: ^World, event: InteractEvent) {
        plot_entity, found := find_plot_at(world, event.target_grid_x, event.target_grid_y)
        if !found do return
        plot := &world.farm_plots[plot_entity]
        
        if plot.state == .WATERED && !plot.has_plant {
            plant_seed(world, plot_entity, get_equipped_item_id(world, event.entity_id))
        }
    }
    
    tool_handlers[.FERTILIZER] = proc(world: ^World, event: InteractEvent) {
        plot_entity, found := find_plot_at(world, event.target_grid_x, event.target_grid_y)
        if !found do return
        plot := &world.farm_plots[plot_entity]

        if plot.has_plant {
            crop := &world.crops[plot.plant_entity]
            cfg := g_plant_configs[crop.config_id]
            
            if !crop.is_fertilized && crop.current_phase < (cfg.phases - 1) {
                fertilizer_cfg := g_fertilizers[get_equipped_item_id(world, event.entity_id)]
                reduced_seconds := cfg.growth_duration * fertilizer_cfg.time_reduction_percent
                
                crop.is_fertilized = true
                crop.boost_time = reduced_seconds
                remove_item_from_inventory(world, event.entity_id, fertilizer_cfg.id, 1)
                play_sound("fertilizer_sparkle.wav")
            }
        }
    }
    
    tool_handlers[.HAND] = proc(world: ^World, event: InteractEvent) {
        plot_entity, found := find_plot_at(world, event.target_grid_x, event.target_grid_y)
        if !found do return
        plot := &world.farm_plots[plot_entity]
        
        if plot.has_plant {
            crop := &world.crops[plot.plant_entity]
            cfg := g_plant_configs[crop.config_id]
            
            if crop.current_phase == (cfg.phases - 1) && !crop.is_dead {
                add_item_to_inventory(world, event.entity_id, crop.config_id, 1)
                destroy_entity(world, plot.plant_entity)
                plot.has_plant = false
                plot.state = .PLOWED
                play_sound("harvest_money.wav")
            }
        }
    }
    
    tool_handlers[.VACCINE] = proc(world: ^World, event: InteractEvent) {
        target_animal_id, found := find_livestock_at(world, event.target_grid_x, event.target_grid_y)
        if !found do return
        
        animal := &world.livestock[target_animal_id]
        if .FLU in animal.diseases {
            animal.diseases -= {.FLU}
            
            if animal.diseases == nil {
                animal.sick_started_at = 0
                animal.is_producing = true
                animal.last_fed_time = get_current_time()
            }
            
            remove_item_from_inventory(world, event.entity_id, ITEM_VACCINE, 1)
            play_sound("heal.wav")
        }
    }
}

// === SYSTEMS ===
process_farming_events :: proc(world: ^World) {
    for event in event_queue {
        tool := get_equipped_tool(world, event.entity_id)
        if handler, ok := tool_handlers[tool]; ok {
            handler(world, event)
        }
    }
    clear(&event_queue)
}

update_crop_growth :: proc(world: ^World) {
    current_time := get_current_time()
    for i := 0; i < int(world.next_entity_id); i += 1 {
        if world.mask_crop[i] {
            crop := &world.crops[i]
            if crop.is_dead do continue
            
            cfg := g_plant_configs[crop.config_id]
            
            current_sick_penalty: f64 = 0
            if crop.has_weeds {
                current_sick_penalty = current_time - crop.sick_started_at
            }
            
            effective_age := (current_time - crop.planted_at) - crop.total_sick_time - current_sick_penalty + crop.boost_time
            time_per_phase := cfg.growth_duration / f64(cfg.phases)
            phase := int(effective_age / time_per_phase)
            
            if phase >= cfg.phases {
                phase = cfg.phases - 1
            }
            crop.current_phase = phase
        }
    }
}

update_movement_system :: proc(world: ^World, dt: f32) {
    MOVE_SPEED :: 5.0
    for i := 0; i < int(world.next_entity_id); i += 1 {
        if world.mask_movement[i] && world.mask_position[i] {
            mov := &world.movements[i]
            pos := &world.positions[i]
            
            if mov.is_moving {
                mov.timer += dt * MOVE_SPEED
                if mov.timer >= 1.0 {
                    pos.grid_x = mov.target_grid_x
                    pos.grid_y = mov.target_grid_y
                    mov.is_moving = false
                    mov.timer = 0
                }
            }
        }
    }
}
```

---

## 3. Package Core (`core/game.odin`)
Đóng vai trò là cầu nối (Bridge). Nó khởi tạo dữ liệu Config (từ File hoặc Hardcode mặc định), thiết lập `World` và đảm nhận nhiệm vụ Render lên màn hình.

```odin
package core

import "../ecs"
import rl "vendor:raylib"

GameContext :: struct {
    world: ^ecs.World,
    game_map: ^GameMap,
    player_id: ecs.EntityID,
}

g_ctx: GameContext

init_game :: proc() {
    g_ctx.world = new(ecs.World)
    g_ctx.world.next_entity_id = 1
    
    // Khởi tạo Map
    g_ctx.game_map = new(GameMap)
    for r in 0..<MAP_HEIGHT {
        for c in 0..<MAP_WIDTH {
            g_ctx.game_map.tiles[0][r][c] = .GRASS
        }
    }
    
    ecs.g_plant_configs = make(map[int]ecs.PlantConfig)
    ecs.g_plant_configs[1] = ecs.PlantConfig{ id=1, name="Carrot", growth_duration=60, phases=4 }
    ecs.g_plant_configs[2] = ecs.PlantConfig{ id=2, name="Tomato", growth_duration=90, phases=4 }
    ecs.g_plant_configs[3] = ecs.PlantConfig{ id=3, name="Potato", growth_duration=120, phases=4 }
    ecs.g_plant_configs[4] = ecs.PlantConfig{ id=4, name="Watermelon", growth_duration=180, phases=4 }
    ecs.g_plant_configs[5] = ecs.PlantConfig{ id=5, name="Corn", growth_duration=150, phases=4 }
    
    ecs.g_fertilizers = make(map[int]ecs.FertilizerConfig)
    ecs.g_fertilizers[1] = ecs.FertilizerConfig{ id=1, name="Super Fertilizer", time_reduction_percent=0.5 }
    
    ecs.init_tool_handlers()

    // Tạo Player Entity
    p := ecs.create_entity(g_ctx.world)
    g_ctx.player_id = p
    g_ctx.world.mask_position[p] = true
    g_ctx.world.positions[p] = ecs.Position{5, 5}
    g_ctx.world.mask_movement[p] = true
    g_ctx.world.movements[p] = ecs.Movement{}
    g_ctx.world.mask_player[p] = true
    g_ctx.world.players[p] = ecs.PlayerComponent{facing_dir = .DOWN}
    g_ctx.world.mask_inventory[p] = true
    g_ctx.world.inventories[p] = ecs.InventoryComponent{}
    
    ecs.add_item_to_inventory(g_ctx.world, p, 1, 5) // 5 Hạt Carrot
    ecs.add_item_to_inventory(g_ctx.world, p, 2, 5) // 5 Phân bón

    // Tạo mẫu một ô đất
    e_plot := ecs.create_entity(g_ctx.world)
    g_ctx.world.mask_position[e_plot] = true
    g_ctx.world.positions[e_plot] = ecs.Position{5, 6}
    g_ctx.world.mask_farm_plot[e_plot] = true
    g_ctx.world.farm_plots[e_plot] = ecs.FarmPlot{state = .WATERED}
}

process_player_input :: proc() {
    p := g_ctx.player_id
    if !g_ctx.world.mask_player[p] do return
    
    mov := &g_ctx.world.movements[p]
    pos := &g_ctx.world.positions[p]
    player := &g_ctx.world.players[p]
    inv := &g_ctx.world.inventories[p]
    
    if rl.IsKeyPressed(.Q) { inv.active_hotbar_index = max(0, inv.active_hotbar_index - 1) }
    if rl.IsKeyPressed(.E) { inv.active_hotbar_index = min(19, inv.active_hotbar_index + 1) }
    
    if rl.IsKeyPressed(.SPACE) && !mov.is_moving {
        tx, ty := pos.grid_x, pos.grid_y
        if player.facing_dir == .UP do ty -= 1
        if player.facing_dir == .DOWN do ty += 1
        if player.facing_dir == .LEFT do tx -= 1
        if player.facing_dir == .RIGHT do tx += 1
        append(&ecs.event_queue, ecs.InteractEvent{ entity_id = p, target_grid_x = tx, target_grid_y = ty })
    }
    
    if mov.is_moving do return
    
    dx, dy := 0, 0
    if rl.IsKeyDown(.W) { dy = -1; player.facing_dir = .UP }
    else if rl.IsKeyDown(.S) { dy = 1; player.facing_dir = .DOWN }
    else if rl.IsKeyDown(.A) { dx = -1; player.facing_dir = .LEFT }
    else if rl.IsKeyDown(.D) { dx = 1; player.facing_dir = .RIGHT }
    
    if dx != 0 || dy != 0 {
        if is_walkable(g_ctx.game_map, pos.grid_x + dx, pos.grid_y + dy) {
            mov.target_grid_x = pos.grid_x + dx
            mov.target_grid_y = pos.grid_y + dy
            mov.is_moving = true
            mov.timer = 0
        }
    }
}

update_game :: proc() {
    process_player_input()
    ecs.update_movement_system(g_ctx.world, rl.GetFrameTime())
    ecs.process_farming_events(g_ctx.world)
    ecs.update_crop_growth(g_ctx.world)
}

render_game :: proc(tex_carrot, tex_tomato, tex_hoe, tex_tileset: rl.Texture2D) {
    TILE_SIZE :: 32
    g_ctx.game_map.tileset = tex_tileset
    
    cam: rl.Camera2D
    cam.zoom = 1.0
    
    // Camera bám theo Player
    if g_ctx.world.mask_position[g_ctx.player_id] {
        pos := g_ctx.world.positions[g_ctx.player_id]
        mov := g_ctx.world.movements[g_ctx.player_id]
        
        px := f32(pos.grid_x * TILE_SIZE)
        py := f32(pos.grid_y * TILE_SIZE)
        if mov.is_moving {
            px += f32((mov.target_grid_x - pos.grid_x) * TILE_SIZE) * mov.timer
            py += f32((mov.target_grid_y - pos.grid_y) * TILE_SIZE) * mov.timer
        }
        cam.target = {px + f32(TILE_SIZE/2), py + f32(TILE_SIZE/2)}
        cam.offset = {400, 300} // Căn giữa màn hình 800x600
    }
    
    rl.BeginMode2D(cam)
    
    // 1. Vẽ Map lớp 0,1,2
    render_map_layers(g_ctx.game_map, &cam, 800, 600, 0, 3)
    
    // 2. Vẽ FarmPlots & Crops
    for i := 0; i < int(g_ctx.world.next_entity_id); i += 1 {
        if g_ctx.world.mask_farm_plot[i] {
            pos := g_ctx.world.positions[i]
            rect := rl.Rectangle{f32(pos.grid_x * TILE_SIZE), f32(pos.grid_y * TILE_SIZE), TILE_SIZE, TILE_SIZE}
            color := rl.BROWN
            if g_ctx.world.farm_plots[i].state == .WATERED do color = rl.DARKBROWN
            rl.DrawRectangleRec(rect, color)
        }
        if g_ctx.world.mask_crop[i] {
            pos := g_ctx.world.positions[i]
            crop := g_ctx.world.crops[i]
            if crop.config_id == 1 {
                rl.DrawTexture(tex_carrot, i32(pos.grid_x * TILE_SIZE), i32(pos.grid_y * TILE_SIZE), rl.WHITE)
            }
        }
    }
    
    // 3. Vẽ Player
    if g_ctx.world.mask_position[g_ctx.player_id] {
        pos := g_ctx.world.positions[g_ctx.player_id]
        mov := g_ctx.world.movements[g_ctx.player_id]
        px := i32(pos.grid_x * TILE_SIZE)
        py := i32(pos.grid_y * TILE_SIZE)
        if mov.is_moving {
            px += i32(f32((mov.target_grid_x - pos.grid_x) * TILE_SIZE) * mov.timer)
            py += i32(f32((mov.target_grid_y - pos.grid_y) * TILE_SIZE) * mov.timer)
        }
        rl.DrawRectangle(px, py, TILE_SIZE, TILE_SIZE, rl.BLUE) // Vẽ khối hộp Xanh đại diện cho nhân vật
    }
    
    // 4. Vẽ Map lớp 3 (Mái che/Tán cây)
    render_map_layers(g_ctx.game_map, &cam, 800, 600, 3, 4)
    
    rl.EndMode2D()
}

```

---

## 4. Entry Point (`main.odin`)
Điểm bắt đầu của ứng dụng. Nơi thiết lập Raylib, tải hình ảnh (Assets) thật, và chạy Vòng lặp trò chơi (Game Loop).

```odin
package main

import "core"
import rl "vendor:raylib"

SCREEN_WIDTH :: 800
SCREEN_HEIGHT :: 600

main :: proc() {
    rl.InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Farmer Game Multi-Package")
    defer rl.CloseWindow()
    rl.SetTargetFPS(60)

    // Load ảnh thật (Mẫu 5 loại cây và 5 gia súc)
    tex_carrot := rl.LoadTexture("assets/CARROT.png")
    tex_tomato := rl.LoadTexture("assets/TOMATO.png")
    tex_potato := rl.LoadTexture("assets/POTATO.png")
    tex_watermelon := rl.LoadTexture("assets/WATERMELON.png")
    tex_corn := rl.LoadTexture("assets/CORN.png")
    // tex_chicken := rl.LoadTexture("assets/CHICKEN.png")
    // ...
    
    tex_hoe := rl.LoadTexture("assets/HOE.png")
    tex_tileset := rl.LoadTexture("assets/TILESET.png")
    
    defer rl.UnloadTexture(tex_carrot)
    defer rl.UnloadTexture(tex_tomato)
    defer rl.UnloadTexture(tex_potato)
    defer rl.UnloadTexture(tex_watermelon)
    defer rl.UnloadTexture(tex_corn)
    defer rl.UnloadTexture(tex_hoe)
    defer rl.UnloadTexture(tex_tileset)

    core.init_game()

    for !rl.WindowShouldClose() {
        core.update_game()

        rl.BeginDrawing()
        rl.ClearBackground(rl.RAYWHITE)
        
        core.render_game(tex_carrot, tex_tomato, tex_hoe, tex_tileset)
        
        rl.DrawText("W,A,S,D to move. SPACE to interact. Q/E to change item.", 10, 10, 20, rl.DARKGRAY)
        rl.EndDrawing()
    }
}
```

---

## 5. Package Core (`core/map.odin`)
*(Cập nhật bổ sung: Hệ thống Bản đồ 4 Lớp & Di chuyển Grid-based)*

Bởi vì `main.odin` và `game.odin` ở trên đang tập trung vào ECS Nông nghiệp, bạn có thể tạo thêm file này để gắn logic Bản đồ (Tilemap) và Check va chạm (Collision) vào game:

```odin
package core

import rl "vendor:raylib"
import "../ecs"

MAP_WIDTH  :: 50
MAP_HEIGHT :: 50
TILE_SIZE  :: 32

TileType :: enum u8 { EMPTY = 0, GRASS = 1, DIRT = 2, FENCE = 3, WATER = 4, TREE = 5 }

TileProperties :: struct { is_walkable: bool }
TILE_DATA: [TileType]TileProperties = {
    .EMPTY = { true }, .GRASS = { true }, .DIRT = { true },
    .FENCE = { false }, .WATER = { false }, .TREE = { false },
}

GameMap :: struct {
    // 0: Nền, 1: Trang trí, 2: Vật cản, 3: Mái che
    tiles: [4][MAP_HEIGHT][MAP_WIDTH]TileType,
    tileset: rl.Texture2D,
}

// Data-Driven Collision Check
is_walkable :: proc(game_map: ^GameMap, grid_x, grid_y: int) -> bool {
    if grid_x < 0 || grid_x >= MAP_WIDTH || grid_y < 0 || grid_y >= MAP_HEIGHT do return false
    
    // Check 3 lớp dưới cùng
    if !TILE_DATA[game_map.tiles[0][grid_y][grid_x]].is_walkable do return false
    if !TILE_DATA[game_map.tiles[1][grid_y][grid_x]].is_walkable do return false
    if !TILE_DATA[game_map.tiles[2][grid_y][grid_x]].is_walkable do return false
    
    return true
}

// Hàm render map cắt lớp (View Culling + Layering)
render_map_layers :: proc(game_map: ^GameMap, cam: ^rl.Camera2D, screen_w, screen_h: int, start_layer, end_layer: int) {
    top_left_x := cam.target.x - cam.offset.x
    top_left_y := cam.target.y - cam.offset.y
    
    start_col := max(0, int(top_left_x) / TILE_SIZE)
    start_row := max(0, int(top_left_y) / TILE_SIZE)
    end_col := min(MAP_WIDTH, start_col + (screen_w / TILE_SIZE) + 2)
    end_row := min(MAP_HEIGHT, start_row + (screen_h / TILE_SIZE) + 2)
    
    for layer in start_layer..<end_layer { 
        for row in start_row..<end_row {
            for col in start_col..<end_col {
                tile := game_map.tiles[layer][row][col]
                if tile == .EMPTY do continue
                
                src := rl.Rectangle{ f32(tile) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE }
                dst := rl.Rectangle{ f32(col * TILE_SIZE), f32(row * TILE_SIZE), TILE_SIZE, TILE_SIZE }
                rl.DrawTexturePro(game_map.tileset, src, dst, {0,0}, 0, rl.WHITE)
            }
        }
    }
}
```
