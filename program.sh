#!/bin/bash
echo "Lancement du program"

# Chemin du fichier CSV de sortie
output_file="/home/azureuser/Python-Git-Linux_Final-Project/prices.csv"

# Récupérer le contenu du fichier HTML à partir de l'URL
file=$(curl -s "https://www.comdirect.de/inf/indizes/werte/FR0003500008")

# Liste des 40 sociétés du CAC40 (selon la structure observée dans le fichier)
companies=(
  "Accor S.A." "Airbus" "ArcelorMittal" "Air Liquide" "AXA S.A." "BNP Paribas" "Bouygues" "Bureau Veritas" "Capgemini"
  "Carrefour" "Compagnie de Saint-Gobain" "Compagnie Generale des Etablissements Michelin" "Crédit Agricole" "Danone"
  "Dassault Systèmes" "Edenred" "Engie S.A." "EssilorLuxottica" "Eurofins Scientific" "HERMES INTL"
  "KERING" "Legrand" "L'Oreal" "LVMH Moët Henn. L. Vuitton" "Orange" "Pernod Ricard" "Publicis Groupe" "Renault"
  "Safran" "Sanofi" "Schneider Electric" "Société Générale" "Stellantis" "STMicroelectronics"
  "Téléperformance" "Thales" "TotalEnergies" "WFD Unibail Rodamco" "Veolia Environnement"
  "Vinci"
)

if [ ! -s "$output_file" ]; then
	echo "" > "$output_file"
	echo -n "Date," >> "$output_file"

	# Ajouter le titres des colonnes du csv
	for ((i=0; i<${#companies[@]}; i++)); do
    		company="${companies[$i]}"
    	     	echo -n "$company," >> "$output_file"
	done

echo "CAC 40" >> "$output_file"
fi

echo -n $(date +"%Y-%m-%d %H:%M:%S,") >> "$output_file" 

# Parcours de la liste et extraction du prix pour chaque société
for ((i=0; i<${#companies[@]}; i++)); do

    company="${companies[$i]}"

    # Recherche dans le contenu du fichier : la balise qui contient le prix est précédée par data-label="Aktuell"
    price=$(echo "$file" | grep -A 2 "$company" | grep -oP '(?<=data-label="Aktuell">)[0-9.]+,[0-9]+')

    # Nettoyage du prix : supprimer les points pour les milliers et remplacer la virgule par un point
    clean_price=$(echo "$price" | tr -d '.' | tr ',' '.')

    # Ajouter les résultats au fichier CSV
    echo -n "$clean_price," >> "$output_file"


done

price_cac40=$(echo "$file" | grep -oP '(?<=itemprop="price" content=")[0-9]+(\.[0-9]+)?')

echo "$price_cac40" >> "$output_file"

# Lancement du dash

source /home/azureuser/Python-Git-Linux_Final-Project/mon_venv/bin/activate
sudo /home/azureuser/Python-Git-Linux_Final-Project/mon_venv/bin/python /home/azureuser/Python-Git-Linux_Final-Project/python_code.py
