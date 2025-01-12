import sqlite3

class Database:
    def __init__(self, database_url):
        self.conn = sqlite3.connect(database_url)
        self.cursor = self.conn.cursor()
        self.setup_tables()

    def setup_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            phone_number TEXT UNIQUE,
            session_string TEXT,
            thumbnail_url TEXT
            )
        ''')

        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS links (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    type TEXT
                )
        ''')

        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS replace_words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    old_word TEXT,
                    new_word TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                 )
        ''')

        self.cursor.execute('''
                 CREATE TABLE IF NOT EXISTS delete_words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                     user_id INTEGER,
                    word TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                 )
        ''')
        self.conn.commit()

    # User CRUD operations
    def add_user(self, telegram_id, phone_number, session_string):
        try:
            self.cursor.execute("INSERT INTO users (telegram_id, phone_number, session_string) VALUES (?, ?, ?)", (telegram_id, phone_number, session_string))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user_by_telegram_id(self, telegram_id):
        self.cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        return self.cursor.fetchone()

    def get_user_by_phone(self, phone_number):
        self.cursor.execute("SELECT * FROM users WHERE phone_number = ?", (phone_number,))
        return self.cursor.fetchone()

    def set_user_session_string(self, telegram_id, session_string):
        self.cursor.execute("UPDATE users SET session_string = ? WHERE telegram_id = ?", (session_string, telegram_id))
        self.conn.commit()

    def set_user_thumbnail(self, telegram_id, thumbnail_url):
              self.cursor.execute("UPDATE users SET thumbnail_url = ? WHERE telegram_id = ?", (thumbnail_url, telegram_id))
        self.conn.commit()

    def delete_user_by_telegram_id(self, telegram_id):
        self.cursor.execute("DELETE FROM users WHERE telegram_id = ?", (telegram_id,))
        self.conn.commit()

    # Link CRUD operations
    def add_link(self, url, link_type):
        try:
            self.cursor.execute("INSERT INTO links (url, type) VALUES (?, ?)", (url, link_type))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def replace_link(self, old_url, new_url):
        self.cursor.execute("UPDATE links SET url = ? WHERE url = ?", (new_url, old_url))
        self.conn.commit()

    def get_all_links(self):
        self.cursor.execute("SELECT * FROM links")
        return self.cursor.fetchall()

    def delete_link(self, url):
        self.cursor.execute("DELETE FROM links WHERE url = ?", (url,))
        self.conn.commit()

    def get_first_links(self, count):
        self.cursor.execute("SELECT * FROM links ORDER BY id ASC LIMIT ?", (count,))
        return self.cursor.fetchall()

    def get_last_links(self, count):
        self.cursor.execute("SELECT * FROM links ORDER BY id DESC LIMIT ?", (count,))
        return self.cursor.fetchall()

    # Replace word CRUD operations
    def add_replace_word(self, user_id, old_word, new_word):
        self.cursor.execute("INSERT INTO replace_words (user_id, old_word, new_word) VALUES (?, ?, ?)", (user_id, old_word, new_word))
        self.conn.commit()

    def get_replace_words_by_user(self, user_id):
        self.cursor.execute("SELECT old_word, new_word FROM replace_words WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    # Delete word CRUD operation
    def add_delete_word(self, user_id, word):
        self.cursor.execute("INSERT INTO delete_words (user_id, word) VALUES (?, ?)", (user_id, word))
        self.conn.commit()

    def get_delete_words_by_user(self, user_id):
        self.cursor.execute("SELECT word FROM delete_words WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()
