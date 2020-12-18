import unittest
import webapp2


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = webapp2.app.test_client()
        self.app.testing = True

    def test_departments(self):
        home = self.app.get('/')
        self.assertIn('Departments', str(home.data))


if __name__ == "__main__":
    unittest.main()
