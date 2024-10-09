import pandas as pd
# 处理33帧的问题!!!
# 读取Excel文件
df = pd.read_excel('src/opencv_test/data/235.xlsx')

# 计算每10个值的平均值
averages = df.iloc[:, 1].groupby(df.index // 10).mean()

# 创建新的DataFrame
new_df = pd.DataFrame({'时间': range(len(averages)), '速度': averages})

# 保存到新的Excel文件
new_df.to_excel('src/opencv_test/over_data/108_235.xlsx', index=False)
