###########yan_text_kg_enrichment.py############
import hashlib
import yan_neo4j
import yan_dbpedia_query
import yan_entity_linking

md5 = lambda x: hashlib.md5(x.encode()).hexdigest()

yan_neo4j.start_neo4j(
	http_port = "5974", 
	bolt_port = "3097",
	neo4j_path = '/yan/')

neo4j_session = yan_neo4j.create_neo4j_session(bolt_port = "3097")

def text_knowledge_enrichment(
	text,
	):
	'''
	entity linking
	'''
	mentions = yan_entity_linking.entity_linking(text)
	'''
	find the entity wikipage id
	'''
	query_wikipage_ids = [e['entity_wikipage_id'] for e in mentions]
	##
	'''
	find all the related triplets by subject or object
	'''
	triplets = yan_dbpedia_query.find_triplets_of_entities(
		query_wikipage_ids,
		skip_rdf_schema_relation = False,
		)
	'''
	build the triplets between the sentence and the linked entities
	'''
	###
	entity_name_type = yan_dbpedia_query.find_entity_id_and_type(
		query_wikipage_ids,
		triplets,
		)
	###
	mention_triplet = []
	for m in mentions:
		try:
			entity_name_type1 = list(filter(lambda t: t['entity_wikipage_id'] == m['entity_wikipage_id'], entity_name_type))[0]
			t = {
				'subject':md5(m['sentence']),
				'subject_type':'Sentence',
				'subject_name':m['sentence'],
				'relation':'mention',
				'object':entity_name_type1['entity_id'],
				'object_type':entity_name_type1['entity_type'],
				'object_name':entity_name_type1['entity_name'],
			}
			mention_triplet.append(t)
		except:
			pass
	###
	'''
	qeury triplets from the es queried triplets
	'''
	top_subject_object_triplets = yan_dbpedia_query.find_top_subject_object_for_each_entity(
		query_wikipage_ids,
		triplets,
		top_triplet_number = 5,
		)
	top_between_relation_tripltes = yan_dbpedia_query.find_top_relations_between_entity_pairs(
		query_wikipage_ids,
		triplets,
		top_triplet_number = 2,
		)
	top_common_subject_object_tripltes = yan_dbpedia_query.find_top_common_subject_object_of_entity_pairs(
		query_wikipage_ids,
		triplets,
		top_triplet_number = 4,
		)
	neo4j_triplets = top_common_subject_object_tripltes + top_subject_object_triplets + top_between_relation_tripltes + mention_triplet
	'''
	ingest to neo4j
	'''
	yan_neo4j.ingest_knowledge_triplets_to_neo4j(
		neo4j_triplets, 
		neo4j_session)

###########yan_text_kg_enrichment.py############