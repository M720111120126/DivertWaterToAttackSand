import ursina, random
from ursina import Ursina, scene, Entity, Button, Vec3, distance, destroy, time, Text
from ursina.prefabs.first_person_controller import FirstPersonController
from set_window import Global

app = Ursina(title="束水攻沙演示")

v = int(900 / (Global.width * Global.height) / 7 // 1)+1
v_sand = int(v ** 3/20//1)+1
Global.elapsed_time = 0.0

class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(parent=scene,
            position=position,
            model='cube', # pyright: ignore[reportArgumentType]
            origin_y=.5,
            texture='white_cube', # pyright: ignore[reportArgumentType]
            color=ursina.color.hsv(0, 0, ursina.random.uniform(.9, 1.0)), # pyright: ignore[reportArgumentType]
            highlight_color=ursina.color.lime,
        )

class Voxel2(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(parent=scene,
            position=position,
            model='cube', # pyright: ignore[reportArgumentType]
            origin_y=.5,
            color=ursina.color.hex('#aeaeaeb4'), # pyright: ignore[reportArgumentType]
        )

class water(Entity):
    def __init__(self, speed=2, start_position=(0,0,0), end_position=(0,0,0), now_position=(0,0,0)):
        super().__init__(model='cube', color=ursina.color.blue, scale=Vec3(0.2, 0.2, 0.5), position=now_position)
        self.speed = speed
        x, y, z = start_position
        self.start_position = Vec3(x, y, z)
        x, y, z = end_position
        self.end_position = Vec3(x, y, z)
        self.direction = (self.end_position - self.start_position).normalized() # pyright: ignore[reportOptionalMemberAccess]
    def update(self):
        if Global.start == 1:
            self.position += self.direction * self.speed * 0.02
            if (distance(self.position, self.end_position) < 0.1) or\
               (self.position.x > self.end_position.x and self.direction.x > 0) or \
               (self.position.x < self.end_position.x and self.direction.x < 0) or \
               (self.position.y > self.end_position.y and self.direction.y > 0) or \
               (self.position.y < self.end_position.y and self.direction.y < 0) or \
               (self.position.z > self.end_position.z and self.direction.z > 0) or \
               (self.position.z < self.end_position.z and self.direction.z < 0):
                self.position = self.start_position

class sand(Entity):
    def __init__(self, speed=2, start_position=(0,0,0), end_position=(0,0,0), now_position=(0,0,0)):
        super().__init__(model='cube', color=ursina.color.yellow, scale=Vec3(0.1, 0.1, 0.1), position=now_position)
        self.speed = speed
        x, y, z = start_position
        self.start_position = Vec3(x, y, z)
        x, y, z = end_position
        self.end_position = Vec3(x, y, z)
        self.direction = (self.end_position - self.start_position).normalized() # pyright: ignore[reportOptionalMemberAccess]

for z in range(10):
    for x in range(Global.width+2):
        voxel = Voxel(position=(x,0,z))
for z in range(10):
    for y in range(Global.height+1):
        Voxel(position=(0,y+1,z))
for z in range(10):
    for y in range(Global.height+1):
        Voxel(position=(Global.width+1,y+1,z))
for z in range(10):
    for x in range(Global.width):
        a = ursina.Animation('water_still.gif', position=(x+1, Global.height, z), scale=1, rotation_x=90, rotation_y=90)
        a.pause()
        Global.Animations.append(a)
        water(speed=v, start_position=(x+1, Global.height-0.09, 0), end_position=(x+1, Global.height-0.09, 9), now_position=(x+1, Global.height-0.09, z))

for z in range(10):
    for y in range(Global.height):
        for x in range(Global.width):
            if y+1 == Global.height:
                Voxel2((x+1, y+0.98, z))
            else:
                Voxel2((x+1, y+1, z))
for x in range(Global.width):
    Global.sands.append(sand(speed=v_sand, start_position=(x+1+random.uniform(-0.1, 0.1), Global.height, 0), end_position=(x+1+random.uniform(-0.1, 0.1), Global.height, 9), now_position=(x+1+random.uniform(-0.1, 0.1), Global.height, random.uniform(0, 9))))

Text.default_resolution = 1080 * Text.size
info_panel = Text(
    text=f"""River Global.width: {Global.width}
River Depth: {Global.height}
Flow Speed (V): {v}
Remaining Sand: {Global.sand_total}
Elapsed Time: {Global.elapsed_time:.2f}""",
    position=(-0.65, 0.45),
    background=True
)

def update():
    if Global.start == 1:
        Global.elapsed_time += time.dt # pyright: ignore[reportAttributeAccessIssue]
        for sand_info in Global.sands:
            direction = (sand_info.end_position - sand_info.position).normalized()
            sand_info.position += direction * sand_info.speed * time.dt # pyright: ignore[reportAttributeAccessIssue]
            if (distance(sand_info.position, sand_info.end_position) < 0.1) or\
               (sand_info.position.x > sand_info.end_position.x and sand_info.direction.x > 0) or \
               (sand_info.position.x < sand_info.end_position.x and sand_info.direction.x < 0) or \
               (sand_info.position.y > sand_info.end_position.y and sand_info.direction.y > 0) or \
               (sand_info.position.y < sand_info.end_position.y and sand_info.direction.y < 0) or \
               (sand_info.position.z > sand_info.end_position.z and sand_info.direction.z > 0) or \
               (sand_info.position.z < sand_info.end_position.z and sand_info.direction.z < 0):
                if Global.sand_total > 1:
                    x_new = random.uniform(0, Global.width)+1
                    sand_info.end_position = Vec3(x_new, Global.height, 9)
                    sand_info.position = Vec3(x_new, Global.height, 0)
                    Global.sand_total -= 1
                else:
                    Global.sand_total = 0
                    sand_info.visible = False
                    Global.start = 2
                    for i in Global.Animations:
                        i.pause()
        info_panel.text=f"""River Global.width: {Global.width}
River Depth: {Global.height}
Flow Speed (V): {v}
Remaining Sand: {Global.sand_total}
Elapsed Time: {Global.elapsed_time:.2f}"""

def input(key):
    if "p up" == key:
        if Global.start == 0:
            Global.start = 1
            for i in Global.Animations:
                i.start()
    if "space" in key:
        player.y += 0.5
    if "shift" in key:
        player.y -= 0.5

ursina.Sky()

player = FirstPersonController(gravity=0, speed=8)
player.z = -2
player.x = 1

app.run()
