import ursina, random
from ursina import Ursina, scene, Entity, Button, Vec3, distance, destroy, time, Text
from ursina.prefabs.first_person_controller import FirstPersonController

class Global:
    set_ok = 0
    sands = []
    sand_total = 0
    elapsed_time = 0.0
    width = 5
    height = 5
    start = 0
    Animations = []

import tkinter as tk
from tkinter import ttk, messagebox
def on_confirm():
    Global.set_ok = 1
    river_width = width_slider.get()
    river_height = height_slider.get()
    sediment_amount = sediment_slider.get()
    result_label.config(text=f"河宽: {river_width}, 河高: {river_height}, 泥沙量: {sediment_amount}")
    Global.width = round(river_width)
    Global.height = round(river_height)
    Global.sand_total = round(sediment_amount)
    root.destroy()
def update_width(*args):
    try:
        value = int(width_var.get())
        if 1 <= value <= 6:
            width_slider.set(value)
        else:
            messagebox.showwarning("输入错误", "河宽必须在1到6之间")
            width_var.set(str(Global.width))
    except ValueError:
        pass
def update_height(*args):
    try:
        value = int(height_var.get())
        if 1 <= value <= 6:
            height_slider.set(value)
        else:
            messagebox.showwarning("输入错误", "河高必须在1到6之间")
            height_var.set(str(Global.height))
    except ValueError:
        pass
def update_sediment(*args):
    try:
        value = int(sediment_var.get())
        if 1 <= value <= 100:
            sediment_slider.set(value)
        else:
            messagebox.showwarning("输入错误", "泥沙量必须在1到100之间")
            sediment_var.set(str(Global.sand_total))
    except ValueError:
        pass
root = tk.Tk()
root.title("河流参数设置")

def validate_integer_input(action, value_if_allowed, text, widget_name):
    if action == '1':
        if not value_if_allowed.isdigit() and (value_if_allowed != "" and not value_if_allowed.startswith("-")):
            return False
    return True
vcmd = (root.register(validate_integer_input), '%d', '%P', '%S', '%W')

# 创建河宽框架
width_frame = ttk.Frame(root)
width_frame.pack(pady=5)

width_label = ttk.Label(width_frame, text="河宽 (1-6):")
width_label.grid(row=0, column=0, padx=5, pady=5)

width_var = tk.StringVar(value="5")
width_var.trace_add("write", update_width)
width_entry = ttk.Entry(width_frame, textvariable=width_var, validate='key', validatecommand=vcmd, width=5)
width_entry.grid(row=0, column=1, padx=5, pady=5)

width_slider = ttk.Scale(width_frame, from_=1, to=6, orient='horizontal', variable=tk.IntVar(value=int(width_var.get())), length=200, command=lambda x: width_var.set(str(int(float(x)))))
width_slider.grid(row=0, column=2, padx=5, pady=5)

# 创建河高框架
height_frame = ttk.Frame(root)
height_frame.pack(pady=5)

height_label = ttk.Label(height_frame, text="河高 (1-6):")
height_label.grid(row=0, column=0, padx=5, pady=5)

height_var = tk.StringVar(value="5")
height_var.trace_add("write", update_height)
height_entry = ttk.Entry(height_frame, textvariable=height_var, validate='key', validatecommand=vcmd, width=5)
height_entry.grid(row=0, column=1, padx=5, pady=5)

height_slider = ttk.Scale(height_frame, from_=1, to=6, orient='horizontal', variable=tk.IntVar(value=int(height_var.get())), length=200, command=lambda x: height_var.set(str(int(float(x)))))
height_slider.grid(row=0, column=2, padx=5, pady=5)

# 创建泥沙量框架
sediment_frame = ttk.Frame(root)
sediment_frame.pack(pady=5)

sediment_label = ttk.Label(sediment_frame, text="泥沙量 (1-100):")
sediment_label.grid(row=0, column=0, padx=5, pady=5)

sediment_var = tk.StringVar(value="50")
sediment_var.trace_add("write", update_sediment)
sediment_entry = ttk.Entry(sediment_frame, textvariable=sediment_var, validate='key', validatecommand=vcmd, width=5)
sediment_entry.grid(row=0, column=1, padx=5, pady=5)

sediment_slider = ttk.Scale(sediment_frame, from_=1, to=100, orient='horizontal', variable=tk.IntVar(value=int(sediment_var.get())), length=200, command=lambda x: sediment_var.set(str(int(float(x)))))
sediment_slider.grid(row=0, column=2, padx=5, pady=5)

result_label = ttk.Label(root, text="由于引擎限制，参数将以英文显示")
result_label.pack(pady=10)
confirm_button = ttk.Button(root, text="确定", command=on_confirm)
confirm_button.pack(pady=10)
root.mainloop()

if Global.set_ok == 0:
    exit()

app = Ursina(title="束水攻沙演示")

v = int(900 / (Global.width * Global.height) / 7 // 1)+1
v_sand = int(v ** 3/10//1)+1
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
    for y in range(Global.height+1):
        for x in range(Global.width):
            if y == 0:
                Voxel2((x+1, y+1.01, z))
            else:
                Voxel2((x+1, y-0.02, z))

Global.sands.append(sand(speed=v_sand, start_position=(1+random.uniform(-0.1, 0.1), Global.height, 0), end_position=(1+random.uniform(-0.1, 0.1), Global.height, 9), now_position=(1+random.uniform(-0.1, 0.1), Global.height, random.uniform(0, 9))))

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
