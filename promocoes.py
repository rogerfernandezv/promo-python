from flask import Flask
import scrapinghub_funcs
import re

app = Flask(__name__)

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
				html += i['nm_obs'] + '</td><td>'
				html += i['nm_prom'][0] + '</td><td>'
				html += '<img src="' + i['url_img'][0] + '"></td><td>'
				html += i['url_prom'][0] + '</td><td>'
				html += i['url_origem'][0] + '</td><td>'
				html += i['valor'][0] + '</td></tr>'

			html +='</table>'

	return html



if __name__ == '__main__':
	app.run()
	#app.run(host='0.0.0.0', debug=True)