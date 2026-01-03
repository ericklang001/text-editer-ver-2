import re 
import ctypes 
from configs import configs 
from tkinter import *
from tkinter.ttk import Separator 


class ColorSeter:
    def __init__(self, master):
        self.master = master

        self.frm = None 
        self.tabfrm = None 
        self.cmdfrm = None 
        self.barfrm = None 

        self.fg_barfrm = None 
        self.bg_barfrm = None 
        self.state_frm = None 

        self.fg_state = None 
        self.bg_state = None 

        self.labs = []
        self.scale_dict = {'fg': {}, 'bg': {}}
        self.state_dict = {'fg': {'red': None, 'green': None, 'blue': None, 
                           'hex': None, 'btn': None},
                           'bg': {'red': None, 'green': None, 'blue': None, 
                           'hex': None, 'btn': None}}

        self.__init_container()


    def __init_container(self):
        self.frm = Frame(self.master)  

        self.tabfrm = Frame(self.frm, bg='lightgreen')
        self.cmdfrm = Frame(self.frm, relief='groove', bd=2)
        self.barfrm = Frame(self.frm, bg='lightblue')

        self.fg_barfrm = LabelFrame(self.barfrm, text='foreground', bg='white', relief='sunken', bd=2)
        self.bg_barfrm = LabelFrame(self.barfrm, text='background', bg='white', relief='sunken', bd=2)
        self.state_frm = Frame(self.barfrm, relief='groove', bd=2)

        self.fg_state = Frame(self.state_frm, relief='flat', bd=0)      # foreground color statebar 
        self.bg_state = Frame(self.state_frm, relief='flat', bd=0)      # background color statebar 

        self.fg_config = None   # foreground color bar frame 
        self.bg_config = None   # backgroudn color bar frame 

        self.__init_tabfrm()
        self.__init_barfrm()
        self.__init_cmdfrm()
        self.__pack__all()
        
    
    def __init_tabfrm(self):    # initialize the labels in self.tabfrm frame
        sizes = [14, 30, 20, 25, 42, 18]
        anchor=['se', 'center', 'sw', 'ne', 'center', 'nw']
        row = 1 
        for index, item in enumerate(sizes):
            if index % 3 == 0:
                row += 1

            lab = Label(self.tabfrm, text="Hello", font=f"Consolas {item} normal", fg='black', 
                        bg='white', anchor=anchor[index])
            lab.grid(row=row, column=index%3, sticky='news')
            self.labs.append(lab)
            
        self.tabfrm.rowconfigure([0, 1], weight=1)
        self.tabfrm.columnconfigure([0, 1, 2], weight=1)


    def __init_cmdfrm(self):    # command btns to open related color scalebar setting frame 
        self.fg_config = Button(self.cmdfrm, text='config foreground', width=15, command=self.pack_fgfrm)
        self.bg_config = Button(self.cmdfrm, text='config background', width=15, command=self.pack_bgfrm)

        self.fg_config.pack(side='left', padx=5, pady=5, anchor='w')
        self.bg_config.pack(side='left', padx=5, pady=5, anchor='w')


    def __init_state(self, type_):      # initialize the state bar which record current fg/bg color state
        frm = self.fg_state if type_ =='fg' else self.bg_state 
        self.state_dict[type_]['red'] = Label(frm, text=f'red: {self.scale_dict[type_]['red'].get()}',
                                                width=10, anchor='w', relief='groove')
        self.state_dict[type_]['green'] = Label(frm, text=f'green: {self.scale_dict[type_]['green'].get()}',
                                                width=10, anchor='w', relief='groove')
        self.state_dict[type_]['blue'] = Label(frm, text=f'blue: {self.scale_dict[type_]['blue'].get()}',
                                                width=10, anchor='w', relief='groove')
        hex_code = 'fg hex_code: #000000' if type_ =='fg' else 'bg hex_code: #ffffff'
        self.state_dict[type_]['hex'] = Label(frm, text=hex_code, width=20, anchor='w', relief='groove')
        btn = Button(frm, text=f'copy {type_} hex_code', width=15, relief='groove')
        btn.bind('<Button-1>', self.copy_code)

        self.state_dict[type_]['btn'] = btn 

    def __init_barfrm(self):        # foreground and background color scale bar 
        self.scale_dict['fg']['red'] = Scale(self.fg_barfrm, from_=0, to=255, bg='white', width=15,
                sliderlength=40, orient='horizontal', relief='sunken', troughcolor='red', command=self.color_track) 
        self.scale_dict['fg']['green'] = Scale(self.fg_barfrm, from_=0, to=255, bg='white', width=15,
                sliderlength=40, orient='horizontal', relief='sunken', troughcolor='green', command=self.color_track)
        self.scale_dict['fg']['blue'] = Scale(self.fg_barfrm, from_=0, to=255, bg='white', width=15,
                sliderlength=40, orient='horizontal', relief='sunken', troughcolor='blue', command=self.color_track)
        
        self.scale_dict['bg']['red'] = Scale(self.bg_barfrm, from_=0, to=255, bg='white', width=15, 
                sliderlength=40, orient='horizontal', relief='sunken', troughcolor='red', command=self.color_track) 
        self.scale_dict['bg']['green'] = Scale(self.bg_barfrm, from_=0, to=255, bg='white', width=15, 
                sliderlength=40, orient='horizontal', relief='sunken', troughcolor='green', command=self.color_track)
        self.scale_dict['bg']['blue'] = Scale(self.bg_barfrm, from_=0, to=255, bg='white', width=15,
                sliderlength=40, orient='horizontal', relief='sunken', troughcolor='blue', command=self.color_track)
        
        # initialize the default color value of foreground and background 
        for item in self.scale_dict['fg'].values():
            item.set(0)

        for item in self.scale_dict['bg'].values():
            item.set(255)

        self.__init_state('fg')
        self.__init_state('bg')
    

    def __pack__all(self):
        # pack all the unfold containers  
        self.frm.pack(side='left', padx=5, pady=5, fil='both', expand=True, anchor='nw')
         
        self.tabfrm.pack(side='top', padx=5, pady=5, fill='x', anchor='nw')
        self.cmdfrm.pack(side='top', padx=5, pady=5, fill='x')
        self.barfrm.pack(side='top', padx=5, pady=5, fill='both', expand=True, anchor='nw')

        self.state_frm.pack(side='top', padx=5, pady=5, fill='x', anchor='nw')

        # pack all the widgets in self.fg_state/ self.bg_state and self.fg_barfrm/ self.bg_barfrm  
        for frm in self.state_dict.values():
            for lab in frm.values():
                lab.pack(side='left', padx=5, pady=5)

        for frm in self.scale_dict.values():
            for scale in frm.values():
                scale.pack(side='top', padx=5, pady=5, fill='x')

    
    def pack_fgfrm(self):     # pack forget background state and color bar about and pack the fg about
        self.bg_state.pack_forget()
        self.fg_state.pack(side='top', padx=5, pady=5, anchor='w', fill='x')

        self.bg_config.config(state='normal')
        self.fg_config.config(state='disabled')
        self.bg_barfrm.pack_forget()
        self.fg_barfrm.pack(side='top', padx=5, pady=5, fill='x')


    def pack_bgfrm(self):     # pack forget foreground state and color bar about and pack the bg about 
        self.fg_state.pack_forget()
        self.bg_state.pack(side='top', padx=5, pady=5, anchor='w', fill='x')

        self.fg_config.config(state='normal')
        self.bg_config.config(state='disabled')
        self.fg_barfrm.pack_forget()
        self.bg_barfrm.pack(side='top', padx=5, pady=5, fill='x')


    def copy_code(self, event):
        if self.fg_config['state'] == 'disabled':
            type_ = 'fg'
        else:
            type_ = 'bg'

        color_code = self.state_dict[type_]['hex']['text'][-7:]     # get color's hex-code
        self.master.clipboard_append(color_code)     # append the hex-color code to clipboard 


    def color_track(self, event):
        if self.fg_config['state'] == 'disabled':
            type_ = 'fg'
        else:
            type_ = 'bg'

        red = self.scale_dict[type_]['red'].get()
        green = self.scale_dict[type_]['green'].get() 
        blue = self.scale_dict[type_]['blue'].get()

        self.__update_state(type_, [red, green, blue])


    def __update_state(self, type_, colors):
        hex_code = '#{:02x}{:02x}{:02x}'.format(*colors)   

        self.state_dict[type_]['red'].config(text=f'red: {colors[0]}')
        self.state_dict[type_]['green'].config(text=f'green: {colors[1]}')
        self.state_dict[type_]['blue'].config(text=f'blue: {colors[2]}')
        self.state_dict[type_]['hex'].config(text=f'{type_} hex_code: {hex_code}')

        for widget in self.labs:        # update the label color state 
            widget[type_] = hex_code 
        
        

