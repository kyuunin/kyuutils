class ROW:
    def __init__(self, tbl, key=None, **kwargs):
        if key is None:
            key = kwargs
        self._key = key
        self._tbl = tbl
        self.clear()
        
    def load(self):
        if self._buff:
            self.flush()
        self._data = self._tbl.select_eq(self._key)[0]
        
    def clear(self):
        self._buff = {}
        
    def flush(self):
        self._tbl.update_eq(self._buff, self._key)
        self._data.update(self._buff)
        self.clear()    
        
    def __enter__(self):
        self.load()
        return self
        
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.flush()
        
    def __getitem__(self, key):
        if key in self._buff:
            return self._buff[key]
        if not hasattr(self, "_data"):
            self.load()
        return self._data[key]
        
    def __getattr__(self, key):
        if key[0] == "_":
            return super().__getattr__(key)
        else:
            return self[key]
    
    def __setitem__(self, key, val):
        self._buff[key] = val
        
    def __setattr__(self, key, val):
        if key[0] == "_":
            super().__setattr__(key,val)
        else:
            self[key] = val
