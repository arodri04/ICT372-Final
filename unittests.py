import unittest
from flask import session
from app import app
from database.Utils import validateLogin, connectDB

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "testkey"
        self.client = app.test_client()
    
    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"To do", response.data)
        
    def test_login_page(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)
        
    
    def test_logout(self):
        with self.client:
            self.client.post("/login", data={"username": "samtest@gmail.com", "password": "AggiesR0ck$"})
            response = self.client.get("/logout", follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn("user", session)
            
class TestSQLiteUtils(unittest.TestCase):
    def test_get_db_connection(self):
        conn =connectDB()
        self.assertIsNotNone(conn)
        conn.close()
        
    def test_validate_login(self):
        self.assertTrue(validateLogin("samtest@gmail.com", "AggiesR0ck$"))
        self.assertFalse(validateLogin("samtest@gmail.com", "wrong"))
        self.assertFalse(validateLogin("wrong", "AggiesR0ck$"))
        
if __name__ == "__main__":
    unittest.main()