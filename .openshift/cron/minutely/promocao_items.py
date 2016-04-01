from pymongo import MongoClient
import pymongo
import os
import sys
sys.path.insert(0,'../../../')
import scrapinghub_funcs

#mongo stuffs OPENSHIFT
#client = MongoClient("mongodb://%s:%s/" % (os.environ['OPENSHIFT_MONGODB_DB_HOST'], os.environ['OPENSHIFT_MONGODB_DB_PORT']))
client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
db = client.promocao

# LOCAL TEST
#client = MongoClient()
#db = client.promocoes

items_collection = db.items
result = items_collection.create_index([('cod_prom', pymongo.ASCENDING)], unique=True)

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

		#scrapinghub_funcs.deleteJob(j['key'])
