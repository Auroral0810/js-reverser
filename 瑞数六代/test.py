import requests

cookies = {
    'enable_NfBCSins2Oyw': 'true',
    'acw_tc': '276aedec17448773981945258e3fba68e42d5e3c7afdfa8a9cf742b928de27',
    'NfBCSins2OywS': '60EuyjpfmwHLgXkvnYAnAM3Kna1WqN22qA2sXLu18XICxlSEug1A_ORIlO.lSTfJFEptpOhJXeEtx4ezpIp1.AmA',
    'token': '',
    'STEP_TIPS_INDEX': 'true',
    'STEP_TIPS_RESULT': 'true',
    'NfBCSins2OywT': '0tjxuSciMqOpiFBFikRHlaWzStCZYpgWoCKkaumoUbHYgt5aZUHaV97RCHbanr3LM67SUZpGhfK1GJxLQQfgq9X8H.Tmf3MIFy3UmDy._dHEIfkA9T2BXVzhRN5edrFasNAnuu6wv9ic1AXoc0PVEaeFroDTHYcFrIR2s8k1T8Lj.5LU8zPaQbaxlqPvSC8dM6RR054BKJwYyetBoanU.6CHRWKjuwgB2iZdKBh5RCqiZer2JWdrKbVp0U69ah5feOeprEPGInxxYejS0K.99Sjo8zUiUfCojopvI7qhx_0vlGCQDBIRCsMk3tdsdNVaWaIGyvB62PMWQW3vo4tzTlbnM5VnTlrYPvkNMaMxGqBR8r9H6reVXgme6pgJPrOw.',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://www.nmpa.gov.cn/datasearch/search-result.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sign': 'ddee2d5f11431b5796cec00baff23ac9',
    'timestamp': '1744877463000',
    'token': 'false',
    # 'Cookie': 'enable_NfBCSins2Oyw=true; acw_tc=276aedec17448773981945258e3fba68e42d5e3c7afdfa8a9cf742b928de27; NfBCSins2OywS=60EuyjpfmwHLgXkvnYAnAM3Kna1WqN22qA2sXLu18XICxlSEug1A_ORIlO.lSTfJFEptpOhJXeEtx4ezpIp1.AmA; token=; STEP_TIPS_INDEX=true; STEP_TIPS_RESULT=true; NfBCSins2OywT=0tjxuSciMqOpiFBFikRHlaWzStCZYpgWoCKkaumoUbHYgt5aZUHaV97RCHbanr3LM67SUZpGhfK1GJxLQQfgq9X8H.Tmf3MIFy3UmDy._dHEIfkA9T2BXVzhRN5edrFasNAnuu6wv9ic1AXoc0PVEaeFroDTHYcFrIR2s8k1T8Lj.5LU8zPaQbaxlqPvSC8dM6RR054BKJwYyetBoanU.6CHRWKjuwgB2iZdKBh5RCqiZer2JWdrKbVp0U69ah5feOeprEPGInxxYejS0K.99Sjo8zUiUfCojopvI7qhx_0vlGCQDBIRCsMk3tdsdNVaWaIGyvB62PMWQW3vo4tzTlbnM5VnTlrYPvkNMaMxGqBR8r9H6reVXgme6pgJPrOw.',
}

params = {
    '7QBHXKaZ': '0V7vpvGlqErI1uiznA.cD.vU.V0vURdGgshCMOpg8mDZyWssDXMlzGhr7FngMbKT0Xl1Oy8qaIfuB3iMiHtmy3Baa1nzFW_iy.unILBripgngbrv_x9nNtpLpc1VDOeVttedqLqQRfTZkgekfNyF3slO83JG.q4OfNZMXDZ4O1ggOLjMsm9I5xg7hD5j0MPcOTxwrBp9P90M1SNlsELqBErWiWpRBdbzDrgC7bmlyzrk5AYR9QcjoutcKsSakWBFQL73530wqr5YVP6mqwDhN8WTeDImmCrDuia',
}

response = requests.get(
    'https://www.nmpa.gov.cn/datasearch/data/nmpadata/search',
    params=params,
    cookies=cookies,
    headers=headers,
)
print(response.text)