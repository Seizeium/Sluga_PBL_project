from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')
from kivy.uix.recycleview import RecycleView
from kivymd.uix.pickers.datepicker.datepicker import date
from kivy.uix.gesturesurface import Line
from kivy.uix.actionbar import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.effectwidget import Rectangle
from kivy.uix.actionbar import Button
from kivy.uix.image import Image
from threading import Thread
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.graphics import Color, Rectangle, PopMatrix, PushMatrix
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.animation import Animation
from kivy.clock import Clock 
from kivy.graphics.texture import Texture
from kivy.core.window import Window 
from kivy.uix.spinner import Spinner
from kivy.graphics import Translate
from kivy.core.text import Label as CoreLabel
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from threading import Thread    
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from threading import Thread
from kivy.lang import Builder
from kivy.properties import StringProperty
import threading
import json
import os
import time
import esman

HIS_F = "history.json"

Builder.load_string('''
<RV>:
    viewclass: 'CustomLabel'
    RecycleGridLayout:
        default_size: dp(250), dp(40)
        cols: 1
        size_hint_y: None
        height: self.minimum_height

<CustomLabel>:
    size_hint: None, None
    size: dp(100), dp(50)
    text_size: self.size
    halign: 'left'
    valign: 'middle'
    color: 1,1,1,1 
''')

class CustomLabel(RecycleDataViewBehavior, Label):
    pass

class HisMan:
    @staticmethod
    def load_his():
        try:
            with open("history.json", "r") as f:
                data = f.read().strip() 
                return json.loads(data) if data else []  
        except json.JSONDecodeError:
            return []  
        return []

    @staticmethod
    def sve_his(his):
        with open(HIS_F, "w") as f:
            json.dump(his, f)

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{"text": item } for item in HisMan.load_his()]

def load_audio():
    global audio
    import audio 
    audio = audio

class LoadingScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(
        source="slugal.png",
        size_hint=(None, None),
        size=(400, 400),
        pos_hint={'center_x': 0.5, 'center_y': 0.5}
        ))
        self.load_ani = Image(
        source="image1.png",
        size_hint=(None, None),
        size=(400, 400),
        pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.load_ani)
        anim_image = Animation(opacity = 0, duration=0.5, t='out_quad') 
        anim_image1 = Animation(opacity = 1, duration=0.5, t='out_quad') 
        anim_image += anim_image1
        anim_image.repeat = True
        anim_image.start(self.load_ani)
        print(self.load_ani.opacity)

