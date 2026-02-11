import os
chemin_python=os.path.dirname(__file__)
#Permet d'avoir le chemin d'accès de tous les fichier qui sont dans le dossier Users (dossier qui doit être dans le même dossier que ce ficheir py)
#Grâce à chemin python, cette fonction est utilisable peut importe l'os et l'ordinateur que vous utilisez
def repertoire(nom_fichier):
    chemin_fichier=os.path.join(chemin_python,'users',nom_fichier)
    return chemin_fichier


def decryptage(fichier,cle):
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


def cryptage(chaine_de_caracteres,cle):
    code_cryptee=''
    for caractere in chaine_de_caracteres:
        code_ascii=ord(caractere)
        if code_ascii in (range(43,123)):
            code_cryptee+=chr((code_ascii-43+cle)%80+43)
        else:
            code_cryptee+=caractere
    return code_cryptee


#Liste de liste pour stocker les informations du fichier de l'utilisateur (Façon Marwan)
def recuperation_donnee(fichier,cle):
    liste_de_donnee= []
    listes_deprypter = decryptage(fichier,cle).split('\n')
    for indice in range(len(listes_deprypter)):
        if listes_deprypter[indice] != "": #Pour ne pas récuperer les lignes vides s'il y en a.
            liste_de_donnee.append(listes_deprypter[indice].split('*'))
    return liste_de_donnee
print(recuperation_donnee(repertoire("90678452.txt"),89))

#Liste de dictionaire pour ident.txt (avec l'aide de la fonction bdd)
def recuperation_user(fichier,cle):
    new_liste_users = []
    listes_donnee_user = recuperation_donnee(fichier,cle)
    for indice in range(len(listes_donnee_user)):
        dico_user = {"identifiant":listes_donnee_user[indice][0],"motdepasse":listes_donnee_user[indice][1],"nom":listes_donnee_user[indice][2],"cle":listes_donnee_user[indice][3]}
        new_liste_users.append(dico_user)
    return new_liste_users


#Fonction qui modifie le fichier lorsque l'utilisateur fait un ajout
def sauvegarde(fichier,cle,listes_de_donnee):
    listes_de_donnee = sorted(listes_de_donnee, key = len)
    chaine = ""
    with open(fichier,"w") as file:
        for indice in range(len(listes_de_donnee)):
            chaine += "*".join(listes_de_donnee[indice])+"\n" 
        file.write(cryptage(chaine,cle))
    file.close()
    return "Votre ajout à été effectué.\n"


#Fonction qui affiche les opérations du compte choisit par l'utilisateur
def visualiser_compte(fichier,cle,compte):
    ope_cpt = []
    listes_donnee_user = recuperation_donnee(fichier,cle)
    print(f"{solde_utilisateur(fichier,cle,compte)}\n")
    print("Voici les opérations du "+compte+":\n")
    for indice in range(len(listes_donnee_user)):
        if listes_donnee_user[indice][0]== "OPE" and compte == listes_donnee_user[indice][3]:
            ope_cpt.append(listes_donnee_user[indice])
    if len(ope_cpt) == 0:
        print("Aucune opération\n")
        print("-"*200)
        gestion_de_compte(fichier,cle,compte)
    for indice in range(len(ope_cpt)):
        print(f"Date: {ope_cpt[indice][1]}, Budget: {ope_cpt[indice][7]}, Motif: {ope_cpt[indice][2]}, Dépenses: {ope_cpt[indice][4]}€, Moyen de payement utilisé: {ope_cpt[indice][5]}, Vérification: {ope_cpt[indice][6]}\n")
    print("-"*200)
    gestion_de_compte(fichier,cle,compte)


#Affichage du solde (somme des achats - le montant de base de l'utilisateur qui est de 5000€)
def solde_utilisateur(fichier,cle,compte):
    achat = []
    solde = 0
    listes_donnee_user = recuperation_donnee(fichier,cle)
    for indice in range(len(listes_donnee_user)):
        if listes_donnee_user[indice][0]=='OPE'and compte == listes_donnee_user[indice][3] and listes_donnee_user[indice][6] == "True":
                achat.append(listes_donnee_user[indice][4])
    for i in range(len(achat)):
        solde += float(achat[i])
    return "Solde "+compte+": "+str(solde)+"€\n"


