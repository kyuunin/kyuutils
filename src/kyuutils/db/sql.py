import mysql.connector
from .sql_active import SQL_active
from .tbl import TBL
class SQL:

    def __init__(self,**settings):
        self.settings=settings
        self.connect()
        
    def __enter__(self):
        self.reconnect()
        return SQL_active(self,self.mydb.cursor())
        
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.mydb.commit()
        
    def __getitem__(self,key):
        assert key in self.tbl_data
        return TBL(self, key)
        
    def connect(self):
        self.mydb = mysql.connector.connect(**self.settings)
        self.mydb._open_connection()
        
    def reconnect(self):
         if not self.mydb.is_connected():
            self.connect()
        
    @property
    def tbl_data(self):
        if not hasattr(self, "_tbl_data"):
            self.load_tbl_data()
        return self._tbl_data
        
    def load_tbl_data(self):
        with self as active:
            active.load_tbl_data()
        
    def run(self, command, args=()):
        with self as active:
            return active.run(command,args)
        
    def insert(self, table, values=None, **kwargs):
        with self as active:
            return active.insert(table, values, **kwargs)
        
    def delete(self, table, conditions=None, **kwargs):
        with self as active:
            return active.delete(table, conditions, **kwargs)
                  
    def update_eq(self, table, values=None, conditions=None, **kwargs):
        with self as active:
            return active.update_eq(table, values, conditions, **kwargs)
            
    def insert_update(self, table, values=None, **kwargs):
        with self as active:
            return active.insert_update(table, values, **kwargs)
        
    def select(self, command, args=(), as_type=list):
        with self as active:
            return active.select(command, args, as_type)
        
    def select_all(self,  table, start=0, num=100, as_type=list):
        with self as active:
            return active.select_all(table, start, num, as_type)
              
    def select_eq(self, table, conditions=None, start=0, num=100, as_type=list, **kwargs):
        with self as active:
            return active.select_eq(table, conditions, start, num, as_type, **kwargs)
