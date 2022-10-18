import csv
import time
import requests
from bs4 import BeautifulSoup
import json
import pymysql
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import mplfinance
import mpl_finance
import tkinter as tk
import pandas as pd
import numpy as np


class LoginPage:
    def __init__(self, master: tk.Tk):
        self.root = master
        self.root.geometry('400x240')
        self.page = tk.Frame(root)
        self.page.pack()
        self.root.title('爬取搜狐财经股票数据')
        tk.Label(self.page).grid(row=0, column=0)
        tk.Button(self.page, text='点击爬取数据', command=self.getnum).grid(row=2, column=1, pady=10)
        tk.Button(self.page, text='点击实现数据可视化', command=self.writegup).grid(row=3, column=1, pady=10)


    def getnum(self):
        html = requests.get("https://q.stock.sohu.com/cn/bk_3137.shtml")  # 获取想要的股票号码
        html.raise_for_status
        text = html.text
        # print(text)
        soup = BeautifulSoup(text, 'html.parser')
        tdL1 = soup.find_all('td', attrs={"class": "e1"})
        tdL2 = soup.find_all('td', attrs={"class": "e2"})
        numL = []
        for td1, td2 in zip(tdL1, tdL2):
            try:
                numL.append([td1.text, td2.text])
            except:
                continue
        self.getgupiao(numL)  # 返回所有股票号码

    def getgupiao(self, numL):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='123456',
                                     database='ch21',
                                     charset='gbk',
                                     autocommit=True)
        print("数据库连接成功")
        count = 0
        for num in numL:
            try:
                count = count + 1
                url = 'https://q.stock.sohu.com/hisHq?code=cn_' + num[
                    0] + '&stat=1&order=D&period=d&callback=historySearchHandler&rt=jsonp&0.13888967033291877'
                r = requests.get(url)
                r.raise_for_status()
                r.encoding = "gbk"
                html = r.text[21:-2]  # 去BOM头
                data = json.loads(html)
                datalist = data[0]['hq']
                # print(num[1])
                # print(datalist[0])
                if count == 2:
                    f = open('dataday.csv', 'w', encoding='gbk')
                    csv_write = csv.writer(f)
                    csv_write.writerow(['日期', '开盘', '收盘', '涨跌额', '涨跌幅	', '最低', '最高', '成交量(手)', '成交金额(万)', '换手率'])
                    for data in datalist:
                        csv_write.writerow(data)
                    f.close()
                try:
                    with connection.cursor() as cursor:
                        sql = 'insert into excel (Name, Open, Close, RiseAndUp, RiseAndUpA, High, Low, Volume, Money, TurnoverRate) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                        value = (num[1], datalist[0][1], datalist[0][2], datalist[0][3], datalist[0][4], datalist[0][5],
                                 datalist[0][6], datalist[0][7], datalist[0][8], datalist[0][9])
                        print(value)
                        affectedcount = cursor.execute(sql, value)
                        # sql = 'insert into user (userid, name) values (%s,%s)'
                        print('影响的数据行数：{0}'.format(affectedcount))
                        connection.commit()
                        # print(num[1]+'成功')
                except  pymysql.DatabaseError as error:
                    connection.rollback()
                    print('插入数据失败' + error)

                '''datalist = data[0]['hq']
                with open(num[1]+'.csv', "w", newline='') as csvFile:  # 写入股票信息
                    csvWriter = csv.writer(csvFile)
                    csvWriter.writerow(['日期', '开盘', '收盘', '涨跌额', '涨跌幅	', '最低', '最高', '成交量(手)', '成交金额(万)', '换手率'])
                    for data in datalist:
                        csvWriter.writerow(data)
                        break
                    csvFile.close
                print(num[1], '爬取成功')'''

            except:
                continue

        connection.close()

    def pot_candlestick_ohlc(self, datafile):
        """绘制K线图"""

        # 从CSV文件中读入数据DataFrame数据结构中
        quotes = pd.read_csv(datafile,
                             index_col=0,
                             parse_dates=True,
                             infer_datetime_format=True)

        # 绘制一个子图，并设置子图大小
        fig, ax = plt.subplots(figsize=(10, 5))
        # 调整子图参数SubplotParams
        fig.subplots_adjust(bottom=0.2)

        mpl_finance.candlestick_ohlc(ax, zip(mdates.date2num(quotes.index.to_pydatetime()),
                                             quotes['Open'], quotes['High'],
                                             quotes['Low'], quotes['Close']),
                                     width=1, colorup='r', colordown='g')

        ax.xaxis_date()
        ax.autoscale_view()
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

        plt.show()

    def writegup(self):
        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='123456',
                               database='ch21',
                               charset='gbk',
                               autocommit=True)
        cursor = conn.cursor()
        sql = " select * into outfile '{0}' CHARACTER SET GBK FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' from(select '日期', '开盘', '收盘', '涨跌额', '涨跌幅	', '最低', '最高', '成交量(手)', '成交金额(万)', '换手率' union select * from excel) as b  "
        try:
            cursor.execute(sql.format("D:/Pycharm/ch21.2/test2/data.csv", ))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        conn.close()
        self.draw()

    def draw(self):
        result_set = pd.read_csv("dataday.csv", error_bad_lines=False, encoding='gbk')
        data = []
        col_1 = result_set["日期"]
        data_1 = np.array(col_1)
        col_2 = result_set["开盘"]
        data_2 = np.array(col_2)
        col_3 = result_set["收盘"]
        data_3 = np.array(col_3)
        col_4 = result_set["最低"]
        data_4 = np.array(col_4)
        col_5 = result_set["最高"]
        data_5 = np.array(col_5)
        col_6 = result_set["成交金额(万)"]
        data_6 = np.array(col_6)
        data.append(data_1)
        data.append(data_2)
        data.append(data_3)
        data.append(data_4)
        data.append(data_5)
        data.append(data_6)
        # print(data[4][0])
        colsname = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        # 临时数据文件名
        datafile = 'temp.csv'
        with open(datafile, 'w', newline='', encoding='utf-8') as wf:
            writer = csv.writer(wf)
            writer.writerow(colsname)
            rows = []
            for col in range(0, 80):
                for row in range(0, 6):
                    rows.append(data[row][col])
                    # print(data[row][col])
                    row += 1
                col += 1
                print(rows)
                writer.writerow(rows)
                rows = []
        self.pot_candlestick_ohlc(datafile)

        '''datafile = 'temp.csv'
        # 写如数据到临时数据文件
        with open(datafile, 'w', newline='', encoding='utf-8') as wf:
            writer = csv.writer(wf)
            writer.writerow(colsname)
        '''


if __name__ == '__main__':
    root = tk.Tk()
    LoginPage(master=root)
    root.mainloop()
    # numL = getnum()
    # getgupiao(numL)
    # writegup()
    # draw()
    #print("爬取完成！")

