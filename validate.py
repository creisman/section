#!/usr/local/bin/python
"""
This script serves as the entry point for a simple validation program
"""

import argparse
import sys

from collections import Counter

from validation.canonicalizer import canonicalize
from validation.validator import is_valid_url

def main():
  parser = argparse.ArgumentParser(description='Simple validation program')

  parser.add_argument('-i', metavar='in-file', required=True,
                      type=argparse.FileType('r'),
                      help='input file of strings to validate, one per line')
  parser.add_argument('-o', metavar='out-file', required=True,
                      type=argparse.FileType('w'),
                      help='output file for validated strings, one per line')
  
  # Read parsed arguments 
  results          = parser.parse_args()
  infile           = results.i
  outfile          = results.o

  # read lines
  try:
    lines = infile.read().splitlines()
  except IOError, e:
    parser.error(str(e))
  finally:
    infile.close()
    infile = None

  source_counter = Counter(lines)
  canonical_lines = map(canonicalize, lines)
  canonical_counter = Counter(canonical_lines)

  for index in range(0, len(lines)):
    url = lines[index]
    curl = canonical_lines[index]
    valid = is_valid_url(url)
    print "Source: " + url
    print "Valid: " + ("true" if valid else "false")
    if valid:
      print "Canonical: " + curl
    print "Source unique: " + ("true" if source_counter[url] == 1 else "false")
    if valid:
      print "Canonicalized URL unique: " + ("true" if canonical_counter[curl] == 1 else "false")

  # write output
  try:
    for line in lines:
      outfile.write(line)
  except IOError, e:
    parser.error(str(e))
  finally:
    outfile.close()
    outfile = None

  sys.exit(0)
  
if __name__ == '__main__':
  main()

