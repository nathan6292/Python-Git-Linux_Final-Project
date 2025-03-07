#!/bin/bash

# Chemin du fichier CSV de sortie
output_file="prices.csv"

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

# Parcours de la liste et extraction du prix pour chaque société
for company in "${companies[@]}"; do
    # Recherche dans le contenu du fichier (la variable $file) : on suppose que la balise contenant le prix est précédée par data-label="Aktuell"
    price=$(echo "$file" | grep -A 2 "$company" | grep -oP '(?<=data-label="Aktuell">)[0-9.]+,[0-9]+')

    # Nettoyage du prix : supprimer les points pour les milliers et remplacer la virgule par un point
    clean_price=$(echo "$price" | tr -d '.' | tr ',' '.')

    # Ajouter les résultats au fichier CSV
    echo "$company,$clean_price" >> "$output_file"
done
