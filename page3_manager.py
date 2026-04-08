from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from PIL import Image, ImageDraw, ImageFont
from kivy.core.image import Image as CoreImage
from io import BytesIO
import os
import sys


class Page3Manager:
    """第三页管理器：处理还款计划图片的文字覆盖"""

    def __init__(self, third_icons_dir):
        self.third_icons_dir = third_icons_dir

        # 可配置的数据
        self.period_37_date = "2026-04-27"
        self.period_37_principal = "957.84"
        self.period_37_interest = "1,495.96"
        self.period_37_total = "2,453.80"

        self.period_38_date = "2026-05-27"
        self.period_38_principal = "960.64"
        self.period_38_interest = "1,493.16"
        self.period_38_total = "2,453.80"

    def create_text_image_for_page3(self, base_filename, text_positions):
        """
        在第三页图片上绘制文字

        text_positions: 列表，每个元素为 (x, y, text, font_size, color)
        """
        try:
            img_path = os.path.join(self.third_icons_dir, base_filename)
            if os.path.exists(img_path):
                img = Image.open(img_path).convert('RGBA')
                draw = ImageDraw.Draw(img)

                # 加载中文字体 - 兼容 Android
                try:
                    if sys.platform == 'android':
                        # Android 系统字体路径
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
                            available_sizes = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24]
                            fonts = {size: ImageFont.truetype(font_path, size) for size in available_sizes}
                        else:
                            raise Exception("No Chinese font found")
                    else:
                        # Windows 系统字体路径
                        font_path = "C:/Windows/Fonts/msyh.ttc"
                        available_sizes = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24]
                        fonts = {size: ImageFont.truetype(font_path, size) for size in available_sizes}
                except:
                    default_font = ImageFont.load_default()
                    fonts = {size: default_font for size in range(8, 30)}

                # 绘制每个文字
                for item in text_positions:
                    x, y, text, font_size, color = item
                    use_font = fonts.get(font_size, fonts[14])

                    # 获取文本边界框
                    bbox = draw.textbbox((0, 0), text, font=use_font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]

                    # 覆盖区域优化：
                    # 向左延伸 12px（包含原有的 2px + 新增的 10px）
                    # 向下延伸 12px（包含原有的 2px + 新增的 10px，通过 padding*6 实现）
                    cover_x = x - 12
                    cover_y = y - 2
                    cover_width = text_width + 14  # 右侧保留 2px 边距
                    cover_height = text_height + 12

                    draw.rectangle(
                        [cover_x, cover_y, cover_x + cover_width, cover_y + cover_height],
                        fill='#ffffff'
                    )

                    # 绘制新文字
                    draw.text((x, y), text, fill=color, font=use_font)

                # 将 PIL Image 转换为 Kivy Image
                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                core_image = CoreImage(BytesIO(img_byte_arr.read()), ext='png')

                return core_image, img.size
            else:
                return None, None
        except Exception as e:
            print(f"创建第三页文字图片失败：{e}")
            import traceback
            traceback.print_exc()
            return None, None

    def create_repayment_plan_card(self):
        """创建还款计划卡片"""
        # 定义需要覆盖的文字位置和样式
        # 注意：请根据你的实际截图微调坐标
        text_positions = [
            # 第 37 期数据
            (300, 362, self.period_37_date, 18, '#666666'),
            (330, 405, self.period_37_principal, 17, '#666666'),
            (315, 445, self.period_37_interest, 17, '#666666'),
            (315, 526, self.period_37_total, 17, '#666666'),

            # 第 38 期数据
            (300, 622, self.period_38_date, 18, '#666666'),
            (330, 663, self.period_38_principal, 17, '#666666'),
            (315, 703, self.period_38_interest, 17, '#666666'),
            (315, 786, self.period_38_total, 17, '#666666'),
        ]

        return self.create_text_image_for_page3('还款计划.png', text_positions)


class ThirdPageScreen(Screen):
    """第三页：还款计划"""

    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        self.page3_manager = Page3Manager(app_instance.third_icons_dir)

    def build_ui(self):
        # 创建滚动视图
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)

        # 主内容布局
        main_layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=(0, 0, 0, 0))
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # 还款计划图片（带文字覆盖）
        core_image, size = self.page3_manager.create_repayment_plan_card()

        if core_image:
            img_width, img_height = size
            container = BoxLayout(size_hint_y=None, height=img_height)

            # 创建可点击的图片组件
            img_widget = KivyImage(texture=core_image.texture, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)

            # 绑定触摸事件
            img_widget.bind(on_touch_down=self.on_screen_touch)

            container.add_widget(img_widget)
            main_layout.add_widget(container)
        else:
            placeholder = BoxLayout(size_hint_y=None, height=500)
            placeholder.add_widget(Label(text='还款计划图片', font_size='20sp'))
            main_layout.add_widget(placeholder)

        scroll_view.add_widget(main_layout)
        return scroll_view

    def on_screen_touch(self, instance, touch):
        """处理屏幕点击事件"""
        # 检查触摸是否在组件内
        if not instance.collide_point(*touch.pos):
            return False

        # 获取点击位置（相对于图片）
        touch_x = touch.x - instance.x
        touch_y = touch.y - instance.y

        img_width = instance.width
        img_height = instance.height

        print(f"第三页点击图片位置：({touch_x:.1f}, {touch_y:.1f}), 图片尺寸：{img_width}x{img_height}")

        # 判断点击区域
        # "<" 返回按钮：左上角区域，基于坐标 (25.0, 798.0)
        # 设置合理的点击范围：x 在 0-60 之间，y 在 780-820 之间
        if 0 <= touch_x <= 60 and 780 <= touch_y <= 820:
            print("点击了返回按钮，跳回第二页")
            self.app_instance.sm.current = 'second_page'
            return True

        return False
