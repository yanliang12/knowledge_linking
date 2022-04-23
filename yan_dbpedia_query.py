############yan_dbpedia_query.py##############
import jessica_es

es_session = jessica_es.start_es(
	es_path = "/yan/elasticsearch_dbpedia",
	es_port_number = "9267")

'''
172.30.96.1:9267/dbpedia_triplet/_search?pretty=true
'''

def find_entity_id_and_type(
	query_wikipage_ids,
	triplets,
	):
	output = []
	for e in query_wikipage_ids:
		entity = None
		e_as_subject = list(filter(lambda t: t['subject_wikipage_id'] == e, triplets))
		if len(e_as_subject) > 0:
			entity = {'entity_wikipage_id':e}
			entity['entity_id'] = e_as_subject[0]['subject']
			entity['entity_name'] = e_as_subject[0]['subject_name']
			entity['entity_type'] = e_as_subject[0]['subject_type']
		else:
			e_as_object = list(filter(lambda t: t['object_wikipage_id'] == e, triplets))
			if len(e_as_object) > 0:
				entity = {'entity_wikipage_id':e}
				entity['entity_id'] = e_as_object[0]['object']
				entity['entity_name'] = e_as_object[0]['object_name']
				entity['entity_type'] = e_as_object[0]['object_type']
		output.append(entity)
	return output

def find_triplets_of_entities(
	query_wikipage_ids,
	skip_rdf_schema_relation = True,
	):
	triplets = []
	for query_wikipage_id in query_wikipage_ids:
		try:
			triplets += jessica_es.search_doc_by_filter(
				index_name = 'dbpedia_triplet',
				field_name = 'subject_wikipage_id',
				entity_name = query_wikipage_id,
				es_session = es_session,
				return_entity_max_number = 10000)
		except:
			pass
		try:
			triplets += jessica_es.search_doc_by_filter(
				index_name = 'dbpedia_triplet',
				field_name = 'object_wikipage_id',
				entity_name = query_wikipage_id,
				es_session = es_session,
				return_entity_max_number = 10000)
		except:
			pass
	triplets = [dict(t) for t in {tuple(d.items()) for d in triplets}]
	if skip_rdf_schema_relation is True:
		triplets = list(filter(lambda t: 'rdf-schema#' not in t['relation'], triplets))
	#print(triplets)
	return triplets


def find_top_subject_object_for_each_entity(
	query_wikipage_ids,
	triplets,
	top_triplet_number = 5,
	):
	output = []
	for e in query_wikipage_ids:
		try:
			##
			e_as_subject = list(filter(lambda t: t['subject_wikipage_id'] == e, triplets))
			e_as_subject.sort(key=lambda t: t['object_out_degree'], reverse = True)
			e_as_subject = e_as_subject[0:top_triplet_number]
			output += e_as_subject
		except:
			pass
		try:
			##
			e_as_object = list(filter(lambda t: t['object_wikipage_id'] == e, triplets))
			e_as_object.sort(key=lambda t: t['subject_out_degree'], reverse = True)
			e_as_object = e_as_object[0:top_triplet_number]
			output += e_as_object
		except:
			pass
	##
	output = [dict(t) for t in {tuple(d.items()) for d in output}]
	return output

def find_top_relations_between_entity_pairs(
	query_wikipage_ids,
	triplets,
	top_triplet_number = 3,
	):
	output = []
	for subject_wikipage_id in query_wikipage_ids:
		for object_wikipage_id in query_wikipage_ids:
			if subject_wikipage_id != object_wikipage_id:
				try:
					relation_triplet = list(filter(lambda t: 
						t['subject_wikipage_id'] == subject_wikipage_id 
						and t['object_wikipage_id'] == object_wikipage_id, triplets))
					output += relation_triplet
				except:
					pass
	output = [dict(t) for t in {tuple(d.items()) for d in output}]
	return output

def find_top_common_subject_object_of_entity_pairs(
	query_wikipage_ids,
	triplets,
	top_triplet_number = 3,
	):
	output = []
	for e1 in query_wikipage_ids:
		for e2 in query_wikipage_ids:
			if e1 < e2:
				###########
				e1_as_subject = list(filter(lambda t: 
					t['subject_wikipage_id'] == e1, triplets))
				e1_object = [
					{'object':t['object'],
					'object_out_degree':t['object_out_degree'],
					} for t in e1_as_subject]
				##
				e2_as_subject = list(filter(lambda t: 
					t['subject_wikipage_id'] == e2, triplets))
				e2_object = [
					{'object':t['object'],
					'object_out_degree':t['object_out_degree'],
					} for t in e2_as_subject]
				##
				e1_e2_common_object = [x for x in e1_object if x in e2_object]
				e1_e2_common_object.sort(key=lambda t: t['object_out_degree'], reverse = True)
				e1_e2_common_object = e1_e2_common_object[0:top_triplet_number]
				e1_e2_common_object = [t['object'] for t in e1_e2_common_object]
				###
				e1_as_subject = list(filter(lambda t: 
					t['object'] in e1_e2_common_object, e1_as_subject))
				e2_as_subject = list(filter(lambda t: 
					t['object'] in e1_e2_common_object, e2_as_subject))
				###
				output += e1_as_subject
				output += e2_as_subject
				###########
				e1_as_object = list(filter(lambda t: 
					t['object_wikipage_id'] == e1, triplets))
				e1_subject = [
					{'subject':t['subject'],
					'subject_out_degree':t['subject_out_degree'],
					} for t in e1_as_object]
				##
				e2_as_object = list(filter(lambda t: 
					t['object_wikipage_id'] == e2, triplets))
				e2_subject = [
					{'subject':t['subject'],
					'subject_out_degree':t['subject_out_degree'],
					} for t in e2_as_object]
				##
				e1_e2_common_subject = [x for x in e1_subject if x in e2_subject]
				e1_e2_common_subject.sort(key=lambda t: t['subject_out_degree'], reverse = True)
				e1_e2_common_subject = e1_e2_common_subject[0:top_triplet_number]
				e1_e2_common_subject = [t['subject'] for t in e1_e2_common_subject]
				###
				e1_as_object = list(filter(lambda t: 
					t['subject'] in e1_e2_common_subject, e1_as_object))
				e2_as_object = list(filter(lambda t: 
					t['subject'] in e1_e2_common_subject, e2_as_object))
				###
				output += e1_as_object
				output += e2_as_object
	output = [dict(t) for t in {tuple(d.items()) for d in output}]
	return output

############yan_dbpedia_query.py##############