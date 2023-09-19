import uuid
import random
import io
import base64
from PIL import Image, ImageDraw, ImageFont

from common import RedisKeys
from db import redis



class SysCaptchaService():

    def generate_code(self, length):
        # 随机选择字符
        characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # 生成指定长度的验证码
        code = ''.join(random.choice(characters) for i in range(length))
        return code

    def generate_image(self, code, width, height, font_size):
        # 创建一个新的图片对象
        img = Image.new(mode='RGB', size=(
            width, height), color=(255, 255, 255))
        # 创建一个画笔对象
        draw = ImageDraw.Draw(img)
        # 设置字体
        font = ImageFont.truetype('arial.ttf', font_size)
        # 获取字符的宽度和高度
        # text_width, text_height = draw.textsize(code, font)
        # 获取字符的宽度和高度
        bbox = draw.textbbox((0, 0, width, height), code, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        # 将字符绘制在图片中央
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        draw.text((x, y), code, font=font, fill=(0, 0, 0))
        # 添加干扰线
        for i in range(5):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=2)
        # 添加干扰点
        for i in range(50):
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.point((x, y), fill=(0, 0, 0))

        img_data = io.BytesIO()
        img.save(img_data, format='PNG')
        image_data_bytes = img_data.getvalue()
        base64_img = base64.b64encode(image_data_bytes).decode('utf-8')
        return 'data:image/png;base64,' + base64_img

    def generate(self):
        key = str(uuid.uuid4())
        code = self.generate_code(5)
        base64_img = self.generate_image(code, 150, 40, 30)
        # 将key和code缓存到缓存服务器
        redis.set(RedisKeys.getCaptchaKey(key), code, 300)
        return {
            "key": key,
            "image": base64_img
        }

    def is_captcha_enabled(self):
        return True if str(redis.hget(RedisKeys.getParamKey(), 'LOGIN_CAPTCHA')) == "true" else False

    def validate(self, key, code):
        # 如果关闭了验证码，则直接效验通过
        if not self.is_captcha_enabled():
            return True
        if not (key and code):
            return False
        captcha = redis.get(RedisKeys.getCaptchaKey(key))
        if captcha:
            redis.delete(RedisKeys.getCaptchaKey(key))
        return str(captcha).lower() == str(code).lower()
