import requests
import time
import pandas as pd
from datetime import datetime
import json
import os
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from functools import wraps
from fake_useragent import UserAgent
import execjs
ua = UserAgent()
useragent=ua.random#随机生成谷歌浏览器的useragent，想要各种浏览器的改chrome为randome


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 配置参数
CONFIG = {
    'batch_size': 100,  # 每批次保存的记录数
    'max_workers': 6,  # 并发线程数
    'retry_times': 3,  # 重试次数
    'base_delay': 1,  # 基础延迟时间（秒）
    'max_delay': 1.5,    # 最大延迟时间（秒）
    'progress_file': 'crawler_progress.json',  # 进度文件
    'output_dir': 'data_batches',  # 批次数据目录
    'final_output': '百度指数_全部关键词.xlsx',  # 最终输出文件
    'use_local_ip': True  # 是否使用本地IP
}


# 线程锁
progress_lock = threading.Lock()
batch_lock = threading.Lock()

# 全局变量
current_batch_data = []
processed_count = 0

# 重试装饰器
def retry(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"函数 {func.__name__} 重试 {max_retries} 次后仍然失败: {e}")
                        raise e
                    else:
                        wait_time = delay * (2 ** attempt) + random.uniform(0, 1)
                        logger.warning(f"函数 {func.__name__} 第 {attempt + 1} 次尝试失败: {e}，等待 {wait_time:.2f} 秒后重试")
                        time.sleep(wait_time)
            return None
        return wrapper
    return decorator

