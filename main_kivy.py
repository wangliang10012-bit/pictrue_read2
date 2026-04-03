from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from datetime import datetime
import os

# 设置窗口大小（移动端尺寸）
Window.size = (360, 740)
Window.clearcolor = (0.96, 0.96, 0.96, 1)  # #f5f5f5 背景色


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
        self.icons_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons')

    def build(self):
        # 创建主布局（可滚动）
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.gridlayout import GridLayout

        # 创建滚动视图
        scroll_view = ScrollView(size_hint=(1, 1))

        # 创建内容布局
        content_layout = GridLayout(cols=1, size_hint_y=None, padding=12, spacing=4)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        # 添加各个组件
        content_layout.add_widget(self.create_status_bar())
        content_layout.add_widget(self.create_user_card())
        content_layout.add_widget(self.create_menu())
        content_layout.add_widget(self.create_time_display())
        content_layout.add_widget(self.create_assets_card())
        content_layout.add_widget(self.create_income_card())
        content_layout.add_widget(self.create_bottom_nav())

        scroll_view.add_widget(content_layout)

        return scroll_view

    def create_status_bar(self):
        layout = BoxLayout(size_hint_y=None, height=50)
        img_path = os.path.join(self.icons_dir, '设置_消息_按钮.png')
        if os.path.exists(img_path):
            img = Image(source=img_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        else:
            layout.add_widget(Label(text='状态栏', size_hint_y=None, height=50))
        return layout

    def create_user_card(self):
        layout = BoxLayout(size_hint_y=None, height=180)
        img_path = os.path.join(self.icons_dir, '个人信息.png')
        if os.path.exists(img_path):
            img = Image(source=img_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        else:
            layout.add_widget(Label(text='用户信息', size_hint_y=None, height=180))
        return layout

    def create_menu(self):
        layout = BoxLayout(size_hint_y=None, height=80)
        img_path = os.path.join(self.icons_dir, '年度账单_商城订单_信用报告_办理进度_更多.png')
        if os.path.exists(img_path):
            img = Image(source=img_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        else:
            layout.add_widget(Label(text='菜单', size_hint_y=None, height=80))
        return layout

    def create_time_display(self):
        layout = BoxLayout(size_hint_y=None, height=30, padding=(10, 0))
        label = Label(
            text=f"时间 {self.current_time}",
            font_size='10sp',
            color=(0.6, 0.6, 0.6, 1),
            halign='left',
            valign='middle',
            size_hint_y=None,
            height=30
        )
        layout.add_widget(label)
        return layout

    def create_assets_card(self):
        layout = BoxLayout(size_hint_y=None, height=220)
        img_path = os.path.join(self.icons_dir, '我的资产负债.png')
        if os.path.exists(img_path):
            img = Image(source=img_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        else:
            layout.add_widget(Label(text='资产负债', size_hint_y=None, height=220))
        return layout

    def create_income_card(self):
        layout = BoxLayout(size_hint_y=None, height=150)
        img_path = os.path.join(self.icons_dir, '我的本月收支.png')
        if os.path.exists(img_path):
            img = Image(source=img_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        else:
            layout.add_widget(Label(text='本月收支', size_hint_y=None, height=150))
        return layout

    def create_bottom_nav(self):
        layout = BoxLayout(size_hint_y=None, height=60)
        img_path = os.path.join(self.icons_dir, '底部按钮.png')
        if os.path.exists(img_path):
            img = Image(source=img_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        else:
            layout.add_widget(Label(text='底部导航', size_hint_y=None, height=60))
        return layout


if __name__ == '__main__':
    FinanceApp().run()
