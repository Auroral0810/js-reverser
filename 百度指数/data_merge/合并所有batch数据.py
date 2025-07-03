import pandas as pd
import os
import glob

def merge_excel_files():
    # 获取data_batches目录下的所有Excel文件
    excel_files = glob.glob('data_batches/batch_*.xlsx')
    
    if not excel_files:
        print("未找到Excel文件")
        return
    
    print(f"找到{len(excel_files)}个Excel文件，开始合并...")
    
    # 创建空的DataFrame列表，用于存储每个文件的数据
    dfs = []
    
    # 读取每个Excel文件并添加到列表中
    for file in excel_files:
        try:
            df = pd.read_excel(file)
            dfs.append(df)
            print(f"已读取: {file}")
        except Exception as e:
            print(f"读取{file}时出错: {e}")
    
    # 合并所有DataFrame
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"合并完成，共{len(combined_df)}行数据")
        
        # 创建输出目录
        output_dir = 'merged_results'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 按照关键词、城市、年份排序
        print("正在对数据进行排序...")
        combined_df = combined_df.sort_values(by=['搜索关键词', '城市', '年份'])
        
        # 生成统计信息
        print("正在生成统计信息...")
        
        # 统计关键词数量
        keywords = combined_df['搜索关键词'].unique()
        keyword_count = len(keywords)
        
        # 创建统计信息DataFrame
        stats_data = []
        
        # 统计每个关键词的城市数和年份数
        for keyword in keywords:
            keyword_df = combined_df[combined_df['搜索关键词'] == keyword]
            cities = keyword_df['城市'].unique()
            years = keyword_df['年份'].unique()
            city_count = len(cities)
            year_count = len(years)
            
            # 统计每个关键词每年的数据条数
            for year in years:
                year_data = keyword_df[keyword_df['年份'] == year]
                year_data_count = len(year_data)
                stats_data.append({
                    '搜索关键词': keyword,
                    '年份': year,
                    '数据条数': year_data_count,
                    '城市数量': city_count,
                    '总年份数': year_count
                })
        
        # 创建统计信息DataFrame并排序
        stats_df = pd.DataFrame(stats_data)
        stats_df = stats_df.sort_values(by=['搜索关键词', '年份'])
        
        # 将合并后的数据保存到一个总表中
        combined_df.to_excel(f"{output_dir}/全部数据.xlsx", index=False)
        print(f"已将合并后的总数据保存到 {output_dir}/全部数据.xlsx")
        
        # 保存统计信息
        stats_df.to_excel(f"{output_dir}/统计信息.xlsx", index=False)
        print(f"已将统计信息保存到 {output_dir}/统计信息.xlsx")
        
        # 输出总体统计信息
        print("\n=== 统计信息摘要 ===")
        print(f"总关键词数量: {keyword_count}")
        print(f"总数据条数: {len(combined_df)}")
        
        # 按关键词统计城市数和年份数
        keyword_stats = combined_df.groupby('搜索关键词').agg({
            '城市': 'nunique',
            '年份': 'nunique'
        }).reset_index()
        keyword_stats.columns = ['搜索关键词', '城市数量', '年份数量']
        
        print("\n关键词统计:")
        for _, row in keyword_stats.iterrows():
            print(f"关键词: {row['搜索关键词']} - 城市数: {row['城市数量']} - 年份数: {row['年份数量']}")
        
        print(f"\n处理完成，结果已保存到 {output_dir} 目录")
    else:
        print("没有成功读取任何数据")

if __name__ == "__main__":
    merge_excel_files()
