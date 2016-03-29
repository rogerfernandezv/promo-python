from hubstorage import HubstorageClient
import requests

apikey = 'ab51ccfb248b4783bc710c25ae09f8db'

hc = HubstorageClient(auth=apikey)

def listJobs():
	jobs = hc.get_project('48869').jobq.list()
	return jobs

def getItems(job):
	items = hc.get_job(job).items.list()
	return items

def getItemCsv(job):
	fields = 'cod_prom,data_prom,name,nm_prom,url_img,url_prom,valor'
	itemsCsv = requests.get('https://storage.scrapinghub.com/items/'+ job + '?apikey=' + apikey + '&format=csv&fields=' + fields)
	return itemsCsv
