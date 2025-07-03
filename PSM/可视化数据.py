import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patheffects as path_effects

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
plt.rcParams['font.size'] = 28
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

# 指定颜色池
colors = ['#A1A9D0', '#F0988C', '#B883D4', '#9E9E9E', '#CFEAF1', '#C4A5DE']

file_path = "学生数据集.xlsx"
df = pd.read_excel(file_path)

# 创建一个大图，包含两个子图
def create_combined_plots(df):
    # 创建一个大的图形和两个子图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(28, 12))
    
    # 1. 连续变量差异对比图 (左侧子图)
    vars_to_plot = ['age', 'previous_score', 'study_hours', 'math_score'] # 选择要展示的连续变量
    labels = ['年龄', '上学期成绩', '每日学习时间', '数学成绩'] # 设置对应的标签
    
    # 设置条形位置
    bar_width = 0.35
    index = np.arange(len(vars_to_plot))
    
    # 获取两组数据的均值
    tutoring_means = [
        df[df['tutoring']==1]['age'].mean(),
        df[df['tutoring']==1]['previous_score'].mean(),
        df[df['tutoring']==1]['study_hours'].mean(),
        df[df['tutoring']==1]['math_score'].mean()
    ]
    
    non_tutoring_means = [
        df[df['tutoring']==0]['age'].mean(),
        df[df['tutoring']==0]['previous_score'].mean(),
        df[df['tutoring']==0]['study_hours'].mean(),
        df[df['tutoring']==0]['math_score'].mean()
    ]
    
    # 绘制条形图
    bars1 = ax1.bar(index, tutoring_means, bar_width, alpha=0.8, color=colors[0], 
                  label='参加补习组')
    bars2 = ax1.bar(index + bar_width, non_tutoring_means, bar_width, alpha=0.8, 
                  color=colors[1], label='未参加补习组')
    
    # 添加数值标签
    def add_labels(bars, ax):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=26)
    
    add_labels(bars1, ax1)
    add_labels(bars2, ax1)
    
    # 添加图表元素
    ax1.set_xlabel('')
    ax1.set_ylabel('数值', fontsize=28)
    ax1.set_title('连续变量差异对比', pad=20, fontsize=33)
    ax1.set_xticks(index + bar_width / 2)
    ax1.set_xticklabels(labels, fontsize=24)
    ax1.legend(loc='upper left', fontsize=24)
    
    # 添加背景网格
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 2. 分类变量差异对比图 (右侧子图)
    # 计算各组的比例
    female_tutoring = df[df['tutoring']==1]['female'].mean() * 100
    female_non_tutoring = df[df['tutoring']==0]['female'].mean() * 100
    
    parent_tutoring = df[df['tutoring']==1]['parent_support'].mean() * 100
    parent_non_tutoring = df[df['tutoring']==0]['parent_support'].mean() * 100
    
    # 准备数据
    categories = ['女生比例', '家长辅导比例']
    tutoring_vals = [female_tutoring, parent_tutoring]
    non_tutoring_vals = [female_non_tutoring, parent_non_tutoring]
    
    # 创建散点图
    x = np.arange(len(categories))
    
    # 绘制散点图并添加连接线
    ax2.plot(x, tutoring_vals, 'o-', markersize=22, linewidth=3, color=colors[2], 
            label='参加补习组', alpha=0.8, path_effects=[path_effects.SimpleLineShadow(), 
                                                    path_effects.Normal()])
    ax2.plot(x, non_tutoring_vals, 's-', markersize=22, linewidth=3, color=colors[3], 
            label='未参加补习组', alpha=0.8, path_effects=[path_effects.SimpleLineShadow(), 
                                                     path_effects.Normal()])
    
    # 添加数值标签
    for i, (v1, v2) in enumerate(zip(tutoring_vals, non_tutoring_vals)):
        ax2.annotate(f'{v1:.1f}%', xy=(i, v1), xytext=(0, 10),
                    textcoords="offset points", ha='center', va='bottom',
                    fontsize=18, fontweight='bold', color=colors[2])
        ax2.annotate(f'{v2:.1f}%', xy=(i, v2), xytext=(0, -20),
                    textcoords="offset points", ha='center', va='top',
                    fontsize=22, fontweight='bold', color=colors[3])
    
    # 添加差异标注
    for i, (v1, v2) in enumerate(zip(tutoring_vals, non_tutoring_vals)):
        diff = v1 - v2
        color = 'red' if diff > 0 else 'blue'
        ax2.annotate(f'差异: {abs(diff):.1f}%', xy=(i, (v1+v2)/2), xytext=(30, 0),
                    textcoords="offset points", ha='left', va='center',
                    fontsize=22, color=color, arrowprops=dict(arrowstyle='->',
                                                            connectionstyle='arc3',
                                                            color=color))
    
    # 添加图表元素
    ax2.set_xlabel('')
    ax2.set_ylabel('百分比 (%)', fontsize=26)
    ax2.set_title('分类变量差异对比', pad=20, fontsize=30)
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories, fontsize=24)
    ax2.legend(loc='upper left', fontsize=24, frameon=True, framealpha=0.9, 
              shadow=True, facecolor='white')
    
    # 添加背景网格和美化
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    ax2.set_facecolor('#f8f9fa')
    
    # 添加区域着色以增强视觉效果
    ax2.fill_between(x, tutoring_vals, non_tutoring_vals, alpha=0.2, 
                    color='purple', label='差异区域')
    
    # 设置y轴范围，使差异更明显
    y_min = min(min(tutoring_vals), min(non_tutoring_vals)) * 0.8
    y_max = max(max(tutoring_vals), max(non_tutoring_vals)) * 1.1
    ax2.set_ylim(y_min, y_max)
    
    # 添加边框
    for spine in ax2.spines.values():
        spine.set_linewidth(2)
        spine.set_color('#333333')
    
    # 调整布局并保存
    plt.tight_layout(rect=[0, 0, 1, 1])  # 为顶部的总标题留出空间
    plt.savefig('补习效果对比分析.png', dpi=600, bbox_inches='tight')
    plt.show()


create_combined_plots(df)
