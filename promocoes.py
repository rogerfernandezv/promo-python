# -*- coding: utf-8 -*-
from flask import Flask, make_response, render_template
from pymongo import MongoClient
from bson import json_util
import scrapinghub_funcs
import pymongo
import os
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
#db = client.promocoes

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

@app.route('/teste')
def teste():
	items_db = items_collection.find().sort("dt_criacao", -1).limit(100)
	return render_template('teste.html',items_db = items_db)

@app.route('/postsprom')
@crossdomain(origin='*')
def json_api():
	
	items_db = items_collection.find().sort("dt_criacao", -1).limit(100)
	#items_db = items_collection.find_one()
	
	response = make_response(json_util.dumps({'promos': items_db}))
	response.content_type="application/json"

	return response


if __name__ == '__main__':
	app.run(debug=True)
	#app.run(host='0.0.0.0', debug="True")