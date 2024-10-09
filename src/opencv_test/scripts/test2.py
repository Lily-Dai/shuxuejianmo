import pandas as pd
import re
# 计算车流密度!!!!!!!
# 读取Excel文件
data = pd.read_excel('src/opencv_test/data/10s数据.xlsx')

# 提取speed值的函数
def extract_speed(cell):
    match = re.search(r"'track_id': (\d+\.?\d*)", str(cell))
    return float(match.group(1)) if match else None

# 遍历整个DataFrame，提取speed值
speed_data = data.applymap(extract_speed)

# 保存到新的Excel文件
speed_data.to_excel('src/opencv_test/over_data/test02.xlsx', index=False)