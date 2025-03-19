#!/bin/bash

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Génération du rapport
/home/azureuser/Python-Git-Linux_Final-Project/mon_venv/bin/python /home/azureuser/Python-Git-Linux_Final-Project/generate_report.py

#Envoie du rapport
# Variables
Date=$(date "+%Y-%m-%d")
subject="Rapport CAC40 $Date"
attachment="/home/azureuser/Python-Git-Linux_Final-Project/daily_report/report_$Date.html"
body="Bonjour, voici la pièce jointe du rapport CAC40 de ce jour."
MAIL_CMD=$(which mutt)

# Envoi de l'email à chaque destinataire
while IFS= read -r email
do
    echo "Envoi du mail à $email"
    echo -e "$body" | $MAIL_CMD -a "$attachment" -s "$subject" -- "$email"
done < /home/azureuser/Python-Git-Linux_Final-Project/liste_mail.txt

