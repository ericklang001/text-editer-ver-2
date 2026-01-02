import ctypes
import json  
from tkinter import *
from tkinter.ttk import Separator, Style
from configer import ConfigableWidget

class LabelText:
    def __init__(self, master, mode='new'):
        self.default_font = 'Consolas 12 normal'
        self.font_type = self.default_font

        self.master = master 
        self.mode = mode
        
        self.theme_code = '2'
        self.active_fg = __import__('theme').theme[self.theme_code]['labelText']['active']['fg']['open lab fg']

        self.paned = None
        self.labfrm = None 
        self.textfrm = None 
        self.action_lst = None 
        self.lab_lst = None
        self.rmbtn_lst = None 
        self.rment_dict = None   
        self.text_dict = {} 
        self.sep_lst = None
        
        
        self.data_getter = None 
        self.configable_widget = None 

        self.__init_container()
        self.__set_configable_widget()
        self.__init_open_text()


    def __set_configable_widget(self):
        if self.configable_widget is None:
            self.configable_widget = ConfigableWidget('labelText') 

        self.configable_widget.set_theme_code(self.theme_code)
        self.configable_widget.add_widgets_fg('UI fg', self.lab_lst + self.action_lst)
        self.configable_widget.append_fg('UI fg', self.labfrm, self.textfrm)
        self.configable_widget.add_widgets_fg('text fg', list(self.text_dict.values()))
        
        names = ['paned', 'labfrm', 'textfrm', 'actionfrm', 'btnfrm', 'btn', 'lab', 'separator bg', 'text bg']
        widgets = [self.paned, self.labfrm, self.textfrm, self.actionfrm, self.btnfrm, 
                    self.action_lst, self.lab_lst, self.style, list(self.text_dict.values())]
        for name, widget in zip(names, widgets):
            self.configable_widget.add_widgets_bg(name, widget)

        self.configable_widget.add_widgets_active_fg('open lab fg', self)

        # initialize the default theme of labelText 
        self.configable_widget.set_widget_color()


    def __init_container(self):
        # create basic containers 
        self.paned = PanedWindow(self.master)
        
        self.labfrm = LabelFrame(self.paned, text='label', width=200, height=400)
        self.textfrm = LabelFrame(self.paned, text='text', width=600, height=400)

        self.actionfrm = Frame(self.labfrm, relief='groove', bd=2)
        self.btnfrm = Frame(self.labfrm, relief='groove', bd=2)
        # initialize widgets in self.actionfrm, self.btnfrm, self.textfrm
        self.__init_actionfrm()
        if self.mode == 'open':
            self.__load_btnfrm()
        elif self.mode == 'new':
            self.__init_btnfrm()
        self.__pack_all()       # pack all the containers


    def __init_data(self):      # when in mode: open, use the json data to initialize widgets
        if self.data_getter is None:
            self.data_getter = DataGetter('./test/data.json')


    def __load_btnfrm(self):    # in mode: open, initialize method
        if self.lab_lst is None:    # collect created widget, to conveniently config theme 
            self.lab_lst = []
            self.sep_lst = []
            self.rmbtn_lst = []
            self.rment_dict = {}

        self.__init_data()
        content = self.data_getter.content  
        count = 2       # use to corectly grid label and separator in one loop
        self.style = Style()    # seperators' style configer
        self.style.configure('TSeparator', background='green')
        for index, (lab, content) in enumerate(content.items()):
            # open text or delete text label
            btn = Button(self.btnfrm, text=lab, width=12, relief='flat', bd=0, anchor='w',
                        font=self.default_font.replace('normal', 'bold'))
            btn.config(command=lambda lab=btn, content_=content: self.__open_text(lab, content_))
            # rename command widget
            rename = Button(self.btnfrm, text='rename', width=7, relief='groove', bd=2,
                            font=self.default_font.replace('normal', 'bold'), fg='gray',
                            command=lambda btn=btn: self.rename(btn))
            # rename entry widget
            ent = Entry(self.btnfrm, relief='sunken', bd=2, insertbackground='red', 
                    insertborderwidth=5, font=self.default_font)
            ent.bind('<Return>', lambda event, btn=btn: self.__confirm(event, btn))
            # text widget relate to label btn
            text = Text(self.textfrm, fg='green', font=self.default_font)
            text.insert('end', content)
            # just is a separator
            sep = Separator(self.btnfrm, style='TSeparator')

            # grid the widgets 
            sep.grid(row=index*count+1, column=0, columnspan=2, sticky='we', padx=5)
            rename.grid(row=index*count, column=1, padx=5, sticky='nw')
            btn.grid(row=index*count, column=0, padx=5, sticky='nw')

            # updata widget data container
            self.lab_lst.append(btn) 
            self.sep_lst.append(sep)
            self.rmbtn_lst.append(rename)
            self.rment_dict[btn] = ent      # use btn's reference as key, for its grid_info 
            self.text_dict[btn] = text 


    def __init_btnfrm(self):    # in mode: new, initialize method 
        if self.lab_lst is None:    # the same as self.__load_btnfrm
            self.lab_lst = []
            self.sep_lst = []
            self.rmbtn_lst = []
            self.rment_dict = {}

        # open text and delete text label
        lab = 'untitled1'    # default label content
        btn = Button(self.btnfrm, text=lab, width=12, relief='flat', bd=0, anchor='w',
                    font=self.default_font.replace('normal', 'bold'))
        btn.config(command=lambda lab=btn: self.__open_text(lab))
        # rename command widget
        rename = Button(self.btnfrm, text='rename', width=7, relief='groove', bd=2, 
                        font= self.default_font.replace('normal', 'bold'), fg='gray', 
                        command=lambda btn=btn: self.rename(btn))
        # rename entry widget 
        ent = Entry(self.btnfrm, relief='sunken', bd=2, insertbackground='red', 
                    insertborderwidth=5, font=self.default_font)
        ent.bind('<Return>', lambda event, btn=btn: self.__confirm(event, btn))
        # text widget relate to label
        text = Text(self.textfrm, fg='green', font=self.default_font)
        
        self.style = Style()    # separator style configer
        self.style.configure('TSeparator', background='green')
        # just a separator widget
        sep = Separator(self.btnfrm, orient='horizontal', style='TSeparator')
        
        # grid the widgets
        btn.grid(row=0, column=0, padx=5, sticky='nw')
        rename.grid(row=0, column=1, padx=5, sticky='nw')
        sep.grid(row=1, column=0, columnspan=2, padx=5, sticky='we')

        # updata the widget data container
        self.lab_lst.append(btn) 
        self.sep_lst.append(sep)
        self.rmbtn_lst.append(rename)
        self.rment_dict[btn] = ent 
        self.text_dict[btn] = text 


    def __init_actionfrm(self):     # initialize the actionfrm's widgets 
        if self.action_lst is None:
            self.action_lst = []

        addbtn = Button(self.actionfrm, text='add', width=7, command=self.__add_label)
        addbtn.pack(side='left', padx=5, pady=5, anchor='w')

        delbtn = Button(self.actionfrm, text='delete', width=7, command=self.__del_label)
        delbtn.pack(side='left', padx=5, pady=5, anchor='w')

        self.action_lst.append(addbtn)
        self.action_lst.append(delbtn)


    def __init_open_text(self):    # open the first label's text 
        btn = self.lab_lst[0]
        self.__open_text(btn)
        

    def __pack_all(self):       # pack all the containers
        self.labfrm.pack(fill='y', padx=5, pady=5)
        self.textfrm.pack(padx=5, pady=5, fill='both', expand=True)

        self.actionfrm.pack(fill='x', padx=5, pady=5)
        self.btnfrm.pack(padx=5, pady=5, fill='both', expand=True)

        self.paned.add(self.labfrm, padx=3, pady=5)
        self.paned.add(self.textfrm, padx=3, pady=5)

        self.paned.pack(side='top', padx=10, pady=5, fill='both', expand=True)


    def __add_label(self):      
        btn = Button(self.btnfrm, text='unititled', relief='flat', bd=0, width=12, anchor='w',
                    font=self.default_font.replace('normal', 'bold'), 
                    fg=__import__('theme').theme[self.theme_code]['labelText']['fg']['UI fg'],
                    bg=__import__('theme').theme[self.theme_code]['labelText']['bg']['lab'])
        btn.config(command=lambda lab=btn, content='': self.__open_text(lab, content)) 
        rename = Button(self.btnfrm, text='rename', relief='groove', bd=2, fg='gray', width=7, 
                        font=self.default_font.replace('normal', 'bold'), 
                        command=lambda btn=btn: self.rename(btn))
        ent = Entry(self.btnfrm, relief='sunken', bd=2, insertbackground='red', 
                    insertborderwidth=5, font=self.default_font)
        sep = Separator(self.btnfrm, style='TSeparator')
        text = Text(self.textfrm, font=self.default_font,
                    fg=__import__('theme').theme[self.theme_code]['labelText']['fg']['text fg'],
                    bg=__import__('theme').theme[self.theme_code]['labelText']['bg']['text bg'])

        pos = len(self.lab_lst) * 2
        btn.grid(row=pos, column=0, padx=5, sticky='nw')
        rename.grid(row=pos, column=1, padx=5, sticky='nw')
        sep.grid(row=pos+1, column=0, columnspan=2, sticky='we')
        ent.bind('<Return>', lambda event, btn=btn: self.__confirm(event, btn))

        self.lab_lst.append(btn)
        self.sep_lst.append(sep)
        self.rmbtn_lst.append(rename)
        self.rment_dict[btn] = ent 
        self.text_dict[btn] = text 
        self.__open_text(btn)

        self.configable_widget.append_fg('UI fg', btn)      # haven't pass self.lab's reference to configable_widget
        self.configable_widget.append_fg('text fg', text)
        self.configable_widget.append_bg('text bg', text)


    def __del_label(self):
        if len(self.lab_lst) == 1:
            return 
        
        del_btn = None 
        for btn in self.lab_lst:
            if btn['fg'] == self.active_fg:
                del_btn = btn 
                break 
        
        index = self.lab_lst.index(del_btn)
        # delete configable_widget refenrence 
        del_rmbtn = self.rmbtn_lst[index]
        del_rment = self.rment_dict[del_btn]
        del_text = self.text_dict[del_btn]
        self.configable_widget.del_labelText_lab(del_btn, del_rmbtn, del_rment, del_text)
        # destroy widget 
        self.lab_lst[index].destroy()
        self.sep_lst[index].destroy()
        self.rmbtn_lst[index].destroy()
        self.rment_dict[del_btn].destroy()
        self.text_dict[del_btn].destroy()
        # delete local reference 
        self.lab_lst.pop(index)
        self.sep_lst.pop(index)
        self.rmbtn_lst.pop(index)
        self.rment_dict.pop(del_btn)
        self.text_dict.pop(del_btn)
        
        for pos in range(len(self.lab_lst)):
            # forget the grid position 
            self.lab_lst[pos].grid_forget()
            self.rmbtn_lst[pos].grid_forget()
            self.sep_lst[pos].grid_forget()
            # regrid the widgets
            self.lab_lst[pos].grid(row=pos*2, column=0, padx=5, sticky='nw')
            self.rmbtn_lst[pos].grid(row=pos*2, column=1, padx=5, sticky='ne')
            self.sep_lst[pos].grid(row=pos*2+1, column=0, columnspan=2, padx=5, sticky='we')

        self.__init_open_text()
        


    def rename(self, btn):      # method to rename the widget
        row_pos = btn.grid_info()['row']
        self.rment_dict[btn].config(width=20)
        self.rment_dict[btn].grid(row=row_pos, column=0, columnspan=2, ipadx=5, 
                                padx=5)
        self.rment_dict[btn].focus_set()
    

    def __confirm(self, event, btn):
        new_name = event.widget.get()
        if new_name != '':
            btn.config(text=new_name)
        event.widget.grid_forget()


    def __open_text(self, lab, content_=''):
        for widget in self.textfrm.pack_slaves():   # forget grid all all the text widgets
            widget.pack_forget()
        for widget in self.lab_lst:     # clear the active foreground of label
            widget.config(fg=__import__('theme').theme[self.theme_code]['labelText']['fg']['UI fg'])
        
        self.text_dict[lab].pack(padx=5, pady=5, fill='both', expand=True)
        lab.config(fg=self.active_fg)


    def get_region(self):
        return self.paned  
    

    def get_configable_widget(self):
        return self.configable_widget
    
   
    def set_font(self, font_str='Consolas 14 normal'):
        self.font_type = font_str
        for item in self.lab_dict.values():
            item['widget'].config(font=self.font_type)

    
