import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    # Create table
    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname VARCHAR(255),
            telegram_id VARCHAR(20) UNIQUE
        );
        """
        self.execute(sql, commit=True)

    def create_voices_data(self):
        sql = """
        CREATE TABLE IF NOT EXISTS voices_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voice_name VARCHAR(255),
            voice_id VARCHAR(255)
        );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, fullname: str, telegram_id: str = None):
        sql = """
        INSERT INTO users(fullname, telegram_id) VALUES(?, ?)
        """
        self.execute(sql, parameters=(fullname, telegram_id), commit=True)

    def add_voice(self, voice_name: str, voice_id: str):
        sql = """
        INSERT INTO voices_data(voice_name, voice_id) VALUES(?, ?)
        """
        self.execute(sql, parameters=(voice_name, voice_id), commit=True)

    def delete_voice_name(self, voice_name: str):
        sql = """
        DELETE FROM voices_data
        WHERE voice_name = ?
        """
        self.execute(sql, parameters=(voice_name,), commit=True)

    def count_users(self):
        result = self.execute("SELECT COUNT(*) FROM users;", fetchone=True)
        return result[0] if result else 0

    def check_code_exists(self, voice_name: str):
        sql = """
        SELECT 1 FROM voices_data WHERE voice_name = ? LIMIT 1
        """
        result = self.execute(sql, parameters=(voice_name,), fetchone=True)
        return result is not None

    def select_all_users(self):
        sql = "SELECT * FROM users"
        return self.execute(sql, fetchall=True)

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


