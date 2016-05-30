import socket
import sys
import threading

#Memory Unit Class, It's the core of the shared memory system
class MU:

	def __init__(self):
		self.name = ""
		self.datatype = ""
		self.content = ""
		self.permissions = ""
		self.owner = ""
		self.accesses = []
		self.restrictions = []

	#Returns the content to the user which asked for it, depending on the permissions granted for "who"
	def read(self, who):
		if who != self.owner:
			if ((self.permissions == "1110") or (self.permissions == "1011") or (self.permissions == "1010")):
				return self.content
			else:
				print "No permissions granted for this Memory Unit"
		else:
			return self.content

	#Changes the content of the MU depending on the permissions granted for "who"
	def write(self, who, datatype, content):
		if who != self.owner:
			if ((self.permissions == "1011") or (self.permissions == "1111")):
				self.content = content
			else:
				print "No permissions granted for this Memory Unit"
		else:
			if ((self.permissions == "1100") or (self.permissions == "1110") or (self.permissions == "1111")):
				self.content = content
			else:
				print "I have no permissions to write this Memory Unit"

	#Changes the permissions for the MU
	def chmod(self, who, newPermissions):
		if who == self.owner:
			self.permissions = newPermissions
		else:
			print "You don't have enough rights to do this!"

#-------------------------------------------------------------------------------------------

# Definicion de Variables Globales
_MEMORYSIZE = 4 											#Un maximo de 4 bloques
peerSocket = "" 											#Socket Handler
HOST = ''													#Host IP info 
PORT = 10000												#Host Port info
servData = (HOST,PORT)										#Tuple with Host Information, useful for the "UDP sending code" reading

# La memoria es un diccionario de Unidades de Memoria (MU)
memory = {}

def listeningThread():
	while True:
		recieved, server = peerSocket.recvfrom(4096)
		print "data: " + recieved
		if recibido == "close1qazxsw2":
			peerSocket.close()
			break

# Acciones para el menu
options = {
	1:"Read data from memory",
	2:"Write data into memory",
	3:"Change permits of a data in memory",
	4:"Create a data in memory",
	5:"Exit",
}

# Devuelve la seleccion hecha en un menu de opciones
def chooseMenuAction():
	#Se inclina por hacer un ciclo while por que la recursividad podria no entregar la opcion correcta
	while True:
		print "Esto es lo que puede hacer aqui:"
		for option in options:
			print option, " - ", options[option]

		print "\nPor favor seleccione la opcion que mas le apetezca"
		selection = int(raw_input(">>> "))
		if selection in options:
			return selection
		else:
			print "Posiblemente algo este mal con su teclado"
			print "Aparentemente ha escogido una opcion incorrecta"

def petitionThread():
	while True:
		command = chooseMenuAction()
		sent = peerSocket.sendTo(command, servData)
		if command == "close":
			break

#Inicializa el servidor, su configuracion y los hilos que escuchan y envian mensajes
def startServer():
	peerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(servData)
	#aqui se inicializan los hilos petition y listening

# Cada nodo debe tener espacios de memoria disponibles (paginas) 
# a los que cada uno de los nodos podra acceder de manera 
# transversal, aleatoria y transparente

# Cada nodo puede hacer las siguientes acciones:
# - Devolver un dato localizado en su propia memoria
# - Puede escribir un dato en la memoria Posicion de memoria, Tipo de dato, Contenido, Quien hace la peticion, y lo hace con los permisos de la pagina
# - Cada nodo puede cambiar los permisos de sus paginas
# - Cada nodo crear una pagina en su propia memoria