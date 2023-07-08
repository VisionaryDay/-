import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient
from pandas.io.json import json_normalize
import random

data = pd.read_csv('data_clean.csv')

"""
问题：

各城市的租房分布怎么样？
城市各区域的房价分布怎么样？
距离地铁口远近有什么关系？
房屋大小对价格的影响如何？
租个人房源好还是公寓好？
精装和简装对房子价格的影响
北方集中供暖对价格的影响
北上广深租房时都看重什么？
"""

#各城市的租房分布怎么样
def get_city_zf_loc(city, city_short, col=['longitude', 'latitude', 'dist'], data=data):
    file_name = 'data_' + city_short + '_latlon.csv'
    data_latlon = data.loc[data['city']==city, col].dropna(subset=['latitude', 'longitude'])
    data_latlon['longitude'] = data_latlon['longitude'].astype(str)
    data_latlon['latitude'] = data_latlon['latitude'].astype(str)
    data_latlon['latlon'] = data_latlon['longitude'].str.cat(data_latlon['latitude'], sep=',')
    data_latlon.to_csv(file_name, index=False)
    print(city+'的数据一共有{}条'.format(data_latlon.shape[0]))

get_city_zf_loc('北京', 'bj', ['longitude','latitude', 'dist'])
get_city_zf_loc('上海', 'sh', ['longitude','latitude', 'dist'])
get_city_zf_loc('广州', 'gz', ['longitude','latitude', 'dist'])
get_city_zf_loc('深圳', 'sz', ['longitude','latitude', 'dist'])

#颜色列表
colors = ['r', 'coral', 'y', 'olive','c','steelblue','cornflowerblue','hotpink']
#北京市租房分布
fig = plt.figure(dpi=300)
plt.rcParams['font.sans-serif'] = 'SimSun'
data_beijing = data.dropna(subset=['latitude', 'longitude']).loc[data['city'] == '北京', 'dist']
data_beijing_counts = data_beijing.value_counts(ascending=True)
data_beijing_counts.plot.barh(color=[random.choice(colors) for _ in range(len(data_beijing_counts))])
plt.title('北京市租房分布', fontdict={'fontsize': 14, 'fontweight': 'bold'})
plt.xlabel("数量", fontdict={'fontsize': 12})
plt.ylabel("区域", fontdict={'fontsize': 12})
plt.grid(True)
plt.savefig('数据结果分析图/各城市的租房分布怎么样/北京市租房分布图.png')
# plt.show()


# 上海市租房分布图
fig = plt.figure(dpi=300)
plt.rcParams['font.sans-serif'] = 'SimSun'
data_shanghai = data.dropna(subset=['latitude', 'longitude']).loc[data['city'] == '上海', 'dist']
data_shanghai_counts = data_shanghai.value_counts(ascending=True)
data_shanghai_counts.plot.barh(color=[random.choice(colors) for _ in range(len(data_shanghai_counts))])
plt.title('上海市租房分布', fontdict={'fontsize': 14, 'fontweight': 'bold'})
plt.xlabel("数量", fontdict={'fontsize': 12})
plt.ylabel("区域", fontdict={'fontsize': 12})
plt.grid(True)
plt.savefig('数据结果分析图/各城市的租房分布怎么样/上海市租房分布图.png')
# plt.show()

# 广州市租房分布图
fig = plt.figure(dpi=300)
plt.rcParams['font.sans-serif'] = 'SimSun'
data_guangzhou = data.dropna(subset=['latitude', 'longitude']).loc[data['city'] == '广州', 'dist']
data_guangzhou_counts = data_guangzhou.value_counts(ascending=True)
data_guangzhou_counts.plot.barh(color=[random.choice(colors) for _ in range(len(data_guangzhou_counts))])
plt.title('广州市租房分布', fontdict={'fontsize': 14, 'fontweight': 'bold'})
plt.xlabel("数量", fontdict={'fontsize': 12})
plt.ylabel("区域", fontdict={'fontsize': 12})
plt.grid(True)
plt.savefig('数据结果分析图/各城市的租房分布怎么样/广州市租房分布图.png')
# plt.show()

