import base64
import requests
from fontTools.ttLib import TTFont


headers = {
        'Referer': 'http://match.yuanrenxue.com/match/6',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    }
number_woff = {
    '1010010010': 0, '1001101111': 1, '1001101010': 2, '1010110010': 3, '1111111111': 4,
    '1110101001': 5, '1010101010': 6, '1111111': 7, '1010101011': 8, '1001010100': 9
}


def get_page(url):
    return requests.get(url=url, headers=headers).json()


def decode_base64(content):
    return base64.b64decode(content)


def write_woff(data, name):
    with open(f'{name}.woff', 'wb') as file:
        file.write(data)


def parse_woff(name):
     """获取uni...对应的数字"""
     font = TTFont(f'{name}.woff')
     font.saveXML(f'{name}.xml')
     uni_list = font.getGlyphOrder()
     uni_list.remove('.notdef')
     real_number_dict = {}
     for uni in uni_list:
        temp = ''
        for i in font['glyf'][uni].flags[:10]:
            temp += str(i)
        real_number = number_woff[temp]
        real_number_dict[uni] = real_number
     return real_number_dict


def get_original_data(url, woff_file_name):
     """获取混淆后的数字"""
     confuse_numbers = []
     content = get_page(url=url)
     write_woff(data=decode_base64(content=content['woff']), name=woff_file_name)
     for _ in content['data']:
        confuse_numbers.append(_['value'].replace('&#x', '').replace(' ', ''))
     return confuse_numbers


def get_real_value(value_data, original_value):
    real_value_list = []
    for i in original_value:
        number = ''
        for index in range(len(i) // 4):
            index = index * 4
            number += str(value_data['uni' + i[index: index + 4]])
        real_value_list.append(int(number))
    return real_value_list

max = 0
if __name__ == '__main__':
    for page in range(1, 6):
        woff_file_name = 'woff_data'
        url = f'http://match.yuanrenxue.com/api/match/7?page={page}'
        original_value = get_original_data(url=url, woff_file_name=woff_file_name)
        real_data = parse_woff(woff_file_name)
        real_value = get_real_value(value_data=real_data, original_value=original_value)
        for i in real_value:
            if i > max:
                max = i
    print(max)