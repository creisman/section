import re
from validator import is_valid_url
from urlparse import urlparse, urlunparse

# Takes in a valid URL and returns the canonicalized form. Returns None if the
# URL is not valid.
def canonicalize(url_string):
  if not is_valid_url(url_string):
    return None

  url = urlparse(url_string)
  # Lowercase protocol and domain
  scheme = url.scheme.lower()
  netloc = url.netloc.lower()
  # Empty query implicitly removed
  # Remove double slashes
  path = "/".join(url.path.split("//"))
  # Sort query parameters
  parameters = url.query.split("&")
  parameters.sort()
  query = "&".join(parameters)

  # Clear fragment
  return urlunparse([scheme, netloc, path, url.params, query, ""])