#深圳
# 深圳市租房分布图
fig = plt.figure(dpi=300)
plt.rcParams['font.sans-serif'] = 'SimSun'
data_shenzhen = data.dropna(subset=['latitude', 'longitude']).loc[data['city'] == '深圳', 'dist']
data_shenzhen_counts = data_shenzhen.value_counts(ascending=True)
data_shenzhen_counts.plot.barh(color=[random.choice(colors) for _ in range(len(data_shenzhen_counts))])
plt.title('深圳市租房分布', fontdict={'fontsize': 14, 'fontweight': 'bold'})
plt.xlabel("数量", fontdict={'fontsize': 12})
plt.ylabel("区域", fontdict={'fontsize': 12})
plt.grid(True)
plt.savefig('数据结果分析图/各城市的租房分布怎么样/深圳市租房分布图.png')
# plt.show()

# 2.城市各区域的房价分布怎么样？
plt.figure(dpi=300)
data['aver_price'] = np.round(data['rent_price_listing'] / data['rent_area'], 1)
g = sns.FacetGrid(data, row="city", height=4, aspect=2)
g = g.map(sns.kdeplot, "aver_price")
plt.savefig('数据结果分析图/城市各区域的房价分布怎么样/平均价格分布图.png')
# plt.show()

# 由于平均租金基本上都集中在250元/平米/月以内，所以选取这部分数据绘制热力图
def get_city_zf_aver_price(city, city_short, col=['longitude', 'latitude', 'aver_price'], data=data):
    file_name = 'data_' + city_short + '_aver_price.csv'
    data_latlon = data.loc[(data['city']==city)&(data['aver_price']<=250), col].dropna(subset=['latitude', 'longitude'])
    data_latlon['longitude'] = data_latlon['longitude'].astype(str)
    data_latlon['latitude'] = data_latlon['latitude'].astype(str)
    data_latlon['latlon'] = data_latlon['longitude'].str.cat(data_latlon['latitude'], sep=',')
    data_latlon.to_csv(file_name, index=False)
    print(city+'的数据一共有{}条'.format(data_latlon.shape[0]))

get_city_zf_aver_price('北京', 'bj')
get_city_zf_aver_price('上海', 'sh')
get_city_zf_aver_price('广州', 'gz')
get_city_zf_aver_price('深圳', 'sz')

# 各城市租金Top10的商圈
bc_top10 = data.groupby(['city', 'bizcircle_name'])['aver_price'].mean().nlargest(50).reset_index()['city'].value_counts()
print(bc_top10)

from pyecharts import Bar
# from pyecharts.charts import Bar

bar = Bar("每平米平均租金前50的北上广深商圈数量", width=400)
bar.add("", bc_top10.index, bc_top10.values, is_stack=True,
       xaxis_label_textsize=16, yaxis_label_textsize=16, is_label_show=True)
bar.render("数据结果分析图/城市各区域的房价分布怎么样/每平米平均租金前50的北上广深商圈数量.html")

def get_top10_bc(city, data=data):
    top10_bc = data[(data['city']==city)&(data['bizcircle_name']!='')].groupby('bizcircle_name')['aver_price'].mean().nlargest(10)
    bar = Bar(city+"市每平米平均租金Top10的商圈", width=600)
    bar.add("", top10_bc.index, np.round(top10_bc.values, 0), is_stack=True,
       xaxis_label_textsize=16, yaxis_label_textsize=16, xaxis_rotate=30, is_label_show=True)
    return bar

# 北京每平米平均租金Top10的商圈
bar = get_top10_bc('北京')
bar.render("数据结果分析图/城市各区域的房价分布怎么样/北京每平米平均租金Top10的商圈.html")

