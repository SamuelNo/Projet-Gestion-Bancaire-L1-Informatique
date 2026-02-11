import tkinter as tk
import customtkinter as ctk
from tkinter import  messagebox
from recuperation import recuperation_donnee,recuperation_user
from liste_deroulantes import liste_deroulante, liste_deroulante_bud
import datetime
import cesar
from tkcalendar import Calendar
from Settings import *

def sauvegarde(fichier,cle,listes_de_donnee: list) -> None:
    listes_de_donnee = sorted(listes_de_donnee, key = len)
    chaine = ""
    with open(cesar.repertoire(fichier),"w") as file:
        for indice in range(len(listes_de_donnee)):
            chaine += "*".join(listes_de_donnee[indice])+"\n" 
        file.write(cesar.cryptage(chaine,cle))
    file.close()


def validate(libelle: str,montant: str) -> str:
    """
    Vérifie si l'utilisateur rentre bien un entier ou un float
    """
    result = libelle!=''
    if montant.isdigit():
        result2=True
    else:
        montant = montant.replace(",", ".")
    try:
        float(montant)
        result2=True
    except ValueError:
        result2=False
    if result and result2:
        return montant
    else:
        return ''
    

def on_close(fenetre,button_d_acces):
    button_d_acces.configure(state='normal')
    fenetre.destroy()

def on_click_buttonvalider_ajout_compte(fichier,cle,champ_nom_compte,champ_solde,menu_page_gestion_compte,page_ajout_compte,button_d_acces):
    nom_compte=champ_nom_compte.get()
    solde=champ_solde.get()
    if validate(nom_compte,solde)!='':
        ajd=datetime.date.today()
        listes_donnee_user = recuperation_donnee(fichier,cle)
        listes_donnee_user.append(["CPT",nom_compte])
        listes_donnee_user.append(["OPE",f'{ajd:%d/%m/%Y}','Ouverture de compte',nom_compte,validate(nom_compte,solde),'VIR','True','aucun'])
        listes_donnee_user.append(["BUD","aucun","0",nom_compte])
        sauvegarde(fichier,cle,listes_donnee_user)
        menu_page_gestion_compte.configure(values=liste_deroulante(fichier,cle,'CPT'))
        messagebox.showinfo("Super", "Votre compte à bel et bien été ajouté")
        on_close(page_ajout_compte,button_d_acces)
    else:
        messagebox.showwarning("Attention","Saisie incorrect")

def compte(fichier,cle,fenetre,button_d_acces,menu_page_gestion_compte) -> None:
    """
    Ajoute un compte en ouvrant une page pour que l'utilisateur rentre les infos nécessaires
    """
    button_d_acces.configure(state='disabled')
    page_ajout_compte=ctk.CTkToplevel(fenetre)
    label1=ctk.CTkLabel(page_ajout_compte,text="Veuiller entrer le nom de votre nouveau compte")
    label1.pack()
    champ_nom_compte=ctk.CTkEntry(page_ajout_compte, placeholder_text='Nom du compte')
    champ_nom_compte.pack()
    label2=ctk.CTkLabel(page_ajout_compte,text="Veuiller entrer le solde initial de ce compte")
    label2.pack()
    champ_solde=ctk.CTkEntry(page_ajout_compte, placeholder_text="Solde du compte")
    champ_solde.pack()
    page_ajout_compte.protocol('WM_DELETE_WINDOW', lambda: on_close(page_ajout_compte,button_d_acces))
    buttonv=ctk.CTkButton(page_ajout_compte, text='valider', command=lambda: on_click_buttonvalider_ajout_compte(fichier,cle,champ_nom_compte,champ_solde,menu_page_gestion_compte,page_ajout_compte,button_d_acces))
    buttonv.pack()

