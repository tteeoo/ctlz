import unittest
import ctlz

class Config(unittest.TestCase):
    def test_config_read(self):
        config = ctlz.Config(["/not/good/path.json"], "json", default={"foo": "bar"})
        self.assertEqual({"foo": "bar"}, config.read())

if __name__ == "__main__":
    unittest.main()