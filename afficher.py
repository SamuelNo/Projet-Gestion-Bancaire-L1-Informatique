import customtkinter as ctk
from recuperation import recuperation_donnee
from liste_deroulantes import liste_deroulante,liste_deroulante_bud
from tkinter import messagebox
import matplotlib.pyplot as plt
from datetime import datetime
from CTkTable import * 


def solde_utilisateur(fichier,cle,compte)-> str:
    """
    :param compte: Le compte que l'on veut afficher
    """
    achat = []
    solde = 0
    listes_donnee_user = recuperation_donnee(fichier,cle)
    for indice in range(len(listes_donnee_user)):
        if listes_donnee_user[indice][0]=='OPE'and compte == listes_donnee_user[indice][3] and listes_donnee_user[indice][6] == "True":
                achat.append(listes_donnee_user[indice][4])
    for i in range(len(achat)):
        solde += float(achat[i])
    return f'Le solde de {compte} est actuellement de : {solde} €'

def solde_utilisateur2(compte,liste_ope)-> str:
    """
    :param compte: Le compte que l'on veut afficher
    """
    achat = []
    solde = 0
    for indice in range(len(liste_ope)):
        if liste_ope[indice][6] == "True":
                achat.append(liste_ope[indice][4])
    for i in range(len(achat)):
        solde += float(achat[i])
    solde=str(solde)
    return f'Le solde de {compte} est actuellement de : {solde} €'

def solde_budget(fichier,cle,compte,budget) -> float:
    liste_donee=recuperation_donnee(fichier,cle)
    for i in range(len(liste_donee)):
        if liste_donee[i][0]=='BUD' and liste_donee[i][1]==budget and liste_donee[i][3]==compte:
            return float(liste_donee[i][2])

# def pourcentage(fichier,cle,compte,budget, montant, valeur):
#     for i in range(len(montant)):
#         pourcent=((valeur-montant)*100)/valeur
def on_close(app,button_d_acces):
    app.destroy()
    button_d_acces.configure(state='normal')

def visualiser_compte(fichier,cle,menucompte,fenetre,button_d_acces)-> None:
    """
    :param: fenetre: fenetre sur laquel on veut places les objets
    :param: buttons: button grâce auquel on va ouvrir cette pop-up
    """
    compte=menucompte.get()
    button_d_acces.configure(state='disabled')
    liste_operations = []
    listes_donnee_user = recuperation_donnee(fichier,cle)
    page=ctk.CTkToplevel(fenetre)
    for indice in range(len(listes_donnee_user)):

        if listes_donnee_user[indice][0]== "OPE" and compte == listes_donnee_user[indice][3]:
            if (listes_donnee_user[indice][4])[0]!='-' and (listes_donnee_user[indice][4])[0]!='+':
                listes_donnee_user[indice][4]='+'+listes_donnee_user[indice][4]
            liste_operations.append(listes_donnee_user[indice])
    liste_trier=sorted(liste_operations,key= lambda date: datetime.strptime(date[1], "%d/%m/%Y"))
    table_labels = ['Type', 'Date', 'Motif', 'Compte', 'Montant', 'Moyen de payement', 'Vérification', 'Budget']
    table = CTkTable(master=page, column=len(table_labels), values=[table_labels, *liste_trier])
    table.delete_column(0) # delete the 'Type' column
    table.pack()
    # for indice in range(len(liste_trier)):
    #     texte+=f"Date: {liste_trier[indice][1]}, Budget: {liste_trier[indice][7]}, Motif: {liste_trier[indice][2]}, Dépenses: {liste_trier[indice][4]}€, Moyen de payement utilisé: {liste_trier[indice][5]}, Vérification: {liste_trier[indice][6]}\n"
    #     text3.configure(text=texte)
    # text.pack()
    # text2.pack()
    # text3.pack()
    page.protocol('WM_DELETE_WINDOW',lambda: on_close(page,button_d_acces))