# 上海每平米平均租金Top10的商圈
bar = get_top10_bc('上海')
bar.render("数据结果分析图/城市各区域的房价分布怎么样/上海每平米平均租金Top10的商圈.html")

# 广州每平米平均租金Top10的商圈
bar = get_top10_bc('广州')
bar.render("数据结果分析图/城市各区域的房价分布怎么样/广州每平米平均租金Top10的商圈.html")

# 深圳每平米平均租金Top10的商圈
bar = get_top10_bc('深圳')
bar.render("数据结果分析图/城市各区域的房价分布怎么样/深圳每平米平均租金Top10的商圈.html")

# 3.距离地铁口远近有什么关系？
from scipy.stats import pearsonr

def distance_price_relation(city, data=data):
    data_city = data[(data['city'] == city) & (data['aver_price'] <= 350)].dropna(subset=['distance'])
    plt.figure(figsize=(8, 6))
    sns.regplot(x='distance', y='aver_price', data=data_city, scatter_kws={'s': 10}, line_kws={'color': 'red'})
    plt.xlabel('最近地铁距离')
    plt.ylabel('每平米租金')
    r, _ = pearsonr(data_city['distance'], data_city['aver_price'])
    plt.title(f'{city}地铁距离与每平米租金相关性 (Pearson相关系数: {r:.2f})', fontsize=14, fontweight='bold')
    plt.grid(True)
    plt.savefig('数据结果分析图/距离地铁口远近有什么关系/{}.png'.format(city))
    plt.show()

bins = [100*i for i in range(13)]
data['bin'] = pd.cut(data.dropna(subset=['distance'])['distance'], bins)
bin_bj = data[data['city']=='北京'].groupby('bin')['aver_price'].mean()
bin_sh = data[data['city']=='上海'].groupby('bin')['aver_price'].mean()
bin_gz = data[data['city']=='广州'].groupby('bin')['aver_price'].mean()
bin_sz = data[data['city']=='深圳'].groupby('bin')['aver_price'].mean()

from pyecharts import Line

line = Line("距离地铁远近跟每平米租金均价的关系")
for city, bin_data in {'北京':bin_bj, '上海':bin_sh, '广州':bin_gz, '深圳':bin_sz}.items():
    line.add(city, bin_data.index, bin_data.values,
            legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
             xaxis_rotate=20, yaxis_min=8, legend_top=30)
print(line)
line.render("数据结果分析图/距离地铁口远近有什么关系/距离地铁远近与租金均价关系.html")

# 4. 房屋大小对每平米租金的影响如何？
def area_price_relation(city, data=data):
    fig = plt.figure(dpi=100)
    g = sns.lineplot(x="rent_area",
                     y="aver_price",
                     data=data[(data['city']==city)&(data['rent_area']<150)],
                     ci=None)
    g.set_xlabel('面积', fontweight='bold')
    g.set_ylabel('每平米均价', fontweight='bold')
    plt.title(f'{city}房屋面积与每平米租金的关系', fontweight='bold')
    plt.grid(True)
    plt.savefig(f'数据结果分析图/房屋大小对每平米租金的影响/{city}房屋面积与租金关系图.png')
    plt.show()
    # plt.close()
#北京
area_price_relation('北京')
#上海
area_price_relation('上海')
#广州
area_price_relation('广州')
#深圳
area_price_relation('深圳')

# 根据house_title和house_tag再造一个字段：is_dep，也就是“是否是公寓”
data['is_dep'] = (data['house_title'].str.contains('公寓') + data['house_tag'].str.contains('公寓')) > 0

# 每个城市房源的公寓占比
for city in ['北京', '上海', '广州', '深圳']:
    print(city+'的公寓占总房源量比重为:{}%。'.format(
        np.round(data[data['city']==city]['is_dep'].mean()*100, 2)))

