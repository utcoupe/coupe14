Code source de notre robot pour la coupe de France de robotique 2014
=========

Commandes de base pour se lancer dans le projet
-------------------

Pour clonner le depot:
* git clone git@github.com:utcoupe/coupe14.git



Commandes à utiliser au quotidien pour developper:
-------------------

Une fois ces installations effectuées, il faudrat systèmatiquement activer l'environement avant de developper pour le projet:
* source coupe2014/virt_env/bin/activate

Pour le deactiver:
* deactivate




Commandes avancées
-------------------

Pour ajouter un submodule :
* git submodule add sshdurepo
Puis commit & push

Pour installer une nouvelle lib, activer l'environement virtuel puis utilisez:
* sudo pip install MaNouvelleLib
Une fois l'env activé, il faudrat mettre à jour le fichier requirements.txt:
* pip freeze > requirements.txt
