from unittest import TestCase
from kyuutils.db import example as sql
from kyuutils.errors import Unknown_Table_Exception, Unknown_Columns_Exception
from mysql.connector.errors import IntegrityError
class Test_SQL(TestCase):

    def test_tbl_data(self):
        res = set(sql.tbl_data.keys())
        soll = {'user', 'message_view', 'message'}
        self.assertEqual(res, soll)
        
    def test_insert(self):
        usr_id = sql.insert("user",name="unittest",passwd="passwd")
        usr, = sql.select_eq("user", id=usr_id)
        self.assertEqual(usr["name"],"unittest")
        self.assertEqual(usr["passwd"],"passwd")
        sql.delete_eq("user",id=usr_id)
        
    def test_duplicate_insert(self):
        with self.assertRaises(IntegrityError):
            sql.insert("user",name="user1",passwd="passwd")
           
    def test_wrong_table_insert(self):
        with self.assertRaises(Unknown_Table_Exception):
            usr_id = sql.insert("user2",name="unittest",passwd="passwd")
            
    def test_wrong_table_column(self):
        with self.assertRaises(Unknown_Columns_Exception):
            usr_id = sql.insert("user",name2="unittest",passwd="passwd")
