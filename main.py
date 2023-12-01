from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from kivy.lang import Builder

import os
from peewee import  SqliteDatabase, Model, CompositeKey, TimestampField, CharField, TextField
from datetime import datetime as dt

# Cargar Vista
Builder.load_file("vista.kv")

# Base de datos (SQLite, ORM: peewee) ######################################
RUTA_DIR = os.getcwd()
DB_P = "user_notes.db"
db = SqliteDatabase(DB_P)

class NotesDb(Model):
    timestamp = TimestampField(null= False)
    user = CharField(null = False)
    title = CharField(null = False)
    note = TextField(null = True)
    class Meta():
        database= db
        db_table='notes'
        primary_key= CompositeKey("timestamp", "title")

try:
    db.connect()
    db.create_tables([NotesDb])
    print(f"\n**\nConexión con:\n {os.path.join(RUTA_DIR,DB_P)}\n**\n")
except:
    raise Exception("\nError de conexión con base SQLite\n")

class DbAdm:
    
    def __init__(self):
        self.tb = NotesDb

    def alta(self, user:str, title:str, note:str):

        # ALTA en SQLite
        try:
            self.tb.create(
                timestamp = dt.now(),
                user = user,
                title = title,
                note = note
            )
            print("Guardada nota")
        except:
            raise Exception("ERROR al guardar nota")
        
    def delet(self):
        self.tb.delete().where()

    def updat(self):
        print(NotImplemented)
    
    def read(self):
        print(NotImplemented)


# Clases Kivy ###############################################################
class ScreenAdm(ScreenManager):
    pass

class Note(MDCard):
    text = StringProperty()

class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        return ScreenAdm()
    def on_start(self):
        styles = {
            "elevated": "#f6eeee", "filled": "#f4dedc", "outlined": "#f8f5f4"
        }
        for style in styles.keys():
            self.root.ids.box.add_widget(
                Note(
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    style=style,
                    text=style.capitalize(),
                    md_bg_color=styles[style],
                    shadow_softness=2 if style == "elevated" else 12,
                    shadow_offset=(0, 1) if style == "elevated" else (0, 2),
                )
            )
if __name__ == "__main__":

    MainApp().run()