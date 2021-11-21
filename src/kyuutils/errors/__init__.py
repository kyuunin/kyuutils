def throw(exception):
    raise exception
    
class Unknown_Table_Exception(Exception):
    def __init__(self, table):
        self.table = table
        super().__init__(f"Table {table} not found.")
        
class Unknown_Columns_Exception(Exception):
    def __init__(self, comuns):
        self.comuns = comuns
        super().__init__(f"Comuns {', '.join(comuns)} not found.")
