import mysql.connector

class SQL:
    def __init__(self,**settings):
        self.settings=settings
        self.connect()
        
    def __enter__(self):
        self.reconnect()
        return self.mydb.cursor()
        
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.mydb.commit()
        
    def connect(self):
        self.mydb = mysql.connector.connect(**self.settings)
        self.mydb._open_connection()
        self.load_tbl_data()
        
    def reconnect(self):
         if not self.mydb.is_connected():
            self.connect()
        
    def load_tbl_data(self):
        with self as cursor:
            cursor.execute("SHOW TABLES;")
            self.tbl_data = {
                table: self.select(
                    cursor, 
                    f"SHOW COLUMNS FROM `{table}`;",
                    as_type=dict
                ) for table, in cursor.fetchall()}
            
    def run(self, cursor, command, args=()):
        print(command)
        cursor.execute(command,args)
        return cursor.lastrowid
        
    def insert(self, cursor, table, values=None, **kwargs):
        if values is None:
            values = kwargs
        assert table in self.tbl_data
        assert all(c in self.tbl_data[table] for c in values.keys())
        
        return self.run(
            cursor,
            f"INSERT `{table}` ({', '.join(map(_quote,values.keys()))}) VALUES ({', '.join(map(_escape,values.keys()))});",
            tuple(values.values())
        )
        
    def delete(self, cursor, table, conditions=None, **kwargs):
        if conditions is None:
            conditions = kwargs
        assert table in self.tbl_data
        assert all(c in self.tbl_data[table] for c in conditions.keys())
        
        return self.run(
            cursor,
            f"DELETE FROM `{table}` WHERE {_and_eqs(conditions)};",
            tuple(conditions.values())
        )
                  
    def update_eq(self, cursor, table, values=None, conditions=None, **kwargs):
        if conditions is None:
            assert values is not None
            conditions = kwargs
        elif values is None:
            values = kwargs
        assert table in self.tbl_data
        assert all(c in self.tbl_data[table] for c in values.keys())
        assert all(c in self.tbl_data[table] for c in conditions.keys())
        
        return self.run(
            cursor,
            f"UPDATE `{table}` SET {_listing(values)} WHERE {_and_eqs(conditions)} ",
            tuple(values.values()) + tuple(conditions.values()) 
        )
        
    def insert_update(self, cursor, table, values=None, **kwargs):
        if values is None:
            values = kwargs
        assert table in self.tbl_data
        assert all(c in self.tbl_data[table] for c in values.keys())
        return self.run(
            cursor,
            f"INSERT `{table}` ({', '.join(map(_quote,values.keys()))}) VALUES ({', '.join(map(_escape,values.keys()))})" + 
            f" ON DUPLICATE KEY UPDATE {_listing(values)};",
            tuple(values.values())*2
        )
        
    def select(self, cursor, command, args=(), as_type=list):
        cursor.execute(command,args)
        if as_type is dict:
            return {row[0]:_to_dict(cursor,row) for row in cursor.fetchall()}
        return as_type(_to_dict(cursor,row) for row in cursor.fetchall())
        
    def select_all(self, cursor, table, start=0, num=100, as_type=list):
        #TODO custom assert
        assert table in self.tbl_data
        assert type(start) is int
        assert type(num) is int
         
        return self.select(
            cursor,
            f"SELECT * FROM `{table}` limit {start},{num};",
            as_type = as_type
        )
              
    def select_eq(self, cursor, table, conditions=None, start=0, num=100, as_type=list, **kwargs):
        if conditions is None:
            conditions = kwargs
        #TODO custom assert
        assert table in self.tbl_data
        assert type(start) is int
        assert type(num) is int
        assert all(c in self.tbl_data[table] for c in conditions.keys())
        
        return self.select(
            cursor,
            f"SELECT * FROM `{table}` WHERE {_and_eqs(conditions)} limit {start},{num};",
            tuple(conditions.values()),
            as_type = as_type
        )
    
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
 
def _to_dict(cursor, item):
    return dict(zip(cursor.column_names,item))
    

