import pandas as pd
import numpy as np
import os
import re
import jieba
import jieba.posseg as pseg
from jieba.analyse import extract_tags, textrank
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from wordcloud import WordCloud
from collections import Counter, defaultdict
import networkx as nx
from tqdm import tqdm
from gensim import corpora, models
import json
import warnings
warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

def load_cleaned_data(file_path):
    """
    加载清洗后的数据
    
    参数:
        file_path: 清洗后数据的文件路径
    
    返回:
        加载的数据框
    """
    print(f"正在加载清洗后的数据: {file_path}")
    df = pd.read_csv(file_path, encoding='utf-8')
    print(f"数据加载完成，共 {df.shape[0]} 行, {df.shape[1]} 列")
    return df

def build_custom_dict(df, output_dir, min_freq=5):
    """
    构建社区特定词典
    
    参数:
        df: 数据框
        output_dir: 输出目录
        min_freq: 最小词频
    
    返回:
        社区特定词典
    """
    print("正在构建社区特定词典...")
    
    # 合并所有评论内容
    all_text = ' '.join(df['内容'].fillna('').astype(str).tolist())
    
    # 使用正则表达式提取可能的社区特定词
    # 1. 提取表情符号
    emoticons = re.findall(r'\[.*?\]', all_text)
    emoticon_counts = Counter(emoticons)
    
    # 2. 提取网络用语特征模式
    # 例如重复的字符、特殊标点组合等
    repeated_chars = re.findall(r'([a-zA-Z\u4e00-\u9fa5])\1{2,}', all_text)  # 连续重复字符
    special_marks = re.findall(r'[！!]{2,}|[？?]{2,}|[。.]{2,}', all_text)  # 连续标点符号
    
    # 3. 提取可能的梗词 (通常是3-6个字的组合)
    potential_memes = []
    segments = [seg for seg in re.split(r'[，。！？,.!?]', all_text) if len(seg) > 2]
    for seg in segments:
        # 提取可能的3-6字组合
        for i in range(len(seg)-2):
            for j in range(3, min(7, len(seg)-i+1)):
                phrase = seg[i:i+j]
                if re.match(r'^[\u4e00-\u9fa5a-zA-Z]+$', phrase):  # 仅包含中文和英文
                    potential_memes.append(phrase)
    
    meme_counts = Counter(potential_memes)
    
    # 创建社区词典
    community_dict = {}
    
    # 添加高频表情符号
    for emoticon, count in emoticon_counts.most_common():
        if count >= min_freq:
            community_dict[emoticon] = count
    
    # 添加可能的梗词
    for meme, count in meme_counts.most_common(300):  # 取频率最高的300个可能梗词
        if count >= min_freq:
            community_dict[meme] = count
    
    # 使用TextRank和TF-IDF提取关键词，作为补充
    textrank_keywords = textrank(all_text, topK=200, allowPOS=('ns', 'n', 'vn', 'v', 'a'))
    tfidf_keywords = extract_tags(all_text, topK=200)
    
    for keyword in set(textrank_keywords + tfidf_keywords):
        if keyword not in community_dict and len(keyword) > 1:
            community_dict[keyword] = 1  # 默认权重
    
    # 保存社区词典
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存为文本文件 (jieba格式)
    with open(f"{output_dir}/community_dict.txt", 'w', encoding='utf-8') as f:
        for word, freq in community_dict.items():
            if len(word.strip()) > 0:  # 确保不写入空词
                f.write(f"{word} {freq}\n")
    
    # 保存为JSON格式 (更易于人类阅读)
    with open(f"{output_dir}/community_dict.json", 'w', encoding='utf-8') as f:
        json.dump(community_dict, f, ensure_ascii=False, indent=2)
    
    print(f"社区词典构建完成，共包含 {len(community_dict)} 个词条")
    return community_dict