class Configer:
    def __init__(self, master):
        self.default_font = 'Consolas 12 bold'
        self.master = master 

        self.region = None
        
        self.canvas = None 
        self.frm = None 
        self.yscrollbar = None 

        self.toolsbar_frm = None 
        self.labelText_frm = None 
        self.noteBook_frm = None 
        self.freeEdit_frm = None 

        # empty dictionary to store config about widgets 
        self.config_widget_dict = {}    # configer about widget dict, include sub-key: label, entry       
        self.colorSetter = None 

        self.__init_container()
        self.__pack_all()

        self.frm.bind('<Configure>', self.__configure_region)
        self.canvas.bind('<Configure>', self.__resize_frm)
        self.frm.bind('<MouseWheel>', self.__mousewheel)
        self.toolsbar_frm.bind('<MouseWheel>', self.__mousewheel)
        self.labelText_frm.bind('<MouseWheel>', self.__mousewheel)
        self.noteBook_frm.bind('<MouseWheel>', self.__mousewheel)
        self.freeEdit_frm.bind('<MouseWheel>', self.__mousewheel)

    def __init_container(self):     # initialize the containers
        self.region = Frame(self.master, relief='groove', bg='lightgreen')
        self.canvas = Canvas(self.region, relief='groove', bg='yellow')
        self.yscrollbar = Scrollbar(self.region, orient='vertical', command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.yscrollbar.set)

        self.frm = Frame(self.canvas, bg='lightblue')
        self.frm_id = self.canvas.create_window((0, 0), anchor='nw', window=self.frm)

        self.toolsbar_frm = Frame(self.frm)
        self.labelText_frm = Frame(self.frm)
        self.noteBook_frm = Frame(self.frm)
        self.freeEdit_frm = Frame(self.frm)

    def __pack_all(self):       # pack all the containers 
        self.region.pack(side='left', padx=5, pady=5, fill='both', expand=True)
        self.canvas.pack(side='left', padx=5, pady=5, fill='both', expand=True)
        self.yscrollbar.pack(side='left', padx=5, pady=5, fill='y')

        self.toolsbar_frm.pack(padx=5, pady=5, fill='x')
        self.labelText_frm.pack(padx=5, pady=5, fill='x')
        self.noteBook_frm.pack(padx=5, pady=5, fill='x')
        self.freeEdit_frm.pack(padx=5, pady=5, fill='x')

        self.__init_toolsbar_frm()
        self.__init_labelText_frm()
        self.__init_noteBook_frm()
        self.__init_freeEdit_frm()

    def __configure_region(self, event):    # when inner widget add or fold/unfold, update the region of canvas
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def __resize_frm(self, event):      # change the canvas' inner widgets' size when window size change 
        canvas_width = self.canvas.winfo_width()

        new_width = int(canvas_width * 0.97)
        x = (canvas_width-new_width) // 2 
        self.canvas.coords(self.frm_id, x, 10)
        self.canvas.itemconfig(self.frm_id, width=new_width)


    def __mousewheel(self, event):      # scroll the view of canvas
        self.canvas.yview_scroll(2 if event.delta < 0 else -2, 'units')
    
    
    def __init_config_frm(self, base_, type_):      # basic method to initialize the other four configer frame 
        lab_ent_dict = {'label': {}, 'entry': {}}
        re_pattern = re.compile(r'separator\d+')
        for index, (name, val) in enumerate(configs[type_]['label'].items()):
            if len(re_pattern.findall(name)) == 1:
                sep = lab_ent_dict['label'][val] = Separator(base_, orient='horizontal')
                sep.grid(row=index, column=0, columnspan=2, padx=5, pady=2, sticky='we')
                continue 
            lab_ent_dict['label'][name] = Label(base_, text=val, width=25, anchor='w')
            lab_ent_dict['label'][name].grid(row=index, column=0, padx=5, pady=3)

        for index, name in enumerate(configs[type_]['entry']):
            if name == 'separator':
                continue 
            lab_ent_dict['entry'][name] = Entry(base_, width=10)
            lab_ent_dict['entry'][name].grid(row=index, column=1, padx=5, pady=3)
        
        self.config_widget_dict[type_] = lab_ent_dict


    def __fold_config(self, btn_, base_, target_):      # fole or unfole configer frame 
        if len(base_.pack_slaves()) == 1:    # if now if fold, unfold it 
            text_ = btn_['text'].replace('open', 'close').replace('>>>', '<<<')
            btn_.config(text=text_)
            target_.pack(side='top', padx=5, pady=5)
        else:       # if now if unfold, fold it 
            text_ = btn_['text'].replace('close', 'open').replace('<<<', '>>>')
            btn_.config(text=text_)
            target_.pack_forget()

    
    def __init_toolsbar_frm(self):      # use self.__init_config_frm() to initialize toolsbar configer frame 
        self.open_toolsbar_config = Button(self.toolsbar_frm, text='open toolsbar config >>>', width=30, 
                                        font=self.default_font, relief='flat', bd=0, anchor='w')
        self.toolsbar = Frame(self.toolsbar_frm, relief='groove')

        self.open_toolsbar_config.config(command=lambda:
                                            self.__fold_config(self.open_toolsbar_config, self.toolsbar_frm, self.toolsbar))
        self.__init_config_frm(self.toolsbar, 'toolsbar')
        self.open_toolsbar_config.pack(side='top', padx=5, pady=5, anchor='w')


    def __init_labelText_frm(self):     # use self.__init_configer_frm() to initialize labelText configer frame 
        self.open_labelText_config = Button(self.labelText_frm, text='open labelText config >>>', width=30,
                                        font=self.default_font, relief='flat', bd=0, anchor='w')
        self.labelText = Frame(self.labelText_frm, relief='groove')

        self.open_labelText_config.config(command=lambda: 
                                            self.__fold_config(self.open_labelText_config, self.labelText_frm, self.labelText))
        self.__init_config_frm(self.labelText, 'labelText')
        self.open_labelText_config.pack(side='top', padx=5, pady=5, anchor='w')


    def __init_noteBook_frm(self):      # use self.__init_configer_frm() to initialize noteBook configer frame 
        self.open_noteBook_config = Button(self.noteBook_frm, text='open noteBook config >>>', width=30,
                                        font=self.default_font, relief='flat', bd=0, anchor='w')
        self.noteBook = Frame(self.noteBook_frm, relief='groove')

        self.open_noteBook_config.config(command=lambda:
                                            self.__fold_config(self.open_noteBook_config, self.noteBook_frm, self.noteBook))
        self.__init_config_frm(self.noteBook, 'noteBook')
        self.open_noteBook_config.pack(side='top', padx=5, pady=5, anchor='w')


    def __init_freeEdit_frm(self):      # use self.__init_configer_frm() to initialize freeEdit configer frame 
        self.open_freeEdit_config = Button(self.freeEdit_frm, text='open freeEdit config >>>', width=30, 
                                        font=self.default_font, relief='flat', bd=0, anchor='w')
        self.freeEdit = Frame(self.freeEdit_frm, relief='groove')

        self.open_freeEdit_config.config(command=lambda: 
                                            self.__fold_config(self.open_freeEdit_config, self.freeEdit_frm, self.freeEdit))
        self.__init_config_frm(self.freeEdit, 'freeEdit')
        self.open_freeEdit_config.pack(side='top', padx=5, pady=5, anchor='w')



