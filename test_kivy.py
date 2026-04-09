from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        label = Label(
            text='Hello Android 15!\n\n如果看到这个说明Kivy正常工作',
            font_size='20sp',
            halign='center'
        )
        layout.add_widget(label)
        return layout


if __name__ == '__main__':
    TestApp().run()
