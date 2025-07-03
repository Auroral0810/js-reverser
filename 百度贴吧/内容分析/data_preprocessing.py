import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import jieba
import os
from tqdm import tqdm
import json
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

def load_data(file_path):
    """
    加载原始数据
    
    参数:
        file_path: 数据文件路径
    
    返回:
        加载的数据框
    """
    print(f"正在加载数据: {file_path}")
    
    # 根据文件类型加载数据
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.json'):
        df = pd.read_json(file_path)
    else:
        raise ValueError("不支持的文件格式，请提供 CSV, Excel 或 JSON 文件")
    
    print(f"数据加载完成，共 {df.shape[0]} 行, {df.shape[1]} 列")
    return df

def check_data_quality(df):
    """
    检查数据质量
    
    参数:
        df: 数据框
    
    返回:
        质量报告字典
    """
    print("正在检查数据质量...")
    
    # 初始化质量报告
    quality_report = {
        "总行数": len(df),
        "总列数": len(df.columns),
        "列名": list(df.columns),
        "数据类型": {col: str(df[col].dtype) for col in df.columns},
        "缺失值": {col: int(df[col].isna().sum()) for col in df.columns},
        "缺失值百分比": {col: round(df[col].isna().sum() / len(df) * 100, 2) for col in df.columns},
        "重复行数": len(df) - len(df.drop_duplicates()),
        "唯一值数量": {col: df[col].nunique() for col in df.columns}
    }
    
    return quality_report

def clean_data(df):
    """
    清洗数据
    
    参数:
        df: 原始数据框
    
    返回:
        清洗后的数据框
    """
    print("正在清洗数据...")
    
    # 创建副本避免修改原始数据
    cleaned_df = df.copy()
    
    # 1. 处理列名 - 确保列名标准化
    cleaned_df.columns = [col.strip() for col in cleaned_df.columns]
    
    # 2. 去除重复行
    before_drop = len(cleaned_df)
    cleaned_df = cleaned_df.drop_duplicates()
    after_drop = len(cleaned_df)
    print(f"已删除 {before_drop - after_drop} 行重复数据")
    
    # 3. 统一时间格式 - 修改这部分代码
    if '发布时间' in cleaned_df.columns:
        # 创建一个日期时间转换标志
        date_converted = False
        
        # 首先检查并移除列名中可能的空格
        if not date_converted and '发布时间' in cleaned_df.columns:
            try:
                # 尝试直接用pandas自动识别格式
                cleaned_df['发布时间'] = pd.to_datetime(cleaned_df['发布时间'], errors='coerce')
                date_converted = True
                print("成功使用自动识别转换日期时间格式")
            except Exception as e:
                print(f"自动识别日期格式失败: {e}")
        
        # 如果自动识别失败，尝试常见格式
        formats = [
            '%Y-%m-%d %H:%M:%S', 
            '%Y-%m-%d %H:%M', 
            '%Y/%m/%d %H:%M:%S',
            '%Y/%m/%d %H:%M',
            '%d/%m/%Y %H:%M:%S',
            '%d/%m/%Y %H:%M',
            '%Y年%m月%d日 %H:%M:%S',
            '%Y年%m月%d日 %H:%M'
        ]
        
        if not date_converted:
            for date_format in formats:
                try:
                    cleaned_df['发布时间'] = pd.to_datetime(cleaned_df['发布时间'], format=date_format, errors='coerce')
                    date_converted = True
                    print(f"成功使用格式 {date_format} 转换日期时间")
                    break
                except Exception as e:
                    print(f"尝试格式 {date_format} 失败: {e}")
        
        # 处理可能的无效日期
        if date_converted:
            # 处理异常日期（如未来日期）
            current_time = pd.Timestamp.now()
            cleaned_df.loc[cleaned_df['发布时间'] > current_time, '发布时间'] = pd.NaT
            # 检查有多少成功转换的日期
            valid_dates = cleaned_df['发布时间'].notna().sum()
            print(f"成功转换 {valid_dates} 行日期数据，占比 {valid_dates/len(cleaned_df)*100:.2f}%")
        else:
            # 如果所有转换都失败，创建一个辅助日期列用于时间分析
            print("所有日期格式转换尝试均失败，创建一个辅助日期标志列")
            cleaned_df['日期已转换'] = False
    
    # 4. 确保ID字段为字符串类型
    id_columns = ['帖子ID', 'ID', '父评论ID']
    for col in id_columns:
        if col in cleaned_df.columns:
            cleaned_df[col] = cleaned_df[col].astype(str)
    
    # 5. 处理文本内容
    if '内容' in cleaned_df.columns:
        # 处理HTML实体和转义字符
        cleaned_df['内容'] = cleaned_df['内容'].fillna('')
        # 替换HTML标签和特殊字符
        cleaned_df['内容'] = cleaned_df['内容'].apply(clean_text)
        # 去除空白内容行
        cleaned_df = cleaned_df[cleaned_df['内容'].str.strip() != '']
    
    # 6. 处理图片链接
    if '图片' in cleaned_df.columns:
        cleaned_df['有图片'] = cleaned_df['图片'].notnull() & (cleaned_df['图片'] != '')
    
    # 7. 数值型列处理
    if '回复数量' in cleaned_df.columns:
        cleaned_df['回复数量'] = pd.to_numeric(cleaned_df['回复数量'], errors='coerce').fillna(0).astype(int)
    
    if '楼层' in cleaned_df.columns:
        cleaned_df['楼层'] = pd.to_numeric(cleaned_df['楼层'], errors='coerce').fillna(0).astype(int)
    
    return cleaned_df

