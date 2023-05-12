import sqlite3
import calendar
from kivy.uix.behaviors import button
from numpy import nan
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import japanize_matplotlib
import math
import pandas as pd
import datetime
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.metrics import dp
# from kivy.config import Config
# Config.set('graphics', 'width', '640')
# Config.set('graphics', 'height', '480')
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from pandas.io.sql import table_exists
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


# デフォルトに使用するフォントを変更する
resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'meiryo.ttc') #日本語が使用できるように日本語フォントを指定する

def csv_read():
    #csv_file = open("./Book1.csv", "r", encoding="ms932", errors="", newline="" )
    #リスト形式
    f=pd.read_csv("./Book1.csv") #filepath_or_buffer="./Book2.csv", encoding="ms932", sep=",")
    for i in range(len(f)):
        yy=str(f.iloc[i,0]).replace(' ', '')
        mm=str(f.iloc[i,1]).replace(' ', '')
        dd=str(f.iloc[i,2]).replace(' ', '')
        cc=str(f.iloc[i,3])
        date=str(datetime.datetime.now())
        r_sum="0"
        flag="0"
        if cc == "nan":
            cc = ""
        elif cc=="調整":
            flag="1"
        inc=str(f.iloc[i,4])
        pay=str(f.iloc[i,5])
        jal=str(f.iloc[i,8])
        smbc=str(f.iloc[i,9])
        sum=str(f.iloc[i,10])
        if inc =="nan":
            inc="0"
        else:
            inc=inc.replace('.0', '')
        if pay =="nan":
            pay="0"
        else:
            pay=pay.replace('.0', '')
        if jal =="nan":
            jal="0"
        else:
            jal=jal.replace('.0', '')
        if smbc =="nan":
            smbc="0"
        else:
            smbc=smbc.replace('.0', '')
        if sum =="nan":
            sum="0"
        else:
            sum=sum.replace('.0', '')
        #print(cc+inc+","+pay+","+jal+","+smbc+"")     
        c.execute("INSERT INTO articles VALUES (" + yy + ","+ mm+","+dd+",'" + cc + "'," + inc + "," + pay + "," + jal+","+smbc+"," + sum+","+ r_sum + ",'" + date + "'," +flag+")")
    
    conn.commit()



#変数管理
class property:
    year=2021
    month = 0
    window_size_x=720
    window_size_y=480

    window_size = (window_size_x,window_size_y)
    df=None
    table=None
    texWed=None
    selected_btn_line=None
    selected_btn_raw=None
    addmonth=0
prop= property()

Window.size = prop.window_size

#SQL
# 接続。なければDBを作成する。
conn = sqlite3.connect('example.db')
 # カーソルを取得
c = conn.cursor()
# テーブルを作成
#c.execute('DROP TABLE articles')
#c.execute('CREATE TABLE articles  (year, month,day, title, income,pay,JAL,SMBC,sum,real_sum, created datetime,flag)')
# Insert実行
#c.execute("INSERT INTO articles VALUES (2021,8,24,'Amazon',0,0,0,0,0,0,'2020-02-01 00:00:00')")


#prop.df=pd.read_sql_query('SELECT * FROM articles', conn)

def graph(num):
    if num ==0:
        x=[]
        y=[]
        for i in range(len(prop.df)):
            x.append(datetime.date(prop.df.iloc[i,0], prop.df.iloc[i,1],prop.df.iloc[i,2]))
            y.append(prop.df.iloc[i,8])


        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

        # 横軸：日付 periods分の日付を用意します。
        #x=[datetime.date(2021, 8, 1),datetime.date(2021, 8, 10),datetime.date(2021, 10, 1)]
        #x = [datetime.datetime.strptime(s,'%Y-%m-%d') for s in x]
        #x = pd.date_range('2018-08-07 00:00:00', periods=10, freq='d')

        # 縦軸：数値
        #y = [130, 141, 142]

        ax.plot(x,y)

        # 日付ラベルフォーマットを修正
        # 目盛のインターバル変更はこれ追加 /（interval=2）の数値をいじる
        #ax.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=100))
        days = mdates.DayLocator() 
        daysFmt = mdates.DateFormatter('%m-%d')
        #ax.xaxis.set_major_locator(days)
        ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=None, interval=7, tz=None))
        ax.xaxis.set_major_formatter(daysFmt)

        # グラフの表示
        plt.show()

