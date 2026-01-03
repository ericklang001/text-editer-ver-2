import ctypes 
from tkinter import *
from freeEdit import *


__all__ = ['LabelManager', 'LabelUnion']


class LabelManager:
    def __init__(self, masterbase):
        self.master = masterbase.get_labfrm() 
        self.region = Frame(self.master)

        self.theme_code = masterbase.theme_code 

        self.labs = None 
        self.configable_widget = None 
        
        self.region.pack(side='top', fill='x')
        self.__init_labs()
        self.__set_configable_widget(masterbase.get_configable_widget())


    def __set_configable_widget(self, configable_widget):
        self.configable_widget = configable_widget
        self.configable_widget.add_widgets_bg('region labfrm', self.region)


    def __init_labs(self):
        self.labs = dict()


    def add_lab(self, obj_kw, editer=None):
        if self.labs is None:
            self.__init_labs()

        name = obj_kw['name']
        self.labs[name] = LabelUnion(self, obj_kw, self.labs, editer) 


    def get_configable_widget(self):
        return self.configable_widget 


    def get_region(self):
        return self.region 



class LabelUnion:
        default_font = "consolas 10 normal"
        default_choose_font = 'Consolas 10 bold'
        
        font_type = default_font
        choose_font = default_choose_font 


        def __init__(self, masterbase, obj_kw, label_lst, editer=None):
            self.labs = label_lst 
            self.name = obj_kw['name']
            self.region = obj_kw['region']
            self.editer = editer 
            self.configable_widget = None 
            self.master = masterbase.get_region()

            self.theme_code = masterbase.theme_code

            self.frm = Frame(self.master)
            self.lab = Button(self.frm, text=self.name, width=15, padx=5, relief='flat', bd=0, bg='white',
                                font=LabelUnion.default_font, command=self.show_lab)
            self.close = Button(self.frm, text='X', padx=3, relief='flat', bd='0', fg='red', bg='white',
                                font=LabelUnion.default_font.replace('normal', 'bold'), command=self.delete_lab)
            
            self.lab.bind('<Button-3>', self.rename_lab)

            self.__pack_all()
            self.show_lab()
            self.__set_configable_widget(masterbase.get_configable_widget())
        

        def __set_configable_widget(self, configable_widget):
            self.configable_widget = configable_widget
            self.configable_widget.set_theme_code(self.theme_code)

            self.configable_widget.append_fg('UI fg', self.lab)
            
            if self.configable_widget.get_configable_widgets()['fg'].get('close fg') is None:
                self.configable_widget.add_widgets_fg('close fg', [self.close])
                self.configable_widget.add_widgets_bg('lab bg', [self.lab])
                self.configable_widget.add_widgets_bg('close bg', [self.close])
            else:
                self.configable_widget.append_fg('close fg', self.close)
                self.configable_widget.append_bg('lab bg', self.lab)
                self.configable_widget.append_bg('close bg', self.close)

            self.configable_widget.add_widgets_active_fg('choose fg', self.lab)
            self.configable_widget.add_widgets_active_bg('choose bg', self.lab)

            self.configable_widget.set_widget_color()
            self.lab.config(bg=__import__('theme').theme[self.theme_code]['toolsbar']['active']['bg']['choose bg'],
                            fg=__import__('theme').theme[self.theme_code]['toolsbar']['active']['fg']['choose fg'],)


        def rename_lab(self, event):
            win_color = __import__('theme').theme[self.theme_code]['window']
            popup_level = Toplevel(self.region, bg=win_color['popup bg'])
            popup_level.overrideredirect(True)
            popup_level.geometry(f'+{event.x_root}+{event.y_root}')
            popup_level.attributes('-topmost', True)

            Label(popup_level, text='new name', font='Consolas 14 bold', bg=win_color['rename lab bg'],
                    fg=win_color['rename lab fg']
                    ).pack(side='left', padx=5, pady=10)
            entry = Entry(popup_level, width=15, font='consolas 14 normal', fg=win_color['rename ent fg'],
                            bg=win_color['rename ent bg'])
            entry.focus_set()
            entry.pack(padx=5, pady=10)

            def confirm(event):
                value = entry.get()
                if value != '':
                    self.lab.config(text=value)
                popup_level.destroy()
            
            entry.bind('<Return>', confirm)
            entry.bind('<Escape>', lambda event: popup_level.destroy())
            popup_level.bind('<FocusOut>', lambda event: popup_level.destroy())
            


        def delete_lab(self):
            # if there are only one element in labelbar, stop delete operation
            if len(self.labs) == 1:
                print("can't delete the last label")
                return 
            
            # when lab to be deleted is now open
            if self.lab['bg'] == __import__('theme').theme[self.theme_code]['toolsbar']['active']['bg']['choose bg']:
                # open a new label except self
                labs_lst = list(self.labs.values())
                labs_lst.remove(self)
                lab_union = list(labs_lst)[-1]

                lab_union.region.pack(padx=5, pady=5, fill='both', expand=True)
                lab_union.lab.config(bg=__import__('theme').theme[self.theme_code]['toolsbar']['active']['bg']['choose bg'],
                                    fg=__import__('theme').theme[self.theme_code]['toolsbar']['active']['fg']['choose fg'],
                                    font=LabelUnion.choose_font)
            else:
                print('not delete self')
            
            del self.labs[self.name]
            self.region.destroy()
            self.configable_widget.del_UI_fg_widget('UI fg', self.lab)
            self.configable_widget.del_toolsbar_widght(self.lab, self.close)
            self.configable_widget
            self.frm.destroy()
            

            if self.editer is not None:
                self.editer.destroy()


        def show_lab(self):
            for lab_union in self.labs.values():
                lab_union.lab.config(bg=__import__('theme').theme[self.theme_code]['toolsbar']['bg']['lab bg'], 
                                     fg=__import__('theme').theme[self.theme_code]['toolsbar']['fg']['UI fg'],
                                    font=lab_union.font_type)
                lab_union.region.pack_forget()

            self.region.pack(padx=5, pady=5, fill='both', expand=True)  
            self.lab.config(bg=__import__('theme').theme[self.theme_code]['toolsbar']['active']['bg']['choose bg'],
                            fg=__import__('theme').theme[self.theme_code]['toolsbar']['active']['fg']['choose fg'], 
                            font=LabelUnion.choose_font)
            self.region.focus_set()


        def __pack_all(self):
            self.frm.pack(side='left', anchor='w', padx=3, pady=5)
            self.lab.pack(side='left', padx=5, pady=5)
            self.close.pack(side='left')


