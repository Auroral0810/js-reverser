import numpy as np
import pandas as pd

# 设置随机种子，确保结果可重现
np.random.seed(42)

# 生成示例数据
n_students = 1000

# 生成学生特征
age = np.random.normal(15, 1.5, n_students)  # 学生年龄
previous_score = np.random.normal(70, 15, n_students)  # 上学期数学成绩
study_hours = np.random.normal(2, 1, n_students)  # 每天学习时间
parent_support = np.random.binomial(1, 0.5, n_students)  # 是否有家长辅导
female = np.random.binomial(1, 0.48, n_students)  # 学生性别（女性=1）

# 添加相关性：成绩低的学生更可能有家长辅导
parent_support = np.where(
    previous_score < 65, 
    np.random.binomial(1, 0.7, n_students), 
    parent_support
)

# 计算参加补习班的倾向（受多个因素影响）
# 成绩低、学习时间少、有家长辅导和女生更可能参加补习班
propensity = (
    -0.2 * previous_score/10 +  # 成绩越低越可能参加
    -0.5 * study_hours +        # 自主学习时间越少越可能参加
    0.8 * parent_support +      # 有家长支持更可能参加
    0.4 * female +              # 女生更可能参加
    np.random.normal(0, 1, n_students)  # 随机因素
)

# 将倾向转换为概率
probability = 1 / (1 + np.exp(-propensity))

# 生成补习班参与情况（处理变量）
tutoring = np.random.binomial(1, probability)

# 生成结果变量（数学成绩）
# 补习班平均提高了5分，但效果与学生特征相关
effect = 5 + 0.1 * (70 - previous_score) + np.random.normal(0, 2, n_students)
math_score = (
    previous_score * 0.7 +                  # 上学期成绩的影响
    study_hours * 3 +                       # 学习时间的影响
    parent_support * 2 +                    # 家长辅导的影响
    female * 1 +                            # 性别影响
    tutoring * effect +                     # 补习班的影响（包括异质性）
    np.random.normal(20, 8, n_students)     # 随机波动和其他因素
)

# 创建数据框
data = pd.DataFrame({
    'student_id': range(1, n_students + 1),
    'age': age,
    'female': female,
    'previous_score': previous_score,
    'study_hours': study_hours,
    'parent_support': parent_support,
    'tutoring': tutoring,
    'math_score': math_score
})

# 查看数据
print("数据集前5行：")
print(data.head())

# 基本统计描述
print("\n数据集基本统计：")
print(data.describe())

# 查看两组学生的特征差异
print("\n参加补习班与未参加补习班学生的特征对比：")
group_comparison = data.groupby('tutoring').mean()
print(group_comparison)

# 将数据保存到Excel文件
data.to_excel("学生数据集.xlsx", index=False)
print("\n数据已保存到'学生数据集.xlsx'文件")

# 将分组比较结果保存到Excel
group_comparison.to_excel("补习班分组对比.xlsx")
print("分组对比结果已保存到'补习班分组对比.xlsx'文件")
