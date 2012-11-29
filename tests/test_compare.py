#!/usr/bin/python
import unittest
import sys
import os

root = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(root)

from sort import _less, _greater, _equals

class TestAlgorithms(unittest.TestCase):
  def test_equals(self):
    self.assertTrue(_equals("http://google.com", "http://google.com"))
    self.assertTrue(_equals("http://GooGLe.COm//test/blah?b=c&a=d", "http://google.cOM/test//blah?a=d&b=c"))
    self.assertFalse(_equals("http://google.com", "http://bing.com"))
  def test_less(self):
    self.assertTrue(_less("http://bing.com", "http://Google.com"))
    self.assertTrue(_less("http://bing.COm//test/blah?b=c&a=d", "http://google.cOM/test//blah?a=d&b=c"))
    self.assertFalse(_less("http://Google.com", "http://bing.com"))
  def test_two(self):
    self.assertTrue(_greater("http://google.com", "http://Bing.com"))
    self.assertTrue(_greater("http://GooGLe.COm//test/blah?b=c&a=d", "http://bing.cOM/test//blah?a=d&b=c"))
    self.assertFalse(_greater("http://Bing.com", "http://google.com"))


if __name__ == "__main__":
    unittest.main()