#Gérer les comptes de l'utilisateur
def gestion_de_compte(fichier,cle,compte):
    print("-"*200)
    print(solde_utilisateur(fichier,cle,compte))
    action_user = input(f"Visualiser les opérations du {compte}, tapez 1.\n\nAjouter une opération, tapez 2.\n\nFaire un virement, tapez 3.\n\nSélectionner un autre compte, tapez 4.\n\nAjouter un compte, tapez 5.\n\nRetourner en arrière, tapez 6.\n\nAppuyer 'Entrer' pour quitter; ")
    if action_user == "":
        exit()
    if action_user not in  "123456":
        print("-"*200)
        print("Erreur")
        print("-"*200)
        return action_user
    if action_user == "1":
        print("-"*200)
        return visualiser_compte(fichier,cle,compte)
    if action_user == "2":
        print("-"*200)
        return ajou_ope(fichier,cle,compte)
    if action_user == "3":
        print("-"*200)
        return virement(fichier,cle,compte)
    if action_user == "4":
        print("-"*200)
        compte_user = input("Veuillez entrer le compte que vous voulez traitez. Exemple : 'Compte A';\n\n") #L'utilisateur doit entrer correctement le nom du compte (espace et maj)
        if ['CPT',compte_user] not in recuperation_donnee(fichier,cle):
            print("Le compte n'existe pas\n")
            print("-"*200)
            return gestion_de_compte(fichier,cle,compte)
        print("-"*200)
        return gestion_de_compte(fichier,cle,compte_user)
    if action_user == "5" :
        print("-"*200)
        return ajou_compte(fichier,cle)
    if action_user == "6":
        print("-"*200)
        fenetre_de_bord(fichier,cle,compte)


#Fonction qui ajoute un compte au fichier de l'utilisateur si ce dernier le demande.
def ajou_compte(fichier,cle):
    listes_donnee_user = recuperation_donnee(fichier,cle)
    lettre_cpt = input(f"Veuillez entrer la lettre en majuscule qui définira vôtre compte: ")#Si le nom du compte doit obligatoirement être "Compte (lettre)"
    if lettre_cpt not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        print("Veuillez entrez une lettre majuscule.\n")
        print("-"*200)
        return ajou_compte(fichier,cle)
    if ["CPT","Compte "+lettre_cpt] in  listes_donnee_user:
        print("Le compte existe déja.\n")
        print("-"*200)
        return ajou_compte(fichier,cle)
    listes_donnee_user.append(["CPT","Compte "+lettre_cpt])  
    print(sauvegarde(fichier,cle,listes_donnee_user))
    print("-"*200)
    gestion_de_compte(fichier,cle,listes_donnee_user[0][1])


#Fonction qui permet de faire un virement d'un utilisateur à un autre mais aussi d'un compte à un autre pour un même utilisateur
def virement(fichier,cle,compte_donneur):
    liste_users = recuperation_user(repertoire("ident.txt"),23)
    listes_donnee_donneur = recuperation_donnee(fichier,cle)
    id_donneur = ""
    for elt in fichier.split("/")[-1]:
         if elt in "0123456789":
            id_donneur += elt
    id_destinataire = input(f"Veuillez entrer l'identifiant du destinataire: ")
    compteur = 0
    for indice in range(len(liste_users)):
        if id_destinataire == liste_users[indice]["identifiant"]:
            compteur += 1
            nom_destinataire= liste_users[indice]["nom"]
            cle_destinataire = liste_users[indice]["cle"]
            listes_donnee_destinataire = recuperation_donnee(repertoire(id_destinataire+".txt"),int(cle_destinataire))      
        if  id_donneur == liste_users[indice]["identifiant"]:
            nom_donneur = liste_users[indice]["nom"]
    if compteur == 0:
        print("Cette identifiant n'existe pas.")
        print('-'*50)
        gestion_de_compte(fichier,cle,compte_donneur)
    compte_destinataire = input(f"Veuillez entrer le nom du compte du destinataire. Ex: 'Compte A'; ")
    if ["CPT",compte_destinataire] not in listes_donnee_destinataire:
        print("Ce destinataire ne possède pas ce compte.\n")
        print('-'*50)
        return virement(fichier,cle,compte_donneur)
    montant=(input(f"Entrer le montant du virement: "))
    if float(montant) < 0:
        print("Le montant ne peut pas être négatif.")
        print('-'*50)
        return virement(fichier,cle,compte_donneur)
    print('-'*50)
    jour=input(f"Entrer le jour du virement: ")
    print('-'*50)
    mois=input(f"Entrer le mois du virement: ")
    print('-'*50)
    annee=input(f"Entrer l'année du virement: ")
    print('-'*50)
    date=jour+'/'+mois+'/'+annee 
    motif=input(f"Entrer la motif du virement: ")
    budget = "aucun"
    print('-'*50)      
    ope_donneur=["OPE",date,motif,compte_donneur,"-"+montant,"VIR","True",budget,nom_destinataire,compte_destinataire]
    ope_destinaire = ["OPE",date,motif,compte_destinataire,montant,"VIR","True",budget,nom_donneur,compte_donneur]
    listes_donnee_donneur.append(ope_donneur)
    solde = ""
    for elt in solde_utilisateur(fichier,cle,compte_donneur).split(":")[-1]: #Le donneur aura donc dans son fichier une opération False qui ne sera pas comptabilisé dans son solde.
        if elt not in " €\n":
            solde+=elt
    if id_destinataire == id_donneur:
            if float(solde) < 0:
                print("Virement refuser.\n")
                del listes_donnee_donneur[-1] 
                listes_donnee_donneur.append(["OPE",date,motif,compte_donneur,"-"+montant,"VIR","False",nom_destinataire,compte_destinataire])
                sauvegarde(fichier,cle,listes_donnee_donneur)
                print('-'*50)
                gestion_de_compte(fichier,cle,compte_donneur)
            listes_donnee_donneur.append(ope_destinaire)
            print(sauvegarde(fichier,cle,listes_donnee_donneur))
            print('-'*50)
            gestion_de_compte(fichier,cle,compte_donneur)
    if float(solde) < 0:
        print("Virement refuser.\n")
        del listes_donnee_donneur[-1] 
        listes_donnee_donneur.append(["OPE",date,motif,compte_donneur,"-"+montant,"VIR","False",nom_destinataire,compte_destinataire])
        sauvegarde(fichier,cle,listes_donnee_donneur)
        print('-'*50)
        gestion_de_compte(fichier,cle,compte_donneur)
    listes_donnee_destinataire.append(ope_destinaire)
    print(sauvegarde(fichier,cle,listes_donnee_donneur))
    sauvegarde(repertoire(id_destinataire+".txt"),int(cle_destinataire),listes_donnee_destinataire)
    print('-'*50)
    gestion_de_compte(fichier,cle,compte_donneur)
    

