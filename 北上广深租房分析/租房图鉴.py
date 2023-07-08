import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient
from pandas.io.json import json_normalize

plt.style.use('ggplot')
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  #解决seaborn中文字体显示问题
plt.rc('figure', figsize=(10, 10))  #把plt默认的图片size调大一点
plt.rcParams["figure.dpi"] =mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

conn = MongoClient(host='127.0.0.1', port=27017)  # 实例化MongoClient
db = conn.get_database('Lianjia')  # 连接到Lianjia数据库

zufang = db.get_collection('zufang') # 连接到集合zufang
mon_data = zufang.find()  # 查询这个集合下的所有记录

data = json_normalize([comment for comment in mon_data])

print(data.head())

print(data.info())

# 每个城市各采样3000条数据，保存为csv文件
data_sample = pd.concat([data[data['city']==city].sample(3000) for city in ['北京', '上海', '广州', '深圳']])
data_sample.to_csv('data_sample.csv', index=False)