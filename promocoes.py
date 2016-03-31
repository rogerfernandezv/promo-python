from flask import Flask
from flask import jsonify
import scrapinghub_funcs
import pymongo
from pymongo import MongoClient
import re
import os

app = Flask(__name__)

#mongo stuffs
#client = MongoClient()
client = MongoClient('mongodb:%s:%s/' % (os.environ['OPENSHIFT_MONGODB_DB_HOST'], os.environ['OPENSHIFT_MONGODB_DB_PORT']))
db = client.promocao
items_collection = db.items
result = items_collection.create_index([('cod_prom', pymongo.ASCENDING)], unique=True)

@app.route('/')
def hello_world():
	return 'Ola mundinho'

@app.route('/gatry')
def index():
	html = ''
	resultado = scrapinghub_funcs.listJobs()

	for j in resultado:
		if(str(j['state']) == 'finished'):
			html += '<table border="1"><tr><td>Key: ' + j['key'] + '</td><td>Status: ' + j['state'] + '</td></tr>'
			html += '''<tr>
							<td>cod_prom</td>
							<td>data_prom</td>
							<td>nm_prom</td>
							<td>url_img</td>
							<td>url_prom</td>
							<td>valor</td>
						</tr>'''
			items = scrapinghub_funcs.getItems(str(j['key']))
			for i in items:
				html += '<tr><td>'
				html += i['cod_prom'][0] + '</td><td>'
				html += i['data_prom'][0] + '</td><td>'
				html += i['nm_prom'][0] + '</td><td>'
				html += '<img src="' + i['url_img'][0] + '"></td><td>'
				html += i['url_prom'][0] + '</td><td>'
				html += i['valor'][0] + '</td></tr>'

			html +='</table>'

	return html

@app.route('/gatryjson')
def json_api():
			
	resultado = scrapinghub_funcs.listJobs()
	itemsJson = []
	for j in resultado:
		if j['state'] == 'finished':
			items = scrapinghub_funcs.getItems(j['key'])

			for i in items:
				itemsJson.append(i)

			#scrapinghub_funcs.deleteJob(j['key'])

	jobs_json = jsonify(itens=itemsJson, total=len(itemsJson))
	try:
		result = items_collection.insert_many(itemsJson)
		#print result
	except:
		print "Um ou mais items ja existiam na base"

	return jobs_json

if __name__ == '__main__':
	app.run(debug=True)
	#app.run(host='0.0.0.0', debug=True)
