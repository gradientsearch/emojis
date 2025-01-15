import unittest
import os


class TestEmojiUnicodeChar(unittest.TestCase):

    def test_unicode(self):
        with open('static/grinning', 'w') as f:
            f.write("\U0001F601")
            f.flush()
            os.fsync(f.fileno())
