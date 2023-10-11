#! /bin/bash


pathToDateFormater="/home/mistea/PhD/study/thesis/tutorials/OWL examples/SHACL/saggmath/data_preparation/CSVtoRDF2/DateParser.py"
pathToCSVparser="/home/mistea/PhD/study/thesis/tutorials/OWL examples/SHACL/saggmath/data_preparation/CSVtoRDF2/CSVparser.py"
pathToCsv="/home/mistea/PhD/study/thesis/tutorials/OWL examples/SHACL/saggmath/data_preparation/CSVtoRDF2/toParse/csv"
pathToCsvParsed="/home/mistea/PhD/study/thesis/tutorials/OWL examples/SHACL/saggmath/data_preparation/CSVtoRDF2/toParse/csv/parsed"
pathToTurtle="/home/mistea/PhD/study/thesis/tutorials/OWL examples/SHACL/saggmath/data_preparation/CSVtoRDF2/toParse/turtle"
pathToConfig="/home/mistea/PhD/study/thesis/tutorials/OWL examples/SHACL/saggmath/data_preparation/CSVtoRDF2/toParse/json"


#parse date
for file in $(ls "$pathToCsv")
do
    echo $file
    if [[ $file != *parsed* ]]
    then
    fullPathFile="$pathToCsv/$file"
    echo full path $fullPathFile
    basename=$(basename $file .csv)
    "$pathToDateFormater" "$fullPathFile"
    fi
done

echo "parser to RDF"
# parse csv to turtle

for file in $(ls "$pathToCsvParsed")
do
    if [[ $file == *parsed* ]]
    then
    fullPathFile="$pathToCsvParsed/$file"
    basename=$(basename $file .csv)
    echo "COMPUTING $pathToCSVparser -i $fullPathFile -o $pathToTurtle/$basename.ttl $pathToConfig/config_$basename.json"
    "$pathToCSVparser" -i "$fullPathFile" -o "$pathToTurtle/$basename.ttl" "$pathToConfig/config_$basename.json"
    fi
done