class TextWidget(Widget):
    #text = StringProperty()    # プロパティの追加
    top_text = StringProperty()
    income_text = StringProperty()
    pay_text = StringProperty()
    min_text = StringProperty()
    rate_text = StringProperty()    

    def __init__(self, **kwargs):
        prop.texWed=self
        super(TextWidget, self).__init__(**kwargs)
        self.top_text= str(prop.month) + "月の収支"
        self.income_text=""
        self.pay_text=""
        self.min_text=""
        self.rate_text=""
        #sort()

    def buttonClicked(self):        # ボタンをクリック時
        draw(self)
    def chosei(self):
        content = ChoseiPopup(popup_close=self.popup_close)
        self.popup = Popup(title='調整日の追加', content=content, size_hint=(0.4, 0.4), auto_dismiss=False)
        self.popup.open()
    def csv(self):
        #csv_read()
        pass
    def graph(self):
        graph(0)
    def sql(self):
        content = SQLPopup(popup_close=self.popup_close)
        self.popup = Popup(title='SQL文実行', content=content, size_hint=(0.9, 0.85), auto_dismiss=False)
        self.popup.open()

    def addbutton(self):
        content = PopupMenu(popup_close=self.popup_close)
        self.popup = Popup(title='収支の追加', content=content, size_hint=(0.9, 0.4), auto_dismiss=False)
        self.popup.open()
    def renew(self):
        sort()
        draw(self)
    def popup_close(self):
        #dtime=datetime.datetime.now()
        #c.execute("INSERT INTO articles VALUES (2021,"+str(prop.addmonth)+",10,'Amazon3',0,0,0,0,0,0,'" +str(dtime)+"')")
        
        self.popup.dismiss()

        #表示の更新
        sort()
        draw(self)

    def on_spinner_change(self, value):
        #print('The spinner', self, 'have text', value)
        prop.month = int(value)
        draw(self)
        

def draw(self):
    if prop.month==0:
        self.top_text = "年間の収支"
        sum=pd.read_sql_query("select sum(income), sum(pay) from articles where year = " + str(prop.year), conn)
        income_sum=sum.iloc[0,0]
        pay_sum=sum.iloc[0,1]
        if income_sum==None:
            income_sum=0
            pay_sum=0
        self.income_text = "総収入" + str("{:,}".format(income_sum))+"円"
        self.pay_text = "総支出"+str("{:,}".format(pay_sum))+"円"
        self.min_text = "差引" + str("{:,}".format(income_sum - pay_sum)) + "円"
        self.rate_text = "貯金率" + str(int((income_sum - pay_sum)/income_sum * 1000) / 10) + "%"
        prop.df=pd.read_sql_query("select * from articles order by month, day", conn)
    else:
        sum=pd.read_sql_query("select sum(income), sum(pay) from articles where month = " + str(prop.month), conn)
        income_sum=sum.iloc[0,0]
        pay_sum=sum.iloc[0,1]
        if income_sum==None:
            income_sum=0
            pay_sum=0
        min = income_sum-pay_sum
        
        self.income_text = "総収入" + str("{:,}".format(income_sum))+"円"
        self.pay_text = "総支出"+str("{:,}".format(pay_sum))+"円"
        self.min_text = "差引" + str("{:,}".format(min)) + "円"
        if income_sum == 0:
            #rate=int(min/income_sum * 1000) / 10
            self.rate_text = "貯金率 * %"
        else:
            rate=int(min/income_sum * 1000) / 10
            self.rate_text = "貯金率" + str(rate) + "%"

        #赤字の場合
        if min <0:
            self.ids.minlab.color=(1,0,0)
        elif min>0:
            self.ids.minlab.color=(0,1,0)
        elif min==0:
            self.ids.minlab.color=(1,1,1)
        self.top_text= str(prop.month) + "月の収支"
        prop.df=pd.read_sql_query("select * from articles where month = " + str(prop.month) + " order by month, day", conn)

    self.remove_widget(prop.table)
    prop.table=Table2()
    self.add_widget(prop.table)