# def choix_budget(fenetre,button,button_initial,fichier,cle,compte,liste_info_ope):
#     button.configure(state='disabled')
#     page_choix=ctk.CTkToplevel(fenetre)
#     liste_derou=liste_deroulante_bud(fichier,cle,compte)
#     menu_budget=ctk.CTkOptionMenu(page_choix, values=liste_derou)
#     menu_budget.pack()
#     page_choix.protocol('WM_DELETE_WINDOW',lambda: on_close(page_choix,button))
#     def action(fichier,cle,liste_ope):
#         liste_donnee=recuperation_donnee(fichier,cle)
#         liste_donnee.append(liste_ope)
#         sauvegarde(fichier,cle,liste_donnee)
#         messagebox.showinfo("Super", "Votre opération à bel et bien été ajoutée")
#     def on_click(fichier,cle,liste):
#         menu=menu_budget.get()
#         liste.append(menu)
#         action(fichier,cle,liste)
#         page_choix.destroy()
#         fenetre.destroy()
#         button_initial.configure(state='normal')
#     button_valider=ctk.CTkButton(page_choix,text='Valider',command=lambda: on_click(fichier,cle,liste_info_ope))
#     button_valider.pack()

def on_click_buttonvalider_ajout_operation(fichier,cle,page,button_d_acces,compte_selectionner,champ_date,champ_libelle,checkbox_signe_operation,champ_montant,menu_moyen_payement,checkbox_resultat,menu_budget):
    date=champ_date.get_date()
    libelle=champ_libelle.get()
    # compte=menu_compte.get()
    signe=checkbox_signe_operation.get()
    montant=champ_montant.get()
    moyen_payement=menu_moyen_payement.get()
    resultat=checkbox_resultat.get()
    budget=menu_budget.get()
    if validate(libelle,signe+montant)!='':
        liste_ope=['OPE',date,libelle,compte_selectionner,validate(libelle,signe+montant),moyen_payement,resultat,budget]
        liste_donnee=recuperation_donnee(fichier,cle)
        liste_donnee.append(liste_ope)
        sauvegarde(fichier,cle,liste_donnee)
        messagebox.showinfo("Super", "Votre opération à bel et bien été ajoutée")
        on_close(page,button_d_acces)
    else:
         messagebox.showwarning("Attention","Saisie Incorrect")


def operation(fichier,cle,fenetre,button_d_acces,menu_cpt) -> None:
    """
    Ajoute une opération en ouvrant une page pour que l'utilisateur rentre les infos nécessaires
    """
    compte_selectionner=menu_cpt.get()
    button_d_acces.configure(state='disabled')
    page=ctk.CTkToplevel(fenetre)
    label1=ctk.CTkLabel(page,text="Veuiller choisir la date de l'opération")
    label2=ctk.CTkLabel(page,text="Veuiller entrer le libellé de l'opération")
    label3=ctk.CTkLabel(page,text="Veuiller entrer le montant de votre opération")
    label4=ctk.CTkLabel(page,text="Veuiller choisir votre moyen de payement")
    label5=ctk.CTkLabel(page,text="Veuiller choisir votre budget")
    champ_date=Calendar(page, locale='fr_FR', date_pattern='dd/mm/yyyy')
    
    champ_libelle=ctk.CTkEntry(page, placeholder_text="Libellé")
    # menu_compte=ctk.CTkOptionMenu(page, values=liste_deroulante(fichier,cle,'CPT'))
    menu_budget=ctk.CTkOptionMenu(page, values=liste_deroulante_bud(fichier,cle,compte_selectionner))
    checkbox_signe_operation=ctk.CTkCheckBox(page, onvalue='-', offvalue='',text="L'opération est elle négatif ?")
    champ_montant=ctk.CTkEntry(page, placeholder_text="Montant")
    menu_moyen_payement=ctk.CTkOptionMenu(page, values=['CB','CHE','ESP'])
    checkbox_resultat=ctk.CTkCheckBox(page, text="L'opération est elle valide", onvalue='True',offvalue='False')
    label1.pack()
    champ_date.pack()
    label2.pack()
    champ_libelle.pack()
    # menu_compte.pack()
    label5.pack()
    menu_budget.pack()
    checkbox_signe_operation.pack()
    label3.pack()
    champ_montant.pack()
    label4.pack()
    menu_moyen_payement.pack()
    checkbox_resultat.pack()
    button_valider=ctk.CTkButton(page, text='valider', command=lambda:on_click_buttonvalider_ajout_operation(fichier,cle,page,button_d_acces,compte_selectionner,champ_date,champ_libelle,checkbox_signe_operation,champ_montant,menu_moyen_payement,checkbox_resultat,menu_budget))
    button_valider.pack()
    page.protocol('WM_DELETE_WINDOW',lambda:on_close(page,button_d_acces))

