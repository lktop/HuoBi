import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem,QWidget,QHBoxLayout,QTableWidget,QPushButton,QVBoxLayout,QCheckBox,QAbstractItemView,QHeaderView,QLabel,QFrame
from untitled import *
import pymysql,time,json,traceback
from PyQt5.QtWidgets import QTableWidget,QFrame,QAbstractItemView
from PyQt5.QtGui import QFont,QColor
from PyQt5.QtCore import Qt

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        # self.setFixedSize(self.width(), self.height())
        self.table1dict = {}
        # self.table1.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        # self.table2.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.table1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)



    def update_item_data(self, data):
        """更新内容"""
        newData=eval(data)
        #print(newData)
        #第一次初始化
        if self.table2.rowCount()==0:
            for i in range(0,len(list(newData.keys()))):
                #print(i,newData.keys())
                self.table2.insertRow(i)

            n=0
            for i in newData.keys():
                ck = QCheckBox()
                ck.id_=i
                ck.stateChanged.connect(self.statechange)
                h = QHBoxLayout()
                h.setAlignment(Qt.AlignCenter)
                h.addWidget(ck)
                w = QWidget()
                w.setLayout(h)
                self.table2.setItem(n,0,QTableWidgetItem(i))
                self.table2.setItem(n, 1, QTableWidgetItem(str(newData[i]["min60"]["open"]+"||"+newData[i]["min60"]["close"]+"||"+newData[i]["min60"]["vol"])))
                self.table2.setItem(n, 2, QTableWidgetItem(str(newData[i]["min30"]["open"] + "||" + newData[i]["min30"]["close"] + "||" + newData[i]["min30"]["vol"])))
                self.table2.setItem(n, 3, QTableWidgetItem(str(newData[i]["min15"]["open"] + "||" + newData[i]["min15"]["close"] + "||" + newData[i]["min15"]["vol"])))
                self.table2.setItem(n, 4, QTableWidgetItem(str(newData[i]["min5"]["open"] + "||" + newData[i]["min5"]["close"] + "||" + newData[i]["min5"]["vol"])))
                self.table2.setCellWidget(n, 7, w)
                n+=1
        else:
         #之后的数据更新
            for i in newData.keys():
                for n in range(0,self.table2.rowCount()):
                    #i和self.table2.item(n,0).text() 都是币种参数
                    if self.table2.item(n,0).text()==i:
                        self.table2.setItem(n, 1, QTableWidgetItem(str(
                            newData[i]["min60"]["open"] + "||" + newData[i]["min60"]["close"] + "||" +
                            newData[i]["min60"]["vol"])))
                        self.table2.setItem(n, 2, QTableWidgetItem(str(
                            newData[i]["min30"]["open"] + "||" + newData[i]["min30"]["close"] + "||" +
                            newData[i]["min30"]["vol"])))
                        self.table2.setItem(n, 3, QTableWidgetItem(str(
                            newData[i]["min15"]["open"] + "||" + newData[i]["min15"]["close"] + "||" +
                            newData[i]["min15"]["vol"])))
                        self.table2.setItem(n, 4, QTableWidgetItem(str(
                            newData[i]["min5"]["open"] + "||" + newData[i]["min5"]["close"] + "||" + newData[i]["min5"][
                                "vol"])))
                        ck = QCheckBox()
                        ck.id_ = i
                        h = QHBoxLayout()
                        h.setAlignment(Qt.AlignCenter)
                        h.addWidget(ck)
                        w = QWidget()
                        w.setLayout(h)
                        #print('self.table1dict.keys():',self.table1dict.keys())
                        #self.table1dict.keys()为报警的币种
                        if i in list(self.table1dict.keys()):
                            #print('self.table1dict[i][6]=',self.table1dict[i][6])
                            if self.table1dict[i][6] != "":#锁定check
                                ck.setChecked(True)
                                self.table2.setCellWidget(n, 7, w)
                            else:
                                self.table2.setCellWidget(n, 7, w)
                        else:
                            self.table2.setCellWidget(n, 7, w)
                        ck.stateChanged.connect(self.statechange)


        try:
            #买入设置
            self.buySet()
            #锁定
            # self.lockUp()
            #三倍
            self.sanbei()
            #表一清除
            for i in list(self.table1dict.keys()):
                if self.table1dict[i][6]=='' and self.table1dict[i][7]=='' and self.table1dict[i][8]=='' and self.table1dict[i][9]=='':
                    del self.table1dict[i]
            #上表数据更新
            self.table1UpData()
            #上表数据填充
            self.table1Tian()
            # 居中处理
            self.centSet()
            #print(self.table1dict)
        except Exception as e:
            pass

    def buySet(self):
        try:
            for i in range(0,self.table1.rowCount()):
                if str(type(self.table1.item(i,5)))!="<class 'NoneType'>":
                    close=float(self.table1.item(i,4).text().split("||")[1])
                    if self.table1.item(i,5).text()!='':
                        if close<=0.9*float(self.table1.item(i,5).text()):
                            self.table1dict[self.table1.item(i,0).text()][5]='1'
                        else:
                            self.table1dict[self.table1.item(i,0).text()][5] = ''
                    else:
                        self.table1dict[self.table1.item(i, 0).text()][5] = ''
        except:
            traceback.print_exc()

    def statechange(self,state):
        # 锁定
        checkBox = self.sender()
        print(state)
        print(checkBox.id_)
        if state==2:
            if checkBox.id_ in list(self.table1dict.keys()):
                self.table1dict[checkBox.id_][6] = 'check'
                # print("{}check".format(checkBox.id_))
            else:
                self.table1dict[checkBox.id_] = ['', '', '', '', '', '', 'check', '', '', '']
        else:
            if checkBox.id_ in list(self.table1dict.keys()):
                self.table1dict[checkBox.id_][6] = ''
            else:
                self.table1dict[checkBox.id_] = ['', '', '', '', '', '', '', '', '', '']
        #print('self.table1dict.keys()',self.table1dict.keys(),self.table1dict[checkBox.id_])
        #self.table1dict.keys() ['btmusdt', 'aeusdt', 'actusdt', 'bixusdt', 'bsvusdt', 'btcusdt', 'bchusdt', 'adausdt']
        # self.table1dict[checkBox.id_] ['0.01096||0.01096||0.0', '0.01096||0.01096||0.0', '0.01096||0.01096||0.0', '0.01096||0.01
        #096||0.0', '', '', 'check', 'min15vol>=min5vol', 'min30vol>=min15vol', 'min60vol>=min30vol']

        for i in list(self.table1dict.keys()):
            if self.table1dict[i][6]=='' and self.table1dict[i][7]=='' and self.table1dict[i][8]=='' and self.table1dict[i][9]=='':
                del self.table1dict[i]



    def centSet(self):
        for i in range(0,self.table2.rowCount()):
            self.table2.item(i,0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table2.item(i, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table2.item(i, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table2.item(i, 3).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table2.item(i, 4).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            try:
                self.table2.item(i, 5).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            except:
                # print("买入价未设置!")
                pass

        for i in range(0,self.table1.rowCount()):
            self.table1.item(i,0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table1.item(i, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table1.item(i, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table1.item(i, 3).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table1.item(i, 4).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            try:
                self.table1.item(i, 5).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            except:
                # print("买入价未设置!")
                pass

    def lockUp(self):
        ischecklist = []
        n = 0
        for i in self.checklist:
            if bool(i.isChecked()):
                ischecklist.append(n)
            n += 1
        for i in ischecklist:
            market = self.table2.item(i, 0).text()
            self.table1dict[market] = ['', '', '', '', '', '', 'check', '', '', '']
        ischecklist = []
        n = 0
        for i in self.checklist:
            if bool(i.isChecked()):
                ischecklist.append(n)
            n += 1
        for i in ischecklist:
            market = self.table2.item(i, 0).text()
            self.table1dict[market] = ['', '', '', '', '', '', 'check', '', '', '']



    def sanbei(self):
        row=self.table2.rowCount()
        for i in range(0,row):
            market=self.table2.item(i, 0).text()
            min5vol=float(self.table2.item(i,4).text().split("||")[2])
            min15vol = float(self.table2.item(i,3).text().split("||")[2])
            min30vol = float(self.table2.item(i,2).text().split("||")[2])
            min60vol = float(self.table2.item(i,1).text().split("||")[2])
            if min15vol>= 3*min5vol:
                if market in self.table1dict.keys():
                    self.table1dict[market][7]="min15vol>=min5vol"
                else:
                    self.table1dict[market] = ['', '', '', '', '', '', '', 'min15vol>=min5vol', '', '']
                self.table2.item(i,3).setBackground(QColor(240, 14, 59))
            else:
                if market in self.table1dict.keys():
                    self.table1dict[market][7]=""


            if min30vol >= 3 * min15vol:
                if market in self.table1dict.keys():
                    self.table1dict[market][8] ="min30vol>=min15vol"
                else:
                    self.table1dict[market] = ['', '', '', '', '', '', '', '', 'min30vol>=min15vol', '']
                self.table2.item(i, 2).setBackground(QColor(240, 14, 59))
            else:
                if market in self.table1dict.keys():
                    self.table1dict[market][8] = ""


            if min60vol >= 3 * min30vol:
                if market in self.table1dict.keys():
                    self.table1dict[market][9] ="min60vol>=min30vol"
                else:
                    self.table1dict[market] = ['', '', '', '', '', '', '', '', '', 'min60vol>=min30vol']
                self.table2.item(i, 1).setBackground(QColor(240, 14, 59))
            else:
                if market in self.table1dict.keys():
                    self.table1dict[market][9] =""

    def table1UpData(self):
        for i in list(self.table1dict.keys()):
            min60, min30, min15, min5, buyPrice, jingshi, check, sanbei=self.searchData(i)
            self.table1dict[i][0]=min60
            self.table1dict[i][1] = min30
            self.table1dict[i][2] = min15
            self.table1dict[i][3] = min5
            # self.table1dict[i][4] = buyPrice
            # self.table1dict[i][5] = jingshi

    def searchData(self,market):
        row=self.table2.rowCount()
        for i in range(0,row):
            if self.table2.item(i,0).text()==market:
                min60=self.table2.item(i,1).text()
                min30=self.table2.item(i,2).text()
                min15 =self.table2.item(i,3).text()
                min5 =self.table2.item(i,4).text()
                buyPrice = self.table2.item(i, 5)
                jingshi = self.table2.item(i, 6)
                check = self.table2.item(i, 7)
                sanbei = self.table2.item(i, 8)
                return min60,min30,min15,min5,buyPrice,jingshi,check,sanbei
        return None

    def table1Tian(self):
        if self.table1.rowCount()==0:
            for i in range(0,len(list(self.table1dict.keys()))):
                self.table1.insertRow(i)
            n=0
            for i in (self.table1dict.keys()):
                self.table1.setItem(n,0,QTableWidgetItem(i))
                self.table1.setItem(n, 1, QTableWidgetItem(self.table1dict[i][0]))
                self.table1.setItem(n, 2, QTableWidgetItem(self.table1dict[i][1]))
                self.table1.setItem(n, 3, QTableWidgetItem(self.table1dict[i][2]))
                self.table1.setItem(n, 4, QTableWidgetItem(self.table1dict[i][3]))
                self.table1.setItem(n, 6, QTableWidgetItem(''))
                if self.table1dict[i][7]!='':
                    self.table1.item(n, 3).setBackground(QColor(240, 14, 59))
                if self.table1dict[i][8] != '':
                    self.table1.item(n, 2).setBackground(QColor(240, 14, 59))
                if self.table1dict[i][9] != '':
                    self.table1.item(n, 1).setBackground(QColor(240, 14, 59))
                ck = QCheckBox()
                ck.id_=i
                h = QHBoxLayout()
                h.setAlignment(Qt.AlignCenter)
                h.addWidget(ck)
                w = QWidget()
                w.setLayout(h)
                if self.table1dict[i][6]!="":
                    ck.setChecked(True)
                    self.table1.setCellWidget(n, 7, w)
                else:
                    self.table1.setCellWidget(n, 7, w)
                ck.stateChanged.connect(self.statechange)
           #     print(self.table1.item(n,7))
                if self.table1dict[i][5]!="":
                    self.table1.item(n, 6).setBackground(QColor(240, 14, 59))
                n=n+1
        else:
            for i in range(0,self.table1.rowCount()):
                if self.table1.item(i,0).text() in list(self.table1dict.keys()):
                    self.table1.setItem(i,1,QTableWidgetItem(self.table1dict[self.table1.item(i,0).text()][0]))
                    self.table1.setItem(i, 2, QTableWidgetItem(self.table1dict[self.table1.item(i, 0).text()][1]))
                    self.table1.setItem(i,3, QTableWidgetItem(self.table1dict[self.table1.item(i, 0).text()][2]))
                    self.table1.setItem(i, 4, QTableWidgetItem(self.table1dict[self.table1.item(i, 0).text()][3]))
                    self.table1.setItem(i, 6, QTableWidgetItem(''))
                    if self.table1dict[self.table1.item(i,0).text()][7] != '':
                        self.table1.item(i, 3).setBackground(QColor(240, 14, 59))
                    if self.table1dict[self.table1.item(i,0).text()][8] != '':
                        self.table1.item(i, 2).setBackground(QColor(240, 14, 59))
                    if self.table1dict[self.table1.item(i,0).text()][9] != '':
                        self.table1.item(i, 1).setBackground(QColor(240, 14, 59))
                    ck = QCheckBox()
                    ck.id_ = self.table1.item(i,0).text()
                    h = QHBoxLayout()
                    h.setAlignment(Qt.AlignCenter)
                    h.addWidget(ck)
                    w = QWidget()
                    w.setLayout(h)
                    if self.table1dict[self.table1.item(i, 0).text()][6] != "":
                        ck.setChecked(True)
                        self.table1.setCellWidget(i, 7, w)
                    else:
                        self.table1.setCellWidget(i, 7, w)
                    ck.stateChanged.connect(self.statechange)

                    if self.table1dict[self.table1.item(i, 0).text()][5] != "":
                        self.table1.item(i, 6).setBackground(QColor(240, 14, 59))

                else:
                    self.table1.removeRow(i)

            nowlist=[]
            for i in range(0, self.table1.rowCount()):
                nowlist.append(self.table1.item(i,0).text())
            needInsert=[]
            for i in list(self.table1dict.keys()):
                if not(i in nowlist):
                    needInsert.append(i)

            row=self.table1.rowCount()
            k=row+len(needInsert)
            for i in range(row,k):
                self.table1.insertRow(i)
            for i in range(row, k):
                market=needInsert.pop()
                self.table1.setItem(i, 0, QTableWidgetItem(market))
                self.table1.setItem(i, 1, QTableWidgetItem(self.table1dict[market][0]))
                self.table1.setItem(i, 2, QTableWidgetItem(self.table1dict[market][1]))
                self.table1.setItem(i, 3, QTableWidgetItem(self.table1dict[market][2]))
                self.table1.setItem(i, 4, QTableWidgetItem(self.table1dict[market][3]))
                self.table1.setItem(i, 6, QTableWidgetItem(''))
                if self.table1dict[market][7] != '':
                    self.table1.item(i, 3).setBackground(QColor(240, 14, 59))
                if self.table1dict[market][8] != '':
                    self.table1.item(i, 2).setBackground(QColor(240, 14, 59))
                if self.table1dict[market][9] != '':
                    self.table1.item(i, 1).setBackground(QColor(240, 14, 59))

                ck = QCheckBox()
                ck.id_ = market
                h = QHBoxLayout()
                h.setAlignment(Qt.AlignCenter)
                h.addWidget(ck)
                w = QWidget()
                w.setLayout(h)
                if self.table1dict[market][6] != "":
                    ck.setChecked(True)
                    self.table1.setCellWidget(i, 7, w)
                else:
                    self.table1.setCellWidget(i, 7, w)
                ck.stateChanged.connect(self.statechange)

                if self.table1dict[market][5] != "":
                    self.table1.item(i, 6).setBackground(QColor(240, 14, 59))

            # print(needInsert)




class UpdateData(QThread):
    """更新数据类"""
    update_date = pyqtSignal(str)  # pyqt5 支持python3的str，没有Qstring

    def run(self):
        db = pymysql.connect(host='localhost', port=3306, db='huobi190', user='root', passwd='root', charset='utf8')
        cursor = db.cursor()
        while True:
            cursor.execute("SELECT * FROM huobi")
            marketdict= {}
            print("--------------------while--------")
            for i in cursor.fetchall():
                data=str(i)
                data = data.split("'")
                market = data[1]
                min5 = data[3]
                min15 = data[5]
                min30 = data[7]
                min60 = data[9]
                timedict={}
                timedict["min5"] = self.dataDeal(min5)
                timedict["min15"] = self.dataDeal(min15)
                timedict["min30"] = self.dataDeal(min30)
                timedict["min60"] = self.dataDeal(min60)
                marketdict[market]=timedict
            self.update_date.emit(str(marketdict))  # 发射信号
            time.sleep(1)

    def dataDeal(self,str):
        x=str.split(":")
        open=x[2].split(",")[0]
        close=x[3].split(",")[0]
        high=x[4].split(",")[0]
        vol = x[7].split(",")[0]
        return {"open":open,"close":close,"high":high,"vol":vol}

if __name__ == '__main__':
        app = QApplication(sys.argv)
        myWin = MyWindow()

        update_data_thread = UpdateData()
        update_data_thread.update_date.connect(myWin.update_item_data)  # 链接信号
        update_data_thread.start()


        myWin.show()
        sys.exit(app.exec_())

