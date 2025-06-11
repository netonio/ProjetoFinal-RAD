import sqlite3
import pandas as pd

#FUNÇÕES DO BANCO "EFEITO ESTUFA"
#Conectando ao banco
def carregar_dados():
    conexao = sqlite3.connect('efeito_estufa.db')
    df = pd.read_sql_query("SELECT * FROM emissoes", conexao)
    conexao.close()

    df['emissao'] = pd.to_numeric(df['emissao'], errors='coerce')
    df['ano'] = pd.to_numeric(df['ano'], errors='coerce')

    return df

#Atualiza todos os novos registros para receberem um ID
def atualizar_id_com_rowid(banco,tabela):
    con = sqlite3.connect(banco)
    cursor = con.cursor()

    # Atualiza a coluna ID com o valor de rowid para todos os registros
    cursor.execute(f"""
        UPDATE {tabela}
        SET id = rowid
        WHERE id IS NULL OR id = 0
    """)

    con.commit()
    con.close()

#Adiciona um novo registro ao banco
def adicionar_bd(ano, gas, atividade_economica, emissao):
    con = sqlite3.connect("efeito_estufa.db")
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO emissoes (ano, gas, atividade_economica, emissao)
        VALUES (?, ?, ?, ?)
    """, (ano, gas, atividade_economica, emissao))
    novo_id = cursor.lastrowid  #pega o ID do novo registro
    con.commit()
    con.close()
    return novo_id

#Lista todos os 50 últimos registros, com base no ID decrescente
def listar_bd():
    con = sqlite3.connect("efeito_estufa.db")
    cursor = con.cursor()
    cursor.execute("""
        SELECT id, ano, gas, atividade_economica, emissao FROM emissoes
        ORDER BY id DESC
        LIMIT 50
    """)
    resultados = cursor.fetchall()
    con.close()
    return resultados

#Função para atualizar os dados do banco
def atualizar_bd(id, ano, gas, atividade_economica, emissao):
    con = sqlite3.connect("efeito_estufa.db")
    cursor = con.cursor()
    cursor.execute("""
        UPDATE emissoes SET ano = ?, gas = ?, atividade_economica = ?, emissao = ? 
        WHERE id = ?
    """, (ano, gas, atividade_economica, emissao, id))
    con.commit()
    con.close()

#Função deletar com base no ID
def deletar_bd(id):
    con = sqlite3.connect("efeito_estufa.db")
    cursor = con.cursor()
    cursor.execute("DELETE FROM emissoes WHERE id = ?", (id,))
    con.commit()
    con.close()

#Obtém o menor e maior ano presentes no banco de forma dinâmica
def obter_min_max_ano():
    con = sqlite3.connect("efeito_estufa.db")
    cursor = con.cursor()

    cursor.execute("SELECT MIN(ano), MAX(ano) FROM emissoes")
    min_ano, max_ano = cursor.fetchone()

    con.close()
    return min_ano, max_ano

#Faz o mapeamento dos gases do banco, para melhor leitura
def obter_mapeamento_gases():
    mapeamento = {
            # Mapeamento para as variações GWP e GTP
            "CO2 (t) GWP-AR2": "Dióxido de Carbono Equivalente (t) - GWP AR2",
            "CO2 (t) GWP-AR4": "Dióxido de Carbono Equivalente (t) - GWP AR4",
            "CO2 (t) GWP-AR5": "Dióxido de Carbono Equivalente (t) - GWP AR5",
            "CO2e (t) GWP-AR2": "Dióxido de Carbono Equivalente (t) - GWP AR2",
            "CO2e (t) GWP-AR4": "Dióxido de Carbono Equivalente (t) - GWP AR4",
            "CO2e (t) GWP-AR5": "Dióxido de Carbono Equivalente (t) - GWP AR5",
            "CO2e (t) GTP-AR2": "Dióxido de Carbono Equivalente (t) - GTP AR2",
            "CO2e (t) GTP-AR4": "Dióxido de Carbono Equivalente (t) - GTP AR4",
            "CO2e (t) GTP-AR5": "Dióxido de Carbono Equivalente (t) - GTP AR5",

            "CO2 (t)": "Dióxido de Carbono (toneladas)",
            "HFC-125 (t)": "HFC-125 (toneladas)",
            "HFC-134a (t)": "HFC-134a (toneladas)",
            "HFC-143a (t)": "HFC-143a (toneladas)", 
        }
    mapeamento_inverso = {v: k for k, v in mapeamento.items()}
    return mapeamento, mapeamento_inverso

#Obtém os gases atualmente presentes no banco de dados, e os renomeia com base no mapeamento
def obter_gases():
    con = sqlite3.connect("efeito_estufa.db")
    cursor = con.cursor()
    cursor.execute("SELECT DISTINCT gas FROM emissoes ORDER BY gas")
    gases_brutos = [row[0] for row in cursor.fetchall()] 
    con.close()

    gases_formatados = []

    mapeamento_gases, _ = obter_mapeamento_gases()

    for gas_item in gases_brutos:
        #Trata valores None ou strings vazias primeiro
        if gas_item is not None:
            #Converte para string e remove espaços (se ainda não for string)
            gas_original_limpo = str(gas_item).strip()

            #Mapea para o nome completo
            gas_renomeado = mapeamento_gases.get(gas_original_limpo, gas_original_limpo) 
            gases_formatados.append(gas_renomeado) #Adiciona o gás formatado a lista

    #Remove duplicatas e ordena
    gases_unicos_e_ordenados = sorted(list(set(gases_formatados)))
    
    # Adicionar "Todos os Gases" explicitamente no início
    gases_unicos_e_ordenados.insert(0, "Todos os Gases")

    return gases_unicos_e_ordenados if gases_unicos_e_ordenados else ["Nenhum Gás Encontrado"]

#Faz o mapeamento das atividades do banco, para melhor leitura
def obter_mapeamento_atividades():
    mapeamento = {
        "AGR": "Agricultura",
        "AGROPEC": "Agropecuária",
        "COM": "Comercial",
        "ENE_ELET": "Energia Elétrica",
        "HFC": "Indústria de Refrigeração", 
        "Outra_IND": "Outras Indústrias",
        "PEC": "Pecuária",
        "PROD_COMB": "Produção de Combustíveis",
        "PUB": "Setor Público",
        "TRAN_CARGA": "Transporte de Cargas",
        "TRAN_PASS": "Transporte de Passageiros",
    }
    mapeamento_inverso = {v: k for k, v in mapeamento.items()}
    return mapeamento, mapeamento_inverso

#Obtém as atividades atualmente presentes no banco de dados, e os renomeia com base no mapeamento
def obter_atividades_economicas():
    con = sqlite3.connect("efeito_estufa.db")
    cursor = con.cursor()

    cursor.execute("SELECT DISTINCT atividade_economica FROM emissoes ORDER BY atividade_economica")

    atividades_brutas = [row[0] for row in cursor.fetchall()] 
    con.close()

    atividades_formatadas = []

    mapeamento_atividades, _ = obter_mapeamento_atividades()

    for atividade_item in atividades_brutas:
        
        #Trata valores None ou strings vazias primeiro
        if atividade_item is None or str(atividade_item).strip() == '':
            atividades_formatadas.append("Todas as Atividades")
        else:
            #Converte para string e remove espaços (se ainda não for string)
            atividade_original_str = str(atividade_item).strip()
            
            #Mapea para o nome completo, usando .upper() para a chave
            atividade_renomeada = mapeamento_atividades.get(atividade_original_str, atividade_original_str) 
            atividades_formatadas.append(atividade_renomeada) #Adiciona o gás formatado a lista

    #Remove duplicatas e ordena
    atividades_unicas_e_ordenadas = sorted(list(set(atividades_formatadas)))

    # Garante que "Total Geral de Atividades" esteja no início
    if "Todas as Atividades" in atividades_unicas_e_ordenadas:
        atividades_unicas_e_ordenadas.remove("Todas as Atividades")
    atividades_unicas_e_ordenadas.insert(0, "Todas as Atividades")

    return atividades_unicas_e_ordenadas if atividades_unicas_e_ordenadas else ["Nenhuma Atividade Encontrada"]


#FUNÇÕES DO BANCO "USUÁRIOS"
#Cria a tabela caso não exista
def criar_tabela_usuarios():
    con = sqlite3.connect("usuarios.db")
    cursor = con.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            senha TEXT
        )
    """)
    con.commit()
    con.close()

