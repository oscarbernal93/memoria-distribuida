import socket
import sys
import threading
import re
import string

# Definicion de Variables Globales
_MEMORYSIZE = 1										#The max size of the memory
_PRIVATEPORT = 12836								#Port to manage the private conection
_PUBLICCONECTION = ("<broadcast>",12835)			#Tuple with Host for Multicast Messaging
_PRIVATECONECTION = ("",_PRIVATEPORT)				#Tuple with Host Information, useful for the "UDP sending code" reading
_DATASIZE = 2048									#Size of data 
_TIMEOUT = 2										#Timeout in seconds of the connection
# IP from the machine
_LOCALIP = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
# Inicializacion de Socket
publicSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
publicSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
publicSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
publicSocket.bind(_PUBLICCONECTION)

privateSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
privateSocket.settimeout(_TIMEOUT)
privateSocket.bind(_PRIVATECONECTION)

#-------------------------------------------------------------------------------------------

#Memory Unit Class, It's the core of the shared memory system
class MU:
	def __init__(self):
		self.datatype = "None"
		self.content = ""
		self.permissions = "1110"
		self.owner = _LOCALIP
		self.accesses = []

	def __str__(self):
		return "{"+"owner:"+self.owner+","+"datatype:"+self.datatype+","+"content:"+self.content+"}"
	#Returns the content to the user which asked for it, depending on the permissions granted for "who"
	def read(self, who):
		if who != self.owner:
			if (self.permissions[2] == "1"):
				return self
		else:
			return self

	#Changes the content of the MU depending on the permissions granted for "who"
	def write(self, who, NewDataType, newContent):
		if who != self.owner:
			if (self.permissions[3] == "1"):
				self.content = newContent
				self.datatype = NewDataType
				return self
		elif (self.permissions[1] == "1"):
			self.content = newContent
			self.datatype = NewDataType
			return self;

	#Changes the permissions for the MU
	def chmod(self, who, newPermissions):
		if who == self.owner:
			self.permissions = newPermissions

# Controller Class, It's the master class, control everything
class CC:
	def __init__(self):
		# The memory is a dictionary of Memory Units (MU)
		self.memory = {}

	def append(self, name, memUnit):
		# put a memory unit in the memory
		# First try to create in the local memory
		if self.check():
			self.memory[name]=memUnit
		else:
			# if the local memory is full, then send a message to all nodes
			sent = publicSocket.sendto("1n33dm3msp4c3_"+str(_PRIVATEPORT), _PUBLICCONECTION)
			recieved = ''
			try:
				recieved, node = privateSocket.recvfrom(_DATASIZE)
			except Exception, e:
				pass
			
			if recieved == "1h4v3m3msp4c3":
				# Somebody have space
				privateSocket.sendto(name+"_"+memUnit.owner,node)
			else:
				print "There is no memory space available"
			pass

	def create(self, who, name):
		#creates a new memory unit in the memory
		newMemUnit = MU()
		newMemUnit.owner = who;
		self.append(name,newMemUnit)

	def check(self):
		# verify the available space in the local memory
		return len(self.memory) < _MEMORYSIZE

	def local_read(self, who, name):
		if name in self.memory:
			return self.memory[name].read(who)
		else:
			return None
	def read(self, name):
		# read a variable name from the memory
		lr = self.local_read(_LOCALIP,name)
		if lr is None:
			#if the variable name isn't in the local memory ask in the broadcast
			sent = publicSocket.sendto("r34dv4rpl34s3_"+str(_PRIVATEPORT)+"_"+name, _PUBLICCONECTION)
			recieved = ''
			try:
				recieved, node = privateSocket.recvfrom(_DATASIZE)
			except Exception, e:
				pass
			if recieved != '':
				# Somebody have the data
				return recieved
			else:
				return None;
			pass
		else:
			return str(lr)
	def local_write(self,who, name, datatype, content):
		if name in self.memory:
			return self.memory[name].write(who, datatype, content)
		else:
			return None
	def write(self, name, datatype, content):
		# write the var to local if is possible
		lw = self.local_write(_LOCALIP,name,datatype,content)
		if lw is None:
			#if the variable name isn't in the local memory ask in the broadcast
			sent = publicSocket.sendto("wr1t3v4rpl0xz_"+str(_PRIVATEPORT)+"_"+name+"_"+datatype+"_"+content, _PUBLICCONECTION)
			recieved = ''
			try:
				recieved, node = privateSocket.recvfrom(_DATASIZE)
			except Exception, e:
				pass
			if recieved != '':
				# Somebody have the data
				return recieved
			else:
				return None;
			pass
		else:
			return str(lw)

