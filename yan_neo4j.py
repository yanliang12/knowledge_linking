#######yan_neo4j.py#######
import os
import time
from neo4j import *

def start_neo4j(
	http_port, 
	bolt_port,
	neo4j_path = '/'):
	###
	os.system(u"""
	rm %sneo4j-community-3.5.12/conf/neo4j.conf
	echo "dbms.security.auth_enabled=false" > %sneo4j-community-3.5.12/conf/neo4j.conf
	echo "dbms.connectors.default_listen_address=0.0.0.0" >> %sneo4j-community-3.5.12/conf/neo4j.conf
	echo "dbms.connector.http.enabled=true" >> %sneo4j-community-3.5.12/conf/neo4j.conf
	echo "dbms.connector.http.address=0.0.0.0:%s" >> %sneo4j-community-3.5.12/conf/neo4j.conf
	echo "dbms.connector.bolt.enabled=true" >> %sneo4j-community-3.5.12/conf/neo4j.conf
	echo "dbms.connector.bolt.address=0.0.0.0:%s" >> %sneo4j-community-3.5.12/conf/neo4j.conf
	"""%(
		neo4j_path,
		neo4j_path,
		neo4j_path,
		neo4j_path,		
		http_port,
		neo4j_path,		
		neo4j_path,	
		bolt_port,
		neo4j_path))
	####
	os.system(u"""
	rm %sneo4j-community-3.5.12/data/dbms/auth
	%sneo4j-community-3.5.12/bin/neo4j-admin set-initial-password neo4j1
	"""%(neo4j_path,
		neo4j_path))
	####
	os.system(u"""
	%sneo4j-community-3.5.12/bin/neo4j start
	"""%(neo4j_path))
	####

def create_neo4j_session(bolt_port):
	while(True):
		try:
			neo4j_instance = GraphDatabase.driver("bolt://0.0.0.0:%s/"%(bolt_port), auth=('neo4j', 'neo4j1'))
			neo4j_session = neo4j_instance.session()
			break
		except:
			pass
	return neo4j_session

def ingest_knowledge_triplets_to_neo4j(
	triplets,
	neo4j_session,
	delete_data = True):
	if delete_data is True:
		neo4j_session.run(u"""
		MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r;
		""")
	#######
	unique_entities = list({item["entity_id"]: item for item in [{'entity_id': t['subject'], 
		'entity_type': t['subject_type'], 
		'entity_name': t['subject_name']} 
		for t in triplets] \
		+ [{'entity_id': t['object'], 
		'entity_type': t['object_type'], 
		'entity_name': t['object_name']} 
		for t in triplets]}.values())
	for e in unique_entities:
		try:
			neo4j_session.run(u"""
			MERGE (n:%s { value: '%s', id: '%s' });
			"""%(e['entity_type'], e['entity_name'], e['entity_id']))
		except:
			pass
	#####
	for t in triplets:
		try:
			neo4j_session.run(
			u"""
			MATCH (a:%s),(b:%s) WHERE a.id = '%s' AND b.id = '%s' 
			MERGE (a)-[r:%s]->(b);
			"""%(t['subject_type'], t['object_type'], 
				t['subject'], t['object'], 
				t['relation']))
		except:
			pass

'''
from yan_neo4j import start_neo4j
from yan_neo4j import create_neo4j_session
from yan_neo4j import ingest_knowledge_triplets_to_neo4j

start_neo4j(http_port = "5967", bolt_port = "3577")
neo4j_session = create_neo4j_session(bolt_port = "3577")

t = [{
'subject':"a",
'subject_type':"b",
'subject_name':"c",
'object':"d",
'object_type':"e",
'object_name':"f",
'relation':"g",
}]
ingest_knowledge_triplets_to_neo4j(t, neo4j_session)

# neo4j: http://0.0.0.0:5967/
'''
#######yan_neo4j.py#######