
import json
import unittest
from http.client import HTTPConnection
from threading import Thread
from http.server import HTTPServer

from app.main import AppHandler


class TestAppHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), AppHandler)
        cls.port = cls.server.server_address[1]

        cls.server_thread = Thread(
            target=cls.server.serve_forever,
            daemon=True,
        )
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def request(self, path):
        connection = HTTPConnection("127.0.0.1", self.port)
        connection.request("GET", path)
        response = connection.getresponse()

        status = response.status
        headers = response.getheaders()
        body = response.read()

        connection.close()
        return status, headers, json.loads(body)

    def test_root_endpoint(self):
        status, headers, body = self.request("/")

        self.assertEqual(status, 200)
        self.assertEqual(body["app"], "Secure Container Delivery Platform")
        self.assertEqual(body["status"], "running")

    def test_health_endpoint(self):
        status, headers, body = self.request("/health")

        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "healthy")

    def test_unknown_endpoint(self):
        status, headers, body = self.request("/unknown")

        self.assertEqual(status, 404)
        self.assertEqual(body["error"], "Not found")

    def test_json_content_type(self):
        status, headers, body = self.request("/health")

        content_type = dict(headers).get("Content-Type")
        self.assertEqual(content_type, "application/json")


if __name__ == "__main__":
    unittest.main()
