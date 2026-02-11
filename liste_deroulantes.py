import recuperation

def liste_deroulante(fichier: str,cle: int,prefixe: str) -> list:
    """
    :param prefixe: Prefixe de la ligne 'CPT/BUD/OPE'
    Renvoie la liste de tous les éléments de la première colone du fichier contenant le prefixe
    (pour la liste déroulante)
    """
    liste_donnee_user=recuperation.recuperation_donnee(fichier,cle)
    liste_derou=[]
    for indice in range(len(liste_donnee_user)):
        if liste_donnee_user[indice][0] == prefixe and liste_donnee_user[indice][1] != 'aucun':
            liste_derou.append(liste_donnee_user[indice][1])
    return liste_derou

def liste_deroulante_bud(fichier: str,cle: int, compte: str):
    liste_donnee=recuperation.recuperation_donnee(fichier,cle)
    liste_derou=[]
    for i in range(len(liste_donnee)):
        if liste_donnee[i][0]=='BUD' and liste_donnee[i][3]==compte:
            liste_derou.append(liste_donnee[i][1])
    return liste_derou