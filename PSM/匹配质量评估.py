import pandas as pd
import numpy as np
from scipy import stats

matched_sample = pd.read_excel("PSM_完整匹配样本.xlsx")

original_data = pd.read_excel("学生数据集.xlsx")

covariates = ["age", "female", "previous_score", "study_hours", "parent_support"]
treatment_var = "tutoring"

# 计算标准化差异函数
def calculate_smd(data, var, treatment_var):
    """计算单个变量的标准化均值差异"""
    treated = data[data[treatment_var] == 1][var]
    control = data[data[treatment_var] == 0][var]
    
    # 计算标准化差异
    mean_diff = treated.mean() - control.mean()
    pooled_std = np.sqrt((treated.var() + control.var()) / 2)
    
    # 如果标准差接近0，返回0
    if pooled_std < 1e-10:
        return 0
    
    return mean_diff / pooled_std

# 计算匹配前后所有协变量的标准化差异
balance_results = []

for var in covariates:
    # 匹配前的标准化差异
    before_smd = calculate_smd(original_data, var, treatment_var)
    
    # 匹配后的标准化差异
    after_smd = calculate_smd(matched_sample, var, treatment_var)
    
    # 保存结果
    balance_results.append({
        'Variable': var,
        'Before_SMD': before_smd,
        'After_SMD': after_smd,
        'Improvement': abs(before_smd) - abs(after_smd)
    })

# 转换为DataFrame
balance_df = pd.DataFrame(balance_results)

# 显示平衡性检验结果
print("协变量平衡性检验结果:")
print(balance_df)

# 计算平均绝对标准化差异(ASMD)
before_asmd = balance_df['Before_SMD'].abs().mean()
after_asmd = balance_df['After_SMD'].abs().mean()
print(f"\n匹配前平均绝对标准化差异(ASMD): {before_asmd:.4f}")
print(f"匹配后平均绝对标准化差异(ASMD): {after_asmd:.4f}")
print(f"改善幅度: {(before_asmd - after_asmd) / before_asmd * 100:.2f}%")

# 匹配前后的统计检验
print("\n匹配后处理组与对照组的协变量t检验结果:")
for var in covariates:
    treated_values = matched_sample[matched_sample[treatment_var] == 1][var]
    control_values = matched_sample[matched_sample[treatment_var] == 0][var]
    
    t_stat, p_value = stats.ttest_ind(treated_values, control_values, equal_var=False)
    
    print(f"{var}: t={t_stat:.4f}, p={p_value:.4f}{' (平衡)' if p_value > 0.05 else ' (不平衡)'}")