# 进度管理类
class ProgressManager:
    def __init__(self, progress_file):
        self.progress_file = progress_file
        self.progress = self.load_progress()
    
    def load_progress(self):
        """加载进度"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                logger.warning("进度文件损坏，重新开始")
        return {}
    
    def save_progress(self):
        """保存进度"""
        with progress_lock:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress, f, ensure_ascii=False, indent=2)
    
    def is_completed(self, word, city_number, year):
        """检查任务是否已完成"""
        key = f"{word}_{city_number}_{year}"
        return key in self.progress
    
    def mark_completed(self, word, city_number, year):
        """标记任务完成"""
        key = f"{word}_{city_number}_{year}"
        self.progress[key] = {
            'completed_at': datetime.now().isoformat(),
            'word': word,
            'city_number': city_number,
            'year': year
        }
        self.save_progress()

# 批次数据管理
class BatchManager:
    def __init__(self, output_dir, batch_size):
        self.output_dir = output_dir
        self.batch_size = batch_size
        self.current_batch = []
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 检查已有批次文件，确定起始批次号
        self.batch_count = self._get_max_batch_number()
        logger.info(f"批次管理初始化，从批次 {self.batch_count + 1} 开始")
    
    def _get_max_batch_number(self):
        """获取已有批次文件的最大批次号"""
        max_batch = 0
        if os.path.exists(self.output_dir):
            batch_files = []
            for file in os.listdir(self.output_dir):
                if file.startswith('batch_') and file.endswith('.xlsx'):
                    try:
                        # 从文件名提取批次号
                        batch_num = int(file.split('_')[1].split('.')[0])
                        batch_files.append(batch_num)
                    except:
                        pass
            
            if batch_files:
                max_batch = max(batch_files)
                logger.info(f"检测到已有批次文件，最大批次号: {max_batch}")
        
        return max_batch
    
    def add_data(self, df):
        """添加数据到当前批次"""
        with batch_lock:
            self.current_batch.append(df)
            
            if len(self.current_batch) >= self.batch_size:
                self.save_current_batch()
    
    def save_current_batch(self):
        """保存当前批次数据"""
        if not self.current_batch:
            return
        
        try:
            combined_df = pd.concat(self.current_batch, ignore_index=True)
            self.batch_count += 1
            batch_file = os.path.join(self.output_dir, f'batch_{self.batch_count:04d}.xlsx')
            combined_df.to_excel(batch_file, index=False)
            
            logger.info(f"批次 {self.batch_count} 已保存，包含 {len(combined_df)} 条记录")
            self.current_batch = []
            
        except Exception as e:
            logger.error(f"保存批次数据失败: {e}")
    
    def save_final_batch(self):
        """保存最后一个批次"""
        if self.current_batch:
            # 强制保存当前批次，即使不满batch_size
            try:
                combined_df = pd.concat(self.current_batch, ignore_index=True)
                self.batch_count += 1
                batch_file = os.path.join(self.output_dir, f'batch_{self.batch_count:04d}.xlsx')
                combined_df.to_excel(batch_file, index=False)
                
                logger.info(f"最终批次 {self.batch_count} 已保存，包含 {len(combined_df)} 条记录")
                self.current_batch = []
                
            except Exception as e:
                logger.error(f"保存最终批次数据失败: {e}")
    
    def merge_all_batches(self, final_output):
        """合并所有批次文件"""
        try:
            batch_files = []
            for file in os.listdir(self.output_dir):
                if file.startswith('batch_') and file.endswith('.xlsx'):
                    batch_files.append(os.path.join(self.output_dir, file))
            
            if not batch_files:
                logger.warning("没有找到批次文件")
                return False
            
            # 按文件名排序
            batch_files.sort()
            
            all_data = []
            for batch_file in batch_files:
                try:
                    df = pd.read_excel(batch_file)
                    all_data.append(df)
                    logger.info(f"读取批次文件: {batch_file}, 记录数: {len(df)}")
                except Exception as e:
                    logger.error(f"读取批次文件失败 {batch_file}: {e}")
            
            if all_data:
                final_df = pd.concat(all_data, ignore_index=True)
                final_df.to_excel(final_output, index=False)
                logger.info(f"所有数据已合并保存到 {final_output}，总记录数: {len(final_df)}")
                return True
            
        except Exception as e:
            logger.error(f"合并批次文件失败: {e}")
            return False

# 请求频率控制
class RateLimiter:
    def __init__(self, min_delay=1, max_delay=1.5):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request_time = 0
        self.lock = threading.Lock()
    
    def wait(self):
        """等待适当的时间间隔"""
        with self.lock:
            current_time = time.time()
            elapsed = current_time - self.last_request_time
            
            delay = random.uniform(self.min_delay, self.max_delay)
            if elapsed < delay:
                sleep_time = delay - elapsed
                time.sleep(sleep_time)
            
            self.last_request_time = time.time()

# 全局速率限制器
rate_limiter = RateLimiter(CONFIG['base_delay'], CONFIG['max_delay'])

# 代理管理类
class ProxyManager:
    def __init__(self, proxy_list, use_local_ip=True):
        # 如果use_local_ip为True，则添加None作为本地IP选项
        self.proxy_list = proxy_list
        if use_local_ip:
            self.proxy_list.append(None)  # None表示使用本地IP
        self.current_index = 0
        self.lock = threading.Lock()
    
    def get_proxy(self):
        """获取一个代理"""
        with self.lock:
            proxy = self.proxy_list[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxy_list)
            return proxy

# 添加Cookie管理类
class CookieManager:
    def __init__(self, cookie_list):
        self.cookie_list = cookie_list
        self.current_index = 0
        self.lock = threading.Lock()
    
    def get_cookie(self):
        """获取一个Cookie"""
        with self.lock:
            cookie = self.cookie_list[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.cookie_list)
            return cookie

# 请求数据
@retry(max_retries=CONFIG['retry_times'])
def get_data(city_number, word, startDate, endDate, cookies, proxy_manager=None, cookie_manager=None):
    """获取百度指数数据"""
    # 频率控制
    rate_limiter.wait()
    
    # 如果提供了cookie_manager，则使用它来获取cookie
    if cookie_manager:
        cookies = cookie_manager.get_cookie()
    
    # 构建请求URL
    url = f'https://index.baidu.com/api/SearchApi/index?area={city_number}&word=[[{{"name":"{word}","wordType":1}}]]&startDate={startDate}&endDate={endDate}'
    
    url_cipyter = f'https://index.baidu.com/v2/main/index.html#/trend/{word}?words={word}'

    with open('Cipher-Text.js', 'r') as f:
        js = f.read()
        ctx = execjs.compile(js)
    cipyer_text=ctx.call('ascToken',url_cipyter)
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Cipher-Text': cipyer_text,
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://index.baidu.com/v2/main/index.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': useragent,
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
    
    # 获取代理配置
    proxies = None
    if proxy_manager:
        proxies = proxy_manager.get_proxy()
        
    # 记录当前使用的代理和cookie
    # proxy_info = "本地IP" if proxies is None else str(proxies)
    # logger.info(f"请求 {word} - {city_number} - {startDate} 使用代理: {proxy_info}")

    # 发送请求
    response = requests.get(url, cookies=cookies, headers=headers, proxies=proxies, timeout=20)
    response.raise_for_status()  # 抛出HTTP错误
    
    return response.json()

# 分析数据
def analyze_data(data, city_number, city_name, word, year):
    """分析百度指数数据"""
    try:
        # 获取统计数据
        generalRatio_all_avg = data['data']['generalRatio'][0]['all']['avg'] # 整体日均值
        generalRatio_wise_avg = data['data']['generalRatio'][0]['wise']['avg'] # 移动日均值
        generalRatio_pc_avg = data['data']['generalRatio'][0]['pc']['avg'] # PC日均值

        # 计算年份的天数
        def get_days_in_year(year):
            if year == 2025:  # 2025年只统计到6月23日
                return (datetime(2025, 6, 23) - datetime(2025, 1, 1)).days + 1
            elif (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):  # 闰年
                return 366
            else:  # 平年
                return 365
        
        # 获取当前年份的天数
        days_in_year = get_days_in_year(year)
        
        # 创建数据框
        df = pd.DataFrame({
            '搜索关键词': [word],
            '城市': [city_name],
            '城市编号': [city_number],
            '年份': [year],
            '整体日均值': [generalRatio_all_avg],
            '移动日均值': [generalRatio_wise_avg],
            'PC日均值': [generalRatio_pc_avg],
            '整体年总值': [generalRatio_all_avg * days_in_year],
            '移动年总值': [generalRatio_wise_avg * days_in_year],
            'PC年总值': [generalRatio_pc_avg * days_in_year],
            '爬取时间': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        })
        
        return df
        
    except Exception as e:
        logger.error(f"数据解析错误: {e}, 原始数据: {data}")
        return pd.DataFrame()

# 处理单个任务
def process_single_task(task_info):
    """处理单个爬取任务"""
    word, city_number, city_name, year, progress_manager, batch_manager, proxy_manager, cookie_manager = task_info
    
    try:
        # 检查是否已完成
        if progress_manager.is_completed(word, city_number, year):
            logger.info(f"跳过已完成任务: {word} - {city_name} - {year}")
            return True
        
        # 构建日期
        startDate = f"{year}-01-01"
        endDate = f"{year}-12-31"
        if year == 2025:
            endDate = "2025-06-23"
        
        logger.info(f"开始处理: {word} - {city_name} - {year}")
        
        # 获取数据，使用代理管理器和Cookie管理器
        data = get_data(city_number, word, startDate, endDate, None, proxy_manager, cookie_manager)
        
        # 分析数据
        df = analyze_data(data, city_number, city_name, word, year)
        
        if not df.empty:
            # 添加到批次管理器
            batch_manager.add_data(df)
            
            # 标记完成
            progress_manager.mark_completed(word, city_number, year)
            
            logger.info(f"完成处理: {word} - {city_name} - {year}")
            return True
        else:
            logger.warning(f"数据为空: {word} - {city_name} - {year}")
            return False
            
    except Exception as e:
        logger.error(f"处理任务失败: {word} - {city_name} - {year}, 错误: {e}")
        return False

def main():
    """主函数"""
    try:
        cookies_list = [
        #     {
        #     'BAIDU_WISE_UID': 'wapp_1744869667916_527',
        #     'BAIDUID': 'FF85DF65CC7463F3726D5301B69C0672:FG=1',
        #     'BAIDUID_BFESS': 'FF85DF65CC7463F3726D5301B69C0672:FG=1',
        #     'PSTM': '1744882843',
        #     'BIDUPSID': '950D047CF79B4A0F8F86462CD08D849F',
        #     'ZFY': ':AYs:BOm:Ajfa1cQtiOrSJADVlDld3:BYmMcahDksItTkOQ:C',
        #     'H_PS_PSSID': '61027_62325_62485_62967_63042_63044_63140_63074_63189_63194_63210_63226_63242_63244_63249_63253',
        #     '__bid_n': '18c42450fcc02886ca93f5',
        #     'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750687271',
        #     'HMACCOUNT': 'DDF927EE5DF25454',
        #     'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihdwitHd04Lvs3Nfz26Zt2holplnIKVacidp8Sue4dMTyfg65BJnOFhn1HthtSiwtygiD7piS4vjG/W9dLb1VAdqMysqdImJFnhAMv/fWi1I5VO0V6uxgO+hV7+7wZFfXG0MSpuMmh7GsZ4C7fF/kTgmvlMIA/tB2qdnJ8KkulgesR5YKU+qTqtaaBkWIZO5dn/GldC1S4QUhUhpm5KMoOoF81v2iwj13daM+9aWJ5GJCQM+RpBohGNhMcqCHhVhtXpVObaDCHgWJZH3ZrTGYHmi7XJB9z3y2o8Kqxep5XBCsugNOW5C73e/g54kuY4PKIS71bGmnPunNtMIatWdCpBi6yoMEZCNh1huwbMdWwuuXVnvNXIEW2pwj4BXINSNFrPKCGZHtLbt/i6efsLSLARZuIGhYqrYfhHGZqJNx2uWmglAIQEZY21OyYDgpfKN3zxRn6ONqHK83MkBENWBMWSAwea/+1VSNUTGfIG+NKu2s+g28sOzjnLUnUE9KukMAMTPZYfT79sbFYuntY0Ry6GX3OsRAJVdXPXKlPRQiighN2h3utZNfUsAGL2WWa3tubT9td9rGfOenGkLOGCRladXTg1IKPDQ9z3/DiqHtAIbmyu3emEg6nEYu6lQuvYr6/UJpAq7e+CnVRC2DzwICP6cu9A5mNm34ZPuoRV+zY3FkhMa5PpAytGwAf1nqFDiyU+WHcGDy5llZtI5Ig4rvXzcdIxeODdssbd+W/AgOwxO3JdRGSluqM4FuAgHCvdnqfGnnbe3vsHq3LuF7pombT65cVprejPaivGVaWugm+VA1kVl5OE/aBXOg67P9UlCyJKVyutwgoMp5Aa/ZkjblrEvPdXZFhAgvw25kAwV0TwSXSe5Q/vbh3nl529wNGdJ0E/Al3XsmHJdLSZ9wC3mJe+ZNDrSwzO8uzPTGJRstuhQcx/x5a3E+Qkao4W1aMhW15Bgywf8BpImierD5YuJm8aNh+b2nRqUTK6NqmhPLvsfMNxShTXBRJdrnFL9nqFcSvY6cuLQt09VwaPPyWktx1V5J+b2nRqUTK6NqmhPLvsfMNZ/k8RFFJMWot30FNQcvJjgmLcRAsZA9ozVp4fEbVslkfSzVKL8rDNNpNjO7rOJCKUwXtmNU/nsKC0PSzAP3Kq4wL4SK3t1tHw4eMSEHL2FCmmrSArB56dw/GBL+N3SuP',
        #     'BDUSS': 'DdGSGdNNUR1bDR2OGdxUU90UE1yZndIRTFEaURSNGNBbXJscXdvWFpMR3M4SUZvSUFBQUFBJCQAAAAAAAAAAAEAAAA72va1yOvEpzg4NgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKxjWmisY1poc',
        #     'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05007666700aotgStKPrY9%2ByDdcKStvWFxvkzgQYr%2Bg84RLwAZGMbj%2FF%2Fu66amlm1lDr3cjP9tg0rCzjxsXcWmRR2tx9I9DDUFPFoGZGrQ%2F6TZ9L3TejNjavrG8nfYC3tt8Z14o9bShwFXz2j2Z7D3NYcEOF8%2FCsv3BOEtk4Z0pHO3j2MHwF0VIElDOzipxIQIhOnEB393eYX9AKcgaUswjfgyqOSa1PD05JzeLRWYhmTixYiOM6MGATtQRnJ%2Bll%2Fp5xczf2rbwz3Qn15J1kr0bItbNvjhVI7V9LDMGTafjpML1CO7iIXI%3D13831269650624471650133306742926',
        #     '__cas__rn__': '500766670',
        #     '__cas__st__212': '87982a3fc457bc966fe3ce7e108a44831e29e6be93e9f0cb7d1ea0e184e0c171cefc7021251f1f469f20c6bc',
        #     '__cas__id__212': '69581500',
        #     'CPTK_212': '2116534421',
        #     'CPID_212': '69581500',
        #     'bdindexid': 'q5r90eqbcm5ijp5am255vc5q63',
        #     'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750754238',
        #     'RT': '"z=1&dm=baidu.com&si=454d90be-3dae-4ce7-84a2-ab2e9d648c5d&ss=mca3zrha&sl=1t&tt=2ucl&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
        #     'ab_sr': '1.0.1_M2JlZDEyMzI2NDQ3ZmQwNjE2ZDkzMTI4NDc3ODkxOWVjODQ3NmQyNDIzY2Y1ZjQyYmI0ZTgyMjhlOTFiYWUyYzg4MTgyMzYwNWY1ZmE2NjMwNWYyMmY2Y2M0YTA2NDhmNGVmNmRlZDcxYmMyYTMxMTQzYWNkYTVlNDBiOGFmYmViMzQ3YjIxMDVjZmUyYmI3N2RlNDY0M2RkNGUyZDQwZQ==',
        #     'BDUSS_BFESS': 'DdGSGdNNUR1bDR2OGdxUU90UE1yZndIRTFEaURSNGNBbXJscXdvWFpMR3M4SUZvSUFBQUFBJCQAAAAAAAAAAAEAAAA72va1yOvEpzg4NgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKxjWmisY1poc',
        # },
            # {
            #     'BAIDU_WISE_UID': 'wapp_1744869667916_527',
            #     'BAIDUID': 'FF85DF65CC7463F3726D5301B69C0672:FG=1',
            #     'BAIDUID_BFESS': 'FF85DF65CC7463F3726D5301B69C0672:FG=1',
            #     'PSTM': '1744882843',
            #     'BIDUPSID': '950D047CF79B4A0F8F86462CD08D849F',
            #     'ZFY': ':AYs:BOm:Ajfa1cQtiOrSJADVlDld3:BYmMcahDksItTkOQ:C',
            #     'H_PS_PSSID': '61027_62325_62485_62967_63042_63044_63140_63074_63189_63194_63210_63226_63242_63244_63249_63253',
            #     '__bid_n': '18c42450fcc02886ca93f5',
            #     'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750687271',
            #     'HMACCOUNT': 'DDF927EE5DF25454',
            #     'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihdwitHd04Lvs3Nfz26Zt2holplnIKVacidp8Sue4dMTyfg65BJnOFhn1HthtSiwtygiD7piS4vjG/W9dLb1VAdqMysqdImJFnhAMv/fWi1I5VO0V6uxgO+hV7+7wZFfXG0MSpuMmh7GsZ4C7fF/kTgmvlMIA/tB2qdnJ8KkulgesR5YKU+qTqtaaBkWIZO5dn/GldC1S4QUhUhpm5KMoOoF81v2iwj13daM+9aWJ5GJCQM+RpBohGNhMcqCHhVhtXpVObaDCHgWJZH3ZrTGYHmi7XJB9z3y2o8Kqxep5XBCsugNOW5C73e/g54kuY4PKIS71bGmnPunNtMIatWdCpBi6yoMEZCNh1huwbMdWwuuXVnvNXIEW2pwj4BXINSNFrPKCGZHtLbt/i6efsLSLARZuIGhYqrYfhHGZqJNx2uWmglAIQEZY21OyYDgpfKN3zxRn6ONqHK83MkBENWBMWSAwea/+1VSNUTGfIG+NKu2s+g28sOzjnLUnUE9KukMAMTPZYfT79sbFYuntY0Ry6GX3OsRAJVdXPXKlPRQiighN2h3utZNfUsAGL2WWa3tubT9td9rGfOenGkLOGCRladXTg1IKPDQ9z3/DiqHtAIbmyu3emEg6nEYu6lQuvYr6/UJpAq7e+CnVRC2DzwICP6cu9A5mNm34ZPuoRV+zY3FkhMa5PpAytGwAf1nqFDiyU+WHcGDy5llZtI5Ig4rvXzcdIxeODdssbd+W/AgOwxO3JdRGSluqM4FuAgHCvdnqfGnnbe3vsHq3LuF7pombT65cVprejPaivGVaWugm+VA1kVl5OE/aBXOg67P9UlCyJKVyutwgoMp5Aa/ZkjblrEvPdXZFhAgvw25kAwV0TwSXSe5Q/vbh3nl529wNGdJ0E/Al3XsmHJdLSZ9wC3mJe+ZNDrSwzO8uzPTGJRstuhQcx/x5a3E+Qkao4W1aMhW15Bgywf8BpImierD5YuJm8aNh+b2nRqUTK6NqmhPLvsfMNxShTXBRJdrnFL9nqFcSvY6cuLQt09VwaPPyWktx1V5J+b2nRqUTK6NqmhPLvsfMNZ/k8RFFJMWot30FNQcvJjgmLcRAsZA9ozVp4fEbVslkfSzVKL8rDNNpNjO7rOJCKUwXtmNU/nsKC0PSzAP3Kq4wL4SK3t1tHw4eMSEHL2FCmmrSArB56dw/GBL+N3SuP',
            #     'BDUSS': 'DdGSGdNNUR1bDR2OGdxUU90UE1yZndIRTFEaURSNGNBbXJscXdvWFpMR3M4SUZvSUFBQUFBJCQAAAAAAAAAAAEAAAA72va1yOvEpzg4NgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKxjWmisY1poc',
            #     'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05007666700aotgStKPrY9%2ByDdcKStvWFxvkzgQYr%2Bg84RLwAZGMbj%2FF%2Fu66amlm1lDr3cjP9tg0rCzjxsXcWmRR2tx9I9DDUFPFoGZGrQ%2F6TZ9L3TejNjavrG8nfYC3tt8Z14o9bShwFXz2j2Z7D3NYcEOF8%2FCsv3BOEtk4Z0pHO3j2MHwF0VIElDOzipxIQIhOnEB393eYX9AKcgaUswjfgyqOSa1PD05JzeLRWYhmTixYiOM6MGATtQRnJ%2Bll%2Fp5xczf2rbwz3Qn15J1kr0bItbNvjhVI7V9LDMGTafjpML1CO7iIXI%3D13831269650624471650133306742926',
            #     '__cas__rn__': '500766670',
            #     '__cas__st__212': '87982a3fc457bc966fe3ce7e108a44831e29e6be93e9f0cb7d1ea0e184e0c171cefc7021251f1f469f20c6bc',
            #     '__cas__id__212': '69581500',
            #     'CPTK_212': '2116534421',
            #     'CPID_212': '69581500',
            #     'bdindexid': 'q5r90eqbcm5ijp5am255vc5q63',
            #     'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750754238',
            #     'RT': '"z=1&dm=baidu.com&si=454d90be-3dae-4ce7-84a2-ab2e9d648c5d&ss=mca3zrha&sl=1t&tt=2ucl&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
            #     'ab_sr': '1.0.1_M2JlZDEyMzI2NDQ3ZmQwNjE2ZDkzMTI4NDc3ODkxOWVjODQ3NmQyNDIzY2Y1ZjQyYmI0ZTgyMjhlOTFiYWUyYzg4MTgyMzYwNWY1ZmE2NjMwNWYyMmY2Y2M0YTA2NDhmNGVmNmRlZDcxYmMyYTMxMTQzYWNkYTVlNDBiOGFmYmViMzQ3YjIxMDVjZmUyYmI3N2RlNDY0M2RkNGUyZDQwZQ==',
            #     'BDUSS_BFESS': 'DdGSGdNNUR1bDR2OGdxUU90UE1yZndIRTFEaURSNGNBbXJscXdvWFpMR3M4SUZvSUFBQUFBJCQAAAAAAAAAAAEAAAA72va1yOvEpzg4NgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKxjWmisY1poc',
            # },
            # {
            #     'BAIDUID': '52562D5AE73814CC36104D6AD3C226E4:FG=1',
            #     'BAIDUID_BFESS': '52562D5AE73814CC36104D6AD3C226E4:FG=1',
            #     'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750749263',
            #     'HMACCOUNT': '0356E59AACAA843E',
            #     'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihdwitHd04Lvs3Nfz26Zt2holplnIKVacidp8Sue4dMTyfg65BJnOFhn1HthtSiwtygiD7piS4vjG/W9dLb1VAdqMysqdImJFnhAMv/fWi1I5VO0V6uxgO+hV7+7wZFfXG0MSpuMmh7GsZ4C7fF/kTgmvlMIA/tB2qdnJ8KkulgesR5YKU+qTqtaaBkWIZO5dn/GldC1S4QUhUhpm5KMoOoF81v2iwj13daM+9aWJ5GJCQM+RpBohGNhMcqCHhVhtXpVObaDCHgWJZH3ZrTGYHmi7XJB9z3y2o8Kqxep5XBCsugNOW5C73e/g54kuY4PKIS71bGmnPunNtMIatWdCpBi6yoMEZCNh1huwbMdWwuuXVnvNXIEW2pwj4BXINSNFrPKCGZHtLbt/i6efsLSLARZuIGhYqrYfhHGZqJNx2uWmglAIQEZY21OyYDgpfKN3zxRn6ONqHK83MkBENWBMWSAwea/+1VSNUTGfIG+NKu2s+g28sOzjnLUnUE9KukMAMTPZYfT79sbFYuntY0Ry6GX3OsRAJVdXPXKlPRQiighN2h3utZNfUsAGL2WWa3tubT9td9rGfOenGkLOGCRladXTg1IKPDQ9z3/DiqHtAIbmyu3emEg6nEYu6lQuvYr6/UJpAq7e+CnVRC2DzwICP6cu9A5mNm34ZPuoRV+zY3FkhMa5PpAytGwAf1nqFDiyU+WHcGDy5llZtI5Ig4rvXzcdIxeODdssbd+W/AgOwxO3JdRGSluqM4FuAgHCvdnqfGnnbe3vsHq3LuF7pombT65cVprejPaivGVaWugm+VA1kVl5OE/aBXOg67P9UlCyJKVyutwgoMp5Aa/ZkjblrEvPdXZFhAgvw25kAwV0TwSXSe5Q/vbh3nl529wNGdJ0E/Al3XsmHJdLSZ9wC3mJe+ZNDrSwzO8uzPTGJRstuhQcx/x5a3E+Qkao4W1aMhW15Bgywf8BpImierD5YuJm8aNh+b2nRqUTK6NqmhPLvsfMNxShTXBRJdrnFL9nqFcSvY6cuLQt09VwaPPyWktx1V5J+b2nRqUTK6NqmhPLvsfMNZ/k8RFFJMWot30FNQcvJjgmLcRAsZA9ozVp4fEbVslkfSzVKL8rDNNpNjO7rOJCKUwXtmNU/nsKC0PSzAP3Kq4wL4SK3t1tHw4eMSEHL2FCmmrSArB56dw/GBL+N3SuP',
            #     'BDUSS': 'Xd2aWpKMVFwamhhaUJONTdzOW5ESU91a1R2MU1oM0kxVjFtRlpGb2p2VFotWUZvSVFBQUFBJCQAAAAAAQAAAAEAAACr6JWZ0KG1sLWwMDgxMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANlsWmjZbFpoW',
            #     'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05007690188QRKacet%2FLYqCaeioKms%2Bmfzp4Hp%2BpZvacb9DvW0Hvhop5YfBVVXjqTc%2BwtQg%2FafAfYYi18mpx0lDgbutA3%2BgNlQYxZb1FuDp7JTL%2Bv5RsBmouOTv899GYX2j3E6bQyDbqTCUFaLRnHgfrqdpiFjhfIXl1jf%2BouhWG41pLDKNvfcbpvrW7xGcxqyMuSNmAzC47dtII6NOjkkJOz0me2X%2BZtks%2FPFhjUCLKsde%2FowOOMI3hIQx%2B0VK1KU1FBRU8WnDzTpAdAXytq%2FG9eryu4F31ITkwe0EiAOz5HzJ%2FJcD9C8Jathw9Ii60uneZud8fCV393177010116505284996838136904143',
            #     '__cas__rn__': '500769018',
            #     '__cas__st__212': '974686bf661878c2d04b8d942db1012e5080cc74bf03313085191feec50cb20a6edaec4df005c5c113148b91',
            #     '__cas__id__212': '69574836',
            #     'CPTK_212': '484586435',
            #     'CPID_212': '69574836',
            #     'bdindexid': '2oblianl1bkcltm1ca4nrddqa5',
            #     'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750761379',
            #     'RT': '"z=1&dm=baidu.com&si=8c042292-2f64-4191-b6d1-9c7511455739&ss=mcae4d4m&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
            #     'ab_sr': '1.0.1_ZTZmZTA5YTUxYzJiMTY4NDYwZTg4Mjg3YzI3ZmEwMWQ0N2MzM2RjOGI3MGY1MWZmMjA3NTZiYmYwMGQ4ZDZhZDU3OTg4MmI0MmJlNGU3ZWY5YTM2MDExM2ZkZDQwYTUzMDk1NjJjYmY3NzI5MTNjZDNkY2Q2YjM5ODY3ZjMwZmU4MjU2OWRjYzZlNmU1OTllMmE2YmMyMTM3NmU5NjU5NA==',
            #     'BDUSS_BFESS': 'Xd2aWpKMVFwamhhaUJONTdzOW5ESU91a1R2MU1oM0kxVjFtRlpGb2p2VFotWUZvSVFBQUFBJCQAAAAAAQAAAAEAAACr6JWZ0KG1sLWwMDgxMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANlsWmjZbFpoW',
            # },
            # {
            #     'BAIDU_WISE_UID': 'wapp_1744869667916_527',
            #     'BAIDUID': 'FF85DF65CC7463F3726D5301B69C0672:FG=1',
            #     'BAIDUID_BFESS': 'FF85DF65CC7463F3726D5301B69C0672:FG=1',
            #     'PSTM': '1744882843',
            #     'BIDUPSID': '950D047CF79B4A0F8F86462CD08D849F',
            #     'ZFY': ':AYs:BOm:Ajfa1cQtiOrSJADVlDld3:BYmMcahDksItTkOQ:C',
            #     'H_PS_PSSID': '61027_62325_62485_62967_63042_63044_63140_63074_63189_63194_63210_63226_63242_63244_63249_63253',
            #     '__bid_n': '18c42450fcc02886ca93f5',
            #     'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750687271',
            #     'HMACCOUNT': 'DDF927EE5DF25454',
            #     'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihdwitHd04Lvs3Nfz26Zt2holplnIKVacidp8Sue4dMTyfg65BJnOFhn1HthtSiwtygiD7piS4vjG/W9dLb1VAdqMysqdImJFnhAMv/fWi1I5VO0V6uxgO+hV7+7wZFfXG0MSpuMmh7GsZ4C7fF/kTgmvlMIA/tB2qdnJ8KkulgesR5YKU+qTqtaaBkWIZO5dn/GldC1S4QUhUhpm5KMoOoF81v2iwj13daM+9aWJ5GJCQM+RpBohGNhMcqCHhVhtXpVObaDCHgWJZH3ZrTGYHmi7XJB9z3y2o8Kqxep5XBCsugNOW5C73e/g54kuY4PKIS71bGmnPunNtMIatWdCpBi6yoMEZCNh1huwbMdWwuuXVnvNXIEW2pwj4BXINSNFrPKCGZHtLbt/i6efsLSLARZuIGhYqrYfhHGZqJNx2uWmglAIQEZY21OyYDgpfKN3zxRn6ONqHK83MkBENWBMWSAwea/+1VSNUTGfIG+NKu2s+g28sOzjnLUnUE9KukMAMTPZYfT79sbFYuntY0Ry6GX3OsRAJVdXPXKlPRQiighN2h3utZNfUsAGL2WWa3tubT9td9rGfOenGkLOGCRladXTg1IKPDQ9z3/DiqHtAIbmyu3emEg6nEYu6lQuvYr6/UJpAq7e+CnVRC2DzwICP6cu9A5mNm34ZPuoRV+zY3FkhMa5PpAytGwAf1nqFDiyU+WHcGDy5llZtI5Ig4rvXzcdIxeODdssbd+W/AgOwxO3JdRGSluqM4FuAgHCvdnqfGnnbe3vsHq3LuF7pombT65cVprejPaivGVaWugm+VA1kVl5OE/aBXOg67P9UlCyJKVyutwgoMp5Aa/ZkjblrEvPdXZFhAgvw25kAwV0TwSXSe5Q/vbh3nl529wNGdJ0E/Al3XsmHJdLSZ9wC3mJe+ZNDrSwzO8uzPTGJRstuhQcx/x5a3E+Qkao4W1aMhW15Bgywf8BpImierD5YuJm8aNh+b2nRqUTK6NqmhPLvsfMNxShTXBRJdrnFL9nqFcSvY6cuLQt09VwaPPyWktx1V5J+b2nRqUTK6NqmhPLvsfMNZ/k8RFFJMWot30FNQcvJjgmLcRAsZA9ozVp4fEbVslkfSzVKL8rDNNpNjO7rOJCKUwXtmNU/nsKC0PSzAP3Kq4wL4SK3t1tHw4eMSEHL2FCmmrSArB56dw/GBL+N3SuP',
            #     'BDUSS': '9HaDdQWS1KMVB2UU5aWHN6TzFLfjgzdnhXMlVSUHdoeUIySUFQMC1FV2QzSUZvSUFBQUFBJCQAAAAAAQAAAAEAAACr6JWZ0KG1sLWwMDgxMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJ1PWmidT1poUW',
            #     'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05007615344DFzmNY7xqbspVuXo4cKiUjZw25gu6lurhhCAzC5rPOkW79C6TfBLxw3oP%2BrNDMyn%2Fst9YNvnm%2BLkfWIoYYSROWJi3g8QxMjbq0eHk0RMqpiWQ5KLbX2uy4w2Uftcuzxo%2Fwy5hs48GEPxjMqxKdoyycOJBRtYO%2BakOMa76DBLr%2BMqRvb33OtWcWqy3bRqRRgDl8SDwi56KYFM4k3c5SFse0aNcxRudp9B6BDMtkPypQE6CVzh9OYdIKw6LqL%2BOo24aiin1BsmNTIBHbku2r5SnlGomuSK1uvq7oRotjImDs1xCH5YHL7LqZ5FzJnuM4A%2F25029310942391112830142674449681',
            #     '__cas__rn__': '500761534',
            #     '__cas__st__212': '2e2ee7c4e96a23391a9aa159fe1915a4869928389127d0a15c86ac4829bd72b398edf48871e9f0cb7e1ecea6',
            #     '__cas__id__212': '69574836',
            #     'CPTK_212': '1332419499',
            #     'CPID_212': '69574836',
            #     'bdindexid': 'rs5kfcksjv897pqps662789id7',
            #     'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750749908',
            #     'RT': '"z=1&dm=baidu.com&si=454d90be-3dae-4ce7-84a2-ab2e9d648c5d&ss=mca3zrha&sl=11&tt=1acf&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
            #     'BDUSS_BFESS': '9HaDdQWS1KMVB2UU5aWHN6TzFLfjgzdnhXMlVSUHdoeUIySUFQMC1FV2QzSUZvSUFBQUFBJCQAAAAAAQAAAAEAAACr6JWZ0KG1sLWwMDgxMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJ1PWmidT1poUW',
            #     'ab_sr': '1.0.1_M2E3OGRlN2U5ZmYyZDhkYTU0ZmE2OTFmMzA2ZWYyZGEzMWRlNTJkNDdhMTU1NzkyNzcwNTYwYTZlNGJiODhjNTcyZTY1ZTIzYmNkYTNhMWY3MzIzYWJlMzY2ODczYWU2MDBjNDVjZWY5ZmYxZDRlMmE2YTliYWFmOWVjNWVmMGJlMmFiZWNhM2E4NGM3YzQyNjVmZmEwNGQ5ZDg4MmFiNA==',
            # },
            # {
            #     'BDUSS': '05jbXB0S003NG52azBWWnZIQk8wdlhQUTViflRmbUxKR0toT2FRak5heHRSSUpvSVFBQUFBJCQAAAAAAQAAAAEAAABBjpqZ0KHT47WwtbAwODEwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG23Wmhtt1poQ',
            #     'BAIDUID': '0437E9BF4224765A2BB8C862C24687D5:FG=1',
            #     'BAIDUID_BFESS': '0437E9BF4224765A2BB8C862C24687D5:FG=1',
            #     'HMACCOUNT': '1EC551B6460E8184',
            # },
            {
                'RT': '"z=1&dm=baidu.com&si=547f12a5-af39-48b0-a181-bdc21662c87b&ss=mcbaf3ke&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
                'ab_sr': '1.0.1_NDlkMWJhNTU2ZDQ0ODYzZDRlOTg3OTUyYjMwMzk4YTBmYmMwN2ZiYzEwYTdlZmVjY2Q1ZTMxZDA1ZDU3MzAxZTFiMDI1OTBjODM1MDhhODZjNjY5ZjczYmI4MGFiZjc1M2VkYTUyMTRiZmRjZWY1MTM0ODU1YmY2NWJlNjhmZjU3MTRmNGNlNWUyMTA4MTk3OTE5NDlkODFjMDQzZDU1YQ==',
                'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750815887',
                'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750747117,1750748674,1750753716,1750763806',
                'bdindexid': 'averdrlegkrm5f6qqnigie18f5',
                'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05007909166N%2BIfIF0sOpDriLgGqkgR9UYzkQJI6dbxGy4OkCEHWexXLE%2Faj9KXlcs8mOHVfulVKYtQjALl0G7YFITHO%2Fm9p1eyKWGqH4JonbubACqyILDpHMycZl%2BNMG9BcFGiddYSPBYs36SFxfXSdIwFsaP1UAErGhS28Rz0E5fTEn7uyr5w%2BUyVwrtUFzS3OHqgsbvT0FrKQvPaWYer07j7hDr8VgyK96%2Fd2%2FzYeFpwWTuVso8lDiUQ0jkKyUXUs8dK9Yxnq9CB%2BxzupU5XcJIRQWXm2A%3D%3D57155609196896830437666246109796',
                'CPID_212': '69554690',
                'CPTK_212': '1890979730',
                '__cas__id__212': '69554690',
                '__cas__rn__': '500790916',
                '__cas__st__212': '9cdcb4cbb059f23d5afe475e7120a6acd641314f05440b5add1dfbe9abe739e1bedf12ce42c8a43aa4d316ea',
                'BDUSS': '5wSkM5U2F2U0kwQWJTcVhwdWtJZHR-ZTNxU2ppVXhicFFTcllqUXI2RmlUNEpvSVFBQUFBJCQAAAAAAQAAAAEAAADqGBSHQXVyb3JhbDY4NjgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGLCWmhiwlpoR0',
                'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihdwitHd04Lvs3Nfz26Zt2honnQBqGZJ1+FooMMOy9VfBMHd4KSE2lo7q2jM/4leBJXqt+nMkIsYwpNA4XBVB5BGpKv8rf9RxKxeW8+CymWcpQ8qfiUvli8qcS/AH/6nfMYq1ZMQFVRuXQF6FC4JGmtin1ybbYbfSfzYRA9mCq3GnejGE5mAFoMKquZJvsf1FvjSGAIcnDl+H0Bfmo1ZE0Hy/Nk2eTwFYhuZsGjwCR7FVAPhMNMWL+Qlfaczl+PBQBDkVV8ysF/wnr6VWwUzKeq+NBDa593uSfHg6jo4zQ+k5UPBBx7NsZfzlUSbKaHt/szuPooLbKBIKSSHTndNj5Tmg/K9eQw6jF8BfLBvVDYMPpFeLs4wygIv6m069lhsdmzfX6/IgAQAsCi0TGpGRt6cfQFXV1C8qyUqcAnBm7hcJuxcqfdReixTVTfT+miI3ZV5eQE96jz5eP/gEigLYjtZnrOQVr9TB3lK8L3WS99/Zr9ng7DJNA0zsRL0eZGEKF1aDRInbESzVqJcCK3XpGJOV/zZ6wkf5f+PnYbtHcSvBB4lPdCgO/rhHbvTb7w1sYiN/Vk5/GFQKmYmpXiN4dJoe04sIEztQcQ/Sj8aeZwWg0mAteMeU9qyn6SoJvv6345Qt76XFBJWSgbZ6/F0ZRwCDo0NPL3fh6V0Qf84X0lHCGZH+bXo6+dPz9Tlk96vm6TgySNgyXjGJSG4FgpxblJLIIlOtlMsm4G5znNYqjxYFMcav1VQU9Nb3SpOs6OnNPHoLTWc9sgd7vyVBOz93uspd4P+v8uPF3aU45FG/PHiWX5Tv2IOghUDulefRvlX9eT7gQwEiclvXWS2pMTilyx6wORXYWMC8Ewe1rUuQprEZZNDywMI17CupLBOAx9qwTTBhEMNzi6OXbElHkA3erw56I0vmkH9G20tmAiqCABGBI1qeHlbtIIUXAPQK2AKm25kN9e++uG7KATaiQSHPJR405LDjC+5v0mQclI0YcJp8DvGLdRUpGcbUX7V27dvoxZBIoD3cMTFVZaFO6JIJzM1T5EoNlrqqJb8Op38LjSNcK',
                'BDORZ': 'FFFB88E999055A3F8A630C64834BD6D0',
                'HMACCOUNT': '496483824474D6A5',
                'BCLID': '8359499958683309882',
                'BCLID_BFESS': '8359499958683309882',
                'BDSFRCVID': 'vjCOJexroGWgCqbsSA0shHVKjQpWxY5TDYrELPfiaimDVu-VvXWoEG0Pts1-dEu-S2EwogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0M5',
                'BDSFRCVID_BFESS': 'vjCOJexroGWgCqbsSA0shHVKjQpWxY5TDYrELPfiaimDVu-VvXWoEG0Pts1-dEu-S2EwogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0M5',
                'H_BDCLCKID_SF': 'tRAOoC8-fIvDqTrP-trf5DCShUFsLtJAB2Q-XPoO3M3JEPjPKpbNDM4JybjiaqojQ5bk_xbgy4op8P3y0bb2DUA1y4vp-qvUa2TxoUJ2-KDVeh5Gqq-KQJ-ebPRiWTj9QgbLMhQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hD89Dj-Ke5PthxO-hI6aKC5bL6rJabC3fRcJXU6q2bDeQnJM3boa-a7CoPOSWUQvjxjx3n7Zjq0vWq54WpOh2C60WlbCb664fxn5hUonDh83KNLLKUQtHGAHK43O5hvv8KoO3M7VBUKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_E5bj2qRufoKtb3f',
                'H_BDCLCKID_SF_BFESS': 'tRAOoC8-fIvDqTrP-trf5DCShUFsLtJAB2Q-XPoO3M3JEPjPKpbNDM4JybjiaqojQ5bk_xbgy4op8P3y0bb2DUA1y4vp-qvUa2TxoUJ2-KDVeh5Gqq-KQJ-ebPRiWTj9QgbLMhQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hD89Dj-Ke5PthxO-hI6aKC5bL6rJabC3fRcJXU6q2bDeQnJM3boa-a7CoPOSWUQvjxjx3n7Zjq0vWq54WpOh2C60WlbCb664fxn5hUonDh83KNLLKUQtHGAHK43O5hvv8KoO3M7VBUKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_E5bj2qRufoKtb3f',
                'H_PS_PSSID': '60279_61684_62325_63144_63324_63568_63563_63584_63617_63639_63645_63646_63657_63693_63724_63728_63715',
                'H_WISE_SIDS': '60279_61684_62325_62967_63144_63194_63210_63241_63268_63324_63352_63386_63394_63390_63440',
                'BIDUPSID': '2FEBFD961790CF3B5CB7C06D0DCA03F8',
                'PSTM': '1745642057',
                'BAIDUID': '5E9B2757D9152FB85FDD6D4AEB4026ED:FG=1',
                'MAWEBCUID': 'web_oHAxQIUvPYLZZQqNfndpkAqAJlTBpabDPBBNaCvdMXrswtkRXG',
                'MCITY': '-%3A',                
            }
        ]

        # 城市列表
        city = {
        1: "济南",
        2: "贵阳",
        4: "六盘水",
        5: "南昌",
        6: "九江",
        7: "鹰潭",
        8: "抚州",
        9: "上饶",
        10: "赣州",
        11: "重庆",
        13: "包头",
        14: "鄂尔多斯",
        15: "巴彦淖尔",
        16: "乌海",
        20: "呼和浩特",
        21: "赤峰",
        22: "通辽",
        25: "呼伦贝尔",
        28: "武汉",
        29: "大连",
        30: "黄石",
        31: "荆州",
        32: "襄阳",
        33: "黄冈",
        34: "荆门",
        35: "宜昌",
        36: "十堰",
        37: "随州",
        39: "鄂州",
        40: "咸宁",
        41: "孝感",
        43: "长沙",
        44: "岳阳",
        45: "衡阳",
        46: "株洲",
        47: "湘潭",
        48: "益阳",
        49: "郴州",
        50: "福州",
        51: "莆田",
        52: "三明",
        53: "龙岩",
        54: "厦门",
        55: "泉州",
        56: "漳州",
        57: "上海",
        59: "遵义",
        66: "娄底",
        67: "怀化",
        68: "常德",
        77: "青岛",
        78: "烟台",
        79: "临沂",
        80: "潍坊",
        81: "淄博",
        82: "东营",
        84: "菏泽",
        85: "枣庄",
        86: "德州",
        87: "宁德",
        88: "威海",
        89: "柳州",
        90: "南宁",
        91: "桂林",
        92: "贺州",
        93: "贵港",
        94: "深圳",
        95: "广州",
        96: "宜宾",
        97: "成都",
        98: "绵阳",
        99: "广元",
        100: "遂宁",
        101: "巴中",
        102: "内江",
        103: "泸州",
        104: "南充",
        106: "德阳",
        107: "乐山",
        108: "广安",
        109: "资阳",
        111: "自贡",
        112: "攀枝花",
        113: "达州",
        114: "雅安",
        115: "吉安",
        117: "昆明",
        118: "玉林",
        119: "河池",
        123: "玉溪",
        125: "南京",
        126: "苏州",
        127: "无锡",
        128: "北海",
        129: "钦州",
        130: "防城港",
        131: "百色",
        132: "梧州",
        133: "东莞",
        134: "丽水",
        135: "金华",
        136: "萍乡",
        137: "景德镇",
        138: "杭州",
        139: "西宁",
        140: "银川",
        141: "石家庄",
        143: "衡水",
        144: "张家口",
        145: "承德",
        146: "秦皇岛",
        147: "廊坊",
        148: "沧州",
        149: "温州",
        150: "沈阳",
        151: "盘锦",
        152: "哈尔滨",
        153: "大庆",
        154: "长春",
        155: "四平",
        156: "连云港",
        157: "淮安",
        158: "扬州",
        159: "泰州",
        161: "徐州",
        162: "常州",
        163: "南通",
        164: "天津",
        165: "西安",
        166: "兰州",
        168: "郑州",
        169: "镇江",
        172: "宿迁",
        173: "铜陵",
        174: "黄山",
        175: "池州",
        178: "淮南",
        179: "宿州",
        181: "六安",
        182: "滁州",
        183: "淮北",
        184: "阜阳",
        185: "马鞍山",
        186: "安庆",
        187: "蚌埠",
        188: "芜湖",
        189: "合肥",
        191: "辽源",
        194: "松原",
        195: "云浮",
        196: "佛山",
        197: "湛江",
        198: "江门",
        199: "惠州",
        200: "珠海",
        201: "韶关",
        202: "阳江",
        203: "茂名",
        204: "潮州",
        205: "揭阳",
        207: "中山",
        208: "清远",
        209: "肇庆",
        210: "河源",
        211: "梅州",
        212: "汕头",
        213: "汕尾",
        215: "鞍山",
        216: "朝阳",
        217: "锦州",
        218: "铁岭",
        219: "丹东",
        220: "本溪",
        221: "营口",
        222: "抚顺",
        223: "阜新",
        224: "辽阳",
        225: "葫芦岛",
        226: "张家界",
        228: "长治",
        229: "忻州",
        230: "晋中",
        235: "朔州",
        236: "阳泉",
        237: "吕梁",
        239: "海口",
        243: "三亚",
        246: "新余",
        253: "南平",
        256: "宜春",
        259: "保定",
        261: "唐山",
        262: "南阳",
        263: "新乡",
        264: "开封",
        265: "焦作",
        266: "平顶山",
        268: "许昌",
        269: "永州",
        270: "吉林",
        271: "铜川",
        272: "安康",
        273: "宝鸡",
        274: "商洛",
        275: "渭南",
        276: "汉中",
        277: "咸阳",
        278: "榆林",
        282: "定西",
        283: "武威",
        284: "酒泉",
        285: "张掖",
        286: "嘉峪关",
        287: "台州",
        288: "衢州",
        289: "宁波",
        291: "眉山",
        292: "邯郸",
        293: "邢台",
        295: "伊春",
        300: "黑河",
        301: "鹤岗",
        302: "七台河",
        303: "绍兴",
        304: "嘉兴",
        305: "湖州",
        306: "舟山",
        307: "平凉",
        308: "天水",
        309: "白银",
        317: "克拉玛依",
        319: "齐齐哈尔",
        320: "佳木斯",
        322: "牡丹江",
        323: "鸡西",
        324: "绥化",
        335: "昭通",
        339: "曲靖",
        342: "丽江",
        343: "金昌",
        344: "陇南",
        350: "临沧",
        352: "济宁",
        353: "泰安",
        359: "双鸭山",
        366: "日照",
        370: "安阳",
        371: "驻马店",
        373: "信阳",
        374: "鹤壁",
        375: "周口",
        376: "商丘",
        378: "洛阳",
        379: "漯河",
        380: "濮阳",
        381: "三门峡",
        391: "亳州",
        395: "吴忠",
        396: "固原",
        401: "延安",
        405: "邵阳",
        407: "通化",
        408: "白山",
        422: "铜仁",
        424: "安顺",
        426: "毕节",
        438: "保山",
        466: "拉萨",
        467: "乌鲁木齐",
        472: "石嘴山",
        480: "中卫",
        506: "来宾",
        514: "北京",
        665: "崇左",
        666: "普洱",
    }

        
        # 读取关键词列表
        try:
            word_list = pd.read_excel('存在的数字设备和服务关键词.xlsx')
            keywords = word_list['关键词'].tolist()
            logger.info(f"成功读取到 {len(keywords)} 个关键词")
        except Exception as e:
            logger.error(f"读取关键词文件失败: {str(e)}")
            logger.info("使用默认关键词'数字政务APP'继续")
            keywords = ["数字政务APP"]
        
        years = list(range(2016, 2026))  # 2016年到2025年
        
        # 初始化管理器
        progress_manager = ProgressManager(CONFIG['progress_file'])
        batch_manager = BatchManager(CONFIG['output_dir'], CONFIG['batch_size'])
        
        # 构建代理管理器
        proxy_manager = ProxyManager([
            # {'http': 'http://15968588744:kwkdvtr6@61.184.8.27:10134', 'https': 'http://15968588744:kwkdvtr6@61.184.8.27:10134'},
            # {'http': 'http://15968588744:kwkdvtr6@110.166.229.165:16817', 'https': 'http://15968588744:kwkdvtr6@110.166.229.165:16817'},
        ], CONFIG['use_local_ip'])
        
        # 构建Cookie管理器
        cookie_manager = CookieManager(cookies_list)
        
        # 构建所有任务
        all_tasks = []
        for word in keywords:
            for year in years:
                for city_number, city_name in city.items():
                    task_info = (word, city_number, city_name, year, progress_manager, batch_manager, proxy_manager, cookie_manager)
                    all_tasks.append(task_info)
        
        logger.info(f"总任务数: {len(all_tasks)}")
        
        # 统计已完成的任务
        completed_tasks = sum(1 for word, city_number, city_name, year, *_ in all_tasks 
                            if progress_manager.is_completed(word, city_number, year))
        logger.info(f"已完成任务数: {completed_tasks}")
        logger.info(f"剩余任务数: {len(all_tasks) - completed_tasks}")
        
        # 并发处理任务
        success_count = 0
        failure_count = 0
        
        with ThreadPoolExecutor(max_workers=CONFIG['max_workers']) as executor:
            # 提交所有任务
            future_to_task = {executor.submit(process_single_task, task): task for task in all_tasks}
            
            # 处理完成的任务
            for future in as_completed(future_to_task):
                task_info = future_to_task[future]
                word, city_number, city_name, year = task_info[:4]
                
                try:
                    result = future.result()
                    if result:
                        success_count += 1
                    else:
                        failure_count += 1
                        
                    # 进度显示
                    total_processed = success_count + failure_count
                    progress_pct = (total_processed / len(all_tasks)) * 100
                    logger.info(f"进度: {progress_pct:.1f}% ({total_processed}/{len(all_tasks)}), "
                              f"成功: {success_count}, 失败: {failure_count}")
                    
                except Exception as e:
                    failure_count += 1
                    logger.error(f"任务执行异常: {word} - {city_name} - {year}, 错误: {e}")
        
        # 保存最后一个批次
        batch_manager.save_final_batch()
        
        # 合并所有批次文件
        logger.info("开始合并所有批次文件...")
        if batch_manager.merge_all_batches(CONFIG['final_output']):
            logger.info(f"数据合并完成！最终文件: {CONFIG['final_output']}")
        else:
            logger.error("数据合并失败！")
        
        # 最终统计
        logger.info(f"爬取完成！成功: {success_count}, 失败: {failure_count}")
        logger.info(f"进度文件: {CONFIG['progress_file']}")
        logger.info(f"批次数据目录: {CONFIG['output_dir']}")
        logger.info(f"最终输出文件: {CONFIG['final_output']}")
        
    except KeyboardInterrupt:
        logger.info("用户中断了程序，进度已保存")
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
    finally:
        logger.info("程序结束")

if __name__ == "__main__":
    main()