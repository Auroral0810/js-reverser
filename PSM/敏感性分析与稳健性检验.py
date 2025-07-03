import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm

original_data = pd.read_excel("学生数据集_带倾向得分.xlsx")
matched_results = pd.read_excel("PSM_匹配结果.xlsx")

# Rosenbaum界限分析 - 敏感性分析的简化版本
def sensitivity_analysis(matched_df):
    # 计算处理组和对照组的结果差异
    outcome_diff = matched_df['treated_outcome'] - matched_df['control_outcome']
    
    # 基本统计量
    mean_diff = outcome_diff.mean()
    std_diff = outcome_diff.std()
    n = len(outcome_diff)
    
    # 计算不同gamma值下的p值(模拟Rosenbaum界限法的简化版)
    gammas = [1.0, 1.2, 1.5, 1.8, 2.0]
    results = []
    
    for gamma in gammas:
        # 调整标准误以模拟未观测混淆因素的影响
        adjusted_se = std_diff * np.sqrt(gamma) / np.sqrt(n)
        
        # 计算调整后的z值和p值
        z_score = mean_diff / adjusted_se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
        
        results.append({
            'gamma': gamma,
            'z_score': z_score,
            'p_value': p_value
        })
    
    return pd.DataFrame(results)

# 不同卡尺宽度的稳健性检验
def caliper_robustness(data, treatment_var, outcome_var, ps_var, calipers):
    results = []
    
    for caliper in calipers:
        treated = data[data[treatment_var] == 1].copy()
        control = data[data[treatment_var] == 0].copy()
        
        matches = []
        for idx, treated_unit in treated.iterrows():
            ps_treated = treated_unit[ps_var]
            
            # 找到在卡尺宽度内的对照单位
            valid_controls = control[(abs(control[ps_var] - ps_treated) <= caliper)]
            
            if len(valid_controls) > 0:
                # 选择最近的一个
                valid_controls['ps_diff'] = abs(valid_controls[ps_var] - ps_treated)
                best_match = valid_controls.loc[valid_controls['ps_diff'].idxmin()]
                
                matches.append({
                    'treated_outcome': treated_unit[outcome_var],
                    'control_outcome': best_match[outcome_var]
                })
        
        if matches:
            # 计算ATT
            match_df = pd.DataFrame(matches)
            att = match_df['treated_outcome'].mean() - match_df['control_outcome'].mean()
            t_stat, p_value = stats.ttest_rel(match_df['treated_outcome'], match_df['control_outcome'])
            
            results.append({
                'caliper': caliper,
                'matches': len(match_df),
                'ATT': att,
                'p_value': p_value
            })
    
    return pd.DataFrame(results)

# 子组分析
def subgroup_analysis(data, treatment_var, outcome_var, subgroup_var):
    results = []
    
    # 获取子组的唯一值
    subgroups = data[subgroup_var].unique()
    
    for subgroup in subgroups:
        # 筛选子组数据
        subgroup_data = data[data[subgroup_var] == subgroup]
        
        # 计算子组ATT
        treated = subgroup_data[subgroup_data[treatment_var] == 1][outcome_var]
        control = subgroup_data[subgroup_data[treatment_var] == 0][outcome_var]
        
        if len(treated) > 0 and len(control) > 0:
            att = treated.mean() - control.mean()
            t_stat, p_value = stats.ttest_ind(treated, control)
            
            results.append({
                'subgroup': subgroup,
                'treated_n': len(treated),
                'control_n': len(control),
                'ATT': att,
                'p_value': p_value
            })
    
    return pd.DataFrame(results)

# 敏感性分析
sensitivity_results = sensitivity_analysis(matched_results)
print("Rosenbaum界限敏感性分析结果:")
print(sensitivity_results)

# 不同卡尺宽度的稳健性分析
calipers = [0.01, 0.03, 0.05, 0.1, 0.2]
caliper_results = caliper_robustness(original_data, 'tutoring', 'math_score', 'propensity_score', calipers)
print("\n不同卡尺宽度下的处理效应估计:")
print(caliper_results)

# 子组分析 - 以性别为例
subgroup_results = subgroup_analysis(original_data, 'tutoring', 'math_score', 'female')
print("\n性别子组分析结果:")
print(subgroup_results)