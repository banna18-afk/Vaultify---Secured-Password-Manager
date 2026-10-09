import sqlite3
import hashlib
import hmac
import os
from Pass_Checker import pass_check

class Authorization:
    def __init__(self, filename='Secure_Vault.db'):
        self.filename = filename
        self.conn = sqlite3.connect(self.filename, check_same_thread=False)
        self.create_users_table()
            
                            
    def _generate_salt(self):
        return os.urandom(16).hex()
        
                        
    def _hash_text(self, text, salt: str) -> str:
        return hashlib.pbkdf2_hmac('sha256', text.encode(), salt.encode(), 100000).hex()
        
    def close(self):
        self.conn.close()
        
                                                        
    def create_users_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email_id TEXT UNIQUE NOT NULL,
            salt TEXT NOT NULL,
            password_hash TEXT NOT NULL)
        ''')
        self.conn.commit()
        
        
    def user_record(self, email_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM users
        WHERE email_id = ?
        ''', (email_id,))
        
        record = cursor.fetchone()
        return record
        
        
    def signup(self, username, email_id, password):
        try:
            is_valid, msg = pass_check(password)
            if is_valid:
                salt = self._generate_salt()
                password_hash = self._hash_text(password, salt)
                
                cursor = self.conn.cursor()
                cursor.execute('''
                INSERT INTO users(username, email_id, salt, password_hash)
                VALUES(?, ?, ?, ?)
                ''', (username, email_id, salt,  password_hash))
                self.conn.commit()
                
                user = self.user_record(email_id)
                
                user_id = user[0]
                return True, 'Account Created Successfully!', user_id
                
                
            else:
                return False, msg, None
        
        except sqlite3.IntegrityError:
            print('===User already exists===')
            return False, 'User Already Exists', None
        
        
    def login(self, email_id, password):
        data = self.user_record(email_id)
        if not data:
            print('User Not Found. Please SignUp First!')
            return False, 'User Not Found!', None
            
        salt = data[3]   
        password_hash = data[4]
        user_id = data[0]
        username = data[1]
        stored_pass = self._hash_text(password, salt)
        
        if hmac.compare_digest(password_hash, stored_pass):
            print(f'===Welcome Back {username.capitalize()}===')
            return True, username, user_id
            
        else:
            print('Wrong Password. Try Again!')
            return False, 'Wrong Password! Check Your Password.', None
            
            
    def get_salt(self, user_id):
        cursor = self.conn.cursor()
        
        cursor.execute('''SELECT salt FROM users WHERE user_id = ?
        ''', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None