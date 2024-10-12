import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        conn = sqlite3.connect(self.path_to_db)
        conn.row_factory = sqlite3.Row  # Lug'at qaytarish uchun
        return conn

    def execute(self, sql: str, parameters: tuple = (), fetchone=False, fetchall=False, commit=False):
        data = None
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute(sql, parameters)
            if commit:
                connection.commit()
            if fetchall:
                data = cursor.fetchall()
            if fetchone:
                data = cursor.fetchone()
        return data

    # Create table for users
    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname VARCHAR(255),
            telegram_id VARCHAR(20) UNIQUE
        );
        """
        self.execute(sql, commit=True)

    # Create table for voice data
    def create_voices_data(self):
        sql = """
        CREATE TABLE IF NOT EXISTS voices_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voice_name VARCHAR(255),
            voice_id VARCHAR(255)
        );
        """
        self.execute(sql, commit=True)

    # Create table for kanal
    def create_table_kanal(self):
        sql = """
        CREATE TABLE IF NOT EXISTS kanal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id VARCHAR(64) NOT NULL,
            url TEXT NOT NULL
        );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])
        return sql, tuple(parameters.values())

    # Add user to the database
    def add_user(self, fullname: str, telegram_id: str = None):
        sql = """
        INSERT INTO users(fullname, telegram_id) VALUES(?, ?)
        """
        self.execute(sql, parameters=(fullname, telegram_id), commit=True)

    def get_user(self, user_id):
        sql = "SELECT * FROM users WHERE telegram_id = ?"
        parameters = (user_id,)
        return self.execute(sql, parameters=parameters, fetchone=True)

    # Add voice data to the database
    def add_voice(self, voice_name: str, voice_id: str):
        sql = """
        INSERT INTO voices_data(voice_name, voice_id) VALUES(?, ?)
        """
        self.execute(sql, parameters=(voice_name, voice_id), commit=True)

    # Delete voice data by voice name
    def delete_voice_name(self, voice_name: str):
        sql = """
        DELETE FROM voices_data
        WHERE voice_name = ?
        """
        self.execute(sql, parameters=(voice_name,), commit=True)

    # Count total users
    def count_users(self):
        result = self.execute("SELECT COUNT(*) FROM users;", fetchone=True)
        return result[0] if result else 0

    # Check if a specific voice name exists
    def check_code_exists(self, voice_name: str):
        sql = """
        SELECT 1 FROM voices_data WHERE voice_name = ? LIMIT 1
        """
        result = self.execute(sql, parameters=(voice_name,), fetchone=True)
        return result is not None

    # Select all users
    def select_all_users(self):
        sql = "SELECT * FROM users"
        return self.execute(sql, fetchall=True)

    # Search for voices by name
    def search_voices(self, search_text: str = None):
        if search_text:
            sql = """
            SELECT id, voice_name, voice_id FROM voices_data 
            WHERE voice_name LIKE ?
            """
            parameters = (f"%{search_text}%",)
        else:
            sql = "SELECT id, voice_name, voice_id FROM voices_data"
            parameters = ()
        return self.execute(sql, parameters=parameters, fetchall=True)

    # Add kanal to the database
    def add_kanal(self, chat_id: str, url: str):
        sql = """
        INSERT INTO kanal(chat_id, url) VALUES (?, ?)
        """
        self.execute(sql, parameters=(chat_id, url), commit=True)

    # Delete a kanal by chat_id
    def delete_kanal(self, chat_id):
        sql = "DELETE FROM kanal WHERE chat_id = ?"
        self.execute(sql, parameters=(chat_id,), commit=True)

    # Get all kanal URLs
    def get_all_url(self):
        sql = "SELECT url FROM kanal"
        channels = self.execute(sql, fetchall=True)
        return [channel['url'] for channel in channels]

    def get_all_channels(self):
        sql = "SELECT chat_id, url FROM kanal"
        return self.execute(sql, fetchall=True)
