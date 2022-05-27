from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivymd.uix.toolbar import MDToolbar
from kivy.graphics import Rectangle, Color
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
import requests
from kivy.properties import ObjectProperty, ColorProperty, StringProperty
from kivymd.uix.toolbar import MDToolbar
from kivy.core.window import Window
from kivy.utils import platform
import datetime;from datetime import timedelta
from utils import add_activity_util, current_time_util, base_url
import json
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.list import OneLineIconListItem
from kivy.uix.gridlayout import GridLayout

from kivy.uix.scrollview import ScrollView
import os
import csv
from kivy.metrics import dp
from scroll_table_data import ScrollViewForTable, TableData

import webbrowser
from kivy.uix.dropdown import DropDown
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from itsdangerous import Serializer
# from config import Config

if platform in ['ios','android']:
    print('kivy.utils.platform:::', platform)
else:
    Window.size = (640, 1136)#iphone demensions

class ParentScreen1(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        screenbackground=CanvasWidget()
        self.add_widget(screenbackground,index=99)
        print('ParentScreen1 initialized')

    def on_enter(self):
        print('ParentScreen2 on_enter')

    # def show_password(self, checkbox, value):
    #     if value:
    #         self.root.ids.password.password = True
    #         self.root.ids.password_text.text = "Hide password"
    #     else:
    #         self.root.ids.password.password = True
    #         self.root.ids.password_text.text = "Show password"

    def login_button(self):
        # base_url= 'http://localhost:8000'
        # base_url = 'https://api.what-sticks-health.com'
        response_login = requests.request('GET',base_url + '/login',
            auth=(self.email.text,self.password.text))
        # response = requests.request('GET','https://api.what-sticks-health.com/login',
        #     auth=(self.email.text,self.password.text))
        print('email/password::', self.email.text, self.password.text)
        print("response:::",response_login.status_code)

        if response_login.status_code ==200:
            # TableScreen.stuff=json.loads(response.content.decode('utf-8'))
            print(json.loads(response_login.content.decode('utf-8')))
            print(type(json.loads(response_login.content.decode('utf-8'))))
            # login_token = json.loads(response.text)['token']
            login_token = json.loads(response_login.content.decode('utf-8'))['token']
            print('login_token accepted!')

            url_user_data = base_url + "/user_account_data"
            headers = {'x-access-token': login_token,'Content-Type': 'application/json'}
            response_user_data = requests.request("GET", url_user_data, headers=headers)
            user_data_dict = json.loads(response_user_data.text)
            print(json.loads(response_user_data.text))
            print(type(json.loads(response_user_data.text)))


            # for i in user_data_dict:
            if user_data_dict['email']==self.email.text:

                # ActivityScreen.user_name_str=i['username']
                ParentScreen2.user_timezone=user_data_dict['user_timezone']
                # print('i[user_timezone;;;;',i['user_timezone'])
                # ActivityScreen.user_id_str=i['id']
                ParentScreen2.email=self.email.text
                ActivityScreen.email=self.email.text
                # ActivityScreen.password=self.password.text
                ActivityScreen.login_token=login_token
                ActivityScreen.user_id_str=user_data_dict['id']
                TableScreen.email=self.email.text
                # TableScreen.password=self.password.text
                TableScreen.login_token=login_token
                TableScreen.user_id_str=user_data_dict['id']
                TableData.email=self.email.text
                # TableData.password=self.password.text
                TableData.login_token=login_token
                TableData.user_id_str=user_data_dict['id']
                # print('ParentScreen1 login_button email:::',self.email.text)

                self.app.psm.current="ps2"
                print('BOTH Tokens Accepted! :::', login_token)
            else:
                invalidLogin()


class ParentScreen2(Screen):
    # user_timezone=''
    # email=''
    def __init__(self,**kwargs):
        super(ParentScreen2, self).__init__(**kwargs)
    #Add NavigationLayout
        self.super_box=BoxLayout(orientation ='vertical')
    #Add navigation slide out thingy
        nav_drawer=MDNavigationDrawer(size_hint=(1,.9))
        self.nav_drawer=nav_drawer
    #Add Menu with buttons to navigation slide out thingy aka nav_drawer
        nav_box=NavMenu()
        nav_drawer.add_widget(nav_box)
    #Make canvas for screenbackground
        screenbackground=CanvasWidget()
    #Make toolbar
        toolbar=Toolbar()
        # toolbar.left_action_items=[["menu", lambda x: nav_drawer.set_state("open")]]
        # print('dir(toolbar):::',dir(toolbar))
        toolbar.left_action_items=[["menu", lambda x: self.toggle_nave_bar()]]
    #order of widgets added to self(ParentScreen2) matters:
        self.add_widget(screenbackground,index=99)
        self.add_widget(self.super_box)
        self.add_widget(nav_drawer)
        self.add_widget(toolbar)
        self.count=0
        print('ParentScreen2 initialized')

    def on_enter(self):
        self.get_screens()
    def get_screens(self):
        if hasattr(self,'csm'):
            pass;
        else:
            ActivityScreen.user_timezone=self.user_timezone
            ActivityScreen.email=self.email
            self.csm=ChildScreenManger()
            self.super_box.add_widget(self.csm)
        # try:
        #     self.remove_widget(self.csm)
        # except:
        #     ActivityScreen.user_timezone=self.user_timezone
        #     ActivityScreen.email=self.email
        #     self.csm=ChildScreenManger()
        #     self.super_box.add_widget(self.csm)

        print('ParentScreen2 on_enter')
        # print('parentScreen2 contents after:::', dir(ParentScreen2))
    def toggle_nave_bar(self):
        # print('self.nav_drawer.set_state:::',self.nav_drawer.state)
        if self.nav_drawer.state=='close':
            self.nav_drawer.set_state("open")
        else:
            self.nav_drawer.set_state("close")

class ActivityScreen(Screen):
    email=''
    email_label=ObjectProperty()
    time_thing=ObjectProperty()
    date_thing=ObjectProperty()
    user_timezone=''
    user_id_str=''
    password=''

    # user_timezone='Europe/Paris'#'US/Eastern'
    def __init__(self,**kwargs):
        super(ActivityScreen,self).__init__(**kwargs)
        self.app=MainApp.get_running_app()
        self.date_time_obj=datetime.datetime.now()
        print('ActivityScreen initialized')

    def on_enter(self,*args):

        self.email_label.text=self.email
        self.date_time_now=current_time_util(self.user_timezone)
        self.ids.date_thing.text=self.date_time_now[0]
        self.ids.time_thing.text=self.date_time_now[1]
        print('ActivityScreen on_enter')

    def log_activity(self):
        title=self.title.text
        note=self.note.text
        try:
            datetime_thing=datetime.datetime.strptime(self.ids.date_thing.text +" "+ self.ids.time_thing.text,'%m/%d/%Y %I:%M %p')
            add_activity_util(title, note,self.user_id_str,self.user_timezone,datetime_thing, self.email,self.login_token)
            self.add_widget(ConfirmBox())

        except ValueError:
            self.add_widget(FailBox())
        print('self=Activity Screen')
        print('self.parent.parent.children[0].children::',
            self.parent.parent.children[0].children)
        print('parent.screens:::',self.parent.screens)
        print('self.parent.screens[1].children:::',
            self.parent.screens[1].children[0].children[0].children[0].children[0].children[0].children[0])
        self.table_data=self.parent.screens[1].children[0].children[0].children[0].children[0].children[0].children[0]
        self.table_data.clear_widgets()
        self.table_data.get_table_data()
        self.table_data.add_data_to_table()
        self.table_data.on_size()
        # print('whos the parent:::', self.parent.children, dir(self.parent))


class TableScreen(Screen):
    user_id_str=''
    email=''
    password=''
    # url_get_activities='https://api.what-sticks-health.com/get_user_health_descriptions/'
    def __init__(self,**kwargs):
        super(TableScreen,self).__init__(**kwargs)
        # print('kwargs::',kwargs)
        self.bigger_box=BiggerBox()
        self.rel_layout01=RelativeLayout01()
        self.big_box=BigBox()
        self.rel_layout02=RelativeLayout02()
        self.heading_box=HeadingBox()
        self.rel_layout03=RelativeLayout03()
        # self.scroll_for_table=ScrollViewForTable()

        self.rel_layout02.add_widget(self.heading_box)

        # self.rel_layout03.add_widget(self.scroll_for_table)
        self.big_box.add_widget(self.rel_layout02)
        self.big_box.add_widget(self.rel_layout03)

        self.rel_layout01.add_widget(self.big_box)

        self.bigger_box.add_widget(self.rel_layout01)
        self.add_widget(self.bigger_box)
        print('TableScreen initialized')

        self.scroll_for_table=ScrollViewForTable()
        self.rel_layout03.add_widget(self.scroll_for_table)
        print('this works??')
        self.table_data=TableData()
        print('this does not work')
        self.scroll_for_table.add_widget(self.table_data)

    # def on_enter(self,*args):
    #     self.handle_table_data()
    #     print('TableScreen on_enter')

    # def handle_table_data(self):
    #     if self.scroll_for_table:
    #         # self.rel_layout03.remove_widget(self.scroll_for_table)
    #         # self.scroll_for_table=ScrollViewForTable()
    #         # self.rel_layout03.add_widget(self.scroll_for_table)
    #         # print('TableData REMOVED scrollview')
    #
    #         # print('TableData ABOUT to be initialized')
    #
    #         # self.table_data=TableData(sort_direction='ascending_test')
    #         print('TableScreen handle_table_data self.scroll exists')
    #         print('self.childred:::',self.children)#BiggerBox
    #         print('self.children[0].children::')
    #         # self.scroll_for_table.add_widget(self.table_data)
    #         # print('TableData initialized and ADDED to scrollview')
    #     else:
    #         pass
    #         # self.scroll_for_table=ScrollViewForTable()
    #         # self.rel_layout03.add_widget(self.scroll_for_table)
    #         # print('is this the problem444????')
    #         # print('TableData ABOUT to be initialized')
    #         # self.table_data=TableData(sort_direction='ascending_test')
    #         # self.scroll_for_table.add_widget(self.table_data)
    #
    #
    #         # print('TableData initialized and ADDED to scrollview')

class BiggerBox(BoxLayout):...
class RelativeLayout01(RelativeLayout):...
class BigBox(BoxLayout):...
class RelativeLayout02(RelativeLayout):...

class GridDropDown(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def last_20_btn(self):
        # pass
        print('last 20 seleted')
        # print('some cousin:::',self.parent.parent.parent.parent.children[0])
        # print('looking for table_data:::',
        #     self.parent.parent.parent.parent.children[0].children[0].children[0])
        self.table_data=self.parent.parent.parent.parent.children[0].children[0].children[0]
        # table_data=TableData()
        # print('looking for TableData:', self.table_data)
        self.table_data.clear_widgets()
        self.table_data.entry_count='20'
        self.table_data.get_table_data()
        self.table_data.add_data_to_table()
        self.table_data.on_size()

    def all_entries_btn(self):
        # pass
        print('all')
        self.table_data=self.parent.parent.parent.parent.children[0].children[0].children[0]
        # print('looking for TableData:', table_data)
        self.table_data.clear_widgets()
        self.table_data.entry_count='all_entries'
        self.table_data.get_table_data()
        self.table_data.add_data_to_table()
        self.table_data.on_size()

class HeadingBox(BoxLayout):
    date_btn_sort=ObjectProperty(None)
    act_btn_sort=ObjectProperty(None)
    # table_dropdown=ObjectProperty(None)
    # grid_drop=ObjectProperty(None)
    btn_date_press_count:int
    btn_act_press_count:int
    def __init__(self,**kwargs):
        if 'btn_date_press_count' in kwargs:
            self.btn_date_press_count = kwargs.pop('btn_date_press_count')
        else:
            self.btn_date_press_count = 0
        if 'btn_act_press_count' in kwargs:
            self.btn_act_press_count = kwargs.pop('btn_act_press_count')
        else:
            self.btn_act_press_count = 0
        super().__init__(**kwargs)

    def date_sort_btn(self):
        self.btn_date_press_count+=1
        self.table_data=self.parent.parent.children[0].children[0].children[0]
        #scroll_table_data TableData(GridLayout)
        print('what is table_data::::', self.table_data)
        self.table_data.clear_widgets()
        # if self.btn_date_press_count==0:
        #     pass
        if self.btn_date_press_count%2==1:
            self.table_data.date_sort_direction='ascending'
            self.date_btn_sort.text='ascending'
            self.act_btn_sort.text='sort'
        elif self.btn_date_press_count%2==0:
            self.table_data.date_sort_direction='descending'
            self.date_btn_sort.text='descending'
            self.act_btn_sort.text='sort'
        self.table_data.get_table_data()
        self.table_data.add_data_to_table()
        self.table_data.on_size()
        # HeadingBox Lineage
        # HeadingBox>rel_layout02>big_box>rel_Layout01>bigger_box>table_screen

    def act_sort_btn(self):
        self.btn_act_press_count+=1
        self.table_data=self.parent.parent.children[0].children[0].children[0]
        self.table_data.clear_widgets()
        # if self.btn_act_press_count==0:
        #     pass
        if self.btn_act_press_count%2==1:
            self.table_data.act_sort_direction='ascending'
            self.act_btn_sort.text='ascending'
            self.date_btn_sort.text='sort'
        elif self.btn_act_press_count%2==0:
            self.table_data.act_sort_direction='descending'
            self.act_btn_sort.text='descending'
            self.date_btn_sort.text='sort'
        self.table_data.get_table_data()
        self.table_data.add_data_to_table()
        self.table_data.on_size()

class RelativeLayout03(RelativeLayout):...
# class ScrollViewForTable(ScrollView):...
#
# class TableData(GridLayout):
#     user_id_str: str
#     email: str
#     password: str
#     url_get_activities='https://api.what-sticks-health.com/get_user_health_descriptions/'
#     date_dict={}
#     act_dict={}
#     del_box_dict={}
#     sort_direction:str
#     def __init__(self,**kwargs):
#         if 'sort_direction' in kwargs:
#             self.sort_direction = kwargs.pop('sort_direction')
#         else:
#             self.sort_direction = sort_direction
#         super(TableData,self).__init__(**kwargs)
#         self.get_table_data()
#         self.add_data_to_table()
#         print('TableData initialized')
#         print('sort_direction::',self.sort_direction)
#
#     def get_table_data(self):
#         response = requests.request('GET',
#             self.url_get_activities+str(self.user_id_str),
#             auth=(self.email,self.password))
#         # print('response in TableDAta:::',response.status_code)
#
#         response_decoded=response.content.decode('utf-8')
#         response_data=json.loads(response.content.decode('utf-8'))
#
#         self.row_data_list=[(i['id'],self.convert_datetime(
#             i['datetime_of_activity']),i['var_activity']) for i in response_data]
#         # print('sort_direction::', self.sort_direction)
#         if self.sort_direction=='ascending':
#             # print('self.row_data_list:::',type(self.row_data_list))
#             # print('self.row_dataPlist.sorted():::',self.row_data_list.sort())
#             self.row_data_list.sort(key=lambda k: (k[1]))
#             # print('triggerd if sort_direction::', self.row_data_list)
#         if self.sort_direction=='descending':
#             self.row_data_list.sort(reverse=True)
#
#     def add_data_to_table(self):
#         # self.row_data_list=self.get_table_data()
#
#         for i in self.row_data_list[-20:]:
#             date_time_obj=MDLabel(
#                 text=str(i[1]),
#                 size_hint=(None,None),
#                 size=(self.width*(1/3),dp(50)),
#                 font_size=10, padding=(dp(15),0)
#                 )
#             activity_obj=MDLabel(
#                 text=str(i[2]),
#                 size_hint=(None,None),
#                 size=(self.width*(1/3),dp(50))
#                 )
#             del_box=RelativeLayout(
#                 size_hint=(None,None),
#                 size=(self.width*(1/3),dp(50))
#                 )
#             delete_btn=Button(
#                 text=str(i[0]),
#                 font_size=2,
#                 color=(.5,.5,.5,0),
#                 size_hint=(.5,.5),
#                 pos_hint={'center_x':.5,'center_y':.5}
#                 )
#
#             delete_btn.bind(on_press=self.delete_button_pressed)
#             delete_label=MDLabel(text='delete',pos_hint={'x':.35})
#
#             del_box.add_widget(delete_btn)
#             del_box.add_widget(delete_label)
#             self.date_dict[i[0]]=date_time_obj
#             self.act_dict[i[0]]=activity_obj
#             # self.del_dict[i[0]]=delete_btn
#             self.del_box_dict[i[0]]=del_box
#             self.add_widget(date_time_obj)
#             self.add_widget(activity_obj)
#             self.add_widget(del_box)
#
#     def delete_button_pressed(self,widget):
#         # print('button preseed')
#         # print('widget.text:',str(widget.text))
#         AreYouSureBox.activity_id_str=str(widget.text)
#         AreYouSureBox.email=self.email
#         AreYouSureBox.password=self.password
#         self.parent.parent.parent.parent.parent.parent.add_widget(AreYouSureBox())
#         # print('self.parent:::',self.parent)
#         # print('self.parent.parent:::',self.parent.parent)
#         # print('self.parent.parent.parent.parent.parent.parent.:::',
#         # self.parent.parent.parent.parent.parent.parent)
#
#     def on_size(self, *args):
#         width_size=self.width
#         for i,j in self.date_dict.items():
#             j.width=width_size*(1/3)
#             # if len(j.text)>15:
#             j.font_size=12
#         for i,j in self.act_dict.items():
#             j.width=width_size*(1/3)
#             if len(j.text)>15:
#                 j.font_size=12
#         for i,j in self.del_box_dict.items():
#             j.width=width_size*(1/3)
#
#     def convert_datetime(self,date_time_str):
#         try:
#             date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%f')
#         except ValueError:
#             date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
#         # return date_time_obj.strftime("%m/%d/%Y, %H:%M:%S")
#         return date_time_obj.strftime("%b%-d '%-y %-I:%M%p")#<------Potential hangup!***************!
#
# class AreYouSureBox(BoxLayout):
#     activity_id_str=''
#     email=''
#     password=''
#     url='https://api.what-sticks-health.com/get_health_descriptions/'
#
#     def __init__(self,**kwargs):
#         super().__init__(**kwargs)
#         self.app=MainApp.get_running_app()
#     def yes_button(self):
#
#         response = requests.request('DELETE',self.url+self.activity_id_str, auth=(self.email,self.password))
#         # print('response:::',response.status_code)
#         self.parent.remove_widget(self)
#         self.app.ps2.csm.current="activity_screen"
#         self.app.ps2.csm.current="table_screen"
#
#         # self.parent.remove_widget(self)
#         # self.parent.remove_widget(parent)
#     def no_button(self):
#         self.parent.remove_widget(self)

class NavMenu(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            # Color(127/255,160/255,189/255,1)
            Color(100/255,160/255,189/255,1)
            self.rect=Rectangle(pos=self.pos,size=self.size)
            self.bind(pos=self.update_rect,
                          size=self.update_rect)

        self.orientation="vertical"
        self.app=MainApp.get_running_app()

    def nav_to_activity(self, *args):
        self.app.ps2.csm.current="activity_screen"

    def nav_to_table(self, *args):
        self.app.ps2.csm.current="table_screen"
    def update_rect(self, *args):
            self.rect.pos = self.pos
            self.rect.size = self.size
    def go_to_webiste(self):
        webbrowser.open("https://what-sticks-health.com/")

class Toolbar(MDToolbar):...



class ConfirmBox(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def ok_button(self):
        self.parent.title.text=''
        self.parent.note.text=''
        self.parent.remove_widget(self)

class FailBox(BoxLayout):...

class ChildScreenManger(ScreenManager):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        activity_screen=ActivityScreen(name="activity_screen")
        table_screen=TableScreen(name="table_screen")
        self.add_widget(activity_screen)
        self.add_widget(table_screen)
        self.current="activity_screen"
        print('ChildScreenManger initialized')
    def on_enter(self):
        print('ChildScreenManger on_enter')

class CanvasWidget(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(127/255,160/255,189/255,1)
            self.rect=Rectangle(pos=self.pos,size=self.size)
            self.bind(pos=self.update_rect,
                          size=self.update_rect)
    def update_rect(self, *args):
            self.rect.pos = self.pos
            self.rect.size = self.size

class MainApp(MDApp):
    def build(self):
        self.ps1=ParentScreen1(name='ps1')
        self.ps2=ParentScreen2(name='ps2')
        psm=ScreenManager()
        self.psm=psm
        psm.add_widget(self.ps1)
        psm.add_widget(self.ps2)
        self.icon = "icon.png"
        # self.config_custom = Config()
        return psm

    def show_password(self, checkbox, value):
        if value:
            self.ps1.ids.password.password = False
            self.ps1.ids.password_text.text = "Hide password"
        else:
            self.ps1.ids.password.password = True
            self.ps1.ids.password_text.text = "Show password"

if __name__ == "__main__":
    MainApp().run()
