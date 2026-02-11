import os

def repertoire(nom_fichier: str) -> str:
    """
    :param nom_fichier: le nom du fichier avec l'extension .txt
    :return: le chemin d'accès absolue du fichier
    """
    if 'ident.txt' not in nom_fichier:
        chemin_python=os.path.dirname(__file__)
        chemin_fichier=os.path.join(chemin_python,'Users',nom_fichier)
        return chemin_fichier
    else:
        return nom_fichier

def decryptage(fichier: str,cle: int)-> str:
    """
    Renvoie la chaine décryptée d'un fichier.txt crypté
    """
    fichier=repertoire(fichier)
    with open(fichier, 'r') as file:
        lignes=file.read()
    code_decryptee=''
    for caractere in lignes:
        code_ascii=ord(caractere)
        if code_ascii in range(43,123) and (caractere!='*'or caractere!='\n'):
            code_decryptee+=chr((code_ascii-43-cle)%80+43)
        else:
            code_decryptee+=caractere
    return code_decryptee

def cryptage(chaine_de_caracteres: str,cle: int) -> str:
    """
    Renvoie la chaine cryptée d'une chaine décryptée
    """
    code_cryptee=''
    for caractere in chaine_de_caracteres:
        code_ascii=ord(caractere)
        if code_ascii in (range(43,123)):
            code_cryptee+=chr((code_ascii-43+cle)%80+43)
        else:
            code_cryptee+=caractere
    return code_cryptee

def cryptage2(fichier:str,cle:int,newfichier:str) -> None:
    """
    :param fichier: fichier non cryptée que l'on veut cryptée
    :param newfichier: fichier sur que l'on va écraser/créer où l'on cryptera le fichier non cryptée
    """
    fichier=repertoire(fichier)
    with open(fichier,'r') as file:
        lignes=file.read()
    with open(newfichier,'w')as newfile:
        for caractere in lignes:
            code_ascii=ord(caractere)
            if code_ascii in range(43,123):
                newfile.write(chr((code_ascii-43+cle)%80+43))
            else:
                newfile.write(caractere)
        newfile.close()

def decryptage2(string: str,cle: int) -> str:
    """
    :param string: string cryptée que l'on veut décrypter
    """
    code_decryptee=''
    for caractere in string:
        code_ascii=ord(caractere)
        if code_ascii in range(43,123) and (caractere!='*'or caractere!='\n'):
            code_decryptee+=chr((code_ascii-43-cle)%80+43)
        else:
            code_decryptee+=caractere
    return code_decryptee

# cryptage2("/Users/mrw/Python/Gestion de Banque GUI/Users/48754135_noncryptee.txt",56,"/Users/mrw/Python/Gestion de Banque GUI/Users/48754135.txt")
# print(decryptage('/Users/mrw/Python/Gestion de Banque GUI/Users/48754135.txt',56))
# print(decryptage('/Users/mrw/Python/Gestion de Banque GUI/Users/90678452.txt',89))
print(cryptage("Samuel",12))
print(decryptage2("_my1qx",12))