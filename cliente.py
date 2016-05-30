import socket
import sys
import threading

# Definicion de Variables Globales
_MEMORYSIZE = 4 											#Un maximo de 4 bloques
peerSocket = "" 											#Socket Handler
HOST = ''													#Host IP info 
PORT = 10000												#Host Port info
servData = (HOST,PORT)										#Tuple with Host Information, useful for the "UDP sending code" reading

#-------------------------------------------------------------------------------------------

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
	def write(self, who, NewDataType, newContent):
		if who != self.owner:
			if ((self.permissions == "1011") or (self.permissions == "1111")):
				self.content = newContent
				self.datatype = NewDataType
			else:
				print "No permissions granted for this Memory Unit"
		else:
			if ((self.permissions == "1100") or (self.permissions == "1110") or (self.permissions == "1111")):
				self.content = newContent
				self.datatype = NewDataType
			else:
				print "I have no permissions to write this Memory Unit"

	#Changes the permissions for the MU
	def chmod(self, who, newPermissions):
		if who == self.owner:
			self.permissions = newPermissions
		else:
			print "You don't have enough rights to do this!"


#-------------------------------------------------------------------------------------------

# Acciones para el menu
optionsList = {
	1:"Read data from memory",
	2:"Write data into memory",
	3:"Change permits of a data in memory",
	4:"Create a data in memory",
	5:"Exit",
}

def listeningThread():
	while True:
		recieved, server = peerSocket.recvfrom(4096)
		print "data: " + recieved
		if recibido == "close1qazxsw2":
			peerSocket.close()
			break

# Devuelve la seleccion hecha en un menu de opciones
def chooseMenuAction():
	#Se inclina por hacer un ciclo while por que la recursividad podria no entregar la opcion correcta
	while True:
		# Se listan las opciones disponibles
		print "\nThese are the options that you have access:"
		for option in optionsList:
			print option, " - ", optionsList[option]
		# Se lee el teclado
		print "\nPlease select an option"
		foo = raw_input(">>> ")
		# Se intenta convertir a int el valor leido
		bar = 0
		try:
			bar = int(foo)
		except Exception, e:
			print "Please, you can do it better, Respect Yourself!"
		# Se busca el valor en la lista y se retorna
		if bar in optionsList:
			return bar
		# Si falla, reimprime el menu
		else:
			print "Possibly something is wrong with your keyboard"
			print "Apparently you chose a wrong option, try again"

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
	tpet = threading.Thread(target=petitionThread)
	tlist = threading.Thread(target=listeningThread)

# Cada nodo debe tener espacios de memoria disponibles (paginas) 
# a los que cada uno de los nodos podra acceder de manera 
# transversal, aleatoria y transparente

# Cada nodo puede hacer las siguientes acciones:
# - Devolver un dato localizado en su propia memoria
# - Puede escribir un dato en la memoria Posicion de memoria, Tipo de dato, Contenido, Quien hace la peticion, y lo hace con los permisos de la pagina
# - Cada nodo puede cambiar los permisos de sus paginas
# - Cada nodo crear una pagina en su propia memoria


# Se imprime el encabezado de bienvenida
print "\n*********"
print "*  DMC  *"
print "*********\n"
print "Hello, This is the Distributed Memory Client"
print "You don't know how or where the info is stored"
# Se Imprime el menu
option = chooseMenuAction()
print ("You choose: " + optionsList[option])
