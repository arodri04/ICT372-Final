import sqlite3
import hashlib
import string
import re
from datetime import date
import random
import requests

def connectDB():
    try:
        conn = sqlite3.connect('./instance/db.sqlite')
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database {e}")
        return None
    
def validateLogin(username, password):
    try:
        conn = connectDB()

        if not conn:
            return False
        
        cursor = conn.cursor()

        query = "SELECT salt, password FROM users WHERE username = ?"
        cursor.execute(query,(username,))
        result = cursor.fetchone()

        if result:
            salt, passHash = result
            combinePass = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
            if combinePass == passHash:
                return True          
        return False
    except sqlite3.Error as e:
        print(f"Database Error {e}")
        return False
    finally:
        if conn:
            conn.close()

def validateEmail(username):
    pattern ='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    try:
        conn = connectDB()
        if not conn:
            return False 
        #Make sure that there isnt more emails
        cursor = conn.cursor()
        query = "SELECT 1 FROM users WHERE username = ?"
        cursor.execute(query,(username,))
        result = cursor.fetchone()
        #Make sure it is an email
        if not result:
            if re.fullmatch(pattern, username):
                return True
        return False
    except sqlite3.Error as e:
        print(f"Database Error {e}")
        return False
    finally:
        if conn:
            conn.close()
    


def getUserId(username):
    try:
        conn = connectDB()
        if not conn:
            return False
        
        cursor = conn.cursor()
        query = "SELECT userId FROM users WHERE username = ?"
        cursor.execute(query,(username,))
        result = cursor.fetchone()
        if result:
            return result
            
        return False 
    except sqlite3.Error as e:
        print(f"Database Error {e}")
        return False  
    finally:
        if conn:
            conn.close()


def getNews():
    url = "https://api.spaceflightnewsapi.net/v4/articles"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        articles = data.get('results', [])
        
        return articles
    else:
        print(f"Error: {response.status_code}") 
    
def saltShaker():
    characters = string.ascii_letters + string.digits
    salt = ''.join(random.choices(characters, k=5))
    return salt



