import sys
import traceback
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock


class TestApp(App):
    def build(self):
        try:
            layout = BoxLayout(orientation='vertical')

            # 显示平台信息
            info_text = f"Platform: {sys.platform}\n"
            info_text += f"Python: {sys.version.split()[0]}\n"
            info_text += "\n如果看到这个，说明 Kivy 正常工作！"

            label = Label(
                text=info_text,
                font_size='18sp',
                halign='center',
                valign='middle'
            )
            label.bind(size=label.setter('text_size'))

            layout.add_widget(label)

            # 延迟1秒后改变颜色，验证应用是否在运行
            Clock.schedule_once(self.change_color, 1.0)

            return layout
        except Exception as e:
            error_label = Label(
                text=f"Error: {str(e)}\n\n{traceback.format_exc()}",
                font_size='12sp',
                color=(1, 0, 0, 1)
            )
            return error_label

    def change_color(self, dt):
        """1秒后改变背景色，证明应用在运行"""
        from kivy.core.window import Window
        Window.clearcolor = (0.2, 0.6, 0.2, 1)  # 绿色


if __name__ == '__main__':
    try:
        print("Starting TestApp...")
        TestApp().run()
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
