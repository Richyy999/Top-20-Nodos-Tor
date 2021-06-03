from datetime import datetime as date
import os
import time

class Nodo():
	
	def __init__(self, nombre, ip, ancho):
		self.nombre = nombre
		self.ip = ip
		self.ancho = ancho

class Log():
    
    def __init__(self):
        carpeta = "./log/"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        
        logName = "error.log"
        
        self.log = open(carpeta + logName, "a")
    
    def error(self, error):
        hora = date.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.log.write(hora + ":\n" + str(error) + "\n")
    
    def close(self):
        self.log.write("\n")
        self.log.close()

def leer():
    archivo = open("/var/lib/tor/cached-microdesc-consensus")
    listaNodos = []
    
    log = Log()
    
    ip = None
    nombre = None
    ancho = None
    
    for linea in archivo:
        linea.strip()
        
        if linea.startswith("r"):
            router = linea.split(" ")
            try:
                ip = router[5]
                nombre = router[1]
            except IndexError as e:
                ip = None
                nombre = None
                log.error(e)
            
        if linea.startswith("w"):
            try:
                ancho = int(linea.replace("w Bandwidth=", ""))
            except ValueError as e:
                ancho = None
                log.error(e)
        
        if ip != None and nombre != None and ancho != None:
            listaNodos.append(Nodo(nombre, ip, ancho))
            ip = None
            nombre = None
            ancho = None
    
    log.close()
    archivo.close()

    listaNodos.sort(key=lambda x: x.ancho, reverse = True)
    
    top20 = []
    
    for i in range(20):
        nodo = listaNodos[i]
        top20.append(nodo)
        print(nodo.nombre + " " + nodo.ip + " " + str(nodo.ancho))
    
    print("Total de nodos: " + str(len(listaNodos)))
    
    carpeta = "./results/"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    hora = date.today().strftime('%Y-%m-%d-%H:%M:%S')

    archivoTop20 = open(carpeta + "{}.csv".format(hora), "w")

    separador = ";"

    for nodo in top20:
        archivoTop20.write(nodo.nombre + separador + nodo.ip + separador + str(nodo.ancho) + "\n")
    
    
    print("Guardado en: " + archivoTop20.name)
    
    archivoTop20.close()


if __name__=="__main__":
    numVueltas = 0
    while numVueltas < 1:
        try:
            leer()
            #time.sleep(15*60)
            numVueltas = numVueltas + 1
        except PermissionError:
            print("Se requiere ejecución con sudo")
            break