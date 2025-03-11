#!/bin/bash
# Génération du rapport
source /home/azureuser/Python-Git-Linux_Final-Project/mon_venv/bin/activate
python /home/azureuser/Python-Git-Linux_Final-Project/generate_report.py

#Envoie du rapport
# Variables
Date=$(date "+%Y-%m-%d")
subject="Rapport CAC40 $Date"
attachment="daily_report/report_$Date.html"
body="Bonjour, voici la pièce jointe du rapport CAC40 de ce jour."

# Envoi de l'email à chaque destinataire
while IFS= read -r email
do
    echo "Envoi du mail à $email"
    echo -e "$body" | mutt -a "$attachment" -s "$subject" -- "$email"
done < liste_mail.txt

