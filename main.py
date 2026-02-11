import customtkinter as ctk
from PIL import Image
from tkinter import  messagebox
import random
from Settings import *
import afficher
from liste_deroulantes import liste_deroulante
import ajout
from recuperation import recuperation_user, recuperation_donnee
import matplotlib.pyplot as plt


#Permet d'avoir le chemin d'accès de tous les fichier qui sont dans le dossier Users (dossier qui doit être dans le même dossier que ce ficheir py)
#Grâce à chemin python, cette fonction est utilisable peut importe l'os et l'ordinateur que vous utilisez
# def repertoire(nom_fichier: str) -> str:
#     """
#     :param nom_fichier: le nom du fichier avec l'extension .txt
#     :return: le chemin d'accès absolue du fichier
#     """
#     chemin_python=os.path.dirname(__file__)
#     chemin_fichier=os.path.join(chemin_python,'Users',nom_fichier)
#     return chemin_fichier

def on_close(fenetre: None, button_d_acces: None,fenetre_de_bord: None) -> None:
    """
    Ferme la page gestion de compte et rend de nouveau le bouton qui a permis d'accèder à cette page "cliquable"
    :param fenetre: La page que l'on veut fermer
    :param bouton_d_acces: Le bouton qui a permis d'ouvrir la page que l'on veut fermer (car il était "incliquable")
    """
    fenetre.destroy()
    fenetre_de_bord.deiconify()
    button_d_acces.configure(state='normal')

def on_clicl_vitrual_keyboard(value: str, champ_mdp: None) -> None:
    """
        Fonction qui permet de cliquer sur le bouton 5 par exemple et écrit le 5
        L'utilisateur ne peut plus rentrer plus de 6 chiffres
        :param value: Le chiffre(str) afficher sur le bouton que l'on clique
        :param champ_mdp: L'endroit où l'on écrit notre mdp via le clavier virtuel
    """
    champ_mdp.configure(state='normal')
    current_text = champ_mdp.get()
    champ_mdp.delete(0, ctk.END)
    champ_mdp.insert(ctk.END, current_text + value)
    champ_mdp.configure(state='disabled')
    if len(champ_mdp.get()) > 6:
        champ_mdp.configure(state='normal')
        champ_mdp.delete(6, ctk.END)
        champ_mdp.configure(state='disabled')

def annuler_click(champ_mdp) -> None:
        """
            Fonction qui permet d'effacer un carractère
            :param champ_mdp: L'endroit où l'on écrit notre mdp via le clavier virtuel
        """
        champ_mdp.configure(state='normal')
        nb=champ_mdp.get()
        champ_mdp.delete(len(nb)-1, ctk.END)
        champ_mdp.configure(state='disabled')

def on_close_page_identification(progressbar: None,button_se_connecter: None,page_identification: None) -> None:
    """
    Ferme la page d'identification, la progressbar de la page de de présentation et rend de nouveau le bouton "Se connecter" "cliquable"
    :param progressbar: La progressbar de la page de présentation qui fait office de bar de chargement annimé
    :param button_se_connecter: Le bouton se connecter de la page de présentation (pour le rendre de nouveau "cliquable")
    :param page_identification: La page d'identification (celle que l'on va fermer à l'appel de cette fonction)
    """
    progressbar.destroy()
    button_se_connecter.configure(state='normal', fg_color=LIGHT_BLUE)
    page_identification.destroy()

def on_click_button_login(page_presentation: None,page_de_bord: None,button_login: None) -> None:
    """
    Renvoie la page d'identification et crée une progressbar
    :param page_presentation: La page de présenation
    :param page_de_bord: La page de bord (qui est caché)
    :param button_login: Le bouton "Se connecter"
    """
    progressbar=ctk.CTkProgressBar(page_presentation, orientation='horizontal' ,mode='indeterminate', progress_color=LIGHT_BLUE ,width=200,height=3, fg_color=GREY , indeterminate_speed=0.8)
    progressbar.start()
    progressbar.place(x=92.50,y=465)
    identificatin_page(page_de_bord,page_presentation,button_login,progressbar)

