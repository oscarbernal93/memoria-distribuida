import socket

opciones = {
	1:"Leer un dato de memoria",
	2:"Escribir un dato en la memoria",
	3:"Cambiar permisos de una pagina de la memoria",
	4:"Crear una pagina en la memoria",
	5:"Salir",
}

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