class MyApp(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dark_mode = True
        self.menu_ste = False
        self.suggt_ste = False
        self.rect_initial_pos = None 
        # self.text = "History"
        # self.label = Label(text="",size_hint=(None, None), size=(100, 50), pos=(50, 50))
        self.rv = RV(size_hint=(None, None), size=(0, 500), pos = (100, 100))
        self.add_widget(self.rv)
        # self.rv.bind(on_resize=self.update_position)
        # self.update_position()  # Call it once initially

        # self.sugg = ['Create a Excel Sheet', '', '', '', '']
        # self.image_initial_pos = No
            # self.rect_label.size = (Window.width * 0.3, 50) 
            # self.rect_label.pos = (1, 1)
        
        self.text_input = TextInput(
            size_hint=(0.4, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.46},
            hint_text="How can I assist you today?",
            background_color=(0, 0, 0, 0),
            foreground_color=(0, 0, 0, 1),
            padding=(10, 10),
            font_size=30,    
        )

        # self.crinput = TextInput(
        #     # size_hint=(0.4, 0.2),
        #     # pos_hint={'center_x': 0.5, 'center_y': 0.46},
        #     hint_text="File Name",
        #     background_color=(0, 0, 0, 0),
        #     # foreground_color=(0, 0, 0, 1),
        #     padding=(10, 10),
        #     font_size=30,    
        # )

        self.add_widget(self.text_input)
        # self.add_widget(self.rect_label)

        self.image = Image(
        source="microphone.png",
        size_hint=(None, None),
        size=(90, 80)
        ) 
        self.add_widget(self.image)

        self.d_mode = Image(
        source="dark_mode.png",
        size_hint=(None, None),
        size=(90, 80)
        )
        self.add_widget(self.d_mode)

        self.image1 = Image(
        source="slugal.png",
        size_hint=(None, None),
        size=(400, 400),
        pos_hint={'center_x': 0.5, 'center_y': 0.5+0.25}
        )
        self.add_widget(self.image1)

        self.SUbut = Button(
                text="",
                size_hint=(0.27, 0.07),
                background_color=(1, 1, 1,0),
                color=(1, 1, 1, 1),
                )
        
        self.SUbut.bind(on_press = self.on_sugg)
        
        self.RRbut = Button(
            text="",
            size_hint=(0.27, 0.07),
            background_color=(1, 1, 1,0),
            color=(1, 1, 1, 1),
            )
        
        self.HIbut = Button(
            text="",
            size_hint=(0.27, 0.07),
            background_color=(1, 1, 1,0),
            color=(1, 1, 1, 1),
            )
        
        self.THbut = Button(
            text="",
            size_hint=(0.27, 0.07),
            background_color=(1, 1, 1,0),
            color=(1, 1, 1, 1),
            )
        
        self.label = Label(
            text="Suggestion",
            font_size=30,
            size_hint=(None, None),
            size=(200, 50),
            halign='left',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))

        self.crlabel = Label(
            text="Create",
            font_size=30,
            size_hint=(None, None),
            size=(200, 50),
            halign='left',
            valign='middle'
        )
        self.crlabel.bind(size=self.crlabel.setter('text_size'))

        self.oplable = Label(
            text="Open",
            font_size=30,
            size_hint=(None, None),
            size=(200, 50),
            halign='left',
            valign='middle'
        )
        self.oplable.bind(size=self.crlabel.setter('text_size'))

        self.edlable = Label(
            text="Edit",
            font_size=30,
            size_hint=(None, None),
            size=(200, 50),
            halign='left',
            valign='middle'
        )
        self.edlable.bind(size=self.crlabel.setter('text_size'))

        self.dellaab = Label(
            text="Delete",
            font_size=30,
            size_hint=(None, None),
            size=(200, 50),
            halign='left',
            valign='middle'
        )
        self.dellaab.bind(size=self.crlabel.setter('text_size'))

        self.label1 = Label(
            text="Recents",
            font_size=30,
            size_hint=(None, None),
            size=(200, 50),
            halign='left',
            valign='middle'
        )
        self.label1.bind(size=self.label.setter('text_size'))
        self.label2 = Label(
            text="History",
            font_size=30,
            size_hint=(None, None),
            size=(200, 50),
            halign='left',
            valign='middle'
        )
        self.label2.bind(size=self.label.setter('text_size'))
        self.label3 = Label(
            text="Theme",
            font_size=30,
            size_hint=(None, None),
            size=(200, 50),
            halign='left',
            valign='middle'
        )
        self.label3.bind(size=self.label.setter('text_size'))

        # self.add_widget(label)

        self.his = Image(
        source="more_vert.png",
        size_hint=(None, None),
        size=(90, 80)
        )
        self.add_widget(self.his)

        self.but = Button(
        text="",
        size_hint=(0.13, 0.15),
        background_color=(1, 1, 1,0),
        color=(1, 1, 1, 1),
        )

        self.add_widget(self.but)

        self.but_m = Button(
        text="",
        size_hint=(0.08, 0.13),
        background_color=(1, 1, 1, 0),
        color=(1, 1, 1, 1),
        )

        self.mic_but = Button(
            text="",
            size_hint=(None, None),  
            size=(90, 90),
            background_color=(1, 1, 1, 0),
            color=(1, 1, 1, 1),
        )

        self.add_widget(self.mic_but)
        self.add_widget(self.but_m)
        self.but.bind(on_press = self.on_click)
        self.mic_but.bind(on_press = self.on_rec)
        self.but_m.bind(on_press = self.on_menu)
        self.is_hovered_image1 = False
        self.is_hovered_image = False
        Clock.schedule_interval(self.check_hover_state, 0.02)
        self.bind(size=self.on_size)

        self.text = ""
        self.pos_text = (10, Window.height - 100) 
        self.bind(pos=self.on_size, size=self.on_size)
        # self.update_canvas()

    def check_hover_state(self, dt):
        parent_window = self.get_parent_window()
        if not parent_window:
            return  
        mouse_pos = self.to_widget(*parent_window.mouse_pos)

        if self.is_mouse_over(self.image1, mouse_pos):
            if not self.is_hovered_image1:
                self.image1.source = "image1.png"
                self.image1.reload()
                self.is_hovered_image1 = True
        else:
            if self.is_hovered_image1:
                self.image1.source = "slugal.png"
                self.image1.reload()
                self.is_hovered_image1 = False

        if self.is_mouse_over(self.image, mouse_pos):
            if not self.is_hovered_image:
                self.animate_hover_in()
                self.is_hovered_image = True
        else:
            if self.is_hovered_image:
                self.animate_hover_out()
                self.is_hovered_image = False

    def on_rec(self, instance):
        if not audio.get_audio_state():
            self.text_input.text = ""  # Clear previous text
            self.text_input.hint_text = "Listening...."
            print("Recording started from UI")

            def update_text(text):
                def update(dt):
                    self.set_text(text)
                    self.text_input.hint_text = "How can I assist you today?"

                Clock.schedule_once(update, 0)

            audio.record_audio(update_text)
        else:
            print("Already recording...")




    def set_text(self, text):
        self.text_input.text = text

    # def _set_text(self, text):
    #     self.text_input.text = text

    def is_mouse_over(self, widget, mouse_pos):
        x, y = widget.pos
        width, height = widget.size
        return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

    def animate_hover_in(self):
        center_x, center_y = self.image.center
        n_wid, n_hgt = 100, 90
        pos_x = center_x - n_wid / 2
        pos_y = center_y - n_hgt / 2
 
        anim = Animation(
            size=(n_wid, n_hgt),          
            pos=(pos_x, pos_y),           
            t='out_quad',                 
            duration=0.2                  
        )
        anim.start(self.image)

    def animate_hover_out(self):
        center_x, center_y = self.image.center
        og_wid, og_hgt = 90, 80  
        pos_x = center_x - og_wid / 2
        pos_y = center_y - og_hgt / 2

        anim = Animation(
            size=(og_wid, og_hgt), 
            pos=(pos_x, pos_y),                      
            t='out_quad',                           
            duration=0.2                             
        )
        
        anim.start(self.image)

    def animate_menu(self, target_x, update_rect, sub_men,  tt, dur):
        self.rect_initial_pos = self.rectt.pos
        # self.rec_mp = self.rec
        anim_this = Animation(pos=(80, Window.height - 85), duration=0.6, t='out_quad') 
        anim_text = Animation(pos_hint={'center_x': target_x}, duration=0.6, t='out_quad')
        anim_image = Animation(pos_hint={'center_x': target_x}, duration=0.6, t='out_quad') 
        anim_his = Animation(size=((Window.width * tt), 500), duration=dur, t = 'in_out_quad')
        anim = Animation(x=((Window.width * target_x) - (self.rectt.size[0] / 2)+self.rect_width-85), duration=0.2)
        anim_but = Animation(x=((Window.width * target_x) - (self.rectt.size[0] / 2)+self.rect_width-85), duration=0.2)
        # anim_his.start(self.rv)
        anim_sug = Animation(size = ((Window.width*sub_men, Window.height * 0.09)),duration=dur, t = 'in_out_quad')
        anim_crd = Animation(size = ((Window.width*sub_men, Window.height * 0.09)),duration=dur, t = 'in_out_quad')
        anim_set = Animation(size = ((Window.width*sub_men, Window.height * 0.09)),duration=dur, t = 'in_out_quad')   
        anim_hisc = Animation(size = ((Window.width*sub_men, Window.height * 0.09)),duration=dur, t = 'in_out_quad')
        # anim_his.start(self.rv)
        anim_set.start(self.setc)
        anim_hisc.start(self.hiscol)
        anim.start(self.image)
        anim_sug.start(self.sugrec)
        anim_crd.start(self.cr_doc)
        anim_but.start(self.mic_but)
        anim_text.start(self.text_input)
        

        # anim_this.start(self.label)
        anim_image.start(self.image1)
        if self.menu_ste == True:
            rect_anim = Animation(size = (Window.width*0, Window.height),  duration=0.2 , t='in_out_quad')
            self.widthx = Window.width*0
        else:
            rect_anim = Animation(size = (Window.width*0.3, Window.height),  duration=0.2, t='in_out_quad')
            self.widthx = Window.width*0.3

        rect_anim.start(self.menu_rec)
        anim_rect = Animation(duration=1, t='out_quad')
        anim_rect.bind(on_progress=update_rect)

        # menu_rect = Animation(duration=1, t='out_quad')
        # menu_rect.bind(on_progress=update_rect)
        anim_rect.start(self)
        # menu_rect.start(self)

    def update_rect(self, instance, value, progress):
        new_x = (Window.width * 0.6) - (self.rectt.size[0] / 2)
        self.rectt.pos = (new_x * progress + self.rectt.pos[0] * (1 - progress), self.rectt.pos[1])
        self.rect_x = (Window.width * 0.6) - (self.rectt.size[0] / 2)

    def update_rect_rev(self, instance, value, progress):
        new_x = (Window.width * 0.5) - (self.rectt.size[0] / 2)
        self.rectt.pos = (new_x * progress + self.rectt.pos[0] * (1 - progress), self.rectt.pos[1])
        self.rect_x = (Window.width * 0.5) - (self.rectt.size[0] / 2)

    def on_size(self, *args):
        print(Window.height, " ", self.rv.pos)
        self.rv.pos = (45, Window.height-620)
        self.canvas.before.clear()
        self.rect_width = self.width * 0.5 
        self.rect_height = self.height * 0.12
        self.rect_x = (self.width - self.rect_width) / 2 
        self.rect_y = (self.height - self.rect_height) / 2 
        self.widthx = Window.width*0

        with self.canvas.before:
            self.rect_color = Color(rgba=( 0.10588,  0.10588,  0.10588, 1))
            Rectangle(pos=(0,0), size=(self.width, self.height))
            self.rrect_color = Color(1, 1, 1, 1) 
            self.rectt = RoundedRectangle(
                pos=(self.rect_x, self.rect_y - 80), 
                size=(self.width*0.5, self.height * 0.26),
                radius=[25])
              
            self.men_col = Color(0.0222, 0.0222, 0.0222, 1) 
            self.menu_rec = Rectangle(
                pos=(0, 0),
                size=(0, Window.height),
            )

            
            self.su_col = Color(0.10588, 0.10588, 0.10588, 1) 
            self.sugrec = RoundedRectangle(
                pos=(30, Window.height-260), 
                size=(0, Window.height * 0.09),
                radius=[25])
            
            self.cre = Color(0.10588, 0.10588, 0.10588, 1) 
            self.crerec = RoundedRectangle(
                pos=(60, Window.height-260 - 110), 
                size=(0, Window.height * 0.08),
                radius=[25])
            self.crlabel.pos[0] = 60+10
            self.crlabel.pos[1] = Window.height - 260 - 110 + 26
            # self.add_widget(self.crlabel)
            
            self.open = Color(0.10588, 0.10588, 0.10588, 1) 
            self.openr = RoundedRectangle(
                pos=(60, Window.height-260 - 220), 
                size=(0, Window.height * 0.08),
                radius=[25])
            
            self.oplable.pos[0] = 60+10
            self.oplable.pos[1] = Window.height - 260 - 220 + 26
            # self.add_widget(self.crlabel)
            
            self.delete = Color(0.10588, 0.10588, 0.10588, 1) 
            self.delete = RoundedRectangle(
                pos=(60, Window.height-260 - 330), 
                size=(0, Window.height * 0.08),
                radius=[25])
            
            self.dellaab.pos[0] = 60+10
            self.dellaab.pos[1] = Window.height - 260 - 330 + 26
            
            self.edit = Color(0.10588, 0.10588, 0.10588, 1) 
            self.editrec = RoundedRectangle(
                pos=(60, Window.height-260 - 440), 
                size=(0, Window.height * 0.08),
                radius=[25])
            
            self.edlable.pos[0] = 60+10
            self.edlable.pos[1] = Window.height - 260 - 440 + 26
            
            self.label.pos[0] = self.sugrec.pos[0] + 35
            self.label.pos[1] = Window.height - 260 + 26
            # self.add_widget(self.label)
            
            self.cr_doc = Color(0.10588, 0.10588, 0.10588, 1) 
            self.cr_doc = RoundedRectangle(
                pos=(30, Window.height-380), 
                size=(0, Window.height * 0.09),
                radius=[25])
            self.label1.pos[0] = self.cr_doc.pos[0] + 35
            self.label1.pos[1] = Window.height - 380 + 26
            # self.add_widget(self.label1)

            self.set_col = Color(0.10588, 0.10588, 0.10588, 1) 
            self.setc = RoundedRectangle(
                pos=(30, Window.height-500), 
                size=(0, Window.height * 0.09),
                radius=[25])
            self.label3.pos[0] = self.setc.pos[0] + 35
            self.label3.pos[1] = Window.height - 500 + 26
            # self.add_widget(self.label3)
            

            self.hisco = Color(0.10588, 0.10588, 0.10588, 1) 
            self.hiscol = RoundedRectangle(
                pos=(30, Window.height-620), 
                size=(0, Window.height * 0.09),
                radius=[25])
            self.label2.pos[0] = self.hiscol.pos[0] + 35
            self.label2.pos[1] = Window.height - 620 + 26
            # self.add_widget(self.label2)
            
            self.SUbut.pos[0] = self.sugrec.pos[0] 
            self.SUbut.pos[1] = Window.height - 260 + 15

            self.RRbut.pos[0] = self.sugrec.pos[0] 
            self.RRbut.pos[1] = Window.height - 380 + 15

            self.HIbut.pos[0] = self.sugrec.pos[0] 
            self.HIbut.pos[1] = Window.height - 500 + 15

            self.THbut.pos[0] = self.sugrec.pos[0] 
            self.THbut.pos[1] = Window.height - 620 + 15

            # self.add_widget(self.SUbut)
            # self.add_widget(self.RRbut)
            # self.add_widget(self.HIbut)
            # self.add_widget(self.THbut)
            # self.su_col = Color(1, 0.0222, 0.0222, 1) 
            # self.sugrec = RoundedRectangle(
            #     pos=(30, Window.height-260), 
            #     size=(0, Window.height * 0.09),
            #     radius=[25])
            
            # self.su_col = Color(1, 0.0222, 0.0222, 1) 
            # self.sugrec = RoundedRectangle(
            #     pos=(30, Window.height-260), 
            #     size=(0, Window.height * 0.09),
            #     radius=[25])
            

        # with self.canvas.before:
        #     Color(1, 1, 1, 1)  
        #     self.label = CoreLabel(text="History", font_size=(45))
        #     self.label.refresh()
        #     texture = self.label.texture

        #     PushMatrix()
        #     Translate(0, Window.height - 85)
        #     Rectangle(texture=texture, size=texture.size)
        #     PopMatrix()
        # with self.canvas.after:
        #     rv = RV(size_hint=(None, None), size=(300, 500), pos=(100, Window.height - 100)) 
            
            # self.history_view = HisView(size_hint=(1, 0.8), pos_hint={"x": 0, "y": 0.2})
            # self.add_widget(self.history_view)
        # self.add_widget(self.label)

        self.image.pos = (self.rect_x + self.rect_width - 85, self.rect_y - 75)
        self.image1.pos = (self.rect_x + self.rect_width/2 - 150, self.rect_y+60)
        self.d_mode.pos = (self.width - 100, self.height-100)
        self.his.pos = (5, self.height-100)
        self.but.pos = self.d_mode.pos
        self.but_m.pos = self.his.pos
        self.mic_but.pos = self.image.pos

    def dr_rec(self, *args):
        with self.canvas.before:
            Color(1, 1, 1, 1) 
            self.rectt = RoundedRectangle(
                pos=(self.rect_x, self.rect_y - 80), 
                size=(self.width*0.5, self.height * 0.26),
                radius=[25])
            if self.dark_mode == True:
                self.men_col = Color(0.0222, 0.0222, 0.0222, 1) 
            else:
                self.men_col = Color(1,1,1,1)
            self.menu_rec = Rectangle(
                pos=(0, 0),
                size=(0, Window.height), 
            )
            
            
    def create_gradient(self):
        texture = Texture.create(size=(2, 2), colorfmt='rgba')
        texture.blit_buffer(
            b'\xff\xe6\xe6\xff'  
            b'\xe6\xe6\xff\xff'  
            b'\xff\xf5\xf5\xff'  
            b'\xff\xe6\xff\xff',
            colorfmt='rgba', bufferfmt='ubyte')
        texture.wrap = 'repeat'
        texture.mag_filter = 'linear'
        return texture

    def anim_sugge(self, tt,ss): 
            
        anim_sug = Animation(pos = (self.sugrec.pos[0], (Window.height-380)-tt), t = 'in_out_quad')
        anim_sug.start(self.cr_doc)

        crear = Animation(size = (Window.width*ss, (Window.height * 0.08)), t = 'in_out_quad')
        crear.start(self.crerec)

        crear = Animation(size = (Window.width*ss, (Window.height * 0.08)), t = 'in_out_quad')
        crear.start(self.openr)

        crear = Animation(size = (Window.width*ss, (Window.height * 0.08)), t = 'in_out_quad')
        crear.start(self.delete)

        crear = Animation(size = (Window.width*ss, (Window.height * 0.08)), t = 'in_out_quad')
        crear.start(self.editrec)

        anim_crd = Animation(pos = (self.cr_doc.pos[0], (Window.height-500)-tt), t = 'in_out_quad')
        anim_crd.start(self.setc)

        but1 = Animation(pos = (self.sugrec.pos[0], (Window.height-380)-tt), t = 'in_out_quad')
        but1.start(self.RRbut)

        anim_hisc = Animation(pos = (self.hiscol.pos[0], (Window.height-620)-tt), t = 'in_out_quad')
        anim_hisc.start(self.hiscol)

        but2 = Animation(pos = (self.hiscol.pos[0], (Window.height-500)-tt), t = 'in_out_quad')
        but2.start(self.HIbut)

        but4 = Animation(pos = (self.hiscol.pos[0], (Window.height-500)-tt), t = 'in_out_quad')
        but4.start(self.THbut)

        anim_all = Animation(pos = (self.label.pos[0], ( Window.height - 380 + 26) - tt), t = 'in_out_quad')
        anim_all.start(self.label1)

        anim_all1 = Animation(pos = (self.label1.pos[0], (Window.height - 500 + 26) -tt), t = 'in_out_quad')
        anim_all1.start(self.label3)

        anim_all2 = Animation(pos = (self.label3.pos[0], (Window.height - 620 + 26) - tt), t = 'in_out_quad')
        anim_all2.start(self.label2)



    def on_sugg(self, instance):
        if not self.suggt_ste:
            self.suggt_ste = True
            self.anim_sugge(450, 0.23)
            self.add_widget(self.crlabel)
            self.add_widget(self.oplable)
            self.add_widget(self.edlable)
            self.add_widget(self.dellaab)
            # self.add_widget(self.crinput)
        else:
            self.suggt_ste = False
            self.anim_sugge(0, 0)
            self.remove_widget(self.crlabel)
            self.remove_widget(self.oplable)
            self.remove_widget(self.edlable)
            self.remove_widget(self.dellaab)

    def on_click(self, instance):
        self.canvas.before.clear() 
        if self.dark_mode:
            self.rrect_color.rgb = (0.92156, 0.92156, 0.92156, 1)
            self.d_mode.source = "light_mode.png"
            self.his.source = "more_vertd.png"
            with self.canvas.before:
                Rectangle(texture=self.create_gradient(), pos=self.pos, size=self.size)
            self.dark_mode = False
        else:
            self.rect_color.rgb = (0.10588, 0.10588, 0.10588, 1)
            self.rrect_color.rgb = (1, 1, 1, 1)
            self.d_mode.source = "dark_mode.png"
            self.his.source = "more_vert.png"
            with self.canvas.before:
                Color(0.10588, 0.10588, 0.10588, 1) 
                Rectangle(pos=self.pos, size=self.size)

            self.dark_mode = True
        print(Window.height, "*", Window.width, "=", Window.height*Window.width)
        self.dr_rec()

    def on_menu(self, instance): 
        if not self.menu_ste:
            self.animate_menu(0.6, self.update_rect,0.267, 0.3, 0.2)
            # self.lay.add_widget(self.label)
            self.menu_ste = True
            self.add_widget(self.label1)
            self.add_widget(self.label)
            self.add_widget(self.label3)
            self.add_widget(self.label2)
            self.add_widget(self.SUbut)
            self.add_widget(self.RRbut)
            self.add_widget(self.HIbut)
            self.add_widget(self.THbut)
        else:
            self.animate_menu(0.5,self.update_rect_rev , 0,0, 0.2)
            # self.lay.remove_widget(self.label)
            self.menu_ste = False
            self.remove_widget(self.label1)
            self.remove_widget(self.label)
            self.remove_widget(self.label3)
            self.remove_widget(self.label2)

            self.remove_widget(self.SUbut)
            self.remove_widget(self.RRbut)
            self.remove_widget(self.HIbut)
            self.remove_widget(self.THbut)

            

class MainApp(App):
    def build(self):
        self.root_layout = LoadingScreen()
        Clock.schedule_once(self.load_whisper_model, 0)
        return self.root_layout

    def load_whisper_model(self, dt):
        def background_load():
            load_audio() 
            Clock.schedule_once(self.switch_to_main_screen, 0) 

        threading.Thread(target=background_load, daemon=True).start()

    def switch_to_main_screen(self, dt):
        self.root.clear_widgets()
        self.root.add_widget(MyApp())
    
if __name__ == "__main__":
    MainApp().run()
