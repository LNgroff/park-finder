from unittest import TestCase
from werkzeug.security import (generate_password_hash, check_password_hash)
from server import app
from model import connect_to_db, db, User
import json
import crud
import server

class TestAuthentication(unittest.TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, db_uri="TEST_DB_URI")

        db.drop_all()
        db.create_all()


    def test_user_login(self):
        """Test login page"""

        result = self.client.post("/login",
                                data={"email": "user0@test.com", "password": "test0"},
                                follow_redirects=True)
        self.assertIn(b"You have logged in", result.data)    

    def test_user_reg(self):
        """Test user registration page"""
        
        result = self.client.post("/register_user",
                                data={"email":"test1@test.com", 
                                "password":"password1",
                                "uname":"test1"},
                                follow_redirects=True)   
        
        self.assertIn(b"you have registerd", result.data)



if __name__ == '__main__':
    unittest.main()