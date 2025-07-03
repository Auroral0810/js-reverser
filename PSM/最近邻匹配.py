import pandas as pd
import numpy as np

student_data = pd.read_excel("学生数据集_带倾向得分.xlsx")

# 1. 将数据分为处理组和对照组
treated = student_data[student_data['tutoring'] == 1].copy()
control = student_data[student_data['tutoring'] == 0].copy()

# 2. 为每个处理组样本找到最近邻的对照组样本
# 用于存储匹配结果
matches = []

# 设置匹配的卡尺宽度(caliper)
caliper = 0.05

# 对每个处理组样本进行匹配
for idx, treated_unit in treated.iterrows():
    # 计算与所有对照组的倾向得分差的绝对值
    control['score_diff'] = abs(control['propensity_score'] - treated_unit['propensity_score'])

    # 选择差异最小的作为匹配对象（必须在卡尺宽度内）
    best_matches = control[control['score_diff'] <= caliper].sort_values('score_diff')

    if len(best_matches) > 0:
        # 取最接近的一个对照单位
        best_match = best_matches.iloc[0].copy()

        # 存储匹配对
        match_pair = {
            'treated_id': treated_unit['student_id'],
            'control_id': best_match['student_id'],
            'treated_ps': treated_unit['propensity_score'],
            'control_ps': best_match['propensity_score'],
            'ps_diff': best_match['score_diff'],
            'treated_outcome': treated_unit['math_score'],
            'control_outcome': best_match['math_score']
        }
        matches.append(match_pair)

# 3. 将匹配结果转换为DataFrame
matched_df = pd.DataFrame(matches)

# 4. 计算匹配数量和统计信息
print(f"\n成功匹配的样本数: {len(matched_df)}")
print(f"匹配率: {len(matched_df) / len(treated) * 100:.2f}%")

# 5. 计算匹配质量
print("\n匹配质量统计:")
print(f"平均倾向得分差异: {matched_df['ps_diff'].mean():.6f}")
print(f"最大倾向得分差异: {matched_df['ps_diff'].max():.6f}")

# 6. 保存匹配结果
matched_df.to_excel("PSM_匹配结果.xlsx", index=False)