def on_closing_app(page_de_bord: None) -> None:
    """
    Ferme la page de bord qu'elle soit caché ou non
    :param page_de_bord: La page de bord (celle qui contient tous les autres pop-up et donc celle qui ferme l'application)
    """
    if plt.fignum_exists(1):
        messagebox.showwarning("Attention","Vous devez d'abord fermer la fenêtre le diagramme")
    else:
        if messagebox.askokcancel('Attention', "Voulez vous quitter l'application ?"):
            page_de_bord.quit()
            page_de_bord.destroy()


def deconnexion(page_de_bord):
    if messagebox.askokcancel("Attention","Voulez vous vous déconnecter ?"):
        page_de_bord.withdraw()
        for widget in page_de_bord.winfo_children():
            if isinstance(widget,ctk.CTkToplevel):
                widget.destroy()
            else:
                widget.pack_forget()
        presentation_page(page_de_bord)


def gestion_compte_page(chemin_fichier: str,cle: int,compte: str,page_de_bord: None,button_acces_page_compte: None) -> None:
    """
    Affiche la page de gestion de comptes
    :param chemin_fichier: Le chemin d'accès absolue du fichier.txt de l'utilisateur
    :param cle: La cle pour déchiffrer le fichier.txt de l'utilisateur
    :param comtpe: Le premier compte du fichier.txt (compte principal)
    :param page_de_bord: La page de bord (sur laquelle on va créer la pop up gestion de comptes)
    :param button_acces_page_compte: Le bouton d'accès à la page de gestion de comptes (pour le rendre "incliquable")
    """
    page_gestion_compte=ctk.CTkToplevel(page_de_bord, fg_color=DARK_BLUE)
    page_gestion_compte.title('Gestion de comptes')
    page_gestion_compte.geometry(MEDIUM_SIZE_WINDOWS)
    button_acces_page_compte.configure(state='disabled')
    page_gestion_compte.protocol('WM_DELETE_WINDOW',lambda: on_close(page_gestion_compte,button_acces_page_compte,page_de_bord))
    font=ctk.CTkFont(FONT,size=35)
    frame=ctk.CTkFrame(page_gestion_compte,fg_color=DARK_BLUE)
    frame.pack()
    manage_account= ctk.CTkImage(dark_image=Image.open('Fichier 3.png'),size=(50,50))
    add_account=ctk.CTkImage(dark_image=Image.open('add_profil_2.png'),size=(50,50))
    label_profil=ctk.CTkLabel(frame,image=manage_account,text='')
    label_profil.pack(pady=10, side=ctk.LEFT)
    solde_texte=ctk.CTkLabel(page_gestion_compte,text=afficher.solde_utilisateur(chemin_fichier,cle, compte), font=font, text_color=WHITE)
    solde_texte.pack(pady=20)
    menu_compte = ctk.CTkOptionMenu(frame,fg_color=LIGHT_BLUE,button_color=LIGHT_BLUE,button_hover_color=LIGHT_BLUE2, values=liste_deroulante(chemin_fichier,cle,'CPT'),command=lambda x: solde_texte.configure(text=afficher.solde_utilisateur(chemin_fichier,cle,x)))
    menu_compte.pack(side=ctk.LEFT)
    button_visualiser=ctk.CTkButton(page_gestion_compte,width=250,height=40,fg_color=LIGHT_BLUE,hover_color=LIGHT_BLUE2,text='Visualiser votre compte',command=lambda: afficher.visualiser_compte(chemin_fichier,cle,menu_compte,page_gestion_compte,button_visualiser))
    button_visualiser.pack(pady=10)
    button_ajoutcompte=ctk.CTkButton(page_gestion_compte, text='',image=add_account,width=50,height=50,fg_color=DARK_BLUE,hover_color=LIGHT_BLUE2, command=lambda: ajout.compte(chemin_fichier,cle,page_gestion_compte,button_ajoutcompte,menu_compte))
    button_ajoutcompte.place(x=800,y=10)
    button_ajoutoperation=ctk.CTkButton(page_gestion_compte,width=250,height=40,fg_color=LIGHT_BLUE,hover_color=LIGHT_BLUE2, text='Ajouter une opération', command=lambda: ajout.operation(chemin_fichier,cle,page_gestion_compte,button_ajoutoperation,menu_compte))
    button_ajoutoperation.pack(pady=10)
    button_ajoutvirement=ctk.CTkButton(page_gestion_compte,width=250,height=40,fg_color=LIGHT_BLUE,hover_color=LIGHT_BLUE2, text="Ajouter un virement",command=lambda: ajout.virement(chemin_fichier,cle,page_gestion_compte,button_ajoutvirement,menu_compte))
    button_ajoutvirement.pack(pady=10)
    button_ajoutvirement_externe=ctk.CTkButton(page_gestion_compte,width=250,height=40,fg_color=LIGHT_BLUE,hover_color=LIGHT_BLUE2,text="Faire un virement vers un\n autre utilisateur BNP Pariscité",command=lambda: ajout.virement_externe(chemin_fichier,cle,page_gestion_compte,button_ajoutvirement_externe))
    button_ajoutvirement_externe.pack(pady=10)


