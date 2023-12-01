from kivy.config import Config
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivy.core.window import Window
# from kivymd.uix.stacklayout import MDStackLayout
# from kivymd.uix.card import MDCardSwipe

import os
from peewee import  SqliteDatabase, Model, CompositeKey, TimestampField, CharField, TextField
from datetime import datetime as dt
import time
import textwrap as tw

# Cargar Vista
Builder.load_file("vista.kv")

# Base de datos (SQLite, ORM: peewee) ######################################
RUTA_DIR = os.getcwd()
DB_P = "user_notes.db"
db = SqliteDatabase(DB_P)

class NotesDb(Model):
    timestamp = TimestampField(primary_key=True)
    user = CharField()
    title = CharField()
    note = TextField()
    class Meta():
        database= db
        db_table='notes'

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
        
        time.sleep(1)
        # ALTA en SQLite
        try:
            self.tb.create(
                timestamp = dt.now(),
                user = user,
                title = title,
                note = note
            )
            print(f"Guardada nota")
        except:
            raise Exception("ERROR al guardar nota")
        
    def delet(self):
        self.tb.delete().where()

    def updat(self):
        print(NotImplemented)
    
    def read_all_items(self):
        return self.tb.select()

    def read_all(self):
        for fila in self.tb.select():
            print(fila.timestamp,fila.user,fila.title)
            print(int(round(fila.timestamp.timestamp())))

    def read(self, timestamp:int):
        r = self.tb.get(self.tb.timestamp==timestamp)
        print(r)

# Clases Kivy ###############################################################
user = ""
class ScreenAdm(ScreenManager):
    name_str = StringProperty()
    def ver_nomb(self):
        global user
        print("nombre:")
        print(self.name_str)
        user = (self.name_str)


class Note(MDCard):
    text = StringProperty()

class Log(Screen):
    pass

class NoteList(Screen):
    pass

class MainApp(MDApp):
    conn = DbAdm()
    
    def build(self):
        Window.size = (950,500)
        Config.set('graphics','resizable', False) # NO FUNCIONA!
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        return ScreenAdm()
    
    def remove_item(self, instance):
        self.root.ids.md_list.remove_widget(instance)
    
    def pr(self):
        self.conn.alta(user, "tit","not")

    def on_start(self):
        '''Cargar todas las notas.'''

        for it in self.conn.read_all_items():
            note_form = "\n".join(tw.wrap(it.note))
            self.root.ids.md_list.add_widget(
                Note(text=f"{it.title} | Por: {it.user}, \
{it.timestamp}\n {note_form}")
            )


if __name__ == "__main__":

    MainApp().run()