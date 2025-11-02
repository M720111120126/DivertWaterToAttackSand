import tkinter as tk
from tkinter import ttk, messagebox

class Global:
    set_ok = 0
    sands = []
    sand_total = 0
    elapsed_time = 0.0
    width = 5
    height = 5
    start = 0
    Animations = []

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