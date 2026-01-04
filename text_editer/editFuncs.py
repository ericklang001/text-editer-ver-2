import ctypes 
import re 
from tkinter import *

__all__ = ['ColorChooser', 'PopupMenu']

class ColorChooser:
    created = []
    def __init__(self, master, text, mode, tag_dict, update, x, y):
        if len(ColorChooser.created) > 0:
            return 
        
        self.master = master
        self.text = text
        self.mode = mode 
        self.tag_dict = tag_dict
        self.update_tag_dict = update 
        ColorChooser.created.append(self)

        self.region = None 
        self.init_widgets(x, y)
        
    def init_widgets(self, x, y):
        self.top = Toplevel(self.master)
        self.top.overrideredirect(True)
        self.top.geometry(f'+{x}+{y}')

        self.region = Frame(self.top, relief='groove', bd=2)
        self.region.pack(padx=5, pady=10)
        
        self.lab = Label(self.region, bg='#000000', height=2)
        self.red = Scale(self.region, from_=0, to=255, orient='horizontal', length=250, troughcolor='red')
        self.green = Scale(self.region, from_=0, to=255, orient='horizontal', length=250, troughcolor='green')
        self.blue = Scale(self.region, from_=0, to=255, orient='horizontal', length=250, troughcolor='blue')
        self.value = Label(self.region, text='#000000', font='Consolas 12 bold')
        self.use = Label(self.region, text='<confirm>', font='Consolas 12 bold')
                
        self.lab.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='news')
        self.red.grid(row=1, column=0, columnspan=2, padx=5, sticky='we')
        self.green.grid(row=2, column=0, columnspan=2, padx=5, sticky='we')
        self.blue.grid(row=3, column=0, columnspan=2, padx=5, sticky='we')
        self.value.grid(row=4, column=0, padx=5, pady=5, sticky='we')
        self.use.grid(row=4, column=1, padx=5, pady=5, sticky='we')

        self.use.bind('<Button-1>', lambda event: self.confirm(event))
        self.region.bind('<Button-3>', lambda event: self.clear(event))
        self.master.bind('<Button-1>', lambda event: self.focus_lost(event))
        self.red.config(command=self.color_change)
        self.green.config(command=self.color_change)
        self.blue.config(command=self.color_change)

    def color_change(self, *args):
        red, green, blue = self.red.get(), self.green.get(), self.blue.get()
        value = '#{:02x}{:02x}{:02x}'.format(red, green, blue)
        self.value.config(text=value, fg=value)
        self.lab.config(bg=value)
        

    def clear(self, event):
        self.top.destroy()
        ColorChooser.created.clear()
        self.master.unbind('<Button-1>')

    def focus_lost(self, event):
        x, y = event.x_root, event.y_root 
        if not (self.region.winfo_x() < x <self.region.winfo_x()+self.region.winfo_width()
                and self.region.winfo_y() < y < self.region.winfo_y()+self.region.winfo_height()):
            self.top.destroy()
            self.master.unbind('<Button-1>')
            ColorChooser.created.clear()

    def confirm(self, event):
        color = self.value['text']
        try:
            start = self.text.index(SEL_FIRST)
            end = self.text.index(SEL_LAST)
            if self.mode == 'fg':
                tag_label = f'fg_{color}'
                self.text.tag_config(tag_label, foreground=color)
            else:
                tag_label = f'bg_{color}'
                self.text.tag_config(tag_label, background=color)
            
            self.update_tag_dict(tag_label, start, end, self.mode)
            self.text.tag_add(tag_label, start, end)
        except Exception as e:
            print(e)
        finally:
            self.clear(event)
            return 'break'


