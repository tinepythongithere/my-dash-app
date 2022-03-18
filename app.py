from dash import dash, html, dcc
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import dash_daq as daq
import dash_extensions as de

df = pd.read_excel('\data\db.xlsx', index_col='Code Chauffeur')
df_unique = df.loc[:,['PRENOM', 'NOM', 'Prenom et Nom', 'TELEPHONE', 'ADRESSE CHAUFFEURS',
       'AGENTS TRANSPORTES', 'ADRESSE EXPERTS', 'CHEF DE BORD', 'VEHICULE',
       'N° CARTE CARBURANT']]

df_unique = df_unique.drop_duplicates()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])

server = app.server

liste_chauffeur = dcc.Dropdown(
    options=[{'label': df_unique.loc[i, "Prenom et Nom"], 'value': i} for i in df_unique.index],
    id='liste_chauffeur',
    value=list(df_unique.index)[1]
)

liste_date_rechargement = dcc.Dropdown(
    options=[
        {'label': 'date1', 'value': 'date1'},
        {'label': 'date2', 'value': 'date2'},
        {'label': 'date3', 'value': 'date3'}
    ], id="date_chargement"
)

img_info = 'assets/68575-icon-of-information.json'
img_speed = 'assets/20534-speedometer.json'
img_fuel = 'assets/76838-fuel-pump.json'
img_money = 'assets/69192-money.json'
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

card_color='#33C6FF'
#33C6FF
#33F4FF
app.layout = html.Div(children=[
    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardImg(src="assets/Logo_ANSD.jpg"),
                     style={'width': '100%', 'border': 'solid'})
        ], width=1),
        dbc.Col(
            dbc.Card(dbc.CardHeader(
                        html.H3("Tableau De Bord De Suivi Consommation Carburant Coordination Carto RGPH-5",
                                    style={'text-align': 'center'}),
                                    ),
                    color= card_color),
            width=11
            )
    ], style={'display': 'flex', 'align-items': 'center', 'margin': '6px'}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(dbc.Col(html.H3("Nom du Chauffeur"))),
                dbc.CardBody(dbc.Col(liste_chauffeur))
            ], color=card_color)
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(dbc.Col(html.H3("Date de rechargement"))),
                dbc.CardBody(dbc.Col(liste_date_rechargement))
            ], color=card_color)
        ]),
    ], style={'margin': '15px'}),

    dbc.Row([
        dbc.Col(dbc.Card([
            #dbc.CardHeader("Informations sur le chauffeur"),
            dbc.CardHeader(de.Lottie(options=options, width="20%", height="20%", url=img_info)),
            dbc.CardBody([
                html.H6("Adresse :"),
                html.H6("Agents transportés :"),
                html.H6("Téléphone :"),
                html.H6("Adresse experts :"),
                html.H6("Chef de Bord :"),
                html.H6("Véhicule :"),
                html.H6("N Carte carburant :"),
            ], id='infos'),
          ], color=card_color), width=3),
    dbc.Col(dbc.Card([
            dbc.CardHeader(de.Lottie(options=options, width="16.5%", height="20%", url=img_fuel)),
            dbc.CardBody("Infos conso", id='conso')
        ], color=card_color
        ), width=3),
    dbc.Col(dbc.Card([
            dbc.CardHeader(de.Lottie(options=options, width="20%", height="20%", url=img_speed)),
            dbc.CardBody("Infos kilometrage", id='kilo')
        ], color=card_color
        ), width=3),
    dbc.Col(dbc.Card([
            dbc.CardHeader(de.Lottie(options=options, width="20%", height="20%", url=img_money)),
            dbc.CardBody("Infos conso totale", id='conso_totale')
        ], color=card_color
        ), width=3)
    ], style={'margin': '15px'}),
], style={'background-color' : '#E7E8EE'})

@app.callback(
    Output(component_id= 'infos', component_property= "children"),
    Output(component_id= "date_chargement", component_property= "options"),
    Output(component_id= "date_chargement", component_property= "value"),
    Input(component_id= 'liste_chauffeur', component_property= 'value')
)
def load_infos_chauffeur(ch):
    list_1 = [
                html.H6("Adresse : " + df_unique.loc[ch, "ADRESSE CHAUFFEURS"]),
                html.H6("Agents transportés : " + df_unique.loc[ch, "AGENTS TRANSPORTES"]),
                html.H6("Téléphone : " + df_unique.loc[ch, "TELEPHONE"]),
                html.H6("Adresse experts : " + df_unique.loc[ch, "ADRESSE EXPERTS"]),
                html.H6("Chef de Bord : " + df_unique.loc[ch, "CHEF DE BORD"]),
                html.H6("Véhicule : " + df_unique.loc[ch, "VEHICULE"]),
                html.H6("N Carte carburant : " + str(df_unique.loc[ch, "N° CARTE CARBURANT"])),
            ]

    list_2 = [{'label': str(i)[0:10], 'value': i} for i in df.loc[ch, "DATE CHARGEMENT"]]

    val = df.loc[ch, "DATE CHARGEMENT"].iloc[0]

    return list_1, list_2, val

@app.callback(
    Output(component_id= 'conso', component_property= "children"),
    Output(component_id='kilo', component_property="children"),
    Output(component_id='conso_totale', component_property="children"),
    Input(component_id= 'date_chargement', component_property= 'value'),
    Input(component_id='liste_chauffeur', component_property='value'),
)
def load_conso(date, ch):
    line_conso = px.line(df.loc[ch, :], y='CONSOMMATION', x='DATE CHARGEMENT')
    list_1 = [html.H6("Consommation : " + str(df[df["DATE CHARGEMENT"]==date].loc[ch, "CONSOMMATION"]),
                     style={'text-align': 'center'}),
              dcc.Graph(figure=line_conso, style={'width': '260px', 'height': '300px'})]

    value_kilo = df[df["DATE CHARGEMENT"] == date].loc[ch, "KILOMETRAGE"]
    max = df.loc[ch, "KILOMETRAGE"].max() + 100
    gauge = daq.Gauge(
        label="Kilométrage : " + str(value_kilo) + " Km",
        value=value_kilo,
        min = 0,
        max=max,
        showCurrentValue=True,
        units="Km",
        color={"gradient": True, "ranges": {"green": [0, max/3], "yellow": [max/3, (2*max)/3], "red": [(2*max)/3, max]}}
    )
    line_kilo = px.line(df.loc[ch, :], y='KILOMETRAGE', x='DATE CHARGEMENT')
    list_2 = [html.H3(gauge,
                      style={'text-align': 'center'}),]
              #dcc.Graph(figure=line_kilo, style={'width': '260px', 'height': '300px'})]

    line_totale = px.line(df.loc[ch, :], y='MONTANT TOTAL EN FCFA', x='DATE CHARGEMENT')
    list_3 = [html.H6("Montant total : " + str(df[df["DATE CHARGEMENT"] == date].loc[ch, "MONTANT TOTAL EN FCFA"]) +
                      " FCFA",
                      style={'text-align': 'center'}),
              dcc.Graph(figure=line_totale, style={'width': '260px', 'height': '300px'})]

    return list_1, list_2, list_3

if __name__=='__main__':
    app.run_server(debug=True)
