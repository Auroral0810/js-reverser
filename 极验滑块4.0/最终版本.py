import logging
import time
import random
import execjs
import requests
import uuid
import json
import re
import cv2
import numpy as np
import onnxruntime
from io import BytesIO
import colorama
from colorama import Fore, Style

# 初始化colorama
colorama.init(autoreset=True)


# 自定义彩色日志处理器
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.BLUE,
        'SUCCESS': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"
            record.msg = f"{self.COLORS[levelname]}{record.msg}{Style.RESET_ALL}"
        return super().format(record)


# 配置日志
# 添加一个SUCCESS日志级别
SUCCESS_LEVEL = 25  # 在INFO和WARNING之间
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

# 创建logger实例
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 创建控制台处理器并设置格式
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# 正确使用自定义日志级别的方法
def log_success(message):
    logger.log(SUCCESS_LEVEL, message)


class SlideDetector:
    def __init__(self, model_path="yolo.onnx"):
        self.onnx_session = onnxruntime.InferenceSession(model_path)
        self.model_inputs = self.onnx_session.get_inputs()

    def detect(self, img_content):
        confidence_thres = 0.8
        iou_thres = 0.8
        bg_img = cv2.imdecode(np.frombuffer(img_content, np.uint8), cv2.IMREAD_ANYCOLOR)
        img_height, img_width = bg_img.shape[:2]
        bg_img = cv2.resize(bg_img, (320, 320))
        image_data = np.array(bg_img) / 255.0
        image_data = np.transpose(image_data, (2, 0, 1))
        image_data = np.expand_dims(image_data, axis=0).astype(np.float32)
        output = self.onnx_session.run(None, {self.model_inputs[0].name: image_data})
        outputs = np.transpose(np.squeeze(output[0]))
        rows = outputs.shape[0]
        boxes, scores = [], []
        x_factor = img_width / 320
        y_factor = img_height / 320
        for i in range(rows):
            classes_scores = outputs[i][4:]
            max_score = np.amax(classes_scores)
            if max_score >= confidence_thres:
                x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]
                left = int((x - w / 2) * x_factor)
                top = int((y - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                boxes.append([left, top, width, height])
                scores.append(max_score)
        indices = cv2.dnn.NMSBoxes(boxes, scores, confidence_thres, iou_thres)
        new_boxes = [boxes[i] for i in indices]
        if len(new_boxes) != 1:
            new_scores = [scores[i] for i in indices]
            max_score_index = np.argmax(new_scores)
            new_boxes = [new_boxes[max_score_index]]
        return new_boxes[0]

    def get_slide_distance(self, content):
        """计算滑块应该移动的距离"""
        left_pos = int(self.detect(content)[0] * 0.9862 - 11.317)
        return left_pos


class GeetestCracker:
    def __init__(self, captcha_id="54088bb07d2df3c46b79f80300b0abbe"):
        self.captcha_id = captcha_id
        self.cookies = {
            'captcha_v4_user': '2007ca91c1754966b5dd806c26ab3d2c',
        }
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Referer': 'https://gt4.geetest.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        self.detector = SlideDetector()

        # 加载JS脚本
        with open('demo.js', 'r', encoding='utf-8') as f:
            self.js_ctx = execjs.compile(f.read())

    def get_callback(self):
        """生成回调函数名"""
        return f'geetest_{int(time.time() * 1000)}'

    def load_captcha(self):
        """加载验证码"""
        callback = self.get_callback()
        uuid_str = str(uuid.uuid4())

        params = {
            'callback': callback,
            'captcha_id': self.captcha_id,
            'challenge': uuid_str,
            'client_type': 'web',
            'risk_type': 'slide',
            'lang': 'zh',
        }

        response = requests.get('https://gcaptcha4.geetest.com/load', params=params, cookies=self.cookies,
                                headers=self.headers)

        # 解析返回结果
        pattern = r'geetest_\d+\((.*)\)'
        match = re.search(pattern, response.text)

        if not match:
            logger.error("无法解析验证码加载结果")
            return None

        json_str = match.group(1)
        result_data = json.loads(json_str)

        return {
            'process_token': result_data['data']['process_token'],
            'payload': result_data['data']['payload'],
            'bg': f"https://static.geetest.com/{result_data['data']['bg']}",
            'slice': f"https://static.geetest.com/{result_data['data']['slice']}",
            'lot_number': result_data['data']['lot_number']
        }

    def verify_captcha(self, captcha_data, slide_distance):
        """验证滑块"""
        callback = self.get_callback()

        # 生成w参数
        w = self.js_ctx.call(
            'getW',
            slide_distance,
            captcha_data['lot_number'],
            self.captcha_id
        )

        params = {
            'callback': callback,
            'captcha_id': self.captcha_id,
            'client_type': 'web',
            'lot_number': captcha_data['lot_number'],
            'risk_type': 'slide',
            'payload': captcha_data['payload'],
            'process_token': captcha_data['process_token'],
            'payload_protocol': '1',
            'pt': '1',
            'w': w
        }

        response = requests.get('https://gcaptcha4.geetest.com/verify', params=params, cookies=self.cookies,
                                headers=self.headers)

        # 解析返回结果
        pattern = r'geetest_\d+\((.*)\)'
        match = re.search(pattern, response.text)

        if not match:
            logger.error("无法解析验证结果")
            return False

        json_str = match.group(1)
        result_data = json.loads(json_str)

        if "data" in result_data and result_data["data"].get("result") == "success":
            log_success("验证通过")
            return True
        else:
            logger.info(f"验证失败: {result_data.get('data', {}).get('result', '未知原因')}")
            return False

    def crack_once(self):
        """完成一次验证过程"""
        # 加载验证码
        captcha_data = self.load_captcha()
        if not captcha_data:
            return False

        # 下载背景图
        bg_response = requests.get(captcha_data['bg'])
        bg_content = bg_response.content

        # 使用YOLO模型检测缺口位置
        slide_distance = self.detector.get_slide_distance(bg_content)
        logger.info(f"检测到滑动距离: {slide_distance}像素")

        # 验证
        return self.verify_captcha(captcha_data, slide_distance)

    def batch_test(self, count=20):
        """批量测试验证码"""
        success_count = 0

        logger.info(f"开始批量测试 {count} 次验证...")

        for i in range(count):
            logger.info(f"第 {i + 1} 次验证:")
            result = self.crack_once()
            if result:
                success_count += 1

            # 间隔一段时间
            if i < count - 1:
                time.sleep(2)

        success_rate = success_count / count * 100
        logger.info(f"总计执行{count}次，成功{success_count}次，成功率: {success_rate:.2f}%")
        return success_rate


if __name__ == "__main__":
    try:
        cracker = GeetestCracker()
        cracker.batch_test(20)
    except Exception as e:
        logger.error(f"发生错误: {e}")