def clean_text(text):
    """
    清洗文本内容
    
    参数:
        text: 原始文本
    
    返回:
        清洗后的文本
    """
    if pd.isna(text) or text == '':
        return ''
    
    # 转换为字符串
    text = str(text)
    
    # 替换HTML标签
    text = re.sub(r'<.*?>', '', text)
    
    # 替换URL
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '[URL]', text)
    
    # 替换特殊ASCII字符
    text = re.sub(r'&#\d+;', '', text)
    
    # 替换连续的空白字符为单个空格
    text = re.sub(r'\s+', ' ', text)
    
    # 去除常见的广告标记
    ad_patterns = [
        r'推广', r'广告', r'关注.*?公众号', r'私聊', r'微信.*?咨询', 
        r'点击链接', r'下载APP', r'购买', r'优惠码'
    ]
    for pattern in ad_patterns:
        text = re.sub(pattern, '', text)
    
    # 去除首尾空白
    text = text.strip()
    
    return text

def build_comment_tree(df):
    """
    构建评论树结构
    
    参数:
        df: 数据框
    
    返回:
        包含树结构的字典
    """
    print("正在构建评论树结构...")
    
    # 确保必要的列存在
    required_cols = ['帖子ID', 'ID', '父评论ID']
    if not all(col in df.columns for col in required_cols):
        print("警告: 缺少构建评论树所需的列")
        missing_cols = [col for col in required_cols if col not in df.columns]
        print(f"缺少的列: {missing_cols}")
        return None
    
    # 初始化评论树字典
    comment_trees = defaultdict(dict)
    
    # 按帖子ID分组
    post_groups = df.groupby('帖子ID')
    
    for post_id, post_df in post_groups:
        # 创建ID到评论的映射
        id_to_comment = {row['ID']: row.to_dict() for _, row in post_df.iterrows()}
        
        # 初始化根节点和子节点映射
        root_comments = []
        children_map = defaultdict(list)
        
        # 遍历评论构建树结构
        for _, row in post_df.iterrows():
            comment_id = row['ID']
            parent_id = row['父评论ID']
            
            # 如果父ID为空或等于自身ID，则为根评论
            if pd.isna(parent_id) or parent_id == '' or parent_id == comment_id:
                root_comments.append(comment_id)
            else:
                # 添加到父评论的子评论列表
                children_map[parent_id].append(comment_id)
        
        # 将树结构存储到字典中
        comment_trees[post_id] = {
            'root_comments': root_comments,
            'children_map': dict(children_map),
            'comments': id_to_comment
        }
    
    print(f"已构建 {len(comment_trees)} 个帖子的评论树")
    return comment_trees

