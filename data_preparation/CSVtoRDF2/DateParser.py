#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import time
import argparse
import os
import ntpath
from itertools import islice


""" This module aims at converting all occurence of a date to
    a valid xsd:dateTimeStamp.

    :Exemple:
    >>> # in python
    >>> datestring = '20-02-2018 blasdjwbc 20-04-2018'
    >>> DateFormatter.fromString(datestring)
    '2018-02-20T12:00:00Z blasdjwbc 2018-04-20T12:00:00Z'
"""
__author__ = "Guilhem Heinrich"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Guilhem Heinrich"
__email__ = "guilhem.heinrich@inra.fr"
__status__ = "Prototype"

class DateFormatter:
    token = 'MATCH'
    date_format_regex = [
        r'(?P<year>\d{4})(?P<sepD>.)(?P<mounth>\d{2})(?P=sepD)(?P<day>\d{2})',
        r'(?P<day>\d{2})(?P<sepD>.)(?P<mounth>\d{2})(?P=sepD)(?P<year>\d{4})',
        r'(?P<year>\d{4})(?P<sepD>.)(?P<mounth>\d{2})(?P=sepD)(?P<day>\d{2}).{0,2}\
(?P<hour>\d{2})(?P<sepT>)(?P<minute>\d{2})(?P=sepT)(?P<second>\d{2})',
        r'(?P<day>\d{2})(?P<sepD>.)(?P<mounth>\d{2})(?P=sepD)(?P<year>\d{4}).{0,2}\
(?P<hour>\d{2})(?P<sepT>)(?P<minute>\d{2})(?P=sepT)(?P<second>\d{2})'
    ]
    def __init__(self,
                 year='2000',
                 mounth='01',
                 day='01',
                 hour='12',
                 minute='00',
                 second='00',
                 timezoneShift=None,
                 **kwargs): # Kwargs is here to allow passing a dict with more
                 # arguments than required. It's a junk.
        self.year = year
        self.mounth = mounth
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.timezone_shift = time.localtime().tm_isdst
        if timezoneShift:
            self.timezone_shift = timezoneShift
    def asXsdDateTimeStamp(self):
        # pattern_XsdDateTimeStamp = '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z|((+|-)\d{2}:\d{2})'
        output = "{year}-{mounth}-{day}T{hour}:{minute}:{second}".format(
            **self.__dict__)
        if self.timezone_shift == 0:
            output += 'Z'
        elif isinstance(self.timezone_shift, int):
            # If it's an integer, it's between -14 and 14
            assert self.timezone_shift < 15 and self.timezone_shift > -15
            if self.timezone_shift > 0:
                output += '+'
                if self.timezone_shift < 9:
                    output += '0' + str(self.timezone_shift) + ':00'
                else:
                    output += str(self.timezone_shift) + ':00'
            else:
                if self.timezone_shift > -10:
                    output += '0' + str(abs(self.timezone_shift)) + ':00'
                else:
                    output += str(abs(self.timezone_shift)) + ':00'
        # Otherwise it's already a string
        else:
            assert isinstance(self.timezone_shift, basestring)
            output += self.timezone_shift
        return output
    @staticmethod
    def compute(stringOrMatch, token=''):
        if stringOrMatch.__class__.__name__ == 'SRE_Match':
            dateFormatter = DateFormatter(**stringOrMatch.groupdict())
            return token + dateFormatter.asXsdDateTimeStamp()
        else:
            return stringOrMatch
    @staticmethod
    def fromFile(infile, outfile=None):
        
        with open(outfile, 'w') as outputFile:
            for chunk in DateFormatter.read_in_chunks(infile, 200):
                new_chunk = DateFormatter.fromString(chunk)
                outputFile.write(new_chunk)
    @staticmethod
    def fromString(stringToParse):
        old_line = stringToParse
        for pattern in DateFormatter.date_format_regex:
            patternAndToken = '(?<!' + DateFormatter.token + ')' + pattern
            new_line = re.sub(patternAndToken, lambda line: DateFormatter.compute(
                line, DateFormatter.token), old_line)
            if old_line != new_line:
                old_line = new_line
        new_line = re.sub(DateFormatter.token, '', new_line)
        return new_line

    @staticmethod
    def read_in_chunks(file_path, n):
        with open(file_path) as fh:
            while True:
                lines = list(islice(fh, n))
                if lines: yield "".join(lines)
                else:     break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=""" This utility converts all dates to
    the xsd:DateTimeStamp format (As described in http://www.datypic.com/sc/xsd11/t-xsd_dateTimeStamp.html).
    If only one file is supplied as input, the output option (-o) can specify the path/to/newfile.
    By default, '_parser' is append to the input filename and written in the directory child '/parsed/'.

    It will convert a string like '20-02-2018 blasdjwbc 20-04-2018' in '2018-02-20T12:00:00Z blasdjwbc 2018-04-20T12:00:00Z'
    """)
    parser.add_argument('inputs', metavar='inputs', nargs='+',
                        help="""Path to the input(s) file""")
    parser.add_argument('-o', dest='output', nargs='?',
                        help="""Path to the output file""")
    args = parser.parse_args()
    # print args.__dict__
    inputs_filename = args.inputs
    if args.output is not None:
        DateFormatter.fromFile(infile=inputs_filename[0], outfile=args.output)
    else:
        for fullname in inputs_filename:
            infile, file_extension = os.path.splitext(fullname)
            directory_name = os.path.dirname(infile)
            filename = os.path.basename(infile)
            if os.path.isdir(infile):
                continue
            if not os.path.isdir(directory_name + '/parsed/'):
                os.mkdir(directory_name + '/parsed/')
            outfile = directory_name + '/parsed/' + filename + '_parsed' + file_extension
            DateFormatter.fromFile(infile=fullname, outfile = outfile)
        
