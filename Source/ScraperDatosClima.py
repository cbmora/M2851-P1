from bs4 import BeautifulSoup

urlAEMET= 'http://www.aemet.es'
urlValClima = 'http://www.aemet.es/es/serviciosclimaticos/datosclimatologicos/valoresclimatologicos'

def download(url):
	import urllib.request
	import urllib.error
	print ('Downloading:', url)  
	try:
		html = urllib.request.urlopen(url).read()
	except urllib.error.URLError as e:
		print ('Download error:', e.reason) 
		html = None
	return html
	
def EscribeFichero(ParListaValores,ParFilename,ParModo):
	import os
	import csv
	currentDir = os.path.dirname(__file__)
	FilePath = os.path.join(currentDir, ParFilename)
	with open(FilePath, ParModo, newline='') as csvFile: # Modo = w, w+
		writer = csv.writer(csvFile)
		for Valor in ParListaValores:
			writer.writerow(Valor)
			
def ObtenerComunidades(ParListaComunidades):
	html = download(urlValClima)
    #ParListaComunidades=list() # inicializamos Matriz que alojara los datos
	soup = BeautifulSoup(html,'html.parser') 
	body = soup.find('body')
	select = body.find('select')
	options = select.findAll('option')
	#print(options)
    # Recorremos option para extraer Comunidades
	for option in options:
		FilaValores=list()
		#print(option.string)
		value =option['value']   # nombre corto comunidad 
		#print('Value='+value)
		#FilaValores.append(value)
		#FilaValores.append(option.string)
		ParListaComunidades.append(value)
	  
def ObtenerEstacionesComunidad(ParListaEstaciones,ParComunidad):
	URLComunidad=urlValClima + '?k=' + ParComunidad  
	html = download(URLComunidad)
	soup = BeautifulSoup(html,'html.parser') 
	tabla = soup.find('table')
	body = tabla.find('tbody') 
	ths = body.findAll('th')
	trs= body.findAll('tr')
	# Recorremos body para extraer datos
	for tr in trs:
		FilaValores=list()
		th = tr.find('th')
		#print(th)
		a = th.find('a')
		href=a['href']   # URL, sin http://www.aemet.es 
		FilaValores.append(a.string) # Nombre de la estacion
		FilaValores.append(urlAEMET+href) # URL completo
		ParListaEstaciones.append(FilaValores)
		
def ObtenerDatosEstacion(ParDatosEstacion, ParURL,ParEstacion,ParComunidad,ParEncabezado):
	html = download(ParURL)
	#print(html)
	soup = BeautifulSoup(html,'html.parser') 
	tabla = soup.find('table')
	# Encabezado
	if ParEncabezado:
		header = tabla.find('thead') 
		ths=header.findAll('th')
		FilaValores=list()
		FilaValores.append('Comunidad')
		FilaValores.append('Estacion')
		for th in ths:
			FilaValores.append(th.string)
		ParDatosEstacion.append(FilaValores)		
	# Encabezado FIN
	
	# Recorremos body para extraer datos
	body = tabla.find('tbody') 
	ths = body.findAll('th')
	trs= body.findAll('tr')	
	for tr in trs:
		FilaValores=list()
		th = tr.find('th')
		mes = th.string
		FilaValores.append(ParComunidad)
		FilaValores.append(ParEstacion.replace(","," ")) # Sustituimos "," en nombre estacion
		FilaValores.append(mes)
		tds = tr.findAll('td')
		for td in tds:
			FilaValores.append(td.string)
		ParDatosEstacion.append(FilaValores)