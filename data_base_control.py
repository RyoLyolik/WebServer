import sqlite3

class DB:
    def __init__(self):
        conn = sqlite3.connect('databases/users', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()

class Users:
    def __init__(self, conn):
        self.conn = conn

    def init_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128),
                             lvls
                             )''')
        cursor.close()
        self.conn.commit()

    def insert(self, user_name, password_hash):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO users (name, password_hash, lvls) VALUES (?, ?, 0)''', (user_name, password_hash))
        cursor.close()
        self.conn.commit()

    def get(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, user_name, password_hash):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

class Levels:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS lvls 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER UNIQUE,
                             title VARCHAR(100),
                             num INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def get(self, lvl_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM lvls WHERE id = ?", (str(lvl_id)))
        row = cursor.fetchone()
        return row

    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM lvls WHERE user_id = ?",
                           (str(user_id)))
        else:
            cursor.execute("SELECT * FROM lvls")
        rows = cursor.fetchall()
        return rows

    def delete(self, lvl_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM lvls WHERE id = ?''', (str(lvl_id)))
        cursor.close()
        self.connection.commit()