def generate_data_report(df, quality_report, output_dir='./output'):
    """
    生成数据报告
    
    参数:
        df: 数据框
        quality_report: 质量报告字典
        output_dir: 输出目录
    """
    print("正在生成数据报告...")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 保存质量报告为JSON
    with open(f"{output_dir}/data_quality_report.json", 'w', encoding='utf-8') as f:
        json.dump(quality_report, f, ensure_ascii=False, indent=2)
    
    # 2. 生成基本统计图表
    if '内容' in df.columns:
        plt.figure(figsize=(10, 6))
        df['内容长度'] = df['内容'].apply(lambda x: len(str(x)) if not pd.isna(x) else 0)
        sns.histplot(df['内容长度'], bins=50)
        plt.title('评论长度分布')
        plt.xlabel('字符数')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/comment_length_distribution.png")
        plt.close()
    
    # 3. 生成数据摘要报告
    with open(f"{output_dir}/data_summary.txt", 'w', encoding='utf-8') as f:
        f.write("===== 孙笑川吧评论数据摘要 =====\n\n")
        f.write(f"数据集大小: {df.shape[0]} 行, {df.shape[1]} 列\n")
        f.write(f"数据列: {', '.join(df.columns)}\n\n")
        
        if '帖子ID' in df.columns:
            f.write(f"帖子数量: {df['帖子ID'].nunique()}\n")
        
        if '用户名' in df.columns:
            f.write(f"用户数量: {df['用户名'].nunique()}\n")
        
        if '发布时间' in df.columns:
            f.write(f"数据时间范围: {df['发布时间'].min()} 至 {df['发布时间'].max()}\n")
        
        if '内容' in df.columns:
            f.write(f"平均评论长度: {df['内容'].apply(len).mean():.2f} 字符\n")
        
        if '回复数量' in df.columns:
            f.write(f"平均回复数: {df['回复数量'].mean():.2f}\n")
        
        f.write("\n===== 数据质量问题 =====\n\n")
        for col, pct in quality_report['缺失值百分比'].items():
            if pct > 0:
                f.write(f"{col}: {pct:.2f}% 数据缺失\n")
    
    print(f"数据报告已生成至目录: {output_dir}")

def convert_timestamps_to_str(obj):
    """
    递归地将字典或列表中的Timestamp对象和NaT转换为可序列化的格式
    
    参数:
        obj: 要转换的对象
    
    返回:
        转换后的对象
    """
    if isinstance(obj, dict):
        return {k: convert_timestamps_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_timestamps_to_str(item) for item in obj]
    elif isinstance(obj, pd.Timestamp):
        return str(obj)
    elif pd.isna(obj):  # 处理NaN和NaT
        return None
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

def save_cleaned_data(df, comment_trees, output_dir='./output'):
    """
    保存清洗后的数据
    
    参数:
        df: 清洗后的数据框
        comment_trees: 评论树结构
        output_dir: 输出目录
    """
    print("正在保存清洗后的数据...")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存清洗后的数据框
    df.to_csv(f"{output_dir}/cleaned_data.csv", index=False, encoding='utf-8')
    
    # 保存评论树结构
    if comment_trees:
        print("正在处理评论树中的Timestamp类型...")
        # 转换Timestamp为字符串
        serializable_trees = convert_timestamps_to_str(comment_trees)
        
        with open(f"{output_dir}/comment_trees.json", 'w', encoding='utf-8') as f:
            json.dump(serializable_trees, f, ensure_ascii=False, indent=2)
    
    print(f"清洗后的数据已保存至目录: {output_dir}")

def main(input_file, output_dir='./output'):
    """
    主函数
    
    参数:
        input_file: 输入文件路径
        output_dir: 输出目录
    """
    # 1. 加载数据
    df = load_data(input_file)
    
    # 2. 检查数据质量
    quality_report = check_data_quality(df)
    
    # 3. 清洗数据
    cleaned_df = clean_data(df)
    
    # 4. 构建评论树
    comment_trees = build_comment_tree(cleaned_df)
    
    # 5. 生成报告
    generate_data_report(cleaned_df, quality_report, output_dir)
    
    # 6. 保存清洗后的数据
    save_cleaned_data(cleaned_df, comment_trees, output_dir)
    
    print("数据清洗与标准化完成!")
    return cleaned_df, comment_trees

if __name__ == "__main__":
    input_file = "孙笑川吧_所有评论回复.csv" 
    output_dir = "data_preprocessing"
    
    # 执行主函数
    cleaned_df, comment_trees = main(input_file, output_dir)
    
    print("\n数据预处理完成，可以进行下一步分析了!")