def gestion_budget_page(chemin_fichier: str,cle: int,page_de_bord: None, button_acces_page_budget: None) -> None:
    """
    Affiche la page de gestion de budgets
    :param chemin_fichier: Le chemin d'accès absolue du fichier.txt de l'utilisateur
    :param cle: La cle pour déchiffrer le fichier.txt de l'utilisateur
    :param page_de_bord: La page de bord (sur laquelle on va créer la pop up gestion de budgets)
    :param button_acces_page_compte: Le bouton d'accès à la page de gestion de budgets (pour le rendre "incliquable")
    """
    page_gestion_budget=ctk.CTkToplevel(page_de_bord, fg_color=DARK_BLUE)
    page_gestion_budget.title('Gestion de Budgets')
    page_gestion_budget.geometry(MEDIUM_SIZE_WINDOWS)
    button_acces_page_budget.configure(state='disabled')
    button_ajoutbudget=ctk.CTkButton(page_gestion_budget,width=250,height=40,fg_color=LIGHT_BLUE,hover_color=LIGHT_BLUE2, text='Ajouter un budget',command=lambda: ajout.budget(chemin_fichier,cle,page_gestion_budget,button_ajoutbudget))
    button_ajoutbudget.pack(pady=100)
    button_visualiser_budget=ctk.CTkButton(page_gestion_budget,width=250,height=40,fg_color=LIGHT_BLUE,hover_color=LIGHT_BLUE2, text='Visualiser vos budgets', command=lambda: afficher.visualiser_budget(chemin_fichier,cle,page_gestion_budget,button_visualiser_budget))
    button_visualiser_budget.pack()
    page_gestion_budget.protocol('WM_DELETE_WINDOW',lambda: on_close(page_gestion_budget,button_acces_page_budget,page_de_bord))

