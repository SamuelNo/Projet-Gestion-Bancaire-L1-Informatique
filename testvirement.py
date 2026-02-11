import tkinter as tk
import customtkinter as ctk
from tkinter import  messagebox
from liste_deroulantes import liste_deroulante, liste_deroulante_bud
import datetime
import cesar
import os
import re
from tkcalendar import Calendar
from recuperation import recuperation_donnee, recuperation_user
from ajout import sauvegarde

def repertoire(nom_fichier: str) -> str:
    """
    :param nom_fichier: le nom du fichier avec l'extension .txt
    :return: le chemin d'accès absolue du fichier
    """
    chemin_python=os.path.dirname(__file__)
    chemin_fichier=os.path.join(chemin_python,'Users',nom_fichier)
    return chemin_fichier

def virement(fichier,cle):
    app=ctk.CTk()
    app.geometry('900x600')
    champ_id_destinataire=ctk.CTkEntry(app, placeholder_text="Veuillez entrer l'identifiant du destinataire: ")
    champ_date=Calendar(app, locale='fr_FR', date_pattern='dd/mm/yyyy')
    champ_libelle=ctk.CTkEntry(app, placeholder_text="Veuiller entrer le libellé de l'opération")
    champ_montant=ctk.CTkEntry(app, placeholder_text="Veuiller entrer le montant de votre opération")
    menu_compte_donneur=ctk.CTkOptionMenu(app, values=liste_deroulante(fichier,cle,'CPT'))
    champ_id_destinataire.pack()
    champ_date.pack()
    champ_libelle.pack()
    champ_montant.pack()
    button_valider=ctk.CTkButton(app, text='Valider',command=lambda: action(fichier,cle,app,champ_id_destinataire,champ_montant,champ_libelle,champ_date,menu_compte_donneur))
    button_valider.pack()
    app.mainloop()


def action(fichier,cle,fenetre,champ_id_destinataire,champ_montant,champ_libelle,champ_date,menu_compte_donneur):
    id_destinataire=champ_id_destinataire.get()
    montant=champ_montant.get()
    libelle=champ_libelle.get()
    date=champ_date.get_date()
    compte_destinataire=menu_compte_donneur.get()
    liste_users=recuperation_user('ident.txt',23)
    listes_donnee_donneur = recuperation_donnee(fichier,cle)
    id_donneur = ""
    
    for elt in fichier.split("/")[-1]:
         if elt in "0123456789":
            id_donneur += elt
    existe = False
    for indice in range(len(liste_users)):
        if id_destinataire == liste_users[indice]["identifiant"]:
            existe = True
            nom_destinataire= liste_users[indice]["nom"]
            cle_destinataire = liste_users[indice]["cle"]
            listes_donnee_destinataire = recuperation_donnee(repertoire(id_destinataire+".txt"),int(cle_destinataire))      
        if  id_donneur == liste_users[indice]["identifiant"]:
            nom_donneur = liste_users[indice]["nom"]
    if not existe:
        messagebox.showerror("Erreur","Le destinataire n'a pas de compte BNP ParisCité")
    else:
        new_app=ctk.CTkToplevel(fenetre)
        menu_compte_destinataire=ctk.CTkOptionMenu(new_app, values=liste_deroulante(repertoire(id_destinataire+".txt"),int(cle_destinataire),'CPT'))
        menu_compte_destinataire.pack()
        def getter():
            compte_donneur=menu_compte_donneur.get()
            ope_donneur=["OPE",date,libelle,compte_donneur,"-"+montant,"VIR","True",'aucun',nom_destinataire,compte_destinataire]
            ope_destinaire = ["OPE",date,libelle,compte_destinataire,"+"+montant,"VIR","True",'aucun',nom_donneur,compte_donneur]
            listes_donnee_donneur.append(ope_donneur)
            listes_donnee_destinataire.append(ope_destinaire)
            sauvegarde(fichier,cle,listes_donnee_donneur)
            sauvegarde(repertoire(id_destinataire+".txt"),int(cle_destinataire),listes_donnee_destinataire)
            messagebox.showinfo('Super','Votre virement à bel et bien été enregistré')
        button_valider=ctk.CTkButton(new_app,text='Valider',command=getter)
        button_valider.pack()