
from matplotlib import pyplot as plt

from datetime import datetime as date

from collections import OrderedDict

import numpy as np

from os import listdir
from os import path
from os.path import isfile

import os

from guardarTop20 import Nodo
from guardarTop20 import RESULTS_FOLDR
from guardarTop20 import Log

#RESULTS_FOLDR = './'

def leerTodo():
	diccionarioNodos = dict()
	for file in listdir(RESULTS_FOLDR):
		try:
			dia = date.strptime(path.splitext(file)[0], '%Y-%m-%d-%H_%M_%S')
		
			listaNodos = []
			archivo = None
			archivo = open(RESULTS_FOLDR + file)
			for linea in archivo:
				datos = linea.split(';')
				listaNodos.append(Nodo(datos[0], datos[1], int(datos[2])))

			diccionarioNodos.update({dia : listaNodos})
		except ValueError as v:
			log = Log()
			log.error(v)
			log.close()
		except PermissionError as p:
			log = Log()
			log.error(p)
			log.close()

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
			if nodo.nombre == 'Unnamed':
				listaNombres.append(nodo.ip)

			elif not nodo.nombre in listaNombres:
				listaNombres.append(nodo.nombre)

	return listaNombres


def getHoras(diccionarioNodos):
	listaHoras = []
	for dia in diccionarioNodos.keys():
		listaHoras.append(dia.strftime('%H:%M'))

	return listaHoras


def getNodosPorDia(diccionarioNodos, dia):
	nodos = dict()
	diaStr = dia.strftime('%Y-%m-%d').strip()
	for k, v in diccionarioNodos.items():
		if k.strftime('%Y-%m-%d') == diaStr:
			nodos.update({k : v})

	return nodos


def getMediaAnchoPorDia(diccionarioNodos):
	#Creo un diccionario con el día como clave y como valor la lista de todos los nodos de ese día
	diccionarioDias = dict()
	indice = 0
	for dia, nodos in diccionarioNodos.items():
		if dia.strptime(dia.strftime('%Y-%m-%d'), '%Y-%m-%d') in diccionarioDias:
			diccionarioDias[dia.strptime(dia.strftime('%Y-%m-%d'), '%Y-%m-%d')].extend(nodos)
		else:
			diccionarioDias.update({dia.strptime(dia.strftime('%Y-%m-%d'), '%Y-%m-%d') : nodos})

	diccionarioMediaPorDia = dict()
	for dia, nodos in diccionarioDias.items():
		#Creo un diccionario con la IP como clave y una lista con todos los anchos de banda de esa IP
		diccionarioIPs = dict()
		for nodo in nodos:
			if nodo.ip in diccionarioIPs:
				diccionarioIPs[nodo.ip].append(nodo.ancho)
			else:
				diccionarioIPs.update({nodo.ip : [nodo.ancho]})

		#Creo un diccionario con la IP como clave y su valor es la media de los anchos de banda de esa IP
		diccionarioMediaIPs = dict()
		for ip, listaAncho in diccionarioIPs.items():
			sumaAnchos = 0
			for ancho in listaAncho:
				sumaAnchos += ancho

			mediaAncho = int(sumaAnchos / len(listaAncho))
			diccionarioMediaIPs.update({ip : mediaAncho})

		#Creo un diccionario con el día como clave y su valor es un diccionario con las IP como clave y 
		#su valor es la media de ese día de esa IP
		diccionarioMediaPorDia.update({dia : dict(sorted(diccionarioMediaIPs.items(), key=lambda x: x[1], reverse=True))})

	#Para volver a asignarle nombres a los nodos, creo un diccionario con la IP del nodo como clave y su nombre como valor
	listaIPs = []
	for IPs in list(diccionarioMediaPorDia.values()):
		for IP in IPs.keys():
			listaIPs.append(IP)

	diccionarioNombres = getNombreNodosPorIP(diccionarioNodos, listaIPs)

	#Una vez tengo los nombres de cada nodo por IP, los días, las IPs y la media de ancho de vanda diaria, creo un diccionario
	#con el día como clave y los nodos de ese día como valor
	diccionarioMedia = dict()
	for dia, diccionarioIP in diccionarioMediaPorDia.items():
		diccionarioMedia.update({dia : []})
		for ip, ancho in diccionarioIP.items():
			diccionarioMedia[dia].append(Nodo(diccionarioNombres[ip], ip, ancho))

	return diccionarioMedia


def getNombreNodosPorIP(diccionarioNodos, listaIPs):
	diccionarioNombres = dict()
	for nodos in diccionarioNodos.values():
		for nodo in nodos:
			if nodo.ip in listaIPs:
				diccionarioNombres.update({nodo.ip : nodo.nombre})

	return diccionarioNombres


