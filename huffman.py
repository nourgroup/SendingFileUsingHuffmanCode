# importing "heapq" to implement heap queue 

class Element:
	def __init__(self,occurrence):
		self.occurrence = occurrence
	# surchage l'operateur ==
	def __eq__(self,p2):
		return True if (p2.occurrence == self.occurrence ) else False
	
	# surchage l'operateur >
	def __gt__(self,p2):
		return True if (p2.occurrence > self.occurrence ) else False
	
	# surchage l'operateur <
	def __lt__(self,p2):
		return True if (p2.occurrence < self.occurrence ) else False
	
	# surchage l'operateur +
	def __add__(self,p2):
		return p2.occurrence + self.occurrence

	# surchage l'operateur >=
	def __ge__(self,p2):
		return True if (p2.occurrence >= self.occurrence ) else False
	
	# surchage l'operateur <=
	def __le__(self,p2):
		return True if (p2.occurrence <= self.occurrence ) else False

	def __str__(self):
		return "Le nombre d'occurrence : %d" % (self.occurrence , )

# creation de classe avec le nombre d'occurence et le nombre d'occurrence.
class Feuille(Element):
	def __init__(self,occurrence,caractere):
		super().__init__(occurrence)
		self._caractere = caractere

	@property
	def caractere(self):
		return self._caractere

	@caractere.setter
	def caractere(self,caractere):
		self._caractere = caractere

	# surcharger la fonction toString
	def __str__(self):
		super().__str__()
		return "caractere : %s" % (self.caractere , )

# Création de classe avec le nombre d'occurence et l'element pointant vers la gauche ou la droite
class Noeud(Element):
	def __init__(self, occurrence,droite=None,gauche=None):
		super().__init__(occurrence)
		self._droite = droite
		self._gauche = gauche

	@property
	def droite(self):
		return self._droite

	@property
	def gauche(self):
		return self._gauche

	@droite.setter
	def droite(self,droite):
		self._droite = droite

	@gauche.setter
	def gauche(self,gauche):
		self._gauche = gauche

	# surcharger la fonction toString
	def __str__(self):
		super().__str__()
		return "occ %d " % (self.occurrence)

# la classe Huffman contenant le fichier, arbre , le dictionnaire
class Huffman:
	def __init__(self,fichier,arbre = [],dictionnaire = {}):
		self.fichier 	= fichier
		self.arbre 		= arbre 
		self.dictionnaire = dictionnaire
	
	# lire le fichier et renvoyer une liste des occurrence avec l'ordre
	def lire(self):
		# nombre d'occurence
		file_ = open(self.fichier ,"r")
		table = {}
		for l in file_.read():
			if l in table:
				table[l] = table[l] + 1
			else:
				table[l] = 1
		# remplir la liste avec les feuilles
		sorted_list = []
		for i in sorted(table.values()):
			for j in table.keys():
				if table[j] == i:
					# ajouter l'occurrence et les caracteres aux feuilles
					sorted_list.append(Feuille(table[j],j))
					# retirer l'element après son insertion à la liste
					table.pop(j)
					break
		return sorted_list

	# construire un arbre binaire 
	def construireArbre(self):
		# retourner une liste des feuilles en ordre
		self.arbre = self.lire()

	# construire code de huffman
	def construireArbreHuffman(self):
		self.construireArbre()
		# repeter tant qu'on n'as pas encore un seul noeud
		while (len(self.arbre)>1):
			# enlever les deux petits elements de l'arbre binaire
			n1 = self.arbre[0]
			del self.arbre[0]
			n2 = self.arbre[0]
			del self.arbre[0]
			# Ajouter  le noeud dans l'arbre
			self.arbre.append(Noeud((n1+n2), n1 , n2))
			# trier à nouveau 
			self.arbre = sorted(self.arbre , key=lambda x:x.occurrence)
		return self.arbre
	# Créer le code de huffman
	def GenererCodeHuffman(self ,elem ,code = ''):
		# Condition d'arrêt pour la focntion récursive
		if isinstance(elem,Feuille):
			self.dictionnaire[elem.caractere] = code ; return
		self.GenererCodeHuffman(elem.gauche , code + '0')
		self.GenererCodeHuffman(elem.droite , code + '1')

	# Compression : je mets le nombre de bits supplémentaires au niveau de premier caractere.
	# normalement comprise entre 0-7 et il n'est pas encodé 
	# et lors de la decompression je prend le chiffre et se baser dessus pour savoir les bits à prendre 
	# en compte.
	def compression(self, data):
		
		DataToCodeHuffman = ''
		# Chercher pour chaque caractere à encoder le serie de bits huffman 
		# compresser le fichier
		for elem in data:
			DataToCodeHuffman = DataToCodeHuffman + self.dictionnaire[elem]
		
		# Le nombre de bits de plus afin de préparer le données pour l'envoi 
		moinsDe8Car = len(DataToCodeHuffman) % 8
		
		# ajouter des 0 pour completer le dernier bloc de 8 binaires 
		if moinsDe8Car!=0 :
			DataToCodeHuffman = DataToCodeHuffman + (8 - moinsDe8Car) * '0'
		
		# header contain the added character's number
		dataCode = str(moinsDe8Car)#str(bin(8 - moinsDe8Car)[2:].zfill(8))#str(self.DecToBin(8 - moinsDe8Car))
		
		# encoder en assci chaque 8 bits
		for i in range(int(len(DataToCodeHuffman)/8)):
			dataCode = dataCode + chr(int(DataToCodeHuffman[(i*8):(i*8+8)],2))
		
		return dataCode

	def decompression(self, dataCode, dico):
		# dataCode dictionnaire 
		tousLeCode = ''

		# header : contient le nombre de bits ajoutés afin d'avoir le nombre de bits multipliable par 8
		header = int(dataCode[0:1])
		
		# tousLeCode : construire le code binaires huffman 
		for data in dataCode[1:]:
			tousLeCode += bin(ord(data))[2:].zfill(8)
		
		# enlever les binaires ajoutés lors de la compression
		tousLeCode = tousLeCode[:-(8-header)]
		
		# inverser clés et valeurs
		# dataInverse : contient dans les clés le binaire et valeur la lettre
		dataInverse = { v : k for k , v in dico.items()}
		# values : contient les binaires extraites de dictionnaire de compression/decompression 
		values = [ k  for k , v in dataInverse.items()]
		
		position = 0
		
		originData = ''
		# search on dictionnary
		# 
		for i in range(0,len(tousLeCode)):
			if tousLeCode[position:(i+1)] in values:
				originData = originData + dataInverse[tousLeCode[position:i+1]]
				position = i + 1
		return originData

"""
h = Huffman("data/text.txt")
#h.construireArbre()
h.construireArbreHuffman()

h.GenererCodeHuffman(h.arbre[0])
file_ = open("data/text.txt" ,"r").read()
print(h.compression(file_))
print(h.decompression(h.compression(file_),h.dictionnaire))
"""