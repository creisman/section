#!/usr/bin/python
import unittest
import sys
import os

root = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(root)

from validation.canonicalizer import canonicalize
from validation.validator import (
  is_valid_url,
  _valid_scheme,
  _valid_netloc,
  _valid_path,
  _valid_query,
  _valid_fragment
)

class TestCanonicalizer(unittest.TestCase):
  def test_lower_scheme_domain(self):
    self.assertEquals("http://google.com", canonicalize("HtTP://GooGlE.COm"))
    self.assertEquals("http://google.com/Bob", canonicalize("HtTP://GooglE.com/Bob"))

  def test_remove_double_slashes(self):
    self.assertEquals("http://google.com/test", canonicalize("http://google.com//test"))
    self.assertEquals("http://google.com/test/blah/ick/", canonicalize("http://google.com/test//blah//ick//"))

  def test_remove_empty_query(self):
    self.assertEquals("http://google.com", canonicalize("http://google.com?"))
    self.assertNotEquals("http://google.com", canonicalize("http://google.com?test=blah"))

  def test_sort_query_parameters(self):
    self.assertEquals("http://google.com?a=b&c=d", canonicalize("http://google.com?c=d&a=b"))
    self.assertEquals("http://google.com?password=******&username=test", canonicalize("http://google.com?username=test&password=******"))

  def test_remove_fragment(self):
    self.assertEquals("http://google.com", canonicalize("http://google.com#thisisatest"))
    self.assertEquals("http://google.com/test/testing", canonicalize("http://google.com/test/testing#boompow"))

class TestValidator(unittest.TestCase):
  # The empty string is not valid.
  def test_empty(self):
    self.assertFalse(is_valid_url(""))

  # Tests varied case schemes.
  def test_scheme(self):
    self.assertFalse(_valid_scheme(""))
    self.assertTrue(_valid_scheme("http"))
    self.assertTrue(_valid_scheme("https"))
    self.assertTrue(_valid_scheme("ftp"))
    self.assertTrue(_valid_scheme("hTTp"))
    self.assertTrue(_valid_scheme("HttP"))
    self.assertTrue(_valid_scheme("fTP"))

  # Tests the scheme with special characters like -, ., numbers, etc.
  def test_scheme_special_characters(self):
    self.assertTrue(_valid_scheme("htt-ps"))
    self.assertFalse(_valid_scheme("ht..pt"))
    self.assertTrue(_valid_scheme("ht09"))
    self.assertFalse(_valid_scheme("blah?:"))

  # Tests basic domains.
  def test_netloc(self):
    self.assertFalse(_valid_netloc(""))
    self.assertTrue(_valid_netloc("www.google.com"))
    self.assertTrue(_valid_netloc("google.com"))
    self.assertTrue(_valid_netloc("mail.google.com"))

  # Domain extensions outside the allowed range.
  def test_netloc_bad_domain_extensions(self):
    self.assertFalse(_valid_netloc("test"))
    self.assertFalse(_valid_netloc("test.x"))
    self.assertFalse(_valid_netloc("test.blargh"))

  # For simplicity, port limited to 5 numbers, not 65535.
  def test_netloc_with_port(self):
    self.assertTrue(_valid_netloc("google.com:8000"))
    self.assertTrue(_valid_netloc("google.com:1"))
    self.assertFalse(_valid_netloc("google.com:")) # No number specified
    self.assertFalse(_valid_netloc("google.com:100000"))

  # Tests whether it correctly validates with the scheme and domain.
  def test_scheme_and_domain_is_valid_url(self):
    self.assertTrue(is_valid_url("http://google.com"))
    self.assertTrue(is_valid_url("http://www.google.com"))
    self.assertTrue(is_valid_url("https://google.com"))

  # Tests whether the port is properly validated (note, limited to 5 numbers, not 65535).
  def test_with_port(self):
    self.assertTrue(is_valid_url("http://google.com:8000"))
    self.assertFalse(is_valid_url("http://google.com:"))
    self.assertFalse(is_valid_url("http://google.com:100000"))

  def test_all(self):
    self.assertTrue(is_valid_url("http://google.com:80/blah/blah?this=test&blah&blah=#icky"))
    self.assertFalse(is_valid_url("htt?p://google.z:800/bla()/?this is a = test#blah test"))

  # Tests the path with no whitespace
  def test_path_no_whitespace(self):
    self.assertTrue(_valid_path(""))
    self.assertTrue(_valid_path("/path/to/stuff"))
    self.assertTrue(_valid_path("/path/with/trailing/slash/"))

  # Tests if it is valid with whitespace in the path.
  def test_path_whitespace(self):
    self.assertFalse(_valid_path("/path to nowhere"))
    self.assertFalse(_valid_path("/path with trailing slash/"))

  # Tests a path with bad characters like () and <>
  def test_path_with_illegal_characters(self):
    self.assertFalse(_valid_path("/path()/"))
    self.assertFalse(_valid_path("/blah>dum<"))

  # Tests a query.
  def test_query(self):
    self.assertTrue(_valid_query("test=blah"))
    self.assertTrue(_valid_query(""))
    self.assertTrue(_valid_query("test"))
    self.assertTrue(_valid_query("test="))
    self.assertTrue(_valid_query("test=blah&bork=test"))
    self.assertFalse(_valid_query("test=blah&"))

  # Tests query with whitespace.
  def test_query_whitespace(self):
    self.assertFalse(_valid_query("test=big truck"))
    self.assertFalse(_valid_query("big truck="))
    self.assertFalse(_valid_query("test=blah&borked test=lol"))

  # Tests fragment.
  def test_fragment(self):
    self.assertTrue(_valid_fragment("adsfkl;jad;fkljasdflk;jasdf;klj"))

  # Tests whitespace in fragment
  def test_fragment_whitespace(self):
    self.assertFalse(_valid_fragment("asdkl;fj adf;lkj asdfa;kdlfjadfadf      "))

if __name__ == "__main__":
    unittest.main()