def diagramme(button_d_acces,liste_pourcentage_depense,liste_valeur_reel,liste_libelle_depense,pourcentage_total_depense,pourcentage_reste_budget,nom_budget):
    # # figure=plt.subplots()
    # plt.pie(values, labels=libelle, autopct='%.2f%%')
    # plt.title(f'Diagramme circulaire du budget {nom_budget}')
    # plt.show()
    # if pourcentage_reste_budget>100:
    #     pourcentage_reste_budget=100
    # elif pourcentage_reste_budget<0:
    #     pourcentage_reste_budget=0
    
    # if pourcentage_total_depense>100:
    #     pourcentage_total_depense=100
    # elif pourcentage_total_depense<0:
    #     pourcentage_total_depense=0
    fig, axs = plt.subplots(1, 2)
    liste_pourcentage_global=[pourcentage_total_depense,pourcentage_reste_budget]
    for i in range(len(liste_pourcentage_global)):
        if liste_pourcentage_global[i] >float(100):
            liste_pourcentage_global[i]=float(100)
        elif liste_pourcentage_global[i]<float(0):
            liste_pourcentage_global[i]=float(0)
    label_global=['Dépenses','Reste du Budget']
    # Premier diagramme circulaire
    axs[0].pie(liste_pourcentage_depense, labels=liste_libelle_depense, autopct='%1.1f%%')
    axs[0].set_title('Diagramme détailler des dépense')

    # Deuxième diagramme circulaire
    axs[1].pie(liste_pourcentage_global, labels=label_global, autopct='%1.1f%%')
    axs[1].set_title(f'Diagramme Global du budget {nom_budget}')

    # Ajustement de l'espacement entre les sous-graphiques
    plt.tight_layout()

    # Affichage des diagrammes
    plt.show()
    # app=ctk.CTkLabel(fenetre)
    # frame=ctk.CTkFrame(app)
    # canvas=FigureCanvasTkAgg(figure,master=app)
    # canvas.get_ctk_widget().pack()
    # frame.pack()
def plt_ouvert(button):
    messagebox.showwarning("","Un diagramme est déjà ouvert")


def on_click_valider_visualiser_budget(menu_mois: None, menu_annee: None, menu_compte: None, menu_budget: None, fichier:str, cle: int, app: None, button_d_acces: None):
        # raise NotImplemented('Problème de robustesse mois/année')
    mois=menu_mois.get()
    annee=menu_annee.get()
    compte=menu_compte.get()
    nom_budget=menu_budget.get()
    liste_donnee=recuperation_donnee(fichier,cle)
    somme_total_depenses=0
    somme_total_revenues=0
    valeur_budget=solde_budget(fichier,cle,compte,nom_budget)
    operation_introuvable=True
    liste_libelle_depense=[]
    liste_operation=[]
    liste_valeur_reel=[]
    liste_pourcentage_depense=[]
    if valeur_budget==0:
        valeur_budget=0.0001
    for i in range(len(liste_donnee)):
        if 'OPE'==liste_donnee[i][0] and compte==liste_donnee[i][3] and nom_budget==liste_donnee[i][7] and f'{mois}/{annee}' == (liste_donnee[i][1])[3:]:
            liste_operation.append(liste_donnee[i])
            operation_introuvable=False
            if (liste_donnee[i][4])[0]!='-' and (liste_donnee[i][4])[0]!='+':
                liste_donnee[i][4]='+'+liste_donnee[i][4]
            if liste_donnee[i][6]=='True':
                if (liste_donnee[i][4])[0]=='-':
                    somme_total_depenses+=(-1*float(liste_donnee[i][4]))
                    liste_libelle_depense.append(liste_donnee[i][2])
                    liste_valeur_reel.append(-1*float(liste_donnee[i][4]))
                else:
                    somme_total_revenues+=(float(liste_donnee[i][4]))
    if operation_introuvable:
        messagebox.showinfo("Erreur","Aucune opération sur votre recherche")
    else:
        button_d_acces.configure(state="disabled")
        page_affichage=ctk.CTkToplevel(app)
        page_affichage.protocol("WM_DELETE_WINDOW",lambda: on_close(page_affichage,button_d_acces))
        pourcentage_total_depense=((somme_total_depenses-somme_total_revenues)/valeur_budget)*100
        pourcentage_reste_budget=((valeur_budget-(somme_total_depenses-somme_total_revenues))/valeur_budget)*100
        for i in range(len(liste_valeur_reel)):
            pourcentage_chaque_depense=(liste_valeur_reel[i]/somme_total_depenses)*100
            liste_pourcentage_depense.append(pourcentage_chaque_depense)
        table_labels = ['Type', 'Date', 'Motif', 'Compte', 'Montant', 'Moyen de payement', 'Vérification', 'Budget']
        liste_trier=sorted(liste_operation,key= lambda date: datetime.strptime(date[1], "%d/%m/%Y"))
        tableau = CTkTable(master=page_affichage, column=len(table_labels), values=[table_labels, *liste_trier])
        tableau.delete_column(0) # delete the 'Type' column
        texte=ctk.CTkLabel(page_affichage,text=solde_utilisateur(fichier,cle,compte))
        texte2=ctk.CTkLabel(page_affichage,text=f'Votre budget {nom_budget} est de {valeur_budget}')
        texte3=ctk.CTkLabel(page_affichage,text=f'Vous avez dépenser actuellement {somme_total_depenses-somme_total_revenues}€ sur {nom_budget} soit {round(pourcentage_total_depense,2)}% de votre budget')
        texte4=ctk.CTkLabel(page_affichage,text=f'Le montant restant de {nom_budget} est actuellement de {valeur_budget-(somme_total_depenses-somme_total_revenues)}€ soit {round(pourcentage_reste_budget,2)}% de votre budget')
        button_diagramme=ctk.CTkButton(page_affichage,text='Afficher le diagramme', command=lambda : diagramme(button_diagramme,liste_pourcentage_depense,liste_valeur_reel,liste_libelle_depense,pourcentage_total_depense,pourcentage_reste_budget,nom_budget))
        if plt.fignum_exists(1):
            button_diagramme.configure(command=lambda: plt_ouvert(button_diagramme))
        tableau.pack()
        texte.pack()
        texte2.pack()
        texte3.pack()
        texte4.pack()
        button_diagramme.pack()
        
        

