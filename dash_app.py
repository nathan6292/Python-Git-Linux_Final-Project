import dash
from dash import dcc, html
from dash.dependencies import Input, Output, ALL, State
import pandas as pd
import plotly.express as px
from dash import dash_table
import base64
from datetime import timedelta

# Initialiser l'application Dash avec suppression des exceptions de callback
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Taux sans risque (2% annuel par exemple)
TAUX_SANS_RISQUE = 0.02 / 252

# Fonction pour lire le fichier CSV
def lire_csv(fichier):
    return pd.read_csv(fichier)

# Encoder l'image en base64
with open('/home/azureuser/Python-Git-Linux_Final-Project/logo.jpg', 'rb') as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

# Mise en page de l'application
app.layout = html.Div([
    html.H1(
        "Cours actions CAC 40",
        style={
            'textAlign': 'center',
            'fontFamily': 'Arial',
            'color': 'white',
            'fontSize': '32px',
            'fontWeight': 'bold',
            'marginBottom': '40px'
        }
    ),

    html.Img(
        src=f'data:image/webp;base64,{encoded_image}',
        style={
            'position': 'absolute',
            'top': '10px',
            'right': '10px',
            'width': '80px',
            'height': '80px'
        }
    ),

    dcc.Interval(id='interval-component', interval=300000, n_intervals=0),

    #Ajouter la date de la dernière mise à jour
    html.P(id='date-maj', style={'color': 'white', 'textAlign': 'center'}),

    html.Div(style={'height': '20px'}),

    # Tableau des actions
    dash_table.DataTable(
        id='table-actions',
        columns=[
            {"name": "Action", "id": "Action"},
            {"name": "Prix (€)", "id": "Prix", "type": "numeric", "format": {"specifier": ".2f"}},
            {"name": "Rendement (%)", "id": "Rendement", "type": "numeric", "format": {"specifier": ".2f"}},
            {"name": "Volatilité (%)", "id": "Volatilité", "type": "numeric", "format": {"specifier": ".2f"}},
            {"name": "Sharpe Ratio", "id": "Sharpe Ratio", "type": "numeric", "format": {"specifier": ".2f"}}
        ],
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'center',
            'color': 'white',
            'fontFamily': 'Arial'
        },
        style_header={
            'backgroundColor': '#003366',
            'color': 'white',
            'fontFamily': 'Arial'
        },
        style_data={
            'backgroundColor': '#001F3F',
            'fontFamily': 'Arial'
        }
    ),

    html.Div(style={'height': '20px'}),

    # Légende pour le graphique
    html.P(
        "Vous trouverez ci-dessous l'évolution graphique des prix normalisés des actions du CAC 40. "
        "Nous avons fait le choix de normaliser les prix afin de vous offrir une meilleure visibilité sur les variations de ces prix "
        "en palliant au problème de la différence conséquente d'échelle entre certains cours d'action. "
        "Afin d'afficher ou de masquer certains cours, n'hésitez pas à utiliser les légendes interactives (à droite du graphique) "
        "qui permettent, en cliquant dessus, de masquer ou de rendre visible le cours choisi.",
        style={'color': 'white', 'textAlign': 'center', 'marginBottom': '20px'}
    ),

    html.Div(style={'height': '20px'}),

    # Graphique évolution prix normalisés
    dcc.Graph(id='graph-evolution'),

    html.Div(style={'height': '40px'}),


    # Ajouter un champ pour l'email avant le simulateur
    html.H3("Recevez ou retirez votre email du rapport quotidien", style={'color': 'white', 'textAlign': 'center'}),
    
    # Zone pour entrer l'email
    html.Label("Entrez votre adresse e-mail :", style={'color': 'white'}),
    dcc.Input(
        id='email-input',
        type='email',
        placeholder='Votre adresse e-mail',
        style={'width': '300px', 'padding': '10px', 'borderRadius': '5px'}
    ),
    html.Button('S\'inscrire', id='submit-email', n_clicks=0, style={
        'marginLeft': '10px',
        'padding': '10px',
        'borderRadius': '5px'
    }),

    html.Button('Se désinscrire', id='remove-email', n_clicks=0, style={
        'marginLeft': '10px',
        'padding': '10px',
        'borderRadius': '5px'
    }),
    
    html.Div(id='email-response', style={'color': 'white'}),

    # Titre du simulateur
    html.H2("Simulateur de stratégie d'investissement", style={'color': 'white', 'textAlign': 'center'}),

    html.P(
        "Ce simulateur de stratégie propose de tester le rendement d'un investissement réalisé à 100% sur des actions du CAC 40. "
        "A l'aide des curseurs, vous pouvez sélectionner le poids à allouer à chaque action dans votre portefeuille total. "
        "Par la suite, vous pourrez indiquer l'horizon temporel à considérer pour obtenir les métriques clés sur vos investissements. "
        "ATTENTION : il est nécessaire que la somme des poids alloués fasse exactement 100%.",
        style={'color': 'white', 'textAlign': 'center', 'marginBottom': '20px'}
    ),

    html.Div(style={'height': '20px'}),

    # Curseurs pour décider du poids sur chaque action
    html.Div([
        html.H4("Allouer des poids à chaque action du CAC 40", style={'color': 'white'}),
        html.Div(id='poids-actions', children=[]),
    ], style={'padding': '20px', 'backgroundColor': '#003366', 'borderRadius': '8px'}),

    html.Div(style={'height': '40px'}),

    # Choix de la durée pour calcul du rendement
    html.Div([
        html.Label("Période de calcul des métriques :", style={'color': 'white'}),
        dcc.Dropdown(
            id='periode-dropdown',
            options=[
                {'label': '1 jour', 'value': '1d'},
                {'label': '5 jours', 'value': '5d'},
                {'label': '1 mois', 'value': '1m'}
            ],
            value='1m',  # Valeur par défaut
            clearable=False,
            style={'color': 'black'}
        )
    ], style={'padding': '20px', 'backgroundColor': '#003366', 'borderRadius': '8px'}),

    html.Div(style={'height': '40px'}),

    # Encadrés pour les métriques
    html.Div([
        html.Div(id='rendement-strategie', style={'color': 'white', 'fontSize': '18px', 'padding': '20px', 'backgroundColor': '#003366', 'borderRadius': '8px'}),
        html.Div(id='volatilite-strategie', style={'color': 'white', 'fontSize': '18px', 'padding': '20px', 'backgroundColor': '#003366', 'borderRadius': '8px', 'marginTop': '20px'}),
        html.Div(id='sharpe-ratio-strategie', style={'color': 'white', 'fontSize': '18px', 'padding': '20px', 'backgroundColor': '#003366', 'borderRadius': '8px', 'marginTop': '20px'})
    ], style={'marginBottom': '40px'}),

], style={
    'backgroundColor': '#001F3F',
    'padding': '20px',
    'min-height': '100vh',
    'fontFamily': 'Arial'
})