class ConfigableWidget:
    def __init__(self, mode):
        self.theme_mode = mode 
        self.theme_code = None 
        self.configable_widgets = {'fg':{}, 'bg': {}, 'color': {}, 
                                'active': {'fg': {}, 'bg': {}}} 

    # add foreground configable widget (list)
    def add_widgets_fg(self, labname, widget_lst):
        self.configable_widgets['fg'][labname] = widget_lst 

    # add background configable widget (list)
    def add_widgets_bg(self, labname, widget_lst):
        self.configable_widgets['bg'][labname] = widget_lst 

    # add active foreground configable widget (list)
    def add_widgets_active_fg(self, labname, widget_lst):
        self.configable_widgets['active']['fg'][labname] = widget_lst

    # add active background configabel widget (list)
    def add_widgets_active_bg(self, labname, widget_lst):
        self.configable_widgets['active']['bg'][labname] = widget_lst
    
    # append etc widget to foreground configable widget list 
    def append_fg(self, labname, *widgets):
        for item in widgets:
            if isinstance(item, list):
                for widget in item:
                    self.configable_widgets['fg'][labname].append(widget)
            else:
                self.configable_widgets['fg'][labname].append(item)

    # append etc widget to background configable widget list 
    def append_bg(self, labname, *widgets):
        for item in widgets:
            if isinstance(item, list):
                for widget in item:
                    self.configable_widgets['bg'][labname].append(widget)
            else:
                self.configable_widgets['bg'][labname].append(item)


    def del_UI_fg_widget(self, name, obj):
        self.configable_widgets['fg'][name].remove(obj)


    def del_labelText_lab(self, lab, rmbtn, rment, text):
        self.configable_widgets['fg']['UI fg'].remove(lab)
        self.configable_widgets['fg']['text fg'].remove(text)

        self.configable_widgets['bg']['text bg'].remove(text)
        # self.configable_widgets['bg']['']


    def del_toolsbar_widght(self, lab, close):
        self.configable_widgets['fg']['close fg'].remove(close)
        self.configable_widgets['bg']['close bg'].remove(close)
        self.configable_widgets['bg']['lab bg'].remove(lab)
        # self.configable_widgets['active']['choose fg'].remove(self.lab)
        # self.configable_widgets['active']['choose bg'].remove(self.lab)


    def del_noteBook_widget(self, fg_dict, bg_dict):
        for key, item in fg_dict.items():
            if not isinstance(item, list):
                self.configable_widgets['fg'][key].remove(item)
                continue
            
            for widget in item:
                self.configable_widgets['fg'][key].remove(widget)
        
        for key, item in bg_dict.items():
            if not isinstance(item, list):
                self.configable_widgets['bg'][key].remove(item)
                continue 

            for widget in item:
                self.configable_widgets['bg'][key].remove(widget)


    def get_configable_widgets(self):
        return self.configable_widgets


    def set_theme_code(self, code):
        self.theme_code = code 


    def set_widget_color(self):
        self.configable_widgets['color']['fg'] = __import__('theme').theme[self.theme_code][self.theme_mode]['fg']
        self.configable_widgets['color']['bg'] = __import__('theme').theme[self.theme_code][self.theme_mode]['bg']
        if __import__('theme').theme[self.theme_code][self.theme_mode].get('active') is not None:
            self.configable_widgets['color']['active'] = __import__('theme').theme[self.theme_code][self.theme_mode]['active']
        else:
            self.configable_widgets['color']['active'] = None 

        # config foreground of foreground configable widgets 
        for key, val in self.configable_widgets['color']['fg'].items():
            if isinstance(self.configable_widgets['fg'][key], list):
                for item in self.configable_widgets['fg'][key]:
                    item.config(fg=val)
            else:
                self.configable_widgets['fg'][key].config(fg=val)

        # config background of background configable widgets 
        for key, val in self.configable_widgets['color']['bg'].items():
            if key == 'separator bg':     # specially process the separator 
                self.configable_widgets['bg'][key].configure('TSeparator', background=val)
                continue 

            if isinstance(self.configable_widgets['bg'][key], list):
                for item in self.configable_widgets['bg'][key]:
                    item.config(bg=val)
            else:
                self.configable_widgets['bg'][key].config(bg=val)

        # check none of active_dict 
        if self.configable_widgets['color']['active'] is None:
            return 
        
        # config active foreground of active foreground configable widgets
        for key, val in self.configable_widgets['color']['active']['fg'].items():
            if isinstance(self.configable_widgets['active']['fg'][key], list):
                for item in self.configable_widgets['active']['fg'][key]:
                    item.active_fg = val       # the loop item should be a object that has active_fg attribute 
            else:
                self.configable_widgets['active']['fg'][key].active_fg = val    # the same

        # config active background of active background configable widgets 
        for key, val in self.configable_widgets['color']['active']['bg'].items():
            if isinstance(self.configable_widgets['active']['bg'][key], list):
                for item in self.configable_widgets['active']['bg'][key]:
                    item.active_bg = val       # the loop item should be a object that has active_bg attribute 
            else:
                self.configable_widgets['active']['bg'][key].active_bg = val 