# def on_click_valider_visualiser_budget():
#     mois=menu_mois.get()
#     annee=menu_annee.get()
#     compte=menu_compte.get()
#     budget=menu_budget.get()
#     action(mois,annee,compte,budget
def validation(menu_mois,menu_annee,menu_compte,fichier,cle,app,button_d_acces):
    button_d_acces.configure(state="disabled")
    newapp=ctk.CTkToplevel(app)
    newapp.protocol("WM_DELETE_WINDOW",lambda: on_close(newapp,button_d_acces))
    compte=menu_compte.get()
    menu_budget=ctk.CTkOptionMenu(newapp,values=liste_deroulante_bud(fichier,cle,compte))
    menu_budget.pack()
    button_valider=ctk.CTkButton(newapp,text="Valider",command=lambda: on_click_valider_visualiser_budget(menu_mois,menu_annee,menu_compte,menu_budget,fichier,cle,newapp,button_valider))
    button_valider.pack()


def visualiser_budget(fichier,cle,fenetre,button_d_acces):
    button_d_acces.configure(state='disabled')
    app=ctk.CTkToplevel(fenetre)
    chiffres_mois=['01','02','03','04','05','06','07','08','09','10','11','12']
    chiffres_annees=[str(j) for j in range(2014,2034)]
    menu_mois=ctk.CTkOptionMenu(app, values=chiffres_mois)
    menu_annee=ctk.CTkOptionMenu(app, values=chiffres_annees)
    menu_compte=ctk.CTkOptionMenu(app, values=liste_deroulante(fichier,cle,'CPT'))
    texte1=ctk.CTkLabel(app,text="Entrer le mois et l'année")
    texte2=ctk.CTkLabel(app, text="Entrer votre compte")
    texte1.pack()
    menu_mois.pack()
    menu_annee.pack()
    texte2.pack()
    menu_compte.pack()
    button_valider=ctk.CTkButton(app, text='Valider',command=lambda: validation(menu_mois,menu_annee,menu_compte,fichier,cle,app,button_valider))
    button_valider.pack()
    app.protocol('WM_DELETE_WINDOW',lambda: on_close(app,button_d_acces))