#Fonction qui permet à l'utilisateur d'entrer une nouvelle opération et de l'ajouter à son fichier.
def ajou_ope(fichier,cle,compte):
    listes_donnee_user = recuperation_donnee(fichier,cle)  
    jour=input(f"Entrer le jour de l'opération: ")
    print('-'*50)
    mois=input(f"Entrer le mois de l'opération: ")
    print('-'*50)
    annee=input(f"Entrer l'année de l'opération numéro: ") 
    print('-'*50)
    date=jour+'/'+mois+'/'+annee 
    description=input(f"Entrer la libellé de l'opération: ")
    print('-'*50)
    montant=(input(f"Entrer le montant de l'opération avec un - si l'opératon est un achat: "))
    print('-'*50)
    moyen_payement=input(f"Entrer le moyen de payement (CHE,CB,VIR) de l'opération: ")
    if moyen_payement not in ["CHE","CB","VIR"]:
        print("Ce moyen de payement n'existe pas.\n")
        print('-'*50)
        return ajou_ope(fichier,cle,compte)
    if float(montant) > 0 and moyen_payement not in  ["CHE","VIR"]:
        print("Vous pouvez ajouter de l'argent que par chèque ou virement.\n")
        print('-'*50)
        return ajou_ope(fichier,cle,compte)
    print('-'*50)
    validation=input(f"Votre opération à t-elle été validé ?: ")
    if validation.upper() == "OUI":
        validation = "True"
    if validation.upper() == "NON":
        validation = "False"       
    print('-'*50)
    budget=input(f"Entrer le budget concerné de votre opération: ")
    #if ["BUD",budget.lower(),str,compte] not in listes_donnee_user: (une manière plus rapide que nous n'avons pas réussi à exploiter.)
    compteur_bud = 0
    if budget.lower() != "aucun":
        for i in range(len(listes_donnee_user)):
            if listes_donnee_user[i][0]=="BUD" and listes_donnee_user[i][1]== budget.lower() and listes_donnee_user[i][3]== compte:
                compteur_bud += 1
        if compteur_bud == 0:
            print("Ce budget n'existe pas. Veuillez l'ajouter à vôtre compte.\n")
            print('-'*50)
            return ajou_ope(fichier,cle,compte)
    print('-'*50)
    ope=["OPE",date,description,compte,montant,moyen_payement,validation,budget.lower()]
    if ope in listes_donnee_user:
        print("Cette opération existe déja.\n")
        print('-'*50)
        return ajou_ope(fichier,cle,compte)
    listes_donnee_user.append(ope)
    print(sauvegarde(fichier,cle,listes_donnee_user))
    print('-'*50)
    gestion_de_compte(fichier,cle,compte)


