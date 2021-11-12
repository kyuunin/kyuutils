from .sql_active import SQL_active
from .row import ROW
class TBL_active:
    def __init__(self, sql, name):
        self.sql = sql
        self.name = name
        
    def __getitem__(self, key):
        if len(self.primary) == 1:
            return seöf.get({self.primary[0]:key})
        assert len(self.primary) == len(key)
        return self.get(dict(zip(self.primary, key)))
       
    def get(self, key = None, **kwargs):
        if key is None:
            key = kwargs
        assert all(c in self.tbl_data for c in key.keys())
        
        return ROW(self,key)
            
    @property
    def primary(self):
        if not hasattr(self, "_primary"):
            self._primary = tuple(k for k,v in self.tbl_data.items() if v["Key"]=="PRI")
        return self._primary
        
    @property
    def tbl_data(self):
        if not hasattr(self.sql, "tbl_data"):
            self.sql.load_tbl_data()
        return self.sql.tbl_data[self.name]
        
    def load_tbl_data(self):
        self.sql.load_tbl_data()
        
    def run(self, command, args=()):
        return self.sql.run(command,args)
        
    def insert(self, values=None, **kwargs):
        return self.sql.insert(self.name, values, **kwargs)
        
    def delete(self, conditions=None, **kwargs):
        return self.sql.delete(self.name, conditions, **kwargs)
                  
    def update_eq(self, values=None, conditions=None, **kwargs):
        return self.sql.update_eq(self.name, values, conditions, **kwargs)
            
    def insert_update(self, values=None, **kwargs):
        return self.sql.insert_update(self.name, values, **kwargs)
        
    def select(self, command, args=(), as_type=list):
        return self.sql.select(command, args, as_type)
        
    def select_all(self, start=0, num=100, as_type=list):
        return self.sql.select_all(self.name, start, num, as_type)
              
    def select_eq(self, conditions=None, start=0, num=100, as_type=list, **kwargs):
        return self.sql.select_eq(self.name, conditions, start, num, as_type, **kwargs)
        
class TBL(TBL_active):
    def __enter__(self):
        active = self.sql.__enter__()
        return TBL_active(active, self.name)
        
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.sql.__exit__(exc_type, exc_value, exc_traceback)