class DataGetter:
    def __init__(self, path_):
        self.path = path_ 
        self.__data = None 

        self.load_data() 

    def load_data(self):
        """
            if successfully, set self.data as a dictionary:
                "length": int,
                "content":{
                    "label_name1": "content1",
                    "label_name2": "content2", 
                    ...
                }
        """
        try:
            with open(self.path, 'r') as f:
                data = f.read()
        except FileNotFoundError as e:
            print('文件错误：初始化的文件路径不存在，请检查，', e)

        try:
            self.__data = json.loads(data)
        except Exception as e:
            print('文件错误：打开的文件内容格式不正确，请检查')
    

    @property 
    def content(self) -> dict[str: str]:
        if self.__data is not None:
            return self.__data['content']
        

    @property 
    def length(self) -> int:
        if self.__data is not None:
            return self.__data['length']
        

    def add_data(self):
        pass 

    def set_path(self, path_):
        self.path = path_ 


if __name__ == '__main__':
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except AttributeError:
        print('attribute error: in setprocessdepawareness(1)')

    root = Tk()
    root.config(bg='#a9b3c4')


    labelText = LabelText(root, 'new')
    # labelText.configable_widget.set_widget_color(fg_dict=__import__('theme').theme['2']['labelText']['fg'],
    #                     bg_dict=__import__('theme').theme['2']['labelText']['bg'],
    #                     active_dict={'fg': {'open lab fg':'red'}, 'bg': {}})
    
    labelText.theme_code = '4'
    labelText.configable_widget.set_theme_code(labelText.theme_code)
    labelText.configable_widget.set_widget_color()

    root.mainloop()
