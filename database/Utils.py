import sqlite3
import hashlib
import string
import re
from datetime import date
import random

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

def getUserTodos(userId):
    try:
        conn = connectDB()
        if not conn:
            return False
        
        cursor = conn.cursor()
        query = "SELECT * FROM todo WHERE userId = ?"
        cursor.execute(query,(userId,))
        result = cursor.fetchall()
        if result:
            return result
            
        return result
    
    except sqlite3.Error as e:
        print(f"Database Error {e}")
        return False
    
    finally:
        if conn:
            conn.close()

def saltShaker():
    characters = string.ascii_letters + string.digits
    salt = ''.join(random.choices(characters, k=5))
    return salt

def getLateList(todos):
    lateList = []
    if len(todos) > 0:
        for todo in todos:
            dueDate = todo[5].split('-')
            if (date(int(dueDate[0]),int(dueDate[1]),int(dueDate[2])) < date.today()) and (todo[4] != todo[5]) and not todo[2]:
                lateList.append(todo)
    return lateList
