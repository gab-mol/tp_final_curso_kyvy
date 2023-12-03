from kivy.config import Config
# from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.utils import asynckivy
from kivymd.uix.refreshlayout import refreshlayout

import os
from peewee import SqliteDatabase, Model, TimestampField, CharField, TextField
from datetime import datetime as dt
import time as t
import textwrap as tw
import pandas as pd

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

    def alta(self, user:str, title:str, note:str, 
            timestamp=dt.now()):
        t.sleep(1)
        try:
            self.tb.create(
                timestamp = timestamp,
                user = user,
                title = title,
                note = note
            )
            print(f"Guardada nota")
        except:
            raise Exception("ERROR al guardar nota")
        
    def delete(self,time_id):
        print("borrar nota del:",time_id)
        rm=self.tb.get(self.tb.timestamp == time_id)
        rm.delete_instance()
        
    def update(self,user, time_id, title, note):
        print("cambiar esto:",time_id)
        upd=self.tb.update(
            user = user,
            title = title,
            note = note
        ).where(self.tb.timestamp == time_id)
        upd.execute()
            
    def read_all_items(self):
        return self.tb.select()

    def read_all(self):
        for fila in self.tb.select():
            print(fila.timestamp,fila.user,fila.title)
            print(int(round(fila.timestamp.timestamp())))

    def read(self, timestamp:int):
        item = self.tb.get(self.tb.timestamp==timestamp)
        response = {
            "user": item.user, 
            "title":item.title, 
            "note":item.note
        }
        return response


# Clases Kivy ###############################################################

class ScreenAdm(ScreenManager):
    id_pointer = StringProperty()
    name_str = StringProperty()
    titl_note = StringProperty()
    text_note = StringProperty()
    
    upd_id = StringProperty()
    def __init__(self, conn:DbAdm, **kwargs):
        super().__init__(**kwargs)
        self.conn= conn

    def save_note(self):
        print("guardar:", self.name_str, self.titl_note, self.text_note)
        
        self.conn.alta(
            timestamp= self.id_pointer,
            user=self.name_str,
            title=self.titl_note,
            note=self.text_note
        )
        
    def change_note(self, title,note):
        timestamp=  dt.strptime(self.id_pointer,"%Y-%m-%d %H:%M:%S")
        print("RESULT",timestamp, type(timestamp))
        self.conn.update(
            user= self.name_str,
            time_id= timestamp,
            title= title,
            note= note
        )


class Note(MDCard):
    text = StringProperty()
    id = StringProperty()
    
    def __init__(self, conn:DbAdm, id_card, **kwargs):
        super().__init__(**kwargs)
        self.id_card = id_card
        self.conn = conn
    
    def _del(self):
        self.conn.delete(self.id_card)

    def _upd(self):
        id_ts = str(self.id_card)
        print("ESTO",self.id_card)
        self.id = id_ts


class Log(Screen): pass


class NoteList(Screen): pass


class WritNote(Screen): pass


class UpdNote(Screen):
    upd_title = StringProperty()
    upd_note = StringProperty()
    def __init__(self, **kw):
        super().__init__(**kw)


class MainApp(MDApp):
    title= "App anotador"
    conn = DbAdm()
    
    def build(self):
        Window.size = (950,500)
        Config.set('graphics','resizable', False) # NO FUNCIONA!
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        return ScreenAdm(self.conn)
    
    def remove_items(self):
        self.root.ids.md_list.clear_widgets() 

    def on_start(self):
        '''Cargar todas las notas.'''
        print("\n\nlanzando on_start !!!!!\n\n")
        for it in self.conn.read_all_items():
            note_form = "\n".join(tw.wrap(it.note))
            self.root.ids.md_list.add_widget(
                Note(
                    id_card= it.timestamp,
                    text=f"[b]{it.title}[/b] | Por: {it.user}, \
{it.timestamp}\n {note_form}", 
                    conn=self.conn
                )
            )


if __name__ == "__main__":

    MainApp().run()