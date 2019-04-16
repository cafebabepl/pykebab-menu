from flask import Flask, json, jsonify
from config import config
from scrapinghub import ScrapinghubClient

app = Flask(__name__)

@app.route('/')
def index():
    return 'To jest mikrousluga, ktora zwraca menu!'

@app.route('/about')
def about():
	return 'pykebab-menu (kebab 2.1)'

@app.route('/menu')
def menu():
	client = ScrapinghubClient(config['scrapinghub']['api_key'])
	project = client.get_project(config['scrapinghub']['project_id'])
	job = project.jobs.list(spider=config['scrapinghub']['spider_name'], state='finished', count=1)[0]
	job = client.get_job(job['key'])

	menu = {}
	menu['aktualnosc'] = job.metadata.get('finished_time')
	menu['restauracja'] = {
		"nazwa": "CamelPizza",
		"logo": "https://www.camelpizza.pl/system/logos/27323/menu_size/1549450693.png",
		"url": "http://camelpizza.pl"
	}
	menu['grupy'] = []

	def get_grupa(item):
		for grupa in menu['grupy']:
			if grupa['nazwa'] == item['grupa']:
				return grupa
		grupa = { 'nazwa': item['grupa'], 'pozycje': [] }
		menu['grupy'].append(grupa)
		return grupa

	def get_pozycja(item):
		grupa = get_grupa(item)
		for pozycja in grupa['pozycje']:
			if pozycja['nazwa'] == item['pozycja']:
				return pozycja
		pozycja = { 'nazwa': item['pozycja'], 'opis': item['opis'], 'warianty': [] }
		grupa['pozycje'].append(pozycja)
		return pozycja

	def get_cena(item):
		kwota, waluta = item['cena'].replace(u'zł', u' zł').split()
		kwota = float(kwota.replace(',', '.'))
		waluta = waluta.replace(u'zł', 'PLN')
		return { 'kwota': kwota, 'waluta': waluta }

	items = job.items.list()
	for item in items:
		pozycja = get_pozycja(item)
		wariant = { 'opis': item['wariant'], 'ceny': [ get_cena(item) ]}
		pozycja['warianty'].append(wariant)

	return jsonify(menu)
	#return json.dumps(menu), 200, 'application/json'
	#return app.response_class(response=json.dumps(menu), status=200, mimetype='application/json')