import unittest
from myproject.api import app  # Assuming your FastAPI app is in 'myproject.api'

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_registration_success(self):
        response = self.app.post("/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "strongpassword123"
        })
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()