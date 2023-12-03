# Dependencias Kivy
from kivy.config import Config
## Configuración de dimensiones de ventana
Config.set('graphics', 'resizable', '0') 
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '500')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from kivy.lang import Builder

# Otras dependencias
import os
from peewee import SqliteDatabase, Model, TimestampField, CharField, TextField
from datetime import datetime as dt
import time as t
import textwrap as tw

# Cargar Vista de archivo KV
Builder.load_file("vista.kv")

# Base de datos (SQLite, ORM: peewee) ######################################

# Creación de Base y tabla, conexión
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

# Lógica del CRUD
class DbAdm:
    '''Métodos de interacción con base de datos'''
    def __init__(self):
        self.tb = NotesDb

    def alta(self, user:str, title:str, note:str, 
            timestamp):
        
        # Crear nuevo registro en base de datos
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
        '''Borra registro.'''
        print("borrar nota del:",time_id)
        rm=self.tb.get(self.tb.timestamp == time_id)
        rm.delete_instance()
        
    def update(self,user, time_id, title, note):
        '''Cambia registro.'''
        print("cambiar esto:",time_id)
        upd=self.tb.update(
            user = user,
            title = title,
            note = note
        ).where(self.tb.timestamp == time_id)
        upd.execute()
        
    def read_all_items(self):
        return self.tb.select()

    def read(self, timestamp:int):
        '''Lee registro.'''
        item = self.tb.get(self.tb.timestamp==timestamp)
        response = {
            "user": item.user, 
            "title":item.title, 
            "note":item.note
        }
        return response


# Clases Kivy ###############################################################

class ScreenAdm(ScreenManager):
    name_str = StringProperty()
    titl_note = StringProperty()
    text_note = StringProperty()
    
    upd_id = StringProperty()
    upd_title = StringProperty()
    upd_note = StringProperty()
    
    def __init__(self, conn:DbAdm, **kwargs):
        super().__init__(**kwargs)
        self.conn= conn

    def save_note(self):
        '''Guarda nueva nota.'''
        print("guardar:", self.name_str, self.titl_note, self.text_note)
        # debido a límite de actualización de datetime.datetime.now()
        t.sleep(1)
        if self.titl_note and self.text_note:
            self.conn.alta(
                timestamp=dt.now(),
                user=self.name_str,
                title=self.titl_note,
                note=self.text_note
            )
        else:
            print("Entrada nula")
    
    def load_old(self):
        '''Carga la nota a editar en campos'''
        
        # castear de nuevo a timestamp
        self.timestamp=  dt.strptime(self.upd_id,"%Y-%m-%d %H:%M:%S")
        
        #cargar titulo y nota campos
        to_upd= self.conn.read(self.timestamp)
        self.upd_title= to_upd["title"]
        self.upd_note= to_upd["note"]
    
    def change_note(self):
        '''Ejecutar actualización de nota.'''
        self.conn.update(
            user= self.name_str,
            time_id= self.timestamp,
            title= self.upd_title,
            note= self.upd_note
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
        self.id = id_ts


class Log(Screen): pass


class NoteList(Screen): pass


class WritNote(Screen): pass


class UpdNote(Screen): pass

class MainApp(MDApp):
    title= "App anotador"
    conn = DbAdm()
    
    def build(self):
        #Window.size = (1000,500)
        #Config.set('graphics','resizable', False) # NO FUNCIONA!
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        return ScreenAdm(self.conn)
    
    def remove_items(self):
        self.root.ids.md_list.clear_widgets() 

    def on_start(self):
        '''Cargar todas las notas.'''
        print("\nCargando lista.\n")
        
        for it in self.conn.read_all_items():
            
            # Formatear párrafo
            note_form = "\n".join(tw.wrap(it.note,90))
            
            # Creando vista de notas
            self.root.ids.md_list.add_widget(
                Note(
                    id_card= it.timestamp,
                    text=f"[size=20][b]{it.title}[/b] | Por: {it.user}, \
{it.timestamp}[/size]\n{note_form}",
                    conn=self.conn
                )
            )

if __name__ == "__main__":

    MainApp().run()