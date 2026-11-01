import unittest
from http.server import HTTPServer
from threading import Thread
from urllib.request import urlopen
from urllib.error import HTTPError

import app


class AppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), app.Handler)
        cls.thread = Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_homepage(self):
        with urlopen(self.base_url + "/") as response:
            body = response.read().decode()

            self.assertEqual(response.status, 200)
            self.assertIn("message:", body)
            self.assertIn("version:", body)
            self.assertIn("hostname:", body)

    def test_health_endpoint(self):
        with urlopen(self.base_url + "/healthz") as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.read().decode(),"ok\n")

    def test_readiness_endpoint(self):
        with urlopen(self.base_url + "/readyz") as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.read().decode(),"ready\n")

    def test_uknown_path(self):
        with self.assertRaises(HTTPError) as error:
            urlopen(self.base_url + "/goobledy")

            self.assertEqual(error.exception.code, 404)

if __name__ == "__main__":
    unittest.main()
