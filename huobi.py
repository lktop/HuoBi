# -*- coding: utf-8 -*-
from websocket import create_connection
import gzip
import time
import json
import pymysql
if __name__ == '__main__':
    db = pymysql.connect(host='localhost', port=3306, db='huobi', user='root', passwd='root', charset='utf8')
    cursor = db.cursor()
    while(1):
        try:
            # ws=websocket.WebSocket()
            # ws.connect("wss://api.huobi.br.com/ws")
            ws = create_connection("wss://api.huobi.br.com/ws")
            break
        except Exception as e:
            print(e)
            print('connect ws error,retry...')
            time.sleep(5)
    print("设置初始化完成!")
    print("当前监视市场:")
    Coinlist = []
    f = open("CoinSets.txt")  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        line = f.readline()
        if line.split("\n")[0] != "":
            Coinlist.append(line.split("\n")[0])
    f.close()
    print(Coinlist)
    cursor.execute("truncate table huobi")

    CoinDic={}
    for i in Coinlist:
        CoinDic[i]={"1min":{},"5min":{},"15min":{},"30min":{},"60min":{},"4hour":{},"1day":{},"1mon":{},"1week":{},"1year":{}}
        cursor.execute("INSERT INTO `huobi`.`huobi` (`market`, `5min`, `15min`, `30min`, `60min`) VALUES ('{}', NULL, NULL, NULL, NULL);".format(i))
    # 订阅 KLine 数据
    # trade1mStr='{"sub": "market.%s.kline.1min","id": "id10"}'
    trade5mStr = '{"sub": "market.%s.kline.5min","id": "id10"}'
    trade15mStr = '{"sub": "market.%s.kline.15min","id": "id10"}'
    trade30mStr = '{"sub": "market.%s.kline.30min","id": "id10"}'
    trade60mStr = '{"sub": "market.%s.kline.60min","id": "id10"}'
    # trade4hStr = '{"sub": "market.%s.kline.4hour","id": "id10"}'
    # trade1dStr = '{"sub": "market.%s.kline.1day","id": "id10"}'
    # trade1monStr = '{"sub": "market.%s.kline.1mon","id": "id10"}'
    # trade1wekStr = '{"sub": "market.%s.kline.1week","id": "id10"}'
    # trade1yearStr = '{"sub": "market.%s.kline.1year","id": "id10"}'

    for i in Coinlist:
        # ws.send(trade1mStr%i)
        # time.sleep(1)
        ws.send(trade5mStr%i)
        # time.sleep(0.2)
        ws.send(trade15mStr%i)
        # time.sleep(0.2)
        ws.send(trade30mStr%i)
        # time.sleep(0.2)
        ws.send(trade60mStr%i)
        # time.sleep(0.2)
        # ws.send(trade4hStr%i)
        # time.sleep(1)
        # ws.send(trade1dStr%i)
        # time.sleep(1)
        # ws.send(trade1monStr%i)
        # time.sleep(1)
        # ws.send(trade1wekStr%i)
        # time.sleep(1)
        # ws.send(trade1yearStr%i)
        # time.sleep(1)
    trade_id = ''
    while True:
        try:
            while(1):
                compressData=ws.recv()
                result=gzip.decompress(compressData).decode('utf-8')
                if result[:7] == '{"ping"':
                    ts=result[8:21]
                    pong='{"pong":'+ts+'}'
                    ws.send(pong)
                    # ws.send(tradeStr)
                else:
                    try:
                        if trade_id == result['data']['id']:
                            print('重复的id')
                            break
                        else:
                            trade_id = result['data']['id']
                    except Exception:
                        pass
                    # print(result)

                    try:
                        result=json.loads(result)
                        markte=result["ch"].split(".")[1]
                        period=result["ch"].split(".")[3]
                        ts=result["ts"]
                        open=result["tick"]["open"]
                        close = result["tick"]["close"]
                        low = result["tick"]["low"]
                        high = result["tick"]["high"]
                        amount = result["tick"]["amount"]
                        vol = result["tick"]["vol"]
                        count = result["tick"]["count"]
                        CoinDic[markte][period]="{ts:%s,open:%s,close:%s,low:%s,high:%s,amount:%s,vol:%s,count:%s}"%(ts,open,close,low,high,amount,vol,count)
                        print(CoinDic)
                        sql='''UPDATE `huobi`.`huobi` SET `'''+period+'''`="'''+CoinDic[markte][period]+'''" WHERE (`market`="'''+markte+'''");'''
                        # print(sql)
                        cursor.execute(sql)
                    except Exception as e :
                        print(e)
                        pass
        except Exception as e:
            print(e)
            try:
                while (1):
                    try:
                        # ws=websocket.WebSocket()
                        # ws.connect("wss://api.huobi.br.com/ws")
                        ws = create_connection("wss://api.huobi.br.com/ws")
                        break
                    except Exception as e:
                        print(e)
                        print('connect ws error,retry...')
                        time.sleep(5)
                for i in Coinlist:
                    # ws.send(trade1mStr%i)
                    # time.sleep(1)
                    ws.send(trade5mStr % i)
                    time.sleep(1)
                    ws.send(trade15mStr % i)
                    time.sleep(1)
                    ws.send(trade30mStr % i)
                    time.sleep(1)
                    ws.send(trade60mStr % i)
                    time.sleep(1)
                    # ws.send(trade4hStr%i)
                    # time.sleep(1)
                    # ws.send(trade1dStr%i)
                    # time.sleep(1)
                    # ws.send(trade1monStr%i)
                    # time.sleep(1)
                    # ws.send(trade1wekStr%i)
                    # time.sleep(1)
                    # ws.send(trade1yearStr%i)
                    # time.sleep(1)
            except:
                pass
                time.sleep(3)
            pass
