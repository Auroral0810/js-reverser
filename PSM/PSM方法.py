# 导入所需库
import pandas as pd
from sklearn.linear_model import LogisticRegression

# 读取数据
student_data = pd.read_excel("学生数据集.xlsx")

# 定义处理变量和协变量
treatment_var = "tutoring"  # 处理变量是否参加补习班
covariates = ["age", "female", "previous_score", "study_hours", "parent_support"]  # 协变量

# 准备特征(X)和标签(y)
X = student_data[covariates]  # 协变量作为特征
y = student_data[treatment_var]  # 处理变量作为标签

# 使用逻辑回归模型估计倾向得分
model = LogisticRegression(random_state=42)
model.fit(X, y)

# 获取倾向得分（参加补习班的概率）
propensity_scores = model.predict_proba(X)[:, 1]

# 将倾向得分添加到原始数据框
student_data['propensity_score'] = propensity_scores

# 输出模型系数
print("逻辑回归模型系数:")
for feature, coef in zip(covariates, model.coef_[0]):
    print(f"{feature}: {coef:.4f}")

# 显示基本统计信息
print("\n倾向得分统计信息:")
print(student_data['propensity_score'].describe())

# 显示前10条数据的倾向得分
print("\n前10条数据的倾向得分:")
print(student_data[['student_id', *covariates, 'tutoring', 'propensity_score']].head(10))

# 或者导出到Excel以查看所有数据
student_data.to_excel("学生数据集_带倾向得分.xlsx", index=False)