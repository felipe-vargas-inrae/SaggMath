#! /bin/bash

#PHIS publi
/mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/eclipse-rdf4j-2.2.4/bin/console.sh -s http://147.100.179.156:8080/rdf4j-server
open phispubli3

#AgMIP
/mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/eclipse-rdf4j-2.2.4/bin/console.sh -s http://138.102.159.37:8080/rdf4j-server
open AgMIP

# load installations
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/Installation_parsed.ttl into http://www.phenome-fppn.fr/set/installation
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/meteosites_parsed.ttl into http://www.phenome-fppn.fr/set/installation

# load species
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/species_parsed.ttl into http://www.phenome-fppn.fr/set/species

# load datasources
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/datasource_parsed.ttl into http://www.phenome-fppn.fr/set/datasource

#load variety
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/variety_parsed.ttl into http://www.phenome-fppn.fr/set/variety

# load experiments & projects
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/experiment_parsed.ttl into http://www.phenome-fppn.fr/set/experiment
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/project_parsed.ttl into http://www.phenome-fppn.fr/set/project

#load variables
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/variables_parsed.ttl into http://www.phenome-fppn.fr/set/variable
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/trait_method_unit_parsed.ttl into http://www.phenome-fppn.fr/set/variable
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/envirovariable_parsed.ttl into http://www.phenome-fppn.fr/set/variable

#load variable experiment
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/var_def_dia.ttl into http://www.phenome-fppn.fr/diaphen/DIA2017-05-19/variables
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/var_def_za17_new.ttl into http://www.phenome-fppn.fr/m3p/ARCH2017-03-30/variables

#load oa
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/oa.ttl into http://www.w3.org/ns/oa

# load agents
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/Agent_parsed.ttl into http://www.phenome-fppn.fr/set/agent

# load devices
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/sensor_parsed.ttl into http://www.phenome-fppn.fr/set/device 
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/sensor_parsed.ttl into http://www.phenome-fppn.fr/mtp/sensors 

# load pots
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/pots_parsed.ttl into http://www.phenome-fppn.fr/set/device

# load scientfic objects Mauguio
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/queryLeafDIA_parsed.ttl into http://www.phenome-fppn.fr/diaphen/DIA2017-05-19
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/queryPlantDIA_parsed.ttl into http://www.phenome-fppn.fr/diaphen/DIA2017-05-19
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/queryPlotDIA_parsed.ttl into http://www.phenome-fppn.fr/diaphen/DIA2017-05-19

# load scientfic objects ARCH
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/queryEarZa17_parsed.ttl into http://www.phenome-fppn.fr/m3p/ARCH2017-03-30
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/queryLeafZA17_parsed.ttl into http://www.phenome-fppn.fr/m3p/ARCH2017-03-30
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/queryPlantZA17_parsed.ttl into http://www.phenome-fppn.fr/m3p/ARCH2017-03-30

# load events
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/Events_ARCH_DIA-toImport_parsed.ttl into http://www.phenome-fppn.fr/set/annotation
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/Events_pest_Mauguio_parsed.ttl into http://www.phenome-fppn.fr/set/annotation
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/events_sensors_parsed.ttl into http://www.phenome-fppn.fr/set/annotation
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/EventsDebutManipZA17MAU17_parsed.ttl into http://www.phenome-fppn.fr/set/annotation
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/move_ARCH2017-03-30-UPDATE-toImport_parsed.ttl into http://www.phenome-fppn.fr/set/annotation
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/sampling_za17_parsed.ttl into http://www.phenome-fppn.fr/set/annotation
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/CSVtoTurtle/toParse/turtle/silking_parsed.ttl into http://www.phenome-fppn.fr/set/annotation

# load ontologies
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/OEPO_OEEv/oeev_3.0ttl.owl into http://www.phenome-fppn.fr/vocabulary/2018/oeev
load /mnt/c/Users/lcabrera/Documents/LEPSE/PHIS/OEPO_OEEv/oepo_3.0ttl.owl into http://www.phenome-fppn.fr/vocabulary/2018/oepo

# Fix /
WITH <http://www.phenome-fppn.fr/m3p/event>
sparql
PREFIX vocabulary: <http://www.phenome-fppn.fr/vocabulary/m3p/2015#>
PREFIX event: <http://www.phenome-fppn.fr/vocabulary/m3p/2015/event#>
DELETE {?event event:to ?oldURI }
INSERT {?event event:to ?newURI }
WHERE {
  ?event event:to ?oldURI .
  BIND (URI(REPLACE(STR(?oldURI), "http://www.phenome-fppn.fr/m3p/phenoarch/", "http://www.phenome-fppn.fr/m3p/phenoarch")) AS ?newURI)
}
.

sparql
PREFIX vocabulary: <http://www.phenome-fppn.fr/vocabulary/m3p/2015#>
PREFIX event: <http://www.phenome-fppn.fr/vocabulary/m3p/2015/event#>
DELETE {?event event:from ?oldURI }
INSERT {?event event:from ?newURI }
WHERE {
  ?event event:from ?oldURI .
  BIND (URI(REPLACE(STR(?oldURI), "http://www.phenome-fppn.fr/m3p/phenoarch/", "http://www.phenome-fppn.fr/m3p/phenoarch")) AS ?newURI)
}
.