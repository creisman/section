#!/usr/local/bin/python
"""
This script serves as the entry point for a simple sorting program
"""

import argparse
import sys

from algorithms import sort_fns
from validation import url_validation_fns
from validation.canonicalizer import canonicalize

def main():
  parser = argparse.ArgumentParser(description='Simple sort program')

  parser.add_argument('-i', metavar='in-file', required=True,
                      type=argparse.FileType('r'),
                      help='input file of strings to sort, one per line')
  parser.add_argument('-o', metavar='out-file', required=True,
                      type=argparse.FileType('w'),
                      help='output file for sorted strings, one per line')
  
  # Create URL validation options
  # Get available functions to use for url validation choices
  # from the list of functions defined in __init__.py
  # 
  url_validation_choices = tuple(url_validation_fns.keys())
  

  # Set a default URL validation function 
  #
  if 'all' in url_validation_fns:
    default_url_validation_choice = 'all'
  else:
    default_url_validation_choice = url_validation_choices[0]
  
  # Add command line argument options to parser 
  parser.add_argument('--validate-fn', dest='validate_fn',
          choices=url_validation_choices,
          default=default_url_validation_choice,
          help='enable url validation type.')
  
  # Get available sort functions to use for argument choices
  choices = tuple(sort_fns.keys())
  if 'selectionsort' in sort_fns:
    default = 'selectionsort'
  else:
    default = choices[0]

  parser.add_argument('--sort-fn', dest='sort_fn', choices=choices,
                      default=default,
                      help='sort function to use')

  # Read parsed arguments 
  results          = parser.parse_args()
  infile           = results.i
  outfile          = results.o
  sort_fn          = results.sort_fn
  url_validate_fn  = results.validate_fn

  # read lines
  try:
    lines = infile.readlines()
  except IOError, e:
    parser.error(str(e))
  finally:
    infile.close()
    infile = None

  # argument parser guarantees a valid choice for url_validate_fn
  lines = _validate(lines, url_validation_fns[url_validate_fn])

  # argument parser guarantees a valid choice for sort_fn
  lines = _sort(lines, sort_fns[sort_fn])

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
  
def _validate(url_list, url_validation_fn):
  """Returns a validated copy of URLs list"""
  validated_url = list(url_list)
  
  validated_url = url_validation_fn(validated_url)
  
  ## See url_validation.py for adding implementations for
  ## various validation functions
  return validated_url

def _sort(str_list, sort_fn):
  """Return a sorted copy of str_list, using functionsort_fn"""
  copy = list(str_list)

  sort_fn(copy)

  return copy

# Define equals to be equality of the canonical form.
# Only defined for valid URLs.
def _equals(url1, url2):
  return canonicalize(url1) == canonicalize(url2)

# Define less than to be less than of the canonical form.
# Only defined for valid URLs.
def _less(url1, url2):
  return canonicalize(url1) < canonicalize(url2)

# Define greater than to be greater than of the canonical form.
# Only defined for valid URLs.
def _greater(url1, url2):
  return canonicalize(url1) > canonicalize(url2)

if __name__ == '__main__':
  main()

