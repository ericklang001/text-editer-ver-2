import tkinter as tk
import ctypes 

ctypes.windll.shcore.SetProcessDpiAwareness(1)

def show_input_popup(event):
    # 创建临时弹窗
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)  # 无边框
    popup.geometry(f"+{event.x_root}+{event.y_root}")
    popup.attributes("-topmost", True)
    
    entry = tk.Entry(popup, width=20)
    entry.pack(padx=5, pady=5)
    entry.focus_set()
    
    def on_submit(event=None):
        value = entry.get()
        print("Input:", value)
        popup.destroy()
    
    entry.bind("<Return>", on_submit)
    entry.bind("<Escape>", lambda e: popup.destroy())
    popup.bind("<FocusOut>", lambda e: popup.destroy())  # 失焦关闭（可选）


def show_input_popup_2(event):
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    popup.geometry(f'+{event.x_root}+{event.y_root}')
    popup.attributes("-topmost", True)

    entry = tk.Entry(popup, width=20, font='Consolas 16 normal')
    entry.pack(padx=5, pady=5)
    entry.focus_set()

    def on_submit(event):
        value = entry.get()
        print('Input: ', value)
        popup.destroy()
    
    entry.bind('<Return>', on_submit)
    entry.bind('<Escape>', lambda event: popup.destroy())
    entry.bind('<FocusOut>', lambda event: popup.destroy())


root = tk.Tk()
root.geometry("400x300")
root.bind("<Button-3>", show_input_popup_2)  # 右键弹出
root.mainloop()

