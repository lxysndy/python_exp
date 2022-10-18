import requests     # 发送网络请求
import csv
file = open('data2.csv', mode='a', encoding='utf-8', newline='')
csv_write = csv.DictWriter(file, fieldnames=['股票代码','股票名称','当前价','涨跌额','涨跌幅','年初至今','成交量','成交额','换手率','市盈率(TTM)','股息率','市值'])
csv_write.writeheader()
# 1.确定url地址(链接地址)
for page in range(1, 56):
    url = f'https://xueqiu.com/service/v5/stock/screener/quote/list?page={page}&size=30&order=desc&order_by=amount&exchange=CN&market=CN&type=sha&_=1637908787379'
    # 2.发送网络请求
    # 伪装
    headers = {
        # 浏览器伪装
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    json_data = response.json()
    # print(json_data)
    # 3.数据解析(筛选数据)
    data_list = json_data['data']['list']
    for data in data_list:
        data1 = data['symbol']
        data2 = data['name']
        data3 = data['current']
        data4 = data['chg']
        data5 = data['percent']
        data6 = data['current_year_percent']
        data7 = data['volume']
        data8 = data['amount']
        data9 = data['turnover_rate']
        data10 = data['pe_ttm']
        data11 = data['dividend_yield']
        data12 = data['market_capital']
        print(data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12)
        data_dict = {
            '股票代码': data1,
            '股票名称': data2,
            '当前价': data3,
            '涨跌额': data4,
            '涨跌幅': data5,
            '年初至今': data6,
            '成交量': data7,
            '成交额': data8,
            '换手率': data9,
            '市盈率(TTM)': data10,
            '股息率': data11,
            '市值': data12,
        }
        csv_write.writerow(data_dict)
file.close()
"""
数据分析: anaconda >>> jupyter notebook  文件格式 .ipynb
"""
import pandas as pd     # 做表格处理

data_df = pd.read_csv('data2.csv')
print(data_df)

