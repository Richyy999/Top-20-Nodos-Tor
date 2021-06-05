
from matplotlib import pyplot as plt
from datetime import datetime as date
from collections import OrderedDict
from os import listdir
from os import path
from os.path import isfile

from guardarTop20 import Nodo
from guardarTop20 import RESULTS_FOLDR

def leerTodo():
	diccionarioNodos = dict()
	for file in listdir(RESULTS_FOLDR):
		dia = date.strptime(path.splitext(file)[0], '%Y-%m-%d-%H_%M_%S')
		
		listaNodos = []
		archivo = open(RESULTS_FOLDR + file)
		for linea in archivo:
			datos = linea.split(';')
			listaNodos.append(Nodo(datos[0], datos[1], int(datos[2])))

		diccionarioNodos.update({dia : listaNodos})

	nodosOrdenados = OrderedDict(sorted(diccionarioNodos.items()))

	return nodosOrdenados

def crearDiccionarioIPs(diccionarioNodos):
	#Crear un diccionario con las IPs como clave para obtener los valores del eje y de la gráfica
	diccionarioIPs = dict()
	for nodos in diccionarioNodos.values():
		for nodo in nodos:
			if nodo.ip in diccionarioIPs:
				diccionarioIPs[nodo.ip].append(nodo.ancho)
			else:
				diccionarioIPs.update({nodo.ip : [nodo.ancho]})

	#Actualizar la lista de las IPs para que en caso de que algún nodo que no aparezca algún día tenga un ancho de banda de 0
	for i in range(len(diccionarioNodos.values())):
		listaNodos = list(diccionarioNodos.values())[i]
		listaIps = []
		for nodo in listaNodos:
			listaIps.append(nodo.ip)

		for k, v in diccionarioIPs.items():
			if not k in listaIps:
				v.insert(i, 0)
		
	return diccionarioIPs

def getDias(listaDias):
	dias = []
	for diaSinFormato in listaDias:
		dia = diaSinFormato.strftime('%d/%m')

		dias.append(dia)

	return dias

def getNombreNodos(diccionarioNodos):
	listaNombres = []
	for nodos in diccionarioNodos.values():
		for nodo in nodos:
			if not nodo.nombre in listaNombres:
				listaNombres.append(nodo.nombre)

	return listaNombres

def getHoras(diccionarioNodos):
	listaHoras = []
	for dia in diccionarioNodos.keys():
		listaHoras.append(dia.strftime('%H:%M'))

	return listaHoras

def getNodosPorDia(diccionarioNodos, dia):
	nodos = dict()
	diaStr = dia.strftime('%Y-%m-%d')
	for k, v in diccionarioNodos.items():
		if k.strftime('%Y-%m-%d') == diaStr:
			nodos.update({k : v})

	return nodos



def generarGraficaGeneral():
	diccionarioNodos = leerTodo()
		
	diccionarioIps = crearDiccionarioIPs(diccionarioNodos)

	dias = getDias(list(diccionarioNodos.keys()))

	plt.style.use('ggplot')

	indice = 0
	for v in diccionarioIps.values():
		if indice < 6:
			plt.plot(dias, v, marker='.', label=(list(diccionarioIps.keys())[indice]))
		else:
			plt.plot(dias, v, marker='.')
		indice = indice + 1

	plt.ylabel('Ancho de banda')
	plt.xlabel('Días')
	plt.title('Top 20 IPs con más ancho de banda')
	plt.legend()
	plt.show()

def generarTop5():
	diccionarioNodos = leerTodo()
	diccionarioNodosFiltrado = dict()

	indice = 0
	for k, v in diccionarioNodos.items():
		if indice < 6:
			diccionarioNodosFiltrado.update({k : v})
		indice = indice + 1

	diccionarioIPs = crearDiccionarioIPs(diccionarioNodosFiltrado)
	
	listaNombres = getNombreNodos(diccionarioNodosFiltrado)

	dias = getDias(list(diccionarioNodosFiltrado.keys()))

	plt.style.use('ggplot')

	indice = 0
	for v in diccionarioIPs.values():
		plt.plot(dias, v, marker='.', label=listaNombres[indice])
		indice = indice + 1

	plt.ylabel('Ancho de banda')
	plt.xlabel('Días')
	plt.title('Top 5 nodos con más ancho de banda')
	plt.legend()
	plt.show()

def generarGraficaUnDia():
	diaStr = input('Indica el día con el formato día-mes-año:')
	dia = date.strptime(diaStr, '%d-%m-%Y')
	diccionarioNodos = leerTodo()
	nodos = getNodosPorDia(diccionarioNodos, dia)

	diccionarioIPs = crearDiccionarioIPs(nodos)

	horas = getHoras(nodos)

	plt.style.use('ggplot')

	indice = 0
	for v in diccionarioIPs.values():
		if indice < 6:
			plt.plot(horas, v, marker='.', label=(list(diccionarioIPs.keys())[indice]))
		else:
			plt.plot(horas, v, marker='.')
		indice = indice + 1

	plt.ylabel('Ancho de banda')
	plt.xlabel('Horas')
	plt.title('Ancho de banda del día ' + dia.strftime('%d/%m/%Y'))
	plt.legend()
	plt.show()


#generarGraficaGeneral()
#generarTop5()
#generarGraficaUnDia()

seguir = True
while seguir:
	print('Elige una opción:\n1.- Gráfica general\n2.- Top 5 nodos\n3.- Gráfica de un día concreto\n4.- Salir')
	eleccion = int(input(''))

	if eleccion == 1:
		generarGraficaGeneral()
	elif eleccion == 2:
		generarTop5()
	elif eleccion == 3:
		generarGraficaUnDia()
	elif eleccion == 4:
		seguir = False
		print('Adios')