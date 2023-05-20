import socket
import time
import threading
import os
# importer mon code
import huffman as HF
import pickle
import os

class classServer(threading.Thread):
	
	def __init__(self,conn,adr,numero):
		threading.Thread.__init__(self)
		self.adr = adr
		self.conn = conn
		self.numero = numero
	
	def run(self):
		# Recevoir le nom du fichier 
		print(f"client n° {self.numero} est connecté")
		# Donner le choix des fichiers à télécharger
		dico = pickle.dumps(listfiles)
		self.conn.send(dico)
		# Recevoir le nom de fichier
		file_name = self.conn.recv(999999).decode("utf-8")
		# si le fichier est dans le dossier data du serveur
		# String to liste 
		filesRequest = file_name.split(",")
		count = 0
		# les fichiers demandés doivent être au niveau du serveur
		for fileClient in filesRequest:
			if fileClient in listfiles:
				count += 1
		#print(f"{filesRequest} - {listfiles}")
		if(len(filesRequest) == count):
			for file_name in filesRequest:
				h = HF.Huffman("data/"+file_name)
				h.dictionnaire = {}
				h.construireArbreHuffman()
				h.GenererCodeHuffman(h.arbre[0])
				print(h.dictionnaire)
				codeHuffman = h.compression(open("data/"+file_name ,"r").read())
				# bcl : nombre de bloc à envoyer
				bcl = int(len(codeHuffman)/8)
				# Envoyer des blocs de 8 octs 
				for i in range(bcl):
					self.conn.send(codeHuffman[i*8:(i*8)+8].encode("utf-8"))
				# Envoyer le dernier bloc restant 
				if(int(len(codeHuffman)%8) != 0):
					self.conn.send(codeHuffman[bcl*8:].encode("utf-8"))
				self.conn.send("FIN".encode("utf-8"))
				print(f"Le serveur a envoyé tous {bcl+1} bloc(s) du fichier compressé, client N° :{self.numero}")
				dico = pickle.dumps(h.dictionnaire)
				self.conn.send(dico)
				print(f"Le serveur a envoyé le dictionnaire pour décompresser, client N° :{self.numero}")
		else:
			self.conn.send("ERROR".encode("utf-8"))
			print("Le client a choisi un fichier qui n'existe pas")
		self.conn.close

# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serversocket.bind(("", 15555))
# become a server socket
serversocket.listen(1)
numero = 1
print(f"En attente d'un client .... N°{numero}")

listfiles = []
for root, dirs, files in os.walk("data/"):
    for filename in files:
        listfiles.append(filename)
while True:
    # accept connections from outside
	(clientsocket, address) = serversocket.accept()
	print(f"adresse : {address} {clientsocket}")
	server = classServer(clientsocket, address,numero)
	server.start()
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
	# je decide si le serveur va receptionner un autre client
	numero += 1
	#if(input("voulez-vous continuer ?! Tapez N pour quitter \n")=="N"):
	#	break
clientsocket.close()
