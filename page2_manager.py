from PIL import Image, ImageDraw, ImageFont
from kivy.core.image import Image as CoreImage
from io import BytesIO
from datetime import datetime
import os
import sys
from logger import logger


class Page2Manager:
    """第二页管理器：处理住房贷款图片的文字覆盖"""

    def __init__(self, second_icons_dir):
        self.second_icons_dir = second_icons_dir

        self.housing_principal = "512,922.29"
        self.next_repayment_amount = "2,453.80"
        self.next_repayment_date = self.calculate_next_repayment_date()

    def calculate_next_repayment_date(self):
        """计算下期还款日：如果今天>=27号，显示下月27号；否则显示本月27号"""
        today = datetime.now()
        current_day = today.day

        if current_day >= 27:
            next_month = today.month + 1
            next_year = today.year
            if next_month > 12:
                next_month = 1
                next_year += 1
        else:
            next_month = today.month
            next_year = today.year

        return f"{next_year}-{next_month:02d}-27"

    def create_text_image_for_page2(self, base_filename, text_positions):
        """
        在第二页图片上绘制文字（专用方法）

        text_positions: 列表，每个元素为 (x, y, text, font_size, color, bg_type)
        """
        try:
            img_path = os.path.join(self.second_icons_dir, base_filename)
            if os.path.exists(img_path):
                img = Image.open(img_path).convert('RGBA')
                draw = ImageDraw.Draw(img)

                try:
                    if sys.platform == 'android':
                        font_paths = [
                            "/system/fonts/DroidSansFallback.ttf",
                            "/system/fonts/NotoSansCJK-Regular.ttc",
                            "/system/fonts/Roboto-Regular.ttf"
                        ]
                        font_path = None
                        for fp in font_paths:
                            if os.path.exists(fp):
                                font_path = fp
                                break
                        if font_path:
                            font_24 = ImageFont.truetype(font_path, 24)
                            font_16 = ImageFont.truetype(font_path, 16)
                            font_14 = ImageFont.truetype(font_path, 14)
                            font_12 = ImageFont.truetype(font_path, 12)
                        else:
                            raise Exception("No Chinese font found")
                    else:
                        font_path = "C:/Windows/Fonts/msyh.ttc"
                        font_24 = ImageFont.truetype(font_path, 24)
                        font_16 = ImageFont.truetype(font_path, 16)
                        font_14 = ImageFont.truetype(font_path, 14)
                        font_12 = ImageFont.truetype(font_path, 12)
                except:
                    font_24 = ImageFont.load_default()
                    font_16 = font_24
                    font_14 = font_24
                    font_12 = font_24

                bg_cover_path = os.path.join(self.second_icons_dir, '下期还款日期及还款金额覆盖底色.png')
                bg_cover_img = None
                if os.path.exists(bg_cover_path):
                    bg_cover_img = Image.open(bg_cover_path).convert('RGBA')

                for item in text_positions:
                    x, y, text, font_size, color, bg_type = item

                    if font_size == 24:
                        use_font = font_24
                    elif font_size == 16:
                        use_font = font_16
                    elif font_size == 14:
                        use_font = font_14
                    else:
                        use_font = font_12

                    if bg_type == 'principal':
                        cover_x = 97
                        cover_y = 116
                        cover_width = 130
                        cover_height = 25
                        text_x = 97
                        text_y = 116
                    elif bg_type == 'repayment_amount':
                        cover_x = 122
                        cover_y = 148
                        cover_width = 100
                        cover_height = 25
                        text_x = 122
                        text_y = 149
                    elif bg_type == 'repayment_date':
                        cover_x = 305
                        cover_y = 150
                        cover_width = 95
                        cover_height = 20
                        text_x = 305
                        text_y = 150
                    else:
                        cover_x = x - 10
                        cover_y = y - 5
                        cover_width = 120
                        cover_height = 25
                        text_x = x
                        text_y = y

                    if bg_type in ['repayment_amount', 'repayment_date'] and bg_cover_img:
                        bg_cover_resized = bg_cover_img.resize((cover_width, cover_height), Image.LANCZOS)
                        img.paste(bg_cover_resized, (cover_x, cover_y), bg_cover_resized)
                    else:
                        draw.rectangle(
                            [cover_x, cover_y, cover_x + cover_width, cover_y + cover_height],
                            fill='#ffffff'
                        )

                    draw.text((text_x, text_y), text, fill=color, font=use_font)

                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                core_image = CoreImage(BytesIO(img_byte_arr.read()), ext='png')

                return core_image, img.size
            else:
                logger.log(f"图片不存在: {img_path}", "WARNING")
                return None, None
        except Exception as e:
            logger.log_error(f"创建第二页文字图片失败: {base_filename}", e)
            return None, None

    def create_housing_loan_card(self):
        """创建住房贷款卡片（带动态文字覆盖）"""
        text_positions = [
            (97, 116, self.housing_principal, 16, '#666666', 'principal'),
            (122, 149, self.next_repayment_amount, 16, '#666666', 'repayment_amount'),
            (305, 150, self.next_repayment_date, 14, '#ff0000', 'repayment_date'),
        ]

        return self.create_text_image_for_page2('我的住房贷款.png', text_positions)
