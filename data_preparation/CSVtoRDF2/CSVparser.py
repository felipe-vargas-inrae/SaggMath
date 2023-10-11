#!/usr/bin/python

""" This module aims at converting a csv file into a RDF graph in turtle syntax.
    More specificly it will read the columns and parse them using the given associative array
"""
__author__ = "Guilhem Heinrich"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Guilhem Heinrich"
__email__ = "guilhem.heinrich@inra.fr"
__status__ = "Prototype"

import argparse
import datetime
import csv
import json
import uuid
import re
from string import Formatter

""" Unicode dict reader, from <https://stackoverflow.com/questions/5004687/python-csv-dictreader-with-utf-8-data>"""
def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, delimiter = ",", **kwargs)
    for row in csv_reader:
        yield {unicode(key, 'utf-8'):unicode(value, 'utf-8') for key, value in row.iteritems()}

class CSVtoTurtleConverter(object):
    """ A class to convert a csv to a rdf turtle file"""
    """ Initialize the attributes's instance with corresponding values"""
    def __init__(self, prefix="", postfix = "", assocRules=[], grouping={}):
        self.assoc_rules = assocRules
        self.prefix = prefix
        self.postfix = postfix
        self.grouping = grouping

        self.END_LINE_SHARED_SUBJECT= ';'
        self.END_LINE= '.'
        self.DELIMITER = ';'

        AllUuidPerRow = []
        for rule in self.assoc_rules:
            AllUuidPerRow += re.findall(r'\{(uuid_\d+)\}', rule)
        self.uuid_per_row = set(AllUuidPerRow)
    """ Intern method responsable of writing the 'agregated' or 'grouped' values"""
    def __computeGrouping(self, csvFile):
        groups_uuid = {}
        group_prefix = []
        with open(csvFile) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for col in self.grouping.keys():
                group = self.grouping[col]
                groups_uuid[col] = {}
                ## dateNow need to be consistent across all rows of a grouping
                dateNow = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
                last_grouping_column_value = None 
                for row in reader:
                    ## Handle multiline string as litteral, clear unused space
                    for key in row.keys():
                        if isinstance(row[key], basestring):
                            row[key] = ' '.join(row[key].split())
                    if last_grouping_column_value == None:
                        group_uuid = str(uuid.uuid4())
                        last_grouping_column_value = row[col]
                    elif last_grouping_column_value != row[col]:
                        group_uuid = str(uuid.uuid4())
                    ## Added for further reference of the grouping inside the grouping rules
                    row['dateNow'] = dateNow
                    row['group_uuid'] = group_uuid
                    groups_uuid[col][row[col]] = group_uuid
                    line = ''
                    for rule in group:
                        line += rule.format(**row) + "\n"
                    line = line.encode('ascii', 'ignore')
                    group_prefix.append(line)
                    last_grouping_column_value = row[col]
            group_prefix = set(group_prefix)
        return groups_uuid, "\n".join(group_prefix)
    """ Intern method responsable of writing a single row"""
    def __processRow(self, row, turtlefile, cpt, groups_uuid):
        # Handle multiline string as litteral
        for key in row.keys():
            if isinstance(row[key], basestring):
                row[key] = ' '.join(row[key].split())
        row['dateNow'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
        # Handle grouping (uuid per column)
        for col in self.grouping:
            row[col] = groups_uuid[col][row[col]]
        # Handle uuid per row 
        for key in self.uuid_per_row:
            row[key] = str(uuid.uuid4())
        # Add an identifier for the row index
        row['row'] = cpt
        # Fullfil the rules
        turtle_block = ''.encode('utf-8', 'ignore')

        triple_line = None
        print("row:", row)
        for rule in self.assoc_rules:
            skip = False
            for value in Formatter().parse(rule):
                if value[1] is not None:  
                    if row[value[1]] is '':
                        skip = True
                        break
            if skip:
                continue
            line = rule.format(**row)
            line = line.strip() # remove spaces in the begining and the end

            if triple_line is not None: # dependency from a delected item
                line = triple_line.subject + " "+ line
                triple_line = None # subject was added to line

            check = self.check_numerical_nulls(line)
            if check: # if there is a null numerical property then don't add the rule

                line_end = line[-1] # last character from the line
                if line_end == self.END_LINE_SHARED_SUBJECT: 
                    if (self.is_a_triple(line)):# it means that the next line depends on current subject
                        triple_line= self.to_triple(line)
                elif line_end == self.END_LINE: # a line with end block line will be deleted

                    # last line in the turtle block contained a ';' character it is replaced by '.'
                    if len(turtle_block) > 2 and turtle_block[-2]==self.END_LINE_SHARED_SUBJECT:
                        turtle_block=self.replace_end_line(turtle_block)
                
                continue
                    

            line += "\n"
            line = line.encode('utf-8', 'ignore')

            turtle_block += line

            #turtlefile.write(line)
        
        turtlefile.write(turtle_block+'\n')

    """ Main public method, parsing a $csvFile into $turtleFile""" 
    def parse_csv(self, csvFile, turtleFile):
        """This function read a csv file and parse its content as a turtle rdf file"""
        groups_uuid, group_prefix = self.__computeGrouping(csvFile)
        with open(csvFile) as csvfile:
            with open(turtleFile, 'w') as turtlefile:
                reader = UnicodeDictReader(csvfile)
                turtlefile.write(self.prefix)
                turtlefile.write('\n')
                turtlefile.write(group_prefix)
                turtlefile.write('\n')
                cpt = 0
                for row in reader:
                    self.__processRow(row, turtlefile, cpt, groups_uuid)
                    cpt += 1
                turtlefile.write(self.postfix)

    """main method to test if a line contains a null numerical value"""
    def check_numerical_nulls(self, line):
        r1 = re.findall(r'"(\w+.?\w*)"\^\^xsd\:[decimal|double]+',line)
        
        for val in r1:
            try:
                y = float(val)
            except ValueError:
                return True # there is a null value

        return False #not null value found
    """main method to test if a line is a triple"""
    def is_a_triple(self,triple):
        pattern = re.compile(r'^\w+\s+\w+\s+\w+\s+[\.|\;]{1}$')
        return bool(pattern.match(triple))

    """main method to create a triple from an string @triple_str should be a valid triple"""
    def to_triple(self,triple_str):
        result = re.findall(r'^(\w+)\s+(\w+)\s+(\w+)\s+[\.|\;]{1}$', triple_str)
        for t in result:
            return dict(subject=t[0], predicate=t[1], object = t[2])
        
    def replace_end_line(self, turtle_block):
        return turtle_block[:-2] + "." + turtle_block[-1:]

        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = """ This module aims at converting a csv file into a text (or any extension) file.
    More specificly it will read the rows and columns and parse them using the given a parameter file.
    This parameter file precise prefixes, suffixes, the rules to execute every lines and the rules to execute only once.

    More specically, the config.json file MAY have a prefix array and a postfix array, and a groupingRules dictionary.
    It MUST have an associative rules array.

    Each lines of the prefix, postfix, associtive array, and arrays in each entry of the groupingRules dictionary
    will be parse using the python string.format, whith python formating field delimiter : \{ ... \}.

    When specifying 'rules' to be parsed, the field between \{\} you should provide should be the columns names, or one 
    of the special values :
        'dateNow' => will output the current machine timestamp
        'row' => the actual row index
        'uuid_X' where X is one or more digit => a unique uuid generated every rows
    Inside the groupingRules, uuid_X and row are no supported, but the 'group_uuid' is available.
    This special field name will generate a unique value based on the key corresponding to the grouping rule.

    Here is a compete exemple config file :

    {
    ## WILL BE PARSED ONCE, WRITING IT AT THE BEIGIN OF THE FILE
    "prefix" : [
        "PREFIX oeev: <http://www.phenome-fppn.fr/vocabulary/m3p/2015/event#> ",
        "PREFIX owl: <http://www.w3.org/2002/07/owl#> ",
        "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ",
        "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> ",
        "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> ",
        "PREFIX dcterms: <http://purl.org/dc/terms/> ",
        "PREFIX oa: <http://www.w3.org/ns/oa#> ",
        "PREFIX dc: <http://purl.org/dc/elements/1.1/>",
        "PREFIX phenology: <http://www.phenome-fppn.fr/vocabulary/m3p/2018/phenology#>",
        "PREFIX time: <http://www.w3.org/2006/time#> ",
        "PREFIX agent: <http://www.phenome-fppn.fr/id/agent/> ",
        "PREFIX annotation: <http://www.phenome-fppn.fr/id/annotation/> ",
        "PREFIX instant: <http://www.phenome-fppn.fr/id/instant/> ",
        "PREFIX event: <http://www.phenome-fppn.fr/id/event/> "
    ],
    ## WILL BE PARSED ONCE, WRITING IT AT THE END OF THE FILE
    "postfix" : [
        ""
    ],
    ## WILL BE PARSED ONCE FOR EVERY DIFFERENT VALUE OF THE KEY, WRITING IT AT THE BEGIN OF THE FILE
    ## EACH ENTRY IN THE DICTIONARY IS THE NAME OF THE COLUMN USED FOR AGGREGATION
    "groupingRules" : {
        "Content" : [
            "annotation:{group_uuid} rdf:type oa:Annotation ;",
            "   oa:bodyValue \"{Content}\"^^xsd:string ;",
            "   oa:motivatedBy oa:describing ;",
            "   dcterms:creator agent:{Creator} ;",
            "   dcterms:created \"{Created}\"^^xsd:dateTimeStamp ."
        ]
    },
    ## WILL BE PARSED EVERY ROW
    "associativeRules" :[
        "instant:{uuid_1} rdf:type time:Instant ;",
        "   time:inXSDDateTimeStamp \"{Date event}\"^^xsd:dateTimeStamp ;",   
        "event:{uuid_1} rdf:type oeev:{RDFType} ;",
        "   time:hasTime instant:{uuid_1} ;", 
        "   oeev:concern <{uri}> ;",
        "   oeev:hasPest \"{RDFLabel}\"^^xsd:string .",
        "annotation:{Content} oa:hasTarget event:{uuid_1} ."
    ]
}

""", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('configJSON', help="""Path to the configuration file to parse the csv, in json format.""")
    parser.add_argument('-i', dest = 'input', help="""Path to the input CSV file""")
    parser.add_argument('-o', dest = 'output', help="""Path to the output turtle file""")
    args = parser.parse_args()
    with open(args.configJSON, 'r') as jsonconfigfile:
        config = json.load(jsonconfigfile)
        converter = CSVtoTurtleConverter(\
        ' \n'.join(config['prefix']) if 'prefix' in config else "\n",\
        ' \n'.join(config['postfix']) if 'postfix' in config else "\n",\
        config['associativeRules'],\
        config['groupingRules'] if 'groupingRules' in config else {})
        converter.parse_csv(args.input, args.output)    
