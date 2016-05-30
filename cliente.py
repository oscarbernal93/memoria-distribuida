import socket

# Definicion de Globales
_MEMORYSIZE = 4

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
		if who != "127.0.0.1":
			if ((self.permissions == "1110") or (self.permissions == "1011") or (self.permissions == "1010")):
				return self.content
			else:
				print "No permissions granted for this Memory Unit"
		else:
			return self.content

	#Changes the content of the MU depending on the permissions granted for "who"
	def write(self, who, datatype, content):
		if who != "127.0.0.1":
			if ((self.permissions == "1011") or (self.permissions == "1111")):
				self.content = content
			else:
				print "No permissions granted for this Memory Unit"
		else:
			if ((self.permissions == "1100") or (self.permissions == "1110") or (self.permissions == "1111")):
				self.content = content
			else:
				print "I have no permissions to write this Memory Unit"

	def chmod(self, who, newPermissions):
		if who == "127.0.0.1":
			self.permissions = newPermissions
		else:
			print "You don't have enough rights to do this!"





# La memoria es un diccionario de Unidades de Memoria (MU)
memory = {}

opciones = {
	1:"Read data from memory",
	2:"Write data into memory",
	3:"Change permits of a data in memory",
	4:"Create a data in memory",
	5:"Exit",
}

# Cada nodo debe tener espacios de memoria disponibles (paginas) 
# a los que cada uno de los nodos podra acceder de manera 
# transversal, aleatoria y transparente

# Cada nodo puede hacer las siguientes acciones:
# - Devolver un dato localizado en su propia memoria
# - Puede escribir un dato en la memoria Posicion de memoria, Tipo de dato, Contenido, Quien hace la peticion, y lo hace con los permisos de la pagina
# - Cada nodo puede cambiar los permisos de sus paginas
# - Cada nodo crear una pagina en su propia memoria

def menu():
	print "Esto es lo que puede hacer aqui:"
	for opcion in opciones:
		print opcion, " - ", opciones[opcion]

	print "\nPor favor seleccione la opcion que mas le apetezca"
	variable = int(raw_input(">>> "))
	if variable in opciones:
		return variable
	else:
		print "Posiblemente algo este mal con su teclado"
		print "Aparetemente ha escogido una opcion incorrecta"
		menu()

print "hola, este es el cliente de memoria distribuida"
print "realmente usted no sabe donde ni como se almacena la info"
opcion = menu()
print ("usted escogio: " + opciones[opcion])