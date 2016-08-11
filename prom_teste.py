from pymongo import MongoClient
from PIL import Image
import urllib
import pymongo
import os
import scrapinghub_funcs

client = MongoClient()
db = client.promocao

items_collection = db.items
#result = items_collection.create_index([('cod_prom', pymongo.ASCENDING)], unique=True)

jobList = scrapinghub_funcs.listJobs()

for j in jobList:
	if j['state'] == 'finished':
		items = scrapinghub_funcs.getItems(j['key'])
		for i in items:
			try:
								
				result = items_collection.insert_one(i)

				print "inserindo dados no banco de dados job: " + j['key']

			except:
				print "Um ou mais items ja existiam na base ou ocorreu falha job: " + j['key'] + " item: " + i['cod_prom'][0]

