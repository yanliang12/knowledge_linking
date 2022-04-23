#############jim_es_vector_search.py#############

import os
import re
import csv
import time
import pandas
import hashlib
from os import listdir
from os.path import isfile, join

from elasticsearch import Elasticsearch,helpers

'''

build_vector_index(
	index_name = "logo",
	vector_fields = [{
		"vector_name":"logo_embedding",
		"vector_dim":3
		}],
	es_session = es_session,
	vector_field_name = 'logo_embedding',
	)

'''

def build_vector_index(
	index_name,
	es_session,
	vector_fields = [],
	geo_point_fields = [],
	):
	properties = {}
	for v in vector_fields:
		properties[v['vector_name']] = {"type": "dense_vector", "dims": v['vector_dim']}
	for g in geo_point_fields:
		properties[g] = {"type": "geo_point"}
	mapping_str = {
	    "settings": {
	        "number_of_shards": 10,
	        "number_of_replicas": 1
	    },
	    "mappings": {
	        "properties": properties
	    }
	}
	es_session.indices.delete(index = index_name, ignore=[400, 404])
	es_session.indices.create(index = index_name, body=mapping_str)


'''

data_body = [
	{'document_id': "logo1","logo_embedding":[1.1,2.2,3.3], "company":"google"},
	{'document_id': "logo2","logo_embedding":[4.4,5.5,6.6], "company":None},
	{'document_id': "logo3","logo_embedding":[-1.1,-2.2,-3.3], "company":"facebook"},
	]

pandas.DataFrame(data_body).to_json(
	'logo.json',
	lines = True,
	orient = 'records',
	)

ingest_json_to_es_index(
	json_file = 'logo.json',
	es_index = 'logo',
	es_session = es_session,
	document_id_feild = 'document_id',
	)

http://localhost:9466/logo/_search?pretty=true
'''

def ingest_json_to_es_index(
	json_file,
	es_index,
	es_session,
	document_id_feild = 'document_id',
	):
	data = pandas.read_json(
		json_file,
		lines = True,
		orient = "records",
		)
	def insert_record_to_es(r):
		try:
			r1 = r.to_dict()
			r1['_index'] = es_index
			r1['_id'] = r1[document_id_feild]
			helpers.bulk(es_session,[r1])
			r['status'] = 'success'
			return r
		except Exception as e:
			r['status'] = e
			return r
	data = data.apply(
		insert_record_to_es, 
		axis = 1)
	return data


'''
search_by_vector(
	index_name = 'logo',
	vector_field_name = 'logo_embedding',
	query_vector = [1.0,2.2,3.3],
	es_session = es_session,
	similarity_measure = 'euclidean',
	return_entity_max_number = 2,
	)
'''

def search_by_vector(
	index_name,
	vector_field_name,
	query_vector,
	es_session,
	similarity_measure = 'euclidean',
	return_entity_max_number = 1,
	return_entity_min_score = 0.0):
	source = "1 / (1 + l2norm(params.query_vector, '{}'))".format(vector_field_name)
	if similarity_measure == 'cosine':
		source = "cosineSimilarity(params.query_vector, '{}') + 1.0".format(vector_field_name)
	vector_dim_size = len(query_vector)
	q_str ={ 
		"size": vector_dim_size,
		"query": {
	    "script_score": {
	      "query" : {"match_all": {}},
	      "script": {
	        "source": source, 
	        "params": { "query_vector": query_vector}
	      }
	    }
	  }
	}
	res = es_session.search(
		index = index_name, 
		body = q_str,
		)
	output = [r for r in res['hits']['hits'] if r['_score'] >= return_entity_min_score]
	output = output[0:return_entity_max_number]
	output1 = []
	for r in output:
		r1 = r['_source']
		r1['score'] = r['_score']
		output1.append(r1)
	return output1

#############jim_es_vector_search.py#############