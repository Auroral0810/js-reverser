import pandas as pd
import os
import json
import glob
from datetime import datetime

def deduplicate_and_update_progress():
    # 1. 查找所有批次Excel文件
    batch_files = sorted(glob.glob('data_batches/batch_*.xlsx'))
    
    # 2. 读取所有文件
    print(f"正在读取 {len(batch_files)} 个Excel文件...")
    file_data = {}
    for file in batch_files:
        try:
            df = pd.read_excel(file)
            file_data[file] = df
            print(f"成功读取 {file}，包含 {len(df)} 行数据")
        except Exception as e:
            print(f"读取 {file} 出错: {e}")
    
    if not file_data:
        print("没有找到有效数据文件。")
        return
    
    # 3. 记录每个唯一组合首次出现的文件
    first_occurrence = {}  # (关键词, 城市, 年份) -> 文件
    for file, df in file_data.items():
        for i, row in df.iterrows():
            key = (row['搜索关键词'], row['城市'], row['年份'])
            if key not in first_occurrence:
                first_occurrence[key] = file
    
    # 4. 过滤每个文件，只保留首次出现的条目
    total_kept = 0
    total_removed = 0
    for file, df in file_data.items():
        rows_to_keep = []
        for i, row in df.iterrows():
            key = (row['搜索关键词'], row['城市'], row['年份'])
            if first_occurrence[key] == file:
                rows_to_keep.append(True)
                total_kept += 1
            else:
                rows_to_keep.append(False)
                total_removed += 1
        
        # 更新DataFrame，只包含要保留的行
        file_data[file] = df[rows_to_keep].reset_index(drop=True)
    
    print(f"保留了 {total_kept} 条唯一记录，删除了 {total_removed} 条重复记录")
    
    # 5. 从去重后的数据创建进度JSON文件
    progress_data = {}
    now = datetime.now().isoformat()
    
    for file, df in file_data.items():
        for _, row in df.iterrows():
            key = f"{row['搜索关键词']}_{int(row['城市编号'])}_{int(row['年份'])}"
            progress_data[key] = {
                "completed_at": now,
                "word": row['搜索关键词'],
                "city_number": int(row['城市编号']),
                "year": int(row['年份'])
            }
    
    # 6. 保存更新后的进度JSON文件
    with open('crawler_progress.json', 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)
    
    print(f"更新了crawler_progress.json，包含 {len(progress_data)} 条记录")
    
    # 7. 将去重后的数据保存回原始批次文件
    for file, df in file_data.items():
        if len(df) > 0:
            df.to_excel(file, index=False)
            print(f"更新文件 {file}，去重后包含 {len(df)} 行")
        else:
            df.to_excel(file, index=False)
            print(f"文件 {file} 去重后为空（全是重复数据）")
    
    # 汇总报告
    print("\n去重完成！")
    print(f"总保留记录: {total_kept}")
    print(f"总删除重复: {total_removed}")
    print(f"更新进度文件记录数: {len(progress_data)}")

if __name__ == "__main__":
    deduplicate_and_update_progress()