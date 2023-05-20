import socket
import huffman as HF
import pickle

# create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
s.connect((socket.gethostname(), 15555))
print("Je me connecte\n")

# Afficher la liste des fichiers à télécharger
liste_fichiers = s.recv(999999)
liste_fichiers = pickle.loads(liste_fichiers)
print(f"Choisir le(s) fichier(s) à télécharger : séparer les avec ','")
for file in liste_fichiers:
    print(f"\t- {file}")


# Choisir le fichier à télécharger 
file_name = input("Entrer le nom du fichier ! \n")
s.send(file_name.encode("utf-8"))
#file_name = "dataClient/"+file_name

print("J'attend de recevoir le fichier ...")

buffer = s.recv(32).decode("utf-8")
msg = str(buffer)
# Le serveur envoi ERROR si le nom du fichier n'est pas disponible dans le dossier "data"
# le client reçoit des blocs de 32 bytes qui correspondent au nombre de 8 bytes envoyés par le serveur et 
# l'encodage utf-8 qui est codé sur 4 bytes alors 8 * 4 = 32 bytes
# le serveur envoie FIN si l'envoi est terminé.
if(str(buffer) != "ERROR"):
    for onefile in file_name.split(","):
        while True:
            buffer = s.recv(32).decode("utf-8")
            # Le serveur decide d'arreter la récéption
            if str(buffer)=="FIN":
                break
            msg += buffer
        # la fonction de decompression est disponible dans la classe huffman 
        h = HF.Huffman("")
        dico = s.recv(999999)
        # récupération du dictionnaire pour la décompression 
        dico = pickle.loads(dico)
        # la fonction prend en paramètre les caractères Unicode reçu par le serveur et le dictionnaire huffman
        buffer = h.decompression(msg , dico)
        # écrire au niveau du fichier 
        with open("dataClient/"+onefile, 'w') as _file:
            _file.write(buffer)
        print('Fichier bien reçu.')
        msg = ''
else:
    print("---------un fichier ou plusieurs n'existent pas sur le serveur.---------")
print('fin de connexion')
    
