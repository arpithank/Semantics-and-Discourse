# Given a input Natural Language query,
# Identifies the matching regex and hits the neo4j graph DB with the corresponding Cypher query

import re,sys
#from neo4j.v1 import GraphDatabase, basic_auth
from py2neo import authenticate, Graph
from bs4 import BeautifulSoup
import wikipedia
#from dateutil import parser


#Reading the XML file content in to a variable
regexXML=open("QAPatterns.xml").read()

#Using BeautifulSoup to parse the loaded XML file
parsedXML=BeautifulSoup(regexXML,"lxml")

#Getting the List of regex patterns from the XML file
patternsList=[patternTag.text for patternTag in parsedXML.findAll("pattern")]

#Getting the List of corresponding Cypher query matches
cypherList=[cypherTag.text for cypherTag in parsedXML.findAll("cypher")]


#Identifies the matching regex and hits the neo4j graph DB with the corresponding Cypher query
def dataretrieve(text):
	text=text.replace("?","")
	hit_yes_no=0
	print ("Question :",text)
	authenticate("linguistic.technology:7474", "neo4j", "DtwAMjrk6zt1bHifYOJ6")
	graph = Graph("http://linguistic.technology:7474/db/data/")
	for i in range(len(patternsList)):
		match=re.match(patternsList[i],text, re.IGNORECASE)
		if match is not None:
			matchedX=list(match.groups())[-1]
			hit_yes_no=1
			print ("Match :", matchedX)
			break
	if hit_yes_no:
		cypher=cypherList[i].replace("(.*)",matchedX.replace(" ","_"))
		print("Cypher :",cypher)
		result=graph.cypher.execute(cypher)
		print (result)
		#Hits Wikipedia only for factual questions
		if len(result)==0 and i<=2:
			print ("Here is what we could find from Wikipedia!!!\n")
			result=str(wikipedia.page(matchedX).summary.encode(sys.stdout.encoding, 'ignore')).split(".")[:2]
			print (".".join(result))
	else:
		print ("No Matches found!")
	print ("-----------------------------------------------------------------------\n")

import re, sys, argparse, configparser, logging, time
from neo4j.v1 import GraphDatabase, basic_auth
# from py2neo import authenticate, Graph
from bs4 import BeautifulSoup
import wikipedia
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from SemDiscUtils import encodeReturn, decodeReturn
from defaults import MODULES, CONFFILE


MODULENAME = "QAMatchingServer"


def loadModel():
    """Loads the XML model of patterns and queries and returns the two lists."""

    # Reading the XML file content in to a variable
    # regexXML = open("QAPatterns.xml").read()
    # Using BeautifulSoup to parse the loaded XML file
    parsedXML = BeautifulSoup(open("QAPatterns.xml").read(), "lxml")

    # Getting the List of regex patterns from the XML file
    patternsList = [patternTag.text for patternTag in parsedXML.findAll("pattern")]

    # Getting the List of corresponding Cypher query matches
    cypherList = [cypherTag.text for cypherTag in parsedXML.findAll("cypher")]

    return patternsList, cypherList


def parse(text):
    """Identifies the matching regex and hits the neo4j graph DB with the corresponding Cypher query"""

    text = text.replace("?", "")
    hit_yes_no = False

    #if log:
    logging.debug("Question:" + text)
    #else:
    print("Question:", text)

    uri = "bolt://linguistic.technology:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "DtwAMjrk6zt1bHifYOJ6"))
    session = driver.session()
    # match (n) optional match (n)-[r]-() return n,r:
    # graph = Neo4J.createCypherQueries(self._edgeList)
    # authenticate("linguistic.technology:7474", "neo4j", "DtwAMjrk6zt1bHifYOJ6")
    # graph = Graph("http://linguistic.technology:7474/db/data/")

    result = ""
    matchedX = ""

    pos = 0
    for pos in range(len(patternsList)):
        match = re.match(patternsList[pos], text, re.IGNORECASE)
        if match:
            matchedX = list(match.groups())[-1]
            print("matchedX:", matchedX)
            hit_yes_no = True
            logging.debug("Match:" + matchedX)
            print("Match:", matchedX)
            break

    if hit_yes_no:
        cypher = cypherList[pos].replace("(.*)", matchedX.replace(" ", "_"))
        logging.debug("Cypher:\n" + cypher)
        print("Cypher:", cypher)
        #result = graph.cypher.execute(cypher)
        result = session.run(cypher)
        logging.debug("Result:")
        logging.debug(result)
        print("Result:", result)
        # Hits Wikipedia only for factual questions
        if not result: #  and pos <= 2:
            logging.debug("Result from Wikipedia:")
            print("Here is what we found on Wikipedia:")
            # changed code:
            #
            result = wikipedia.suggest(matchedX)
            print("Wikipedia suggests for:", matchedX)
            print(result)
            if result:
                result = str(wikipedia.page(result).summary.encode(sys.stdout.encoding, 'ignore')) # .split(".")[:2]
                print("Wikipedia:")
                print(result)
            else:
                result = wikipedia.search(matchedX)
                if result:
                    result = result[0]
                print("Wikipedia search result:")
                print(result)
            if result:
                wikipedia.page(result).summary.encode(sys.stdout.encoding, 'ignore')
            logging.debug(result)
            print(result)
    else:
        logging.debug("No Matches found!")
        print("No Matches found!")
    # close Neo4J session
    session.close()

    print("Type of result:", type(result))
    print("Test", list(result))
    for record in result:
        print("BoltStatementResult:")
        print(record["a"], record["r"], record["b"])
    logging.debug("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    print("")
    return ""

def main():
	#Sample questions
	sentence_1 ="Who is Obama?"
	sentence_2= "Who likes cherries?"
	sentence_3= "Who likes Apple?"
	sentence_4="Tell me about Peter"
	sentence_5="who is the president of united states of america?"
	parse(sentence_1)
	parse(sentence_2)
	parse(sentence_3)
	parse(sentence_4)
	parse(sentence_5)


if __name__=="__main__":
	main()