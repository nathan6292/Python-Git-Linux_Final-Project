import pandas as pd
import json
from datetime import datetime
import locale
import os
from jinja2 import Template

# Set locale to French
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

class CAC40Report:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.data = None
        
    def load_data(self):
        """Charge et prépare les données du CSV"""
        self.data = pd.read_csv(self.csv_path, parse_dates=['Date'])
        self.data.set_index('Date', inplace=True)
        self.data = self.data[self.data.index.date == datetime.now().date()]
        
    def prepare_stock_data(self):
        """Prépare les données des actions pour le rapport"""
        stocks_data = []
        
        # Calculer l'indice base 100 pour le CAC 40
        cac40_initial = float(self.data['CAC 40'].iloc[0])
        cac40_data = {
            "time_series": [],
            "opening": float(self.data['CAC 40'].iloc[0]),
            "closing": float(self.data['CAC 40'].iloc[-1]),
            "variation": ((float(self.data['CAC 40'].iloc[-1]) - cac40_initial) / cac40_initial) * 100
        }
        
        # Préparer les données du CAC 40 en base 100
        for timestamp, value in self.data['CAC 40'].items():
            cac40_data["time_series"].append({
                "time": timestamp.strftime("%H:%M"),
                "value": float(value),
                "index": (float(value) / cac40_initial) * 100
            })
        
        for column in self.data.columns:
            if column == 'CAC 40':
                continue
                
            series = self.data[column]
            initial_value = float(series.iloc[0])
            opening_price = initial_value
            closing_price = float(series.iloc[-1])
            high = series.max()
            low = series.min()
            variation = ((closing_price - opening_price) / opening_price) * 100
            
            time_series = []
            for timestamp, value in series.items():
                time_series.append({
                    "time": timestamp.strftime("%H:%M"),
                    "value": float(value),
                    "index": (float(value) / initial_value) * 100
                })
            
            stocks_data.append({
                "stock": column,
                "opening": opening_price,
                "closing": closing_price,
                "high": float(high),
                "low": float(low),
                "variation": float(variation),
                "data": time_series
            })
        
        return sorted(stocks_data, key=lambda x: x['variation'], reverse=True), cac40_data

    def generate_html_report(self):
        """Génère un rapport HTML complet"""
        stocks_data, cac40_data = self.prepare_stock_data()
        date = datetime.now()
        
        # Template HTML avec styles et scripts intégrés
        template = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport CAC40 - {{ date_str }}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary: #2563eb;
            --success: #34d399;
            --danger: #f87171;
        }
        
        body {
            font-family: system-ui, -apple-system, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f3f4f6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background-color: white;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }
        
        .header-title {
            flex-grow: 1;
        }
        
        .header h1 {
            margin: 0;
            color: #111827;
            font-size: 24px;
        }
        
        .header p {
            margin: 5px 0 0;
            color: #6b7280;
        }
        
        .cac40-status {
            text-align: right;
            padding-left: 20px;
        }
        
        .cac40-value {
            font-size: 24px;
            font-weight: bold;
            color: #111827;
        }
        
        .cac40-variation {
            font-size: 16px;
            margin-top: 5px;
        }
        
        .card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .card h2 {
            margin-top: 0;
            color: #111827;
            font-size: 18px;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        th, td {
            padding: 12px;
            text-align: right;
            border-bottom: 1px solid #e5e7eb;
        }
        
        th:first-child, td:first-child {
            text-align: left;
        }
        
        th {
            background-color: #f9fafb;
            font-weight: 600;
            color: #374151;
        }
        
        .positive {
            color: var(--success);
        }
        
        .negative {
            color: var(--danger);
        }
        
        .chart-container {
            position: relative;
            height: 300px;
            margin-bottom: 30px;
        }
        
        .main-chart {
            height: 400px;
        }

        .chart-subtitle {
            color: #6b7280;
            font-size: 14px;
            margin-top: 4px;
            margin-bottom: 16px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <div class="header-content">
                <div class="header-title">
                    <h1>Rapport CAC40</h1>
                    <p>{{ date_str }}</p>
                </div>
                <div class="cac40-status">
                    <div class="cac40-value">
                        {{ "%.2f"|format(cac40_data.closing) }}
                    </div>
                    <div class="cac40-variation {{ 'positive' if cac40_data.variation >= 0 else 'negative' }}">
                        {{ '%+.2f'|format(cac40_data.variation) }}%
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="card">
            <h2>Évolution comparative</h2>
            <p class="chart-subtitle">Base 100 à l'ouverture</p>
            <div class="chart-container main-chart">
                <canvas id="mainChart"></canvas>
            </div>
        </div>
        
        <div class="card">
            <h2>Performances du jour</h2>
            <div class="chart-container">
                <canvas id="performanceChart"></canvas>
            </div>
        </div>
        
        <div class="card">
            <h2>Valeurs les plus volatiles</h2>
            <div class="grid">
                {% for stock in volatile_stocks %}
                <div class="chart-container">
                    <canvas id="stockChart{{ loop.index }}"></canvas>
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="card">
            <h2>Détail des valeurs</h2>
            <table>
                <thead>
                    <tr>
                        <th>Valeur</th>
                        <th>Ouverture</th>
                        <th>Clôture</th>
                        <th>Plus Haut</th>
                        <th>Plus Bas</th>
                        <th>Variation</th>
                    </tr>
                </thead>
                <tbody>
                    {% for stock in stocks %}
                    <tr>
                        <td>{{ stock.stock }}</td>
                        <td>{{ "%.2f"|format(stock.opening) }} €</td>
                        <td>{{ "%.2f"|format(stock.closing) }} €</td>
                        <td>{{ "%.2f"|format(stock.high) }} €</td>
                        <td>{{ "%.2f"|format(stock.low) }} €</td>
                        <td class="{{ 'positive' if stock.variation >= 0 else 'negative' }}">
                            {{ '%+.2f'|format(stock.variation) }}%
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // Données des actions
        const stocksData = {{ stocks_json|safe }};
        const cac40Data = {{ cac40_json|safe }};
        
        // Graphique principal comparatif en base 100
        new Chart(document.getElementById('mainChart'), {
            type: 'line',
            data: {
                labels: cac40Data.time_series.map(d => d.time),
                datasets: [
                    {
                        label: 'CAC 40',
                        data: cac40Data.time_series.map(d => d.index),
                        borderColor: '#2563eb',
                        tension: 0.1
                    },
                    {
                        label: stocksData[0].stock + ' (Meilleure performance)',
                        data: stocksData[0].data.map(d => d.index),
                        borderColor: '#34d399',
                        tension: 0.1
                    },
                    {
                        label: stocksData[stocksData.length - 1].stock + ' (Pire performance)',
                        data: stocksData[stocksData.length - 1].data.map(d => d.index),
                        borderColor: '#f87171',
                        tension: 0.1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${context.parsed.y.toFixed(2)}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        ticks: {
                            callback: function(value) {
                                return value.toFixed(1);
                            }
                        }
                    }
                }
            }
        });
        
        // Graphique des performances
        new Chart(document.getElementById('performanceChart'), {
            type: 'bar',
            data: {
                labels: stocksData.slice(0, 10).map(s => s.stock),
                datasets: [{
                    label: 'Variation (%)',
                    data: stocksData.slice(0, 10).map(s => s.variation),
                    backgroundColor: stocksData.slice(0, 10).map(s => 
                        s.variation >= 0 ? '#34d399' : '#f87171'
                    )
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
        
        // Graphiques des valeurs volatiles
        stocksData.slice(0, 6).forEach((stock, index) => {
            new Chart(document.getElementById(`stockChart${index + 1}`), {
                type: 'line',
                data: {
                    labels: stock.data.map(d => d.time),
                    datasets: [{
                        label: stock.stock,
                        data: stock.data.map(d => d.value),
                        borderColor: '#2563eb',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top'
                        }
                    }
                }
            });
        });
    </script>
</body>
</html>
        """
        
        # Préparer les données pour le template
        template_data = {
            'date_str': date.strftime("%A %d %B %Y").capitalize(),
            'stocks': stocks_data,
            'cac40_data': cac40_data,
            'volatile_stocks': sorted(stocks_data, key=lambda x: abs(x['variation']), reverse=True)[:6],
            'stocks_json': json.dumps(stocks_data, ensure_ascii=False),
            'cac40_json': json.dumps(cac40_data, ensure_ascii=False)
        }
        
        # Générer le HTML
        html = Template(template).render(**template_data)
        
        # Sauvegarder le rapport
        output_path = f"/home/azureuser/Python-Git-Linux_Final-Project/daily_report/report_{date.strftime('%Y-%m-%d')}.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
            
        return output_path

def generate_daily_report(csv_path):
    """Génère le rapport quotidien"""
    try:
        report = CAC40Report(csv_path)
        report.load_data()
        html_path = report.generate_html_report()
        print(f"Rapport HTML généré avec succès: {html_path}")
        return html_path
    except Exception as e:
        print(f"Erreur lors de la génération du rapport: {e}")
        return None

if __name__ == "__main__":
    csv_path = "/home/azureuser/Python-Git-Linux_Final-Project/prices.csv"
    generate_daily_report(csv_path)
