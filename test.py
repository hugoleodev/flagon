import unittest
from main import app


class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_app(self):
        resp = self.client.get("/abc")

        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