#Gérer les budgets du compte choisit par l'utilisateur (A faire)
def gestion_de_bugdet(fichier,cle,compte):
    print("-"*200)
    listes_donnee_user = recuperation_donnee(fichier,cle)
    print(solde_utilisateur(fichier,cle,compte))
    action_user = input("Accéder à un budget, tapez 1.\n\nCréer un budget, tapez 2.\n\nSélectionner un autre compte, tapez 3.\n\nRetourner en arrière, tapez 4.\n\nAppuyer 'Entrer' pour quitter; ")
    if action_user == "":
        exit()
    if action_user not in  "1234":
        print("Erreur.\n")
        print("-"*200)
        return gestion_de_bugdet(fichier,cle,compte)
    if action_user == "1":
        print("-"*200)
        return solde_budget(fichier,cle,compte)
    if action_user == "2":
        print("-"*200)
        return ajou_bugdet(fichier,cle,compte)
    if action_user == "3":
        print("-"*200)
        compte_user = input("Veuillez entrer le compte que vous voulez traitez. Exemple : 'Compte A'.\n\nAppuyer 'Entrer' pour quitter ; ")
        if compte_user == "":
            exit()
        if ['CPT',compte_user] not in listes_donnee_user:
            print("Le compte n'existe pas.\n")
            print("-"*200)
            return gestion_de_bugdet(fichier,cle,compte)  
        return gestion_de_bugdet(fichier,cle,compte_user)
    print("-"*200)
    if action_user == "4":
        print("-"*200)
        fenetre_de_bord(fichier,cle,listes_donnee_user[0][1])


#Fonction qui permet à l'utiliseur de creer un nouveau budget et de l'ajouter à son fichier
def ajou_bugdet(fichier,cle,compte):
    listes_donnee_user = recuperation_donnee(fichier,cle)
    print('-'*50)
    categorie=input(f"Entrer le libellé de votre budget: ")
    print('-'*50)
    montant=input(f"Entrer le montant maximal de votre budgets: ")
    print('-'*50)
    #if ["BUD",categorie.lower(),str(),compte] in listes_donnee_user: (pareil)
    for indice in range(len(listes_donnee_user)):
        if listes_donnee_user[indice][0]=="BUD" and listes_donnee_user[indice][1]== categorie.lower() and listes_donnee_user[indice][3]== compte:
            print("Ce budget existe déja.\n")
            print('-'*50)
            return ajou_bugdet(fichier,cle,compte)
    listes_donnee_user.append(["BUD",categorie.lower(),montant,compte])
    print(sauvegarde(fichier,cle,listes_donnee_user))
    print('-'*50)
    gestion_de_bugdet(fichier,cle,compte)


#Fonction qui affiche le montant du budget demander par l'utilisateur ainsi que le totale des dépenses dans ce dernier et dans un mois donner.
def solde_budget(fichier,cle,compte):
    listes_donnee_user = recuperation_donnee(fichier,cle)
    bud = input("Veuillez entrer le budget que vous voulez consulter ; ") #Il faudra faire attention au (espace, maj, accent, 's').
    #if ["BUD",budget_user.lower(),"400",compte_user] not in listes_donnee_user: (pareil que pour la fonction ajou_ope())
    compteur_bud = 0
    for indice in range(len(listes_donnee_user)):
        if listes_donnee_user[indice][0]=="BUD" and listes_donnee_user[indice][1]== bud.lower() and listes_donnee_user[indice][3]== compte:
            compteur_bud += 1
    if compteur_bud == 0:
        print("Ce budget n'existe pas ou ne fait pas partie du "+compte+"\n")
        print("-"*200)
        return solde_budget(fichier,cle,compte)
    annee_ope = input("Veuillez en entrer l'année que vous voulez conuslter ; ")
    mois_ope = input("Veuillez en entrer le mois que vous voulez conuslter ; ")
    date = mois_ope+"/"+annee_ope
    print(solde_utilisateur(fichier,cle,compte))
    ope_cpt = "Opération lié à ce budget:\n\n"
    achat = []
    totale = 0
    for indice in range(len(listes_donnee_user)):
        #if ["BUD",bud,str,compte] in listes_donnee_user: (pareil)
        if listes_donnee_user[indice][0]=="BUD" and listes_donnee_user[indice][1]== bud and listes_donnee_user[indice][3]== compte:
            montant_bud = listes_donnee_user[indice][2]
            print(f"Budget '{bud}' à ne pas dépasser: {montant_bud}€\n")
        if listes_donnee_user[indice][0]=="OPE" and "/"+date in listes_donnee_user[indice][1] and listes_donnee_user[indice][3] == compte and float(listes_donnee_user[indice][4])<0 and listes_donnee_user[indice][6]=="True" and listes_donnee_user[indice][7]==bud:
            ope_cpt+=f"Date: {listes_donnee_user[indice][1]}, Budget: {bud}, Motif: {listes_donnee_user[indice][2]}, Dépenses: {listes_donnee_user[indice][4]}€, Moyen de payement utilisé: {listes_donnee_user[indice][5]}\n"
            achat.append(listes_donnee_user[indice][4])
    if ope_cpt == "Opération lié à ce budget:\n\n": #Condition qui remplace ("aucune opération corespondante dans ce mois" dans gestion_de_budget)
        ope_cpt+="Aucune opération valide.\n"
    print(solde_utilisateur(fichier,cle,compte))
    print(ope_cpt)
    for indice in range(len(achat)):
        totale += float(achat[indice])
    solde = float(montant_bud) + totale
    print(f"Vous avez utiliser dans ce budget: {str(totale)}€\n\nVotre budget est donc de: {str(solde)}€\n")
    if solde < 0:
        print("Votre budget a été dépasser\n")
    print("-"*200)
    gestion_de_bugdet(fichier,cle,compte)


