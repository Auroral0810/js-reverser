import pandas as pd
import numpy as np
from scipy import stats

# 1. 读取匹配结果
matched_df = pd.read_excel("PSM_匹配结果.xlsx")

# 2. 计算配对样本的平均处理效应(ATT)
att = matched_df['treated_outcome'].mean() - matched_df['control_outcome'].mean()

# 3. 执行配对t检验，评估统计显著性
t_stat, p_value = stats.ttest_rel(matched_df['treated_outcome'], matched_df['control_outcome'])

# 4. 计算效应量的置信区间
# 首先计算每个匹配对的差异
matched_df['outcome_diff'] = matched_df['treated_outcome'] - matched_df['control_outcome']
# 然后计算标准误
se = matched_df['outcome_diff'].std() / np.sqrt(len(matched_df))
# 95%置信区间
ci_lower = att - 1.96 * se
ci_upper = att + 1.96 * se

# 5. 计算标准化效应量(Cohen's d)
cohens_d = att / matched_df['outcome_diff'].std()

# 6. 输出结果
print("平均处理效应(ATT)估计结果:")
print(f"补习班对数学成绩的平均效应: {att:.4f} 分")
print(f"t统计量: {t_stat:.4f}, p值: {p_value:.4f}")
print(f"95%置信区间: [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"标准化效应量(Cohen's d): {cohens_d:.4f}")

# 7. 基本统计数据
print("\n基本统计数据:")
print(f"匹配样本数量: {len(matched_df)}")
print(f"参加补习班组平均成绩: {matched_df['treated_outcome'].mean():.4f}")
print(f"未参加补习班组平均成绩: {matched_df['control_outcome'].mean():.4f}")