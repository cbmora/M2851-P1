from bs4 import BeautifulSoup

def download(url):
	import urllib.request
	import urllib.error
	#print ('Downloading:', url)  Descomentar!!!
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
			
def ObtenerComunidades(ParListaComunidades,ParURL):
	html = download(ParURL)
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
	  
def ObtenerEstacionesComunidad(ParListaEstaciones,ParComunidad, ParURL):
	html = download(ParURL)
	#print('Aqui:'+ParURL)
	#ParListaEstaciones=list() # inicializamos Matriz que alojara los datos
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
		#print(a.string)  #  nombre de la estacion
		#print(href)
		#print(a.attrs)
		FilaValores.append(a.string)
		FilaValores.append(urlAEMET+href)
		ParListaEstaciones.append(FilaValores)
		
def ObtenerDatosEstacion(ParDatosEstacion, ParURL,ParEstacion,ParComunidad):
	html = download(ParURL)
	#print(html)
	soup = BeautifulSoup(html,'html.parser') 
	tabla = soup.find('table')
	# encabezados
	header = tabla.find('thead') 
	#print("Header==============>>>")
	#print (header) # Muestra todas los encabezados
	ths=header.findAll('th')
	FilaValores=list()
	FilaValores.append(ParEstacion)
	FilaValores.append(ParComunidad)
	for th in ths:
		#print (th.string)
		FilaValores.append(th.string)
	ParDatosEstacion.append(FilaValores)
	# encabezados FIN
	body = tabla.find('tbody') 
	ths = body.findAll('th')
	trs= body.findAll('tr')

	# Recorremos body para extraer datos
	for tr in trs:
		FilaValores=list()
		th = tr.find('th')
		#print(th)
		mes = th.string
		#print(mes)
		FilaValores.append(mes)
		tds = tr.findAll('td')
		#print (tds)
		for td in tds:
			#print (td.string)
			FilaValores.append(td.string)
		ParDatosEstacion.append(FilaValores)
		
# A continuacion lo que iria en el main
urlAEMET= 'http://www.aemet.es'
url2 = 'http://www.aemet.es/es/serviciosclimaticos/datosclimatologicos/valoresclimatologicos?l=3129&k=mad'  #borrar
url1 = 'http://www.aemet.es/es/serviciosclimaticos/datosclimatologicos/valoresclimatologicos?k=mad'#borrar
urlClima = 'http://www.aemet.es/es/serviciosclimaticos/datosclimatologicos/valoresclimatologicos'

NombreFichero = "DatosClimaNew.csv"
ListaComunidades=list()
ObtenerComunidades(ListaComunidades,urlClima) # Construimos lista de comunidades
DatosEstacion=list()
for Comunidad in ListaComunidades[1:]: #Omitimos 1er valor
	ListaEstaciones=list()
	URLComunidad=urlClima + '?k=' +Comunidad  # Revisar!!
	#print(URLComunidad)
	ObtenerEstacionesComunidad(ListaEstaciones,Comunidad, URLComunidad) # Construimos lista de estaciones de una comunidad
	for Estacion in ListaEstaciones:
		URLEstacion= Estacion[1] 
		ObtenerDatosEstacion(DatosEstacion, URLEstacion,Estacion[0],Comunidad) # Obtenemos datos climatologicos de una estacion
EscribeFichero(DatosEstacion,NombreFichero,'w')