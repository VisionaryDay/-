import pandas as pd
import numpy as np


data = pd.read_csv('data_sample.csv')
print(data)

print(data.head())

print(data.info())

# 数据清洗（案列清理）
# 1.去掉“id_"列
data = data.drop(columns='_id')
print(data)
# 2.bathroom_num
# # 完整显示pandas
# pd.set_option('display.max_columns',None)
# pd.set_option('display.max_rows',None)
# pd.set_option('display.expand_frame_repr',False)
print(data['bathroom_num'].unique())
df = data[data['bathroom_num'].isin([8,9])]
df.to_csv('filter.csv')
# 数据没有问题，4，5是合租

# 3. bedroom_num
print(data['bedroom_num'].unique())
# 没有异常数据，只是很多10室以上都是专门用来合租的
df = data[data['bedroom_num'].isin([10,13,20])]
#
# 4. distance
print(data['frame_orientation'].unique())  # 这个数据太乱了，要用的时候再处理吧

# 5. hall_num
print(data['hall_num'].unique())
df = data[data['hall_num'].isin([0,1,2,3,4,5])]
df.to_csv('filter.csv')

# 59223行是异常数据，删去
# data = data.drop([59223])

# 6. rent_area
print(data.sample(5)['rent_area'])

# rent_area字段有些填写的是一个范围，比如23-25平房米，后期转换成“float”类型的时候不好转换，考虑取平均值
def get_aver(data):
    if isinstance(data, str) and '-' in data:
        low, high = data.split('-')
        return (int(low)+int(high))/2
    else:
        return int(data)

data['rent_area'] = data['rent_area'].apply(get_aver)

print(data[data['rent_area'] < 5])
# 房间只有1平米，是异常数据，删去
data = data.drop(data[data['rent_area'] < 5].index)

# 7. rent_price_unit
data['rent_price_unit'].unique()
# 租金都是以“元/月”计算的，所以这一列没用了，可以删了
data = data.drop(columns='rent_price_unit')

# 8. rent_price_listing
data[data['rent_price_listing'].str.contains('-')].sample(3)
# 价格是有区间的，需要按照处理rent_area一样的方法处理
data['rent_price_listing'] = data['rent_price_listing'].apply(get_aver)
# 数据类型转换
for col in ['bathroom_num', 'bedroom_num', 'hall_num', 'rent_price_listing']:
    data[col] = data[col].astype(int)# 数据类型转换


# 'distance', 'latitude', 'longitude'因为有None，需另外处理
def dw_None_dis(data):
    if data is None:
        return np.nan
    else:
        return int(data)


def dw_None_latlon(data):
    if data is None or data == '':
        return np.nan
    else:
        return float(data)


# data['distance'] = data['distance'].apply(dw_None_dis)
# data['latitude'] = data['latitude'].apply(dw_None_latlon)
# data['longitude'] = data['longitude'].apply(dw_None_latlon)

# 查看数据概况
df = data.sample(5)
df.to_csv('filter.csv')
print(data.info())

# 干净的数据
data.to_csv('data_clean.csv', index=False)