def fenetre_de_bord(chemin_fichier: str,cle: int,nom: str,page_presentation: None,page_identification: None,page_de_bord: None) -> None:
    """
    Affiche la fenêtre de bord (qui avait été créer et cacher au lancemnt du programme)
    et détruit les pages d'identifications grâce à destroy ce qui permet de supprimer toutes les variables créer dans ces pages
    et donc de supprimer le mot de passe de l'utilisateur par sécurité
    :param chemin_fichier: Le chemin d'accès absolue du fichier.txt de l'utilisateur
    :param cle: La cle pour déchiffrer le fichier.txt de l'utilisateur
    :param page_presentation: La page de présentation pour détruire la page et les informations essentiel à l'identification
    :param page_identification: La page d'identification pour détruire la page et les informations essentiel à l'identification
    :param page_de_bord: La page de bord (pour la rendre visible)
    """
    page_presentation.destroy()
    page_identification.destroy()
    page_de_bord.deiconify()
    compte=recuperation_donnee(chemin_fichier,cle)[0][1]
    solde=afficher.solde_utilisateur(chemin_fichier,cle,compte)
    font=ctk.CTkFont(FONT,size=35)
    texte=ctk.CTkLabel(page_de_bord,text=f'Bonjour {nom}\n\n {solde}', font=font, text_color=WHITE)
    texte.place(x=10,y=50)
    logo_deconnexion= ctk.CTkImage(dark_image=Image.open('deconnexion.png'),size=(35,35))
    button_deconnexion=ctk.CTkButton(page_de_bord,fg_color=DARK_BLUE,hover_color=GREY, text='',image=logo_deconnexion,width=40,height=40,command=lambda: deconnexion(page_de_bord))
    button_deconnexion.place(x=800,y=50)
    button_acces_page_compte=ctk.CTkButton(page_de_bord,text='Accéder à vos comptes',fg_color=LIGHT_BLUE ,hover_color=LIGHT_BLUE2,width=300,height=35,command=lambda:gestion_compte_page(chemin_fichier,cle,compte,page_de_bord,button_acces_page_compte))
    button_acces_page_compte.place(x=300,y=260)
    button_acces_page_budget=ctk.CTkButton(page_de_bord,text='Accéder à vos budgets',fg_color=LIGHT_BLUE ,hover_color=LIGHT_BLUE2,width=300,height=35,command=lambda: gestion_budget_page(chemin_fichier,cle,page_de_bord,button_acces_page_budget))
    button_acces_page_budget.place(x=300,y=300)

def verif_data(num_identifiant: str,mdp: str,page_de_presentation: None,page_identification: None,page_de_bord: None) -> None:
    """
    Vérifie si les données entrer par l'utilisateur sont correcte
    :param num_identifiant: Le numéro identifiant de l'utilisateur
    :param mdp: Le mot de passe de l'utilisateur
    :param page_de_presentation: La page de présentation
    :param page_identification: La page d'identification
    :param page_de_bord: La page de bord
    """
    liste_user=recuperation_user('ident.txt',23)
    for indice in range(len(liste_user)):
        if num_identifiant == liste_user[indice]['identifiant'] and mdp == liste_user[indice]['motdepasse']:
            return fenetre_de_bord(liste_user[indice]['identifiant']+'.txt',int(liste_user[indice]['cle']),liste_user[indice]['nom'], page_de_presentation,page_identification,page_de_bord)
    else:
        messagebox.showerror(title='Error', message='Identifiant ou mot de passe incorrect.')
        page_identification.deiconify()

