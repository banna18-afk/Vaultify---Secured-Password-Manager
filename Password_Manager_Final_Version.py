import os
import sqlite3
from cryptography.fernet import Fernet


class Vault:
    def __init__(self, filename='Secure_Vault.db', key_file='secret.key'):

        self.filename = filename

        self.key_file = key_file
        self.key = self.load_or_generate_key()
        self.cipher = Fernet(self.key)

        self.create_table()
            
    def get_connection(self):
        return sqlite3.connect(self.filename, timeout=15)

    def create_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS passwords(
                        SNo INTEGER PRIMARY KEY AUTOINCREMENT,
                        website TEXT NOT NULL,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        user_id INTEGER NOT NULL
                        )
                 ''')
            conn.commit()

    def load_or_generate_key(self):

        if not os.path.exists(self.key_file):

            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key

        else:

            with open(self.key_file, 'rb') as f:
                return f.read()

    def add_passwords(self, user_id, website, username, password):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM passwords
            WHERE website = ? AND username = ? AND user_id = ?
            ''', (website, username, user_id))
    
            account = cursor.fetchone()
    
            if account:
                return False
    
            encrypted_pass = self.cipher.encrypt(password.encode()).decode()
            
            cursor.execute('''
                    INSERT INTO passwords(website, username, password, user_id)
                    VALUES(?, ?, ?, ?)
                    ''', (website, username, encrypted_pass, user_id))
            conn.commit()
            return True

    def search_passwords(self, user_id, website):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                    SELECT * FROM passwords
                    WHERE website = ? AND user_id = ?
                    ''', (website, user_id))
            accounts = cursor.fetchall()
            if not accounts:
                return None
            result = []
            for row in accounts:
                index = row[0]
                web = row[1]
                user = row[2]
                pwd = row[3]
                decrypted_pass = self.cipher.decrypt(pwd.encode()).decode()
                data = {'Index': index, 'Website': web, 'Username': user, 'Password': decrypted_pass}
                result.append(data)
            return result

    def view_all_passwords(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM passwords
             WHERE user_id = ?
             ORDER BY website
            ''', (user_id,))
            accounts = cursor.fetchall()
    
            if not accounts:
                return None
    
            result = []
            for row in accounts:
                index = row[0]
                web = row[1]
                user = row[2]
                pwd = row[3]
                decrypted_pass = self.cipher.decrypt(pwd.encode()).decode()
                data = {'Index': index, 'Website': web, 'Username': user, 'Password': decrypted_pass}
                result.append(data)
    
            return result

    def records(self, user_id, website, username):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM passwords
                WHERE website = ? AND username = ? AND user_id = ?
                ''', (website, username, user_id))
            account = cursor.fetchone()
            if not account:
                raise ValueError('Record Not Found!')
            return account

    def update_password(self, user_id, website, username, new_password):
        try:
            data = self.records(user_id, website, username)

            encrypted_newpass = self.cipher.encrypt(new_password.encode()).decode()
            with self.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute('''
                    UPDATE passwords
                    SET password = ?
                    WHERE website = ? AND username = ? AND user_id = ?
                    ''', (encrypted_newpass, website, username, user_id))
                conn.commit()
                return True
        except ValueError:
            return None

    def delete_password(self, user_id, website, username):
        try:
            data = self.records(user_id, website, username)
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''DELETE FROM passwords
                    WHERE website = ? AND username = ? AND user_id = ?
                ''', (website, username, user_id))
                conn.commit()
                return True
    
        except ValueError:
            return None
