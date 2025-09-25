import unittest
import json
from app import app

class AnimalHealthcareAPITest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Animal Healthcare AI Agent', response.data)

    def test_get_profiles(self):
        response = self.app.get('/get_profiles')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('profiles', data)

    def test_create_profile(self):
        profile_data = {
            "name": "TestPet",
            "animal_type": "Dog",
            "age": 3,
            "gender": "Male"
        }
        response = self.app.post('/create_profile', json=profile_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('profile', data)
        self.assertEqual(data['profile']['name'], "TestPet")

    def test_advice(self):
        payload = {
            "profile_name": "TestPet",
            "user_response": "My dog is coughing"
        }
        response = self.app.post('/advice', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('advice', data)

    def test_tips(self):
        payload = {
            "animal_type": "Dog"
        }
        response = self.app.post('/tips', json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('tips', data)

    def test_save_and_get_history(self):
        history_data = {
            "profile_name": "TestPet",
            "chat": [
                {"message": "Hello", "sender": "user"},
                {"message": "Hi, how can I help?", "sender": "agent"}
            ]
        }
        save_response = self.app.post('/save_history', json=history_data)
        self.assertEqual(save_response.status_code, 200)
        save_data = json.loads(save_response.data)
        self.assertIn('history', save_data)

        get_response = self.app.get('/get_history')
        self.assertEqual(get_response.status_code, 200)
        get_data = json.loads(get_response.data)
        self.assertIn('history', get_data)

if __name__ == '__main__':
    unittest.main()
