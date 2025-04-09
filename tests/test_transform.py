import unittest
from etl.transform import clean_text, tokenize_text

class TestTransform(unittest.TestCase):
    def test_clean_text(self):
        text = "Check this out! https://example.com #wow @user" # Mens Lume Dial Army Analog Quartz Wrist Watch Sport Blue Nylon Fabric  - Full reaÛ_ http://t.co/hEP9k0XgHb http://t.co/80EBvglmrA,0
        clean = clean_text(text)

        self.assertEqual(clean, "check this out!")
        

    def test_tokenize_text(self):
        tokens = tokenize_text("this is a test tweet")
        self.assertTrue("test" in tokens and "tweet" in tokens)