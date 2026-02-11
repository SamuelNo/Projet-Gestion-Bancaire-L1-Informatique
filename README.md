# BNP Cité - Application de Gestion Bancaire

Ce projet a été réalisé dans le cadre de l'unité d'enseignement Informatique en Licence 1 à l'Université Paris Cité pour l'année universitaire 2023-2024. Il s'agit d'un logiciel de simulation bancaire permettant la gestion de comptes, de budgets et le suivi d'opérations financières.

## Équipe de développement 
* Samuel NOEL : Développement du backend (gestion des données) et de l'interface de gestion de compte.
* Valentin PONNOUSSAMY : Développement du backend et de l'interface de gestion de budget.
* Timahi LESAGE CAFFA : Implémentation des systèmes de chiffrement et génération des composants visuels (graphiques et tableaux).
* Marwan DENAGNON : Implémentation des systèmes de chiffrement et interface d'authentification.

Encadrant : Jérôme DELOBELLE

## Fonctionnalités principales
L'application repose sur une architecture combinant un traitement de données logique et une interface utilisateur graphique.

* Sécurité : Chiffrement des données utilisateurs basé sur un algorithme de décalage. La clé de décryptage utilisée pour le fichier d'indexation (ident.txt) est fixée à 23.
* Gestion de comptes : Consultation du solde, création de comptes et réalisation de virements internes ou externes.
* Suivi budgétaire : Définition de plafonds par catégorie de dépense et visualisation des indicateurs de suivi.
* Historique : Consultation et tri des transactions bancaires selon différents critères (date, type de compte, budget).
* Interface graphique : Environnement utilisateur développé avec les bibliothèques Tkinter et CustomTkinter pour une navigation fluide.

## Spécifications techniques
* Langage : Python 3
* Bibliothèques graphiques : CustomTkinter, Tkinter, PIL (Pillow)
* Gestion temporelle : Tkcalendar
* Persistance des données : Fichiers textes structurés et chiffrés

## Installation et Lancement

### Dépendances
Il est nécessaire d'installer les bibliothèques suivantes via le gestionnaire de paquets pip :
```bash
pip install customtkinter tkcalendar pillow

Lancement avec la commande:

pyhton3 main.py