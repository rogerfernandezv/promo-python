from pymongo import MongoClient
from PIL import Image
import urllib
import pymongo
import os
import scrapinghub_funcs

#mongo stuffs OPENSHIFT
#client = MongoClient("mongodb://%s:%s/" % (os.environ['OPENSHIFT_MONGODB_DB_HOST'], os.environ['OPENSHIFT_MONGODB_DB_PORT']))
client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
db = client.promocao

# LOCAL TEST
#client = MongoClient()
#db = client.promocoes
#db = client.promocao

items_collection = db.items
#result = items_collection.create_index([('cod_prom', pymongo.ASCENDING)], unique=True)

jobList = scrapinghub_funcs.listJobs()

for j in jobList:
	if j['state'] == 'finished':
		items = scrapinghub_funcs.getItems(j['key'])
		for i in items:
			try:
				url_image = 'http://promocao-rogerdev.rhcloud.com/static/images/imagenotfound.png'
				try:
					img = urllib.urlopen(i['url_img'])

					#verificando se a url funciona
					if(img.getcode() == 200):

						# nomeando e capturando dados dos links
						name = i['url_img'].split('/')[-1]
						local_img = open(os.environ['OPENSHIFT_REPO_DIR'] + 'imgs/' + name, 'w')
						local_img.write(img.read())

						#fechando dados pegos da url
						img.close()
						local_img.close()

						#tratando a imagem diminindo para 200x200 px
						im = Image.open(os.environ['OPENSHIFT_REPO_DIR'] + 'imgs/' + name)
						im.thumbnail((200,200))
						im.save(os.environ['OPENSHIFT_REPO_DIR'] + 'imgs/mini_' + name)
						im.close()

						url_image = 'http://promocao-rogerdev.rhcloud.com/static/imgs/mini_' + name

						#removendo antiga imagem
						os.remove(os.environ['OPENSHIFT_REPO_DIR'] + 'imgs/' + name)

				except:
					pass
				
				i['url_img'] = url_image
				
				result = items_collection.insert_one(i)

				print "inserindo dados no banco de dados job: " + j['key']

			except:
				print "Um ou mais items ja existiam na base ou ocorreu falha job: " + j['key'] + " item: " + i['cod_prom'][0]

		scrapinghub_funcs.deleteJob(j['key'])
