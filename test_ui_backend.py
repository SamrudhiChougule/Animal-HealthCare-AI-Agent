import unittest
import requests
import subprocess
import time

class TestAnimalHealthcareApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the Flask app
        cls.app_process = subprocess.Popen(['python', 'app.py'])
        time.sleep(5)  # Wait for app to start
        cls.base_url = "http://localhost:5000"

    @classmethod
    def tearDownClass(cls):
        cls.app_process.terminate()
        cls.app_process.wait()

    def test_backend_api(self):
        base_url = self.base_url

        # Test get_profiles endpoint
        r = requests.get(f"{base_url}/get_profiles")
        self.assertEqual(r.status_code, 200)
        self.assertIn("profiles", r.json())

        # Test create_profile endpoint
        profile_data = {
            "name": "TestPetAPI",
            "type": "Cat",
            "age": "2",
            "breed": "Siamese",
            "gender": "Female"
        }
        r = requests.post(f"{base_url}/create_profile", json=profile_data)
        self.assertEqual(r.status_code, 200)
        self.assertIn("profile", r.json())
        self.assertEqual(r.json()["profile"]["name"], "TestPetAPI")

        # Test advice endpoint
        advice_payload = {
            "profile_name": "TestPetAPI",
            "user_response": "My cat is sneezing"
        }
        r = requests.post(f"{base_url}/advice", json=advice_payload)
        self.assertEqual(r.status_code, 200)
        self.assertIn("advice", r.json())

        # Test tips endpoint
        tips_payload = {"animal_type": "Cat"}
        r = requests.post(f"{base_url}/tips", json=tips_payload)
        self.assertEqual(r.status_code, 200)
        self.assertIn("tips", r.json())

        # Test save_history and get_history endpoints
        history_data = {
            "title": "Chat with TestPetAPI",
            "messages": [
                {"sender": "user", "message": "Hello"},
                {"sender": "bot", "message": "Hi, how can I help?"}
            ]
        }
        r = requests.post(f"{base_url}/save_history", json=history_data)
        self.assertEqual(r.status_code, 200)
        self.assertIn("history", r.json())

        r = requests.get(f"{base_url}/get_history")
        self.assertEqual(r.status_code, 200)
        self.assertIn("history", r.json())

if __name__ == "__main__":
    unittest.main()
