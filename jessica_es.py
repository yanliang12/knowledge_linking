###########jessica_es.py###########
import os
import re
import csv
import time
import pandas
import hashlib
from os import listdir
from os.path import isfile, join

from elasticsearch import *

def value_is_none(value):
	try:
		if value is None:
			return True
	except:
		pass
	try:
		if pandas.isna(value):
			return True
	except:
		pass
	return False

def start_es(
	es_path = "/jessica/elasticsearch-6.7.1",
	es_port_number = "9466"):
	'''
	check if es service is already running
	if yes, return the session
	'''
	if os.system(u"""
		curl -XPUT -H "Content-Type: application/json" http://localhost:%s/_cluster/settings -d '{ "transient": { "cluster.routing.allocation.disk.threshold_enabled": false } }'
		curl -XPUT -H "Content-Type: application/json" http://localhost:%s/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'
		"""%(es_port_number,
			es_port_number
			)) == 0:
		return Elasticsearch([{'host':'localhost','port':int(es_port_number)}])
	###
	'''
	if not running, start the service
	firstly overwrit the configuration file
	'''
	os.system(u"""
	rm %s/config/elasticsearch.yml
	echo "transport.host: localhost " > %s/config/elasticsearch.yml
	echo "transport.tcp.port: 9300 " >> %s/config/elasticsearch.yml
	echo "http.port: %s" >> %s/config/elasticsearch.yml
	echo "network.host: 0.0.0.0" >> %s/config/elasticsearch.yml
	"""%(es_path,
		es_path,
		es_path,
		es_port_number,
		es_path,
		es_path))
	'''
	the start the docker service
	'''
	os.system(u"""
		%s/bin/elasticsearch &
		"""%(es_path))
	'''
	keeps checking if es is up, if up return the session
	otherwise keeps checking, until 100K times
	'''
	try_time = 0
	while(try_time <= 100):
		try_time += 1
		if os.system(u"""
			curl -XPUT -H "Content-Type: application/json" http://localhost:%s/_cluster/settings -d '{ "transient": { "cluster.routing.allocation.disk.threshold_enabled": false } }'
			curl -XPUT -H "Content-Type: application/json" http://localhost:%s/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'
			"""%(es_port_number,
				es_port_number
				)) == 0:
			return Elasticsearch([{'host':'localhost','port':int(es_port_number)}])
		else:
			time.sleep(10)
	return None

def insert_doc_to_es(
	es_session,
	es_index,
	doc_dict,
	doc_id = None):
	try:
		if doc_id is None:
			doc_id = hashlib.md5(str(doc_dict).encode()).hexdigest()
		result = es_session.index(
			index = es_index,
			doc_type='doc',
			id = doc_id,
			body = doc_dict)
	except Exception as e:
		print(e)

def search_doc_by_match(
	index_name,
	entity_name,
	field_name,
	es_session,
	return_entity_max_number = 1,
	return_entity_min_score = 5.0):
	try:
		res = es_session.search(
			index = index_name,
			body={'query':{'match':{ field_name: entity_name}}})
		output = [r for r in res['hits']['hits'] if r['_score'] >= return_entity_min_score]
		output = output[0:return_entity_max_number]
		output1 = []
		for r in output:
			r1 = r['_source']
			r1['score'] = r['_score']
			output1.append(r1)
		return output1
	except:
		return None

def search_doc_by_filter(
	index_name,
	field_name,
	entity_name,
	es_session,
	return_entity_max_number = 100):
	triplet_query_body = {
		"size": return_entity_max_number, 
		"query": { 
			"bool": { 
				"filter": { "term":  { field_name : entity_name }}      
			}
		}
	}
	res = es_session.search(
		index = index_name,
		body = triplet_query_body)
	return [r['_source'] for r in res['hits']['hits']]