def on_click_buttonvalider_ajout_budget(fichier,cle,champ_libelle,champ_montant,menu_compte,page,button_d_acces):
    libelle=champ_libelle.get()
    montant=champ_montant.get()
    compte=menu_compte.get()
    listes_donnee_user=recuperation_donnee(fichier,cle)
    if validate(libelle,montant)!='' and float(montant)>float(0):
        for indice in range(len(listes_donnee_user)):
            if listes_donnee_user[indice][0]=="BUD" and listes_donnee_user[indice][1]==libelle and listes_donnee_user[indice][3]== compte:
                messagebox.showwarning("Erreur","Ce budget existe déja.")
        listes_donnee_user.append(["BUD",libelle,validate(libelle,montant),compte])
        sauvegarde(fichier,cle,listes_donnee_user)
        messagebox.showinfo("Super", "Votre ajout à bel et bien été effectué")
        on_close(page,button_d_acces)
    else:
        messagebox.showwarning('Attention','Saisie Incorrect (le budget doit être strictement positif)')

def budget(fichier,cle,fenetre,button_d_acces):
    """
    Ajoute un budget en ouvrant une page pour que l'utilisateur rentre les infos nécessaires
    """
    button_d_acces.configure(state='disabled')
    page=ctk.CTkToplevel(fenetre)
    label1=ctk.CTkLabel(page,text="Entrer le libellé de votre budget: ")
    label1.pack()
    champ_libelle=ctk.CTkEntry(page,placeholder_text="Libellé")
    champ_libelle.pack()
    label2=ctk.CTkLabel(page,text="Entrer le montant maximal de votre budgets: ")
    label2.pack()
    champ_montant=ctk.CTkEntry(page,placeholder_text="Montant")
    champ_montant.pack()
    label3=ctk.CTkLabel(page,text="Veuiller choisir votre compte")
    label3.pack()
    menu_compte=ctk.CTkOptionMenu(page,values=liste_deroulante(fichier,cle,'CPT'))
    menu_compte.pack()
    button_valider=ctk.CTkButton(page, text='valider', command=lambda: on_click_buttonvalider_ajout_budget(fichier,cle,champ_libelle,champ_montant,menu_compte,page,button_d_acces))
    button_valider.pack()
    page.protocol('WM_DELETE_WINDOW',lambda: on_close(page,button_d_acces))

def on_click_buttonvalider_ajout_virement(fichier,cle,page,button_d_acces,champ_libelle,champ_montant,compte_selectionner,menu_compte_destinataire,menu_date,checkbox_resultat,checkbox_signe_operation):
    libelle=champ_libelle.get()
    montant=champ_montant.get()
    # compte_expediteur=menu_compte_expediteur.get()
    compte_expediteur=compte_selectionner
    compte_destinataire=menu_compte_destinataire.get()
    date=menu_date.get_date()
    validiter=checkbox_resultat.get()
    signe=checkbox_signe_operation.get()
    if validate(libelle,signe+montant)!='':
        liste_vir_expediteur=['OPE',date,libelle,compte_expediteur,validate(libelle,signe+montant),'VIR',validiter,'aucun']
        list_vir_destinataire=['OPE',date,libelle,compte_destinataire,validate(libelle,montant),'VIR',validiter,'aucun']
        liste_donnee=recuperation_donnee(fichier,cle)
        liste_donnee.append(liste_vir_expediteur)
        liste_donnee.append(list_vir_destinataire)
        sauvegarde(fichier,cle,liste_donnee)
        on_close(page,button_d_acces)
    else:
        messagebox.showwarning("Attention","Saisie incorrect")

