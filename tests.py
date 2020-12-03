import unittest
import crud
import os
from server import app, current_user
from model import connect_to_db, db, User

class TestAuthentication(unittest.TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()

        

    def test_create_user(self):
        """Test create_user function by checking if instance returned is User."""
        user = crud.create_user(email="test1@test.com", password="password1", uname="test1")
        self.assertIsInstance(user, User)


    def test_park_search_response(self):
        """Test response from landing page."""

        response = self.client.get('/park_search', content_type="html/text")
        self.assertEqual(response.status_code, 200)


    def test_park_search(self):
        """Test that park_search loads correctly."""

        response = self.client.get('/park_search')
        self.assertIn(b'Which features would you like to search by?', response.data)


    def test_user_reg(self):
        """Test user registration page"""
        
        response = self.client.post("/users",
                                data={"email":"test1000@test.com", 
                                "password":"password1000",
                                "uname":"test1000"},
                                follow_redirects=True)   
        
        self.assertIn(b"Account created! You can now log in.", response.data)

        
    def test_user_login(self):
        """Test login page"""

        response = self.client.post("/login",
                                data={"email":"test1@test.com", 
                                "password":"password1"},
                                follow_redirects=True)

        self.assertIn(b"Logged in", response.data)    

    def tearDown(self):
        """Do at the end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()


if __name__ == '__main__':
    unittest.main()