# Callback pour afficher la date de la dernière mise à jour
@app.callback(
    Output('date-maj', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def afficher_date_maj(n):
    df = lire_csv('/home/azureuser/Python-Git-Linux_Final-Project/prices.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return f"Dernière mise à jour : {df['Date'].max()}"

@app.callback(
    Output('email-response', 'children'),
    Input('submit-email', 'n_clicks'),
    Input('remove-email', 'n_clicks'),
    State('email-input', 'value')
)
def manage_email_subscription(subscribe_clicks, unsubscribe_clicks, email):
    ctx = dash.callback_context  # Context pour savoir quel bouton a été cliqué
    
    if not ctx.triggered:
        return ""
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if email and '@' in email:
        if button_id == 'submit-email' and subscribe_clicks > 0:
            # Vérifier que l'email n'est pas déjà inscrit
            with open('/home/azureuser/Python-Git-Linux_Final-Project/liste_mail.txt', 'r') as f:
                liste_mail = f.readlines()
            liste_mail = [line.strip() for line in liste_mail]

            if email in liste_mail:
                return f"L'email {email} est déjà inscrit."
            else:
                # Inscription de l'email
                with open('/home/azureuser/Python-Git-Linux_Final-Project/liste_mail.txt', 'a') as f:
                    f.write(email + '\n')
                return f"Merci ! Vous recevrez  le rapport quotidien tous les jours du lundi au vendredi à 20h à : {email}"
        
        elif button_id == 'remove-email' and unsubscribe_clicks > 0:
            # Retirer l'email de la liste
            result = retirer_email(email)
            return result
    return "Adresse e-mail invalide. Veuillez réessayer."

def retirer_email(email):
    # Lire le fichier des emails
    with open('/home/azureuser/Python-Git-Linux_Final-Project/liste_mail.txt', 'r') as f:
        liste_mail = f.readlines()
    liste_mail = [line.strip() for line in liste_mail]
    
    # Vérifier si l'email est dans la liste
    if email in liste_mail:
        # Si l'email est trouvé, le retirer
        liste_mail.remove(email)
        
        # Réécrire la liste mise à jour dans le fichier
        with open('/home/azureuser/Python-Git-Linux_Final-Project/liste_mail.txt', 'w') as f:
            for line in liste_mail:
                f.write(line + '\n')
        return f"L'email {email} a été retiré de la liste."
    else:
        return f"L'email {email} n'est pas inscrit."

@app.callback(
    Output('table-actions', 'data'),
    [Input('interval-component', 'n_intervals')]
)
def mettre_a_jour_prix(n):
    try:
        df = lire_csv('/home/azureuser/Python-Git-Linux_Final-Project/prices.csv')
        df['Date'] = pd.to_datetime(df['Date'])

        derniere_ligne = df.iloc[-1]
        prix_actuels = derniere_ligne[1:].to_dict()

        data = []

        for action in prix_actuels.keys():
            historique = df[['Date', action]].dropna()
            historique = historique[historique['Date'].dt.day >= historique['Date'].max().day]
            rendement = ((historique[action].iloc[-1] - historique[action].iloc[0]) / historique[action].iloc[0]) * 100
            historique['retours'] = historique[action].pct_change()
            volatilite = historique['retours'].std() * 100
            rendement_moyen = historique['retours'].mean()

            sharpe_ratio = (rendement_moyen - TAUX_SANS_RISQUE) / historique['retours'].std() if historique['retours'].std() != 0 else 0

            data.append({
                "Action": action,
                "Prix": prix_actuels[action],
                "Rendement": rendement,
                "Volatilité": volatilite,
                "Sharpe Ratio": sharpe_ratio
            })

        return data
    except Exception as e:
        return [{"Action": "Erreur", "Prix": 0, "Rendement": 0, "Volatilité": 0, "Sharpe Ratio": 0}]

@app.callback(
    Output('graph-evolution', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def mettre_a_jour_graphique(n):
    try:
        df = lire_csv('/home/azureuser/Python-Git-Linux_Final-Project/prices.csv')
        df['Date'] = pd.to_datetime(df['Date'])

        # Filtrer uniquement les jours ouvrés et horaires de marché (9h-18h)
        df = df[(df['Date'].dt.weekday < 5) & (df['Date'].dt.hour >= 9) & (df['Date'].dt.hour < 18)]

        df_melted = df.melt(id_vars=['Date'], var_name='Entreprise', value_name='Prix')

        # Normalisation des prix en base 100
        df_melted['Prix Normalisé'] = df_melted.groupby("Entreprise")['Prix'].transform(lambda x: (x / x.iloc[0]) * 100)

        df_melted['Date'] = df_melted['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')


        fig = px.line(df_melted, x='Date', y='Prix Normalisé', color='Entreprise', title="Évolution des prix normalisés")

        # Ajuster l'axe X pour ne pas afficher les heures de fermeture
        fig.update_xaxes(type='category')  

        fig.update_layout(
            plot_bgcolor='#001F3F',
            paper_bgcolor='#001F3F',
            font_color='white'
        )

        fig.update_xaxes(
            tickformat="%d %b\n%Hh",  # Ex: "12 Mar\n15h"
            tickmode='linear',
            dtick=6 * 6,  # Affiche une date toutes les 6 heures
            tickangle=45,  # Rotation des labels pour éviter le chevauchement
            showgrid=True
        )


        return fig
    except Exception as e:
        return px.line(title="Erreur lors du chargement des données")

@app.callback(
    Output('poids-actions', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def generate_sliders(n):
    try:
        df = lire_csv('/home/azureuser/Python-Git-Linux_Final-Project/prices.csv')
        actions = df.columns[1:]  # Assurez-vous de ne pas inclure la colonne 'Date'

        sliders = []
        for action in actions:
            sliders.append(html.Div([
                html.Label(f"Poids pour {action} (%)", style={'color': 'white'}),
                dcc.Slider(
                    id={'type': 'poids-slider', 'index': action},
                    min=0,
                    max=100,
                    step=1,
                    value=0,  # Valeur par défaut, ici 0%
                    marks={i: str(i) for i in range(0, 101, 10)}
                ),
                html.Br()
            ], style={'color': 'white', 'marginBottom': '20px'}))  # Ajout d'un espace entre les curseurs
        return sliders
    except Exception as e:
        return [html.Div(f"Erreur : {str(e)}")]

@app.callback(
    [Output('rendement-strategie', 'children'),
     Output('volatilite-strategie', 'children'),
     Output('sharpe-ratio-strategie', 'children')],
    [Input({'type': 'poids-slider', 'index': ALL}, 'value'),
     Input('periode-dropdown', 'value')]
)
def calculer_rendement(poids, periode):
    try:
        # Vérifier que la somme des poids est égale à 100%
        total_poids = sum(poids)
        if total_poids != 100:
            return (
                f"Erreur : la somme des poids doit être égale à 100%. Total actuel : {total_poids:.2f}%",
                "",
                ""
            )

        df = lire_csv('/home/azureuser/Python-Git-Linux_Final-Project/prices.csv')
        df['Date'] = pd.to_datetime(df['Date'])

        # Déterminer la date de début en fonction de la période sélectionnée
        derniere_date = df['Date'].max()
        if periode == '1d':
            date_debut = derniere_date - timedelta(days=1)
        elif periode == '5d':
            date_debut = derniere_date - timedelta(days=5)
        elif periode == '1m':
            date_debut = derniere_date - timedelta(days=30)

        df_filtre = df[df['Date'] >= date_debut]

        actions = df.columns[1:]  # Assurez-vous de ne pas inclure la colonne 'Date'
        rendement_portefeuille = 0
        volatilite_portefeuille = 0
        rendement_moyen_portefeuille = 0

        # Calcul du rendement global basé sur les poids
        for i, action in enumerate(actions):
            poids_action = poids[i] / 100  # Convertir en fraction
            historique = df_filtre[['Date', action]].dropna()
            if not historique.empty:
                rendement = ((historique[action].iloc[-1] - historique[action].iloc[0]) / historique[action].iloc[0]) * 100
                rendement_portefeuille += poids_action * rendement

                # Calcul des rendements quotidiens
                historique['retours'] = historique[action].pct_change()
                volatilite_portefeuille += poids_action * (historique['retours'].std() * 100)
                rendement_moyen_portefeuille += poids_action * historique['retours'].mean()

        # Calcul du Sharpe Ratio du portefeuille
        sharpe_ratio_portefeuille = (rendement_moyen_portefeuille - TAUX_SANS_RISQUE) / (volatilite_portefeuille / 100) if volatilite_portefeuille != 0 else 0

        return (
            f"Rendement total de la stratégie : {rendement_portefeuille:.2f}%",
            f"Volatilité du portefeuille : {volatilite_portefeuille:.2f}%",
            f"Sharpe Ratio du portefeuille : {sharpe_ratio_portefeuille:.2f}"
        )
    except Exception as e:
        return f"Erreur lors du calcul : {e}", "", ""

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True, port=80, host='0.0.0.0')
