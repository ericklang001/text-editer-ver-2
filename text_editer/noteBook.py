import ctypes 
from tkinter import * 
from configer import ConfigableWidget

__all__ = ['NoteBook', 'NoteBase', 'CanvasBase']

class CanvasBase:
    def __init__(self, master):
        self.region = Frame(master)
        self.canvas = None 
        self.configable_widget = None 

        self.theme_code = '4'

        self.__init_canvas()
        self.__set_configable_widget()

        self.canvas.bind('<Button-1>', self.__mouse_click_left)    
        self.canvas.bind('<MouseWheel>', self.__mouse_wheel)
    

    def __set_configable_widget(self):
        if self.configable_widget is None:
            self.configable_widget = ConfigableWidget('noteBook')

        self.configable_widget.add_widgets_bg('region', self.region)
        self.configable_widget.add_widgets_bg('canvas', self.canvas)
        self.configable_widget.add_widgets_bg('region yscrollbar', self.yscrollbar)


    def __init_canvas(self):
        self.canvas = Canvas(self.region, bg='lightgreen')
        self.yscrollbar = Scrollbar(self.region, orient='vertical', command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.yscrollbar.set)

        self.region.pack(side='top', padx=5, pady=5, fill='both', expand=True)
        self.canvas.pack(side='left', padx=5, pady=5, fill='both', expand=True)
        self.yscrollbar.pack(side='left', padx=5, pady=5, fill='y')


    def get_configable_widget(self):
        return self.configable_widget 


    def __mouse_click_left(self, event):
        """
            track the focus transfer, if click a position out of Text widget, 
            then the focus turn back to based canvas.
        """
        if not isinstance(event.widget.winfo_containing(event.x_root, event.y_root), Text):
            self.canvas.focus_set()
        

    def __mouse_wheel(self, event):
        # if the focus now if in Text widget, canvas can't use the method of mouse wheel
        if isinstance(self.region.focus_get(), Text):
            return
        
        self.canvas.yview_scroll(2 if event.delta < 0 else -2, 'units')

    
    def get_canvas(self):
        if self.canvas is None:
            print('self.canvas is None')
        return self.canvas 
    

    def get_region(self):
        return self.region



class NoteBase:
    def __init__(self, masterbase):
        self.theme_code = '4'
        if isinstance(masterbase, CanvasBase):
            self.master = masterbase.get_canvas()
            self.theme_code = masterbase.theme_code
        else:
            self.master = masterbase 

        
        self.container = None 
        self.container_id = None 

        self.configable_widget = None 

        self.__init_container()
        if isinstance(masterbase, CanvasBase):
            self.__set_configable_widget(masterbase.get_configable_widget())
            
        self.container.bind('<Button-1>', lambda event: self.master.focus_set())
        self.container.bind('<MouseWheel>', self.__mouse_wheel)
        self.master.bind('<Configure>', self.__resize)
    

    def __set_configable_widget(self, configable_widget):
        self.configable_widget = configable_widget

        self.configable_widget.add_widgets_bg('notebase', self.container)
    

    def __init_container(self):
        self.container = Frame(self.master, bg='yellow')
        self.container_id = self.master.create_window((0, 0), anchor='nw', window=self.container)

        self.container.bind('<Configure>', self.__config_region)


    def __config_region(self, event):
        self.master.config(scrollregion=self.master.bbox('all'))


    def __mouse_wheel(self, event):
        if isinstance(self.container.focus_get(), Canvas):
            self.master.yview_scroll(2 if event.delta < 0 else -2, 'units')


    def __resize(self, event):
        master_w = self.master.winfo_width()

        new_w = int(master_w * 0.95)
        x = (master_w - new_w) // 2 

        self.master.coords(self.container_id, x, 10)
        self.master.itemconfig(self.container_id, width=new_w)


    def get_container(self):
        return self.container 
    

    def get_configable_widget(self):
        return self.configable_widget
    

    def get_container_id(self):
        return self.container_id
    


