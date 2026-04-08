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
import os
import sys
import traceback
from page2_manager import Page2Manager
from page3_manager import ThirdPageScreen

# 不在 Android 上设置固定窗口大小
if sys.platform != 'android':
    Window.size = (360, 740)

Window.clearcolor = (0.96, 0.96, 0.96, 1)


class ImageButton(ButtonBehavior, KivyImage):
    """可点击的图片按钮"""
    pass


class FirstPageScreen(Screen):
    """第一页"""

    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance

    def build_ui(self):
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
        return scroll_view


class SecondPageScreen(Screen):
    """第二页"""

    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        self.page2_manager = Page2Manager(app_instance.second_icons_dir)

    def build_ui(self):
        from kivy.uix.scrollview import ScrollView

        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        main_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=1, padding=(0, 0, 0, 0))
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # 第一张：贷款金额图片（置顶，可点击）
        loan_amount_img_path = os.path.join(self.app_instance.second_icons_dir, '贷款金额.png')

        if os.path.exists(loan_amount_img_path):
            from PIL import Image as PILImage
            try:
                pil_img = PILImage.open(loan_amount_img_path)
                img_width, img_height = pil_img.size
                scaled_height = int(img_height * (360 / img_width))

                # 创建可点击的容器
                loan_layout = BoxLayout(size_hint_y=None, height=scaled_height)
                loan_widget = ImageButton(source=loan_amount_img_path, size_hint=(1, 1), allow_stretch=True,
                                          keep_ratio=False)

                # 绑定 on_touch_down 事件来获取点击位置
                loan_widget.bind(on_touch_down=self.on_loan_image_click)

                loan_layout.add_widget(loan_widget)
                main_layout.add_widget(loan_layout)
            except Exception as e:
                print(f"加载贷款金额图片失败: {e}")

        # 第二张：我的住房贷款图片
        housing_loan_layout = self.create_housing_loan_card()
        main_layout.add_widget(housing_loan_layout)

        scroll_view.add_widget(main_layout)
        return scroll_view

    def on_loan_image_click(self, instance, touch):
        """处理贷款金额图片的点击事件"""
        # 检查触摸是否在组件内
        if not instance.collide_point(*touch.pos):
            return False

        # 获取图片尺寸
        img_width = instance.width
        img_height = instance.height

        # 获取点击位置（相对于图片）
        touch_x = touch.x - instance.x
        touch_y = touch.y - instance.y

        print(f"点击图片位置：({touch_x:.1f}, {touch_y:.1f}), 图片尺寸：{img_width}x{img_height}")

        # 判断点击区域
        # "<" 返回按钮：左上角区域 (x < 60, y > img_height - 80)
        if touch_x < 60 and touch_y > img_height - 80:
            print("点击了返回按钮，跳回第一页")
            self.app_instance.sm.current = 'first_page'
            return True

        # "还款计划" 图标：根据实际点击位置调整 (x > 300, y < 200)
        # 用户反馈的点击位置：(331, 158)
        if touch_x > 300 and touch_y < 200:
            print("点击了还款计划，跳转到第三页")
            self.app_instance.sm.current = 'third_page'
            return True

        return False

    def create_housing_loan_card(self):
        """创建住房贷款卡片"""
        core_image, size = self.page2_manager.create_housing_loan_card()

        if core_image:
            img_width, img_height = size
            container = BoxLayout(size_hint_y=None, height=img_height)
            img_widget = KivyImage(texture=core_image.texture, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            container.add_widget(img_widget)
            return container
        else:
            return BoxLayout(size_hint_y=None, height=300)


class FinanceApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 可配置的数据
        self.total_assets = "0"  # 总资产
        self.total_liabilities = "512,922.29"  # 总负债
        self.loan_amount = "512,922.29"  # 贷款金额（贷款进度区域）
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 时间（动态获取当前时间）
        self.last_login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 上次登录时间（动态获取当前时间）

        # 获取图标目录
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.icons_dir = os.path.join(base_dir, 'icons', 'first_icons')
        self.second_icons_dir = os.path.join(base_dir, 'icons', 'second_icons')
        self.third_icons_dir = os.path.join(base_dir, 'icons', 'third_icons')

    def build(self):
        try:
            # 创建屏幕管理器（使用 NoTransition 去掉切换动画）
            self.sm = ScreenManager(transition=NoTransition())

            # 第一页
            self.first_page = FirstPageScreen(app_instance=self, name='first_page')
            self.first_page.add_widget(self.first_page.build_ui())
            self.sm.add_widget(self.first_page)

            # 第二页
            self.second_page = SecondPageScreen(app_instance=self, name='second_page')
            self.second_page.add_widget(self.second_page.build_ui())
            self.sm.add_widget(self.second_page)

            # 第三页
            self.third_page = ThirdPageScreen(app_instance=self, name='third_page')
            self.third_page.add_widget(self.third_page.build_ui())
            self.sm.add_widget(self.third_page)

            # 定时更新时间（每秒更新一次）
            Clock.schedule_interval(self.update_time, 1)

            return self.sm

        except Exception as e:
            error_msg = f"应用启动失败\n\n错误: {str(e)}\n\n请检查日志"
            print(error_msg)
            traceback.print_exc()

            # 返回一个简单的错误提示界面
            error_layout = BoxLayout(orientation='vertical')
            error_layout.add_widget(Label(
                text=error_msg,
                font_size='14sp',
                halign='center'
            ))
            return error_layout

    def update_time(self, dt):
        """每秒更新当前时间"""
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def on_assets_click(self, instance):
        """跳转到第二页"""
        self.sm.current = 'second_page'

    def create_text_image(self, base_filename, text_positions):
        """
        在第一页图片上绘制文字（专用方法）

        text_positions: 列表，每个元素为 (x, y, text, font_size, color, bg_type)
        """
        try:
            img_path = os.path.join(self.icons_dir, base_filename)
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
                            font_24 = ImageFont.truetype(font_path, 24)
                            font_16 = ImageFont.truetype(font_path, 16)
                            font_12 = ImageFont.truetype(font_path, 12)
                            font_10 = ImageFont.truetype(font_path, 10)
                        else:
                            raise Exception("No Chinese font found")
                    else:
                        # Windows 系统字体路径
                        font_path = "C:/Windows/Fonts/msyh.ttc"
                        font_24 = ImageFont.truetype(font_path, 24)
                        font_16 = ImageFont.truetype(font_path, 16)
                        font_12 = ImageFont.truetype(font_path, 12)
                        font_10 = ImageFont.truetype(font_path, 10)
                except:
                    # 使用默认字体
                    font_24 = ImageFont.load_default()
                    font_16 = font_24
                    font_12 = font_24
                    font_10 = font_24

                # 绘制每个文字
                for item in text_positions:
                    if len(item) == 6:
                        x, y, text, font_size, color, bg_type = item
                    else:
                        x, y, text, font_size, color, bg_type, _ = item

                    # 选择字体
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

                    # 固定的覆盖区域坐标
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

                    # 绘制背景覆盖
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

                    # 绘制新文字
                    draw.text((text_x, text_y), text, fill=color, font=use_font)

                # 将 PIL Image 转换为 Kivy Image
                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                core_image = CoreImage(BytesIO(img_byte_arr.read()), ext='png')

                return core_image, img.size
            else:
                return None, None
        except Exception as e:
            print(f"创建文字图片失败：{e}")
            traceback.print_exc()
            return None, None

    def create_status_bar(self):
        layout = BoxLayout(size_hint_y=None, height=50)
        img_path = os.path.join(self.icons_dir, '设置_消息_按钮.png')
        if os.path.exists(img_path):
            img = KivyImage(source=img_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        else:
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
            return BoxLayout(size_hint_y=None, height=180)

    def create_menu(self):
        layout = BoxLayout(size_hint_y=None, height=80)
        img_path = os.path.join(self.icons_dir, '年度账单_商城订单_信用报告_办理进度_更多.png')
        if os.path.exists(img_path):
            img = KivyImage(source=img_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        else:
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
            return BoxLayout(size_hint_y=None, height=220)

    def create_income_card(self):
        layout = BoxLayout(size_hint_y=None, height=150)
        img_path = os.path.join(self.icons_dir, '我的本月收支.png')
        if os.path.exists(img_path):
            img = KivyImage(source=img_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        else:
            layout.add_widget(Label(text='本月收支', size_hint_y=None, height=150))
        return layout

    def create_bottom_nav(self):
        layout = BoxLayout(size_hint_y=None, height=60)
        img_path = os.path.join(self.icons_dir, '底部按钮.png')
        if os.path.exists(img_path):
            img = KivyImage(source=img_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        else:
            layout.add_widget(Label(text='底部导航', size_hint_y=None, height=60))
        return layout


if __name__ == '__main__':
    FinanceApp().run()
