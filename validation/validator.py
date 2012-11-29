import re
from urlparse import urlparse

# These are function entry points to match the URL validation options
def all(urlList):
	# This method is added for completeness in mapping options to a
	# function, but functionally, this function does not perform 
	# any real work at this time.
	return urlList

def valid(urlList):
	return filter(is_valid_url, urlList)
	
def invalid(urlList):
	return filter(lambda url: not is_valid_url(url), urlList)

def _valid_scheme(scheme):
  return re.match("^[\w-]+$", scheme)

def _valid_netloc(netloc):
  return re.match("^[a-zA-Z0-9.-]+[.][a-zA-Z]{2,4}(:[0-9]{1,5})?$", netloc)

def _valid_path(path):
  return re.match("^(/[^\s()<>?]*)*$", path)

def _valid_query(query):
  return re.match("^([^\s&=#]+(=[^\s&=#]*)?(&[^\s&=#]+(=[^\s&=#]*)?)*)?$", query)

def _valid_fragment(fragment):
  return re.match("^[^\s]*$", fragment)

# Takes in a string and returns true if it is a valid URL, else false.
def is_valid_url(url_string):
  url = urlparse(url_string)

  return _valid_scheme(url.scheme) and _valid_netloc(url.netloc) and _valid_path(url.path) and \
         _valid_query(url.query) and _valid_fragment(url.fragment)

  # The old way...
  #return re.match("[a-z][\w-]+://[a-zA-Z0-9.-]+[.][a-zA-Z]{2,4}[0-9]{0,5}(/[^\s()<>?]*)*(\?([^\s&=]+(=[^\s&=]*)?(&[^\s&=]+(=[^\s&=]*)?)*))?(#[^\s]*)?$", url_string)
