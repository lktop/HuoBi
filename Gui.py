#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
import pymysql
class PrinterTkinter:
    def __init__(self):
        self.db = pymysql.connect(host='localhost', port=3306, db='huobi', user='root', passwd='root', charset='utf8')
        self.cursor = self.db.cursor()
        self.price={}
        self.marketlist=self.getAllmarket()
        self.marklist=[]
        self.root = Tk()
        self.root.title("HuoBi Monitor")
        self.root.geometry("1450x710")
        self.frame_center = Frame(width=1450, height=300)
        self.frame_bottom = Frame(width=1450, height=300)
        self.frame_buyprice=Frame(width=1450,height=100)

        # 定义中心列表区域
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=("a", "b", "c", "d", "e","f","g","h", "i"))
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        self.buyprice = ttk.Entry(self.frame_buyprice)
        self.Set = ttk.Button(self.frame_buyprice,text="Set",command=self.SetPrice)
        self.Mark = ttk.Button(self.frame_buyprice, text="N/Mark", command=self.lockMark)
        # 创建一个下拉列表
        self.number = StringVar()
        self.numberChosen = ttk.Combobox(self.frame_buyprice, width=12, textvariable=self.number)
        self.numberChosen['values'] = self.marketlist  # 设置下拉列表的值
        self.numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

        self.number1 = StringVar()
        self.numberChosen1 = ttk.Combobox(self.frame_buyprice, width=12, textvariable=self.number1)
        self.numberChosen1['values'] = self.marketlist  # 设置下拉列表的值
        self.numberChosen1.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
        #价格位置
        self.numberChosen1.grid(column=0,row=1)
        self.Mark.grid(column=1,row=1)
        self.numberChosen.grid(column=0, row=0)
        self.buyprice.grid(row=0, column=1 ,sticky=EW)
        self.Set.grid(row=0, column=2,sticky=EW)

        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("a", width=100, anchor="center")
        self.tree.column("b", width=210, anchor="center")
        self.tree.column("c", width=210, anchor="center")
        self.tree.column("d", width=210, anchor="center")
        self.tree.column("e", width=210, anchor="center")
        self.tree.column("f", width=190, anchor="center")
        self.tree.column("g", width=100, anchor="center")
        self.tree.column("h", width=80, anchor="center")
        self.tree.column("i", width=100, anchor="center")
        self.tree.heading("a", text="交易对")
        self.tree.heading("b", text="1hour")
        self.tree.heading("c", text="30min")
        self.tree.heading("d", text="15min")
        self.tree.heading("e", text="5min")
        self.tree.heading("f", text="买入价")
        self.tree.heading("g", text="止损警示")
        self.tree.heading("h", text="锁定")
        self.tree.heading("i", text="三倍")
        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        # 定义底部列表区域
        self.tree2 = ttk.Treeview(self.frame_bottom, show="headings", height=18,columns=("a", "b", "c", "d", "e", "f", "g", "h", "i"))
        self.vbar2 = ttk.Scrollbar(self.frame_bottom, orient=VERTICAL, command=self.tree2.yview)
        # 定义树形结构与滚动条
        self.tree2.configure(yscrollcommand=self.vbar2.set)
        self.tree2.column("a", width=100, anchor="center")
        self.tree2.column("b", width=210, anchor="center")
        self.tree2.column("c", width=210, anchor="center")
        self.tree2.column("d", width=210, anchor="center")
        self.tree2.column("e", width=210, anchor="center")
        self.tree2.column("f", width=190, anchor="center")
        self.tree2.column("g", width=100, anchor="center")
        self.tree2.column("h", width=80, anchor="center")
        self.tree2.column("i", width=100, anchor="center")
        self.tree2.heading("a", text="交易对")
        self.tree2.heading("b", text="1hour")
        self.tree2.heading("c", text="30min")
        self.tree2.heading("d", text="15min")
        self.tree2.heading("e", text="5min")
        self.tree2.heading("f", text="买入价")
        self.tree2.heading("g", text="止损警示")
        self.tree2.heading("h", text="锁定")
        self.tree2.heading("i", text="三倍")

        # 调用方法获取表格内容插入
        self.get_tree()
        self.tree2.grid(row=0, column=0, sticky=NSEW)
        self.vbar2.grid(row=0, column=1, sticky=NS)

        # 整体区域定位

        self.frame_center.grid(row=1, column=0, padx=4, pady=5)
        self.frame_bottom.grid(row=2, column=0, padx=4, pady=5)
        self.frame_buyprice.grid(row=3, column=0, padx=4, pady=5)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)
        self.frame_buyprice.grid_propagate(0)
        self.root.mainloop()

    # 表格内容插入
    def get_tree(self):
        self.cursor.execute("SELECT * FROM huobi")
        for item in self.tree2.get_children():
                self.tree2.delete(item)
        for item in self.tree.get_children():
                self.tree.delete(item)
        for i in self.cursor.fetchall():
            i=str(i).split(",")
            # print(i)
            market=i[0].split("'")[1]
            min5=str(i[2].split(":")[1])+","+str(i[3].split(":")[1])+","+str(i[7].split(":")[1])
            min15=str(i[10].split(":")[1])+","+str(i[11].split(":")[1])+","+str(i[15].split(":")[1])
            hfhour=str(i[18].split(":")[1])+","+str(i[19].split(":")[1])+","+str(i[23].split(":")[1])
            hour =str(i[26].split(":")[1])+","+str(i[27].split(":")[1])+","+str(i[31].split(":")[1])
            listred = [market, hour, hfhour, min15, min5,'','','','']
            min5vol=float(i[7].split(":")[1])
            min15vol=float(i[15].split(":")[1])
            hfhourvol=float(i[23].split(":")[1])
            hourvol=float(i[31].split(":")[1])
            min5close=float(i[3].split(":")[1])
            sanbei=''
            if (min15vol-3*min5vol)>=0:
                sanbei="15min > 5min"
            if (hfhourvol-3*min15vol)>=0:
                sanbei="30min > 15min"
            if (hourvol-3*hfhourvol)>=0:
                sanbei="60min > 30min"
            if sanbei!='':
                listred[8]=sanbei
            if market in self.marklist:
                listred[7]=1
                #价格预警判断
                if self.Prices(market):
                    listred[5]=self.price[market]
                    if float(self.price[market])>=(0.9*min5close):
                        #预警
                        listred[6] = "1"
                        self.tree.insert("", "end", value=listred,tags=("yujing",))
                        self.tree.tag_configure("yujing", background="#e60606")
                        self.tree2.insert("", "end", value=listred,tags=("yujing",))
                        self.tree2.tag_configure("yujing", background="#e60606")
                    else:
                        #不预警
                        self.tree.insert("", "end", value=listred)
                        self.tree2.insert("", "end", value=listred)
                else:
                    self.tree.insert("", "end", value=listred)
                    self.tree2.insert("", "end", value=listred)
            else:
                #价格预警判断
                if self.Prices(market):
                    listred[5]=self.price[market]
                    if float(self.price[market])>=(0.9*min5close):
                        #预警
                        listred[6]="1"
                        if listred[8]=='':
                            self.tree2.insert("", "end", value=listred,tags=("yujing",))
                            self.tree2.tag_configure("yujing", background="#e60606")
                        else:
                            self.tree.insert("", "end", value=listred, tags=("yujing",))
                            self.tree.tag_configure("yujing", background="#e60606")
                            self.tree2.insert("", "end", value=listred, tags=("yujing",))
                            self.tree2.tag_configure("yujing", background="#e60606")
                    else:
                        #不预警
                        if listred[8] == '':
                            self.tree2.insert("", "end", value=listred)
                        else:
                            self.tree.insert("", "end", value=listred)
                            self.tree2.insert("", "end", value=listred)
                else:
                    if listred[8] == '':
                        self.tree2.insert("", "end", value=listred)
                    else:
                        self.tree.insert("", "end", value=listred)
                        self.tree2.insert("", "end", value=listred)

        self.tree.after(100, self.get_tree)

    def getAllmarket(self):
        self.cursor.execute("SELECT * FROM huobi")
        marketlist=[]
        for i in self.cursor.fetchall():
            i=str(i).split(",")
            # print(i)
            market=i[0].split("'")[1]
            marketlist.append(market)
        return marketlist

    def lockMark(self):
        mark=self.numberChosen1.get()
        print(mark)
        if mark in self.marklist:
            self.marklist.remove(mark)
        else:
            self.marklist.append(mark)

    def SetPrice(self):
        market=self.numberChosen.get()
        self.price[market]=self.buyprice.get()
        print(self.price)

    def Prices(self,market):
        keylist=self.price.keys()
        if market in keylist:
            if self.price[market]!="":
                return 1
            return 0
        else:
            return 0


if __name__ == '__main__':
    PrinterTkinter()