def mostrarGrafica(dias, diccionarioIPs, listaNombres, xlabel, ylabel, title):
	plt.style.use('ggplot')
	indice = 0
	for v in diccionarioIPs.values():
		if indice < 5:
			plt.plot(dias, v, marker='.', label=listaNombres[indice])
		else:
			plt.plot(dias, v, marker='.')
		indice = indice + 1

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.legend()
	plt.show()


def generarGraficaGeneral():
	diccionarioNodos = leerTodo()

	diccionarioMedia = getMediaAnchoPorDia(diccionarioNodos)

	dias = getDias(diccionarioMedia)

	diccionarioIPs = crearDiccionarioIPs(diccionarioMedia)

	listaNombres = getNombreNodos(diccionarioMedia)

	mostrarGrafica(dias, diccionarioIPs, listaNombres, 'Ancho de banda (bps)', 'Día', 'Top 20 IPs con más ancho de banda')


def generarTop5():
	diccionarioNodos = leerTodo()
	
	diccionarioMediaNodos = getMediaAnchoPorDia(diccionarioNodos)

	#Calculo el total general de cada IP
	diccionarioIPTotal = dict()
	for nodos in diccionarioMediaNodos.values():
		for nodo in nodos:
			if nodo.ip in diccionarioIPTotal:
				diccionarioIPTotal[nodo.ip] += nodo.ancho
			else:
				diccionarioIPTotal.update({nodo.ip : nodo.ancho})

	#Ordeno el diccionario de manera descendente según el ancho de banda total
	diccionarioIPTotalOrdenado = dict(sorted(diccionarioIPTotal.items(), key= lambda x: x[1], reverse=True))

	#Obtengo las 5 IPs con más ancho de banda
	listaTop5IPs = []
	indice = 0
	for ip in diccionarioIPTotalOrdenado.keys():
		if indice < 5:
			listaTop5IPs.append(ip)
		indice += 1

	diccionarioTop5 = dict()
	for dia, nodos in diccionarioMediaNodos.items():
		for nodo in nodos:
			if nodo.ip in listaTop5IPs:
				if not dia in diccionarioTop5:
					diccionarioTop5.update({dia : [nodo]})
				else:
					diccionarioTop5[dia].append(nodo)

	diccionarioIPs = crearDiccionarioIPs(diccionarioTop5)
	
	dias = getDias(diccionarioTop5)
	
	listaNombres = getNombreNodos(diccionarioTop5)

	mostrarGrafica(dias, diccionarioIPs, listaNombres, 'Ancho de banda (bps)', 'Día', 'Top 5 nodos con más ancho de banda')


def generarGraficaUnDia():
	diaStr = input('Indica el día con el formato día-mes-año: ')
	dia = date.strptime(diaStr, '%d-%m-%Y')
	diccionarioNodos = leerTodo()
	nodos = getNodosPorDia(diccionarioNodos, dia)

	if len(nodos) == 0:
		print('No hay datos de el día indicado')
		return

	diccionarioIPs = crearDiccionarioIPs(nodos)

	horas = getHoras(nodos)

	listaNombres = getNombreNodos(nodos)

	mostrarGrafica(horas, diccionarioIPs, listaNombres, 'Ancho de banda (bps)', 'Hora', 
		'Ancho de banda del día ' + dia.strftime('%d/%m/%Y'))


def generarGraficaUnaIP():
	ip = input('Introduce la IP: ')
	diccionarioNodos = leerTodo()
	diccionarioMediaNodos = getMediaAnchoPorDia(diccionarioNodos)
	diccionarioIPs = crearDiccionarioIPs(diccionarioMediaNodos)

	ipSeleccionada = dict()
	for k, v in diccionarioIPs.items():
		if k == ip:
			ipSeleccionada.update({k : v})

	dias = getDias(list(diccionarioMediaNodos.keys()))

	ejeY = np.arange(len(dias))

	try:
		plt.xticks(ejeY, dias)
		plt.bar(ejeY, list(ipSeleccionada.values())[0])
		plt.ylabel('Ancho de banda (bps)')
		plt.xlabel('Día')
		plt.title('Ancho de banda de la IP: ' + list(ipSeleccionada.keys())[0])

		plt.show()
	except IndexError as e:
		log = Log()
		log.error(e)
		log.close()
		print('La IP seleccionada no existe')


seguir = True
while seguir:
	print('Elige una opción:\n1.- Gráfica general\n2.- Top 5 nodos\n3.- Gráfica de un día concreto\n' + 
		'4.- Gráfica de una IP concreta\n5.- Salir')
	eleccion = int(input(''))
	os.system('clear')
	if eleccion == 1:
		generarGraficaGeneral()
	elif eleccion == 2:
		generarTop5()
	elif eleccion == 3:
		generarGraficaUnDia()
	elif eleccion == 4:
		generarGraficaUnaIP()
	elif eleccion == 5:
		seguir = False
		print('Adios')