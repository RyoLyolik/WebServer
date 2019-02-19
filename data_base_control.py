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
                             lvls,
                             email MESSAGE_TEXT UNIQUE NOT NULL
                             )''')
        cursor.close()
        self.conn.commit()

    def insert(self, user_name, password_hash, email):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO users (user_name, password_hash, lvls, email) VALUES (?, ?, 0,?)''', (user_name, password_hash, email))
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

    def exists(self, email, password_hash):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password_hash = ?",
                       (email, password_hash))
        row = cursor.fetchall()
        return (True, row[0]) if row else (False,)

class Levels:
    def __init__(self, connection):
        self.connection = connection

    def table_init(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE if NOT EXISTS levels
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_id int NOT NULL,
            likes int DEFAULT 0 NOT NULL,
            dislikes int DEFAULT 0 NOT NULL,
            rate int DEFAULT 0 NOT NULL
        );''')
        cursor.close()
        self.connection.commit()

    def insert(self, us_id):
        cursor = self.connection.cursor()
        print(us_id)
        cursor.execute('''INSERT INTO levels (author_id, storage) VALUES (?,?)''',(us_id,'0'))
        self.connection.commit()
        rows = self.get_all(user_id=us_id)
        rows.sort(key=lambda x:x[0])
        rows.reverse()
        lvl_id = rows[0][0]
        storage = '/levels/lvl_'+str(rows[0][0])+'.txt'
        # print(storage)
        cursor.execute('''UPDATE levels
                            SET storage = ?
                            WHERE lvl_id = ?''', (str(storage),str(lvl_id)))
        cursor.close()
        self.connection.commit()
        return lvl_id

    def get(self, lvl_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM levels WHERE lvl_id = ?", (str(lvl_id)))
        row = cursor.fetchone()
        return row

    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM levels WHERE author_id = ?",
                           (str(user_id)))
        else:
            cursor.execute("SELECT * FROM levels")
        rows = cursor.fetchall()
        return rows

    def delete(self, lvl_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM levels WHERE lvl_id = ?''', (str(lvl_id)))
        cursor.close()
        self.connection.commit()