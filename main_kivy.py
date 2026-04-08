import os
import sys

# 最先导入日志模块（在任何 Kivy 导入之前）
from logger import logger

# 立即初始化日志
logger.setup()
logger.log("===== 应用开始加载 =====")
logger.log(f"Python 版本: {sys.version}")
logger.log(f"平台: {sys.platform}")
logger.log(f"工作目录: {os.getcwd()}")

# 在导入 Kivy 之前设置环境变量
if sys.platform == 'android':
    logger.log("检测到 Android 平台")
    os.environ['KIVY_WINDOW'] = 'sdl2'
    os.environ['KIVY_METRICS_DENSITY'] = '1'
else:
    logger.log("非 Android 平台")

# 现在导入 Kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.behaviors import ButtonBehavior
from PIL import Image, ImageDraw, ImageFont
from kivy.core.image import Image as CoreImage
from io import BytesIO
from datetime import datetime
import traceback

logger.log("Kivy 模块导入成功")

# 不在 Android 上设置固定窗口大小（这可能导致闪退）
if sys.platform != 'android':
    Window.size = (360, 740)
    logger.log(f"设置窗口大小: {Window.size}")
else:
    logger.log("Android 平台，不设置固定窗口大小")
    # Android 上使用默认窗口配置
    Window.clearcolor = (0.96, 0.96, 0.96, 1)

Window.clearcolor = (0.96, 0.96, 0.96, 1)
logger.log("窗口配置完成")

from page2_manager import Page2Manager
from page3_manager import ThirdPageScreen

logger.log("所有自定义模块导入成功")


class ImageButton(ButtonBehavior, KivyImage):
    """可点击的图片按钮"""
    pass


class FirstPageScreen(Screen):
    """第一页"""

    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        logger.log("FirstPageScreen 初始化")

    def build_ui(self):
        try:
            logger.log("开始构建第一页 UI")
            from kivy.uix.scrollview import ScrollView
            from kivy.uix.gridlayout import GridLayout

            scroll_view = ScrollView(size_hint=(1, 1))
            content_layout = GridLayout(cols=1, size_hint_y=None, padding=12, spacing=4)
            content_layout.bind(minimum_height=content_layout.setter('height'))

            content_layout.add_widget(self.app_instance.create_status_bar())
            content_layout.add_widget(self.app_instance.create_user_card())
            content_layout.add_widget(self.app_instance.create_menu())
            content_layout.add_widget(self.app_instance.create_assets_card())
            content_layout.add_widget(self.app_instance.create_income_card())
            content_layout.add_widget(self.app_instance.create_bottom_nav())

            scroll_view.add_widget(content_layout)
            logger.log("第一页 UI 构建成功")
            return scroll_view
        except Exception as e:
            logger.log_error("第一页 UI 构建失败", e)
            raise