def load_stopwords(stopwords_file="停用词.txt"):
    """
    加载停用词表
    
    参数:
        stopwords_file: 停用词文件路径
    
    返回:
        停用词集合
    """
    print("正在加载停用词表...")
    stopwords = set()
    
    # 加载停用词文件
    if os.path.exists(stopwords_file):
        try:
            with open(stopwords_file, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        stopwords.add(word)
            print(f"成功加载停用词文件: {stopwords_file}，加载了 {len(stopwords)} 个停用词")
        except Exception as e:
            print(f"加载停用词文件失败: {e}")
    else:
        print(f"警告: 停用词文件不存在: {stopwords_file}")
    
    # 添加标点符号、数字和特殊字符到停用词
    punctuation_stopwords = set('，。！？：；''""【】《》（）、,.!?:;\'"[]()<>/')
    digit_stopwords = set('0123456789０１２３４５６７８９')
    special_chars = set('_~`@#$%^&*+=|\\')
    
    # 合并所有停用词
    stopwords = stopwords.union(punctuation_stopwords).union(digit_stopwords).union(special_chars)
    
    print(f"停用词加载完成，共 {len(stopwords)} 个停用词")
    return stopwords

def segment_text(df, community_dict_path, stopwords, output_dir):
    """
    对文本进行分词和词性标注
    
    参数:
        df: 数据框
        community_dict_path: 社区词典路径
        stopwords: 停用词集合
        output_dir: 输出目录
    
    返回:
        包含分词结果的数据框
    """
    print("正在进行文本分词与词性标注...")
    
    # 加载社区词典
    jieba.load_userdict(community_dict_path)
    
    # 定义预处理函数
    def preprocess_text(text):
        """文本预处理，清理标点符号和特殊字符"""
        if pd.isna(text) or text == '':
            return ''
        
        text = str(text)
        
        # 替换URL
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '[URL]', text)
        
        # 替换连续空格为单个空格
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    # 定义分词函数
    def segment(text):
        if pd.isna(text) or text == '':
            return [], []
        
        # 预处理文本
        text = preprocess_text(text)
        
        # 分词并标注词性
        words_pos = pseg.cut(text)
        
        # 过滤停用词和短词，提取词和词性
        filtered_words = []
        pos_tags = []
        
        # 实质性内容词性
        content_pos = {'n', 'v', 'a', 'vn', 'an', 'ns', 'nr', 'nz', 'nt'}
        
        for word, pos in words_pos:
            # 过滤停用词、空词，并优先保留多字词或实质性词汇
            if (word not in stopwords and len(word.strip()) > 0 and
                (len(word) > 1 or pos in content_pos)):
                filtered_words.append(word)
                pos_tags.append(pos)
        
        return filtered_words, pos_tags
    
    # 应用分词函数
    print("正在处理评论内容...")
    
    # 创建结果列
    df['分词结果'] = None
    df['词性标注'] = None
    
    # 使用tqdm显示进度
    tqdm.pandas(desc="分词进度")
    
    # 对非空内容进行分词
    segmented_data = df['内容'].fillna('').progress_apply(segment)
    
    # 分离词和词性到不同列
    df['分词结果'] = segmented_data.apply(lambda x: x[0])
    df['词性标注'] = segmented_data.apply(lambda x: x[1])
    
    # 保存分词结果
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存为CSV
    segmented_df = df[['ID', '内容', '分词结果', '词性标注']]
    segmented_df.to_csv(f"{output_dir}/segmented_comments.csv", index=False, encoding='utf-8')
    
    # 创建分词统计
    word_counter = Counter()
    for words in df['分词结果']:
        word_counter.update(words if isinstance(words, list) else [])
    
    # 保存词频统计
    word_freq = pd.DataFrame({
        '词': list(word_counter.keys()),
        '频率': list(word_counter.values())
    }).sort_values('频率', ascending=False)
    
    word_freq.to_csv(f"{output_dir}/word_frequency.csv", index=False, encoding='utf-8')
    
    print(f"文本分词完成，共处理 {len(df)} 条评论，发现 {len(word_counter)} 个唯一词汇")
    return df