print(data[(data['city']=='广州')&
    (data['rent_area']>0)&
    (data['rent_area']<60)&
    (data['aver_price']>100)]['is_dep'].mean())

# 5. 租个人房源好还是公寓好？
is_dep = data[(data['city'].isin(['广州','深圳']))&
             (data['is_dep']==1)].groupby('city')['aver_price'].mean()
not_dep = data[(data['city'].isin(['广州','深圳']))&
             (data['is_dep']==0)].groupby('city')['aver_price'].mean()

bar = Bar("个人房源和公寓的每平米租金差别", width=600)
bar.add("个人房源", not_dep.index, np.round(not_dep.values, 0),
        legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)
bar.add("公寓", is_dep.index, np.round(is_dep.values, 0),
       legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)
bar.render('数据结果分析图/租个人房源好还是公寓好/个人房源和公寓的每平米租金差别.html')

# 6. 精装和简装对房子价格的影响
data['decorated'] = data[data['house_tag'].notna()]['house_tag'].str.contains('精装')
decorated = data[data['decorated']==1].groupby('city')['aver_price'].mean()
not_decorated = data[data['decorated']==0].groupby('city')['aver_price'].mean()
bar = Bar("各城市精装和简装的每平米租金差别", width=600)
bar.add("精装(刷过墙)", decorated.index, np.round(decorated.values, 0),
        legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)
bar.add("简装(破房子)", not_decorated.index, np.round(not_decorated.values, 0),
       legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)
bar.render('数据结果分析图/精装和简装对房子价格的影响/各城市精装和简装的每平米租金差别.html')


is_dec_dep = data[(data['decorated']==1)&
                  (data['is_dep']==1)&
                 (data['city'].isin(['北京','上海','广州', '深圳']))].groupby('city')['aver_price'].mean()
is_dec_not_dep = data[(data['decorated']==1)&
                      (data['is_dep']==0)&
                     (data['city'].isin(['北京','上海','广州', '深圳']))].groupby('city')['aver_price'].mean()
not_dec_dep = data[(data['decorated']==0)&
                   (data['is_dep']==0)&
                  (data['city'].isin(['北京','上海','广州', '深圳']))].groupby('city')['aver_price'].mean()
bar = Bar("各城市装修和房源类型的每平米租金差别", width=600)
bar.add("精装公寓", is_dec_dep.index, np.round(is_dec_dep.values, 0),
        legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)
bar.add("精装个人房源", is_dec_not_dep.index, np.round(is_dec_not_dep.values, 0),
       legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)
bar.add("简装个人房源", not_dec_dep.index, np.round(not_dec_dep.values, 0),
       legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)
bar.render('数据结果分析图/精装和简装对房子价格的影响/各城市装修和房源类型的每平米租金差别.html')

# 7. 北方集中供暖对价格的影响
data['ct_heating'] = data['house_tag'].str.contains('集中供暖')
print(data[data['city']=='北京'].groupby('ct_heating')['aver_price'].mean())
data[data['city']=='北京'].groupby('ct_heating')['aver_price'].mean().to_csv('数据结果分析图/北方集中供暖对价格的影响/北京集中供暖')

# 读取CSV文件
df = pd.read_csv('数据结果分析图/北方集中供暖对价格的影响/北京集中供暖')

# 创建柱状图对象
bar = Bar("北京集中供暖对价格的影响",width=450)

# 添加数据
bar.add("", df['ct_heating'], df['aver_price'],xaxis_name="是否集中供暖",yaxis_name="每平米租金均价",
        legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True
        )

# 生成图表
bar.render("数据结果分析图/北方集中供暖对价格的影响/北京集中供暖图表.html")

# 8. 各城市房屋租售比
zs_ratio = [57036, 62779, 32039, 56758]/(data.groupby('city')['rent_price_listing'].sum()/data.groupby('city')['rent_area'].sum())/12
bar =Bar("各城市房屋租售比(租多少年可以在该城市买下一套房)", width=450)
bar.add("", zs_ratio.index, np.round(zs_ratio.values, 0),
        legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)