def sort():
    prop.df=pd.read_sql_query("select * from articles order by month, day", conn)
    #print(prop.df)
    c.execute("delete from articles")
    

    for i in range(len(prop.df)):
        yy = str(prop.df.iloc[i,0])
        mm = str(prop.df.iloc[i,1])
        dd = str(prop.df.iloc[i,2])
        cc = str(prop.df.iloc[i,3])
        inc = str(prop.df.iloc[i,4])
        pay = str(prop.df.iloc[i,5])
        jal = str(prop.df.iloc[i,6])
        smbc = str(prop.df.iloc[i,7])
        rsum = str(prop.df.iloc[i,9])
        date = str(prop.df.iloc[i,10])
        flag = str(prop.df.iloc[i,11])
        pre_sum = 0
        if i == 0:
            pre_sum = 0
        else:
            pre_sum = int(prop.df.iloc[i-1,8])

        if flag == "1":
            prop.df.iloc[i,8]=str(prop.df.iloc[i,8])
        elif flag == "0":
            prop.df.iloc[i,8]=str(pre_sum + int(inc) - int(pay))
        sum = prop.df.iloc[i,8]
        #print(yy + ","+ mm+","+dd+",'" + cc + "'," + inc + "," + pay + "," + jal+","+smbc+"," + sum+","+rsum + ",'" + date + "'," +flag+")")
        c.execute("INSERT INTO articles VALUES (" + yy + ","+ mm+","+dd+",'" + cc + "'," + inc + "," + pay + "," + jal+","+smbc+"," + sum+","+rsum + ",'" + date + "'," +flag+")")
    
    conn.commit()
    #prop.df=pd.read_sql_query("select * from articles", conn)
    #print(prop.df)
    

class DeletePopup(BoxLayout):
    popup_close = ObjectProperty(None)
    def okbutton(self):    #ポップアップの決定ボタン
        i=prop.selected_btn_line
        yy=str(prop.df.iloc[i,0])
        mm=str(prop.df.iloc[i,1])
        dd=str(prop.df.iloc[i,2])
        cc=str(prop.df.iloc[i,3])
        inc=str(prop.df.iloc[i,4])
        pay=str(prop.df.iloc[i,5])
        sum=str(prop.df.iloc[i,8])
        date=str(prop.df.iloc[i,10])
        c.execute("delete from articles where year=" + yy + " and month=" + mm + " and day=" + dd + " and title='" + cc + "' and income=" + inc + " and pay=" + pay + " and sum=" + sum + " and created ='" + date + "'")
        #conn.commit()
        sort()            
        draw(prop.texWed)        
        self.popup_close()
    def cancelbutton(self):    #ポップアップのキャンセルボタン
        self.popup_close()

class SQLPopup(BoxLayout):
    popup_close = ObjectProperty(None)
    def okbutton(self):    #ポップアップの決定ボタン
        sent = self.ids.sentence.text
        try:
            c.execute(sent)
        except:
            print("Error!")
        self.popup_close()
    def cancelbutton(self):    #ポップアップのキャンセルボタン
        self.popup_close()

#曜日を返す関数
def weekday(now=True, year=None,month=None, day=None):
    dt=None
    if now:
        dt_now = datetime.datetime.now()
        dt = datetime.datetime(dt_now.year, dt_now.month, dt_now.day)
    else:        
        dt = datetime.datetime(year, month, day)   
    w_list = ['(月)', '(火)', '(水)', '(木)', '(金)', '(土)', '(日)']
    wd = w_list[dt.weekday()]
    return wd

