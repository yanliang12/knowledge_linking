##############yan_entity_linking.py########
import os
import re
import time
import requests

def start_entity_linker(
	dexter_folder = '.',
	):
	print('loading the entity linking models')
	os.system(u"""
		cd {}
		java -Xmx3000m -jar {}/dexter-2.1.0.jar &
		""".format(dexter_folder, dexter_folder))
	time.sleep(30)

def entity_linking(text):
	try:
		r = requests.post("http://localhost:8080/dexter-webapp/api/rest/annotate", 
			data = {
				"text":text,
				"n":50, "wn":False, "debug":False, "format":"text", "min-conf":"0.5",
			})
		entities = r.json()['spots']
		output = [{'mention':s['mention'],
			'entity_wikipage_id':str(s['entity']),
			'sentence':text,
			} for s in entities]
		return output
	except:
		return None

'''

o = entity_linking("I live at the Al Reem Island of Abu Dhabi and work in the Aldar headquarters building.")
o = entity_linking("I study at Heriot-Watt University Dubai, but I live at Abu Dhabi. I want to work at Apple. I was born in China, 1997")

for e in o:
	print(e)

'''
##############yan_entity_linking.py########