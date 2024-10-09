import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 创建一个新的图形窗口
fig, ax = plt.subplots()

# 添加文本
ax.text(0.5, 0.8, 'CIB', ha='center', va='center', fontsize=12)
ax.text(0.5, 0.6, 'N', ha='center', va='center', fontsize=12)
ax.text(0.5, 0.4, '1x1', ha='center', va='center', fontsize=12)

ax.text(2.5, 0.8, 'CIB', ha='center', va='center', fontsize=12)
ax.text(2.5, 0.6, '3x3DW', ha='center', va='center', fontsize=12)

ax.text(5.5, 0.8, '1x1', ha='center', va='center', fontsize=12)
ax.text(5.5, 0.6, '3x3DW', ha='center', va='center', fontsize=12)
ax.text(5.5, 0.4, '1x1', ha='center', va='center', fontsize=12)

# 添加箭头
arrowprops=dict(arrowstyle='-|>', color='black')

# 绘制箭头
ax.annotate('', xy=(0.8, 0.5), xytext=(0.2, 0.5),
            arrowprops=arrowprops)
ax.annotate('', xy=(2.8, 0.5), xytext=(2.2, 0.5),
            arrowprops=arrowprops)
ax.annotate('', xy=(5.8, 0.5), xytext=(5.2, 0.5),
            arrowprops=arrowprops)

# 设置坐标轴的范围
ax.set_xlim(0, 7)
ax.set_ylim(0, 1)

# 隐藏坐标轴
ax.axis('off')

# 显示图形
plt.show()