class ConfigManager:
    def __init__(self, editers, code='4'):
        self.editers = editers
        self.toolsbar = None 
        self.theme_code = code 


    def set_theme_with_code(self, code):
        self.theme_code = code

        list(self.editers.values())[0].master.config(
            bg=__import__('theme').theme[self.theme_code]['window']['bg'])
        self.set_toolsbar_theme()
        self.set_theme() 

    
    def set_theme_with_color(self, colors):
        pass 


    def add_toolsbar(self, toolsbar):
        self.toolsbar = toolsbar


    def set_toolsbar_theme(self):
        if self.toolsbar is None:
            return 

        self.toolsbar.theme_code = self.theme_code 
        self.toolsbar.label_manager.theme_code = self.theme_code 
        for labelUnion in self.toolsbar.label_manager.labs.values():
            labelUnion.theme_code = self.theme_code 

        configable_widget = self.toolsbar.get_configable_widget()
        configable_widget.set_theme_code(self.theme_code)
        configable_widget.set_widget_color()


    def set_theme(self):
        for editer in self.editers.values():
            editer.base.theme_code = self.theme_code 
            configableWidth = editer.base.get_configable_widget()
            configableWidth.set_theme_code(self.theme_code)
            configableWidth.set_widget_color() 

    pass 

                 
        

if __name__ == '__main__':
    if hasattr(ctypes.windll.shcore, "SetProcessDpiAwareness"):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    root = Tk()
    root.geometry('1480x900')
    root['bg'] = 'yellow'

    Configer(root)
    ColorSeter(root)

    root.mainloop()