import  ScraperDatosClima 

NombreFichero = "DatosClimaEsp.csv"
ListaComunidades=list()
Encabezado=True

ScraperDatosClima.ObtenerComunidades(ListaComunidades) # Construimos lista de comunidades
DatosEstaciones=list()
for Comunidad in ListaComunidades[1:]: # Omitimos 1er valor 0
	ListaEstaciones=list()
	ScraperDatosClima.ObtenerEstacionesComunidad(ListaEstaciones,Comunidad) # Construimos lista de estaciones de una comunidad
	for Estacion in ListaEstaciones: # Estacion[0]= Nombre Estacion, Estacion[1]= URl estacion
		URLEstacion= Estacion[1] 
		ScraperDatosClima.ObtenerDatosEstacion(DatosEstaciones, URLEstacion,Estacion[0],Comunidad,Encabezado) # Obtenemos datos climatologicos de una estacion
		Encabezado=False
ScraperDatosClima.EscribeFichero(DatosEstaciones,NombreFichero,'w')