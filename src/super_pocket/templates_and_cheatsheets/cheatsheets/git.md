# Feuille de triche Git

## Installer Git

### GitHub pour Windows
[https://windows.github.com](https://windows.github.com)

### GitHub pour Mac
[https://mac.github.com](https://mac.github.com)

### Git pour toutes les plateformes
Le programme d'installation le plus récent se trouve sur le site Git officiel. [https://git-scm.com](https://git-scm.com)

## Configurer l'outillage

Configure le nom que vous voulez associer à toutes vos transactions de validation 
```
git config --global user.name "[nom]"
```

Configure l'e-mail que vous voulez associer à toutes vos transactions de validation 
```
git config --global user.email "[adresse e-mail]"
```

Configure la coloration automatique de la ligne de commande pour Git pour une revue facile 
```
git config --global color.ui auto
```

## Créer des référentiels

Crée un nouveau référentiel local avec le nom spécifié 
```
git init [nom-du-projet]
```

Clone (télécharge) un référentiel qui existe déjà sur GitHub, y compris tous les fichiers, les branches et les validations 
```
git clone [url]
```

## Apporter des modifications

Affiche tous les nouveaux fichiers ou les fichiers modifiés à valider 
```
git status
```

Répertorie l'historique de version pour la branche actuelle 
```
git log
```

Répertorie l'historique de version pour un fichier, y compris les renommages 
```
git log --follow [fichier]
```

Montre les différences de contenu entre deux branches 
```
git diff [première-branche]...[deuxième-branche]
```

Affiche les différences de métadonnées et de contenu d'une validation 
```
git show [validation]
```

Valide un instantané du répertoire de travail dans l'historique de version de la branche 
```
git add [fichier]
```

Valide tous les fichiers du répertoire de travail dans l'historique de version de la branche 
```
git add .
```

Valide un instantané de tous les changements suivis dans l'historique de version 
```
git commit -m "[message de validation]"
```

## Changements de groupe

Répertorie toutes les branches locales dans le référentiel actuel 
```
git branch
```

Crée une nouvelle branche 
```
git branch [nom-de-branche]
```

Bascule vers la branche spécifiée et met à jour le répertoire de travail 
```
git checkout [nom-de-branche]
```

Combine l'historique de la branche spécifiée dans la branche actuelle 
```
git merge [branche]
```

Supprime la branche spécifiée 
```
git branch -d [nom-de-branche]
```

## Déplacer et supprimer des fichiers

Supprime le fichier du répertoire de travail et indexe la suppression 
```
git rm [fichier]
```

Supprime le fichier de la gestion de version, mais préserve le fichier localement 
```
git rm --cached [fichier]
```

Renomme le fichier et le prépare pour la validation 
```
git mv [fichier-original] [fichier-renommé]
```

## Annuler des validations

Efface la zone d'index, mais garde votre répertoire de travail intact 
```
git reset --hard HEAD
```

Crée une nouvelle validation qui annule tous les changements faits dans 
```
[validation]
``` 
```
git revert [validation]
```

## Branches et fusion

Répertorie toutes les branches locales dans le référentiel actuel 
```
git branch
```

Crée une nouvelle branche 
```
git branch [nom-de-branche]
```

Bascule vers la branche spécifiée et met à jour le répertoire de travail 
```
git checkout [nom-de-branche]
```

Crée une nouvelle branche et y bascule 
```
git checkout -b [nouvelle-branche]
```

Combine l'historique de la branche spécifiée dans la branche actuelle 
```
git merge [branche]
```

Supprime la branche spécifiée 
```
git branch -d [nom-de-branche]
```

## Référentiels distants

Ajoute un référentiel distant nommé 
```
git remote add [nom-distant] [url-distante]
```

Télécharge tous les changements de `[nom-distant]`, mais ne les intègre pas dans `HEAD` 
```
git fetch [nom-distant]
```

Télécharge tous les changements du `HEAD` distant et les fusionne dans le `HEAD` local 
```
git pull [nom-distant] [branche]
```

Pousse tous les commits de la branche locale vers GitHub 
```
git push [nom-distant] [branche]
```

## Annuler des modifications (distantes)

Récupère et fusionne les changements sur le serveur distant avec votre version locale 
```
git pull
```

Remplace vos changements locaux par le dernier contenu de GitHub. Les changements faits sur votre machine locale seront **perdus** 
```
git reset --hard origin/master
```