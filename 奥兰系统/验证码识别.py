import ddddocr
import os
import time
from PIL import Image, ImageEnhance


def enhance_image(image_path):
    """预处理图片以提高识别率"""
    img = Image.open(image_path)
    # 增加对比度
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    # 增加锐度
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.0)
    # 保存增强后的图片
    enhanced_path = f"enhanced_{os.path.basename(image_path)}"
    img.save(enhanced_path)
    return enhanced_path


def recognize_with_ddddocr(image_path, enhance=True):
    """使用ddddocr识别验证码"""
    if enhance:
        image_path = enhance_image(image_path)

    # 创建识别器
    ocr = ddddocr.DdddOcr(show_ad=False)

    # 读取图片内容
    with open(image_path, 'rb') as f:
        img_bytes = f.read()

    # 识别验证码
    result = ocr.classification(img_bytes)

    # 清理临时文件
    if enhance and os.path.exists(image_path) and image_path.startswith("enhanced_"):
        os.remove(image_path)

    # 对结果进行处理，确保只返回数字
    result = ''.join(filter(str.isdigit, result))

    return result


# 示例使用
if __name__ == "__main__":
    captcha_path = "captcha.jpg"
    result = recognize_with_ddddocr(captcha_path)
    print(f"识别结果: {result}")