def extract_text_features(df, output_dir):
    """
    提取文本特征
    
    参数:
        df: 包含分词结果的数据框
        output_dir: 输出目录
    
    返回:
        特征提取结果
    """
    print("正在提取文本特征...")
    
    # 将分词结果转换为文本
    df['分词文本'] = df['分词结果'].apply(lambda x: ' '.join(x) if isinstance(x, list) else '')
    
    # 创建词袋模型
    print("构建词袋模型...")
    count_vectorizer = CountVectorizer(max_features=5000)
    count_matrix = count_vectorizer.fit_transform(df['分词文本'].fillna(''))
    
    # 创建TF-IDF模型
    print("构建TF-IDF模型...")
    tfidf_vectorizer = TfidfVectorizer(max_features=5000)
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['分词文本'].fillna(''))
    
    # 创建Gensim词典和语料库
    print("构建Gensim词典和语料库...")
    texts = [words for words in df['分词结果'] if isinstance(words, list)]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    
    # 生成词特征映射
    feature_names = count_vectorizer.get_feature_names_out()
    
    # 保存特征提取结果
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存词典和语料库
    dictionary.save(f"{output_dir}/gensim_dictionary.dict")
    corpora.MmCorpus.serialize(f"{output_dir}/gensim_corpus.mm", corpus)
    
    # 保存向量化器
    with open(f"{output_dir}/count_vectorizer.pkl", 'wb') as f:
        import pickle
        pickle.dump(count_vectorizer, f)
    
    with open(f"{output_dir}/tfidf_vectorizer.pkl", 'wb') as f:
        import pickle
        pickle.dump(tfidf_vectorizer, f)
    
    # 保存部分TF-IDF结果用于检查
    tfidf_df = pd.DataFrame(
        tfidf_matrix.toarray()[:100, :50],  # 取前100条评论，前50个特征
        columns=feature_names[:50]
    )
    tfidf_df.to_csv(f"{output_dir}/tfidf_sample.csv", index=False)
    
    # 返回特征提取结果
    features = {
        'count_vectorizer': count_vectorizer,
        'count_matrix': count_matrix,
        'tfidf_vectorizer': tfidf_vectorizer,
        'tfidf_matrix': tfidf_matrix,
        'dictionary': dictionary,
        'corpus': corpus,
        'feature_names': feature_names
    }
    
    print("文本特征提取完成")
    return features

