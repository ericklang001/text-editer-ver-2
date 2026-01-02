import ctypes 
from tkinter import *

__all__ = ['WinManager']

class WinManager:
    def __init__(self):
        self.__first = None 
        self.__second = None 

        self.__init_first()


    def __init_first(self):
        self.__first = Tk()
        self.__first.config(bg='lightblue')


    def __init_second(self):
        self.__second = Tk()
        self.__second.geometry('1700x1200')
        self.__second.config(bg=__import__('test').theme['2']['window']['bg'])


    def start_second(self):
        self.__first.destroy()
        self.__first = None 

        self.__init_second()


    def start(self):
        if self.__first is None:
            return 
        self.__first.mainloop()


    def second_mainloop(self):
        if self.__second is None:
            return 
        self.__second.mainloop()


    def get_first(self):
        return self.__first
    

    def get_second(self):
        return self.__second 


if __name__ == '__main__':
    if hasattr(ctypes.windll.shcore, "SetProcessDpiAwareness"):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    winManager = WinManager()

    root = winManager.get_first()

    btn = Button(root, text='destroy', command=winManager.start_second)
    btn.pack(padx=5, pady=5)

    root.update_idletasks()

    winManager.start()
    