class PopupMenu(BoxLayout):
    input = None
    popup_close = ObjectProperty(None)
    #現在月を選択
    dt_now = datetime.datetime.now()
    mon = str(dt_now.month)
    #月の日数を取得
    maxday = calendar.monthrange(dt_now.year, dt_now.month)[1]
    mday=[]
    for i in range(maxday):
        mday.append(str(i+1))

    #現在日を選択
    dd = str(dt_now.day)
    wd = weekday()

    # def __init__(self):
    #     #super().__init__()
    #     pass
    def on_addspinner_change(self, value):#月のプルダウン変更時
        #prop.addmonth=int(value)
        #print(self.ids.textbox1.text)
        #print(value)
        self.mon=str(value)
        #月の日数を取得
        self.maxday = calendar.monthrange(self.dt_now.year, int(value))[1]
        self.mday=[]
        for i in range(self.maxday):
            self.mday.append(str(i+1))
        #print(self.mday)
        #現在日を選択
        self.dd = "1"

        #曜日を選択
        #dt = datetime.datetime(self.dt_now.year, int(value), 1)    
        self.wd=weekday(False, self.dt_now.year, int(value), 1)
        #self.wd = self.w_list[dt.weekday()]

        #更新
        self.ids.day.values=self.mday
        self.ids.day.text=self.dd
        self.ids.youbi.text=self.wd

    def on_dayspinner_change(self, value):#日のプルダウン変更時
        #曜日を選択
        #dt = datetime.datetime(self.dt_now.year, int(self.ids.month.text), int(value))    
        #self.wd = self.w_list[dt.weekday()]
        self.wd=weekday(False, self.dt_now.year, int(self.ids.month.text), int(value))
        self.ids.youbi.text=self.wd

    def okbutton(self):    #ポップアップの決定ボタン
        month = self.ids.month.text
        day = self.ids.day.text
        title = self.ids.catagory.text + self.ids.title.text
        income = self.ids.income2.text
        pay = self.ids.pay2.text
        
        jal = self.ids.jal.text
        smbc = self.ids.smbc.text
        dtime=datetime.datetime.now()
        c.execute("INSERT INTO articles VALUES (2021,"+month+","+ day +",'" + title+"',"+str(income)+","+str(pay)+","+str(jal)+","+str(smbc)+",0,0,'" +str(dtime)+"',0)")
        # コミット
        conn.commit()   

        self.popup_close()
    def cancelbutton(self):    #ポップアップのキャンセルボタン
        self.popup_close()

class ChoseiPopup(BoxLayout):
    input = None
    popup_close = ObjectProperty(None)
    #現在月を選択
    dt_now = datetime.datetime.now()
    mon = str(dt_now.month)
    #月の日数を取得
    maxday = calendar.monthrange(dt_now.year, dt_now.month)[1]
    mday=[]
    for i in range(maxday):
        mday.append(str(i+1))

    #現在日を選択
    dd = str(dt_now.day)
    #曜日を選択
    dt = datetime.datetime(dt_now.year, dt_now.month, dt_now.day)    
    w_list = ['(月)', '(火)', '(水)', '(木)', '(金)', '(土)', '(日)']
    
    wd = w_list[dt.weekday()]

    # def __init__(self):
    #     #super().__init__()
    #     pass
    def on_addspinner_change(self, value):#月のプルダウン変更時
        #prop.addmonth=int(value)
        #print(self.ids.textbox1.text)
        #print(value)
        self.mon=str(value)
        #月の日数を取得
        self.maxday = calendar.monthrange(self.dt_now.year, int(value))[1]
        self.mday=[]
        for i in range(self.maxday):
            self.mday.append(str(i+1))
        #print(self.mday)
        #現在日を選択
        self.dd = "1"
        #曜日を選択
        dt = datetime.datetime(self.dt_now.year, int(value), 1)    
        self.wd = self.w_list[dt.weekday()]

        #更新
        self.ids.day.values=self.mday
        self.ids.day.text=self.dd
        self.ids.youbi.text=self.wd

    def on_dayspinner_change(self, value):#日のプルダウン変更時
        #曜日を選択
        dt = datetime.datetime(self.dt_now.year, int(self.ids.month.text), int(value))    
        self.wd = self.w_list[dt.weekday()]
        self.ids.youbi.text=self.wd

    def okbutton(self):    #ポップアップの決定ボタン
        month = self.ids.month.text
        day = self.ids.day.text
        sum = self.ids.sum.text

        dtime=datetime.datetime.now()
        c.execute("INSERT INTO articles VALUES (2021,"+month+","+ day +",'調整',0,0,0,0," + sum + ",0,'" +str(dtime)+"',1)")
        # コミット
        conn.commit()   

        self.popup_close()
    def cancelbutton(self):    #ポップアップのキャンセルボタン
        self.popup_close()
      
class CustomSpinner(Spinner):
    pass

def get_id(self,  instance):
    for id, widget in self.ids.items():#instance.parent.ids.items():
        if widget.__self__ == instance:
            return id