#Lista os usuários presentes no banco
def listar_usuarios():
    con = sqlite3.connect("usuarios.db")
    cursor = con.cursor()
    cursor.execute("SELECT id, usuario FROM usuarios ORDER BY usuario ASC")
    resultados = cursor.fetchall()
    con.close()
    return resultados

#Adiciona o usuário com base no usuario e senha
def adicionar_usuario(usuario, senha):
    con = sqlite3.connect("usuarios.db")
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        con.commit()
    except sqlite3.IntegrityError:
        con.close()
        raise ValueError("Usuário já existe.") # Raise error se o nome não for único
    finally:
        con.close()

#Busca usuário pelo nome
def buscar_usuario(usuario):
    con = sqlite3.connect("usuarios.db")
    cursor = con.cursor()
    cursor.execute("SELECT id, usuario, senha FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    con.close()
    return resultado

#Busca usuário e senha para login
def buscar_usuario_senha(usuario, senha):
    con = sqlite3.connect("usuarios.db")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
    user = cursor.fetchone()

    con.close()
    return user

#Busca ID do usuário
def buscar_usuario_id(id_usuario):
    con = sqlite3.connect("usuarios.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
    resultado = cursor.fetchone()
    con.close()
    return resultado

#Atualiza o usuário
def atualizar_usuario(id_usuario, novo_nome, nova_senha):
    con = sqlite3.connect("usuarios.db")
    cursor = con.cursor()
    try:
        cursor.execute("UPDATE usuarios SET usuario = ?, senha = ? WHERE id = ?", (novo_nome, nova_senha, id_usuario))
        con.commit()
    except sqlite3.IntegrityError:
        con.close()
        raise ValueError("Novo nome de usuário já existe.") #Raise error se o usuário já existir
    finally:
        con.close()

#Deleta o usuário com base no ID
def deletar_usuario(id_usuario):
    con = sqlite3.connect("usuarios.db")
    cursor = con.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
    con.commit()
    con.close()