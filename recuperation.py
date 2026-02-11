import cesar

def recuperation_donnee(fichier: str,cle: int) -> list[list]:
    """
    Liste de listes contenants toutes le fichier .txt
    """
    liste_de_donnee= []
    listes_deprypter = cesar.decryptage(fichier,cle).split('\n')
    for indice in range(len(listes_deprypter)):
        if listes_deprypter[indice] != "": #Pour ne pas récuperer les lignes vides s'il y en a.
            liste_de_donnee.append(listes_deprypter[indice].split('*'))
    return liste_de_donnee
# print(recuperation_donnee(repertoire("23456789.txt"),24)) #Pour regarder les données qui peuvent être traitées lors de la simulation


#Liste de dictionaire pour ident.txt (avec l'aide de la fonction bdd)
def recuperation_user(fichier:str ,cle: int) -> list[dict]:
    """
    Liste de dictionnaire contenant les information du fichier ident.txt
    """
    new_liste_users = []
    listes_donnee_user = recuperation_donnee(fichier,cle)
    for indice in range(len(listes_donnee_user)):
        dico_user = {"identifiant":listes_donnee_user[indice][0],"motdepasse":listes_donnee_user[indice][1],"nom":listes_donnee_user[indice][2],"cle":listes_donnee_user[indice][3]}
        new_liste_users.append(dico_user)
    return new_liste_users

