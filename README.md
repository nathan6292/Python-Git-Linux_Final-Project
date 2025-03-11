# 📊 Advanced Python, Git Linux Projet : CAC 40 Dashboard & Rapport Automatisé

Ce projet utilise une **machine virtuelle Ubuntu sur Azure** pour :
- **Scraper** les cours des **40 actions du CAC 40** toutes les 5 minutes.
- Générer un **rapport quotidien** à **20h**.
- Envoyer automatiquement ce rapport à une liste d'emails.
- Fournir une **application Dash** en ligne accessible 24h/24 pour visualiser les données.

L'application web est disponible via le lien suivant : http://20.199.89.214:80

## 📂 Structure du projet
```plaintext
cac40-dashboard/
├── daily_report/                # Dossier contenant les rapports générés chaque jour
│   └── report_YYYY-MM-DD.html   # Exemple : report_2024-10-08.html
│
├── generate_report.py           # Script Python pour générer le rapport quotidien (le fichier html)
│
├── liste-mail.txt              # Liste des adresses email recevant le rapport quotidien
│
├── log.txt                     # Fichier de logs pour suivre l'exécution du crontab
│
├── prices.csv                  # Fichier des cours des actions du CAC 40 (actualisé toutes les 5 minutes via program.sh)
│
├── program.sh                # Script Bash pour scraper les données et les enregistrer dans prices.csv
│
├── python_code.py              # Script Python pour :
│                               # - Lancer l'application Dash
│                               # - Mettre en ligne l'application
│
├── report.sh                   # Script Bash pour générer et envoyer le rapport quotidien
│
└── schedule-crontab.txt        # Fichier listant les commandes crontab utilisées
```
## 📋 Description des fichiers

### 1. **daily_report/**
Contient les rapports quotidiens générés sous le format : report_YYYY-MM-DD.html
Ces rapports incluent les principales informations sur les performances du **CAC 40**.

---

### 2. **generate_report.py**
Script Python pour :
- **Générer** un rapport détaillé à partir des données du **prices.csv**.
- Stocker ce rapport dans le dossier **DailyReport/**.

---

### 3. **liste_mail.txt**
Un simple fichier texte contenant la **liste des adresses email** auxquelles le rapport quotidien est envoyé.  
Chaque adresse est inscrite sur une **ligne distincte**.

Exemple : email@exemple.com

---

### 4. **log.txt**
Fichier de **log** permettant de suivre l'exécution des différentes tâches automatisées via **crontab**.  
Il consigne les événements, erreurs et statuts d'exécution.

---

### 5. **prices.csv**
Ce fichier est mis à jour **toutes les 5 minutes** et stocke les **cours des 40 actions du CAC 40**.

---

### 6. **program.sh**
Script Bash exécuté par le **cron** pour :
- **Scraper** les données des **40 actions du CAC 40**.
- Mettre à jour le fichier **prices.csv**.

---

### 7. **python_code.py**
Script Python central qui :
- Lance l'**application Dash** pour visualiser les **données en temps réel**.
- Met en ligne l'application sur la **machine virtuelle**, accessible 24h/24.

---

### 8. **report.sh**
Script Bash exécuté quotidiennement pour :
- **Générer le rapport** via **GenerateReport.py**.
- Envoyer le rapport aux emails listés dans **liste-mail.txt**.

---

### 9. **schedule_crontab.txt**
Fichier de référence contenant les **commandes crontab** utilisées pour automatiser :
- Le **scraping** toutes les 5 minutes.
- La **génération et l'envoi** du rapport quotidien.

---

🎯 *Projet développé dans le cadre du module Advanced Python, Git & Linux.*



