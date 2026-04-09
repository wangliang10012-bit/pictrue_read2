import sys
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window


class TestApp(App):
    def build(self):
        # 设置窗口背景色（vivo 可能需要）
        Window.clearcolor = (1, 1, 1, 1)  # 白色背景

        layout = BoxLayout(orientation='vertical')

        label = Label(
            text='Hello Vivo!\n\nAndroid 15 Test',
            font_size='20sp',
            color=(0, 0, 0, 1),  # 黑色文字
            halign='center',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))

        layout.add_widget(label)

        return layout


if __name__ == '__main__':
    # vivo 兼容性：确保正确初始化
    try:
        print("Starting app on vivo...")
        TestApp().run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
