import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller as ADF
import os

# 确保 over_figure 文件夹存在
if not os.path.exists('src/opencv_test/over_figure'):
    os.makedirs('src/opencv_test/over_figure')

try:
    # 使用 pd.read_excel 读取 Excel 文件
    ChinaBank = pd.read_excel('src/opencv_test/data/103.xlsx', index_col='时间')
    print("文件读取成功，显示前几行数据：")
    print(ChinaBank.head())

    # 筛选指定t范围内的数据
    # 确保 '0' 和 '860' 是有效的数字索引
    sub = ChinaBank.loc[0:860, '103的速度']
    print("筛选后的数据：")
    print(sub.head())
except Exception as e:
    print("执行过程中遇到错误：", e)

train = sub.loc[0:820]
test = sub.loc[820:860]
    #查看训练集的时间序列与数据(只包含训练集)
plt.figure(figsize=(10,4))
plt.plot(train, color='deepskyblue')  # 使用深天蓝色
plt.savefig('src/opencv_test/over_figure/training_data.png')  # 保存图片
plt.close()

#.diff(1)做一个时间间隔
ChinaBank['diff_1'] = ChinaBank['103的速度'].diff(1) #1阶差分

#对一阶差分数据在划分时间间隔
ChinaBank['diff_2'] = ChinaBank['diff_1'].diff(1) #2阶差分

fig = plt.figure(figsize=(12,10))
#原数据
ax1 = fig.add_subplot(311)
ax1.plot(ChinaBank['103的速度'], color='lightpink')  # 使用浅粉色
#1阶差分
ax2 = fig.add_subplot(312)
ax2.plot(ChinaBank['diff_1'], color='deepskyblue')
#2阶差分
ax3 = fig.add_subplot(313)
ax3.plot(ChinaBank['diff_2'], color='lightcoral')
plt.savefig('src/opencv_test/over_figure/diff_data.png')  # 保存图片
plt.close()


# 计算原始序列、一阶差分序列、二阶差分序列的单位根检验结果
ChinaBank['diff_1'] = ChinaBank['diff_1'].fillna(0)
ChinaBank['diff_2'] = ChinaBank['diff_2'].fillna(0)

timeseries_adf = ADF(ChinaBank['103的速度'].tolist())
timeseries_diff1_adf = ADF(ChinaBank['diff_1'].tolist())
timeseries_diff2_adf = ADF(ChinaBank['diff_2'].tolist())


# 打印单位根检验结果
print('timeseries_adf : ', timeseries_adf)
print('timeseries_diff1_adf : ', timeseries_diff1_adf)
print('timeseries_diff2_adf : ', timeseries_diff2_adf)


#绘制
fig = plt.figure(figsize=(12,7))
ax1.set_title('')
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(train, lags=20,ax=ax1)
# ax1.xaxis.set_ticks_position('bottom') # 设置坐标轴上的数字显示的位置，top:显示在顶部  bottom:显示在底部
#fig.tight_layout()

ax2 = fig.add_subplot(212)
ax2.set_title('')
fig = sm.graphics.tsa.plot_pacf(train, lags=20, ax=ax2)
# ax2.xaxis.set_ticks_position('bottom')
plt.savefig('src/opencv_test/over_figure/acf_pacf.png')  # 保存图片
plt.close()

#遍历，寻找适宜的参数
import pandas as pd
import itertools
import numpy as np
import seaborn as sns
#确定pq的取值范围
p_min = 0
d_min = 0
q_min = 0
p_max = 5
d_max = 0
q_max = 5

#Initialize a DataFrame to store the results,，以BIC准则
results_bic = pd.DataFrame(index=['AR{}'.format(i) for i in range(p_min,p_max+1)],
                           columns=['MA{}'.format(i) for i in range(q_min,q_max+1)])

for p,d,q in itertools.product(range(p_min,p_max+1),
                               range(d_min,d_max+1),
                               range(q_min,q_max+1)):
    if p==0 and d==0 and q==0:
        results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = np.nan
        continue
    try:
        model = sm.tsa.ARIMA(train, order=(p, d, q),
                               #enforce_stationarity=False,
                               #enforce_invertibility=False,
                              )
        results = model.fit()
        results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = results.bic
    except:
        continue

print(results_bic)

#得到结果后进行浮点型转换
results_bic = results_bic[results_bic.columns].astype(float)


#绘制热力图
fig, ax = plt.subplots(figsize=(10, 8))
ax = sns.heatmap(results_bic,
                 mask=results_bic.isnull(),
                 ax=ax,
                 annot=True,
                 fmt='.2f',
                 cmap="coolwarm"
                 )


plt.savefig('src/opencv_test/over_figure/bic_heatmap.png')  # 保存图片
plt.close()

results_bic.stack().idxmin()

train_results = sm.tsa.arma_order_select_ic(train, ic=['aic', 'bic'], trend='n', max_ar=8, max_ma=8)

print('AIC', train_results.aic_min_order)
print('BIC', train_results.bic_min_order)

#根据以上求得
p = 2
d = 0
q = 1

model = sm.tsa.ARIMA(train, order=(p,d,q))
results = model.fit()
resid = results.resid #获取残差
predict_sunspots = results.predict(dynamic=False)
print(predict_sunspots)


# 查看测试集的时间序列与数据(只包含测试集)
plt.figure(figsize=(12,6))
plt.plot(test, color='lightpink')  # 使用浅粉色
plt.xticks(rotation=45)  # 旋转45度
plt.plot(predict_sunspots, color='deepskyblue')  # 使用深天蓝色
plt.savefig('src/opencv_test/over_figure/test_data.png')  # 保存图片
plt.close()

# 绘图
fig, ax = plt.subplots(figsize=(12, 6))
ax = sub.plot(ax=ax, color='lightpink')  # 使用浅粉色
plt.plot(predict_sunspots, color='deepskyblue')  # 使用深天蓝色
predict_sunspots.plot(ax=ax, color='deepskyblue')  # 使用深天蓝色
plt.savefig('src/opencv_test/over_figure/original_predicted_data.png')  # 保存图片
plt.close()



