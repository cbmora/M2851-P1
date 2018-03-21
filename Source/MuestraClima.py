# Ejecuta OK
# https://www.manejandodatos.es/2014/02/trabajando-con-beautifulsoup-en-python/
import urllib.request # antes import urllib2
import urllib.error
def download(url):
	print ('Downloading:', url) # CBM: agregado (
	try:
		html = urllib.request.urlopen(url).read()
	except urllib.error.URLError as e:
		print ('Download error:', e.reason) # CBM: agregado (
		html = None
	return html

from bs4 import BeautifulSoup

url = 'http://www.aemet.es/es/serviciosclimaticos/datosclimatologicos/valoresclimatologicos?l=3129&k=mad'
html = download(url)
#print(html)
soup = BeautifulSoup(html,'lxml') # CBM: agrego lxml para que no de warning
# locate the area row
tabla = soup.find('table')
#print (tabla)  # Muestra Tabla
body = tabla.find('tbody') # locate the area tag
#print (body) # Muestra todas filas
ths = body.findAll('th')
print(ths) # Muestra todos encabezados