#-------------------------------------------------------------------------------------------

# Actions available to the menu, remember if edit, do it too in the bottom of the code in the main loop
optionsList = {
	1:"Read data from memory",
	2:"Write data into memory",
	3:"Change permits of a data in memory",
	4:"Create a data in memory",
	5:"Exit",
}

# Messages Codes:
# 1n33dm3msp4c3 = the sender need space in the memory
# 1h4v3m3msp4c3 = the sender have space in the memory
# r34dv4rpl34s3 = the sender need to read a memory unit
# wr1t3v4rpl0xz = the sender need to write to a memory unit

def listeningThread():
	while True:
		recieved, sender = publicSocket.recvfrom(4096)
		if recieved == "close1qazxsw2":
			break
		recieved = string.split(recieved,"_");
		# asign the private port to sender tuple
		sender = (sender[0],int(recieved[1]))
		# save the recived data
		data = recieved[0]
		if data == '1n33dm3msp4c3':
			if master.check():
				privateSocket.sendto('1h4v3m3msp4c3',sender)
				try:
					recieved, node = privateSocket.recvfrom(_DATASIZE)
					recieved = string.split(recieved,"_");
					name = recieved[0]
					owner = recieved[1]
					master.create(owner,name)
				except Exception, e:
					pass
			pass
		if data == 'r34dv4rpl34s3':
		# this mesage have a extra parameter
			varname = recieved[2]
			lr = master.local_read(sender[0],varname);
			# if the var is in the local mem
			if lr is not None:
				privateSocket.sendto(str(lr),sender)
		if data == 'wr1t3v4rpl0xz':
		# this mesage have some extra parameters
			varname = recieved[2]
			datatype = recieved[3]
			content = recieved[4]
			lw = master.local_write(sender[0],varname, datatype, content);
			# if the var is in the local mem
			if lw is not None:
				privateSocket.sendto(str(lw),sender)
				

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

# print a welcome message
print "\n*********"
print "*  DMC  *"
print "*********\n"
print "Hello, This is the Distributed Memory Client"
print "You don't know how or where the info is stored"
# the master controller is created
master = CC()

# the listening thread is initializated
tlist = threading.Thread(target=listeningThread)
tlist.start()

# Begins the MAIN LOOP
while True:
	option = chooseMenuAction()
	print ("You choose: " + optionsList[option])
	if option == 1:
		#Read
		print "\nPlease write the variable name"
		name = raw_input(">>> ")
		mu = master.read(name)
		if mu is None:
			print "The selected variable is inaccessible"
		else:
			print mu
	if option == 2:
		#Write
		print "\nPlease write the variable name"
		name = raw_input(">>> ")
		print "\nPlease write the content type"
		datatype = raw_input(">>> ")
		print "\nPlease write the content"
		content = raw_input(">>> ")
		mu = master.write(name,datatype,content)
		if mu is None:
			print "The selected variable is inaccessible"
		else:
			print "new content of the variable: "+mu
	if option == 3:
		#ChMod
		pass
	if option == 4:
		#Create Data
		print "\nPlease write the variable name"
		name = raw_input(">>> ")
		print "\nPlease write the owner ip, you can write \"me\""
		owner = raw_input(">>> ")
		if owner == "me":
			owner = _LOCALIP
		pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
		if not pattern.match(owner):
			print "Incorrect owner's ip address"
		else:
			master.create(owner,name)

	if option == 5:
		#Exit
		publicSocket.sendto('close1qazxsw2',_PUBLICCONECTION);
		publicSocket.close()
		privateSocket.close()
		break