class NoteBook:
    created_count: int = 0 
    created_note: dict = {}
    default_font = 'Consolas 12 normal'
    font_type = default_font 

    def __init__(self, masterbase):
        NoteBook.created_count += 1
        NoteBook.created_note[NoteBook.created_count] = self
        self.index = NoteBook.created_count 
        self.masterbase = masterbase 
        self.master = masterbase.get_container()

        self.theme_code = masterbase.theme_code

        self.frm = None     # all the widget include the notebook will be pack/grid on it

        self.title = None       # notebook's title frame
        self.edit = None        # notebook's edit frame
        self.cmd = None         # notebook's command frame

        self.text = None 

        self.cmd_labs = None    # just some vertical orient separator between cmd btns 
        self.cmd_btns = None    # command btns, control notebook's create and delete, rename 

        self.configable_widget = None   # Configer object

        self.__init_container()
        self.__pack_container()
        self.__init_title()
        self.__init_edit()
        self.__init_cmd()
        self.__canvas_event_bind()

        self.__set_configable_widget(masterbase.get_configable_widget())


    def __set_configable_widget(self, configable_widget):
        self.configable_widget = configable_widget 
        if len(self.configable_widget.get_configable_widgets()['fg']) == 0:
            self.configable_widget.add_widgets_fg('UI fg', self.cmd_labs + self.cmd_btns)
            self.configable_widget.append_fg('UI fg', self.t_lab, self.t_ent) 
            self.configable_widget.add_widgets_fg('text fg', [self.text])
        else:
            self.configable_widget.append_fg('UI fg', self.cmd_labs, self.cmd_btns, self.t_lab, self.t_ent)
            self.configable_widget.append_fg('text fg', self.text)
            
        names = ['title', 't_lab', 't_ent', 'edit', 'text bg', 'text yscrollbar', 
                    'cmd', 'cmd widgets', 'frm']
        widgets = [self.title, self.t_lab, self.t_ent, self.edit, self.text, self.yscrollbar,
                    self.cmd, self.cmd_btns + self.cmd_labs, self.frm]
        if len(self.configable_widget.get_configable_widgets()['bg']) <= 4:
            for name, widget in zip(names, widgets):
                if isinstance(widget, list):
                    self.configable_widget.add_widgets_bg(name, widget)
                else:
                    self.configable_widget.add_widgets_bg(name, [widget])
        else:
            for name, widget in zip(names, widgets):
                self.configable_widget.append_bg(name, widget)

        if self.configable_widget.theme_code is None:
            self.configable_widget.set_theme_code(self.theme_code)
        self.configable_widget.set_widget_color()

    
    def __init_container(self):
        self.frm = Frame(self.master, relief='groove', bd=3)

        self.title = Frame(self.frm)
        self.edit = Frame(self.frm)
        self.cmd = Frame(self.frm)


    def __canvas_event_bind(self):
        self.title.bind('<Button-1>', lambda event: self.master.master.focus_set())
        self.edit.bind('<Button-1>', lambda event: self.master.master.focus_set())
        self.cmd.bind('<Button-1>', lambda event: self.master.master.focus_set())

        self.title.bind('<MouseWheel>', self.__canvas_mouse_wheel)
        self.edit.bind('<MouseWheel>', self.__canvas_mouse_wheel)
        self.cmd.bind('<MouseWheel>', self.__canvas_mouse_wheel)
        self.text.bind('<MouseWheel>', self.__canvas_mouse_wheel)

    def __canvas_mouse_wheel(self, event):
        if isinstance(event.widget, Text) and self.text.focus_get() is self.text:
            self.text.yview_scroll(2 if event.delta < 0 else -2, 'units')
            return 'break'
        
        self.master.master.yview_scroll(2 if event.delta < 0 else -2, 'units')


    def __pack_container(self):
        self.title.pack(side='top', padx=5, pady=5, fill='x')
        self.edit.pack(side='top', padx=5, pady=5, fill='x')
        self.cmd.pack(side='top', padx=5, pady=5, fill='x')

        self.frm.pack(side='top', padx=10, pady=15, fill='x')


    def __init_title(self):
        self.t_lab = Label(self.title, text='untitled', font='Consolas 14 bold')
        self.t_ent = Entry(self.title, font='Consolas 14 bold', insertbackground='red', fg='gray')

        self.t_lab.pack(side='left', padx=5, pady=5, fill='x')
        self.t_ent.bind('<Return>', self.__confirm_name)


    def __init_edit(self):
        self.text = Text(self.edit, font=self.default_font, height=14)
        self.yscrollbar = Scrollbar(self.edit, orient='vertical', command=self.text.yview)
        self.text.config(yscrollcommand=self.yscrollbar.set)

        self.text.grid(row=0, column=0, padx=5, pady=5, sticky='we')
        self.yscrollbar.grid(row=0, column=1, padx=5, pady=5, sticky='ns')

        self.edit.columnconfigure(0, weight=1)
    

    def __init_cmd(self):
        new_btn = Button(self.cmd, text='new note', command=self.new_note, relief='flat', 
               bd=0)
        lab1 = Label(self.cmd, text='|')
        new_btn.pack(side='left', padx=5, pady=5)
        lab1.pack(side='left', pady=5)
        
        del_btn = Button(self.cmd, text='delete note', command=self.delete_note, relief='flat', 
               bd=0)
        lab2 = Label(self.cmd, text='|')
        del_btn.pack(side='left', padx=5, pady=5)
        lab2.pack(side='left', pady=5)

        rename_btn = Button(self.cmd, text='rename', command=self.rename, relief='flat',
               bd=0)
        rename_btn.pack(side='left', padx=5, pady=5)

        self.cmd_labs = [lab1, lab2]
        self.cmd_btns = [new_btn, del_btn, rename_btn]

    
    @classmethod 
    def set_font(cls, font_str='Consolas 12 normal'):
        cls.font_type = font_str
        for item in NoteBook.created_note.values():
            item.text.config(font=cls.font_type) 


    def new_note(self):
        NoteBook(self.masterbase)

    
    def delete_note(self):
        if NoteBook.created_count == 1:
            return 
        
        fg_dict = {'UI fg': self.cmd_labs + self.cmd_btns + [self.t_lab, self.t_ent],
                   'text fg': self.text}
        names = ['title', 't_lab', 't_ent', 'edit', 'text bg', 'text yscrollbar', 
                    'cmd', 'cmd widgets', 'frm']
        widgets = [self.title, self.t_lab, self.t_ent, self.edit, self.text, self.yscrollbar,
                    self.cmd, self.cmd_btns + self.cmd_labs, self.frm]
        bg_dict = dict(zip(names, widgets))

        self.configable_widget.del_noteBook_widget(fg_dict, bg_dict)

        self.frm.destroy()
        NoteBook.created_note.pop(self.index)

    def theme(self):
        pass 

    def rename(self):
        if self.t_ent in self.title.pack_slaves():      # already in the state of rename
            return 
        
        self.t_lab.pack_forget()
        self.t_ent.pack(side='left', padx=5, pady=5, fill='x')
        self.t_ent.insert('end', 'enter new name')
        self.t_ent.focus_set()

    def __confirm_name(self, *args):
        last_name = self.t_lab['text']
        name = self.t_ent.get()
        if name.strip() == 'enter new name' or name == '':
            name = last_name 
        
        self.t_ent.pack_forget()
        self.t_lab.config(text=name)
        self.t_lab.pack(side='left', padx=5, pady=5, fill='x')
        self.t_ent.delete('0', 'end')
    



if __name__ == '__main__':
    if hasattr(ctypes.windll.shcore, "SetProcessDpiAwareness"):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    root = Tk()
    root.geometry('1400x1000')

    canvasbase = CanvasBase(root)
    container = NoteBase(canvasbase)
    note1 = NoteBook(container)
    note1.theme_code = '4'
    note1.configable_widget.set_theme_code(note1.theme_code)
    note1.configable_widget.set_widget_color()

    root.mainloop()
