from dash import dash, html, dcc
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import dash_daq as daq
import dash_extensions as de

df = pd.read_excel('db.xlsx', index_col='Code Chauffeur')
#df = pd.read_excel('data\db.xlsx', index_col='Code Chauffeur')
df_unique = df.loc[:,['PRENOM', 'NOM', 'Prenom et Nom', 'TELEPHONE', 'ADRESSE CHAUFFEURS',
       'AGENTS TRANSPORTES', 'ADRESSE EXPERTS', 'CHEF DE BORD', 'VEHICULE',
       'N° CARTE CARBURANT']]

df_unique = df_unique.drop_duplicates()
kilometrage_total = df.groupby("VEHICULE").max("KILOMETRAGE")["KILOMETRAGE"].sum()
consommation_total = df["CONSOMMATION"].sum()
montant_total_FCFA = df.groupby("VEHICULE").max("MONTANT TOTAL EN FCFA")["MONTANT TOTAL EN FCFA"].sum()

graph_1 = px.bar(df.groupby("VEHICULE").max("KILOMETRAGE"), y=["KILOMETRAGE", "MONTANT TOTAL EN FCFA"], text_auto=True)
df2 = pd.DataFrame(df.groupby("VEHICULE").sum("CONSOMMATION"))
df2["Plaque"]= df2.index
graph_2 = px.pie(df2, values="CONSOMMATION", names="Plaque",
                 color_discrete_sequence=px.colors.sequential.RdBu, hole=.3)
#_______________________________________________________________________________________________________________________
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])
app.title = "Suivi conso carburant"
server = app.server

card_color='#33C6FF'
#_______________________________________________________________________________________________________________________
# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "15rem",
    "padding": "1rem 1rem",
    "background-color": card_color,
}
#"#f8f9fa"
# padding for the page content
CONTENT_STYLE = {
    "margin-left": "14rem",
    #"margin-right": "2rem",
    #"padding": "2rem 1rem",
}
sidebar = html.Div(
    [
        dbc.Card(dbc.CardImg(src="assets/RGPH-5.jpg"),
                     style={'width': '80%', 'border': 'solid'}),
        html.Label("Je suis recencé, je compte"),
        html.Hr(),
        html.H5("Menu"),
        #html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Accueil", href="/", active="exact", style={'color': 'black'}),
                dbc.NavLink("Situation par chauffeur", href="/page-1-ch", active="exact", style={'color': 'black'}),
                dbc.NavLink("Situation par carte", href="/page-2-carte", active="exact", style={'color': 'black'}),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        dbc.Card(dbc.CardImg(src="assets/Logo_ANSD.jpg"),
                     style={'width': '80%', 'border': 'solid'}),
    ],
    style=SIDEBAR_STYLE
)
#_______________________________________________________________________________________________________________________

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
#_______________________________________________________________________________________________________________________
img_info = 'assets/68575-icon-of-information.json'
img_speed = 'assets/20534-speedometer.json'
img_fuel = 'assets/76838-fuel-pump.json'
img_money = 'assets/69192-money.json'
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))
#_______________________________________________________________________________________________________________________

