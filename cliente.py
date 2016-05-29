import socket

opciones = {
	1:"Leer un dato de memoria",
	2:"Escribir un dato en la memoria",
	3:"Cambiar permisos de un dato de la memoria",
	4:"Crear un dato en la memoria",
	5:"Salir",
}

# Cada nodo debe tener espacios de memoria disponibles (paginas) 
# a los que cada uno de los nodos podra acceder de manera 
# transversal, aleatoria y transparente

# Cada nodo puede hacer las siguientes acciones:
# - Devolver un dato localizado en su propia memoria
# - Puede escribir un dato en la memoria Posicion de memoria, Tipo de dato, Contenido, Quien hace la peticion, y lo hace con los permisos de la pagina
# - Cada nodo puede cambiar los permisos de sus paginas
# - Cada nodo crear una pagina en su propia memoria



def listen_petition():
	while True:
		received, server = s.recvfrom(4096)

def send_petition():

def start_server():

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