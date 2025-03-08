import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Initialiser l'application Dash avec Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

# Taux sans risque (exemple : 2% annuel, ajusté pour un jour de trading)
TAUX_SANS_RISQUE = 0.02 / 252

# Fonction pour lire le fichier CSV
def lire_csv(fichier):
    return pd.read_csv(fichier)

# Mise en page de l'application
app.layout = dbc.Container([
    html.H1("Prix des Actions en Temps Réel", className="text-center mt-4 mb-4"),
    
    # Interval pour la mise à jour automatique (toutes les 5 minutes)
    dcc.Interval(id='interval-component', interval=300000, n_intervals=0),
    
    # Affichage des derniers prix et statistiques sous forme de cartes
    dbc.Row([html.Div(id='prix-actions', className="d-flex flex-wrap justify-content-center")]),
    
    # Graphique de l'évolution des prix
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-evolution'), width=12)
    ])
], fluid=True)

# Callback pour mettre à jour les prix et statistiques des actions
@app.callback(
    Output('prix-actions', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def mettre_a_jour_prix(n):
    try:
        df = lire_csv('prices.csv')  # Charger le CSV
        df['Date'] = pd.to_datetime(df['Date'])  # Convertir en format datetime

        derniere_ligne = df.iloc[-1]  # Derniers prix disponibles
        date = derniere_ligne['Date']
        prix_actuels = derniere_ligne[1:].to_dict()  # Prix des actions

        cartes = [html.H5(f"Dernière mise à jour : {date}", className="w-100 text-center my-3")]  
        
        for action, prix in prix_actuels.items():
            historique = df[['Date', action]].dropna()
            rendement = ((historique[action].iloc[-1] - historique[action].iloc[0]) / historique[action].iloc[0]) * 100
            historique['retours'] = historique[action].pct_change()
            volatilite = historique['retours'].std() * 100
            rendement_moyen = historique['retours'].mean()
            sharpe_ratio = (rendement_moyen - TAUX_SANS_RISQUE) / historique['retours'].std() if historique['retours'].std() != 0 else 0

            cartes.append(
                dbc.Card([
                    dbc.CardBody([
                        html.H4(action, className="card-title text-primary"),
                        html.P(f"Prix : {prix:.2f} €", className="card-text"),
                        html.P(f"Rendement : {rendement:.2f} %", className="card-text"),
                        html.P(f"Volatilité : {volatilite:.2f} %", className="card-text"),
                        html.P(f"Sharpe Ratio : {sharpe_ratio:.2f}", className="card-text")
                    ])
                ], className="m-2 shadow", style={"width": "250px", "border-radius": "10px"})
            )

        return cartes
    except Exception as e:
        return html.P(f"Erreur lors de la mise à jour : {e}", className="text-danger")

# Callback pour mettre à jour le graphique
@app.callback(
    Output('graph-evolution', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def mettre_a_jour_graphique(n):
    try:
        df = lire_csv('prices.csv')
        df['Date'] = pd.to_datetime(df['Date'])

        df_melted = df.melt(id_vars=['Date'], var_name='Entreprise', value_name='Prix')

        fig = px.line(df_melted, x='Date', y='Prix', color='Entreprise',
                      title="Évolution des prix des actions des 40 entreprises",
                      template="plotly_dark")

        fig.update_layout(
            paper_bgcolor='#1e1e1e',
            plot_bgcolor='#1e1e1e',
            font=dict(color='white')
        )
        return fig
    except Exception as e:
        return px.line(title=f"Erreur lors du chargement des données : {e}")

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