#33C6FF
#33F4FF
page_1 = html.Div(children=[
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardHeader(
                        html.H5("Tableau De Bord De Suivi Consommation Carburant Coordination Carto RGPH-5",
                                    style={'text-align': 'center'}),
                                    ),
                    color= card_color),
            )
    ], style={'display': 'flex', 'align-items': 'center', 'margin': '6px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(dbc.Col(html.H5("Nom du Chauffeur"))),
                dbc.CardBody(dbc.Col(liste_chauffeur))
            ], color=card_color)
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(dbc.Col(html.H5("Date de rechargement"))),
                dbc.CardBody(dbc.Col(liste_date_rechargement))
            ], color=card_color)
        ]),
    ], style={'margin': '15px'}),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(de.Lottie(options=options, width="20%", height="20%", url=img_speed)),
            dbc.CardBody("Infos kilometrage", id='kilo')
        ], color=card_color
        ), width=4),
        dbc.Col(dbc.Card([
                dbc.CardHeader(de.Lottie(options=options, width="16.5%", height="20%", url=img_fuel)),
                dbc.CardBody("Infos conso", id='conso')
            ], color=card_color
            ), width=4),
        dbc.Col(dbc.Card([
                dbc.CardHeader(de.Lottie(options=options, width="20%", height="20%", url=img_money)),
                dbc.CardBody("Infos conso totale", id='conso_totale')
            ], color=card_color
            ), width=4)
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
          ], color=card_color, style={'width': '100%', 'height': '300px'}), width=4),
        dbc.Col(dbc.Card(
            dbc.CardBody(
                dcc.Graph(id='global_graph', style={'width': '100%', 'height': '300px'})
                )
            , color=card_color),
            width=8
        )
    ], style={'margin': '15px'}),
], style={'background-color' : '#E7E8EE'})
#_______________________________________________________________________________________________________________________
page_accueil = html.Div(children=[
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardHeader(
                        html.H5("Tableau De Bord De Suivi Consommation Carburant Coordination Carto RGPH-5",
                                    style={'text-align': 'center'}),
                                    ),
                    color= card_color),
            )
    ], style={'display': 'flex', 'align-items': 'center', 'margin': '6px'}),

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(de.Lottie(options=options, width="20%", height="20%", url=img_speed)),
            dbc.CardBody([
                html.H5("Kilométrage total (toute voitures confondues): "),
                daq.LEDDisplay(value=kilometrage_total, color="#FF5E5E")
            ], id='kilo-accueil')
        ], color=card_color
        ), width=4),
        dbc.Col(dbc.Card([
                dbc.CardHeader(de.Lottie(options=options, width="16.5%", height="20%", url=img_fuel)),
                dbc.CardBody([html.H5("Consommation totale en Litre (toute voitures confondues): "),
                              daq.LEDDisplay(value=consommation_total, color="#FF5E5E")
                              ],
                             id='conso-accueil')
            ], color=card_color
            ), width=4),
        dbc.Col(dbc.Card([
                dbc.CardHeader(de.Lottie(options=options, width="20%", height="20%", url=img_money)),
                dbc.CardBody([
                    html.H5("Montant total en FCFA(toute voitures confondues): "),
                    daq.LEDDisplay(value=montant_total_FCFA, color="#FF5E5E")
                ],
                             id='conso_totale-accueil')
            ], color=card_color
            ), width=4)
        ], style={'margin': '15px'}),
    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody(
                dcc.Graph(figure=graph_1,
                    id='global_graph_1-accueil', style={'width': '100%', 'height': '300px'})
                )
            , color=card_color),
            width=7
        ),
        dbc.Col(dbc.Card(
            dbc.CardBody(
                dcc.Graph(figure=graph_2,
                    id='global_graph_2-accueil', style={'width': '100%', 'height': '300px'})
                )
            , color=card_color),
            width=5
        ),
    ], style={'margin': '15px'}),
], style={'background-color' : '#E7E8EE'})
#_______________________________________________________________________________________________________________________
content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname=="/":
        return page_accueil
    elif pathname=="/page-1-ch":
        return page_1
    elif pathname=="/page-2-carte":
        return html.H1("Page à définir ...", style={"margin-left": "1rem"}, className="text-danger")
    return dbc.Container(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ], style={"margin-left": "1rem"}
    )
#________________________________________Callback Accueil_______________________________________________________________________________

#_______________________________________________Callback page_1________________________________________________________________________
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
    Output(component_id='global_graph', component_property="figure"),
    Input(component_id= 'date_chargement', component_property= 'value'),
    Input(component_id='liste_chauffeur', component_property='value'),
)
def load_conso(date, ch):
    line_conso = px.line(df.loc[ch, :], y='CONSOMMATION', x='DATE CHARGEMENT')
    list_1 = [html.H6("Consommation : " + str(df[df["DATE CHARGEMENT"]==date].loc[ch, "CONSOMMATION"]),
                     style={'text-align': 'center'}),
              dcc.Graph(figure=line_conso, style={'width': '100%', 'height': '300px'})]

    value_kilo = df[df["DATE CHARGEMENT"] == date].loc[ch, "KILOMETRAGE"]
    max = df.loc[ch, "KILOMETRAGE"].max() + 100
    gauge = daq.Gauge(
        label="Kilométrage : " + str(value_kilo) + " Km",
        value=value_kilo,
        min = 0,
        max=max,
        showCurrentValue=True,
        units="Km",
        color={"gradient": True, "ranges": {"green": [0, max/3], "yellow": [max/3, (2*max)/3], "red": [(2*max)/3, max]}},
        style={'width': '100%'}
    )
    line_kilo = px.line(df.loc[ch, :], y='KILOMETRAGE', x='DATE CHARGEMENT')
    list_2 = gauge
              #dcc.Graph(figure=line_kilo, style={'width': '260px', 'height': '300px'})]

    line_totale = px.line(df.loc[ch, :], y='MONTANT TOTAL EN FCFA', x='DATE CHARGEMENT')
    list_3 = [html.H6("Montant total : " + str(df[df["DATE CHARGEMENT"] == date].loc[ch, "MONTANT TOTAL EN FCFA"]) +
                      " FCFA",
                      style={'text-align': 'center'}),
              dcc.Graph(figure=line_totale, style={'width': '100%', 'height': '300px'})]

    global_graph = px.line(df.loc[ch, :], y=['MONTANT TOTAL EN FCFA', 'KILOMETRAGE', 'CONSOMMATION'], x='DATE CHARGEMENT')

    return list_1, list_2, list_3, global_graph
# {'width': '260px', 'height': '300px'}
if __name__=='__main__':
    app.run_server(debug=True)
