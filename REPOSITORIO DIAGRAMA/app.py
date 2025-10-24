import plotly.express as px
from dash import Dash, dcc, html

import plotly
print("Versión de Plotly:", plotly.__version__)

# Crear la app
app = Dash()

datos = px.data.tips()  # guardamos los datos

# Figura 1: Diagrama de pastel
fig_pie = px.pie(datos, names="sex", values="tip", title="Propinas por sexo (Diagrama de Pastel)")

# Figura 2: Diagrama de barras
fig_bar = px.bar(datos, x="sex", y="tip", color="sex", title="Propinas por sexo (Diagrama de Barras)")

# Layout de la aplicación (estructura simple)
app.layout = html.Div([
    html.H1("Dashboard de Propinas", style={'textAlign': 'center'}),
    
    html.Div([
        dcc.Graph(figure=fig_pie)
    ]),
    
    html.Div([
        dcc.Graph(figure=fig_bar)
    ])
])

# Ejecutar la app
app.run(debug=True, use_reloader=False)


