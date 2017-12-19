import re
from nltk import pos_tag,word_tokenize
from neo4j.v1 import GraphDatabase, basic_auth
from py2neo import authenticate, Graph

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def dataretrieve(text):
    print ("Question :",text)
    authenticate("localhost:7474", "neo4j", "neo4j")
    graph = Graph("http://localhost:7474/db/data/")
    noun,verb=extraction(text)
    print(noun, verb)
    name=" ".join(noun)
    if len(verb)==0:
        str = 'MATCH (m{name:"'+name+'"})RETURN m'
        print("Cypher :",str)
        print(graph.cypher.execute(str))
        return
    if re.search(r'\bWhich\b', text) :
        #print(noun,verb)
        #name=""
        #name=noun[0]+" "+noun[1]
        verb=verb[0].upper()+"_IN"

        str = "MATCH (" + noun[
            0].lower() + ":Person{name:" + "'" + name + "'})-[:" + verb + "]" + "->(tomHanksMovies) RETURN " + noun[
                  0].lower() + "," + noun[0].lower() + noun[1] + "Movies"
        print ("Cypher :",str)
        print(graph.cypher.execute(str))
        return
    elif re.search(r'\b(?:Who)\b', text):
        #name = ""
        #name = noun[0] + " " + noun[1]
        str = "MATCH (" + noun[0].lower() + ":Person{name:" + "'" + name + "'})-[:" + "ACTED_IN" + "]" + "->(m)<-[:ACTED_IN]-("+"coActors"+") RETURN coActors.name"
        print ("Cypher :",str)
        print(graph.cypher.execute(str))
        return
    elif re.search(r'\b(?:What)\b', text):
        #print(noun, verb)
        #name = ""
        #name = noun[0] + " " + noun[1]
        verb = verb[0].upper()
        str= "MATCH (" + noun[
            0].lower() + ":Person{name:" + "'" + name + "'})-[:" + verb + "]" + "->(tomHanksMovies) RETURN " + noun[0].lower() + noun[1] + "Movies"
        print ("Cypher :",str)
        print(graph.cypher.execute(str))
        return
    else:
        "Not Found"


def extraction(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    noun = [token for token, pos in pos_tag(filtered_sentence) if pos.startswith('NNP')]
    verb=[token for token, pos in pos_tag(filtered_sentence) if pos.startswith('V')]
    return  noun,verb


def main():
    sentence_1 ="Which movie did Tom Hanks acted in"
    #sentence_2= "Who were the co-actors of  Tom Hanks movies"
    sentence_3="What movies did Tom Hanks directed"
    sentence_4="who is Tom Hanks"
    sentence_5="who acted in the movie The Da Vinci Code"
    dataretrieve(sentence_1)
    dataretrieve(sentence_3)
    dataretrieve(sentence_4)
    dataretrieve(sentence_5)
main()