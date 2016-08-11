from pymongo import MongoClient
from PIL import Image
import urllib
import pymongo
import os
import scrapinghub_funcs
import httplib
import re


#mongo stuffs OPENSHIFT
#client = MongoClient("mongodb://%s:%s/" % (os.environ['OPENSHIFT_MONGODB_DB_HOST'], os.environ['OPENSHIFT_MONGODB_DB_PORT']))
client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
db = client.promocao

# LOCAL TEST
#client = MongoClient()
#db = client.promocao

items_collection = db.items
#result = items_collection.create_index([('cod_prom', pymongo.ASCENDING)], unique=True)

jobList = scrapinghub_funcs.listJobs()

def tratar_img(name):
	#tratando a imagem diminindo para 200x200 px
	im = Image.open(os.environ['OPENSHIFT_REPO_DIR'] + 'static/imgs/' + name)
	print "Abrindo imagem para modificar..."
	im.thumbnail((200,200))
	im.save(os.environ['OPENSHIFT_REPO_DIR'] + 'static/imgs/mini_' + name)
	print "Salvando imagem modificada..."
	im.close()

	url_image = 'http://promocao-rogerdev.rhcloud.com/static/imgs/mini_' + name

	#removendo antiga imagem
	os.remove(os.environ['OPENSHIFT_REPO_DIR'] + 'static/imgs/' + name)

for j in jobList:
	if j['state'] == 'finished':
		items = scrapinghub_funcs.getItems(j['key'])
		for i in items:
			try:
				url_image = 'http://promocao-rogerdev.rhcloud.com/static/images/imagenotfound.png'
				try:
					print "tentando baixar imagem"

					img = urllib.urlopen(i['url_img'])

					#verificando se a url funciona
					if(img.getcode() == 200):
						print "imagem baixada com sucesso"
						# nomeando e capturando dados dos links
						name = i['url_img'].split('/')[-1]
						local_img = open(os.environ['OPENSHIFT_REPO_DIR'] + 'static/imgs/' + name, 'w')
						print "Imagem salva no disco..."
						local_img.write(img.read())

						#fechando dados pegos da url
						img.close()
						local_img.close()

						tratar_img(name)

					elif img.getcode() == 403:
						teste = re.compile("^(https).*")
						result = teste.match(i['url_img'])
						url_p1 = ''
						url_p2 = ''
						fname = ''
						if result:
							url_https = result.group(0)
							url_p1 = re.sub(r'^(https://)','',result.group(0))
							url_p1 = re.sub(r'\/.*','',url_p1)
							url_p2 = re.sub(r'.*\.com\.br','',result.group(0))
							print "url_p1: " + url_p1
							print "url_p2: " + url_p2
							print "result: " + result.group(0)
							
							fname = re.sub(r'.*\/','',result.group(0))

							conn = httplib.HTTPSConnection(url_p1)
							conn.request("GET",url_p2)
							r1 = conn.getresponse()
							print r1.status, r1.reason
							if r1.status == 200 and r1.reason == 'OK':
								data1 = r1.read()
								with open(os.environ['OPENSHIFT_REPO_DIR'] + 'static/imgs/' + fname,"w") as f:
								  f.write(data1)

								tratar_img(fname)

				except IOError:
					print 'Arquivo ou Diretorio nao encontrado!'
				except:
					print 'Erro inesperado'
				
				i['url_img'] = url_image
				
				result = items_collection.insert_one(i)

				print "inserindo dados no banco de dados job: " + j['key']

			except:
				print "Um ou mais items ja existiam na base ou ocorreu falha job: " + j['key'] + " item: " + i['cod_prom'][0]

		scrapinghub_funcs.deleteJob(j['key'])
