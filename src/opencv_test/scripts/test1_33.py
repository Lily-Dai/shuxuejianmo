import pandas as pd
import re
import os

# 提取speed值的函数
def extract_speed(cell):
    match = re.search(r"'speed': (\d+\.?\d*)", str(cell))
    return float(match.group(1)) if match else None

# 数据清洗函数
def clean_data(row):
    values = row.dropna()
    if len(values) <= 1:
        return 0
    max_value = values.max()
    min_value = values.min()
    deviation = max_value - min_value
    if deviation > 20:
        cleaned_values = values[(values != max_value) & (values != min_value)]
        return cleaned_values.mean() if not cleaned_values.empty else 0
    return values.mean()

# 遍历文件夹下所有Excel文件
folder_path = 'src/opencv_test/data/'
output_folder = 'src/opencv_test/over_data/'

for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx'):
        data = pd.read_excel(os.path.join(folder_path, filename))
        speed_data = data.applymap(extract_speed)
        mean_values = speed_data.apply(clean_data, axis=1)
        result = pd.DataFrame(mean_values, columns=['Average'])
        result = pd.concat([result, speed_data], axis=1)
        result['Average'] = result['Average'].replace(0, pd.NA).interpolate(method='linear')
        average_per_25 = result['Average'].groupby(result.index // 33).mean()
        final_result = pd.DataFrame({
            '时间': [i*10 for i in range(len(average_per_25))],
            '速度': average_per_25.values
        })
        final_result['速度'] = final_result['速度'].replace(0, pd.NA).interpolate(method='linear')
        final_result['速度'].fillna(method='ffill', inplace=True)
        final_result['速度'].fillna(method='bfill', inplace=True)
        final_result.to_excel(os.path.join(output_folder, filename), index=False)
