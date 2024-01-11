import sqlite3

class Sqlite:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')

    async def select(self, cmd, one=False):
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        if not one:
            data_list = cursor.fetchall()
        else:
            data_list = cursor.fetchone()
        return data_list

    async def insert_delete(self, cmd):
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        self.conn.commit()
