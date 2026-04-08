import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
from datetime import datetime


class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("我的资产")
        self.root.geometry("360x740")
        self.root.configure(bg='#f5f5f5')
        self.root.resizable(False, False)

        self.images = {}
        self.icons_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'first_icons')

        # 统一的间距设置
        self.padding_x = 12
        self.padding_y = 4

        # 可配置的数据
        self.total_assets = "0"  # 总资产
        self.total_liabilities = "512,922.29"  # 总负债
        self.loan_amount = "512,922.29"  # 贷款金额（贷款进度区域）
        self.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 时间（动态获取当前时间）
        self.last_login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 上次登录时间（动态获取当前时间）

        self.create_widgets()

    def load_photo(self, filename, width=None, height=None):
        try:
            img_path = os.path.join(self.icons_dir, filename)
            if os.path.exists(img_path):
                img = Image.open(img_path)

                if width or height:
                    img = img.resize((width or img.width, height or img.height), Image.LANCZOS)

                photo = ImageTk.PhotoImage(img)
                self.images[filename] = photo
                return photo, img.size
            else:
                print(f"图片不存在：{img_path}")
                return None, None
        except Exception as e:
            print(f"加载图片失败：{filename}, 错误：{e}")
            return None, None

    def create_text_image(self, base_filename, text_positions):
        """
        在图片上绘制文字，先用背景色覆盖原位置，再绘制新文字

        text_positions: 列表，每个元素为 (x, y, text, font_size, color, bg_type)

        bg_type: 背景类型
            - 'gradient': 渐变背景（从左到右）
            - 'solid': 纯色背景
            - 'white': 白色背景
            - 'loan': 贷款金额背景
            - 'login_time': 上次登录时间背景
        """

        try:
            img_path = os.path.join(self.icons_dir, base_filename)
            if os.path.exists(img_path):
                img = Image.open(img_path).convert('RGBA')
                draw = ImageDraw.Draw(img)

                # 使用中文字体
                try:
                    font_path = "C:/Windows/Fonts/msyh.ttc"
                    font_24 = ImageFont.truetype(font_path, 24)
                    font_16 = ImageFont.truetype(font_path, 16)
                    font_12 = ImageFont.truetype(font_path, 12)
                    font_10 = ImageFont.truetype(font_path, 10)  # 添加 10 号字体（权益中心字体）
                except:
                    font_24 = ImageFont.load_default()
                    font_16 = font_24
                    font_12 = font_24
                    font_10 = font_24

                # 绘制每个文字
                for item in text_positions:
                    # 解析参数（支持 6 元组和 7 元组）
                    if len(item) == 6:
                        x, y, text, font_size, color, bg_type = item
                    else:  # len(item) == 7
                        x, y, text, font_size, color, bg_type, _ = item

                    # 选择字体（使用参数中的 font_size，不被覆盖）
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

                    # 固定的覆盖区域坐标（绝对坐标，不随文字位置变化）
                    if bg_type == 'gradient':
                        # 总资产：固定覆盖区域（暂时不使用）
                        cover_x = 20  # 覆盖区域左上角 X 坐标
                        cover_y = 70  # 覆盖区域左上角 Y 坐标
                        cover_width = 120  # 覆盖区域宽度
                        cover_height = 32  # 覆盖区域高度
                        text_x = 25  # 文字 X 坐标（在覆盖区域内）
                        text_y = 75  # 文字 Y 坐标（在覆盖区域内）
                    elif bg_type == 'white':
                        # 总负债：固定覆盖区域
                        cover_x = 180  # 覆盖区域左上角 X 坐标
                        cover_y = 70  # 覆盖区域左上角 Y 坐标
                        cover_width = 134  # 覆盖区域宽度
                        cover_height = 28  # 覆盖区域高度
                        text_x = 185  # 文字 X 坐标（在覆盖区域内）
                        text_y = 70  # 文字 Y 坐标（在覆盖区域内）
                    elif bg_type == 'loan':
                        # 贷款金额：固定覆盖区域
                        cover_x = 200  # 覆盖区域左上角 X 坐标
                        cover_y = 134  # 覆盖区域左上角 Y 坐标
                        cover_width = 85  # 覆盖区域宽度（根据数字长度调整）
                        cover_height = 20  # 覆盖区域高度（小字体）
                        text_x = 208  # 文字 X 坐标（在覆盖区域内）
                        text_y = 135  # 文字 Y 坐标（在覆盖区域内）
                        # 注意：这里不再设置 font_size，使用参数中的值
                    elif bg_type == 'login_time':
                        # 上次登录时间：固定覆盖区域
                        cover_x = 85  # 覆盖区域左上角 X 坐标
                        cover_y = 55  # 覆盖区域左上角 Y 坐标
                        cover_width = 180  # 覆盖区域宽度
                        cover_height = 20  # 覆盖区域高度
                        text_x = 85  # 文字 X 坐标（在覆盖区域内）
                        text_y = 55  # 文字 Y 坐标（在覆盖区域内）
                        # 注意：这里不再设置 font_size，使用参数中的值
                    else:
                        # 纯色背景
                        cover_x = x - 10
                        cover_y = y - 5
                        cover_width = 120
                        cover_height = 25
                        text_x = x
                        text_y = y

                    # 绘制背景矩形覆盖原内
                    if bg_type == 'loan':
                        # 贷款金额 - 使用背景图片覆盖
                        bg_img_path = os.path.join(self.icons_dir, '贷款金额覆盖参考.png')
                        if os.path.exists(bg_img_path):
                            bg_img = Image.open(bg_img_path).convert('RGBA')
                            # 调整背景图片尺寸以匹配覆盖区域
                            bg_img_resized = bg_img.resize((cover_width, cover_height), Image.LANCZOS)
                            # 将背景图片粘贴到覆盖区域
                            img.paste(bg_img_resized, (cover_x, cover_y), bg_img_resized)
                        else:
                            # 如果没有背景图片，使用白色背景
                            draw.rectangle(
                                [cover_x, cover_y, cover_x + cover_width, cover_y + cover_height],
                                fill='#ffffff'
                            )
                    elif bg_type == 'login_time':
                        # 上次登录时间 - 使用背景图片覆盖
                        bg_img_path = os.path.join(self.icons_dir, '权益中心下时间的覆盖色.png')
                        if os.path.exists(bg_img_path):
                            bg_img = Image.open(bg_img_path).convert('RGBA')
                            # 调整背景图片尺寸以匹配覆盖区域
                            bg_img_resized = bg_img.resize((cover_width, cover_height), Image.LANCZOS)
                            # 将背景图片粘贴到覆盖区域
                            img.paste(bg_img_resized, (cover_x, cover_y), bg_img_resized)
                        else:
                            # 如果没有背景图片，使用白色背景
                            draw.rectangle(
                                [cover_x, cover_y, cover_x + cover_width, cover_y + cover_height],
                                fill='#ffffff'
                            )


                    elif bg_type == 'white':
                        # 白色背景 - 固定覆盖区域
                        draw.rectangle(
                            [cover_x, cover_y, cover_x + cover_width, cover_y + cover_height],
                            fill='#ffffff'
                        )
                    else:
                        # 纯色背景 - 固定覆盖区域
                        draw.rectangle(
                            [cover_x, cover_y, cover_x + cover_width, cover_y + cover_height],
                            fill=bg_type
                        )


                    # 绘制新文字（使用固定坐标）
                    draw.text((text_x, text_y), text, fill=color, font=use_font)

                photo = ImageTk.PhotoImage(img)
                self.images[base_filename + '_modified'] = photo
                return photo, img.size
            else:
                return None, None
        except Exception as e:
            print(f"创建文字图片失败：{e}")
            return None, None

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg='#f5f5f5')
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_status_bar(main_frame)
        self.create_user_card(main_frame)
        self.create_menu(main_frame)
        self.create_time_display(main_frame)
        self.create_assets_card(main_frame)
        self.create_income_card(main_frame)
        self.create_bottom_nav()

    def create_status_bar(self, parent):
        # 只显示顶部图片，不添加额外文字和图标
        photo, size = self.load_photo('设置_消息_按钮.png', width=330, height=50)

        frame = tk.Frame(parent, bg='#f5f5f5', height=50)
        frame.pack(fill=tk.X, padx=self.padding_x, pady=self.padding_y)
        frame.pack_propagate(False)

        if photo:
            icon_label = tk.Label(frame, image=photo, bg='#f5f5f5')
            icon_label.pack(fill=tk.X, expand=True)

    def create_user_card(self, parent):
        # 在个人信息图片上绘制上次登录时间（使用覆盖图片背景）
        text_positions = [
            # 上次登录时间：在权益中心卡片内，用户名下方
            (85, 55, "上次登录 " + self.last_login_time, 10, '#666666', 'login_time'),
        ]

        photo, size = self.create_text_image('个人信息.png', text_positions)

        if photo:
            img_width, img_height = size

            container = tk.Frame(parent, bg='#f5f5f5', width=img_width, height=img_height)
            container.pack(padx=self.padding_x, pady=self.padding_y)
            container.pack_propagate(False)

            bg_label = tk.Label(container, image=photo, bg='#f5f5f5')
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        else:
            frame = tk.Frame(parent, bg='#fff1e3', height=180)
            frame.pack(fill=tk.X, padx=self.padding_x, pady=self.padding_y)
            frame.pack_propagate(False)

    def create_menu(self, parent):
        photo, size = self.load_photo('年度账单_商城订单_信用报告_办理进度_更多.png')

        if photo:
            img_width, img_height = size

            container = tk.Frame(parent, bg='#f5f5f5', width=img_width, height=img_height)
            container.pack(padx=self.padding_x, pady=self.padding_y)
            container.pack_propagate(False)

            bg_label = tk.Label(container, image=photo, bg='#f5f5f5')
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        else:
            frame = tk.Frame(parent, bg='white', height=80)
            frame.pack(fill=tk.X, padx=self.padding_x, pady=self.padding_y)
            frame.pack_propagate(False)

    def create_time_display(self, parent):
        frame = tk.Frame(parent, bg='#f5f5f5')
        frame.pack(fill=tk.X, padx=self.padding_x, pady=self.padding_y)

        tk.Label(
            frame,
            text="时间 " + self.current_time,
            font=('Arial', 9),
            bg='#f5f5f5',
            fg='#999999'
        ).pack(side=tk.LEFT)

        tk.Label(
            frame,
            text="🔄",
            font=('Arial', 11),
            bg='#f5f5f5',
            fg='#999999'
        ).pack(side=tk.LEFT, padx=5)

    def create_assets_card(self, parent):
        # 修改三个内容：总资产、总负债、贷款金额（不再包含时间）
        text_positions = [
            # 总资产：暂时不显示（使用渐变背景）
            # (25, 55, self.total_assets, 24, '#333333', 'gradient'),

            # 总负债：使用白色背景
            (185, 55, self.total_liabilities, 24, '#333333', 'white'),

            # 贷款金额：使用背景图片（小字体）
            (225, 88, self.loan_amount, 16, '#333333', 'loan'),
        ]

        photo, size = self.create_text_image('我的资产负债.png', text_positions)

        if photo:
            img_width, img_height = size

            container = tk.Frame(parent, bg='#f5f5f5', width=img_width, height=img_height)
            container.pack(padx=self.padding_x, pady=self.padding_y)
            container.pack_propagate(False)

            bg_label = tk.Label(container, image=photo, bg='#f5f5f5')
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        else:
            frame = tk.Frame(parent, bg='white', height=220)
            frame.pack(fill=tk.X, padx=self.padding_x, pady=self.padding_y)
            frame.pack_propagate(False)

    def create_income_card(self, parent):
        photo, size = self.load_photo('我的本月收支.png')

        if photo:
            img_width, img_height = size

            container = tk.Frame(parent, bg='#f5f5f5', width=img_width, height=img_height)
            container.pack(padx=self.padding_x, pady=self.padding_y)
            container.pack_propagate(False)

            bg_label = tk.Label(container, image=photo, bg='#f5f5f5')
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        else:
            frame = tk.Frame(parent, bg='white', height=150)
            frame.pack(fill=tk.X, padx=self.padding_x, pady=self.padding_y)
            frame.pack_propagate(False)

    def create_bottom_nav(self):
        photo, size = self.load_photo('底部按钮.png')

        frame = tk.Frame(self.root, bg='white', height=60)
        frame.pack(side=tk.BOTTOM, fill=tk.X)
        frame.pack_propagate(False)

        if photo:
            img_width, img_height = size

            container = tk.Frame(frame, bg='white', width=img_width, height=img_height)
            container.pack(expand=True)
            container.pack_propagate(False)

            bg_label = tk.Label(container, image=photo, bg='white')
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        else:
            tk.Label(frame, text="底部导航", bg='white', fg='#999').pack(expand=True)

    def update_assets_data(self, total_assets=None, total_liabilities=None, loan_amount=None, current_time=None,
                           last_login_time=None):
        """
        更新资产数据并刷新显示

        参数：
        - total_assets: 总资产（字符串格式，如 "50,000.00"）
        - total_liabilities: 总负债（字符串格式，如 "600,000.00"）
        - loan_amount: 贷款金额（字符串格式，如 "600,000.00"）
        - current_time: 当前时间（字符串格式，如 "2026-03-27 14:28:14"）
        - last_login_time: 上次登录时间（字符串格式，如 "2026-03-26 09:19:24"）
        """
        if total_assets:
            self.total_assets = total_assets
        if total_liabilities:
            self.total_liabilities = total_liabilities
        if loan_amount:
            self.loan_amount = loan_amount
        if current_time:
            self.current_time = current_time
        if last_login_time:
            self.last_login_time = last_login_time

        # 获取主框架
        main_frame = self.root.winfo_children()[0]

        # 清除主框架中的所有子组件
        for widget in main_frame.winfo_children():
            widget.destroy()

        # 重新创建所有组件
        self.create_status_bar(main_frame)
        self.create_user_card(main_frame)
        self.create_menu(main_frame)
        self.create_time_display(main_frame)
        self.create_assets_card(main_frame)
        self.create_income_card(main_frame)
        self.create_bottom_nav()


if __name__ == '__main__':
    root = tk.Tk()
    app = FinanceApp(root)

    # 示例：修改数据
    # app.update_assets_data(
    #     total_assets="100,000.00",
    #     total_liabilities="500,000.00",
    #     loan_amount="612,348.29",
    #     current_time="2026-03-28 10:30:00"
    # )

    root.mainloop()
