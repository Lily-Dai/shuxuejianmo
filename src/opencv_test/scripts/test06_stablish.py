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
#根据以上求得
p = 2
d = 0
q = 1

model = sm.tsa.ARIMA(train, order=(p,d,q))
results = model.fit()
resid = results.resid #获取残差

#绘制
#查看测试集的时间序列与数据(只包含测试集)
fig, ax = plt.subplots(figsize=(12, 3))
ax = sm.graphics.tsa.plot_acf(resid, lags=40, ax=ax)
plt.title('Figure 1: Residuals Autocorrelation')
plt.savefig('src/opencv_test/over_figure/residuals_autocorrelation.png')  # 保存图片
plt.close()  # 关闭图形，避免显示

# predict_sunspots = results.predict(start=len(train), end=len(train)+len(test)-20, dynamic=False)
predict_sunspots = results.predict(dynamic=False)
print(predict_sunspots)

#查看测试集的时间序列与数据(只包含测试集)
plt.figure(figsize=(10,4))
plt.plot(train, label='Predicted Data', color='#5283C5', linewidth=3)  # 浅蓝色，边框宽度为3
plt.plot(predict_sunspots, label='Training Data', color='lightpink', linewidth=3)  # 浅粉色，边框宽度为3
plt.xticks(rotation=45) #旋转45度
plt.legend() # 添加图例
# plt.title('Figure 2: 训练数据和预测数据') 
plt.savefig('src/opencv_test/over_figure/训练数据和预测数据.png')  # 保存图片
plt.close()  # 关闭图形，避免显示

#绘图
fig, ax = plt.subplots(figsize=(10, 4))
ax = sub.plot(ax=ax, label='Predicted Data', color='#5283C5', linewidth=3)  # 浅蓝色，边框宽度为3
predict_sunspots.plot(ax=ax, label='Original Data', color='lightpink', linewidth=3)  # 浅粉色，边框宽度为3
plt.legend() # 添加图例
# plt.title('Figure 3: 原始数据和预测数据') 
plt.savefig('src/opencv_test/over_figure/原始数据和预测数据.png')  # 保存图片
plt.close()  # 关闭图形，避免显示