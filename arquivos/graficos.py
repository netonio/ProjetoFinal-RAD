import pandas as pd
import matplotlib.pyplot as plt
import sqlite3 

def carregar_dados():
    #iniciando conexao
    conexao = sqlite3.connect('efeito_estufa.db')

    #Transformando os dados do banco em um dataframe
    df = pd.read_sql_query("SELECT * FROM emissoes", conexao)
    conexao.close()

    #Removendo linhas nulas
    df.dropna(inplace=True)

    #Garantindo que todos os dados da coluna emissão são numéricos
    df['emissao'] = pd.to_numeric(df['emissao'], errors='coerce')

    return df

def grafico_emissao_por_ano(df, gas = None, ano_inicio = None, ano_fim = None):

    if (ano_inicio is None and ano_fim is None) or (1970<=ano_inicio<=2019) and (1970<=ano_fim<=2019) and (ano_inicio < ano_fim):

        df_filtrado = df.copy()

        # Filtra por gás, se necessário
        if gas:
            df_filtrado = df_filtrado[df_filtrado['gas'] == gas]

        # Filtra intervalo de anos, se fornecido
        if ano_inicio is not None and ano_fim is not None:
            df_filtrado = df_filtrado[(df_filtrado['ano'] >= ano_inicio) & (df_filtrado['ano'] <= ano_fim)]
            
        dados = df_filtrado.groupby('ano')['emissao'].sum()

        dados.plot(kind='line', title=f"Emissões por Ano{' - ' + gas if gas else ''}")
        plt.xlabel('Ano')
        plt.ylabel('Emissão')
        plt.grid(True)
        plt.show()

    else:
        print("Por favor, insira anos válidos entre 1970 e 2019, e verifique se o ano de ínicio é menor que o de término.")

def grafico_emissao_por_categoria(df, categoria='gas', ano = None):

    if ano is None or (1970<=ano<=2019):
        # Filtra intervalo de anos, se fornecido
        if ano:
            df = df[df['ano'] == ano]

        #Verifica se categoria é válida
        if categoria not in ['gas','atividade_economica']:
            raise ValueError("Categoria deve ser 'gas' ou 'atividade_economica'.")
        
        dados = df.groupby(categoria)['emissao'].sum()
        dados = dados[dados > 0]

        categoria_formatada = categoria.replace('_',' ').captalize()

        dados.plot(kind='bar', tittle=f'Emissões por {categoria_formatada}', rot=45)
        plt.ylabel('Total Emitido')
        plt.tight_layout() #Ajusta o espaço entre gráfico e texto
        plt.show()
    else:
        print("Por favor, insira um ano de 1970 a 2019")

def grafico_pizza_por_atividade(df, ano = None):

    if ano is None or (1970<=ano<=2019):
        # Filtra intervalo de anos, se fornecido
        if ano:
            df = df[df['ano'] == ano]

        dados = df.groupby('atividade_economica')['emissao'].sum()
        dados = dados[dados > 0]

        valores = dados.values
        labels = dados.index
        explode = [0.2] * len(valores) #Separa as fatias igualmente

        ano = str(ano)

        plt.pie(valores, labels = labels, explode = explode, autopct = '%1.1f%%', startangle = 90)
        plt.legend(labels, loc = 'best')
        plt.axis('equal')
        plt.title(f"Emissões por Atividades Econômicas {' - ' + ano if ano else ''}")
        plt.tight_layout()
        plt.show()

    else:
        print("Por favor, insira um ano de 1970 a 2019")

df = carregar_dados()