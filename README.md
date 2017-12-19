# Semantics-and-Discourse
Project based on Neo4j

This paper talks about a question and answer system that allows natural language question to be asked of
a knowledge base of information. The questions are asked to a digital assistant like Alexa or Google Home.
We figure out various patterns in the question. Using these patterns, we write cypher queries that can fetch
answers for these questions. We use Neo4j to store data in the form of a graph. We return the answer in
the form of statements on the web interface. If the answer for the question does not exist in the database,
we return the rst two sentences of what is found regarding the question from Wikipedia.
