import plotly.express as px
import plotly.graph_objects as go
from db import * 

# Gráfico de Linha
def grafico_linha(df_filtrado, gas, ano_inicio, ano_fim, atividade):
    #Guarda o agrupamento do data frame "ano" e "emissão"
    dados = df_filtrado.groupby('ano')['emissao'].sum().reset_index()

    #Cria o título conforme os filtros aplicados
    titulo = f"Emissões entre {ano_inicio} e {ano_fim}"
    if gas and gas != "Todos os Gases":
        titulo += f" para {gas}"
    if atividade and atividade != "Todas as Atividades":
        titulo += f" em {atividade}"

    #Cria o gráfico e o tipo de gráfico
    fig = go.Figure(data=go.Scatter(
        x=dados["ano"], y=dados["emissao"],
        mode="lines+markers",
        line=dict(color='deepskyblue'),
        marker=dict(size=6),
    ))

    #Atualiza o design do gráfico, cor de fundo, cor da fonte e etc
    fig.update_layout(
        template='plotly_dark',
        title=titulo,
        xaxis_title="Ano",
        yaxis_title="Emissões",
        plot_bgcolor='rgb(43, 43, 43)',
        paper_bgcolor='rgb(43, 43, 43)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='gray'),
        yaxis=dict(gridcolor='gray'),
    )

    return fig

# Gráfico de Barras
def grafico_barras(df_filtrado, gas, ano_inicio, ano_fim, atividade):
    dados = df_filtrado.groupby('ano')['emissao'].sum().reset_index()

    titulo = f"Emissões entre {ano_inicio} e {ano_fim}"
    if gas and gas != "Todos os Gases":
        titulo += f" para {gas}"
    if atividade and atividade != "Todas as Atividades":
        titulo += f" em {atividade}"

    fig = px.bar(dados, x='ano', y='emissao', title=titulo,
                 labels={'emissao': 'Total Emitido', 'ano': 'Anos'})

    fig.update_layout(
        template='plotly_dark',
        xaxis_title="Ano",
        yaxis_title="Emissões",
        plot_bgcolor='rgb(43, 43, 43)',
        paper_bgcolor='rgb(43, 43, 43)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='gray'),
        yaxis=dict(gridcolor='gray'),
    )

    return fig

# Gráfico de Pizza
def grafico_pizza(df_filtrado, gas, ano_inicio, ano_fim, atividade):

    #Obtém o mapeamento dos gases e atividades para melhor leitura das legendas
    gases_formatados, _ = obter_mapeamento_gases()
    atividades_formatadas, _ = obter_mapeamento_atividades()

    titulo = f"Emissões entre {ano_inicio} e {ano_fim}"
    if gas and gas != "Todos os Gases":
        titulo += f" para {gases_formatados.get(gas, gas)}"
    if atividade and atividade != "Todas as Atividades":
        titulo += f" em {atividades_formatadas.get(atividade, atividade)}"

    #Agrupa por ano e emissão caso os dois filtros estejam presentes
    if atividade != "Todas as Atividades" and gas != "Todos os Gases":
        dados = df_filtrado.groupby('ano')['emissao'].sum().reset_index()
        dados["ano"] = dados["ano"].astype(str)
        fig = px.pie(dados, values='emissao', names='ano', title=titulo, hole=0.2)
    
    #Se o filtro de atividades não foi aplicado, então agrupa por atividade e emissão
    elif atividade == "Todas as Atividades":
        dados = df_filtrado.groupby('atividade_economica')['emissao'].sum().reset_index()
        # Aplica o mapeamento aos nomes
        dados["atividade_economica"] = dados["atividade_economica"].map(
            lambda x: atividades_formatadas.get(x, x)
        )
        fig = px.pie(dados, values='emissao', names='atividade_economica', title=titulo, hole=0.2)

    #Se nenhuma das opções foram atendidas (o filtro de gases não foi adicionado) agrupa por gas e emissão
    else:  
        dados = df_filtrado.groupby('gas')['emissao'].sum().reset_index()
        dados["gas"] = dados["gas"].map(
            lambda x: gases_formatados.get(x, x)
        )
        fig = px.pie(dados, values='emissao', names='gas', title=titulo, hole=0.2)

    #Mostra apenas duas casas decimais da porcentagem no gráfico
    fig.update_traces(
        textinfo='percent+label',
        texttemplate='%{percent:.2%}',
        marker=dict(line=dict(color='black', width=1))
    )

    fig.update_layout(
        template='plotly_dark',
        title=titulo,
        plot_bgcolor='rgb(43, 43, 43)',
        paper_bgcolor='rgb(43, 43, 43)',
        font=dict(color='white'),
    )

    return fig