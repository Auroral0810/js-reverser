import pandas as pd
import numpy as np
from scipy import stats

# 读取数据集
file_path = "学生数据集.xlsx"
data = pd.read_excel(file_path)

# 创建统计特征报告
with open("统计学特征报告.txt", "w", encoding="utf-8") as f:
    f.write("学生数据集统计学特征报告\n")
    f.write("=" * 50 + "\n\n")
    
    f.write("1. 基本信息\n")
    f.write("-" * 30 + "\n")
    f.write(f"样本数量: {data.shape[0]}\n")
    f.write(f"变量数量: {data.shape[1]}\n\n")
    
    # 描述性统计
    f.write("2. 描述性统计\n")
    f.write("-" * 30 + "\n")
    desc_stats = data.describe().T
    desc_stats['变异系数'] = desc_stats['std'] / desc_stats['mean']
    f.write(desc_stats.to_string() + "\n\n")
    
    # 分类变量频率统计
    f.write("3. 分类变量频率统计\n")
    f.write("-" * 30 + "\n")
    
    # 性别分布
    gender_counts = data['female'].value_counts()
    gender_percent = data['female'].value_counts(normalize=True) * 100
    f.write("性别分布:\n")
    f.write(f"男生: {gender_counts.get(0, 0)}人 ({gender_percent.get(0, 0):.2f}%)\n")
    f.write(f"女生: {gender_counts.get(1, 0)}人 ({gender_percent.get(1, 0):.2f}%)\n\n")
    
    # 家长辅导分布
    parent_counts = data['parent_support'].value_counts()
    parent_percent = data['parent_support'].value_counts(normalize=True) * 100
    f.write("家长辅导分布:\n")
    f.write(f"无家长辅导: {parent_counts.get(0, 0)}人 ({parent_percent.get(0, 0):.2f}%)\n")
    f.write(f"有家长辅导: {parent_counts.get(1, 0)}人 ({parent_percent.get(1, 0):.2f}%)\n\n")
    
    # 补习班参与情况
    tutor_counts = data['tutoring'].value_counts()
    tutor_percent = data['tutoring'].value_counts(normalize=True) * 100
    f.write("补习班参与情况:\n")
    f.write(f"未参加补习: {tutor_counts.get(0, 0)}人 ({tutor_percent.get(0, 0):.2f}%)\n")
    f.write(f"参加补习: {tutor_counts.get(1, 0)}人 ({tutor_percent.get(1, 0):.2f}%)\n\n")
    
    # 分组统计
    f.write("4. 按补习班参与情况分组统计\n")
    f.write("-" * 30 + "\n")
    group_stats = data.groupby('tutoring').agg({
        'age': ['mean', 'std'],
        'female': 'mean',
        'previous_score': ['mean', 'std'],
        'study_hours': ['mean', 'std'],
        'parent_support': 'mean',
        'math_score': ['mean', 'std']
    })
    f.write(group_stats.to_string() + "\n\n")
    
    # 计算标准化差异
    f.write("5. 标准化差异(Standardized Differences)\n")
    f.write("-" * 30 + "\n")
    
    # 获取两组数据
    treated = data[data['tutoring'] == 1]
    control = data[data['tutoring'] == 0]
    
    # 计算连续变量的标准化差异
    continuous_vars = ['age', 'previous_score', 'study_hours', 'math_score']
    f.write("连续变量标准化差异:\n")
    
    for var in continuous_vars:
        mean_treated = treated[var].mean()
        mean_control = control[var].mean()
        var_treated = treated[var].var()
        var_control = control[var].var()
        
        # 计算标准化差异
        std_diff = (mean_treated - mean_control) / np.sqrt((var_treated + var_control) / 2)
        f.write(f"{var}: {std_diff:.4f}\n")
    
    # 计算二分类变量的标准化差异
    binary_vars = ['female', 'parent_support']
    f.write("\n二分类变量标准化差异:\n")
    
    for var in binary_vars:
        p_treated = treated[var].mean()
        p_control = control[var].mean()
        
        # 计算二分类变量的标准化差异
        std_diff = (p_treated - p_control) / np.sqrt((p_treated * (1 - p_treated) + p_control * (1 - p_control)) / 2)
        f.write(f"{var}: {std_diff:.4f}\n")
    
    # 相关性分析
    f.write("\n6. 相关性分析\n")
    f.write("-" * 30 + "\n")
    corr_matrix = data.corr()
    f.write(corr_matrix.to_string() + "\n\n")
    
    # 处理效应初步估计
    f.write("7. 处理效应初步估计\n")
    f.write("-" * 30 + "\n")
    
    # 简单比较
    mean_diff = treated['math_score'].mean() - control['math_score'].mean()
    f.write(f"补习班参与对数学成绩的简单平均效应: {mean_diff:.4f}\n")
    
    # t检验
    t_stat, p_val = stats.ttest_ind(treated['math_score'], control['math_score'], equal_var=False)
    f.write(f"t检验结果: t={t_stat:.4f}, p={p_val:.4f}\n")