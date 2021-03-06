# -*- coding: utf-8 -*-
from flask import Flask, make_response, render_template
from pymongo import MongoClient
from bson import json_util
import scrapinghub_funcs
import pymongo
import os
import re
from datetime import timedelta
from flask import request, current_app
from functools import update_wrapper

app = Flask(__name__)

#mongo stuffs OPENSHIFT
#client = MongoClient("mongodb://%s:%s/" % (os.environ['OPENSHIFT_MONGODB_DB_HOST'], os.environ['OPENSHIFT_MONGODB_DB_PORT']))
client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
db = client.promocao

# LOCAL TEST
#client = MongoClient()
#db = client.promocao

#set collection
items_collection = db.items
#result = items_collection.create_index([('cod_prom', pymongo.ASCENDING)], unique=True)


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/postsprom')
@crossdomain(origin='*')
def json_api():
	
	items_db = items_collection.find().sort("dt_criacao", -1).limit(100)
	
	response = make_response(json_util.dumps({'promos': items_db}))
	response.content_type="application/json"

	return response

@app.route('/postsprom/<post_id>')
@crossdomain(origin='*')
def json_api_id(post_id):
    
    items_db = items_collection.find_one({"cod_prom":post_id})
    response = make_response(json_util.dumps({'promos': items_db}))
    response.content_type="application/json"

    return response

@app.route('/postnew/<cod_prom>')
@crossdomain(origin='*')
def json_api_new(cod_prom):
    
    items_db = items_collection.find().sort("dt_criacao", -1).limit(100)
    
    #last = items_db[0]
    items_result = []
    if(cod_prom != items_db[0]['cod_prom']): 
        for i in items_db:
            if(cod_prom != i['cod_prom']):
                items_result.append(i)
            else:
                break

    response = make_response(json_util.dumps({'diffs': items_result, 'len': len(items_result)}))
    response.content_type="application/json"
    return response

@app.route('/postjson', methods=['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*',headers='Content-Type')
def json_resp():

    #pegando conteudo em formato json
    content = request.json
    
    #definindo variaveis
    cod_prom = content['cod_prom']
    filtros = content['filtros']
    allnotification = content['not']

    items_db = items_collection.find().sort("dt_criacao", -1).limit(100)
    
    #last = items_db[0]
    items_result = []
    items_filtered = []

    if(cod_prom != items_db[0]['cod_prom']): 
        for i in items_db:
            if(cod_prom != i['cod_prom']):
                items_result.append(i)
            else:
                break

    if len(items_result) > 0 and not allnotification and len(filtros) > 0:
        for item in items_result:
            for filtro in filtros:
                inc = re.compile(filtro['palavra'], re.I)
                exc = None
                if(filtro['excludente'] != ''):
                    exc = re.compile(filtro['excludente'], re.I)

                if exc:
                    if inc.search(item['nm_prom']) and not exc.search(item['nm_prom']):
                        items_filtered.append(item)

                else:
                    if inc.search(item['nm_prom']):
                        items_filtered.append(item)
    else:
        if allnotification:
            items_filtered = items_result

    response = make_response(json_util.dumps({'result': items_filtered}))
    response.content_type="application/json"

    return response

if __name__ == '__main__':
	app.run(debug=True)
	#app.run(host='0.0.0.0', debug="True")