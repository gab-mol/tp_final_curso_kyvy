from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder

Builder.load_file("vista.kv")


class PruebaPantalla(MDBoxLayout):pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        return PruebaPantalla()

if __name__ == "__main__":
    MainApp().run()