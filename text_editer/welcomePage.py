import ctypes 
import re 
import os 
from tkinter import *
from noteBook import *
from labelText import *
from freeEdit import * 
from nameManager import * 
from labelManage import * 
from winManager import *
from configer import *
from PIL import Image, ImageTk 
from tkinter.ttk import Separator 


__all__ = []


class Launcher:
    # the default height of the loader and default width of leader panel
    default_height: int = 700
    default_leader_width: int = 240
    # default wallpaper index
    default_index: int = 0 
    def __init__(self, manager, paths: list):
        if isinstance(manager, WinManager):
            self.manager = manager
            self.master = self.manager.get_first() 
        else:
            self.manager = None 
            self.master = manager 

        self.resource = paths 
        
        self.wallpaper = None 
        self.leader = None 

        self.leader_container = None 

        self.__decleration_self()

        self.__init_welcome()
        self.__load_wallpaper()


    def __decleration_self(self):
        # create new conponents
        self.has_createdNewWidgts = False
        self.new = None 
        self.create = None 
        self.label_text = None 
        self.note_book = None 
        self.free_edit = None
        self.cancel = None 

        self.toolsbar = None 
        self.configManager = ConfigManager(Editer.created_obj, '2')


    def __init_welcome(self):
        # create basis containers
        self.wallpaper = Label(self.master, bg='yellow')      # use to show wallpaper
        self.leader = Canvas(self.master, width=Launcher.default_leader_width, bg='lightblue')      # contains some quick operation
        yscrollbar = Scrollbar(self.master, orient='vertical', )
        
        # pack all the basis containers 
        self.wallpaper.pack(side='left', padx=5, pady=5)
        self.leader.pack(side='left', padx=5, pady=5, fill='y')
        yscrollbar.pack(side='left', padx=0, pady=5, fill='y')

        # use relative method to initialize the conatainer 
        self.__load_wallpaper()
        self.__init_leader()


    def __load_wallpaper(self):
        default_path = self.resource[Launcher.default_index] 

        img = Image.open(default_path)
        width, height = img.size 
        target_width = int(width / (height/Launcher.default_height))
        wallpaper = ImageTk.PhotoImage(img.resize((target_width, Launcher.default_height)))
        
        self.wallpaper.image = wallpaper     # keep image reference live 
        self.wallpaper.config(image=wallpaper)
        

    def __init_leader(self):
        # create a self.leader_container frame obj on the leader canvas
        self.__init_leader_container()

        self.theme = Button(self.leader_container, text='theme', relief='groove', bd=2, 
                            command=lambda: print('change theme'))
        self.__init_created_new()
        self.current = Frame(self.leader_container, relief='groove', bd=2) 

        self.theme.pack(side='top', padx=5, pady=5, fill='x')
        self.new.pack(side='top', padx=5, pady=5, fill='x')
        self.current.pack(side='top', padx=5, pady=5, fill='both', expand=True)
        

    def __init_leader_container(self):
        if self.leader_container is not None:
            return 
        
        container_obj = NoteBase(self.leader)    
        width = Launcher.default_leader_width * 0.90
        height = Launcher.default_height * 0.98 

        x = (Launcher.default_leader_width - width) // 2
        y = (Launcher.default_height - height) // 2

        self.leader.coords(container_obj.get_container_id(), x, y)
        self.leader.itemconfig(container_obj.get_container_id(), height=height)
        self.leader_container = container_obj.get_container()


    def __init_created_new(self):
        if self.leader_container is None:
            self.__init_leader_container()

        # create necessary widgets about create new function
        self.new = Frame(self.leader_container)
        self.create = Button(self.new, text='create new')
        if isinstance(self.manager, WinManager):
            self.create.config(command=self.__unfold_option)
        else:
            self.create.config(command=lambda: print('create new notebook'))
        # pack all the widgets in self.new frame 
        self.create.pack(padx=5, pady=5, fill='x')

    def __unfold_option(self):
        if self.new is None:
            self.__init_created_new()

        self.create.config(state='disabled', text='choose mode')
        # create all the btns 
        if not self.has_createdNewWidgts:
            self.label_text = Button(self.new, text='>>    Label Text', relief='sunken', bd=2, anchor='w', fg='blue', 
                                 command=lambda: self.open_create_new(1))
            self.note_book = Button(self.new, text='>>    Note Book', relief='sunken', bd=2, anchor='w', fg='blue',
                                    command=lambda: self.open_create_new(2))
            self.free_edit = Button(self.new, text='>>    Free Edit', relief='sunken', bd=2, anchor='w', fg='blue',
                                    command=lambda: self.open_create_new(3))
            self.cancel = Button(self.new, text='>>    cancel', relief='sunken', bd=2, anchor='w', fg='blue',
                                 command=self.cancel)
            # update widgets' state 
            self.has_createdNewWidgts = True 

        # pack all the btns 
        self.label_text.pack(padx=5, pady=5, anchor='w', fill='x')
        self.note_book.pack(padx=5, anchor='w', fill='x')
        self.free_edit.pack(padx=5, pady=5, anchor='w', fill='x')
        self.cancel.pack(padx=5, anchor='w', fill='x')


    def cancel(self):
        for widget in self.new.pack_slaves():
            widget.pack_forget()

        self.create.config(state='normal', text='create new')
        self.create.pack(padx=5, pady=5, fill='x')


    def open_create_new(self, order):
        if self.manager is None:
            return 
        self.manager.start_second()
        self.toolsbar = ToolsBar(self.manager.get_second())
        self.configManager.add_toolsbar(self.toolsbar)
        self.toolsbar.set_configManager(self.configManager)

        Launcher.init_create_new(order, self.manager.get_second(), self.toolsbar)

    @classmethod
    def init_create_new(cls, order, master, toolsbar):
        base_type = None 
        if order % 3 == 1:
            base_type = LabelText(master)

        elif order % 3 == 2:
            base_type = CanvasBase(master)
            container = NoteBase(base_type)
            NoteBook(container)

        elif order % 3 == 0:
            base_type = FreeEditer(master) 

        else:
            base_type = None 

        edit = Editer(master, toolsbar, base_type)



