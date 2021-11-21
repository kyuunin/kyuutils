class SQL_active:

    def __init__(self, sql, cursor):
        self.sql = sql
        self.cursor = cursor
        
    @property
    def tbl_data(self):
        if not hasattr(self.sql, "_tbl_data"):
            self.load_tbl_data()
        return self.sql._tbl_data
        
    def load_tbl_data(self):
        self.cursor.execute("SHOW TABLES;")
        self.sql._tbl_data = {
            table: self.select(
                f"SHOW COLUMNS FROM `{table}`;",
                as_type=dict
            ) for table, in self.cursor.fetchall()}
        
    def run(self, command, args=()):
        self.cursor.execute(command,args)
        return self.cursor.lastrowid
        
    def insert(self, table, values=None, **kwargs):
        if values is None:
            values = kwargs
        assert table in self.tbl_data
        assert all(c in self.tbl_data[table] for c in values.keys())
        
        return self.run(
            f"INSERT `{table}` ({', '.join(map(_quote,values.keys()))}) VALUES ({', '.join(map(_escape,values.keys()))});",
            tuple(values.values())
        )
        
    def delete(self, table, conditions=None, **kwargs):
        if conditions is None:
            conditions = kwargs
        assert table in self.tbl_data
        assert all(c in self.tbl_data[table] for c in conditions.keys())
        
        return self.run(
            f"DELETE FROM `{table}` WHERE {_and_eqs(conditions)};",
            tuple(conditions.values())
        )
                  
    def update_eq(self, table, values=None, conditions=None, **kwargs):
        if conditions is None:
            assert values is not None
            conditions = kwargs
        elif values is None:
            values = kwargs
        assert table in self.tbl_data
        assert all(c in self.tbl_data[table] for c in values.keys())
        assert all(c in self.tbl_data[table] for c in conditions.keys())
        
        return self.run(
            f"UPDATE `{table}` SET {_listing(values)} WHERE {_and_eqs(conditions)} ",
            tuple(values.values()) + tuple(conditions.values()) 
        )
        
    def insert_update(self, table, values=None, **kwargs):
        if values is None:
            values = kwargs
        assert table in self.tbl_data
        assert all(c in self.tbl_data[table] for c in values.keys())
        return self.run(
            f"INSERT `{table}` ({', '.join(map(_quote,values.keys()))}) VALUES ({', '.join(map(_escape,values.keys()))})" + 
            f" ON DUPLICATE KEY UPDATE {_listing(values)};",
            tuple(values.values())*2
        )
        
    def select(self, command, args=(), as_type=list):
        self.cursor.execute(command,args)
        if as_type is dict:
            return {row[0]:self._to_dict(row) for row in self.cursor.fetchall()}
        return as_type(self._to_dict(row) for row in self.cursor.fetchall())
        
    def select_all(self,  table, start=0, num=100, as_type=list):
        #TODO custom assert
        assert table in self.tbl_data
        assert type(start) is int
        assert type(num) is int
         
        return self.select(
            f"SELECT * FROM `{table}` limit {start},{num};",
            as_type = as_type
        )
              
    def select_eq(self, table, conditions=None, start=0, num=100, as_type=list, **kwargs):
        if conditions is None:
            conditions = kwargs
        #TODO custom assert
        assert table in self.tbl_data
        assert type(start) is int
        assert type(num) is int
        assert all(c in self.tbl_data[table] for c in conditions.keys())
        
        return self.select(
            f"SELECT * FROM `{table}` WHERE {_and_eqs(conditions)} limit {start},{num};",
            tuple(conditions.values()),
            as_type = as_type
        )
    
    def _to_dict(self, item):
        return dict(zip(self.cursor.column_names,item))
    
##########
# Helper #
##########    
           
def _quote(value):
    return f'`{value}`'
    
def _escape(value):
    return '%s'

def _and_eqs(conditions):
    return 'AND'.join(f' `{c}` = %s ' for c in conditions)
    
def _listing(conditions):
    return ','.join(f' `{c}` = %s ' for c in conditions)
 
    

