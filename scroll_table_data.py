from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import os
import csv
from kivy.metrics import dp
import requests;import json;import datetime#;from datetime import timedelta
from kivymd.uix.label import MDLabel
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
# from main import MainApp
from utils import base_url

Builder.load_file("scroll_table_data.kv")
class ScrollViewForTable(ScrollView):...

class TableData(GridLayout):
    user_id_str: str
    email: str
    login_token: str
    url_get_activities=base_url + '/kivy_table01'
    date_dict={}
    act_dict={}
    del_box_dict={}
    date_sort_direction:str
    act_sort_direction:str
    entry_count:str
    def __init__(self,**kwargs):
        #when adding to kwargs, while initizlizing, must remove from kwargs
        #otherwise kv file instructions for this widget won't work
        if 'date_sort_direction' in kwargs:
            self.date_sort_direction = kwargs.pop('date_sort_direction')
        else:
            self.date_sort_direction = ''
        if 'act_sort_direction' in kwargs:
            self.act_sort_direction = kwargs.pop('act_sort_direction')
        else:
            self.act_sort_direction = ''
        if 'entry_count' in kwargs:
            self.entry_count = kwargs.pop('entry_count')
        else:
            self.entry_count = ''
        super(TableData, self).__init__(**kwargs)
        self.get_table_data()
        self.add_data_to_table()
        print('TableData initialized')

    def get_table_data(self):
        headers = {'x-access-token':self.login_token, 'Content-Type': 'application/json'}
        response = requests.request('GET',self.url_get_activities, headers=headers)
        print('url_get_activities:::', self.url_get_activities)
        response_dict = json.loads(response.text)
        print('response_list:::',type(response_dict['content']))
        print('response_list:::', response_dict['content'][0])
        # user_data_dict = response_list
        # print('user_data_dict::', type(response_list[0]), response_list[0])
        # print(user_data_dict[user_data_dict.keys()[0]])
        # response_data=json.loads(response.content.decode('utf-8'))
        self.row_data_list=[[i[0],self.convert_datetime(
            i[1]),i[2], self.make_date_string(i[1])] for i in response_dict['content']]

        #sort row_data_list (aka the api response date from table) asc based on date
        self.row_data_list.sort(key=lambda k: (k[3]))

        if self.entry_count!='all_entries':
            self.row_data_list=self.row_data_list[-20:]

        if self.date_sort_direction=='ascending':
            print('sort ascending triggered')
            self.row_data_list.sort(key=lambda k: (k[1]))
        if self.date_sort_direction=='descending':
            print('sort descending triggered')
            self.row_data_list.sort(key=lambda k: (k[1]),reverse=True)
        if self.act_sort_direction=='ascending':
            # print('sort ascending triggered')
            self.row_data_list.sort(key=lambda k: (k[2]))
        if self.act_sort_direction=='descending':
            # print('sort descending triggered')
            self.row_data_list.sort(key=lambda k: (k[2]),reverse=True)

    def add_data_to_table(self):
        for i in self.row_data_list:
            date_time_obj=Label(text=str(i[1]), size_hint=(None,None),
                size=(self.width*(1/3),dp(50)),
                font_size=10, padding=(dp(15),0))
            activity_obj=Label(text=str(i[2]), size_hint=(None,None), size=(self.width*(1/3),dp(50)))
            del_box=RelativeLayout(size_hint=(None,None),size=(self.width*(1/3),dp(50)))
            delete_btn=Button(text=str(i[0]),
                color=(.5,.5,.5,0),
                size_hint=(.5,.5),
                pos_hint={'center_x':.5,'center_y':.5}
                )
            delete_btn.bind(on_press=self.delete_button_pressed)
            delete_label=Label(text='delete',pos_hint={'x':0}, font_size=15)
            del_box.add_widget(delete_btn)
            del_box.add_widget(delete_label)
            self.date_dict[i[0]]=date_time_obj
            self.act_dict[i[0]]=activity_obj
            self.del_box_dict[i[0]]=del_box
            self.add_widget(date_time_obj)
            self.add_widget(activity_obj)
            self.add_widget(del_box)

    def delete_button_pressed(self,widget):
        AreYouSureBox.activity_id_str=str(widget.text)
        AreYouSureBox.email=self.email
        AreYouSureBox.password=self.password
        self.parent.parent.parent.parent.parent.parent.add_widget(AreYouSureBox())

    def on_size(self, *args):
        width_size=self.width
        for i,j in self.date_dict.items():
            j.width=width_size*(1/3)
            # if len(j.text)>15:
            j.font_size=12
        for i,j in self.act_dict.items():
            j.width=width_size*(1/3)
            if len(j.text)>15:
                j.font_size=12
        for i,j in self.del_box_dict.items():
            j.width=width_size*(1/3)
            # j.font_size=12

    def convert_datetime(self,date_time_str):
        try:
            date_time_obj = datetime.datetime.strptime(date_time_str, '%a, %d %b %Y %H:%M:%S %Z')
        except ValueError:
            # date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
            print("""There is an error converting datetimes in
            scroll_table_data.py or with API call to kivy_table01""")
        # return date_time_obj.strftime("%m/%d/%Y, %H:%M:%S")
        return date_time_obj.strftime("%b%-d '%-y %-I:%M%p")#<------Potential hangup!***************!

    def make_date_string(self,date_time_str):
        date_time_obj = datetime.datetime.strptime(date_time_str, '%a, %d %b %Y %H:%M:%S %Z')
        return date_time_obj.strftime('%Y%m%d')

class AreYouSureBox(BoxLayout):
    activity_id_str=''
    email=''
    password=''
    url='https://api.what-sticks-health.com/get_health_descriptions/'

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # print('find MainApp:::', self.parent)

    def yes_button(self):
        # print('find MainApp:::',
        #     self.parent.children[1].children[0].children[0].children[0].children[0].children[0])
        # parent>table_screen
        # child>
        response = requests.request('DELETE',self.url+self.activity_id_str, auth=(self.email,self.password))
        self.table_data=self.parent.children[1].children[0].children[0].children[0].children[0].children[0]
        # print('table_data dir::::', dir(table_data))
        self.table_data.clear_widgets()
        self.table_data.get_table_data()
        self.table_data.add_data_to_table()
        self.table_data.on_size()
        self.parent.remove_widget(self)

    def no_button(self):
        self.parent.remove_widget(self)