class PopupMenu:
    def __init__(self, master, text: Text, theme_code='4'):
        self.master = master 
        self.text = text 
        self.theme_code = theme_code

        self.menu = None 
        self.x = 0
        self.y = 0 

        self.bg='white'
        self.fg='black'
        self.active_fg = 'white'
        self.active_bg = 'pink'
        

        self.tag_dict = {}
        self.tag_count = 0

        self.__text_tag_add()
        self.__bind_events()
        self.__init__data()

    def popup(self, event):
        self.x = event.x_root 
        self.y = event.y_root 
        self.__init_widgets(event)


    def __text_tag_add(self):
        self.text.tag_config('underline', underline=True)
        self.text.tag_config('deleteline', overstrike=True)
        self.text.tag_config('bold', font=self.text['font'].replace('normal', 'bold'))
        self.text.tag_config('normal', font=self.text['font'].replace('bold', 'normal'))


    def __init__data(self):
        self.font_sizes = [8, 9, 10, 12, 14, 16, 20, 25, 32, 40, 50, 64, 100]
        self.font_types = ['Times', 'Consolas', '微软雅黑', '新宋体']


    def __init_widgets(self, event):
        if self.menu is not None:
            self.menu.destroy()
        
        win_color = __import__('theme').theme[self.theme_code]['window']
        self.menu = Menu(self.master, tearoff='false', fg = win_color['menu fg'], 
                        bg = win_color['menu bg'],
                        activeforeground=win_color['menu active fg'], 
                        activebackground=win_color['menu active bg'])
        self.menu.add_command(label='underline', command=self.underline)
        self.menu.add_command(label='deleteline', command=self.deleteline)
        self.menu.add_command(label='bold', command=self.bold)
        self.menu.add_command(label='normal', command=self.normal)
        self.menu.add_command(label='foreground', command=lambda: self.set_color('foreground'))
        self.menu.add_command(label='background', command=lambda: self.set_color('background'))

        self.font_size_cascade = Menu(self.menu, tearoff='false', fg = win_color['menu fg'], 
                        bg = win_color['menu bg'],
                        activeforeground=win_color['menu active fg'], 
                        activebackground=win_color['menu active bg'])
        self.menu.add_cascade(label='font-size', menu=self.font_size_cascade)

        self.font_type_cascade = Menu(self.menu, tearoff='false', fg = win_color['menu fg'], 
                        bg = win_color['menu bg'],
                        activeforeground=win_color['menu active fg'], 
                        activebackground=win_color['menu active bg'])
        self.menu.add_cascade(label='font-type', menu=self.font_type_cascade)

        self.__init_font_size_cascade()
        self.__init_font_type_cascade()

        self.menu.post(event.x_root, event.y_root)


    def __bind_events(self):
        self.text.bind('u', self.underline)
        self.text.bind('d', self.deleteline)
        self.text.bind('b', self.bold)
        self.text.bind('n', self.normal)

    
    def __init_font_size_cascade(self):
        for item in self.font_sizes:
            self.font_size_cascade.add_command(label=str(item), 
                        command=lambda size=item: self.set_font_size(size))


    def __init_font_type_cascade(self):
        for item in self.font_types:
            self.font_type_cascade.add_command(label=item,
                        command=lambda type_=item: self.set_font_type(type_))
            
    
    def updata_tag_dict(self, type_, start, end, etc=None):
        self.tag_count += 1
        self.tag_dict[self.tag_count] = {'type': type_, 'start': start, 
                                        'end': end, 'etc': etc}


    def __normal_type(self, type_, char, event=None):
        try:
            start = self.text.index(SEL_FIRST)
            end = self.text.index(SEL_LAST)
            self.updata_tag_dict(type_, start, end)
            self.text.tag_add(type_, start, end)
        except:
            if event is not None:
                self.text.insert('insert', char)
        finally:
           return 'break' 
        
        
    def underline(self, event=None):
        return self.__normal_type('underline', 'u', event=event)   
    

    def deleteline(self, event=None):
        return self.__normal_type('deleteline', 'd', event=event)


    def bold(self, event=None):
        return self.__normal_type('bold', 'b', event=event)  
    

    def normal(self, event=None):
        return self.__normal_type('normal', 'n', event=event)


    def set_color(self, mode):
        if mode == 'foreground':
            mode = 'fg'
        else:
            mode = 'bg'
        ColorChooser(self.master, self.text, mode, self.tag_dict, 
                        self.updata_tag_dict, self.x+190, self.y)

    def set_font_size(self, size):
        font = self.text['font']
        new_font = re.sub(r'(\d+)', str(size), font)
        tag_label = f'font_size_{size}'
        print(new_font, tag_label)
        try:
            start = self.text.index(SEL_FIRST)
            end = self.text.index(SEL_LAST)
            self.updata_tag_dict('font size', start, end, size)
            self.text.tag_config(tag_label, font=new_font)
            self.text.tag_add(tag_label, start, end)
        except Exception as e:
            print(e)
            print('set font size error')
        finally:
            return 'break'


    def set_font_type(self, type_):
        font = self.text['font']
        new_font = re.sub(r'(\D+)\s', f'{type_} ', font)
        tag_label = f'font_type_{type_}'
        
        try:
            start = self.text.index(SEL_FIRST)
            end = self.text.index(SEL_LAST)
            self.updata_tag_dict(tag_label, start, end, type_)
            self.text.tag_config(tag_label, font=new_font)
            self.text.tag_add(tag_label, start, end)
        except Exception as e:
            print(e)
            print('set font type error')
        finally:
            return 'break'


if __name__ == '__main__':
    if hasattr(ctypes.windll.shcore, 'SetProcessDpiAwareness'):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        
    root = Tk()
    text = Text(root, font='consolas 14 normal')
    text.pack(padx=5, pady=5, fill='both', expand=True)

    popupmenu = PopupMenu(root, text)

    root.bind('<Button-3>', lambda event: popupmenu.popup(event))
    root.mainloop()