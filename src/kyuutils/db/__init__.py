from .sql import SQL
example = SQL(host="localhost",user="kyuutils_test",passwd="test",database="kyuutils_test")

#for tbl, rows in sql.tbl_data.items():
#...     print(tbl,[k for k,v in rows.items() if v["Key"]=="PRI"])