class Table2(ScrollView):
    def popup_close(self):

        self.popup.dismiss()
    def btn_click(self, btn):
        #print(self.ids.items())
        btn_id=get_id(self,btn)
        #ボタンの行と列
        i,j=btn_id.split('x')
        i=int(i)
        j=int(j)
        if int(j)==0:
            prop.selected_btn_line=i
            content = DeletePopup(popup_close=self.popup_close)
            self.popup = Popup(title='削除', content=content, size_hint=(0.9, 0.4), auto_dismiss=False)
            self.popup.open()
        elif int(j)==1:
            #タイトル
            cc=str(prop.df.iloc[i,3])
            sum=pd.read_sql_query("select sum(income), sum(pay) from articles where title= '" + cc + "'", conn)
            total_sum=pd.read_sql_query("select sum(income), sum(pay) from articles", conn)
            print("income:" + str(sum.iloc[0,0]) + "円 pay:" + str(sum.iloc[0,1]) + "円")

            fig = plt.figure()
            ax1 = fig.add_subplot(1, 2, 1)
            ax2 = fig.add_subplot(1, 2, 2)
            ax1.set_title("収入\n￥" + str(total_sum.iloc[0,0]), fontsize = 22)
            ax2.set_title("支出\n￥" + str(total_sum.iloc[0,1]), fontsize = 22)
            lab1=[cc + "\n￥" + str(sum.iloc[0,0]), "その他"]
            lab2=[cc + "\n￥" + str(sum.iloc[0,1]), "その他"]
            x = np.array([sum.iloc[0,0], total_sum.iloc[0,0] - sum.iloc[0,0]])
            ax1.pie(x, labels=lab1,autopct="%1.1f %%", startangle=90)
            y = np.array([sum.iloc[0,1], total_sum.iloc[0,1] - sum.iloc[0,1]])
            ax2.pie(y, labels=lab2,autopct="%1.1f %%", startangle=90)
            plt.show()


    def __init__(self, **kwargs):
        super(Table2, self).__init__(**kwargs) 
        layout = GridLayout(size_hint=(1, None))
        layout.cols = 8
        #layout.orientation = 'vertical'
        layout.bind(minimum_height=layout.setter('height'))
        column = prop.df.columns.tolist()

        for j in range(8):
            lbl=Label(text=column[j+2],height=30,size_hint=(1,None))
            layout.add_widget(lbl)
        for i in range(len(prop.df)):
            for j in range(8):  #range(len(df.columns)):
                data=""
                if j ==0:
                    data=str(prop.df.iloc[i,0]) +"/" + str(prop.df.iloc[i,1])+"/"+str(prop.df.iloc[i,2])
                elif j==1:
                    data = str(prop.df.iloc[i,j+2])
                elif j >= 2:
                    data = str("{:,}".format(prop.df.iloc[i,j+2]))
                #各項目のボタンを追加
                button_id = str(i) +"x"+ str(j)
                #print(button_id)
                
                
                #色付け
                clr=(1,1,1)
                if prop.df.iloc[i,11] == 1:
                    clr=(0,1,0)
                elif j==0 and weekday(False, prop.df.iloc[i,0], prop.df.iloc[i,1], prop.df.iloc[i,2])=="(日)":
                    clr=(1,0,0)
                elif j==0 and weekday(False, prop.df.iloc[i,0], prop.df.iloc[i,1], prop.df.iloc[i,2])=="(土)":
                    clr=(0,0,1)


                btn = Button(text=data, height=30, size_hint=(1, None), color=clr)
                #idを設定
                self.ids[button_id] = btn
                #関数を紐づけ
                btn.bind(on_release=self.btn_click)

                layout.add_widget(btn)

        root=self
        root.size = (prop.window_size_x,prop.window_size_y * 0.8)
        root.add_widget(layout)


        


    # def __init__(self, **kwargs):
    #     super(Table, self).__init__(**kwargs)
        #button = Button(text='aa')
        #self.add_widget(button)

class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.title = 'greeting'



    def build(self):
        r=TextWidget()
        return r

if __name__ == '__main__':
    TestApp().run()

# コミット
conn.commit()

# コネクションをクローズ
conn.close()
