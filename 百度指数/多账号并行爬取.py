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
    level=logging.INFO,  # 默认级别为INFO，减少DEBUG输出
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
    'max_workers': 5,   # 每个账号组的并发线程数（不要设置太高，避免单个账号被封）
    'retry_times': 1,   # 重试次数
    'base_delay': 1,  # 基础延迟时间（秒）
    'max_delay': 1.5,   # 最大延迟时间（秒）
    'progress_file': 'crawler_progress.json',  # 进度文件
    'output_dir': 'data_batches',  # 批次数据目录
    'final_output': '百度指数_全部关键词.xlsx',  # 最终输出文件
    'use_local_ip': True  # 是否使用本地IP
}

# 进度汇总类
class ProgressSummary:
    def __init__(self, interval=60):  # 默认每60秒汇总一次
        self.interval = interval
        self.running = False
        self.thread = None
        self.results = {}
        self.total_tasks = 0
        self.completed_tasks = 0  # 已完成的任务数
        self.last_completed = 0   # 上次统计时的完成任务数
        self.last_check_time = None  # 上次检查时间
        self.lock = threading.Lock()
        self.results_lock = threading.RLock()  # 初始化results的锁
        # 存储所有cookie manager的引用
        self.cookie_managers = {}
    
    def start(self, results, total_tasks, completed_tasks=0):
        """启动进度汇总线程"""
        self.results = results
        self.total_tasks = total_tasks
        self.completed_tasks = completed_tasks  # 初始已完成任务数
        self.last_completed = completed_tasks
        self.last_check_time = time.time()
        self.start_time = time.time()  # 初始化开始时间
        self.results_lock = threading.RLock()  # 初始化results的锁
        self.running = True
        self.thread = threading.Thread(target=self._summary_loop)
        self.thread.daemon = True
        self.thread.start()
        logger.info(f"进度汇总线程已启动，每 {self.interval} 秒汇总一次，初始已完成任务数: {self.completed_tasks}")
    
    def stop(self):
        """停止进度汇总线程"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        self._print_summary()  # 停止时打印最后一次汇总
    
    def register_cookie_manager(self, group_name, cookie_manager):
        """注册一个cookie manager用于统计可用账号"""
        with self.lock:
            self.cookie_managers[group_name] = cookie_manager
    
    def _summary_loop(self):
        """定期汇总进度的循环"""
        while self.running:
            time.sleep(self.interval)
            self._print_summary()
    
    def _count_available_accounts(self):
        """统计当前可用账号数量"""
        available_accounts = 0
        total_accounts = 0
        
        with self.lock:
            for group_name, manager in self.cookie_managers.items():
                if not manager:
                    continue
                
                group_total = len(manager.cookie_list)
                group_blocked = len(manager.blocked_indices)
                group_available = group_total - group_blocked
                
                total_accounts += group_total
                available_accounts += group_available
                
                if group_blocked > 0:
                    logger.info(f"账号组 {group_name}: {group_available}/{group_total} 个账号可用")
        
        return available_accounts, total_accounts
    
    def _calculate_speed(self):
        """计算每分钟处理的任务数"""
        current_time = time.time()
        current_completed = 0
        
        # 汇总所有成功的任务数量
        with self.results_lock:
            for group_name, data in self.results.items():
                if isinstance(data, dict):
                    current_completed += data.get('success', 0)
        
        current_completed += self.completed_tasks
        
        time_diff = current_time - self.last_check_time
        task_diff = current_completed - self.last_completed
        
        # 避免除以零
        if time_diff <= 0:
            return 0
        
        # 计算每分钟速度
        speed_per_minute = (task_diff / time_diff) * 60
        
        # 更新上次检查时间和完成任务数
        self.last_check_time = current_time
        self.last_completed = current_completed
        
        return speed_per_minute
    
    def _print_summary(self):
        """打印进度汇总信息"""
        current_time = time.time()
        elapsed_seconds = current_time - self.start_time
        elapsed_minutes = elapsed_seconds / 60
        
        # 计算已完成任务数、成功数和失败数
        with self.results_lock:
            completed = 0
            success = 0
            failure = 0
            
            for group_name, data in self.results.items():
                if isinstance(data, dict):  # 确保data是字典
                    success += data.get('success', 0)
                    failure += data.get('failure', 0)
                    # 不依赖于'status'键，直接使用success和failure计算
                    if 'success' in data or 'failure' in data:
                        completed += 1
        
        # 计算总处理量（包括之前已完成的任务）
        total_processed = success
        
        # 避免除以零错误
        if elapsed_minutes == 0:
            rate = 0
        else:
            rate = total_processed / elapsed_minutes
        
        # 估算剩余时间
        remaining_tasks = self.total_tasks - total_processed
        if rate == 0:
            etc_minutes = '未知'
        else:
            etc_minutes = int(remaining_tasks / rate)
        
        # 计算可用账号数量
        available_accounts, total_accounts = self._count_available_accounts()
        
        # 获取账号冷却信息
        cooldown_info = []
        for group_name, cookie_manager in self.cookie_managers.items():
            if not cookie_manager:
                continue
            status = cookie_manager.get_status()
            if 'cooldown_status' in status and status['cooldown_status']:
                for idx, cooldown_data in status['cooldown_status'].items():
                    cooldown_info.append(f"{group_name}-账号{idx+1}: 已冷却{cooldown_data['elapsed_minutes']}分钟，剩余{cooldown_data['remaining_minutes']}分钟")

        # 构建进度摘要
        summary = [
            f"进度汇总 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]",
            f"已处理: {total_processed}/{self.total_tasks} ({total_processed/self.total_tasks*100:.1f}%)",
            f"成功: {success}, 失败: {failure}",
            f"平均处理速度: {rate:.2f} 任务/分钟",
            f"已用时: {int(elapsed_minutes)}分钟, 预计剩余: {etc_minutes}分钟",
            f"可用账号数量: {available_accounts}/{total_accounts}",
        ]
        
        # 添加账号冷却信息
        if cooldown_info:
            summary.append("账号冷却状态:")
            for info in cooldown_info:
                summary.append(f"  - {info}")
        
        # 添加性能指标
        speed = self._calculate_speed()
        if speed > 0:
            summary.append(f"当前速度: {speed:.2f} 任务/分钟")
        
        # 检查线程状态
        self._check_threads_status()
                
        # 打印汇总信息
        logger.info("\n" + "\n".join(summary))
    
    def _check_threads_status(self):
        """检查是否有线程卡住"""
        with self.lock:
            for group, stats in self.results.items():
                if stats.get('thread') and stats['thread'].is_alive():
                    logger.debug(f"账号组 {group} 的线程仍在运行")
                elif stats.get('thread'):
                    logger.warning(f"账号组 {group} 的线程已停止运行")

# 线程锁
progress_lock = threading.Lock()
batch_lock = threading.Lock()

# 全局变量
current_batch_data = []
processed_count = 0

# 重试装饰器
def retry(max_retries=1, delay=0.3):
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
        
        # 检查现有批次文件，确定下一个批次编号
        self.batch_count = self._get_max_batch_number()
        logger.info(f"初始化批次管理器，下一个批次编号将从 {self.batch_count + 1:04d} 开始")
    
    def _get_max_batch_number(self):
        """扫描输出目录找到最大的批次编号"""
        max_batch = 0
        if os.path.exists(self.output_dir):
            batch_files = []
            for file in os.listdir(self.output_dir):
                if file.startswith('batch_') and file.endswith('.xlsx'):
                    try:
                        # 提取批次编号
                        batch_num = int(file.split('_')[1].split('.')[0])
                        max_batch = max(max_batch, batch_num)
                    except (ValueError, IndexError):
                        continue
            
            if max_batch > 0:
                logger.info(f"找到已存在的最大批次编号: {max_batch}")
        
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
        """保存最后一个批次，即使数据不足batch_size条"""
        if self.current_batch:
            logger.info(f"保存最后一个不完整批次，包含 {len(self.current_batch)} 条记录")
            self.save_current_batch()
    
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
    def __init__(self, min_delay=1, max_delay=1.2):
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
        self.blocked_indices = set()  # 存储被锁定的账号索引
        self.last_check_time = time.time()  # 上次检查账号状态的时间
        self.block_times = {}  # 记录每个账号被锁定的时间
        self.tried_after_cooldown = set()  # 记录冷却后尝试过的账号
        
        # 为每个工作线程分配一个独立的cookie
        self.thread_cookies = {}
    
    def get_cookie(self):
        """获取一个Cookie，为每个线程分配独立的cookie以支持并行"""
        thread_id = threading.get_ident()
        
        # 先检查是否所有账号都被锁定
        with self.lock:
            if len(self.blocked_indices) >= len(self.cookie_list):
                logger.error("所有账号都已被锁定！")
                return None
        
        # 如果该线程已经有分配的cookie，检查该cookie对应的账号是否已被锁定
        if thread_id in self.thread_cookies:
            cookie = self.thread_cookies[thread_id]
            # 检查该cookie对应的账号是否被锁定
            for i, c in enumerate(self.cookie_list):
                if c == cookie and i in self.blocked_indices:
                    # 如果已被锁定，从thread_cookies中删除
                    with self.lock:
                        if thread_id in self.thread_cookies:
                            del self.thread_cookies[thread_id]
                        logger.debug(f"线程 {thread_id} 原分配的账号 {i+1} 已被锁定，将重新分配账号")
                    # 跳出循环，走下面重新分配账号的逻辑
                    break
            else:
                # 如果账号未被锁定，直接返回
                return cookie
        
        # 需要新分配或重新分配一个账号
        with self.lock:
            # 再次检查是否所有账号都被锁定（可能在等锁期间其他线程已锁定所有账号）
            if len(self.blocked_indices) >= len(self.cookie_list):
                logger.error("所有账号都已被锁定！")
                return None
            
            # 尝试解除冷却时间已到的账号
            current_time = time.time()
            for idx in list(self.blocked_indices):
                if idx in self.block_times:
                    # 计算已冷却的时间（分钟）
                    cooldown_minutes = (current_time - self.block_times[idx]) / 60
                    if cooldown_minutes >= 30:  # 冷却30分钟后解锁
                        logger.info(f"账号 {idx+1} 已冷却 {int(cooldown_minutes)} 分钟，尝试解除锁定")
                        # 将账号移出锁定集合，但标记为尝试过解锁
                        self.blocked_indices.remove(idx)
                        self.tried_after_cooldown.add(idx)
            
            # 获取所有未锁定的账号索引
            available_indices = [i for i in range(len(self.cookie_list)) if i not in self.blocked_indices]
            
            if not available_indices:
                logger.error("所有账号都已被锁定，无法继续爬取!")
                return None
            
            # 随机选择一个可用账号，避免固定顺序可能导致的问题
            chosen_index = random.choice(available_indices)
            cookie = self.cookie_list[chosen_index]
            
            # 为当前线程分配这个cookie
            self.thread_cookies[thread_id] = cookie
            logger.debug(f"线程 {thread_id} 分配到账号 {chosen_index+1}")
            
            return cookie
    
    def block_account(self, cookie):
        """标记一个账号为被锁定状态"""
        with self.lock:
            for i, c in enumerate(self.cookie_list):
                if c == cookie:
                    current_time = time.time()
                    # 记录锁定时间
                    self.blocked_indices.add(i)
                    self.block_times[i] = current_time
                    
                    # 如果此账号是冷却后再次被锁定，记录并延长冷却时间
                    if i in self.tried_after_cooldown:
                        logger.warning(f"账号 {i+1} 在冷却后再次被锁定，将延长冷却时间")
                        # 将其从tried_after_cooldown中移除，因为它现在又被锁定了
                        self.tried_after_cooldown.remove(i)
                    
                    # 从thread_cookies中移除该cookie的所有引用
                    # 使用list()创建一个副本进行迭代，避免"dictionary changed size during iteration"错误
                    for thread_id in list(self.thread_cookies.keys()):
                        if self.thread_cookies[thread_id] == cookie:
                            del self.thread_cookies[thread_id]
                    
                    logger.warning(f"账号 {i+1} 已被锁定，设置冷却时间30分钟，剩余可用账号: {len(self.cookie_list) - len(self.blocked_indices)}")
                    break
    
    def get_status(self):
        """获取账号状态信息"""
        with self.lock:
            total = len(self.cookie_list)
            blocked = len(self.blocked_indices)
            available = total - blocked
            
            # 计算每个被锁定账号已冷却的时间
            current_time = time.time()
            cooldown_status = {}
            # 使用list()创建一个副本进行迭代，避免"dictionary changed size during iteration"错误
            for idx in list(self.blocked_indices):
                if idx in self.block_times:
                    elapsed_minutes = (current_time - self.block_times[idx]) / 60
                    remaining_minutes = max(0, 30 - elapsed_minutes)
                    cooldown_status[idx] = {
                        'elapsed_minutes': int(elapsed_minutes),
                        'remaining_minutes': int(remaining_minutes)
                    }
            
            return {
                'total': total,
                'blocked': blocked,
                'available': available,
                'blocked_indices': list(self.blocked_indices),
                'cooldown_status': cooldown_status
            }
            
    def try_unblock_accounts(self, cooldown_minutes=30):
        """尝试解除账号锁定状态，默认冷却时间为30分钟"""
        current_time = time.time()
        
        # 如果距离上次检查还不到5分钟，则不执行解锁
        if current_time - self.last_check_time < 300:  # 5分钟检查一次
            return False
            
        self.last_check_time = current_time
        unblocked = False
        
        # 尝试解锁
        with self.lock:
            if not self.blocked_indices:
                return False
            
            # 检查每个被锁定的账号，解除已经冷却足够时间的账号
            for idx in list(self.blocked_indices):
                if idx in self.block_times:
                    elapsed_minutes = (current_time - self.block_times[idx]) / 60
                    if elapsed_minutes >= cooldown_minutes:
                        logger.info(f"账号 {idx+1} 已冷却 {int(elapsed_minutes)} 分钟，解除锁定")
                        self.blocked_indices.remove(idx)
                        self.tried_after_cooldown.add(idx)
                        unblocked = True
        
        return unblocked

# 请求数据
@retry(max_retries=CONFIG['retry_times'])
def get_data(city_number, word, startDate, endDate, cookies, proxy_manager=None, cookie_manager=None):
    """获取百度指数数据"""
    thread_id = threading.get_ident()
    
    # 频率控制
    rate_limiter.wait()
    
    # 如果提供了cookie_manager，则使用它来获取cookie
    if cookie_manager:
        cookies = cookie_manager.get_cookie()
        # 如果所有账号都被锁定，无法获取cookie
        if cookies is None:
            logger.warning(f"线程 {thread_id}: 无可用账号，任务将被跳过或重新分配")
            raise Exception("所有账号都已被锁定，无法继续爬取")
    
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
        
    try:
        # 发送请求
        response = requests.get(url, cookies=cookies, headers=headers, proxies=proxies, timeout=20)
        response.raise_for_status()  # 抛出HTTP错误
        
        # 解析响应
        data = response.json()
        
        # 检查是否账号被锁定
        if data.get('status') == 10001 and data.get('message') == 'request block':
            if cookie_manager:
                logger.error(f"线程 {thread_id}: 账号被锁定: {data}")
                cookie_manager.block_account(cookies)  # 标记该账号为锁定状态
                # 立即重新尝试获取不同的账号
                return get_data(city_number, word, startDate, endDate, None, proxy_manager, cookie_manager)
            else:
                raise Exception("账号被锁定，但无法切换账号")
        
        return data
    
    except requests.exceptions.RequestException as e:
        logger.error(f"线程 {thread_id}: 请求异常: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"线程 {thread_id}: JSON解析异常: {e}")
        raise Exception(f"JSON解析失败: {e}")
    except Exception as e:
        if "所有账号都已被锁定" in str(e):
            # 不重试，直接抛出
            raise
        logger.error(f"线程 {thread_id}: 其他异常: {e}")
        raise

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
    thread_id = threading.get_ident()
    
    try:
        # 检查是否已完成
        if progress_manager.is_completed(word, city_number, year):
            # 减少日志输出，提高并行效率
            return True
        
        # 构建日期
        startDate = f"{year}-01-01"
        endDate = f"{year}-12-31"
        if year == 2025:
            endDate = "2025-06-23"
        
        # 只在任务开始时输出一次调试日志，减少日志量
        logger.debug(f"线程 {thread_id} 开始处理: {word} - {city_name} - {year}")
        
        # 获取数据，使用代理管理器和Cookie管理器
        data = get_data(city_number, word, startDate, endDate, None, proxy_manager, cookie_manager)
        
        # 分析数据
        df = analyze_data(data, city_number, city_name, word, year)
        
        if not df.empty:
            # 添加到批次管理器
            batch_manager.add_data(df)
            
            # 标记完成
            progress_manager.mark_completed(word, city_number, year)
            
            # 减少日志输出，只输出调试信息
            logger.debug(f"线程 {thread_id} 完成处理: {word} - {city_name} - {year}")
            return True
        else:
            logger.warning(f"线程 {thread_id} 数据为空: {word} - {city_name} - {year}")
            return False
            
    except Exception as e:
        logger.error(f"线程 {thread_id} 处理任务失败: {word} - {city_name} - {year}, 错误: {e}")
        return False

def process_group_tasks(group_name, tasks, progress_manager, batch_manager, proxy_manager, cookie_manager, results, account_manager=None):
    """处理单个账号组的任务"""
    logger.info(f"账号组 {group_name} 开始处理 {len(tasks)} 个任务")
    
    # 初始化该组的结果统计
    with threading.Lock():
        results[group_name] = {
            'success': 0,
            'failure': 0,
            'total': len(tasks),
            'thread': threading.current_thread()
        }
    
    # 创建线程池
    with ThreadPoolExecutor(max_workers=CONFIG['max_workers']) as executor:
        # 准备完整的任务信息
        full_tasks = []
        skipped_count = 0
        for word, city_number, city_name, year in tasks:
            # 检查是否已完成
            if progress_manager.is_completed(word, city_number, year):
                skipped_count += 1
                continue
                
            task_info = (word, city_number, city_name, year, progress_manager, batch_manager, proxy_manager, cookie_manager)
            full_tasks.append(task_info)
        
        # 更新已跳过的任务数
        if skipped_count > 0:
            with threading.Lock():
                results[group_name]['success'] += skipped_count
                logger.info(f"账号组 {group_name} 跳过 {skipped_count} 个已完成任务")
        
        # 如果没有需要处理的任务，直接返回
        if not full_tasks:
            logger.info(f"账号组 {group_name} 没有需要处理的任务")
            return
        
        # 提交所有任务
        future_to_task = {executor.submit(process_single_task, task): task for task in full_tasks}
        
        # 处理完成的任务
        completed_count = 0
        for future in as_completed(future_to_task):
            task_info = future_to_task[future]
            word, city_number, city_name, year = task_info[:4]
            
            try:
                result = future.result()
                with threading.Lock():
                    if result:
                        results[group_name]['success'] += 1
                    else:
                        results[group_name]['failure'] += 1
                
                # 计算进度
                completed_count += 1
                progress_pct = (completed_count / len(full_tasks)) * 100
                
                # 每完成10个任务或进度达到整数百分比时输出一次日志
                if completed_count % 10 == 0 or completed_count == len(full_tasks):
                    with threading.Lock():
                        success = results[group_name]['success']
                        failure = results[group_name]['failure']
                        logger.info(f"账号组 {group_name} 进度: {progress_pct:.1f}% ({completed_count}/{len(full_tasks)}), "
                                  f"成功: {success}, 失败: {failure}")
                
            except Exception as e:
                with threading.Lock():
                    results[group_name]['failure'] += 1
                logger.error(f"账号组 {group_name} 任务执行异常: {word} - {city_name} - {year}, 错误: {e}")
                
                # 检查是否是因为所有账号被锁定而失败
                if "所有账号都已被锁定" in str(e):
                    logger.critical(f"账号组 {group_name} 的所有账号都已被锁定，停止该组的爬取任务")
                    
                    # 取消所有未完成的任务
                    remaining_tasks = []
                    # 创建字典的副本进行迭代，避免"dictionary changed size during iteration"错误
                    for f, t in list(future_to_task.items()):
                        if not f.done() and not f.running():
                            f.cancel()
                            # 收集未完成的任务
                            word, city_number, city_name, year = t[:4]
                            remaining_tasks.append((word, city_number, city_name, year))
                    
                    # 如果提供了账号管理器，尝试重分配任务
                    if account_manager and remaining_tasks:
                        account_manager.mark_group_blocked(group_name)
                        logger.info(f"尝试重分配账号组 {group_name} 的 {len(remaining_tasks)} 个未完成任务")
                        account_manager.redistribute_tasks(group_name, remaining_tasks, progress_manager, batch_manager, proxy_manager, results)
                    
                    break
    
    # 最终统计
    with threading.Lock():
        success = results[group_name]['success']
        failure = results[group_name]['failure']
        logger.info(f"账号组 {group_name} 完成处理，成功: {success}, 失败: {failure}")

class AccountManager:
    def __init__(self, account_groups):
        """
        初始化账号管理器
        account_groups: 字典，键为账号组名称，值为该组的cookie列表
        """
        self.account_groups = account_groups
        self.group_tasks = {}  # 存储每个账号组分配的任务
        self.group_progress = {}  # 存储每个账号组的进度
        self.blocked_groups = set()  # 存储被锁定的账号组
        self.lock = threading.Lock()  # 用于保护共享数据
        self.redistributed_threads = []  # 存储重分配的任务线程
        
    def distribute_tasks(self, all_tasks):
        """将任务平均分配给各个账号组"""
        group_count = len(self.account_groups)
        if group_count == 0:
            return
            
        # 计算每组应分配的任务数
        tasks_per_group = len(all_tasks) // group_count
        remainder = len(all_tasks) % group_count
        
        start_idx = 0
        for i, group_name in enumerate(self.account_groups.keys()):
            end_idx = start_idx + tasks_per_group + (1 if i < remainder else 0)
            self.group_tasks[group_name] = all_tasks[start_idx:end_idx]
            start_idx = end_idx
            
        return self.group_tasks
    
    def mark_group_blocked(self, group_name):
        """标记一个账号组为被锁定状态"""
        with self.lock:
            self.blocked_groups.add(group_name)
            logger.warning(f"账号组 {group_name} 已被标记为锁定状态")
    
    def is_group_blocked(self, group_name):
        """检查账号组是否被锁定"""
        return group_name in self.blocked_groups
    
    def get_redistributed_threads(self):
        """获取所有重分配的任务线程"""
        with self.lock:
            return list(self.redistributed_threads)
    
    def redistribute_tasks(self, blocked_group_name, remaining_tasks, progress_manager=None, batch_manager=None, proxy_manager=None, results=None):
        """将被锁定账号组的未完成任务重新分配给其他账号组"""
        with self.lock:
            # 获取所有未被锁定的账号组
            available_groups = [name for name in self.account_groups.keys() 
                               if name != blocked_group_name and name not in self.blocked_groups]
            
            if not available_groups:
                logger.error("没有可用的账号组来重新分配任务！")
                return False
            
            # 计算每个可用组应分配的任务数
            tasks_per_group = len(remaining_tasks) // len(available_groups)
            remainder = len(remaining_tasks) % len(available_groups)
            
            logger.info(f"重新分配账号组 {blocked_group_name} 的 {len(remaining_tasks)} 个任务给 {len(available_groups)} 个可用账号组")
            
            # 分配任务并启动新线程
            start_idx = 0
            new_threads = []
            
            for i, group_name in enumerate(available_groups):
                end_idx = start_idx + tasks_per_group + (1 if i < remainder else 0)
                group_tasks = remaining_tasks[start_idx:end_idx]
                self.group_tasks[group_name].extend(group_tasks)
                start_idx = end_idx
                
                logger.info(f"账号组 {group_name} 新增 {len(group_tasks)} 个任务")
                
                # 如果提供了必要的参数，启动新线程处理这些任务
                if progress_manager and batch_manager and proxy_manager and results is not None:
                    # 创建该组的Cookie管理器
                    cookie_manager = CookieManager(self.account_groups[group_name])
                    
                    # 启动新线程处理这些新分配的任务
                    logger.info(f"为账号组 {group_name} 启动新线程处理 {len(group_tasks)} 个重分配的任务")
                    thread = start_task_thread(
                        group_name + "_redistributed", 
                        group_tasks, 
                        progress_manager, 
                        batch_manager, 
                        proxy_manager, 
                        cookie_manager, 
                        results, 
                        self
                    )
                    new_threads.append(thread)
                    self.redistributed_threads.append(thread)
            
            return new_threads if new_threads else True

def start_task_thread(group_name, tasks, progress_manager, batch_manager, proxy_manager, cookie_manager, results, account_manager):
    """启动一个任务处理线程"""
    thread = threading.Thread(
        target=process_group_tasks,
        args=(group_name, tasks, progress_manager, batch_manager, proxy_manager, cookie_manager, results, account_manager)
    )
    thread.start()
    return thread

def main():
    """主函数"""
    batch_manager = None  # 声明在try外部，使finally可访问
    progress_summary = None  # 声明进度汇总对象
    
    try:
        # 定义多个账号组
        account_groups = {
            "account_group_1": [# 18114461685
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
                    'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihdwitHd04Lvs3Nfz26Zt2honnQBqGZJ1+FooMMOy9VfBMHd4KSE2lo7q2jM/4leBJXqt+nMkIsYwpNA4XBVB5BGpKv8rf9RxKxeW8+CymWcpQ8qfiUvli8qcS/AH/6nfMYq1ZMQFVRuXQF6FC4JGmtin1ybbYbfSfzYRA9mCq3GnejGE5mAFoMKquZJvsf1FvjSGAIcnDl+H0Bfmo1ZE0Hy/Nk2eTwFYhuZsGjwCR7FVAPhMNMWL+Qlfaczl+PBQBDkVV8ysF/wnr6VWwUzKeq+NBDa593uSfHg6jo4zQ+k5UPBBx7NsZfzlUSbKaHt/szpDZmZbzEXZCOH7A43Q25NsmgYE289mszO99fMXxzLmdnvNXIEW2pwj4BXINSNFrPPV5wQJ1URP2/J3SSQnmckwFMb7+JFWxNGoA0JNiv6hCb0gkXpkEpISi6tVHh+hsQifjACGGz0MbLI9AAutvQNmLovQE8DrrUkOPSWZkiBwIUvxonSGS2lgiNZBxgK/Nad6P3sfvyvYhyXNwxm6SzH+Oja1l6cy9uoP7y446ILa1CLEOaV1jDkGoksNhRtn7B1VPovN1TRU04qLrmECuDGMBVR4vlhy8DqZQ1/LUEQ9mjyqP/SnZsRdyLAjuA3ESTcrCSmS6iWcmxBDT8gjuTbf5rG4+h0gsZ2eMGgzIHtuS4zhpfoAZYfd+R7pkXZXlVZsh4TITMtC54LZjiFwYUTw/8Vr7jyxVr5frOPWZM81V8YClTpPkuiWM0gZm41VCO+vNeIKxJyJ0hcHJ83oQN1+3jtOOi8LxWmDSZzbPJDJU9Bq7zt2A9A8E851l8QtBoQFIuWEGY3DMQGzE4fLtBnD2IBA1xgIrbF95h/aKYBNVXdvBhoLwXhcnXaiqXEpcvFQlonIv85FfaVbfEoKujQX2IBA1xgIrbF95h/aKYBNVh6Y0NjEKZ13xldTgKDiG2QRBJFTPsviSSEvgLGRO3YgGOv+/I3nwGp9q5hLF8/07goRUnieOy9WY3CCu1FKQrXv4Kl2tvhm/51VQHSSoTtFbHhSGlEKo+S0ciyUHoRYU',
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
            ],
            "account_group_2": [# 15968588744
                {
                    'BAIDUID': '0437E9BF4224765A2BB8C862C24687D5:FG=1',
                    'BAIDUID_BFESS': '0437E9BF4224765A2BB8C862C24687D5:FG=1',
                    'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750771421',
                    'HMACCOUNT': '1EC551B6460E8184',
                    'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihdwitHd04Lvs3Nfz26Zt2holplnIKVacidp8Sue4dMTyfg65BJnOFhn1HthtSiwtygiD7piS4vjG/W9dLb1VAdqMysqdImJFnhAMv/fWi1I5VO0V6uxgO+hV7+7wZFfXG0MSpuMmh7GsZ4C7fF/kTgmvlMIA/tB2qdnJ8KkulgesR5YKU+qTqtaaBkWIZO5dn/GldC1S4QUhUhpm5KMoOoF81v2iwj13daM+9aWJ5GJCQM+RpBohGNhMcqCHhVhtXpVObaDCHgWJZH3ZrTGYHmi7XJB9z3y2o8Kqxep5XBCsugNOW5C73e/g54kuY4PKIS71bGmnPunNtMIatWdCpBi6yoMEZCNh1huwbMdWwuuXVnvNXIEW2pwj4BXINSNFrPHKL0yGxCa0DTjN6SHq8QhCIGhYqrYfhHGZqJNx2uWmglAIQEZY21OyYDgpfKN3zxRn6ONqHK83MkBENWBMWSAwea/+1VSNUTGfIG+NKu2s+g28sOzjnLUnUE9KukMAMTPZYfT79sbFYuntY0Ry6GX3OsRAJVdXPXKlPRQiighN2h3utZNfUsAGL2WWa3tubT9td9rGfOenGkLOGCRladXTg1IKPDQ9z3/DiqHtAIbmyu3emEg6nEYu6lQuvYr6/UJpAq7e+CnVRC2DzwICP6cu9A5mNm34ZPuoRV+zY3FkhMa5PpAytGwAf1nqFDiyU+WHcGDy5llZtI5Ig4rvXzcdIxeODdssbd+W/AgOwxO3JdRGSluqM4FuAgHCvdnqfGnnbe3vsHq3LuF7pombT65cVprejPaivGVaWugm+VA1kVl5OE/aBXOg67P9UlCyJKVyutwgoMp5Aa/ZkjblrEvPdXZFhAgvw25kAwV0TwSXSe5Q/vbh3nl529wNGdJ0E/Al3XsmHJdLSZ9wC3mJe+ZNDrSwzO8uzPTGJRstuhQcx/x5a3E+Qkao4W1aMhW15Bgywf8BpImierD5YuJm8aNh+b2nRqUTK6NqmhPLvsfMNxShTXBRJdrnFL9nqFcSvY6cuLQt09VwaPPyWktx1V5J+b2nRqUTK6NqmhPLvsfMNZ/k8RFFJMWot30FNQcvJjgmLcRAsZA9ozVp4fEbVslkfSzVKL8rDNNpNjO7rOJCKUwXtmNU/nsKC0PSzAP3Kq4wL4SK3t1tHw4eMSEHL2FCmmrSArB56dw/GBL+N3SuP',
                    'BDUSS': 'BMbG01UHpSNDY3MjhqYTF5Zn52dlFUVXV4eGV-bE42WkVwSkVHV05sakI0SUpvSVFBQUFBJCQAAAAAAQAAAAEAAACSeU9mTHVja19mZjA4MTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMFTW2jBU1toRn',
                    'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05008281311rMb1A9IG0Y7arSh3ElcF5U9ZmIY%2FiGmrI6wx44%2F8juPz%2FcFAsquFJfDmaXeLVCL9Qg2TcREiSVddkVEveIl1xCD2B6yVZZR2HzSKiKpigcW1bmmBtvVfwOsFjAByyTymUI36%2BAGNMtQuxXKR0lxKKcHKzOqUstqiwMlxc71DNRikuNz5ezjrXBMJj3kJzZ4BPJ4MPAgPHKBdFcyuLOJqhkGy4jQiFr1HYylSfhJYe649Pq0CetwLJXjouAX%2BX4FIeMlEBbk563ZRvuLB8Sv0kA%3D%3D94345733970954583999839931689454',
                    '__cas__rn__': '500828131',
                    '__cas__st__212': '8922ec26455bfdabc30a2e2ff8271c68cbbd82a6ecf99335b83a0f261f17f01c663698577d1fb00c08ff601c',
                    '__cas__id__212': '69553869',
                    'CPTK_212': '854404927',
                    'CPID_212': '69553869',
                    'bdindexid': 'gp7b4tja8pevijpp93hctpopd0',
                    'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750815688',
                    'RT': '"z=1&dm=baidu.com&si=d48f2b07-2742-49bd-8b6f-37bbc6dcd087&ss=mcbaf2i5&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
                    'ab_sr': '1.0.1_NDM0ZjViNmY4MmUwM2Q2ODgxOWY5NDgzNzI2NGYwNzc2N2ZmNDI4OThhNjI1MjllZTk1MzcwNGNhNzhjY2FjYjMyZDRiNmVjM2VkMGY3NjQ4Y2M2YTBiNTU4MWQ2MzE5YThmZjEyYThiNjJmZWEwMTU2NDZkN2JkNzM0NWI3N2JkYjJhNTdiOGY3MjRmYTczZTMyZDA1NzFmNTRkZDA2NQ==',
                    'BDUSS_BFESS': 'BMbG01UHpSNDY3MjhqYTF5Zn52dlFUVXV4eGV-bE42WkVwSkVHV05sakI0SUpvSVFBQUFBJCQAAAAAAQAAAAEAAACSeU9mTHVja19mZjA4MTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMFTW2jBU1toRn',
                }
            ],
            "account_group_3": [# 18860961079
                {
                    'BAIDU_WISE_UID': 'wapp_1744869667916_527',
                    'BAIDUID': 'FF85DF65CC7463F3726D5301B69C0672:FG=1',
                    'BAIDUID_BFESS': 'FF85DF65CC7463F3726D5301B69C0672:FG=1',
                    'PSTM': '1744882843',
                    'BIDUPSID': '950D047CF79B4A0F8F86462CD08D849F',
                    'ZFY': ':AYs:BOm:Ajfa1cQtiOrSJADVlDld3:BYmMcahDksItTkOQ:C',
                    'H_PS_PSSID': '61027_62325_62485_62967_63042_63044_63140_63074_63189_63194_63210_63226_63242_63244_63249_63253',
                    '__bid_n': '18c42450fcc02886ca93f5',
                    'BDUSS': '3ZlcTY5VmdtR055LS0yWUZIekVwaXpQdlhhZTVWNkQ1RjJZd1Z2RjZlMnZKb0pvSVFBQUFBJCQAAAAAAAAAAAEAAABKXe14tuS25MCyxL625AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK-ZWmivmVpoa',
                    'bdindexid': 'lbjajepvj48ik2npi9efsppm32',
                    'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750687271,1750768658',
                    'HMACCOUNT': 'DDF927EE5DF25454',
                    'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05007811055iHW74BOJZpR8fIXeOGeBx5M6y7phE8fVUA6A5%2FT9V%2FlsHxmc8X4j0VNC%2F9LwP2zmQdfNMKxnxGOsso9i6z5EBqAppSnxsfJ24BKZ2HbQq2iyXFknWsLKsmgGjJw1B4gnKBPQaKQ17uqsRk7kRjIMxMQ9I09xx2H5mLprCONYZIbGfHaYp1BTvGG6rrGQtybXmNaMwxxsWVpk5FXOZ9eQ4K3Wkdor%2FZuxF6vZoZZboMBLW7wT1x8%2FnAf2M49uCYlG7sR%2B%2F2vpsj8pGF1p7tZvY9RSVz9Zuo7VoVT643%2FkQeIjx7VwkUgLo5BwXQ4wGzR60WWFDjO93A1KqcAW0Cufkg%3D%3D19042442273391681046897992923981',
                    '__cas__st__212': 'bbc20157a0eb310bf75a06fe47852349e3fdc208669fbd29ee3ef0f2081a8a25ae8d802c8eff57ed1747ef5a',
                    '__cas__id__212': '69563296',
                    '__cas__rn__': '500781105',
                    'CPTK_212': '1747583717',
                    'CPID_212': '69563296',
                    'RT': '"z=1&dm=baidu.com&si=454d90be-3dae-4ce7-84a2-ab2e9d648c5d&ss=mcbaf2i5&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
                    'BDUSS_BFESS': '3ZlcTY5VmdtR055LS0yWUZIekVwaXpQdlhhZTVWNkQ1RjJZd1Z2RjZlMnZKb0pvSVFBQUFBJCQAAAAAAAAAAAEAAABKXe14tuS25MCyxL625AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK-ZWmivmVpoa',
                    'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750816072',
                    'ab_sr': '1.0.1_NDQ4MjFmZWIxYjFhNjAwYzk2NjM2YzZkYTc5ODk1MmM4YTA1Yjk2ZTgzNjE5OWQ1YzMwOGZiOGQ2OTUyODAzMjk5NjE5MDJiNzdkOTkxN2JlNTU5MDQ2MjY0NGZlZTFhMmI3N2E2ZjRlODhjZmY3OTQzZGY1YTRlYjMzYzUzYjgwODk3ZTg1MmE2OTdmZDY3YzQyN2NmZGNiNjk1MTdjZQ==',
                }
            ],
            "account_group_4": [# 张国建老师
                {
                    'BDUSS': '1QWW1LZnJFWDVPN350SDV6dWJTZHRNWnhWeEFjSVpPckduLTRMakQyRGhoa1ZvSVFBQUFBJCQAAAAAAAAAAAEAAABGVUcnzOy6o9PAs7oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOH5HWjh-R1oM2',
                    'BAIDUID': 'E8C2F89B2338E88F38F4D0A154FC1B64:SL=0:NR=50:FG=1',
                    'HMACCOUNT': 'B14ADDE7C745CD61',
                }
            ],   
            "account_group_5": [# 15950590655
                {
                    'BAIDUID': 'BB069E74A97B4457314AF9E557A775B5:FG=1',
                    'BIDUPSID': 'BB069E74A97B445759DF452FC47CF33C',
                    'PSTM': '1750817887',
                    'H_PS_PSSID': '60279_62327_62831_63144_63326_63403_63513_63567_63563_63583_63576_63639_63274_63646_63653_63684_63691_63724_63720_63749',
                    'delPer': '0',
                    'PSINO': '5',
                    'BA_HECTOR': '810l810g812k25848g84ak05250g0k1k5mn3125',
                    'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
                    'ZFY': 'Ys35EjG1tLOOy87JpBudB4kv2T3jlkknwwJRbbpCoWs:C',
                    'BCLID': '5868022272419550351',
                    'BCLID_BFESS': '5868022272419550351',
                    'BDSFRCVID': 'Jn4OJexroGWgCqbsSnoxMMnrkopWxY5TDYrEOwXPsp3LGJLVvXWoEG0Pts1-dEu-S2EwogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0M5',
                    'BDSFRCVID_BFESS': 'Jn4OJexroGWgCqbsSnoxMMnrkopWxY5TDYrEOwXPsp3LGJLVvXWoEG0Pts1-dEu-S2EwogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0M5',
                    'H_BDCLCKID_SF': 'tRAOoC8-fIvDqTrP-trf5DCShUFsBtCJB2Q-XPoO3M3JEPjPKpb_hnkIXfTHa-RjQ5bk_xbgy4op8P3y0bb2DUA1y4vp-qvUa2TxoUJ2-KDVeh5Gqq-KQJ-ebPRiWTj9QgbLMhQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0HPonHjL5Djv33j',
                    'H_BDCLCKID_SF_BFESS': 'tRAOoC8-fIvDqTrP-trf5DCShUFsBtCJB2Q-XPoO3M3JEPjPKpb_hnkIXfTHa-RjQ5bk_xbgy4op8P3y0bb2DUA1y4vp-qvUa2TxoUJ2-KDVeh5Gqq-KQJ-ebPRiWTj9QgbLMhQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0HPonHjL5Djv33j',
                    'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750817896',
                    'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750822823',
                    'HMACCOUNT': '27C1B7F9FD18913C',
                    'RT': '"z=1&dm=baidu.com&si=5832934a-e70e-45ad-9bcd-836faf2d1ea5&ss=mcbeoy3k&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
                    'ab_sr': '1.0.1_MGM3NzdjZmVhMmUyOWI4NDczMzQ2ZDYzNDYxYmU1MDFiYWFhYWQ4YTc4ODE3NmIxYjcwOThjMTgyOTU5NjQyYTE1OGM2Y2UxM2QyMDQyYmMxYTQ0NDllMTU2NjVkM2NjNWI5YTdhNzU1MzgxZGY3YjI4ZjY1M2Y5ZjQzZTZiNGU1ZjFlMDQwZDk2ZjdkMTJlMTQ4NDFkMmRkODJmMmJhOQ==',
                    'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihd0enHWGiHNa8jc3p2YbsY9BJz/l8wKWpVe71o56icb5WJpuXZiPIDDB1PsImjYrujSNfb+bWJc++UzD3f3/si633O1Nvov0ewgGWYj3KlR//Yvc91cDLyteMW0POvLzphByqmnXQFcEK1EAvma7KU4MDN3WmJY/NWBcNvpqdRBdKrEEfvwQKWpWE08OG0Oa852CXWQYpvBie32q9dmRfwfjHu7PS+78rSATuF9ZmxajHuK36gVAlel31+rZpX2v1w0G3gqifdSzT35NQlL/KGVZl29TNM8Tn9jGWq9feGmPlmfSlGcsA4Zw7tT4tSNMvZNUOzo1AK/5AiuC5hwc5h6SJpPqKnTWDeDxWVlsOQQ+px2RTt0mgeBku85QaxtnC5vJU0ZdfSWHGHKr8tz/+dJsaVg8FFAuKbyjhfXvqcDau5eh8yhGcgjFA3flugImpLGIrvuAAM+9jpzEH4AMjVG1tyMsy+XPlAYbfO1lIoDmPWpXCLkfp9YMJ/g5n97pwE2Brb9MypgKINzcvcBWIkP4HSkq0fQ9uR0sKy0MiHuUCk5CkpWOp1Xr/DIWk9wFD8KCJLToVpiOq1G0BHRvSH1+YLQpEgFjmQoey69Fz+kM7Y5cg925MGCeBU4jWp2g2g3MZ7/q5Nm5qKyRlsnUZctqOY+iIuQVwXDu+NPsd2Gs5cOoZ68Hq8cNrmezkUtisZ7jbCSee7nPW0+PyJuXQBghmXwRbrJcGaELL9QLspNgqMM0aOdAredMfLeYMj+uN0MK5mpzYSmDsgYAGcZbGmnun8qe7C/Z6wAh6Sxpet2o2XdT5gjozQON5/HVPvKJVz/HEk0MlL4OWxuq7efgjrm7u8eNg3xj0WwQipSI+BocHNo9YRuQO2pi4iArzUvik/DxSHbvZCfaziGZggaG+BY2OEydWPa1CZLO/GyxE2lrKfp8o7MtQH8zZ7JAK2DmuATYE6knbkS7/y5uZBK5lY9wL+toPXRBoL0qepeNu3r3x',
                    'BDUSS': 'ZGY1NEMThRV21hOTNRUUNlYWVrc1U0UHRIVERCTFpWenBHY0N-VVpDLVR-SUpvSUFBQUFBJCQAAAAAAQAAAAEAAACr6JWZ0KG1sLWwMDgxMgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJNvW2iTb1tofj',
                    'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05008352533z3UFWXdlVsvPwYeSqkUGPpq0vV39sLthRTWOevCXrB4%2F6bAX3dyX2KSuxYhnrvE0uHEKv8FO3Puy4p8iwxa2bQ2QUJ3f%2BGaytKmUHbhezVJNG9eX%2Be3XIftTHEbALlmcM6E%2BrsEK%2FhlkIR%2BYnH38RDRAzvxJE0Bw8tIPEdI%2BuUvlr7gg4wFwCwKZDCi%2BvEmfKoa%2BrviCuTEAs9Wtr%2BeIMUcr7jeB9QithCHC6PaEbgIFAEhOekK%2BnTnt%2B7r1ADKl7o4zze3yDaBK4BluMY4XwCBogLA4MC6DcU16%2FMxMPBewADQMTuEY03qLD989qYbs23484171432709265225849181739678',
                    '__cas__st__212': '888a9c12f768d1f9293a364c3b0e0ece65eff5e50fbbfe5e014479ecf48c484769b094d1a2f3a6eadcd65970',
                    '__cas__id__212': '69574836',
                    '__cas__rn__': '500835253',
                    'CPTK_212': '490965985',
                    'CPID_212': '69574836',
                    'bdindexid': '15lrb5hef6t0i16h0g6j50o7v4',
                }
            ],  
            "account_group_6":[ #gwb
                {
                    'BAIDUID_BFESS': 'E52624072E8C2748B58A33D56C74D2BD:FG=1',
                    'BAIDU_WISE_UID': 'wapp_1742225288708_994',
                    '__bid_n': '1961127fbb7753622ae024',
                    'BDUSS': 'zJoOWV-SWZuQlAzQlRIMjhtWXI1Y1MtLUt1QTBxN0Jua0d5SH4tTEMxdkhkak5vSVFBQUFBJCQAAAAAAQAAAAEAAACP60d6AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMfpC2jH6QtoV',
                    'ZFY': 'Bj7F3PpiC4TawLboy4uR2qTGSwN3UHL2k2fPQPgbO3A:C',
                    'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750829591',
                    'HMACCOUNT': '2B61E22BE976E512',
                    'bdindexid': 'kf60ks6q5oo6gqgkarnfn1vhv7',
                    'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05008420411GZ2K8WAlnZ5cahRy1Opj6sfC5kTpKu2LA1zaVryIRAXz0PAenC2H2kNLwQsAkqogzLwjx^%^2Fv7BT2iNGJa0Nvl9BMU4PpaqO0T2bmE26iuH3xnZunBwvPTlVPqkuYkoAti9h6^%^2Bc34HcovgGTk^%^2B5Gm5^%^2FttR^%^2FTVYnISooqNPaju0rbs^%^2Fn9hRl^%^2FKmgx7g23NtkaT7ljdgtz7ZRtX^%^2B0n4wPpOx7XdoFhQjZmZ1am^%^2Bc0UgYmqqot8TmXaCDMlLzYGgcYFC2VU5bKDUKep^%^2F2OnQYIf7CmsBU4AvHq6kbYnH7SgjQmL8^%^3D58061619596105409221903586651799',
                    '__cas__rn__': '500842041',
                    '__cas__st__212': '5004bd2d7c9fb23b843ebe1bff7f1567fca528259b059a898d1d8c6e01bacfb1e4da501fca468a9f274e84d1',
                    '__cas__id__212': '69606588',
                    'CPTK_212': '413968405',
                    'CPID_212': '69606588',
                    'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750829803',       
                }
            ],
            "account_group_7":[ # jbw
                {
                    'BIDUPSID': 'AB0605F82B2079C8C5A1E5364B252D09',
                    'PSTM': '1740833878',
                    'BDUSS': 'cyOEpSejhqMnl2ZUlxaHZGUUs1MEN1dG5kWUc0ekpCS1FGOGw3Zm9UQUgxfnhuSVFBQUFBJCQAAAAAAAAAAAEAAAC-JbMxc3QwbmllAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAdK1WcHStVnMF',
                    'MAWEBCUID': 'web_tzegyGKkSamsoaIQfizrJCOefVWiigezZtBnZFYuZvxAnuYAYI',
                    'MCITY': '-%3A',
                    'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
                    'BAIDUID': 'E65F507D5A349CFF9EABC848D4C1FBF6:SL=0:NR=10:FG=1',
                    'H_WISE_SIDS_BFESS': '62325_63140_63567_63563_63583_63576_63618_63636_63275_63646_63659_63677_63692_63725_63717',
                    'H_PS_PSSID': '62325_63140_63563_63583_63576_63618_63636_63275_63646_63659_63692_63725_63717',
                    'BAIDUID_BFESS': 'E65F507D5A349CFF9EABC848D4C1FBF6:SL=0:NR=10:FG=1',
                    'log_chanel': 'seo_qadetail',
                    '__bid_n': '1974d056f320288ea181aa',
                    'BAIDU_WISE_UID': 'wapp_1750823162445_952',
                    'BA_HECTOR': '25850g8h8g2l2k0l0k0k8h218085an1k5muiv24',
                    'ZFY': 'LXSty0styX3hNQclkCgj2jDj6qTPaVz5OljhGyJUcnY:C',
                    'H_WISE_SIDS': '62325_63140_63563_63583_63576_63618_63636_63275_63646_63659_63692_63725_63717',
                    'bdindexid': 'jbdlaprsmrrqbn4nrak2a45vg6',
                    'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05008433033yLAJbFdMUyP8M7Hs%2Brk2Aptd7SiLddNong65G6qlu8JFnxK21SWZ%2BGD1ai47aOMOE%2FRbWUJ5PzdUSFRNLCzZ65SyB%2Fo7ti8nWOciXQxqlj9T6Jvtqzc2j4rClfIBOdr6Ut40yWkooYTY4wMc%2BsebuLi4zwNgKCFBdCo5mgIcKgB7LPQk12ExDenOVn60mWAtuQxUA26S5HTUFqxE4zxL%2BptMZewNGE351xfQUsr19C7S2HSzPEQgw5pOcxh1ZKPz6gdQw9BjQ3lETgep7aohew%3D%3D05874955142039816981701466845642',
                    '__cas__rn__': '500843303',
                    '__cas__st__212': '9f2a188411d1407ae4ea978f96fc497c9485b7d5f37172465525f11f1f469c207bf20d285cf23632c281dd7e',
                    '__cas__id__212': '69607373',
                    'CPTK_212': '1335003607',
                    'CPID_212': '69607373',
                    'RT': '"z=1&dm=baidu.com&si=2f786486-513e-41c2-911b-814aa7189bd9&ss=mcbjhduf&sl=2&tt=4gq&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
                    'ab_sr': '1.0.1_NmE5ZjQyOGQ3OTJkMzQ4ZDRmZTlkNTE2NjRjNzRiOWFjMWIzMWE4YTM4OWI1M2UyNDlkNTc2NmU3ZjEwNWE1YzRiYWJkOWM0N2QyNTc4MGY4MzRhYzFmOWM5MGQxMWVkMjdjODA1ZDE3NmZiNDNjMGRmM2ZlYTU0YmVmY2MyOGEwMjc5MTlhNjdkYzQyNmMwNWQyNzAzNzhlZDgzNTg2Yw==',
                    'BDUSS_BFESS': 'cyOEpSejhqMnl2ZUlxaHZGUUs1MEN1dG5kWUc0ekpCS1FGOGw3Zm9UQUgxfnhuSVFBQUFBJCQAAAAAAAAAAAEAAAC-JbMxc3QwbmllAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAdK1WcHStVnMF',
                }
            ],  
            "account_group_8":[ # 妈妈
                {
                    'BAIDUID': '93130EF96DA886E8003BA7591E93216A:FG=1',
                    'BAIDUID_BFESS': '93130EF96DA886E8003BA7591E93216A:FG=1',
                    'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750817945',
                    'HMACCOUNT': '0786A047F830F07B',
                    'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihdwitHd04Lvs3Nfz26Zt2holplnIKVacidp8Sue4dMTyfg65BJnOFhn1HthtSiwtygiD7piS4vjG/W9dLb1VAdqO71sNtrfJH2UrRokTvezUwO0V6uxgO+hV7+7wZFfXG0GCyVhyn+t8xbPWkfFyVoPmJ22c9Ug13XZOliEMC05vZZ77btup0W8HDa4x5wBW4KUIYL7ubmYEYlZiivYWEOqpfF7ozSx2WUjlOduTlsW9EzZNnk8BWIbmbBo8AkexVQH/dl84vw+R1Dcfej0yqc+Terld8wjGrZonj8gE2rhKeVRKCfkBUbih20ajKSj+uMYsCx0BvEXLwO1q8FEfRhlJmGeXOUcw93X11sNGWvmEfXsCOOEd92gV8y8Vvj+JNyQSboWtpcXid0tljotqyzsji/2M6q3zPK1Wo+8n7iPU1MqbhDMFoOt7qoyB+htm3rbJPA5KGT8o1URIxJNebk4sfjEwqD5L6ysH6oaiSfWAIq5mds/qgPQwTUKr/Kgrl35NvPdjn/bCrvcI9uY483nqRL6LzHBhVCnFiYt5qOVEdblwzL2ZX24BwNPZkinid6zttTyx6kW2BH//OSFswrj8kE+hNVmgRBbJ0I/xFKLJ2QwdZGmF7oqqViE/4ynC2CTVf0EUKc/TsS9laaV4lYdBuM/96pgH5QsfKw7REIWEl+7cU2GfHS8QIfv9EPuM4ElnGnZH3TOGDfIrtA3G4p0onlU9kkR0ClLVHTvf2xIh7f6dEr8ykUagxnw/9Xas1DmwECJlWpG6YOr7NXdyKs51qWCN90OY6m+jpOxBQ4wDO7lUU65gYEbbJ+tZkSSfcCbgdgXHnYC1cITJ41Q/15EVlsKzcG2FfJWn6enEH2VIfcCX6SR/qPB2aUOs8a30/f3iYuErxyZrTU5B4SqWEeCSNkURYtyQCZlyILbGgoXSK3JFq5WutfXiXVWYzpJZIrDDNGjnQK3nTHy3mDI/rjdDCuZqc2Epg7IGABnGWxpp7p/Knuwv2esAIeksaXrdqNl3U+YI6M0Djefx1T7yiVc/xxJNDJS+Dlsbqu3n4I65u7vHjYN8Y9FsEIqUiPgaHBzaPWEbkDtqYuIgK81L4pPw8Uh272Qn2s4hmYIGhvgWNjhMnVj2tQmSzvxssRNpayn6fKOzLUB/M2eyQCtg5rgE2BOpJ25Eu/8ubmQSuZWPcC/raD10QaC9KnqXjbt698Q==',
                    'BDUSS': 'hGYS1mNHl5NVFEVHlMUX5hWjhIVmpRbVEyWVpHWDBUbH41eEdjeUdvWWdHWU5vSUFBQUFBJCQAAAAAAAAAAAEAAAA72va1yOvEpzg4NgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCMW2ggjFtoSD',
                    'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05008425611BYRDi1ELcYXThg8DUVv0l%2F%2BkC2LWwdeeGO18egaMDv0xAAkzI8bmavQDfocHi01ArJ5bGdvMKEH%2FTMxpG3Xapttk3rkO0QW45AmcD6Z78DnNXz%2FofWNo%2FW8BMis9g1eQ5OL8Tx228%2BdP9FqrQR01QSreFQEhiZ8Q%2FqdQHpqRbh%2BDp0fzRYhE8eQXiZA%2Fnc3OvVimb%2FH2w9nQuHMT84so0mBVGs%2B09QmPTrl3VRcX8S6nU3PcKN9xiEkFcNveSYoIwB1BpIba6vS3ZJIyaYDGlgB6uZMmbkCAQi4c2jO1SbI%3D82983210130847024551183059627376',
                    '__cas__rn__': '500842561',
                    '__cas__st__212': '7ee3cb8ce483b806b26908aa4a57712ca4f1d512377c34440b5add1dfbe9abe7855b9989e3ca96c8a73a17e9',
                    '__cas__id__212': '69581500',
                    'CPTK_212': '683861019',
                    'CPID_212': '69581500',
                    'bdindexid': 'rtj08rfoonq6s4blqm2tle0hn3',
                    'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750830351',
                    'RT': '"z=1&dm=baidu.com&si=790ffdd1-25f7-4260-a844-fe5d06e89088&ss=mcbj1lkt&sl=1&tt=ng&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
                    'ab_sr': '1.0.1_YTc3ZGU0MWE0YzdhMDZmMDdjY2E5ZDM4NjViYzE2ODQwY2JkZmVjMjI1ZGE3YzcxNzdhN2Q4MTgyZjJkMTRkOWNmMDA3NzE2MDNjMjQ5NTEyZmRmZDdkZjRhYjgzOTc4ZTZiNTIzMjkzZDMxODI0NGMyNjk5ZDc3ZGMyMGE1NWE1NTM3ZjU0ODBlMGVjMTAxNzlkMzdmNDgwMTRkN2JkMA==',
                    'BDUSS_BFESS': 'hGYS1mNHl5NVFEVHlMUX5hWjhIVmpRbVEyWVpHWDBUbH41eEdjeUdvWWdHWU5vSUFBQUFBJCQAAAAAAAAAAAEAAAA72va1yOvEpzg4NgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCMW2ggjFtoSD',
                }
            ],
            "account_group_9":[ # fkc
                {
                    'BAIDUID': '93130EF96DA886E8003BA7591E93216A:FG=1',
                    'BAIDUID_BFESS': '93130EF96DA886E8003BA7591E93216A:FG=1',
                    'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750817945',
                    'HMACCOUNT': '0786A047F830F07B',
                    'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihdwitHd04Lvs3Nfz26Zt2holplnIKVacidp8Sue4dMTyfg65BJnOFhn1HthtSiwtygiD7piS4vjG/W9dLb1VAdqO71sNtrfJH2UrRokTvezUwO0V6uxgO+hV7+7wZFfXG0GCyVhyn+t8xbPWkfFyVoPmJ22c9Ug13XZOliEMC05vZZ77btup0W8HDa4x5wBW4KUIYL7ubmYEYlZiivYWEOqpfF7ozSx2WUjlOduTlsW9EzZNnk8BWIbmbBo8AkexVQH/dl84vw+R1Dcfej0yqc+Terld8wjGrZonj8gE2rhKeVRKCfkBUbih20ajKSj+uMYsCx0BvEXLwO1q8FEfRhlJmGeXOUcw93X11sNGWvmEfXsCOOEd92gV8y8Vvj+JNyQSboWtpcXid0tljotqyzsji/2M6q3zPK1Wo+8n7iPU1MqbhDMFoOt7qoyB+htm3rbJPA5KGT8o1URIxJNebk4sfjEwqD5L6ysH6oaiSfWAIq5mds/qgPQwTUKr/Kgrl35NvPdjn/bCrvcI9uY483nqRL6LzHBhVCnFiYt5qOVEdblwzL2ZX24BwNPZkinid6zttTyx6kW2BH//OSFswrj8kE+hNVmgRBbJ0I/xFKLJ2QwdZGmF7oqqViE/4ynC2CTVf0EUKc/TsS9laaV4lYdBuM/96pgH5QsfKw7REIWEl+7cU2GfHS8QIfv9EPuM4ElnGnZH3TOGDfIrtA3G4p0onlU9kkR0ClLVHTvf2xIh7f6dEr8ykUagxnw/9Xas1DmwECJlWpG6YOr7NXdyKs51qWCN90OY6m+jpOxBQ4wDO7lUU65gYEbbJ+tZkSSfcCbgdgXHnYC1cITJ41Q/15EVlsKzcG2FfJWn6enEH2VIfcCX6SR/qPB2aUOs8a30/f3iYuErxyZrTU5B4SqWEeCSNkURYtyQCZlyILbGgoXSK3JFq5WutfXiXVWYzpJZIrDDNGjnQK3nTHy3mDI/rjdDCuZqc2Epg7IGABnGWxpp7p/Knuwv2esAIeksaXrdqNl3U+YI6M0Djefx1T7yiVc/xxJNDJS+Dlsbqu3n4I65u7vHjYN8Y9FsEIqUiPgaHBzaPWEbkDtqYuIgK81L4pPw8Uh272Qn2s4hmYIGhvgWNjhMnVj2tQmSzvxssRNpayn6fKOzLUB/M2eyQCtg5rgE2BOpJ25Eu/8ubmQSuZWPcC/raD10QaC9KnqXjbt698Q==',
                    'BDUSS': 'hGYS1mNHl5NVFEVHlMUX5hWjhIVmpRbVEyWVpHWDBUbH41eEdjeUdvWWdHWU5vSUFBQUFBJCQAAAAAAAAAAAEAAAA72va1yOvEpzg4NgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCMW2ggjFtoSD',
                    'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05008425611BYRDi1ELcYXThg8DUVv0l%2F%2BkC2LWwdeeGO18egaMDv0xAAkzI8bmavQDfocHi01ArJ5bGdvMKEH%2FTMxpG3Xapttk3rkO0QW45AmcD6Z78DnNXz%2FofWNo%2FW8BMis9g1eQ5OL8Tx228%2BdP9FqrQR01QSreFQEhiZ8Q%2FqdQHpqRbh%2BDp0fzRYhE8eQXiZA%2Fnc3OvVimb%2FH2w9nQuHMT84so0mBVGs%2B09QmPTrl3VRcX8S6nU3PcKN9xiEkFcNveSYoIwB1BpIba6vS3ZJIyaYDGlgB6uZMmbkCAQi4c2jO1SbI%3D82983210130847024551183059627376',
                    '__cas__rn__': '500842561',
                    '__cas__st__212': '7ee3cb8ce483b806b26908aa4a57712ca4f1d512377c34440b5add1dfbe9abe7855b9989e3ca96c8a73a17e9',
                    '__cas__id__212': '69581500',
                    'CPTK_212': '683861019',
                    'CPID_212': '69581500',
                    'bdindexid': 'rtj08rfoonq6s4blqm2tle0hn3',
                    'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750830351',
                    'RT': '"z=1&dm=baidu.com&si=790ffdd1-25f7-4260-a844-fe5d06e89088&ss=mcbj1lkt&sl=1&tt=ng&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
                    'ab_sr': '1.0.1_YTc3ZGU0MWE0YzdhMDZmMDdjY2E5ZDM4NjViYzE2ODQwY2JkZmVjMjI1ZGE3YzcxNzdhN2Q4MTgyZjJkMTRkOWNmMDA3NzE2MDNjMjQ5NTEyZmRmZDdkZjRhYjgzOTc4ZTZiNTIzMjkzZDMxODI0NGMyNjk5ZDc3ZGMyMGE1NWE1NTM3ZjU0ODBlMGVjMTAxNzlkMzdmNDgwMTRkN2JkMA==',
                    'BDUSS_BFESS': 'hGYS1mNHl5NVFEVHlMUX5hWjhIVmpRbVEyWVpHWDBUbH41eEdjeUdvWWdHWU5vSUFBQUFBJCQAAAAAAAAAAAEAAAA72va1yOvEpzg4NgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCMW2ggjFtoSD',
                }
            ],
            "account_group_10":[ # tqh
                {
                    'BAIDUID': '8B4C40F37A023F26D4310F9C9A7B2377:FG=1',
                    'PSTM': '1736560135',
                    'BIDUPSID': 'F3CB31A2E97BC1DB49A50F9204947BE2',
                    'H_WISE_SIDS_BFESS': '61027_62130_62125_62169_62325_62339_62347_62329_62363_62372_62393',
                    'BDUSS': '094U0VYYWFzVFRYbXRQc1RmNmpFMnZNUVFyRkhjQVRPdWJKQmJJWVdkb09xfjFuRVFBQUFBJCQAAAAAAAAAAAEAAACp9ZpfzfjT0TIyMzQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4e1mcOHtZnS',
                    'BAIDUID_BFESS': '8B4C40F37A023F26D4310F9C9A7B2377:FG=1',
                    'ZFY': 'hOYJUrQSyzDx0PujEJTheQUcjAQCAEQsiHcRcoTNXNQ:C',
                    'H_PS_PSSID': '61027_62325_62718_62867_62892_62969_63018_63042_63046_63147_63154_63155_63179_63195_63161_63211',
                    'H_WISE_SIDS': '61027_62325_62718_62867_62892_62969_63018_63042_63046_63147_63154_63155_63179_63195_63161_63211',
                    'MCITY': '-315^%^3A',
                    'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750863707',
                    'HMACCOUNT': 'C32385ED95A3E258',
                    'bdindexid': 'cl0ujfttrrngho4sonute444f2',
                    'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05008761588Gjguq0KjJREQgSau^%^2BAyHS6s0TmjKtHXJTPVxogN2Vk1OQnwd8YYi^%^2FFNVmYFznUn5iYJ9F1LNgzbIppDr01CVd5o9Nb4jEatlhllBHXO1HLSfV47cGgLQsbmkYfCyNvldU1X5f9u3EaMSY^%^2BuSaUieGot4MPabdToQUXe^%^2BcaNniYs5cGeBviWXy9jAuJFFoQECwgDzDRzJlHi7dQFehQUdDllOG6NH0vqGF',
                }
            ],
            # "account_group_11":[ # gz
            #     {
            #         'BAIDUID': '1E4DD50786E976883A6A8FD400D04C68:FG=1',
            #         'BAIDUID_BFESS': '1E4DD50786E976883A6A8FD400D04C68:FG=1',
            #         'PSTM': '1750262257',
            #         'H_PS_PSSID': '60273_62325_62832_63145_63327_63392_63402_63440_63429_63457_63560_63567_63564_63582_63576_63610_63243_63639_63646_63655_63690',
            #         'BIDUPSID': '6F8E7B7D482EF1A6804DA5D8AB694B55',
            #         'ZFY': 'zaprdIQuDEUI8i7xG3eOHHU381Ks:BvhBANzGNJ:B:AsjU:C',
            #         'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750863216',
            #         'HMACCOUNT': '9AC3C7B02E02440B',
            #         'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGljCd5+jGDsnlfrx8M3l+ysGEimjy3MrXEpSuItnI4KD0R4BgE1H69Wr1FiRilpMeemv06A+VOqtMEDgVc1mdlkx/rCLfVT5cuLHoeOW4tzd/kXueet19Rw8In68C4JyaVK3WkYstEGtfI5jznZi4Hoi8AnPDlqwWqJtUZbCMa8eIsjCSrY0dsjahexSoaXoeCUeuxiToCgDf/WQNHMgcrQbamcJqAjhBkTDPJDH4mcUK9+GzXm18RxdTtcRqpQ/kumOxIZj5RQ+RLxHJl103SQjL8desdxkCio68R/Rf8ctKZJRLUyn8eYR3PY+J7q0a3Nx5TEoRvZyTcnLD8C/IOF/a63+PqSXGe4v/GYvsT8CIQSBPL5QNLEmSFDh37CqqQRF+YoRnVR2qmoIQm0/b5lsk8DkoZPyjVREjEk15uTix+MTCoPkvrKwfqhqJJ9YAirmZ2z+qA9DBNQqv8qCuXfk2892Of9sKu9wj25jjzeepEvovMcGFUKcWJi3mo5UR1uXDMvZlfbgHA09mSKeJ3rO21PLHqRbYEf/85IWzCuPyQT6E1WaBEFsnQj/EUosnZDB1kaYXuiqpWIT/jKcLYJNV/QRQpz9OxL2VppXiVh0IG4z5Iej5fHUmTzo7G7KQ35rG4',
            #     }
            # ],
            "account_group_12":[ # 老爸
                {
                    'ab_sr': '1.0.1_OWM5NDJiMjE4NTUwYzUzNGYyODE2MTM5ZTU5NTVlMmRhYzA2MDM2NTM0N2FhOGI3NGZmM2RjNTMyN2I0YWIxZDA2ZTY0OTkyYjAwZGZmMWE4OWYwNDY4ZDZhZWU4ODg1YzY3MTJhMzQwOWEwZTMxMTA4ZTg4YThjNThiNDBhNjViM2VkMjM4NDhiMTIzZDcxMjZhMzE5YTY3Zjk5YzE5Nw==',
                    'RT': '"z=1&dm=baidu.com&si=7a109fcd-459f-4410-acd2-b92a4f792a96&ss=mcbjq8sq&sl=3&tt=6lp&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
                    'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750831355',
                    'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750831264',
                    'bdindexid': '1f1uabtf9pssfn92lnelul15b4',
                    'CPID_212': '69607570',
                    'CPTK_212': '2035619263',
                    '__cas__id__212': '69607570',
                    '__cas__rn__': '500843794',
                    '__cas__st__212': '027ec97e2cb29ed9e494e650b93e5df8460a2d2aac95e625067c34440b5add1d69c98de3ede1bc8d34ca1502',
                    'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05008437944ZB%2BIlTEywCY1Dj7f%2FHmBGNTaStlt2witucaeJ688jtjAGTpXcteLYJ55Waa2LHm5AsmH%2BiIwwqtYRBysdaqFCFpoVkmBXr%2Bpb2ALWzOTZF4AoAZDrrtAquItc8oL9FSEThKQHwCgUly93dQtY17LtggeixRtisXgD83maU07hj5tiRlFij4ar3IzX7aOMSl0XvG8yArBY%2F8IoLL9EKn3UTv7d6Cb9tx4VKOf3Q8%2BEOR2lALchFzimTJSMvh1aTzgdnDvjI6HEPo9TbA9nb4aYrG3dIwP8PR5kdNVx8c83hs%3D87034466152019784773664513767458',
                    'BDUSS': 'FIRTN-TElKTVdvaDJGeG5lLXYtZkNyRG1jb1FYTHdXVklEWjRrWTZLYnZIWU5vSUFBQUFBJCQAAAAAAQAAAAEAAACRAOIhAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO-QW2jvkFtoSE',
                    'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihdwitHd04Lvs3Nfz26Zt2honnQBqGZJ1+FooMMOy9VfBMHd4KSE2lo7q2jM/4leBJXqt+nMkIsYwpNA4XBVB5BGpKv8rf9RxKxeW8+CymWcpQ8qfiUvli8qcS/AH/6nfMYq1ZMQFVRuXQF6FC4JGmtimz2DXekkwSCAmMYTF/dLSzUpJfuFvvgkHA3khHNtJ5dl4mcFJuwYS8+bE/6LLyA5PNk2eTwFYhuZsGjwCR7FVAPhMNMWL+Qlfaczl+PBQBDkVV8ysF/wnr6VWwUzKeq+NBDa593uSfHg6jo4zQ+k5UPBBx7NsZfzlUSbKaHt/szpDZmZbzEXZCOH7A43Q25NsmgYE289mszO99fMXxzLmdnvNXIEW2pwj4BXINSNFrPPV5wQJ1URP2/J3SSQnmckwFMb7+JFWxNGoA0JNiv6hCb0gkXpkEpISi6tVHh+hsQifjACGGz0MbLI9AAutvQNmLovQE8DrrUkOPSWZkiBwIUvxonSGS2lgiNZBxgK/Nad6P3sfvyvYhyXNwxm6SzH+Oja1l6cy9uoP7y446ILa1CLEOaV1jDkGoksNhRtn7B1VPovN1TRU04qLrmECuDGMBVR4vlhy8DqZQ1/LUEQ9mjyqP/SnZsRdyLAjuA3ESTcrCSmS6iWcmxBDT8gjuTbf5rG4+h0gsZ2eMGgzIHtuS4zhpfoAZYfd+R7pkXZXlVZsh4TITMtC54LZjiFwYUTw/8Vr7jyxVr5frOPWZM81V8YClTpPkuiWM0gZm41VCO+vNeIKxJyJ0hcHJ83oQN1+3jtOOi8LxWmDSZzbPJDJU9Bq7zt2A9A8E851l8QtBoQFIuWEGY3DMQGzE4fLtBnD2IBA1xgIrbF95h/aKYBNVXdvBhoLwXhcnXaiqXEpcvFQlonIv85FfaVbfEoKujQX2IBA1xgIrbF95h/aKYBNVh6Y0NjEKZ13xldTgKDiG2QRBJFTPsviSSEvgLGRO3YgGOv+/I3nwGp9q5hLF8/07goRUnieOy9WY3CCu1FKQrXv4Kl2tvhm/51VQHSSoTtFbHhSGlEKo+S0ciyUHoRYU',
                    'HMACCOUNT': '59D7B00BAF8CF5E3',
                    'BA_HECTOR': '8h8505212l2k80252l042400818h0m1k5n44s24',
                    'BDORZ': 'FFFB88E999055A3F8A630C64834BD6D0',
                    'ZFY': 'j1F5mEivMw:BC:AWGx6dVpP0QlsSOQx95ifowSQkPM12s:C',
                    'BAIDUID': '5FD8DE0306F5BD9D402A2CCF80FFF9EC:FG=1',
                    'BDRCVFR[d9MwMhSWl4T]': 'mk3SLVN4HKm',
                    'BIDUPSID': '5FD8DE0306F5BD9DF3901492EBC292E2',
                    'H_PS_PSSID': '61677_62327_62832_63147_63326_63401_63563_63582_63579_63636_63647_63655_63725_63711_63752',
                    'PSINO': '5',
                    'PSTM': '1750831258',    
                }
            ],
            "account_group_13": [# 13645222106
                {
                    'BAIDUID': '1B938E2318FB791FA216F67036EDB19A:FG=1',
                    'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750831164',
                    'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1750861256',
                    'HMACCOUNT': '2C7C49A4B8DC49C5',
                    'RT': '"z=1&dm=baidu.com&si=9239fbab-8bfe-48cd-bd2a-e1044dcec186&ss=mcc1cztt&sl=c&tt=8vr&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
                    'ppfuid': 'FOCoIC3q5fKa8fgJnwzbE0LGziLN3VHbX8wfShDP6RCsfXQp/69CStRUAcn/QmhIlFDxPrAc/s5tJmCocrihd0enHWGiHNa8jc3p2YbsY9BJz/l8wKWpVe71o56icb5WJpuXZiPIDDB1PsImjYrujSNfb+bWJc++UzD3f3/si633O1Nvov0ewgGWYj3KlR//Yvc91cDLyteMW0POvLzphByqmnXQFcEK1EAvma7KU4MDN3WmJY/NWBcNvpqdRBdKrEEfvwQKWpWE08OG0Oa852CXWQYpvBie32q9dmRfwfjHu7PS+78rSATuF9ZmxajHuK36gVAlel31+rZpX2v1w0G3gqifdSzT35NQlL/KGVZl29TNM8Tn9jGWq9feGmPlmfSlGcsA4Zw7tT4tSNMvZNUOzo1AK/5AiuC5hwc5h6SJpPqKnTWDeDxWVlsOQQ+px2RTt0mgeBku85QaxtnC5vJU0ZdfSWHGHKr8tz/+dJsaVg8FFAuKbyjhfXvqcDau5eh8yhGcgjFA3flugImpLGIrvuAAM+9jpzEH4AMjVG1tyMsy+XPlAYbfO1lIoDmPWpXCLkfp9YMJ/g5n97pwE2Brb9MypgKINzcvcBWIkP4HSkq0fQ9uR0sKy0MiHuUCk5CkpWOp1Xr/DIWk9wFD8KCJLToVpiOq1G0BHRvSH1+YLQpEgFjmQoey69Fz+kM7Y5cg925MGCeBU4jWp2g2g3MZ7/q5Nm5qKyRlsnUZctqOY+iIuQVwXDu+NPsd2Gs5cOoZ68Hq8cNrmezkUtisZ7jbCSee7nPW0+PyJuXQBghmXwRbrJcGaELL9QLspNgqMM0aOdAredMfLeYMj+uN0MK5mpzYSmDsgYAGcZbGmnun8qe7C/Z6wAh6Sxpet2o2XdT5gjozQON5/HVPvKJVz/HEk0MlL4OWxuq7efgjrm7u8eNg3xj0WwQipSI+BocHNo9YRuQO2pi4iArzUvik/DxSHbvZCfaziGZggaG+BY2OEydWPa1CZLO/GyxE2lrKfp8o7MtQH8zZ7JAK2DmuATYE6knbkS7/y5uZBK5lY9wL+toPXRBoL0qepeNu3r3x',
                    'ab_sr': '1.0.1_NTljOTFlYzc1ZTZkN2Q2MTkyMTA4MTY0OWU1ZTE2NDA0NWQwMDYyNjg0NjI5MzFmZGVlYjZkNjg1MDExNDBiOGQ1OTgyNjhjZjhhOTc5MTNiYTY4NGI2ODNhZWExY2E0ZmE4MTEwN2Q5ZDUyMmMwYzRjMzFhNGFjMGJkNDI1ZThiOGY2YjQ5YWYwZGE2NWM1YWZiOWJlOGY4ZTA0YzE2NQ==',
                    '__cas__st__212': '7130641a6a5e1dc934b8fde45f8fcb6d382049ddc28c4847dd10b1d576f3a6eae70b55100c21ade3b3925d76',
                    '__cas__id__212': '69590328',
                    '__cas__rn__': '500873696',
                    'CPTK_212': '741465614',
                    'CPID_212': '69590328',
                    'BDUSS': '1GU0VuSFV2SFNoWU1SeXVFN2VuMGVKd0dFMnVTUVQ0ZXlmTn5JMkVESy1rb05vSVFBQUFBJCQAAAAAAQAAAAEAAABBjpqZ0KHT47WwtbAwODEwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL4FXGi-BVxoUU',
                    'SIGNIN_UC': '70a2711cf1d3d9b1a82d2f87d633bd8a05008736966ni%2BNHkWbuhSsg8MWk%2Fy56BC93tYjfIZiO5zB3pg6B%2FSanRw%2F1HmH5bdjzfPqeSt5rcBn54aZiLZ9Ibv6rh%2Fr4V3O%2F%2FHNcATjeEPRcjlggyRbHiDoCXhtVpiOgmqXWG99pZZEd7WTIFoAH4gFKvIHM%2F8bbwMTLrpMe%2FH7z2pxCD%2FCQ7JcaBJh1g%2F7bOWWghfRSc3zYw54mgpKkWW9il1Bg78bZBKNkc150LJEet1kp%2BVKmpkrr1lgUeVDPvZo7U0Of4qR8OHHiNZCIfFmd2gcrOLFj43EAnBtQhYkRTZ%2FWFpOZ5uvChwCkeE98VTm%2BetSBMXJOXsIqfiP70ap5ALzLg%3D%3D21490865168355435844684425407864',
                    'bdindexid': '9ltp5uoreslcceakcvoaqg08k1'
                }
            ],
            "account_group_14": [# 测试1
                {
                    'BAIDUID': '31A2581F9B511E33DA72A58868316861:FG=1',
                    'BA_HECTOR': 'a4218h012k2ka104a504o5810nai131k0j6hu23',
                    'BDORZ': 'AE84CDB3A529C0F8A2B9DCDD1D18B695',
                    'bd_af': '1',
                    'SE_LAUNCH': '5%3A29090996_0%3A29090996',
                    'fuid': 'FOCoIC3q5fKa8fgJnwzbE3sZaS3poGTofPItBD67MTHOloTQtOTfZukshuG%2BjikLm4hHmAx3rWyjKMimKPlDURdOZYjm4lcUocmmPo49Ag480a0mIC63O1c%2FBqEcMZVC5V%2FzNUpLEokpWzcno%2BKUGBuSZbHXdousNlXNZr5jO0AvJtn1O5lWzGMQkFhNOLYdX65B3ntaX4EpPKtgIsF42NLpjQDF22s1z8%2BSNqoNmkmDCTx%2BTKL6w8GdxcRcztzA0KCW4y3gL0%2Bx%2B9R3bd9LHOb679Knr40H9B6zovvywMHBzc2sZvrgJOXi%2FiDQUzufMzUuKkwELga8f2H51MsSNJR67GJOgKAN%2F9ZA0cyBytB6qEGLYOh%2FONfiFdHd%2BRk9HSUGGK9g6JxGFzohdyyVcZlPnmOSyBOCNOSiCV8knMk1slEN%2BViKJ9mQd1J%2FRTLpd1LLXXo2U70WwlfVbkbQ%2FNwWESDc3WjNykHQgmFW5sUV4uzjDKAi%2FqbTr2WGx2bN67l1jJiOBxk4GDIdx5%2FaJAUxvv4kVbE0agDQk2K%2FqEJvSCRemQSkhKLq1UeH6GxCJ%2BMAIYbPQxssj0AC629A2Yui9ATwOutSQ49JZmSIHAhS%2FGidIZLaWCI1kHGAr81p3o%2Fex%2B%2FK9iHJc3DGbpLMf46NrWXpzL26g%2FvLjjogtrUIsQ5pXWMOQaiSw2FG2fsHzUJ6aS6x2ARHpppRXfhHh4ZaJNSUKp1t%2FygYdhyiZtb0PJErm9NuhhgSVQWw3o94fvkJSdbeTSUCYUcSDfs1oaktJ7CISS0STF94GtUDhRi%2FtsJB9aics6wilyMAm769%2FlTRa%2BIffW9qYdS%2F8IMr41ftb3vGuZ5AMhJMrFU3OYFNetS6mrAjm2GHsp1aRoBwrXcL%2FjvKH252h3bbQIEd5KpCpLHE5%2F11gXBWFEw88CJ5Iw4KsvF9ewnNvSZYYkOfGEQw3OLo5dsSUeQDd6vDni1evF%2FM7yvmL%2BFUAwPmWZFbvNq69O2z3wBW%2BogxJUDy9IDhObhno4D7MBZG4B%2BpNlhGWn0jikQ5zzmAASlnix3V2XtmwNAzvtRZUfKm%2Fj5ohXGVaLqOQwr5UIY0Yb6SLXLM1qkKE39xuHQXz2y787L7W199bwgobYc9164V8Y6I40dDn9N%2F3gRsPisyHi6z8aphVNhJG%2F707P2GcCYlcR4%3D',
                    'rsv_i': '7e6a+IoXs7+ObkM62n6bbBVV3Rb7EatVM1P3OZgLBPKJ5BxCecuOU8X29LF5i1UGIzGlr3vjM/L+JInA4EQqijbBV0wmriI',
                    'H_WISE_SIDS': '110085_626068_628198_632156_633619_636706_637553_641765_642950_643583_641767_644372_644659_644675_644640_645095_645170_645434_645928_644402_646540_646557_647614_647626_647658_647709_647689_647900_648256_647483_648404_648454_648451_648466_648464_648470_648479_648476_648450_648501_648475_648498_648505_648502_648506_648472_648457_648444_648652_648591_648722_649006_649054_649075_648937_649047_649058_649019_648587_649038_649156_648093_649235_648964_649326_646543_649354_649344_641262_649533_649589_649649_649716_649818_649809_649868_649855_649777_649909_649231_649926_649959_649935_646203_650035_650059_650055_650062_639680_644053_650205_650213_650211_650221_650084_650257_650267_650272_650288_650285_650330_650326_650327_650323_650420_650010_650470_650522_650302_8000075_8000118_8000134_8000138_8000160_8000166_8000171_8000176_8000180_8000185',
                    'BDUSS': 'JuWFd-Vk43by1COVZvQXNuRUhsQkFkQlVYbWxPRzlJSWxvR2poZjdsSW1LREZvRUFBQUFBJCQAAAAAAQAAAAEAAAB2EzOXQzIxQWI1OTQ5MTM0NgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACabCWgmmwloR2',
                    'SEARCH_MARKET_URL': 'http%3A//wk.baidu.com/ndWapLaunch/browse/view/e257afcaf11dc281e53a580216fc700aba685278%3Ffr%3Dlaunch_ad%26utm_source%3Dbdss-WD%26utm_medium%3Dcpc%26keyword%3D%25E7%2599%25BE%25E5%25BA%25A6%25E6%2596%2587%25E5%25BA%2593%25E4%25BC%259A%25E5%2591%2598%25E5%2593%25AA%25E9%2587%258C%25E5%258F%2596%25E6%25B6%2588%25E8%2587%25AA%25E5%258A%25A8%25E7%25BB%25AD%25E8%25B4%25B9%26utm_account%3DSS-bdtg883%26e_creative%3D108585211755%26e_keywordid%3D950416350347%26query_reqid%3DuHIWm17WmHRsnjKBnj03n-tk%26bd_vid%3D8764586727771552885%26_wkts_%3D1745322131306%26needWelcomeRecommand%3D1',
                    'Hm_lvt_0533c9749e3953bc202dc826fea9bcf8': '1745460077',
                    'Hm_lpvt_0533c9749e3953bc202dc826fea9bcf8': '1745460077',
                    '__bid_n': '1966582ac879888df45213'
                }
            ],
            "account_group_15": [# 测试2
                {
                    'BAIDUID': '0847F44F05CED62B7984A1F61457C322:FG=1',
                    'BA_HECTOR': '802k052l8h2k8lag8124g00l8lqtev1k0j6c922',
                    'BDORZ': 'AE84CDB3A529C0F8A2B9DCDD1D18B695',
                    'bd_af': '1',
                    'SE_LAUNCH': '5%3A29090993_0%3A29090993',
                    'fuid': 'FOCoIC3q5fKa8fgJnwzbE3sZaS3poGTofPItBD67MTHOloTQtOTfZukshuG%2BjikL0BLZATIysMZjIWM25YkzcOzx42AgVwH%2BQiRkYeSdQRX7pD6IAtw%2FB1vAZBFSZg6KPVooT%2F7PbHY2R%2F%2BpdmY%2BloQCXA%2FjWsVU99N5aeUCl4BoVg9vfhdYe%2FeDrTJH07dCJvcEdb68gHdA2UsMYRAo09TqDPKZgfjFmOPY2vLt%2Bg3HFyRaugxWDX%2FKOkX6bggSw5tr3KUJUzjo%2Br5dGtAgbWBgQBPOtnE8BQ7BIltSXGS3lmrP4M1iwuxRGegVZNCeowaXPHngVQMRm6PtZO2pdLl69fslWV7RhqHxc8QZna8S7h9hTwtHueurzSUO31NYkICx44IlIgvBq7Ab5JQWQ9ckH3PfLajwqrF6nlcEKy6A05bkLvd7%2BDniS5jg8ohLtIfEwLYPDMJ%2F1KfrzX109PrDoJ4LyeuAIWWfI6C6KGFFO9ZDRdnbL6n8KLyBHKCEuerHm37EZLal5KwM6tCLmMheeciRI7bZS61mzwLJvT54XIWkktu4TY6WXC6fyKrok1ZcoSdyVwupM9EDeOngYM963nQ6KHi7INdTJoQ%2B430GlkeTLZiPZ8AuCF%2BPgL8Rbni4tAhmgyEPkLb4lD4V%2BiBe%2Bw8usmWA7PWIi4qEuSHCaQeG2ysZGa%2FGX7VWAylrasHjUj1CSrUe7jPtRI3cnwET2bral0E%2FJK6%2FilWpD1KUBSPLSwZYy3pvDmxbzbLCu8DswBB2N%2FRkMW%2FthSpNgujQ08vd%2BHpXRB%2FzhfSUcIaHPhEvjg4XLL%2Br9axZtHmhrOK6OPZXIGGPLkewVepfhPPF%2F%2F07OJKnyfGTZ2nKT6txq%2FVVBT01vdKk6zo6c08eh1M6RLDSrNAOF6HajDa6MPmMLGC9%2F3W1TAj7Jir%2FzxIMkRVl1yvsSYgu4PZBQGX7EOWfx0oHud59wS6fx2Wqhmzi406j6mSnJyTBY%2FhVtaWgL3a9RS1naVWoqIay8kq8uBpQD2w%2BfEsel1%2Fheiao8nPBpgxFG%2BfK82%2Bm1ib8f1MnzYS2uBw%2F%2BeqDXtP%2BEes4VbZvKn%2Bi7GkjiUXx1C06iO5tvXxI56x2WnpCBxHUSkZmxkkJ644Fymto2YVGh4UQwuo%2Fu5GI9LEKglalBZoWi5CJfNSGrHvwtel1Tyjo%2FVw%3D',
                    'logTraceID': '6467aeb1f0e9428cc998ccca36cbeee88205fd251fdf6d6b82',
                    'LASTLOGINTYPE': '0',
                    'BAIDU_WISE_UID': 'wpass_1745459778784_873',
                    'rsv_i': '67f7gB0iuqDMuoKX4gZf91pfRsv4k4yy0F0jiC6kP5W7Si+e2uIk82gbjcGsOnJFeHZZe/LHEPBdbFbVQazEMp9qGElYZpU',
                    'H_WISE_SIDS': '110085_621489_626068_628198_632161_633612_637557_632292_632299_641765_642950_643584_641767_644665_644641_645101_645227_644369_645169_645434_645925_646541_646274_646561_647080_646774_646741_645030_646084_647709_647689_647904_644402_647925_648254_648404_648428_648453_648452_648467_648465_648470_648479_648476_648449_648500_648474_648498_648504_648503_648506_648473_648460_648355_648448_648438_648595_648727_648852_648995_649074_649061_649038_649034_649159_648093_649235_649325_649361_649344_641262_649532_649592_649658_649652_649233_649715_649818_649775_649869_649848_649777_649910_649960_649935_649919_646202_650035_650047_650071_650057_650041_639680_649893_644053_650213_650203_650209_650220_650084_650256_650262_650287_650329_650324_650322_650328_650418_650452_650521_650302',
                    'BDUSS': 'dzZzNGSUhQU2JBb2ZxQXpqWWNSNlRuOH5MWnpWbnVITFFsfmwtN203LXRKekZvRUFBQUFBJCQAAAAAAQAAAAEAAAAhEzOXQzIwQWIxODEyMjAzNwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK2aCWitmgloWD',
                    'STOKEN': '5c3b70fe4bafddc80cb589ffcbd1b8283eceecf949818e6fa6c88c2c5f21bffd',
                    'PTOKEN': '7c2a60f32225e9be6d5b42fd9e253795',
                    'UBI': 'fi_PncwhpxZ%7ETaJc9Kk3IgEPU3f3FHRWh4Y',
                    'SEARCH_MARKET_URL': 'http%3A//wk.baidu.com/ndWapLaunch/browse/view/e257afcaf11dc281e53a580216fc700aba685278%3Ffr%3Dlaunch_ad%26utm_source%3Dbdss-WD%26utm_medium%3Dcpc%26keyword%3D%25E7%2599%25BE%25E5%25BA%25A6%25E6%2596%2587%25E5%25BA%2593%25E4%25BC%259A%25E5%2591%2598%25E5%2593%25AA%25E9%2587%258C%25E5%258F%2596%25E6%25B6%2588%25E8%2587%25AA%25E5%258A%25A8%25E7%25BB%25AD%25E8%25B4%25B9%26utm_account%3DSS-bdtg883%26e_creative%3D108585211755%26e_keywordid%3D950416350347%26query_reqid%3DuHIWm17WmHRsnjKBnj03n-tk%26bd_vid%3D8764586727771552885%26_wkts_%3D1745322131306%26needWelcomeRecommand%3D1',
                    '__bid_n': '196657fe3c192962d04961'
                }
            ]
        }
        
        # 初始化账号管理器
        account_manager = AccountManager(account_groups)
        
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
            word_list = pd.read_excel('数字设备和服务关键词.xlsx')
            keywords = word_list['关键词'].tolist()
            logger.info(f"成功读取到 {len(keywords)} 个关键词")
        except Exception as e:
            logger.error(f"读取关键词文件失败: {str(e)}")
            logger.info("使用默认关键词'数字政务APP'继续")
            keywords = ["数字政务APP"]
        
        years = list(range(2016, 2026))  # 2016年到2025年
        
        # 构建所有任务
        all_tasks = []
        for word in keywords:
            for year in years:
                for city_number, city_name in city.items():
                    all_tasks.append((word, city_number, city_name, year))
        
        # 分配任务给不同账号组
        group_tasks = account_manager.distribute_tasks(all_tasks)
        
        # 创建共享的进度管理器和批次管理器
        progress_manager = ProgressManager(CONFIG['progress_file'])
        batch_manager = BatchManager(CONFIG['output_dir'], CONFIG['batch_size'])
        
        # 创建代理管理器
        proxy_manager = ProxyManager([], CONFIG['use_local_ip'])
        
        # 统计任务数量
        logger.info(f"总任务数: {len(all_tasks)}")
        completed_tasks = sum(1 for word, city_number, city_name, year in all_tasks 
                            if progress_manager.is_completed(word, city_number, year))
        logger.info(f"已完成任务数: {completed_tasks}")
        logger.info(f"剩余任务数: {len(all_tasks) - completed_tasks}")
        
        # 为每个账号组创建处理线程
        threads = []
        results = {}
        
        # 创建并启动进度汇总线程
        progress_summary = ProgressSummary(interval=30)  # 每30秒汇总一次进度
        progress_summary.start(results, len(all_tasks), completed_tasks)
        
        # 创建并启动线程
        for group_name, tasks in group_tasks.items():
            # 创建该组的Cookie管理器
            cookie_manager = CookieManager(account_groups[group_name])
            
            # 注册Cookie管理器到进度汇总对象
            progress_summary.register_cookie_manager(group_name, cookie_manager)
            
            # 创建并启动线程
            thread = start_task_thread(group_name, tasks, progress_manager, batch_manager, proxy_manager, cookie_manager, results, account_manager)
            threads.append(thread)
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
            
        # 检查是否有重分配的任务线程需要等待
        logger.info("检查是否有重分配的任务线程需要等待...")
        redistributed_threads = account_manager.get_redistributed_threads()
        if redistributed_threads:
            logger.info(f"发现 {len(redistributed_threads)} 个重分配的任务线程，等待它们完成")
            for thread in redistributed_threads:
                thread.join()
        else:
            logger.info("没有发现重分配的任务线程")
        
        # 停止进度汇总
        if progress_summary:
            progress_summary.stop()
        
        # 汇总结果
        total_success = sum(results.get(group, {}).get('success', 0) for group in results)
        total_failure = sum(results.get(group, {}).get('failure', 0) for group in results)
        
        # 最终统计
        logger.info(f"爬取完成！成功: {total_success}, 失败: {total_failure}")
        logger.info(f"进度文件: {CONFIG['progress_file']}")
        logger.info(f"批次数据目录: {CONFIG['output_dir']}")
        logger.info(f"最终输出文件: {CONFIG['final_output']}")
        
    except KeyboardInterrupt:
        logger.info("用户中断了程序，正在保存当前进度...")
        # 确保在中断时也保存当前批次的数据
        if progress_summary:
            progress_summary.stop()
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        if progress_summary:
            progress_summary.stop()
    finally:
        # 无论程序如何结束，都确保保存最后一个批次和合并所有批次文件
        if batch_manager:
            logger.info("保存最后一个批次数据...")
            batch_manager.save_final_batch()
            
            logger.info("开始合并所有批次文件...")
            if batch_manager.merge_all_batches(CONFIG['final_output']):
                logger.info(f"数据合并完成！最终文件: {CONFIG['final_output']}")
            else:
                logger.error("数据合并失败！")
                
        logger.info("程序结束")

if __name__ == "__main__":
    main()