bar.render('数据结果分析图/各城市房屋租售比/各城市房屋租售比(租多少年可以在该城市买下一套房).html')


# 9. 北上广深租房时都看重什么？
def layout_top3(city, data):
    layout_data = data[data['city']==city]['layout'].value_counts().nlargest(3)
    bar = Bar(city+"最受欢迎的户型", width=600)
    bar.add("", layout_data.index, layout_data.values,
        legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)
    return bar
# 北京
layout_top3('北京', data).render('数据结果分析图/北上广深租房时都看重什么？/北京偏爱户型.html')
# 上海
layout_top3('上海', data).render('数据结果分析图/北上广深租房时都看重什么？/上海偏爱户型.html')
# 广州
layout_top3('广州', data).render('数据结果分析图/北上广深租房时都看重什么？/广州偏爱户型.html')
#深圳
layout_top3('深圳', data).render('数据结果分析图/北上广深租房时都看重什么？/深圳偏爱户型.html')

from wordcloud import WordCloud
from collections import Counter
# # 获取系统默认字体路径
# font_path = fm.findfont(fm.FontProperties(family='Arial'))
# 北京词云图
bj_tag = []
for st in data[data['city'] == '北京'].dropna(subset=['house_tag'])['house_tag']:
    bj_tag.extend(st.split(' '))

counter = Counter(bj_tag)

wordcloud = WordCloud(width=800, height=400, font_path='C:/Windows/Fonts/simhei.ttf',background_color='white')
#background_color='white'
#'C:/Windows/Fonts/ARIALN.TTF'
wordcloud.generate_from_frequencies(counter)

plt.imshow(wordcloud, interpolation='bilinear')
plt.title("北京市词云图")
plt.axis('off')
plt.savefig('数据结果分析图/北上广深租房时都看重什么？/北京词云图.png')
plt.show()

#上海词云图
# 获取词频统计结果
sh_tag = []
for st in data[data['city'] == '上海'].dropna(subset=['house_tag'])['house_tag']:
    sh_tag.extend(st.split(' '))
counter = Counter(sh_tag)

# 生成词云
wordcloud = WordCloud(font_path='simhei.ttf', width=800, height=400,background_color='white')
wordcloud.generate_from_frequencies(counter)

# 显示词云图像
plt.imshow(wordcloud, interpolation='bilinear')
plt.title("上海市词云图")
plt.axis('off')
plt.savefig('数据结果分析图/北上广深租房时都看重什么？/上海词云图.png')
plt.show()

# 广州词云图
gz_tag = []
for st in data[data['city'] == '广州'].dropna(subset=['house_tag'])['house_tag']:
    gz_tag.extend(st.split(' '))
counter = Counter(gz_tag)

# 生成词云
wordcloud = WordCloud(font_path='simhei.ttf', width=800, height=400,background_color='white')
wordcloud.generate_from_frequencies(counter)

# 显示词云图像
plt.imshow(wordcloud, interpolation='bilinear')
plt.title("广州市词云图")
plt.axis('off')
plt.savefig('数据结果分析图/北上广深租房时都看重什么？/广州词云图.png')
plt.show()

#深圳词云图
# 获取词频统计结果
sz_tag = []
for st in data[data['city'] == '深圳'].dropna(subset=['house_tag'])['house_tag']:
    sz_tag.extend(st.split(' '))
counter = Counter(sz_tag)

# 生成词云
wordcloud = WordCloud(font_path='simhei.ttf', width=800, height=400,background_color='white')
wordcloud.generate_from_frequencies(counter)

# 显示词云图像
plt.imshow(wordcloud, interpolation='bilinear')
plt.title("深圳市词云图")
plt.axis('off')
plt.savefig('数据结果分析图/北上广深租房时都看重什么？/深圳词云图.png')
plt.show()