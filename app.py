import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import copy

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Análisis SACMEX"
server = app.server

df = pd.read_csv('POZOS_IZTAPALAPA.csv')

pozos = list(df['NOMBRE'])

# Create global chart template
#px.set_mapbox_access_token("pk.eyJ1IjoiZ29uemFsb3NhIiwiYSI6ImNrcmRyNWU3bjBlMHgydmxqZndncG0wc20ifQ.FXQC4_1tyoVfPbE1SFbfIw")

mapbox_access_token = "pk.eyJ1IjoiZ29uemFsb3NhIiwiYSI6ImNrcmRyNWU3bjBlMHgydmxqZndncG0wc20ifQ.FXQC4_1tyoVfPbE1SFbfIw"

layout = dict(
    autosize=True,
    #automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Vista Satélite",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="streets",
        center=dict(lon=-99.08, lat=19.34),
        zoom=11,
    ),
)

app.layout = html.Div([
    html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("logo_2048.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "POZOS IZTAPALAPA",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Análisis de Información", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "10px"},
        ),

    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in pozos],
                value='CERRO DE LA ESTRELLA No. 1'
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),
        html.Div(
        [
            html.Div(
                [html.H6(id="num_nan_text"), html.P("Num. NaN")],
                id="wells",
                className="mini_container",
            ),
            html.Div(
                [html.H6(id="por_nan_text"), html.P("% NaN")],
                id="gas",
                className="mini_container",
            ),
            html.Div(
                [html.H6(id="num_cero_text"), html.P("Num Cero")],
                id="oil",
                className="mini_container",
            ),
            html.Div(
                [html.H6(id="por_cero_text"), html.P("% Cero")],
                id="water",
                className="mini_container",
            ),
        ],
        id="info-container",
        className="row container-display",
        ),
        html.Div(
        [
            html.Div(
                [html.H6(id="Q_med_text"), html.P("Num. NaN")],
                id="wells1",
                className="mini_container",
            ),
            html.Div(
                [html.H6(id="vol_tot_text"), html.P("% NaN")],
                id="gas1",
                className="mini_container",
            ),
            html.Div(
                [html.H6(id="num_cero_text1"), html.P("Num Cero")],
                id="oil1",
                className="mini_container",
            ),
            html.Div(
                [html.H6(id="por_cero_text1"), html.P("% Cero")],
                id="water1",
                className="mini_container",
            ),
        ],
        id="info-container2",
        className="row container-display",
        ),

    ], style={
        'padding': '10px 5px'
    }),
    html.Div(
        [
            html.Div(
                [dcc.Graph(id='crossfilter-indicator-scatter')],
                className="pretty_container seven columns",
            ),
            html.Div(
                [dcc.Graph(id='x-time-series')],
                className="pretty_container five columns",
            ),
        ],
        className="row flex-display",
    ),
    html.Div(
        [
            html.Div(
                [dcc.Graph(id="count_graph")],
                className="pretty_container twelve columns",
            ),
        ],
        className="row flex-display"
    ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value')]
)
def update_graph(xaxis_column_name):

    mi = df[df["NOMBRE"] == xaxis_column_name]
    mi.reset_index(inplace=True)
    la = mi["Y"][0]
    lo = mi["X"][0]
    layout["mapbox"]["center"]["lon"] = lo
    layout["mapbox"]["center"]["lat"] = la

    traces =[]
    trace = dict(
        type="scattermapbox",
        lon=df["X"],
        lat=df["Y"],
        text=df["NOMBRE"],
        customdata=df["NOMBRE"],
        name="Pozos",
        marker=dict(size=10, color=df["Q_L_S"], colorscale="Viridis", showscale=True),
    )
    traces.append(trace)
    fig = dict(data=traces, layout=layout)
    """
    fig = px.scatter_mapbox(df, lat="Y", lon="X",  color="NOMBRE", hover_name="NOMBRE",size="Q_L_S",color_continuous_scale="icefire", zoom =10, size_max=15)
    fig.update_traces(showlegend=False)
    fig.update_layout(margin={'l': 20, 'b': 10, 't': 10, 'r': 10}, hovermode='closest')
    """
    return fig
"""
@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value')]
)
def update_operacion(xaxis_column_name):
    mi = df[df["NOMBRE"] == xaxis_column_name]
    mi.reset_index(inplace=True)
    a = mi["ID_2"][0]
    dfpozo = pd.read_excel("data/0"+a+".xlsx")
    dfpozo.columns = ["fecha_hora", "gasto", "presion"]
    #genera el index con la columna Fecha_Hora
    datetime_rowid = dfpozo['fecha_hora'].map(lambda t: pd.to_datetime(t, format= '%d/%m/%Y %H:%M'))
    dfpozo.index = datetime_rowid
    
    layout_individual = copy.deepcopy(layout)
    data = [
        dict(
            type="scatter",
            mode="markers",
            #name="Gas Produced (mcf)",
            x=dfpozo["gasto"],
            y=dfpozo["presion"],
            #line=dict(shape="spline", smoothing=2, width=1, color="#fac1b7"),
            marker=dict(symbol="diamond-open"),
            labels=dict(x="Gasto (lps)", y="Presion (kg/cm2)"),
        )
    ]
    layout_individual["title"] = "Gasto (x) vs Presiones (y)"
    fig = dict(data=data, layout=layout_individual)

    return fig

@app.callback(
    dash.dependencies.Output('count_graph', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value')]
)
def update_serie(xaxis_column_name):
    mi = df[df["NOMBRE"] == xaxis_column_name]
    mi.reset_index(inplace=True)
    a = mi["ID_2"][0]
    dfpozo = pd.read_excel("data/0"+a+".xlsx")
    dfpozo.columns = ["fecha_hora", "gasto", "presion"]
    #genera el index con la columna Fecha_Hora
    datetime_rowid = dfpozo['fecha_hora'].map(lambda t: pd.to_datetime(t, format= '%d/%m/%Y %H:%M'))
    dfpozo.index = datetime_rowid
    
    layout_individual = copy.deepcopy(layout)
    data = [
        dict(
            type="scatter",
            mode="lines+markers",
            name="Gas Produced (mcf)",
            x=dfpozo.index,
            y=dfpozo["gasto"],
            line=dict(shape="spline", smoothing=2, width=1, color="blue"),
            #marker=dict(symbol="diamond-open"),

        )
    ]
    layout_individual["title"] = "Serie de Tiempo"
    fig = dict(data=data, layout=layout_individual)

    return fig
"""
if __name__ == '__main__':
    app.run_server(debug=True)
    