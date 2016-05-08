# -*- coding: utf-8 -*-
from flask import Flask, make_response, render_template
from pymongo import MongoClient
from bson import json_util
import scrapinghub_funcs
import pymongo
import os


app = Flask(__name__)

#mongo stuffs OPENSHIFT
#client = MongoClient("mongodb://%s:%s/" % (os.environ['OPENSHIFT_MONGODB_DB_HOST'], os.environ['OPENSHIFT_MONGODB_DB_PORT']))
client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
db = client.promocao

# LOCAL TEST
#client = MongoClient()
#db = client.promocoes

#set collection
items_collection = db.items
#result = items_collection.create_index([('cod_prom', pymongo.ASCENDING)], unique=True)

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/teste')
def teste():
	items_db = items_collection.find().sort("dt_criacao", -1).limit(40)
	return render_template('teste.html',items_db = items_db)

@app.route('/promojson')
def json_api():
	
	items_db = items_collection.find().sort("dt_criacao", -1).limit(40)
	#items_db = items_collection.find_one()

	response = make_response(json_util.dumps({'promos': items_db}))
	response.content_type="application/json"
	#response.headers.add('Access-Control-Allow-Origin', '*')
  	#response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  	#response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')

	return response

@app.route('/old')
def old():
	html = ''
	items_db = items_collection.find().sort("dt_criacao", -1).limit(40)
	for i in items_db:
		html += '<table border="1">'
		html += '''<tr>
					<td>cod_prom</td>
					<td>data_prom</td>
					<td>nm_prom</td>
					<td>url_img</td>
					<td>url_prom</td>
					<td>url_origem</td>
					<td>valor</td>
					<td>nm_obs</td>
					<td>dt_criacao<td>
				</tr>'''
		html += '<tr><td>'

		if(isinstance(i['cod_prom'],list)):
			html += i['cod_prom'][0] + '</td><td>'
		else:
			html += i['cod_prom'] + '</td><td>'

		html += i['data_prom'] + '</td><td>'
		html += i['nm_prom'] + '</td><td>'
		if(i['url_img']):
			html += '<img src="' + i['url_img'] + '"></td><td>'
		else:
			html += 'null</td><td>'

		if(isinstance(i['url_prom'],list)):
			for u in i['url_prom']:
				html += '<a href="' + u + '">LINK</a><br>'
			html += '</td><td>'
		else:
			html += '<a href="' + i['url_prom'] + '">LINK</a></td><td>'
		html += i['url_origem'] + '</td><td>'

		if(i['valor']):
			html += i['valor'] + '</td><td>'
		else:
			html +='</td><td>'

		if(i['nm_obs']):
			html += i['nm_obs'] + '</td><td>'
		else:
			html +='</td><td>'

		if('dt_criacao' in i):
			html += i['dt_criacao'] + '</td></tr>'
		else:
			html += '</td></tr>'

	html +='</table>'


	return html


if __name__ == '__main__':
	app.run(debug=True)
	#app.run(host='0.0.0.0', debug="True")