#Fenêtre qui demande à l'utilisateur si il veut gérer ses comptes ou ses budgets
def fenetre_de_bord(fichier,cle,compte):
    action_user = input("Accéder à la gestion de compte, tapez 1.\n\nAccéder à la gestion de buget, tapez 2.\n\nRetourner à l'identification, tapez 3.\n\nAppuyer 'Entrer' pour quitter; ")
    if action_user == "":
        exit()
    if action_user not in "123":
        print("Erreur")
        return fenetre_de_bord(fichier,cle)
    if action_user == "1":
        return gestion_de_compte(fichier,cle,compte)
    if action_user == "2":
        return gestion_de_bugdet(fichier,cle,compte)
    if action_user == "3":
        return simulation(repertoire("ident.txt"),23)


#Lancement du simulateur d'application de banque qui contient. Phase d'identification --> Fenêtre de bord --> Gestion de compte ou Gestion de Budget
def simulation(fichier,cle):
    print("-"*200)
    print("Bienvenue dans ParisCitéBank")
    id = input("Veuillez entrez votre identifiant à 8 chiffre:" )
    if id == "":
        exit()
    for caractere in id:
        if caractere not in "0123456789":
            print("Veuillez entrez que des chiffre.\n")
            return simulation(fichier,cle)
    if len(id) != 8:
        print("Le nombre de chiffre entrer est incorrect.\n")
        return simulation(fichier,cle)
    mdp = input("Veuillez entrez votre mot de passe:" )
    for caractere in mdp:
        if caractere not in "0123456789":
            print("Veuillez entrez que des chiffre.\n")
            return simulation(fichier,cle)
    if len(mdp) != 6:
        print("Le nombre de chiffre entrer est incorrect.\n")
        return simulation(fichier,cle)
    liste_user = recuperation_user(fichier,cle)
    for indice in range(len(liste_user)):
        if id == liste_user[indice]["identifiant"] and mdp == liste_user[indice]["motdepasse"]:
            liste_donnee_user = recuperation_donnee(repertoire(id+".txt"),int(liste_user[indice]["cle"]))
            print("-"*200)
            print("Connexion réussi !!!\n\n"+"Bonjour "+ liste_user[indice]["nom"]+"\n")
            print(solde_utilisateur(repertoire(liste_user[indice]["identifiant"]+".txt"),int(liste_user[indice]["cle"]),liste_donnee_user[0][1]))
            print("-"*200)
            return fenetre_de_bord(repertoire(liste_user[indice]["identifiant"]+".txt"),int(liste_user[indice]["cle"]),liste_donnee_user[0][1])
    else:
        print("Identifiant ou mot de passe incorrect.\n")
        print("-"*200)
        return simulation(fichier,cle)


#print(recuperation_donnee(repertoire("23456789.txt"),24))
#print("-"*200)
#print(recuperation_donnee(repertoire("90678452.txt"),89))
print("-"*200)
print(recuperation_user(repertoire("ident.txt"),23))
print("-"*200)
#print(simulation(repertoire("ident.txt"),23))

