import pandas as pd
import ast
import os

# 定义源文件夹和目标文件夹路径
src_folder = 'src/opencv_test/data'  # 替换为你的源文件路径
dst_folder = 'src/opencv_test/over_data'  # 替换为你的目标文件路径

# 确保目标文件夹存在
if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)

# 遍历源文件夹中的所有文件
for file_name in os.listdir(src_folder):
    # 检查文件是否为Excel文件
    if file_name.endswith('.xlsx'):
        # 构建完整的文件路径
        file_path = os.path.join(src_folder, file_name)
        
        # 读取 Excel 文件
        df = pd.read_excel(file_path)
        
        # 定义清除不匹配数据的函数
        def clear_non_matching(cell):
            if isinstance(cell, str):
                try:
                    data = ast.literal_eval(cell)  # 将字符串转为字典
                    if data.get('class') != 2.0:
                        return ''  # 清除不匹配的数据
                except (ValueError, SyntaxError):
                    pass  # 如果不是字典格式，保持不变
            return cell
        
        # 应用函数到整个 DataFrame
        df = df.applymap(clear_non_matching)
        
        # 构建目标文件路径
        dst_file_path = os.path.join(dst_folder, file_name)
        
        # 将修改后的 DataFrame 写回到新的 Excel 文件
        df.to_excel(dst_file_path, index=False)

print("所有文件处理完成，并保存到目标文件夹。")