def virement(fichier,cle,fenetre,button_d_acces,menu_compte):
    """
    Ajoute un virement en ouvrant une page pour que l'utilisateur rentre les infos nécessaires
    """
    compte_selectionner=menu_compte.get()
    button_d_acces.configure(state='disabled')
    page=ctk.CTkToplevel(fenetre)
    label1=ctk.CTkLabel(page,text="Veuiller choisir la date de l'opération")
    label2=ctk.CTkLabel(page,text="Veuiller entrer le libellé de l'opération")
    label3=ctk.CTkLabel(page,text="Veuiller entrer le montant de votre opération")
    label4=ctk.CTkLabel(page,text="Veuiller choisir le compte de destination")
    checkbox_signe_operation=ctk.CTkCheckBox(page,text='Cette opération est elle négatif ?', onvalue='-', offvalue='',state=tk.DISABLED)
    checkbox_signe_operation.select()
    champ_montant=ctk.CTkEntry(page,placeholder_text='Montant')
    # menu_compte_expediteur=ctk.CTkOptionMenu(page, values=liste_deroulante(fichier,cle,'CPT'))
    menu_budget=ctk.CTkOptionMenu(page)
    menu_compte_destinataire=ctk.CTkOptionMenu(page, values=liste_deroulante(fichier,cle,'CPT'))
    menu_date=Calendar(page,locale='fr_FR', date_pattern='dd/mm/yyyy')
    checkbox_resultat=ctk.CTkCheckBox(page, text="L'opération est elle valide", onvalue='True',offvalue='False')
    champ_libelle=ctk.CTkEntry(page, placeholder_text="Libellé")
    label1.pack()
    menu_date.pack()
    label2.pack()
    champ_libelle.pack()
    checkbox_signe_operation.pack()
    label3.pack()
    champ_montant.pack()
    # menu_compte_expediteur.pack()
    label4.pack()
    menu_compte_destinataire.pack()
    checkbox_resultat.pack()
    button_valider=ctk.CTkButton(page, text="Valider", command=lambda:on_click_buttonvalider_ajout_virement(fichier,cle,page,button_d_acces,champ_libelle,champ_montant,compte_selectionner,menu_compte_destinataire,menu_date,checkbox_resultat,checkbox_signe_operation))
    button_valider.pack()
    page.protocol('WM_DELETE_WINDOW',lambda: on_close(page,button_d_acces))


def action_virement_externe2(fichier,cle,fenetre,button_d_acces,id_destinataire,cle_destinataire,menu_compte_donneur,montant,nom_destinataire,compte_destinataire,nom_donneur,date,libelle,listes_donnee_donneur,listes_donnee_destinataire):
    compte_donneur=menu_compte_donneur.get()
    ope_donneur=["OPE",date,libelle,compte_donneur,"-"+montant,"VIR","True",'aucun',nom_destinataire,compte_destinataire]
    ope_destinaire = ["OPE",date,libelle,compte_destinataire,"+"+montant,"VIR","True",'aucun',nom_donneur,compte_donneur]
    listes_donnee_donneur.append(ope_donneur)
    listes_donnee_destinataire.append(ope_destinaire)
    sauvegarde(fichier,cle,listes_donnee_donneur)
    sauvegarde(id_destinataire+".txt",int(cle_destinataire),listes_donnee_destinataire)
    messagebox.showinfo('Super','Votre virement à bel et bien été enregistré')
    button_d_acces.configure(state='normal')
    fenetre.destroy()