def exploratory_text_analysis(df, features, output_dir):
    """
    探索性文本分析
    
    参数:
        df: 包含分词结果的数据框
        features: 特征提取结果
        output_dir: 输出目录
    """
    print("正在进行探索性文本分析...")
    
    # 创建输出目录
    viz_dir = f"{output_dir}/visualizations"
    os.makedirs(viz_dir, exist_ok=True)
    
    # 1. 词频分析
    print("正在进行词频分析...")
    
    # 获取词频统计
    all_words = []
    for words in df['分词结果']:
        if isinstance(words, list):
            all_words.extend(words)
    
    word_counts = Counter(all_words)
    
    # 过滤词频统计中的低价值词
    filtered_word_counts = {}
    for word, count in word_counts.items():
        # 保留长度大于1的词以避免单字干扰
        if len(word) > 1:
            filtered_word_counts[word] = count
    
    # 如果过滤后的词典为空，则回退到原词典
    if not filtered_word_counts:
        print("警告: 过滤后词典为空，使用原始词典")
        filtered_word_counts = word_counts
    
    # 获取前50个高频词
    top_words = sorted(filtered_word_counts.items(), key=lambda x: x[1], reverse=True)[:50]
    
    # 创建词频柱状图
    plt.figure(figsize=(15, 8))
    
    # 提取词和频率
    words = [word for word, count in top_words[:20]]  # 只展示前20个
    counts = [count for word, count in top_words[:20]]
    
    # 创建条形图
    bars = plt.bar(range(len(words)), counts, color='skyblue')
    plt.xticks(range(len(words)), words, rotation=45, ha='right')
    plt.title('Top 20 词频统计')
    plt.xlabel('词语')
    plt.ylabel('频率')
    plt.tight_layout()
    plt.savefig(f"{viz_dir}/top_words_frequency.png")
    plt.close()
    
    # 2. 词云可视化
    print("正在生成词云...")
    
    # 准备词频数据
    word_freq = {word: count for word, count in filtered_word_counts.items()}
    
    # 尝试找到系统可用字体
    system_fonts = []
    
    # 检查常见字体位置
    potential_font_paths = [
        # macOS常见中文字体
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/Library/Fonts/Arial Unicode.ttf',
        # Windows常见中文字体
        'C:/Windows/Fonts/simhei.ttf',
        'C:/Windows/Fonts/msyh.ttc',
        # Linux常见中文字体
        '/usr/share/fonts/truetype/arphic/uming.ttc',
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
    ]
    
    # 添加用户当前目录下的字体文件
    local_fonts = [
        'simhei.ttf', 
        'msyh.ttc', 
        'simsun.ttc', 
        'SimHei.ttf', 
        'SimSun.ttf'
    ]
    for font in local_fonts:
        if os.path.exists(font):
            potential_font_paths.append(font)
    
    # 检查哪些字体文件存在
    for font_path in potential_font_paths:
        if os.path.exists(font_path):
            system_fonts.append(font_path)
            print(f"找到可用字体: {font_path}")
    
    # 如果没有找到字体，尝试使用matplotlib的内置字体
    if not system_fonts:
        try:
            import matplotlib.font_manager as fm
            system_fonts = [f.path for f in fm.fontManager.ttflist if 'simhei' in f.name.lower() or 'heiti' in f.name.lower() or 'yahei' in f.name.lower()]
            if system_fonts:
                print(f"找到matplotlib内置字体: {system_fonts[0]}")
        except:
            print("未找到matplotlib内置字体")
    
    # 生成词云
    try:
        # 尝试使用找到的字体
        if system_fonts:
            print(f"使用字体生成词云: {system_fonts[0]}")
            wordcloud = WordCloud(
                font_path=system_fonts[0],
                width=800,
                height=500,
                background_color='white',
                max_words=200,
                collocations=False,  # 避免显示重复词汇组合
                min_font_size=10,
                max_font_size=150,
                random_state=42
            ).generate_from_frequencies(word_freq)
        else:
            # 如果没有找到合适的字体，尝试不指定字体路径
            print("未找到合适字体，使用默认字体生成词云")
            wordcloud = WordCloud(
                width=800,
                height=500,
                background_color='white',
                max_words=200,
                collocations=False,
                min_font_size=10,
                max_font_size=150,
                random_state=42
            ).generate_from_frequencies(word_freq)
        
        # 显示词云
        plt.figure(figsize=(12, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f"{viz_dir}/word_cloud.png", dpi=300)
        plt.close()
        print("词云生成成功，保存至:", f"{viz_dir}/word_cloud.png")
        
        # 保存词云原始数据用于后续分析
        with open(f"{viz_dir}/wordcloud_data.json", 'w', encoding='utf-8') as f:
            # 将Counter转换为字典后保存
            json.dump({word: count for word, count in top_words}, f, ensure_ascii=False, indent=2)
        
    except Exception as e:
        print(f"生成词云失败，错误: {e}")
    
    # 3. 词共现网络分析
    print("正在进行词共现分析...")
    
    # 创建共现矩阵
    co_occurrence = defaultdict(int)
    
    # 对每条评论的分词结果，统计词共现频率
    for words in df['分词结果']:
        if isinstance(words, list) and len(words) > 1:
            # 只考虑出现频率较高的词
            filtered_words = [w for w in words if word_counts[w] > 10]
            # 统计共现
            for i in range(len(filtered_words)):
                for j in range(i+1, len(filtered_words)):
                    word_pair = tuple(sorted([filtered_words[i], filtered_words[j]]))
                    co_occurrence[word_pair] += 1
    
    # 创建网络图
    G = nx.Graph()
    
    # 添加节点和边
    for (word1, word2), weight in sorted(co_occurrence.items(), key=lambda x: x[1], reverse=True)[:100]:
        if weight > 5:  # 只保留权重大于5的边
            G.add_edge(word1, word2, weight=weight)
    
    # 根据权重计算节点大小
    node_size = {node: sum(data['weight'] for _, _, data in G.edges(node, data=True)) for node in G.nodes()}
    sizes = [node_size[node] * 10 for node in G.nodes()]
    
    # 绘制网络图
    plt.figure(figsize=(15, 15))
    pos = nx.spring_layout(G, k=0.4)  # k影响节点间斥力
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color='lightblue', alpha=0.8)
    
    # 绘制边，边的粗细表示权重
    edge_weights = [G[u][v]['weight']/5 for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.5, edge_color='gray')
    
    # 绘制标签
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='SimHei')
    
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f"{viz_dir}/word_co_occurrence_network.png", dpi=300)
    plt.close()
    
    # 4. 简单主题分析
    print("正在进行初步主题分析...")
    
    # 使用LDA进行主题建模
    lda_model = models.LdaModel(
        corpus=features['corpus'],
        id2word=features['dictionary'],
        num_topics=10,
        passes=10,
        alpha='auto'
    )
    
    # 保存主题模型
    lda_model.save(f"{output_dir}/lda_model.model")
    
    # 提取主题关键词
    topics_keywords = []
    for topic_id in range(10):
        top_words = lda_model.show_topic(topic_id, topn=15)
        topics_keywords.append([word for word, _ in top_words])
    
    # 创建主题关键词可视化
    fig, axes = plt.subplots(5, 2, figsize=(15, 20))
    axes = axes.flatten()
    
    for i, topic_words in enumerate(topics_keywords):
        ax = axes[i]
        y_pos = range(len(topic_words))
        
        # 获取权重
        topic_weights = [weight for _, weight in lda_model.show_topic(i, topn=15)]
        
        ax.barh(y_pos, topic_weights, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(topic_words)
        ax.invert_yaxis()  # 最大值在顶部
        ax.set_title(f'主题 #{i+1}')
        ax.set_xlabel('权重')
    
    plt.tight_layout()
    plt.savefig(f"{viz_dir}/lda_topics.png")
    plt.close()
    
    # 替换 pyecharts 饼图为 matplotlib 饼图
    topic_dist = [lda_model.get_document_topics(bow) for bow in features['corpus'][:1000]]  # 取前1000条
    
    # 计算每个主题的总权重
    topic_weights = np.zeros(10)
    for doc_topics in topic_dist:
        for topic_id, weight in doc_topics:
            topic_weights[topic_id] += weight
    
    # 归一化
    topic_weights = topic_weights / topic_weights.sum()
    
    # 创建主题分布饼图
    plt.figure(figsize=(10, 10))
    plt.pie(topic_weights, labels=[f'主题{i+1}' for i in range(10)], 
            autopct='%1.1f%%', startangle=90, shadow=True)
    plt.axis('equal')
    plt.title('主题分布')
    plt.savefig(f"{viz_dir}/topic_distribution.png")
    plt.close()
    
    # 创建文本分析报告
    print("正在生成文本分析报告...")
    
    with open(f"{output_dir}/text_analysis_report.md", 'w', encoding='utf-8') as f:
        f.write("# 孙笑川吧评论文本分析报告\n\n")
        
        f.write("## 1. 基本词频统计\n\n")
        f.write("### 1.1 最常用词汇\n\n")
        f.write("| 排名 | 词语 | 出现频率 |\n")
        f.write("|------|------|----------|\n")
        for rank, (word, count) in enumerate(top_words[:30], 1):
            f.write(f"| {rank} | {word} | {count} |\n")
        
        f.write("\n## 2. 词性分布\n\n")
        
        # 统计词性分布
        pos_counter = Counter()
        for pos_tags in df['词性标注']:
            if isinstance(pos_tags, list):
                pos_counter.update(pos_tags)
        
        f.write("| 词性 | 数量 | 占比 |\n")
        f.write("|------|------|------|\n")
        total_pos = sum(pos_counter.values())
        for pos, count in pos_counter.most_common(10):
            f.write(f"| {pos} | {count} | {count/total_pos*100:.2f}% |\n")
        
        f.write("\n## 3. 主题分析\n\n")
        f.write("### 3.1 识别出的10个主题及其关键词\n\n")
        
        for i, keywords in enumerate(topics_keywords, 1):
            f.write(f"**主题{i}**: {', '.join(keywords[:10])}\n\n")
        
        f.write("\n## 4. 社区特定表达\n\n")
        f.write("### 4.1 可能的梗和特殊表达\n\n")
        
        # 加载社区词典
        try:
            with open(f"{output_dir}/../text_preprocessing/community_dict.json", 'r', encoding='utf-8') as dict_file:
                community_dict = json.load(dict_file)
                
            # 筛选出高频的社区特定词
            top_community_words = sorted(community_dict.items(), key=lambda x: x[1], reverse=True)[:50]
            
            f.write("| 表达 | 频率 |\n")
            f.write("|------|------|\n")
            for word, freq in top_community_words:
                f.write(f"| {word} | {freq} |\n")
        except:
            # 如果找不到词典文件，使用词频统计作为替代
            f.write("无法加载社区词典，使用词频统计代替\n\n")
            f.write("| 表达 | 频率 |\n")
            f.write("|------|------|\n")
            for word, count in top_words[:50]:
                f.write(f"| {word} | {count} |\n")
        
        f.write("\n## 5. 评论长度分析\n\n")
        
        # 评论长度统计
        comment_lengths = df['分词结果'].apply(lambda x: len(x) if isinstance(x, list) else 0)
        mean_length = comment_lengths.mean()
        median_length = comment_lengths.median()
        
        f.write(f"- 平均词数: {mean_length:.2f}\n")
        f.write(f"- 中位数词数: {median_length:.0f}\n")
        f.write(f"- 最长评论词数: {comment_lengths.max()}\n")
        f.write(f"- 词数小于5的评论占比: {(comment_lengths < 5).mean()*100:.2f}%\n\n")
        
        f.write("## 6. 初步发现\n\n")
        f.write("1. 社区语言特点显著，存在大量特定表达方式\n")
        f.write("2. 评论普遍简短，表达方式直接\n")
        f.write("3. [待分析具体主题特点...]\n")
        f.write("4. [待分析可能的梗文化特征...]\n")
    
    print("探索性文本分析完成!")

def main(input_file, output_dir='./output'):
    """
    主函数
    
    参数:
        input_file: 清洗后数据的文件路径
        output_dir: 输出目录
    """
    # 1. 加载清洗后的数据
    df = load_cleaned_data(input_file)
    
    # 创建子目录
    text_preprocessing_dir = f"{output_dir}/text_preprocessing"
    os.makedirs(text_preprocessing_dir, exist_ok=True)
    
    # 2. 构建社区特定词典
    community_dict = build_custom_dict(df, text_preprocessing_dir)
    
    # 3. 加载停用词
    stopwords = load_stopwords()
    
    # 4. 文本分词与词性标注
    segmented_df = segment_text(df, f"{text_preprocessing_dir}/community_dict.txt", stopwords, text_preprocessing_dir)
    
    # 5. 提取文本特征
    features = extract_text_features(segmented_df, text_preprocessing_dir)
    
    # 6. 探索性文本分析
    exploratory_text_analysis(segmented_df, features, text_preprocessing_dir)
    
    print("文本预处理与特征提取完成!")
    return segmented_df, features

if __name__ == "__main__":
    # 设置输入文件路径和输出目录
    input_file = "data_preprocessing/cleaned_data.csv"  # 第一步清洗后的数据文件路径
    output_dir = "output"
    
    # 执行主函数
    segmented_df, features = main(input_file, output_dir)
    
    print("\n文本预处理与特征提取完成，可以进行下一步分析了!")