def identificatin_page(page_de_bord: None,page_de_presentation: None,button_se_connecter: None,progressbar: None):
    """
    Affiche la page d'identification (celle qui contient le clavier virtuel)
    :param page_de_bord: La page de bord (qui est caché)
    :param button_se_connecter: Le bouton se connecter de la page de présentation
    :param progressbar: Le bar de chargement annimé qui s'affiche sur la page de présentation
    """
    button_se_connecter.configure(state='disabled', fg_color=GREY)
    page_identification=ctk.CTkToplevel(page_de_bord,fg_color=DARK_BLUE)
    page_identification.title('Login Page')
    page_identification.geometry(NORMAL_SIZE_WINDOWS)
    page_identification.resizable(False,False)
    page_identification.protocol('WM_DELETE_WINDOW',lambda: on_close_page_identification(progressbar,button_se_connecter,page_identification))
    champ_id=ctk.CTkEntry(page_identification, width=220, height=35, placeholder_text="Numéro d'identifiant")
    champ_mdp=ctk.CTkEntry(page_identification,state='disabled', width=220, height=35 , show='*',placeholder_text='Mot de passe')
    champ_id.place(x=178,y=38)
    champ_mdp.place(x=178, y=93)
    buttons = [str(i) for i in range(10)]
    liste=[]
    ordonee = 150
    abscisse = 178
    for i in range(10): #placement des 10 boutons 0123456789
        a=random.choice(buttons)
        buttons.remove(a)
        liste.append(a)
        button_a=ctk.CTkButton(page_identification, text=a, width=60, height=30,fg_color=LIGHT_BLUE,hover_color=LIGHT_BLUE2, command=lambda b=a: on_clicl_vitrual_keyboard(b, champ_mdp))
        button_a.place(x=abscisse, y=ordonee)
        abscisse += 80
        if abscisse >= 400:
            ordonee += 50
            abscisse = 178
            if ordonee >= 300:
                abscisse=258
    abscisse=178
    annuler=ctk.CTkButton(page_identification, text='annuler', width=60, height=30,command=lambda: annuler_click(champ_mdp),fg_color=LIGHT_BLUE,hover_color=LIGHT_BLUE2)
    annuler.place(x=abscisse, y=ordonee) #placement du boutton annuler
    abscisse=338
    valider=ctk.CTkButton(page_identification, text='valider', width=60, height=30,fg_color=LIGHT_BLUE,hover_color=LIGHT_BLUE2,command=lambda: verif_data(champ_id.get(),champ_mdp.get(),page_de_presentation,page_identification,page_de_bord))
    valider.place(x=abscisse, y=ordonee)

def presentation_page(page_de_bord: None) -> None:
    """
    Affiche la page de présentation (celle qui contient le bouton se connecter)
    :param page_de_bord: La page de bord (qui est caché)
    """
    page_presentation=ctk.CTkToplevel(page_de_bord,fg_color=DARK_BLUE)
    page_presentation.title('BNP ParisCité')
    w1=385
    h1=570
    ws=page_presentation.winfo_screenwidth()
    hs=page_presentation.winfo_screenheight()#Pour l'afficher directement au centre de l'écran
    x= (ws/2)-(w1/2)
    y= (hs/2)-(h1/2)
    page_presentation.geometry('%dx%d+%d+%d' % (w1, h1, x, y))
    page_presentation.resizable(False,False)
    font=ctk.CTkFont(FONT,size=35)
    texte=ctk.CTkLabel(page_presentation,text='La première étape\n vers une gestion\n financière sans souci', font=font, text_color=WHITE)
    texte.place(x=25 ,y=250)
    img=ctk.CTkImage(dark_image=Image.open('LogoParisCité.png'), size=(75, 73))
    image_label=ctk.CTkLabel(page_presentation, image=img, text='')
    image_label.place(x=155, y=150)
    button_login=ctk.CTkButton(page_presentation,text='Se connecter',bg_color='#0d1b2a',fg_color=LIGHT_BLUE,hover_color=LIGHT_BLUE2,width=300,height=30,command=lambda: on_click_button_login(page_presentation,page_de_bord,button_login))
    button_login.place(x=42.5,y=400)
    page_presentation.protocol('WM_DELETE_WINDOW',lambda: on_closing_app(page_de_bord))

def main() -> None:
    """
    Fonction main qui va commencer par créer la page de bord "invisible" puis afficher la page de présentation
    et le reste en fonction des actions de l'utilisateur
    """
    page_de_bord=ctk.CTk(fg_color=DARK_BLUE)
    page_de_bord.geometry(BIG_SIZE_WINDOWS)
    page_de_bord.title('BNP Pariscité')
    page_de_bord.resizable(False,False)
    page_de_bord.withdraw()
    presentation_page(page_de_bord)
    page_de_bord.protocol('WM_DELETE_WINDOW', lambda: on_closing_app(page_de_bord))
    page_de_bord.mainloop()

if __name__=='__main__':
    main()