class Editer:
    # a class dictionary to keep the reference of created Editer object
    created_obj = {}

    def __init__(self, master, toolsbar, base):
        self.master = master 
        self.toolsbar = toolsbar 
        self.base = base 
        self.name = None 
        self.mode = None

        self.__init_name()
        self.__add_label()
        
        # update class created object data 
        Editer.created_obj[self.name] = self 


    def __add_label(self):      # append label to toolsbar's label_manager 
        obj_kw = {'name': self.name, 'region': self.base.get_region()}
        self.toolsbar.label_manager.add_lab(obj_kw, self) 


    def __init_name(self):      # use NameManager to produce name and manager it 
        if isinstance(self.base, LabelText):
            self.mode = 'labelText'
            self.name = NameManager.add_name('labelText')

        elif isinstance(self.base, CanvasBase):
            self.mode = 'noteBook'
            self.name = NameManager.add_name('noteBook') 
        
        elif isinstance(self.base, FreeEditer):
            self.mode = 'freeEdit'
            self.name = NameManager.add_name('freeEdit')
        
        else:
            print('unknow object type had been passed')


    def destroy(self):
        NameManager.del_name(self.mode, self.name)
        del Editer.created_obj[self.name]



class ToolsBar:
    default_font = "Consolas 12 bold"
    default_optmenu_abg = "lightblue"

    def __init__(self, master):
        self.master = master
        self.base = self 
        self.configManager = None 

        self.theme_code = '2'

        self.region = None 

        self.labfrm = None 
        self.configfrm = None 
        self.fontfrm = None 

        self.optmenu = None 

        self.label_manager = None 
        self.font_labs = None 
        self.font_ents = None 
        
        self.configable_widget = None 

        self.__init_container()
        self.__set_configable_widget()
        self.__init_labfrm()

    
    def set_configManager(self, configManager):
        self.configManager = configManager


    def __set_configable_widget(self):
        if self.configable_widget is None:
            self.configable_widget = ConfigableWidget('toolsbar')

        self.configable_widget.add_widgets_fg('UI fg', self.font_labs)
        self.configable_widget.append_fg('UI fg', self.theme, self.new)

        names = ['region toolsbar', 'top label', 'labfrm', 'configfrm', 'btn', 'fontfrm', 'font lab']
        widgets = [self.region, self.toplabel, self.labfrm, self.configfrm, [self.theme, self.new], 
                    self.fontfrm, self.font_labs]
        for name, widget in zip(names, widgets):
            self.configable_widget.add_widgets_bg(name, widget)
    

    def __init_container(self):     # initialize toolsbar's container 
        self.region = Frame(self.master)
        
        self.toplabel = Label(self.master, height=1, text=' ')
        self.labfrm = Frame(self.region, bg='lightgreen')
        self.configfrm = Frame(self.region, bg='yellow')
        self.fontfrm = Frame(self.region, bg='lightblue')

        self.toplabel.pack(side='top', padx=5, fill='x')
        self.region.pack(side='top', padx=5, fill='x')
        self.labfrm.grid(row=1, column=1, padx=5, sticky='we')
        self.configfrm.grid(row=1, column=0, padx=5)
        self.fontfrm.grid(row=2, column=0, columnspan=2, padx=5, sticky='we')       # last change 

        self.region.columnconfigure(1, weight=1)

        self.__init_configfrm()
        self.__init_fontfrm()

    
    def __init_configfrm(self):
        self.theme = Button(self.configfrm, text='theme', width=10, relief='flat', bd=0)
        self.new = Button(self.configfrm, text='create', width=10, relief='flat', bd=0)
        
        # new create post menu
        self.optmenu = Menu(self.configfrm, tearoff='false', activebackground=ToolsBar.default_optmenu_abg)
        self.optmenu.add_command(label='label text', command=lambda: self.__open_label(1))
        self.optmenu.add_command(label='note book', command=lambda: self.__open_label(2))
        self.optmenu.add_command(label='free edit', command=lambda: self.__open_label(3))
        self.optmenu.add_command(label='cancel', command=self.__cancel)

        # theme post menu
        self.theme_menu = Menu(self.configable_widget, tearoff='false', activebackground=ToolsBar.default_optmenu_abg)
        self.theme_menu.add_command(label='theme 2', command=lambda: self.configManager.set_theme_with_code('2'))
        self.theme_menu.add_command(label='theme 4', command=lambda: self.configManager.set_theme_with_code('4'))
        self.theme_menu.add_command(label='self config', command=lambda: print('self config'))
        
        

        self.theme.pack(side='left', padx=5, pady=5)
        self.new.pack(side='left', padx=5, pady=5)

        self.new.bind('<Button-1>', lambda event, menu=self.optmenu: self.__post_option(event, menu))
        self.optmenu.bind_all('<Button-1>', self.__menu_click)
        self.optmenu.bind_all('<Button-3>', self.__menu_click)

        self.theme.bind('<Button-1>', lambda event, menu=self.theme_menu: self.__post_option(event, menu))
        self.theme_menu.bind('<Button-1>', self.__menu_click)
        self.theme_menu.bind('<Button-3>', self.__menu_click)

    
    def __init_labfrm(self):
        self.label_manager = LabelManager(self)


    def __init_fontfrm(self):
        fonttype = Label(self.fontfrm, text='type:')
        fontsize = Label(self.fontfrm, text='size:')
        fontmode = Label(self.fontfrm, text='mode:')

        fonttype.grid(row=0, column=0, padx=5, pady=5)
        fontsize.grid(row=0, column=2, padx=5, pady=5)
        fontmode.grid(row=0, column=4, padx=5, pady=5)
        self.font_labs = [fonttype, fontsize, fontmode]


    def __menu_click(self, event):
        if self.new['state'] == 'disabled':
            self.__cancel()
        self.new.config(state='normal')
        self.theme.config(state='normal')


    def __post_option(self, event, menu):
        if self.new['state'] == 'disabled':
            return 
        
        widget = event.widget
        x, y = widget.winfo_rootx(), widget.winfo_rooty() + widget.winfo_height()
        widget.config(state='disabled')
        menu.post(x, y) 



    def __open_label(self, order):
        for val in Editer.created_obj.values():
            val.base.get_region().pack_forget()
        
        Launcher.init_create_new(order, self.master, self)
        new_item = list(self.configManager.editers.values())[-1]
        new_item.base.theme_code = self.configManager.theme_code
        new_item.base.get_configable_widget().set_theme_code(new_item.base.theme_code)
        new_item.base.get_configable_widget().set_widget_color()

        self.new.config(state='normal')


    def __cancel(self):
        self.optmenu.unpost()
        self.theme_menu.unpost()
        self.new.config(state='normal') 


    def get_labfrm(self):
        return self.labfrm
    

    def get_configable_widget(self):
        return self.configable_widget 



class PhotoLoader:
    def __init__(self, dir_, pattern: str):
        self.directory = dir_ 
        self.re_pattern = re.compile(pattern)
        
        self.photos: list = None 

        self.__load_photos()

    def __load_photos(self):
        self.photos = []
        photo_list = os.listdir(self.directory)
        photos = [self.directory + '/' + file for file in photo_list]
        self.photos = sorted(photos, key=lambda item: int(self.re_pattern.findall(item)[0]))

    def get_photos(self):
        if self.photos is None:
            return []
        
        return self.photos 

if __name__ == '__main__':
    if hasattr(ctypes.windll.shcore, "SetProcessDpiAwareness"):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    winManager = WinManager()

    photos = PhotoLoader('photo/new_photos', r'photo(\d+)').get_photos()
    launcher = Launcher(winManager, photos)

    winManager.start()   