from kivy.config import Config
from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem

import os
from peewee import  SqliteDatabase, Model, CompositeKey, TimestampField, CharField, TextField
from datetime import datetime as dt
import time
import textwrap as tw

# Cargar Vista
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
        
    def delete(self,time_id):
        #self.tb.delete().where()
        print("borrar esto:",time_id)

    def update(self,time_id):
        print("cambiar esto:",time_id)
    
    def read_all_items(self):
        return self.tb.select()

    def read_all(self):
        for fila in self.tb.select():
            print(fila.timestamp,fila.user,fila.title)
            print(int(round(fila.timestamp.timestamp())))

    def read(self, timestamp:int):
        r = self.tb.get(self.tb.timestamp==timestamp)
        print(r)


conn = DbAdm()

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
    id_card = StringProperty()
    def __init__(self, conn:DbAdm, id_card, **kwargs): # esto tiene que ir en cada instancia de card
        super().__init__(**kwargs) # tengoq que descubrir como meter en menu_items 
        #print("dentro de class Note:", id_card, type(id_card),"\n",conn)
        menu_items = [
            {
                "text": f"{i[0]}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x: i[1](id_card)
            } for i in [["Borrar", conn.delete], ["Modificar", conn.update]] # meter acá todas las claves de las funciones CRUD
        ]
        #print("\n #### IDs:",self.ids,",\n")
        self.menu = MDDropdownMenu(
            caller=self.ids.dot_button,
            items=menu_items,
            width_mult=4,
        )


class Log(Screen):
    pass


class NoteList(Screen):
    pass
#     def __init__(self, **kw):
#         super().__init__(**kw)
#         global conn
#         for it in conn.read_all_items():
#             note_form = "\n".join(tw.wrap(it.note))
#             self.app.ids.md_list.add_widget(
#                 Note(
#                     id_card= it.timestamp,
#                     text=f"{it.title} | Por: {it.user}, \
# {it.timestamp}\n {note_form}", 
#                     conn=conn
#                 )
#             )


class MainApp(MDApp):
    
    def build(self):
        Window.size = (950,500)
        Config.set('graphics','resizable', False) # NO FUNCIONA!
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        return ScreenAdm()
    
    def remove_item(self, instance):
        self.root.ids.md_list.remove_widget(instance)

    def on_start(self):
        '''Cargar todas las notas.'''
        
        global conn
        for it in conn.read_all_items():
            note_form = "\n".join(tw.wrap(it.note))
            self.root.ids.md_list.add_widget(
                Note(
                    id_card= it.timestamp,
                    text=f"{it.title} | Por: {it.user}, \
{it.timestamp}\n {note_form}", 
                    conn=conn
                )
            )


if __name__ == "__main__":

    MainApp().run()