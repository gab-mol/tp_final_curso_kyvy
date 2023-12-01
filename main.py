from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.card import MDCardSwipe

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
class ScreenAdm(ScreenManager):
    pass

class SwipeToDeleteItem(MDCardSwipe):
    '''Card with `swipe-to-delete` behavior.'''

    text = StringProperty()

class Note(MDCard):
    text = StringProperty()


class MainApp(MDApp):
    conn = DbAdm()
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        return ScreenAdm()
    
    def remove_item(self, instance):
        self.root.ids.md_list.remove_widget(instance)
    
    def on_start(self):
        '''Cargar todas las notas.'''

        for it in self.conn.read_all_items():
            note_form = "\n".join(tw.wrap(it.note))
            self.root.ids.md_list.add_widget(
                Note(text=f"{it.title} | Por: {it.user}, \
{it.timestamp}\n {note_form}")
            )

    # def on_start(self):

    #     for i in range(10):
    #         self.root.ids.box.add_widget(
    #             Note(
    #                 line_color=(0.2, 0.2, 0.2, 0.8),
    #                 style="elevated",
    #                 text=str(i),
    #                 md_bg_color="#f6eeee",
    #                 shadow_softness=2,
    #                 shadow_offset=(0, 1),
    #             )
    #         )


if __name__ == "__main__":

    MainApp().run()