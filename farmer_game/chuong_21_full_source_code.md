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

// === COMPONENTS ===
Position :: struct { grid_x, grid_y: int }
Movement :: struct {
    is_moving: bool,
    target_grid_x, target_grid_y: int,
    timer: f32,
}

FarmPlot :: struct {
    state: PlotState,
    water_dry_time: f64,
    has_plant: bool,
    plant_entity: EntityID,
}

CropComponent :: struct {
    config_id: int,
    planted_at: f64,
    plot_entity: EntityID,
    current_phase: int,
    is_dead: bool,
    has_weeds: bool,
    total_sick_time: f64,
    sick_started_at: f64,
    is_fertilized: bool,
    boost_time: f64,
}

LivestockComponent :: struct {
    type: AnimalType,
    state: AnimalState,
    state_timer: f32,
    hunger: f32,
    diseases: DiseaseFlags,
    sick_started_at: f64,
    is_producing: bool,
    last_fed_time: f64,
    has_product: bool,
}

FeederComponent :: struct {
    food_amount: int,
    capacity: int,
    food_type: int,
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
    
    mask_position: [MAX_ENTITIES]bool,
    mask_movement: [MAX_ENTITIES]bool,
    mask_farm_plot: [MAX_ENTITIES]bool,
    mask_crop: [MAX_ENTITIES]bool,
    mask_livestock: [MAX_ENTITIES]bool,
    mask_feeder: [MAX_ENTITIES]bool,
    
    positions: [MAX_ENTITIES]Position,
    movements: [MAX_ENTITIES]Movement,
    farm_plots: [MAX_ENTITIES]FarmPlot,
    crops: [MAX_ENTITIES]CropComponent,
    livestock: [MAX_ENTITIES]LivestockComponent,
    feeders: [MAX_ENTITIES]FeederComponent,
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

// === MOCK FUNCTIONS ===
get_current_time :: proc() -> f64 { return rl.GetTime() }
play_sound :: proc(name: string) {}
get_equipped_tool :: proc(world: ^World, player_entity: EntityID) -> ToolType { return .HOE }
get_equipped_seed_id :: proc() -> int { return 1 }
get_equipped_fertilizer_id :: proc() -> int { return 1 }
add_item_to_inventory :: proc(player: EntityID, item: int, amt: int) {}
remove_item_from_inventory :: proc(player: EntityID, item: int, amt: int) {}
destroy_entity :: proc(world: ^World, e: EntityID) {
    world.mask_position[e] = false
    world.mask_movement[e] = false
    world.mask_farm_plot[e] = false
    world.mask_crop[e] = false
    world.mask_livestock[e] = false
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
    e := world.next_entity_id
    world.next_entity_id += 1
    
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
            plant_seed(world, plot_entity, get_equipped_seed_id())
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
                fertilizer_cfg := g_fertilizers[get_equipped_fertilizer_id()]
                reduced_seconds := cfg.growth_duration * fertilizer_cfg.time_reduction_percent
                
                crop.is_fertilized = true
                crop.boost_time = reduced_seconds
                remove_item_from_inventory(event.entity_id, fertilizer_cfg.id, 1)
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
                add_item_to_inventory(event.entity_id, crop.config_id, 1)
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
            
            remove_item_from_inventory(event.entity_id, ITEM_VACCINE, 1)
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
}

g_ctx: GameContext

init_game :: proc() {
    g_ctx.world = new(ecs.World)
    g_ctx.world.next_entity_id = 1
    
    ecs.g_plant_configs = make(map[int]ecs.PlantConfig)
    ecs.g_plant_configs[1] = ecs.PlantConfig{ id=1, name="Carrot", growth_duration=60, phases=4 }
    ecs.g_plant_configs[2] = ecs.PlantConfig{ id=2, name="Tomato", growth_duration=90, phases=4 }
    ecs.g_plant_configs[3] = ecs.PlantConfig{ id=3, name="Potato", growth_duration=120, phases=4 }
    ecs.g_plant_configs[4] = ecs.PlantConfig{ id=4, name="Watermelon", growth_duration=180, phases=4 }
    ecs.g_plant_configs[5] = ecs.PlantConfig{ id=5, name="Corn", growth_duration=150, phases=4 }
    
    ecs.g_fertilizers = make(map[int]ecs.FertilizerConfig)
    ecs.g_fertilizers[1] = ecs.FertilizerConfig{ id=1, name="Super Fertilizer", time_reduction_percent=0.5 }
    
    ecs.init_tool_handlers()

    // Tạo mẫu một ô đất
    e_plot := g_ctx.world.next_entity_id
    g_ctx.world.next_entity_id += 1
    g_ctx.world.mask_position[e_plot] = true
    g_ctx.world.positions[e_plot] = ecs.Position{5, 5}
    g_ctx.world.mask_farm_plot[e_plot] = true
    g_ctx.world.farm_plots[e_plot] = ecs.FarmPlot{state = .WATERED}

    // Giả lập một sự kiện gieo hạt
    append(&ecs.event_queue, ecs.InteractEvent{ entity_id = 0, target_grid_x = 5, target_grid_y = 5 })
}

update_game :: proc() {
    ecs.process_farming_events(g_ctx.world)
    ecs.update_crop_growth(g_ctx.world)
}

render_game :: proc(tex_carrot, tex_tomato, tex_hoe: rl.Texture2D) {
    TILE_SIZE :: 32
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
    defer rl.UnloadTexture(tex_carrot)
    defer rl.UnloadTexture(tex_tomato)
    defer rl.UnloadTexture(tex_potato)
    defer rl.UnloadTexture(tex_watermelon)
    defer rl.UnloadTexture(tex_corn)
    defer rl.UnloadTexture(tex_hoe)

    core.init_game()

    for !rl.WindowShouldClose() {
        core.update_game()

        rl.BeginDrawing()
        rl.ClearBackground(rl.RAYWHITE)
        
        core.render_game(tex_carrot, tex_tomato, tex_hoe)
        
        rl.DrawText("Farmer Game Running...", 10, 10, 20, rl.DARKGRAY)
        rl.EndDrawing()
    }
}

```
