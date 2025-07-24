import dash
from dash import dcc, html, Input, Output, State, dash_table, callback
import requests
import pandas as pd
from datetime import datetime
import json

# Configuração da API
API_BASE_URL = "https://deploy-f39z.onrender.com"

# Inicializar a aplicação Dash
app = dash.Dash(__name__)
app.title = "Gerenciador de Livros"
server = app.server

# Layout da aplicação
app.layout = html.Div([
    html.H1("Gerenciador de Livros", style={'textAlign': 'center', 'marginBottom': 30}),
    
    # Container para adicionar novos livros
    html.Div([
        html.H2("Adicionar Novo Livro"),
        html.Div([
            html.Div([
                html.Label("Título:"),
                dcc.Input(
                    id='input-titulo',
                    type='text',
                    placeholder='Digite o título do livro',
                    style={'width': '100%', 'padding': '8px', 'marginTop': '5px'}
                )
            ], style={'marginBottom': '15px'}),
            
            html.Div([
                html.Label("Autor:"),
                dcc.Input(
                    id='input-autor',
                    type='text',
                    placeholder='Digite o nome do autor',
                    style={'width': '100%', 'padding': '8px', 'marginTop': '5px'}
                )
            ], style={'marginBottom': '15px'}),
            
            html.Div([
                html.Label("Ano:"),
                dcc.Input(
                    id='input-ano',
                    type='number',
                    placeholder='Digite o ano de publicação',
                    min=1000,
                    max=datetime.now().year + 10,
                    style={'width': '100%', 'padding': '8px', 'marginTop': '5px'}
                )
            ], style={'marginBottom': '15px'}),
            
            html.Button(
                'Adicionar Livro',
                id='btn-adicionar',
                n_clicks=0,
                style={
                    'backgroundColor': '#007bff',
                    'color': 'white',
                    'padding': '10px 20px',
                    'border': 'none',
                    'borderRadius': '5px',
                    'cursor': 'pointer',
                    'fontSize': '16px'
                }
            )
        ], style={
            'backgroundColor': '#f8f9fa',
            'padding': '20px',
            'borderRadius': '10px',
            'marginBottom': '30px'
        })
    ]),
    
    # Container para mensagens
    html.Div(id='mensagem', style={'marginBottom': '20px'}),
    
    # Container para listar livros
    html.Div([
        html.H2("Lista de Livros"),
        html.Button(
            'Atualizar Lista',
            id='btn-atualizar',
            n_clicks=0,
            style={
                'backgroundColor': '#28a745',
                'color': 'white',
                'padding': '8px 16px',
                'border': 'none',
                'borderRadius': '5px',
                'cursor': 'pointer',
                'marginBottom': '15px'
            }
        ),
        html.Div(id='tabela-livros')
    ])
], style={'max-width': '1200px', 'margin': '0 auto', 'padding': '20px'})

# Função para buscar livros da API
def buscar_livros():
    try:
        response = requests.get(f"{API_BASE_URL}/livros")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except requests.RequestException:
        return []

# Função para adicionar livro via API
def adicionar_livro_api(titulo, autor, ano):
    try:
        data = {
            "titulo": titulo,
            "autor": autor,
            "ano": ano
        }
        response = requests.post(f"{API_BASE_URL}/livros", json=data)
        return response.status_code == 201, response.json() if response.status_code == 201 else response.text
    except requests.RequestException as e:
        return False, str(e)

# Callback para adicionar livro
@app.callback(
    [Output('mensagem', 'children'),
     Output('input-titulo', 'value'),
     Output('input-autor', 'value'),
     Output('input-ano', 'value')],
    [Input('btn-adicionar', 'n_clicks')],
    [State('input-titulo', 'value'),
     State('input-autor', 'value'),
     State('input-ano', 'value')]
)
def adicionar_livro(n_clicks, titulo, autor, ano):
    if n_clicks > 0:
        # Validações
        if not titulo or len(titulo.strip()) < 3:
            return html.Div("Título deve ter pelo menos 3 caracteres.", 
                          style={'color': 'red', 'padding': '10px', 'backgroundColor': '#f8d7da', 'borderRadius': '5px'}), titulo, autor, ano
        
        if not autor or len(autor.strip()) < 3:
            return html.Div("Autor deve ter pelo menos 3 caracteres.", 
                          style={'color': 'red', 'padding': '10px', 'backgroundColor': '#f8d7da', 'borderRadius': '5px'}), titulo, autor, ano
        
        if not ano or ano < 1000:
            return html.Div("Ano deve ser maior que 1000.", 
                          style={'color': 'red', 'padding': '10px', 'backgroundColor': '#f8d7da', 'borderRadius': '5px'}), titulo, autor, ano
        
        # Tentar adicionar o livro
        sucesso, resultado = adicionar_livro_api(titulo.strip(), autor.strip(), ano)
        
        if sucesso:
            return html.Div(f"Livro '{titulo}' adicionado com sucesso!", 
                          style={'color': 'green', 'padding': '10px', 'backgroundColor': '#d4edda', 'borderRadius': '5px'}), "", "", None
        else:
            return html.Div(f"Erro ao adicionar livro: {resultado}", 
                          style={'color': 'red', 'padding': '10px', 'backgroundColor': '#f8d7da', 'borderRadius': '5px'}), titulo, autor, ano
    
    return "", titulo, autor, ano

# Callback para atualizar a tabela de livros
@app.callback(
    Output('tabela-livros', 'children'),
    [Input('btn-atualizar', 'n_clicks'),
     Input('btn-adicionar', 'n_clicks')]
)
def atualizar_tabela(n_clicks_atualizar, n_clicks_adicionar):
    livros = buscar_livros()
    
    if not livros:
        return html.Div("Nenhum livro encontrado ou erro na conexão com a API.", 
                       style={'padding': '20px', 'textAlign': 'center', 'color': '#6c757d'})
    
    # Converter para DataFrame para usar com dash_table
    df = pd.DataFrame(livros)
    
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[
            {"name": "ID", "id": "id", "type": "numeric"},
            {"name": "Título", "id": "titulo", "type": "text"},
            {"name": "Autor", "id": "autor", "type": "text"},
            {"name": "Ano", "id": "ano", "type": "numeric"}
        ],
        style_cell={
            'textAlign': 'left',
            'padding': '12px',
            'fontFamily': 'Arial, sans-serif'
        },
        style_header={
            'backgroundColor': '#007bff',
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_data={
            'backgroundColor': '#f8f9fa'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#ffffff'
            }
        ],
        sort_action="native",
        filter_action="native",
        page_action="native",
        page_current=0,
        page_size=10
    )

if __name__ == '__main__':
    app.run(debug=True, port=8050)
