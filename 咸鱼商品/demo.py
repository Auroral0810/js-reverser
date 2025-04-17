import requests

cookies = {
    'mtop_partitioned_detect': '1',
    '_m_h5_tk': '88f2b098ff083926e37dc0c27ffb004f_1744290359610',
    '_m_h5_tk_enc': '825a30a94621c1fe58c86aeeca277bd6',
    'cookie2': '14074476be78d62c2b645fe5d837f590',
    'xlly_s': '1',
    '_samesite_flag_': 'true',
    't': 'a29855ba281a4316c5c585273b8ba6ac',
    '_tb_token_': '56739836fea3e',
    'sgcookie': 'E100wITMz%2B7s6T%2By4xIwVwn7zeAMPVTJv%2Fa9RWOnx%2FhtnRMp8Ew5%2FJoO3wp226%2Bqt0eIO1H74hWFg5NJ5M4CHxNHEZ3sL3f6k6PW4vp5HfkT1ZM%3D',
    'tracknick': 'tb535945311',
    'csg': '33e8962a',
    'unb': '2201292691262',
    'tfstk': 'grEIC-xk87Eav2dgK6BZhMZf2YmWA7s2FLM8n8KeeDnpwQex_WlEYTjSwWcaYXyEvbK7a8rUauwkVYe8Z9cPKNy3K0mRgsr50J230dQwxt-KWfeiEvBZJhb5xNmRgsSw7d3hT0Fe_Eh55RhiFYKJ27K9Bxhtp3h8wf3tHxRK20FRCVHmUHH-20L9WYGtw0n8wRBsEflR9Y_STJ6HS8kxA1vbCftJ2lMOZY2BI3k_AvgIMJEB23Bxd2GYpfC0yBcZPWgQbMOmdPebTvNlmHmKPyUxvu1fAce07WH_wsTS6rZ3VqrCGEcLxbVjvP19A0nLArumVZ9nQkwTm4ZhOhhQsRUqxoCMVSea3k0gVsOtZykmXva1eFhKygSX0jiFZU9so3MsgO66rUx7QmokQsNiP2HiduX1CBdnJADsgO66rU0KIvZlCOOpt',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.goofish.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.goofish.com/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'mtop_partitioned_detect=1; _m_h5_tk=88f2b098ff083926e37dc0c27ffb004f_1744290359610; _m_h5_tk_enc=825a30a94621c1fe58c86aeeca277bd6; cookie2=14074476be78d62c2b645fe5d837f590; xlly_s=1; _samesite_flag_=true; t=a29855ba281a4316c5c585273b8ba6ac; _tb_token_=56739836fea3e; sgcookie=E100wITMz%2B7s6T%2By4xIwVwn7zeAMPVTJv%2Fa9RWOnx%2FhtnRMp8Ew5%2FJoO3wp226%2Bqt0eIO1H74hWFg5NJ5M4CHxNHEZ3sL3f6k6PW4vp5HfkT1ZM%3D; tracknick=tb535945311; csg=33e8962a; unb=2201292691262; tfstk=grEIC-xk87Eav2dgK6BZhMZf2YmWA7s2FLM8n8KeeDnpwQex_WlEYTjSwWcaYXyEvbK7a8rUauwkVYe8Z9cPKNy3K0mRgsr50J230dQwxt-KWfeiEvBZJhb5xNmRgsSw7d3hT0Fe_Eh55RhiFYKJ27K9Bxhtp3h8wf3tHxRK20FRCVHmUHH-20L9WYGtw0n8wRBsEflR9Y_STJ6HS8kxA1vbCftJ2lMOZY2BI3k_AvgIMJEB23Bxd2GYpfC0yBcZPWgQbMOmdPebTvNlmHmKPyUxvu1fAce07WH_wsTS6rZ3VqrCGEcLxbVjvP19A0nLArumVZ9nQkwTm4ZhOhhQsRUqxoCMVSea3k0gVsOtZykmXva1eFhKygSX0jiFZU9so3MsgO66rUx7QmokQsNiP2HiduX1CBdnJADsgO66rU0KIvZlCOOpt',
}

params = {
    'jsv': '2.7.2',
    'appKey': '34839810',
    't': '1744288277664',
    'sign': '69c7dcac5f2d5229b40cd6da1ab01318',
    'v': '1.0',
    'type': 'originaljson',
    'accountSite': 'xianyu',
    'dataType': 'json',
    'timeout': '20000',
    'api': 'mtop.taobao.idlemtopsearch.pc.search',
    'sessionOption': 'AutoLoginOnly',
    'spm_cnt': 'a21ybx.search.0.0',
    'spm_pre': 'a21ybx.search.searchInput.0',
}

data = {
    'data': '{"pageNumber":1,"keyword":"平板","fromFilter":false,"rowsPerPage":30,"sortValue":"","sortField":"","customDistance":"","gps":"","propValueStr":{},"customGps":"","searchReqFromPage":"pcSearch","extraFilterValue":"{}","userPositionJson":"{}"}',
}

response = requests.post(
    'https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.pc.search/1.0/',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
).json()

print(response)