def action_virement_externe1(fichier,cle,fenetre,button,button2,champ_id_destinataire,champ_montant,champ_libelle,champ_date,menu_compte_donneur):
    id_destinataire=champ_id_destinataire.get()
    montant=champ_montant.get()
    libelle=champ_libelle.get()
    date=champ_date.get_date()
    compte_destinataire=menu_compte_donneur.get()
    liste_users=recuperation_user('ident.txt',23)
    listes_donnee_donneur = recuperation_donnee(fichier,cle)
    existe = False
    id_donneur = ""
    for elem in fichier.split("/")[-1]:
         if elem in "0123456789":
            id_donneur += elem
    for indice in range(len(liste_users)):
        if id_destinataire == liste_users[indice]["identifiant"]:
            existe = True
            nom_destinataire= liste_users[indice]["nom"]
            cle_destinataire = liste_users[indice]["cle"]
            listes_donnee_destinataire = recuperation_donnee(id_destinataire+".txt",int(cle_destinataire))
        if  id_donneur == liste_users[indice]["identifiant"]:
            nom_donneur = liste_users[indice]["nom"]
    if not existe:
        messagebox.showwarning("Erreur","Le destinataire n'a pas de compte BNP ParisCité")
    elif not validate(libelle,montant):
        messagebox.showwarning("Erreur","Saisie incorrect")
    elif id_destinataire==id_donneur:
        messagebox.showwarning("Erreur","Si vous voulez vous faire un virement aller dans la section ajout virement interne")
    else:
        new_app=ctk.CTkToplevel(fenetre)
        button2.configure(state='disabled')
        new_app.protocol("WM_DELETE_WINDOW",lambda: on_close(new_app,button2))
        menu_compte_destinataire=ctk.CTkOptionMenu(new_app, values=liste_deroulante(id_destinataire+".txt",int(cle_destinataire),'CPT'))
        menu_compte_destinataire.pack()
        button_valider=ctk.CTkButton(new_app,text='Valider',command=lambda: action_virement_externe2(fichier,cle,fenetre,button,id_destinataire,cle_destinataire,menu_compte_donneur,montant,nom_destinataire,compte_destinataire,nom_donneur,date,libelle,listes_donnee_donneur,listes_donnee_destinataire))
        button_valider.pack()

def virement_externe(fichier,cle,fenetre,button):
    page=ctk.CTkToplevel(fenetre)
    button.configure(state='disabled')
    page.protocol("WM_DELETE_WINDOW",lambda: on_close(page,button))
    label1=ctk.CTkLabel(page,text="Veuiller choisir la date de l'opération")
    label2=ctk.CTkLabel(page,text="Veuiller entrer le libellé de l'opération")
    label3=ctk.CTkLabel(page,text="Veuiller entrer le montant de votre opération")
    label4=ctk.CTkLabel(page,text="Veuiller entrer l'identifiant du destinataire")
    champ_id_destinataire=ctk.CTkEntry(page, placeholder_text="Veuillez entrer l'identifiant du destinataire: ")
    champ_date=Calendar(page, locale='fr_FR', date_pattern='dd/mm/yyyy')
    champ_libelle=ctk.CTkEntry(page, placeholder_text="Veuiller entrer le libellé de l'opération")
    champ_montant=ctk.CTkEntry(page, placeholder_text="Veuiller entrer le montant de votre opération")
    menu_compte_donneur=ctk.CTkOptionMenu(page, values=liste_deroulante(fichier,cle,'CPT'))
    label1.pack()
    champ_date.pack()
    label4.pack()
    champ_id_destinataire.pack()
    label2.pack()
    champ_libelle.pack()
    label3.pack()
    champ_montant.pack()
    button_valider=ctk.CTkButton(page, text='Valider',command=lambda: action_virement_externe1(fichier,cle,page,button,button_valider,champ_id_destinataire,champ_montant,champ_libelle,champ_date,menu_compte_donneur))
    button_valider.pack()
