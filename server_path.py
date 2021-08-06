######server_path.py########
import time
import logging
import argsparser
from flask_restplus import *
from flask import *

import yan_text_kg_enrichment

ns = Namespace('text_kg_enrichment', description='')
args = argsparser.prepare_args()

parser = ns.parser()
parser.add_argument('text', type=str, location='json')

req_fields = {'text': fields.String(\
	example = u"I graduated from UC Berkeley, and worked for Google for a while. Later I am an engineer at Apple. Now I live in San Jose.")\
	}
yan_api_req = ns.model('yan', req_fields)

rsp_fields = {\
	'status':fields.String,\
	'running_time':fields.Float\
	}

yan_api_rsp = ns.model('text_kg_enrichment', rsp_fields)

@ns.route('')
class yan_api(Resource):
	def __init__(self, *args, **kwargs):
		super(yan_api, self).__init__(*args, **kwargs)
	@ns.marshal_with(yan_api_rsp)
	@ns.expect(yan_api_req)
	def post(self):		
		start = time.time()
		output = {}
		try:			
			args = parser.parse_args()		
			yan_text_kg_enrichment.text_knowledge_enrichment(
				args['text'],
				)
			output['status'] = 'success'
			output['running_time'] = float(time.time()- start)
			return output, 200
		except Exception as e:
			output['status'] = str(e)
			output['running_time'] = float(time.time()- start)
			return output

######server_path.py########