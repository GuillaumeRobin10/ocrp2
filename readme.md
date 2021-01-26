# Programme de scrapping

ce programme permet de récupérer les informations de tout les livres du site [booktoscrape.com](https://books.toscrape.com/index.html "booktoscrape.com").


## Fonctionnement

afin de lancer le programme vous devez suivre les étapes indiquées pour votre système d'exploitation



###installer python
telecharger [python](https://www.python.org/downloads/ "python") et installez-le en suivant les instructions.


#### Windows
1. rendez-vous dans le dossier ou ce situe le programme
2. Tout en maintenant la touche Maj ⇧ enfoncée, faites un clic droit et sélectionnez Ouvrir la fenêtre PowerShell ici.
3. entrez la commande : ``pip install virtualenv``
4. entrez la commande : ``virtualenv -p $env:python3 env``
5. entrez la commande : ``./env/scripts/activate.ps1``
6. entrez la commande : ``pip install -r requirements.txt``
7. entrez la commande : ``python main.py``
 
#### linux/mac

1. ouvrir le terminal (vous pouvez trouver l'outil directement en tapant “terminal” dans la barre de recherche des applications.(finder sous mac))
2. entrez la commande : ``pip install virtualenv``
2. entrez la commande : ``virtualenv -p python3 env``
3. entrez la commande :``source env/bin/activate``
4. entrez la commande : ``pip install -r requirements.txt``
5. entrez la commande : ``python3 main.py``


### exploitation des résultats
1. un dossier résultat vient d'être créé, ouvrez-le.
2. choisir la catégorie qui vous intéresse. 

	-le dossier images contient toutes les images des livres de la catégorie.
	-le fichier "catégorie.csv" contient les informations des livres
	
3. ouvir le fichier "catégorie.csv"
	1. sélectionner uniquement les cases suivantes:
		-Séparé par
		-Autre, puis remplir le champs par | (alt Gr + 6)
		-vérifier que tous les autres champs sous décocher
		-vérifier que le champs Séparateur de chaîne de caractère soit vide.
