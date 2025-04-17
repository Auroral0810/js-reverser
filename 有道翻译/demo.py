import time
from hashlib import md5
import json
import execjs
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# 初始化rich控制台
console = Console()

cookies = {
    'OUTFOX_SEARCH_USER_ID': '2050097210@112.2.255.96',
    'OUTFOX_SEARCH_USER_ID_NCOO': '321865632.90403944',
    'DICT_DOCTRANS_SESSION_ID': 'YmE5MTAzZTUtYmUwOC00YWYwLWExNjQtYzhkYzhlYTY0YWJm',
    '_uetsid': 'b9e330a0186811f0babf29c79671995d',
    '_uetvid': 'b9e32f80186811f080ab59a404edf487',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://fanyi.youdao.com',
    'Pragma': 'no-cache',
    'Referer': 'https://fanyi.youdao.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    # 'Cookie': 'OUTFOX_SEARCH_USER_ID=2050097210@112.2.255.96; OUTFOX_SEARCH_USER_ID_NCOO=321865632.90403944; DICT_DOCTRANS_SESSION_ID=YmE5MTAzZTUtYmUwOC00YWYwLWExNjQtYzhkYzhlYTY0YWJm; _uetsid=b9e330a0186811f0babf29c79671995d; _uetvid=b9e32f80186811f080ab59a404edf487',
}
aesKey = "ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl";
aesIv = "ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4";

def translate(content):
    """翻译指定内容并以美观格式展示"""
    d = "fanyideskweb"
    u = "webfanyi"
    t = 'Vy4EQ1uwPkUoqvcP1nIu6WiAjxFeA3Y3'
    mysticTime = int(time.time() * 1000)
    sign = md5((f'client={d}&mysticTime={mysticTime}&product={u}&key={t}').encode('utf-8')).hexdigest()
    
    data = {
        'i': content,
        'from': 'auto',
        'to': '',
        'useTerm': 'false',
        'domain': '0',
        'dictResult': 'true',
        'keyid': 'webfanyi',
        'sign': sign,
        'client': 'fanyideskweb',
        'product': 'webfanyi',
        'appVersion': '1.0.0',
        'vendor': 'web',
        'pointParam': 'client,mysticTime,product',
        'mysticTime': str(mysticTime),
        'keyfrom': 'fanyi.web',
        'mid': '1',
        'screen': '1',
        'model': '1',
        'network': 'wifi',
        'abtest': '0',
        'yduuid': 'abcdefg',
    }

    with open('demo.js', 'r', encoding='utf-8') as f:
        js = f.read()
        ctx = execjs.compile(js)
    
    response = requests.post('https://dict.youdao.com/webtranslate', cookies=cookies, headers=headers, data=data).text
    res = json.loads(ctx.call('O', response, aesKey, aesIv))

    # 提取有用信息
    word = res['dictResult']['ce']['word']['return-phrase']
    pronunciation = res['dictResult']['ce']['word']['phone'] if 'phone' in res['dictResult']['ce']['word'] else "无发音"
    translations = [tr['#text'] + ': ' + tr['#tran'] for tr in res['dictResult']['ce']['word']['trs']]
    target_translation = res['translateResult'][0][0]['tgt']
    
    # 创建基本翻译表格
    console.print("\n" + "="*50, style="bold blue")
    console.print("有道翻译结果", style="bold cyan")
    console.print("="*50 + "\n", style="bold blue")
    
    # 基本信息表格
    basic_table = Table(show_header=True, header_style="bold magenta", title="基本翻译信息")
    basic_table.add_column("原词", style="dim", width=20)
    basic_table.add_column("发音", style="dim", width=20)
    basic_table.add_column("翻译", style="green", width=30)
    basic_table.add_row(word, pronunciation, target_translation)
    console.print(basic_table)
    
    # 详细释义
    console.print("\n详细释义：", style="bold yellow")
    detail_panel = Panel("\n".join([f"- {tr}" for tr in translations]), 
                         title="详细解释",
                         border_style="yellow",
                         expand=False)
    console.print(detail_panel)
    console.print("\n" + "="*50, style="bold blue")

if __name__ == "__main__":
    while True:
        console.print("请输入要翻译的内容 (输入'q'退出):", style="bold green")
        content = input("> ")
        if content.lower() == 'q':
            break
        translate(content)