def start_kibana(
	kibana_port_number = "5145",
	es_port_number = "9466",
	):
	try:
		'''
		set the configuration file
		'''
		os.system(u"""
		rm /jessica/kibana-6.7.1-linux-x86_64/config/kibana.yml
		echo "server.port: %s" > /jessica/kibana-6.7.1-linux-x86_64/config/kibana.yml
		echo "server.host: \"0.0.0.0\"" >> /jessica/kibana-6.7.1-linux-x86_64/config/kibana.yml
		echo "elasticsearch.hosts: [\"http://localhost:%s\"]" >> /jessica/kibana-6.7.1-linux-x86_64/config/kibana.yml
		"""%(kibana_port_number,
		es_port_number))
		'''
		start the service
		'''
		os.system(u"""
			/jessica/kibana-6.7.1-linux-x86_64/bin/kibana &
			""")
		return 'success'
	except Exception as e:
		return str(e)

'''
ingest a json file's data to a index

es_session = start_es(
	es_path = "/jessica/elasticsearch-6.7.1",
	es_port_number = "9466")


ingest_json_to_es_index(
	json_file = '/Downloads/data_sample.json',
	es_index = "customers",
	es_session = es_session,
	document_id_feild = 'CustomerName',
	)

http://192.168.1.114:9466/customers/_search?pretty=true

'''

def ingest_json_to_es_index(
	json_file,
	es_index,
	es_session,
	document_id_feild = 'document_id',
	check_value_is_none = True,
	):
	data = pandas.read_json(
		json_file,
		lines = True,
		orient = "records",
		)
	def insert_record_to_es(r):
		try:
			r1 = r.to_dict()
			if check_value_is_none is True:
				r1 = {k: v for k, v in r1.items() if value_is_none(v) is False}
			result = insert_doc_to_es(
				es_session,
				es_index = es_index,
				doc_dict = r1,
				doc_id = r1[document_id_feild])
			r['status'] = 'success'
			return r
		except Exception as e:
			r['status'] = e
			return r
	data = data.apply(
		insert_record_to_es, 
		axis = 1)
	return data

def start_kibana(
	kibana_path = '/jessica/kibana-6.7.1-linux-x86_64',
	kibana_port_number = "5145",
	es_port_number = "9466",
	):
	try:
		'''
		set the configuration file
		'''
		os.system(u"""
		rm %s/config/kibana.yml
		echo "server.port: %s" > %s/config/kibana.yml
		echo "server.host: \"0.0.0.0\"" >> %s/config/kibana.yml
		echo "elasticsearch.hosts: [\"http://localhost:%s\"]" >> %s/config/kibana.yml
		"""%(
		kibana_path,
		kibana_port_number,
		kibana_path,
		kibana_path,
		es_port_number,
		kibana_path
		))
		'''
		start the service
		'''
		os.system(u"""
			%s/bin/kibana &
			"""%(kibana_path))
		return 'success'
	except Exception as e:
		return str(e)


'''
ingest the json files of a folder of folders, the folder is the output of spark writh repartioned to 
each record each file
'''

def ingest_partitioned_json_to_es(
	es_data_json_path,
	index_name,
	es_session,
	document_id_feild = "document_id",
	):
	'''
	find all the sub folders
	'''
	es_folders = listdir(es_data_json_path) 
	es_folders = ['%s/%s'%(es_data_json_path,f) for f in es_folders]
	####
	'''
	find all the json files
	'''
	files = []
	for e in es_folders:
		try:
			files += [join(e, f) 
				for f in listdir(e) 
				if isfile(join(e, f))
				and bool(re.search(r'.+\.json$', f))]
		except:
			pass
	####
	'''
	ingest each json file to the index
	'''
	for f in files:
		try:
			df = ingest_json_to_es_index(
				json_file = f,
				es_index = index_name,
				es_session = es_session,
				document_id_feild = document_id_feild,
				)
		except Exception as e:
			print(e)

###########jessica_es.py###########