class SecondPageScreen(Screen):
    """第二页"""

    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        logger.log("SecondPageScreen 初始化")
        try:
            self.page2_manager = Page2Manager(app_instance.second_icons_dir)
            logger.log("Page2Manager 初始化成功")
        except Exception as e:
            logger.log_error("Page2Manager 初始化失败", e)
            raise

    def build_ui(self):
        try:
            logger.log("开始构建第二页 UI")
            from kivy.uix.scrollview import ScrollView

            scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
            main_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=1, padding=(0, 0, 0, 0))
            main_layout.bind(minimum_height=main_layout.setter('height'))

            # 第一张：贷款金额图片（置顶，可点击）
            loan_amount_img_path = os.path.join(self.app_instance.second_icons_dir, '贷款金额.png')
            logger.log(f"检查贷款金额图片: {loan_amount_img_path}")

            if os.path.exists(loan_amount_img_path):
                logger.log("贷款金额图片存在")
                from PIL import Image as PILImage
                try:
                    pil_img = PILImage.open(loan_amount_img_path)
                    img_width, img_height = pil_img.size
                    scaled_height = int(img_height * (360 / img_width))
                    logger.log(f"贷款金额图片尺寸: {img_width}x{img_height}, 缩放后高度: {scaled_height}")

                    loan_layout = BoxLayout(size_hint_y=None, height=scaled_height)
                    loan_widget = ImageButton(source=loan_amount_img_path, size_hint=(1, 1), allow_stretch=True,
                                              keep_ratio=False)

                    loan_widget.bind(on_touch_down=self.on_loan_image_click)

                    loan_layout.add_widget(loan_widget)
                    main_layout.add_widget(loan_layout)
                    logger.log("贷款金额图片组件添加成功")
                except Exception as e:
                    logger.log_error(f"加载贷款金额图片失败", e)
            else:
                logger.log("贷款金额图片不存在", "WARNING")

            # 第二张：我的住房贷款图片
            logger.log("开始创建住房贷款卡片")
            housing_loan_layout = self.create_housing_loan_card()
            main_layout.add_widget(housing_loan_layout)
            logger.log("住房贷款卡片添加成功")

            scroll_view.add_widget(main_layout)
            logger.log("第二页 UI 构建成功")
            return scroll_view
        except Exception as e:
            logger.log_error("第二页 UI 构建失败", e)
            raise

    def on_loan_image_click(self, instance, touch):
        """处理贷款金额图片的点击事件"""
        if not instance.collide_point(*touch.pos):
            return False

        img_width = instance.width
        img_height = instance.height

        touch_x = touch.x - instance.x
        touch_y = touch.y - instance.y

        logger.log(f"点击图片位置：({touch_x:.1f}, {touch_y:.1f}), 图片尺寸：{img_width}x{img_height}")

        if touch_x < 60 and touch_y > img_height - 80:
            logger.log("点击了返回按钮，跳回第一页")
            self.app_instance.sm.current = 'first_page'
            return True

        if touch_x > 300 and touch_y < 200:
            logger.log("点击了还款计划，跳转到第三页")
            self.app_instance.sm.current = 'third_page'
            return True

        return False

    def create_housing_loan_card(self):
        """创建住房贷款卡片"""
        try:
            logger.log("调用 Page2Manager.create_housing_loan_card")
            core_image, size = self.page2_manager.create_housing_loan_card()

            if core_image:
                img_width, img_height = size
                logger.log(f"住房贷款卡片图片创建成功: {img_width}x{img_height}")
                container = BoxLayout(size_hint_y=None, height=img_height)
                img_widget = KivyImage(texture=core_image.texture, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
                container.add_widget(img_widget)
                return container
            else:
                logger.log("住房贷款卡片图片创建失败，使用占位符", "WARNING")
                return BoxLayout(size_hint_y=None, height=300)
        except Exception as e:
            logger.log_error("create_housing_loan_card 异常", e)
            return BoxLayout(size_hint_y=None, height=300)


class FinanceApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        logger.log("FinanceApp 初始化开始")

        self.total_assets = "0"
        self.total_liabilities = "512,922.29"
        self.loan_amount = "512,922.29"
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.icons_dir = os.path.join(base_dir, 'icons', 'first_icons')
        self.second_icons_dir = os.path.join(base_dir, 'icons', 'second_icons')
        self.third_icons_dir = os.path.join(base_dir, 'icons', 'third_icons')
        
        logger.log(f"基础目录: {base_dir}")
        logger.log(f"icons 目录: {self.icons_dir}")
        logger.log(f"second_icons 目录: {self.second_icons_dir}")
        logger.log(f"third_icons 目录: {self.third_icons_dir}")
        
        for dir_name, dir_path in [
            ('icons', self.icons_dir),
            ('second_icons', self.second_icons_dir),
            ('third_icons', self.third_icons_dir)
        ]:
            if os.path.exists(dir_path):
                files = os.listdir(dir_path)
                logger.log(f"{dir_name} 目录存在，包含 {len(files)} 个文件: {files[:3]}...")
            else:
                logger.log(f"警告: {dir_name} 目录不存在: {dir_path}", "WARNING")
        
        logger.log("FinanceApp 初始化完成")

    def build(self):
        try:
            logger.log("========== 开始构建 UI ==========")
            
            self.sm = ScreenManager(transition=NoTransition())
            logger.log("ScreenManager 创建成功")

            logger.log("创建第一页")
            self.first_page = FirstPageScreen(app_instance=self, name='first_page')
            self.first_page.add_widget(self.first_page.build_ui())
            self.sm.add_widget(self.first_page)
            logger.log("✓ 第一页添加成功")

            logger.log("创建第二页")
            self.second_page = SecondPageScreen(app_instance=self, name='second_page')
            self.second_page.add_widget(self.second_page.build_ui())
            self.sm.add_widget(self.second_page)
            logger.log("✓ 第二页添加成功")

            logger.log("创建第三页")
            self.third_page = ThirdPageScreen(app_instance=self, name='third_page')
            self.third_page.add_widget(self.third_page.build_ui())
            self.sm.add_widget(self.third_page)
            logger.log("✓ 第三页添加成功")

            Clock.schedule_interval(self.update_time, 1)
            logger.log("定时器设置成功")
            
            logger.log("========== UI 构建完成 ==========")
            return self.sm

        except Exception as e:
            logger.log_error("UI 构建失败", e)
            
            error_layout = BoxLayout(orientation='vertical')
            error_layout.add_widget(Label(
                text=f"应用启动失败\n\n错误: {str(e)}\n\n请查看日志文件",
                font_size='14sp',
                halign='center'
            ))
            return error_layout

    def update_time(self, dt):
        """每秒更新当前时间"""
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def on_assets_click(self, instance):
        """跳转到第二页"""
        logger.log("点击资产卡片，跳转到第二页")
        self.sm.current = 'second_page'

    def create_text_image(self, base_filename, text_positions):
        """
        在第一页图片上绘制文字（专用方法）
        """
        try:
            img_path = os.path.join(self.icons_dir, base_filename)
            if os.path.exists(img_path):
                logger.log(f"加载图片: {base_filename}")
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
                            logger.log(f"使用 Android 字体: {font_path}")
                            font_24 = ImageFont.truetype(font_path, 24)
                            font_16 = ImageFont.truetype(font_path, 16)
                            font_12 = ImageFont.truetype(font_path, 12)
                            font_10 = ImageFont.truetype(font_path, 10)
                        else:
                            raise Exception("No Chinese font found")
                    else:
                        font_path = "C:/Windows/Fonts/msyh.ttc"
                        logger.log(f"使用 Windows 字体: {font_path}")
                        font_24 = ImageFont.truetype(font_path, 24)
                        font_16 = ImageFont.truetype(font_path, 16)
                        font_12 = ImageFont.truetype(font_path, 12)
                        font_10 = ImageFont.truetype(font_path, 10)
                except Exception as e:
                    logger.log_error(f"字体加载失败，使用默认字体", e)
                    font_24 = ImageFont.load_default()
                    font_16 = font_24
                    font_12 = font_24
                    font_10 = font_24

                for item in text_positions:
                    if len(item) == 6:
                        x, y, text, font_size, color, bg_type = item
                    else:
                        x, y, text, font_size, color, bg_type, _ = item

                    if font_size == 24:
                        use_font = font_24
                    elif font_size == 16:
                        use_font = font_16
                    elif font_size == 12:
                        use_font = font_12
                    elif font_size == 10:
                        use_font = font_10
                    else:
                        use_font = font_12

                    if bg_type == 'white':
                        cover_x = 180
                        cover_y = 70
                        cover_width = 134
                        cover_height = 28
                        text_x = 185
                        text_y = 70
                    elif bg_type == 'loan':
                        cover_x = 200
                        cover_y = 134
                        cover_width = 85
                        cover_height = 20
                        text_x = 208
                        text_y = 135
                    elif bg_type == 'login_time':
                        cover_x = 85
                        cover_y = 55
                        cover_width = 180
                        cover_height = 20
                        text_x = 85
                        text_y = 55
                    else:
                        cover_x = x - 10
                        cover_y = y - 5
                        cover_width = 120
                        cover_height = 25
                        text_x = x
                        text_y = y

                    if bg_type == 'loan':
                        bg_img_path = os.path.join(self.icons_dir, '贷款金额覆盖参考.png')
                        if os.path.exists(bg_img_path):
                            bg_img = Image.open(bg_img_path).convert('RGBA')
                            bg_img_resized = bg_img.resize((cover_width, cover_height), Image.LANCZOS)
                            img.paste(bg_img_resized, (cover_x, cover_y), bg_img_resized)
                        else:
                            draw.rectangle(
                                [cover_x, cover_y, cover_x + cover_width, cover_y + cover_height],
                                fill='#ffffff'
                            )
                    elif bg_type == 'login_time':
                        bg_img_path = os.path.join(self.icons_dir, '权益中心下时间的覆盖色.png')
                        if os.path.exists(bg_img_path):
                            bg_img = Image.open(bg_img_path).convert('RGBA')
                            bg_img_resized = bg_img.resize((cover_width, cover_height), Image.LANCZOS)
                            img.paste(bg_img_resized, (cover_x, cover_y), bg_img_resized)
                        else:
                            draw.rectangle(
                                [cover_x, cover_y, cover_x + cover_width, cover_y + cover_height],
                                fill='#ffffff'
                            )
                    elif bg_type == 'white':
                        draw.rectangle(
                            [cover_x, cover_y, cover_x + cover_width, cover_y + cover_height],
                            fill='#ffffff'
                        )
                    else:
                        draw.rectangle(
                            [cover_x, cover_y, cover_x + cover_width, cover_y + cover_height],
                            fill=bg_type
                        )

                    draw.text((text_x, text_y), text, fill=color, font=use_font)

                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                core_image = CoreImage(BytesIO(img_byte_arr.read()), ext='png')

                logger.log(f"图片处理成功: {base_filename}")
                return core_image, img.size
            else:
                logger.log(f"图片不存在: {img_path}", "WARNING")
                return None, None
        except Exception as e:
            logger.log_error(f"创建文字图片失败: {base_filename}", e)
            return None, None

    def create_status_bar(self):
        layout = BoxLayout(size_hint_y=None, height=50)
        img_path = os.path.join(self.icons_dir, '设置_消息_按钮.png')
        if os.path.exists(img_path):
            img = KivyImage(source=img_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        else:
            logger.log("状态栏图片不存在，使用占位符", "WARNING")
            layout.add_widget(Label(text='状态栏', size_hint_y=None, height=50))
        return layout

    def create_user_card(self):
        text_positions = [
            (85, 55, "上次登录 " + self.last_login_time, 10, '#666666', 'login_time'),
        ]

        core_image, size = self.create_text_image('个人信息.png', text_positions)

        if core_image:
            img_width, img_height = size
            container = BoxLayout(size_hint_y=None, height=img_height)
            img_widget = KivyImage(texture=core_image.texture, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            container.add_widget(img_widget)
            return container
        else:
            logger.log("用户卡片图片处理失败，使用占位符", "WARNING")
            return BoxLayout(size_hint_y=None, height=180)

    def create_menu(self):
        layout = BoxLayout(size_hint_y=None, height=80)
        img_path = os.path.join(self.icons_dir, '年度账单_商城订单_信用报告_办理进度_更多.png')
        if os.path.exists(img_path):
            img = KivyImage(source=img_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        else:
            logger.log("菜单图片不存在，使用占位符", "WARNING")
            layout.add_widget(Label(text='菜单', size_hint_y=None, height=80))
        return layout

    def create_assets_card(self):
        text_positions = [
            (185, 55, self.total_liabilities, 24, '#333333', 'white'),
            (225, 88, self.loan_amount, 16, '#333333', 'loan'),
        ]

        core_image, size = self.create_text_image('我的资产负债.png', text_positions)

        if core_image:
            img_width, img_height = size
            container = BoxLayout(size_hint_y=None, height=img_height)

            img_widget = ImageButton(
                texture=core_image.texture,
                size_hint=(1, 1),
                allow_stretch=True,
                keep_ratio=True
            )

            img_widget.bind(on_press=self.on_assets_click)

            container.add_widget(img_widget)
            return container
        else:
            logger.log("资产卡片图片处理失败，使用占位符", "WARNING")
            return BoxLayout(size_hint_y=None, height=220)

    def create_income_card(self):
        layout = BoxLayout(size_hint_y=None, height=150)
        img_path = os.path.join(self.icons_dir, '我的本月收支.png')
        if os.path.exists(img_path):
            img = KivyImage(source=img_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        else:
            logger.log("收支卡片图片不存在，使用占位符", "WARNING")
            layout.add_widget(Label(text='本月收支', size_hint_y=None, height=150))
        return layout

    def create_bottom_nav(self):
        layout = BoxLayout(size_hint_y=None, height=60)
        img_path = os.path.join(self.icons_dir, '底部按钮.png')
        if os.path.exists(img_path):
            img = KivyImage(source=img_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        else:
            logger.log("底部导航图片不存在，使用占位符", "WARNING")
            layout.add_widget(Label(text='底部导航', size_hint_y=None, height=60))
        return layout


if __name__ == '__main__':
    try:
        logger.log("========================================")
        logger.log("应用主入口启动")
        logger.log("========================================")
        app = FinanceApp()
        logger.log("FinanceApp 实例创建成功，开始运行")
        app.run()
    except Exception as e:
        logger.log_error("应用运行异常", e)
        # 即使崩溃也要确保日志被写入
        import time
        time.sleep(2)  # 等待日志写入
        raise
