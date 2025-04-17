import requests
import ddddocr

def slide_match(front_url, bg_url):
    slice_bytes = requests.get(front_url).content
    with open("front.png", mode='wb') as f:
        f.write(slice_bytes)
    bg_bytes = requests.get(bg_url).content
    with open("bg.png", mode='wb') as f:
        f.write(bg_bytes)

    slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    res = slide.slide_match(slice_bytes, bg_bytes, simple_target=True)
    x1, y1, x2, y2 = res['target']
    # print(x1, y1, x2, y2)  # 114 45 194 125
    return int(x1 / 1.5)



x_distance = slide_match('https://necaptcha.nosdn.127.net/a09ec05100454f229f4038063fa60e99@2x.png', 'https://necaptcha.nosdn.127.net/a1569000a85a440dbae108b3623a655c@2x.jpg')
print(x_distance)