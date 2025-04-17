import asyncio
import aiohttp
import aiofiles
import requests


# 可以根据实际网络和系统情况调整此值
MAX_CONCURRENCY = 10

# 全局请求头，避免重复传递
HEADERS = {
    'User-Agent': (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
}


def down_m3u8(url: str, file_path: str = "video.m3u8") -> None:
    """
    同步下载 m3u8 文件并保存到本地。

    :param url:      m3u8 文件的下载链接
    :param file_path:保存后的 m3u8 文件名
    """
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()  # 若下载失败则会抛出异常
    with open(file_path, 'wb') as f:
        f.write(resp.content)
    print(f"[INFO] m3u8 文件已保存: {file_path}")


async def fetch_ts(session: aiohttp.ClientSession, sem: asyncio.Semaphore, url: str, folder: str = "video") -> None:
    """
    使用给定的 session 并发下载单个 ts 文件并保存到本地。

    :param session: 已创建好的 aiohttp.ClientSession
    :param sem:     asyncio.Semaphore，用于限制并发
    :param url:     ts 文件的下载链接
    :param folder:  ts 文件保存的目标文件夹
    """
    async with sem:  # 控制并发数量
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                # 这里以最后 15 个字符作为文件名区分，可根据实际需求调整
                name_part = url[-15:-1]
                file_name = f"{folder}/{name_part}.ts"
                async with aiofiles.open(file_name, 'wb') as f:
                    await f.write(await response.content.read())
                print(f"[INFO] 下载成功: {file_name}")
        except Exception as e:
            print(f"[ERROR] 下载失败: {url}, 错误信息: {e}")


async def download_ts_files(m3u8_file: str = "video.m3u8", folder: str = "video") -> None:
    """
    异步读取 m3u8 文件中的 ts 链接并发下载。

    :param m3u8_file: m3u8 文件路径
    :param folder:    保存 ts 文件的文件夹
    """
    # 创建文件夹（若不存在）
    import os
    os.makedirs(folder, exist_ok=True)

    # 读取 m3u8 文件中的所有链接
    with open(m3u8_file, 'r') as f:
        ts_urls = [
            line.strip() for line in f
            if line and not line.startswith("#")
        ]

    # 创建异步 ClientSession
    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        tasks = [
            fetch_ts(session, sem, url, folder=folder)
            for url in ts_urls
        ]
        # 并发执行所有下载任务
        await asyncio.gather(*tasks)


async def main(m3u8_url: str) -> None:
    """
    主函数，用于调用下载 m3u8 文件并分发异步任务。

    :param m3u8_url: 在线 m3u8 文件的链接
    """
    down_m3u8(m3u8_url, file_path="video.m3u8")  # 同步下载 m3u8
    await download_ts_files("video.m3u8", folder="video")


if __name__ == '__main__':
    # 在这里替换成你要下载的 m3u8 文件地址
    m3u8_url = "https://m3u8.hmrvideo.com/play/44463559b9b54909acb2a260e624739d.m3u8"

    # 开始运行
    asyncio.run(main(m3u8_url))
