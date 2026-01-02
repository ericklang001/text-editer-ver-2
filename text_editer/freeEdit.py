import ctypes 
from tkinter import *
from configer import ConfigableWidget


__all__ = ['FreeEditer']


class FreeEditer:
    default_text_font: str = "Consolas 15 normal"
    default_state_font: str = "Consolas 10 normal"

    def __init__(self, master):
        self.master = master

        self.theme_code = '2'

        self.region = None      # basic container frame
        self.edit = None        # text frame 
        self.statebar = None    # statebar frame 

        self.text = None 
        self.xscrollbar = None 
        self.yscrollbar = None 

        self.configable_widget = None 

        self.__init_container()
        self.__init_edit()
        self.__init_statebar()
        self.__set_configable_widget()


    def __set_configable_widget(self):
        if self.configable_widget is None:
            self.configable_widget = ConfigableWidget('freeEdit')
        
        self.configable_widget.set_theme_code(self.theme_code)
        self.configable_widget.add_widgets_fg('UI fg', [self.row, self.column, self.count, self.font_type])
        self.configable_widget.add_widgets_fg('text fg', self.text)
        
        names = ['region', 'edit', 'text bg', 'scrollbar', 'statebar', 'lab']
        widgets = [self.region, self.edit, self.text, [self.xscrollbar, self.yscrollbar], 
                    self.statebar, [self.row, self.column, self.count, self.font_type]]
        for name, widget in zip(names, widgets):
            self.configable_widget.add_widgets_bg(name, widget)

        self.configable_widget.set_widget_color()


    def __init_container(self):
        self.region = Frame(self.master)

        self.edit = Frame(self.region, bg='lightblue', relief='groove', bd=2) 
        self.statebar = Frame(self.region, bg='lightgreen', relief='groove', bd=2)

        self.region.pack(side='top', ipadx=5, ipady=5, fill='both', expand=True)
        self.edit.pack(side='top', padx=10, pady=5, fill='both', expand=True)
        self.statebar.pack(side='top', padx=10, pady=5, fill='x')
    

    def __init_edit(self):
        self.text = Text(self.edit, fg='blue', wrap='none', padx=5, font=FreeEditer.default_text_font)
        self.xscrollbar = Scrollbar(self.edit, orient='horizontal', command=self.text.xview)
        self.yscrollbar = Scrollbar(self.edit, orient='vertical', command=self.text.yview)
        self.text.config(xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)

        self.text.grid(row=0, column=0, padx=5, pady=5, sticky='news')
        self.xscrollbar.grid(row=1, column=0, padx=5, pady=5, sticky='we')
        self.yscrollbar.grid(row=0, column=1, padx=5, pady=5, sticky='ns')

        self.edit.columnconfigure(0, weight=1)
        self.edit.rowconfigure(0, weight=1)


    def __init_statebar(self):
        self.row = Label(self.statebar, text='row: 0', width=12, relief='groove', bd=1, anchor='w',  
                        padx=5, font=FreeEditer.default_state_font)
        self.column = Label(self.statebar, text='col: 0', width=12, relief='groove', bd=1, anchor='w', 
                        padx=5, font=FreeEditer.default_state_font) 
        self.count = Label(self.statebar, text='coount: 0', width=15, relief='groove', bd=1, anchor='w',
                        padx=5, font=FreeEditer.default_state_font)
        self.font_type = Label(self.statebar, text='base_font: %s' % FreeEditer.default_text_font, relief='groove', bd=1,
                              padx=5, anchor='w', font=FreeEditer.default_state_font)
        
        self.row.pack(side='left', padx=5, pady=5)
        self.column.pack(side='left', padx=5, pady=5)
        self.count.pack(side='left', padx=5, pady=5)
        self.font_type.pack(side='left', anchor='w', padx=5, pady=5, fill='x', expand=True)


    def get_region(self):
        return self.region
    
    
    def get_configable_widget(self):
        return self.configable_widget



if __name__ == '__main__':
    if hasattr(ctypes.windll.shcore, "SetProcessDpiAwareness"):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    root = Tk()

    freeEdit = FreeEditer(root)
    freeEdit.theme_code = '4'
    freeEdit.configable_widget.set_theme_code(freeEdit.theme_code)
    freeEdit.configable_widget.set_widget_color()

    root.mainloop()