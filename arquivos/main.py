import customtkinter as ctk
from customtkinter import CTkImage
import plotly.io as pio
import io
import os
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
from tkinter import filedialog
from db import *
from graficos import *

#Classe principal da aplicação
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Tenta carregar o ícone da janela
        try:
            icon_image = Image.open("imagens/efeito_estufa_icone.png")
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.iconphoto(False, icon_photo)
            self._icon_image_ref = icon_photo  # Evita o garbage collection da imagem
        except Exception as e:
            print("Erro ao carregar ícone:", e)

        # Configurações iniciais da janela
        self.geometry("950x500")  # Define o tamanho da janela
        self.title("Estufatos")  # Define o título da janela

        # Exibe a tela de login ao iniciar
        self.login_frame = Tela_login(self, self.entrar)
        self.login_frame.pack(fill="both", expand=True)

        # Garante que a tabela de usuários exista no banco de dados
        criar_tabela_usuarios()

    # Função chamada ao tentar fazer login
    def entrar(self, usuario, senha):
        user = buscar_usuario_senha(usuario, senha)  # Verifica se as credenciais são válidas
        if user:
            self.login_frame.destroy()  # Remove a tela de login
            self.menu_principal()  # Cria o menu lateral
            self.abrir_inicio()  # Abre a página inicial
        else:
            self.login_frame.mensagem("Usuário ou senha incorretos")  # Mostra erro

    # Cria o menu lateral com botões de navegação
    def menu_principal(self):
        # Frame do menu lateral
        self.menu = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu.pack(side="left", fill="y")

        # Estilo padrão dos botões
        botao_config = {
            "corner_radius": 0,
            "fg_color": "#2a2a2a",
            "hover_color": "#3a3a3a",
            "text_color": "white",
            "width": 180,
            "height": 40
        }

        # Criação dos botões de navegação
        ctk.CTkLabel(self.menu, text="Menu", font=("Arial", 20)).pack(pady=20)
        ctk.CTkButton(self.menu, text="Início", command=self.abrir_inicio, **botao_config).pack()
        ctk.CTkButton(self.menu, text="Gráficos", command=self.abrir_graficos, **botao_config).pack()
        ctk.CTkButton(self.menu, text="Usuários", command=self.abrir_usuarios, **botao_config).pack()
        ctk.CTkButton(self.menu, text="Dados", command=self.abrir_pagina_bd, **botao_config).pack()

        # Frame onde as páginas serão exibidas
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="left", fill='both', expand=True)

    # Funções para abrir as páginas correspondentes
    def abrir_inicio(self):
        self._abrir_pagina(Pagina_inicio)

    def abrir_graficos(self):
        self._abrir_pagina(Pagina_graficos)

    def abrir_usuarios(self):
        # Passa o callback para permitir edição de usuários
        def abrir_pagina_usuarios(parent):
            self.pagina_usuarios = Pagina_usuarios(parent, self.abrir_dialogo_edicao)
            return self.pagina_usuarios

        self._abrir_pagina(abrir_pagina_usuarios)

    def abrir_pagina_bd(self):
        self._abrir_pagina(Pagina_bd)

    # Função genérica para abrir qualquer página
    def _abrir_pagina(self, Pagina):
        # Remove qualquer conteúdo anterior do container
        for widget in self.container.winfo_children():
            widget.destroy()
        # Verifica se a página é uma função ou classe e a instancia
        if callable(Pagina):
            Pagina(self.container).pack(fill="both", expand=True)
        else:
            Pagina(self.container).pack(fill="both", expand=True)

    # Mostra a tela de login
    def mostrar_login(self):
        if hasattr(self, "cadastro_frame"):
            self.cadastro_frame.destroy()  # Remove tela de cadastro se existir
        self.login_frame = Tela_login(self, self.entrar)
        self.login_frame.pack(fill="both", expand=True)

    # Mostra a tela de cadastro
    def mostrar_cadastro(self):
        self.login_frame.destroy()  # Remove a tela de login
        self.cadastro_frame = Tela_cadastro(self, self.mostrar_login)
        self.cadastro_frame.pack(fill="both", expand=True)

    # Abre o diálogo de edição de usuário
    def abrir_dialogo_edicao(self, id_usuario, nome_usuario, callback_atualizar_lista):
        EditarUsuarioDialog(
            parent=self,
            id_usuario=id_usuario,
            nome_atual=nome_usuario,
            callback_atualizar_lista=callback_atualizar_lista,
            callback_status_label=self._atualizar_status_usuarios
        )

    # Atualiza a mensagem de status da página de usuários (ex: após editar ou excluir alguém)
    def _atualizar_status_usuarios(self, mensagem, cor="white"):
        if hasattr(self, 'pagina_usuarios'):
            self.pagina_usuarios._atualizar_status_label(mensagem, cor)

# Tela de login
class Tela_login(ctk.CTkFrame):
    def __init__(self, parent, entrar_callback):
        super().__init__(parent)
        self.entrar_callback = entrar_callback  # Função de callback que será chamada após login bem-sucedido

        # Define estrutura de grid da tela de login
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)

        # Cria um frame central para conter os campos de login
        login_frame = ctk.CTkFrame(self)
        login_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        login_frame.grid_columnconfigure(0, weight=1)
        login_frame.grid_rowconfigure((0,1,2,3,4), weight=1)

        # Título da seção de login
        ctk.CTkLabel(login_frame, text="Login", font=("Arial", 28, "bold")).grid(row=0, column=0, pady=20, sticky="s")

        # Campo para entrada do nome de usuário
        self.entrada_usuario = ctk.CTkEntry(login_frame, placeholder_text="Usuário", width=200)
        self.entrada_usuario.grid(row=1, column=0, pady=10)

        # Campo de senha (ocultando o texto com '*')
        self.entrada_senha = ctk.CTkEntry(login_frame, placeholder_text="Senha", show="*", width=200)
        self.entrada_senha.grid(row=2, column=0, pady=10)

        # Botão de login
        ctk.CTkButton(login_frame, text="Entrar", command=self._fazer_login,
                      font=("Arial", 16, "bold"), fg_color="#007bff", hover_color="#0056b3").grid(row=3, column=0, pady=15)

        # Label que mostra mensagens de erro
        self.label_erro = ctk.CTkLabel(login_frame, text="", text_color="red", font=("Arial", 12))
        self.label_erro.grid(row=4, column=0, pady=5, sticky="n")

        # Texto e botão para quem ainda não tem conta
        ctk.CTkLabel(login_frame, text="Não tem uma conta?", font=("Arial", 14)).grid(row=5, column=0, pady=(20,5))
        ctk.CTkButton(login_frame, text="Criar Conta", command=lambda: self.master.mostrar_cadastro(),
                      font=("Arial", 14), fg_color="transparent", text_color="#007bff", hover_color="#3a3a3a").grid(row=6, column=0, pady=(0,10))

    def _fazer_login(self):
        # Obtém os valores digitados e remove espaços em branco
        usuario = self.entrada_usuario.get().strip()
        senha = self.entrada_senha.get().strip()

        # Verifica se os campos estão preenchidos
        if not usuario or not senha:
            self.mensagem("Por favor, preencha todos os campos.")
            return

        # Busca usuário no banco de dados
        user = buscar_usuario_senha(usuario, senha)
        if user:
            self.entrar_callback(usuario, senha)  # Login bem-sucedido -> entra na aplicação
        else:
            self.mensagem("Usuário ou senha incorretos.")  # Mensagem de erro

    def mensagem(self, msg, cor="red"):
        # Mostra uma mensagem (erro ou sucesso) com a cor definida
        self.label_erro.configure(text=msg, text_color=cor)

# Tela de cadastro
class Tela_cadastro(ctk.CTkFrame):
    def __init__(self, parent, mostrar_login_callback):
        super().__init__(parent)
        self.mostrar_login_callback = mostrar_login_callback  # Callback para voltar à tela de login

        # Define a estrutura de grid da tela
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5), weight=1)

        # Cria o frame onde os campos de cadastro ficam
        cadastro_frame = ctk.CTkFrame(self)
        cadastro_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        cadastro_frame.grid_columnconfigure(0, weight=1)
        cadastro_frame.grid_rowconfigure((0,1,2,3,4), weight=1)

        # Título da seção de cadastro
        ctk.CTkLabel(cadastro_frame, text="Criar Nova Conta", font=("Arial", 28, "bold")).grid(row=0, column=0, pady=20, sticky="s")

        # Campo para novo nome de usuário
        self.entrada_usuario = ctk.CTkEntry(cadastro_frame, placeholder_text="Novo Usuário", width=200)
        self.entrada_usuario.grid(row=1, column=0, pady=10)

        # Campo para senha da nova conta
        self.entrada_senha = ctk.CTkEntry(cadastro_frame, placeholder_text="Senha", show="*", width=200)
        self.entrada_senha.grid(row=2, column=0, pady=10)

        # Botão para cadastrar o novo usuário
        ctk.CTkButton(cadastro_frame, text="Cadastrar", command=self._cadastrar,
                      font=("Arial", 16, "bold"), fg_color="#28a745", hover_color="#218838").grid(row=3, column=0, pady=15)

        # Mensagens de erro ou sucesso
        self.label_mensagem = ctk.CTkLabel(cadastro_frame, text="", text_color="red", font=("Arial", 12))
        self.label_mensagem.grid(row=4, column=0, pady=5, sticky="n")

        # Texto e botão para voltar ao login
        ctk.CTkLabel(cadastro_frame, text="Já tem uma conta?", font=("Arial", 14)).grid(row=5, column=0, pady=(20,5))
        ctk.CTkButton(cadastro_frame, text="Voltar ao Login", command=self.mostrar_login_callback,
                      font=("Arial", 14), fg_color="transparent", text_color="#007bff", hover_color="#3a3a3a").grid(row=6, column=0, pady=(0,10))

        def _cadastrar(self):
        # Obtém entradas e remove espaços em branco
            usuario = self.entrada_usuario.get().strip()
            senha = self.entrada_senha.get().strip()

            # Verifica se os campos estão preenchidos
            if not usuario or not senha:
                self.mensagem("Por favor, preencha todos os campos.")
                return

            try:
                # Tenta adicionar o novo usuário ao banco de dados
                adicionar_usuario(usuario, senha)
                self.mensagem("Conta criada com sucesso! Faça login.", "green")
                
                # Limpa os campos após sucesso
                self.entrada_usuario.delete(0, ctk.END)
                self.entrada_senha.delete(0, ctk.END)

                # Retorna para a tela de login após 1 segundo
                self.master.after(1000, self.mostrar_login_callback)
            except ValueError as e:
                # Erro esperado, como usuário já existente
                self.mensagem(str(e))
            except Exception as e:
                # Erro inesperado
                self.mensagem(f"Erro ao cadastrar: {e}")

    def mensagem(self, msg, cor="red"):
        # Exibe mensagem com a cor desejada
        self.label_mensagem.configure(text=msg, text_color=cor)

# Página inicial com rolagem
class Pagina_inicio(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.sections = []

        self.titulo_label = ctk.CTkLabel(self, text="Início", font=("Arial", 28, "bold"))
        self.titulo_label.pack(pady=15)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(expand=True, fill="both", padx=20, pady=10)

        # Dados das seções para recriar quando necessário
        # Formato: (titulo, texto, caminho_da_imagem)
        # Usar None se não houver imagem para a seção
        self.section_data = [
            ("O que é o Efeito Estufa?",
             "O efeito estufa é um processo natural e essencial para a vida na Terra. Ele ocorre quando certos gases na atmosfera — como dióxido de carbono (CO2), metano (CH4) e vapor d'água — retêm parte do calor irradiado pela superfície do planeta.Essa retenção de calor é crucial para manter a temperatura média da Terra em níveis que permitem a existência de água líquida e, consequentemente, da vida. Sem o efeito estufa, nosso planeta seria um lugar muito gelado e inabitável.",
             "imagens/efeito_estufa.png"), 
            ("Como funciona?",
             "Funciona assim: a luz solar atravessa a atmosfera e aquece a Terra. Parte desse calor é refletido de volta para o espaço. No entanto, os gases de efeito estufa presentes na atmosfera absorvem e reirradiam esse calor em todas as direções, inclusive de volta para a superfície. Esse processo aprisiona o calor, elevando a temperatura do planeta. É um equilíbrio delicado que mantém nosso clima estável e adequado para a vida.",
             "imagens/funcionamento.png"),
            ("Efeitos do aquecimento global",
             "O aquecimento global é o agravamento do efeito estufa natural devido às atividades humanas. A queima de combustíveis fósseis (carvão, petróleo, gás) e o desmatamento liberam um excesso de gases de efeito estufa na atmosfera, intensificando a retenção de calor e elevando a temperatura média da Terra. As consequências são severas e globais: degelo polar, elevação do nível do mar, eventos climáticos extremos (ondas de calor, secas, inundações) e impactos na biodiversidade. Compreender isso é vital para a busca por soluções climáticas.",
             None),
            ("Anos de Pico de Emissões no Brasil (1990-2019)",
             "Entre 1990 e 2019, as emissões de gases do efeito estufa (GEE) no Brasil foram fortemente influenciadas pelo desmatamento. Os anos de **maior emissão** ocorreram principalmente no **início dos anos 2000, com picos notáveis por volta de 2004 e 2005**, devido às altas taxas de devastação da Amazônia para a expansão da agropecuária. Apesar de uma queda significativa de 2005 a 2012, as emissões voltaram a crescer a partir de **2013**, com **2019** registrando outro aumento considerável, novamente impulsionado pelo desmatamento. Além da mudança de uso da terra, a agropecuária e a energia também foram contribuintes importantes nesse período.",
             "imagens/grafico.png"),
            ("Dióxido de Carbono (CO2)",
             "O **Dióxido de Carbono (CO2)** é o gás de efeito estufa mais emitido por atividades humanas e o principal responsável pelo aquecimento global. Sua emissão é predominantemente causada pela queima de combustíveis fósseis (carvão, petróleo e gás natural) em processos industriais, geração de energia, transportes e aquecimento. Além disso, o desmatamento, que libera o carbono armazenado em árvores e solos, também contribui significativamente para o aumento das concentrações de CO2 na atmosfera.",
             None),
            ("HFC-125 (Pentafluoroetano)",
             "O **HFC-125** é um hidrofluorcarbono (HFC) e um potente gás de efeito estufa sintético. Ele é amplamente utilizado como agente extintor de incêndio, substituindo os antigos halons que danificavam a camada de ozônio. Também pode ser encontrado em algumas misturas refrigerantes. Embora seja uma alternativa aos produtos que afetam o ozônio, o HFC-125 tem um alto potencial de aquecimento global, contribuindo para o efeito estufa.",
             None),
            ("HFC-134a (Tetrafluoroetano)",
             "O **HFC-134a** é outro hidrofluorcarbono com um impacto significativo no efeito estufa. É um dos refrigerantes mais comuns, utilizado em sistemas de ar condicionado automotivo e residencial, bem como em aerossóis e alguns produtos de espuma. Sua popularidade cresceu como substituto de substâncias que esgotavam a camada de ozônio, mas seu elevado potencial de aquecimento global o torna uma preocupação ambiental.",
             None),
            ("HFC-143a (1,1,1-Trifluoroetano)",
             "O **HFC-143a** é um terceiro hidrofluorcarbono potente. Ele é frequentemente usado como um componente em misturas refrigerantes, especialmente em sistemas de refrigeração de alta temperatura, e também pode ser encontrado em aerossóis e aplicações de isolamento. Assim como outros HFCs, o HFC-143a foi desenvolvido para substituir substâncias danosas ao ozônio, mas contribui substancialmente para o aquecimento global devido ao seu alto potencial de retenção de calor.",
             None) 
        ]

        # Cria seções iniciais
        self._create_sections()

    def _create_sections(self):
        # Limpa seções existentes
        for section in self.sections:
            section['titulo'].destroy()
            section['texto'].destroy()
            if 'imagem' in section and section['imagem'] is not None:
                section['imagem'].destroy()
        self.sections.clear()

        # Calcula tamanhos responsivos - usa largura da janela principal se disponível
        try:
            largura_janela = self.winfo_toplevel().winfo_width()
            # Subtrai a largura do menu (200px) e margens
            largura_disponivel = max(300, largura_janela - 250)
        except:
            # Fallback se não conseguir obter largura
            largura_disponivel = 500
        
        # Ajusta tamanho da fonte baseado no tamanho da janela
        if largura_disponivel < 400:
            titulo_size = 16
            texto_size = 12
            wrap_length = max(250, largura_disponivel - 60)
        elif largura_disponivel < 600:
            titulo_size = 18
            texto_size = 14
            wrap_length = max(350, largura_disponivel - 80)
        else:
            titulo_size = 20
            texto_size = 16
            wrap_length = min(650, largura_disponivel - 100)

        # Cria seções com tamanhos responsivos
        for item in self.section_data:
            # Unpacking direto para melhorar a legibilidade
            titulo, texto, imagem_path = item if len(item) == 3 else (item[0], item[1], None)
            self._add_section(titulo, texto, titulo_size, texto_size, wrap_length, imagem_path)

    def _add_section(self, titulo, texto, titulo_size, texto_size, wrap_length, imagem_path=None):
        # Título
        titulo_label = ctk.CTkLabel(self.scroll, text=titulo,
                                     font=("Arial", titulo_size, "bold"))
        titulo_label.pack(pady=(20, 5))

        # Texto
        texto_label = ctk.CTkLabel(self.scroll,
                                     text=texto,
                                     font=("Arial", texto_size),
                                     wraplength=wrap_length,
                                     justify="left")
        texto_label.pack(padx=20, pady=10)
        
        # Imagem (se fornecida)
        imagem_label = None
        if imagem_path:
            imagem_label = self._add_image(imagem_path, wrap_length)
        
        # Armazena referências
        section_dict = {
            'titulo': titulo_label,
            'texto': texto_label
        }
        if imagem_label:
            section_dict['imagem'] = imagem_label
        
        self.sections.append(section_dict)

    def _add_image(self, imagem_path, largura_maxima):
        try:
            # Verifica se o arquivo existe
            if not os.path.exists(imagem_path):
                # Se não existir, mostrar uma mensagem
                placeholder = ctk.CTkLabel(self.scroll, 
                                           text=f"[Imagem: {imagem_path} não encontrada]",
                                           font=("Arial", 12),
                                           text_color="gray")
                placeholder.pack(pady=10)
                return placeholder
            
            # Carrega e redimensiona a imagem
            imagem_pil = Image.open(imagem_path)
            
            # Calcula tamanho responsivo da imagem
            largura_img = min(largura_maxima - 40, 400)  # Máximo 400px ou largura disponível
            altura_img = int((largura_img / imagem_pil.width) * imagem_pil.height)
            
            # Redimensiona mantendo proporção
            imagem_pil = imagem_pil.resize((largura_img, altura_img), Image.Resampling.LANCZOS)
            
            # Converte para CTkImage
            ctk_image = ctk.CTkImage(light_image=imagem_pil, 
                                     dark_image=imagem_pil,
                                     size=(largura_img, altura_img))
            
            # Cria label da imagem
            imagem_label = ctk.CTkLabel(self.scroll, image=ctk_image, text="")
            imagem_label.pack(pady=10)
            
            return imagem_label
            
        except Exception as e:
            # Em caso de erro, mostrar a mensagem
            error_label = ctk.CTkLabel(self.scroll, 
                                       text=f"[Erro ao carregar: {imagem_path}]",
                                       font=("Arial", 12),
                                       text_color="red")
            error_label.pack(pady=10)
            return error_label

    def _update_responsive_layout(self):
        try:
            # Atualizar tamanho do título principal
            largura_janela = self.winfo_toplevel().winfo_width()
            largura_disponivel = largura_janela - 250  # Subtrair menu
            
            if largura_disponivel < 400:
                titulo_principal_size = 20
            elif largura_disponivel < 600:
                titulo_principal_size = 24
            else:
                titulo_principal_size = 28
                
            self.titulo_label.configure(font=("Arial", titulo_principal_size, "bold"))
            
            # Recriar seções com novos tamanhos
            self.after(50, self._create_sections)  # Pequeno delay para evitar conflitos
        except:
            # Se houver erro, usar valores padrão
            pass

# Página de gráficos com rolagem
class Pagina_graficos(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.df = carregar_dados() 

        self.canvas_widget = None
        self.fig = None

       # Configuração do grid para o frame principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0) # Linha dos títulos
        self.grid_rowconfigure(1, weight=1) # Linha do scrollable_frame

        # Cria o scrollable_frame para conter todos os controles e o gráfico
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=600, height=800)
        self.scrollable_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Configuração do grid dentro do scrollable_frame
        self.scrollable_frame.grid_columnconfigure(0, weight=1) 
        self.scrollable_frame.grid_columnconfigure(1, weight=0) # Coluna central para os widgets
        self.scrollable_frame.grid_columnconfigure(2, weight=1) 
        
        # Mantém peso alto para a linha do gráfico (onde o gráfico_frame estará)
        self.scrollable_frame.grid_rowconfigure(8, weight=10)
        # Define pesos para outras linhas (garante que não roubem espaço)
        self.scrollable_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,9), weight=0)

        # --- CONTEÚDO DENTRO DO SCROLLABLE_FRAME ---
        # Título "Gerar gráficos" no topo da página
        ctk.CTkLabel(self, text="Gerar Gráficos", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

        # Tipo de Gráfico
        ctk.CTkLabel(self.scrollable_frame, text="Escolha o tipo de gráfico:", font=("Arial", 14)).grid(row=0, column=1, pady=5)
        self.tipo_grafico = ctk.CTkOptionMenu(self.scrollable_frame, values=["Linha", "Barras", "Pizza"])
        self.tipo_grafico.set("Linha") # Definir valor padrão
        self.tipo_grafico.grid(row=1, column=1, pady=5, sticky="ew", padx=5) 

        # Frame para os anos
        self.anos_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent") 
        self.anos_frame.grid(row=3, column=1, pady=5, sticky="ew") 
        self.anos_frame.grid_columnconfigure(0, weight=1) 
        self.anos_frame.grid_columnconfigure(1, weight=1) 

        #Obtém o maior e menor ano do banco de dados
        intervalo = obter_min_max_ano()
        #Cria uma lista com esses anos
        anos_disponiveis = [str(ano) for ano in range(intervalo[0], intervalo[1] + 1)]

        ctk.CTkLabel(self.scrollable_frame, text="Escolha o intervalo temporal:", font=("Arial", 14)).grid(row=2, column=1, pady=5) 
        
        # Ano Início OptionMenu
        self.ano_inicio = ctk.CTkOptionMenu(self.anos_frame, 
                                            values= anos_disponiveis)
        self.ano_inicio.set(intervalo[0]) # Definir valor padrão
        self.ano_inicio.grid(row=0, column=0, pady=5, padx=5, sticky="ew")

        # Ano Fim OptionMenu
        self.ano_fim = ctk.CTkOptionMenu(self.anos_frame, 
                                         values= anos_disponiveis)
        self.ano_fim.set(intervalo[1]) # Definir valor padrão
        self.ano_fim.grid(row=0, column=1, pady=5, padx=5, sticky="ew") 

        # Atividades
        atividades_disponiveis = obter_atividades_economicas() # Obtém as atividades com nomes formatados
        ctk.CTkLabel(self.scrollable_frame, text="Escolha o tipo de atividade (opcional):", font=("Arial", 14)).grid(row=5, column=1, pady=5)
        self.filtro_atividades = ctk.CTkOptionMenu(self.scrollable_frame, values=atividades_disponiveis)
        self.filtro_atividades.set("Todas as Atividades") # Definir valor padrão
        self.filtro_atividades.grid(row=6, column=1, pady=5, padx=5, sticky="ew") 

        # Gases
        gases_disponiveis = obter_gases() # Obtém os gases com nomes formatados
        ctk.CTkLabel(self.scrollable_frame, text="Escolha o tipo de gás (opcional):", font=("Arial", 14)).grid(row=7, column=1, pady=5) 
        self.filtro_gases = ctk.CTkOptionMenu(self.scrollable_frame, values=gases_disponiveis)
        self.filtro_gases.set("Todos os Gases") # Definir valor padrão
        self.filtro_gases.grid(row=8, column=1, pady=5, padx=5, sticky="ew")

        # Botão Gerar Gráfico
        ctk.CTkButton(self.scrollable_frame, text="Gerar Gráfico", command=self.gerar_grafico).grid(row=9, column=1, pady=10, padx=5)

        # Frame para exibir o gráfico
        self.grafico_frame = ctk.CTkFrame(self.scrollable_frame)
        self.grafico_frame.grid(row=10, column=0, columnspan=3, padx=10, pady=10, sticky="nsew") 
        
        self.grafico_frame.grid_rowconfigure(0, weight=1) 
        self.grafico_frame.grid_columnconfigure(0, weight=1) 

        self.canvas_grafico = ctk.CTkLabel(self.grafico_frame, text="")
        self.canvas_grafico.grid(row=0, column=0, sticky="nsew") 

        # Botão Baixar Gráfico
        self.botao_download = ctk.CTkButton(self.scrollable_frame, text="Baixar gráfico", command=self.salvar_grafico)
        self.botao_download.grid(row=11, column=1, pady=(0, 20), padx=5)

    def gerar_grafico(self):
        self.canvas_grafico.configure(image=None)
        
        #Obtém as entradas do usuário
        tipo = self.tipo_grafico.get()
        filtro_atividades = self.filtro_atividades.get()
        filtro_gases = self.filtro_gases.get()

        print("filtro_gases:", filtro_gases)
        print("filtro_atividades:", filtro_atividades)

        #Obtém o mapeamento inverso dos gases - transforma os nomes formatados em abreviações do banco
        _, gas_inv = obter_mapeamento_gases()
        gas_cod = gas_inv.get(filtro_gases)
        print("Gas codificado:", gas_cod)

        #Obtém o mapeamento inverso das atividades - transforma os nomes formatados em abreviações do banco
        _, atividade_inv = obter_mapeamento_atividades()
        atividade_cod = atividade_inv.get(filtro_atividades)
        print("Atividade codificada:", atividade_cod)

        #Função para transformar os anos em inteiros
        def parse_ano(valor):
            if not valor:  #Trata None, "" ou strings com espaços
                return None
            try:
                return int(valor.strip())
            except Exception:
                return None
            
        intervalo = obter_min_max_ano()

        ano_inicio_int = parse_ano(self.ano_inicio.get())
        ano_fim_int = parse_ano(self.ano_fim.get())

        #Se não tiver ano_inicio nem ano_fim, puxa os valores do banco
        if not ano_inicio_int or ano_inicio_int is None:
            ano_inicio_int = intervalo[0]
        if not ano_fim_int or ano_fim_int is None:
            ano_fim_int = intervalo[1]

        #Cria uma cópia do dataframe original
        df_filtrado = self.df.copy()

        try:
            #Se os anos não estiverem vazios, filtra o dataframe
            if ano_inicio_int is not None and ano_fim_int is not None:
                df_filtrado = df_filtrado[(df_filtrado['ano'] >= ano_inicio_int) & (df_filtrado['ano'] <= ano_fim_int)]

            #Se o filtro de atividades foi aplicado, filtra o dataframe
            if filtro_atividades != "Todas as Atividades":
                _, atividade_inv = obter_mapeamento_atividades()
                atividade_cod = atividade_inv.get(filtro_atividades.strip())
                if atividade_cod:
                    df_filtrado = df_filtrado[df_filtrado["atividade_economica"] == atividade_cod]
                else:
                    print(f"Atividade '{filtro_atividades}' não encontrada no mapeamento!")

            #Se o filtro de gases foi aplicado, filtra o dataframe
            if filtro_gases != "Todos os Gases":
                _, gas_inv = obter_mapeamento_gases()
                gas_cod = gas_inv.get(filtro_gases.strip())
                if gas_cod:
                    df_filtrado = df_filtrado[df_filtrado["gas"] == gas_cod]
                else:
                    print(f"Gás '{filtro_gases}' não encontrado no mapeamento!")
            
            print(f"{ano_inicio_int} - {ano_fim_int}")
            print(df_filtrado["gas"].unique())
            print(df_filtrado["atividade_economica"].unique())

            if tipo == "Linha":
                fig = grafico_linha(df_filtrado, filtro_gases, ano_inicio_int, ano_fim_int, filtro_atividades)

            elif tipo == "Barras":
                fig = grafico_barras(df_filtrado, filtro_gases, ano_inicio_int, ano_fim_int, filtro_atividades)

            elif tipo == "Pizza":
                fig = grafico_pizza(df_filtrado, filtro_gases, ano_inicio_int, ano_fim_int, filtro_atividades)

            self.fig = fig
            
            # Força o Tkinter a calcular o layout para obter as dimensões mais precisas
            self.update_idletasks() # Atualiza a Pagina_graficos
            self.scrollable_frame.update_idletasks() # Atualiza o frame rolável
            self.grafico_frame.update_idletasks() # Atualiza o frame do gráfico
            self.canvas_grafico.update_idletasks() # Atualiza o label do canvas

            target_width = 700
            target_height = 400

            plotly_render_width = target_width + 100
            plotly_render_height = target_height + 120

            #Proporções mínimas
            if plotly_render_width < 300: plotly_render_width = 300
            if plotly_render_height < 200: plotly_render_height = 200

            img_bytes = pio.to_image(fig, format='png', width=plotly_render_width, height=plotly_render_height, scale=1)
            image = Image.open(io.BytesIO(img_bytes))

            # Calcula proporção e redimensiona
            img_ratio = image.width / image.height
            container_ratio = target_width / target_height

            if img_ratio > container_ratio:
                final_height = int(target_width / img_ratio)
                final_width = target_width
            else:
                final_width = int(target_height * img_ratio)
                final_height = target_height

            image = image.resize((final_width, final_height), Image.Resampling.LANCZOS)

            # Limpa imagem anterior
            self.canvas_grafico.configure(image=None)

            # Atualiza imagem
            self.imagem_tk = CTkImage(light_image=image, size=(final_width, final_height)) 
            self.canvas_grafico.configure(image=self.imagem_tk, text="") 
            self.canvas_grafico.image = self.imagem_tk 

        except Exception as e:
            print(f"Erro ao gerar gráfico: {e}")
            self.label_erro_grafico.configure(text=f"Erro ao gerar gráfico: {e}")


    def salvar_grafico(self):
        if self.fig is None:
            print("Nenhum gráfico gerado para salvar.")
            return

        caminho = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            self.fig.write_image(caminho)  # usando plotly para salvar

class EditarUsuarioDialog(ctk.CTkToplevel):
    def __init__(self, parent, id_usuario, nome_atual, callback_atualizar_lista, callback_status_label):
        super().__init__(parent)

        # Tentativa de carregar e definir o ícone da janela
        try:
            icon_image = Image.open("imagens/efeito_estufa_icone.png")
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.iconphoto(False, icon_photo)
            self._icon_image_ref = icon_photo  # Referência salva para não ser coletada pelo garbage collector
        except Exception as e:
            print("Erro ao carregar ícone:", e)

        # Define o comportamento modal (bloqueia outras janelas até fechar)
        self.grab_set()
        # Fecha junto com a janela principal
        self.transient(parent)
        # Define o título da janela com o nome do usuário sendo editado
        self.title(f"Editar Usuário: {nome_atual}")

        # Armazena os dados e callbacks recebidos como parâmetros
        self.id_usuario = id_usuario
        self.callback_atualizar_lista = callback_atualizar_lista
        self.callback_status_label = callback_status_label

        # Configuração do layout
        self.grid_columnconfigure(1, weight=1)  # A segunda coluna pode se expandir
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)  # Linhas fixas

        # Título na parte superior da janela
        ctk.CTkLabel(self, text=f"Editando usuário ID: {id_usuario}", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

        # Campo para editar o nome de usuário
        ctk.CTkLabel(self, text="Novo Nome:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entrada_novo_usuario = ctk.CTkEntry(self, placeholder_text="Novo nome de usuário")
        self.entrada_novo_usuario.insert(0, nome_atual)  # Preenche com o nome atual
        self.entrada_novo_usuario.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Campo para definir nova senha
        ctk.CTkLabel(self, text="Nova Senha:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entrada_nova_senha = ctk.CTkEntry(self, placeholder_text="Nova senha", show="*")
        self.entrada_nova_senha.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Frame para os botões
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        # Botão para salvar as alterações
        ctk.CTkButton(btn_frame, text="Salvar Alterações", command=self._salvar_edicao,
                      font=("Arial", 16, "bold"), fg_color="#007bff", hover_color="#0056b3").pack(side="left", padx=10)

        # Botão para cancelar e fechar a janela
        ctk.CTkButton(btn_frame, text="Cancelar", command=self.destroy,
                      font=("Arial", 16, "bold"), fg_color="gray", hover_color="darkgray").pack(side="right", padx=10)

        # Centraliza a janela em relação à janela principal
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() / 2) - (self.winfo_width() / 2)
        y = parent.winfo_y() + (parent.winfo_height() / 2) - (self.winfo_height() / 2)
        self.geometry(f"+{int(x)}+{int(y)}")

    # Função chamada ao clicar em "Salvar Alterações"
    def _salvar_edicao(self):
        novo_nome = self.entrada_novo_usuario.get().strip()
        nova_senha = self.entrada_nova_senha.get().strip()

        # Verifica se os campos foram preenchidos
        if not novo_nome or not nova_senha:
            CTkMessagebox(title="Erro de Validação", message="Por favor, preencha o nome de usuário e a senha.", icon="warning")
            return

        try:
            # Atualiza os dados do usuário no banco de dados
            atualizar_usuario(self.id_usuario, novo_nome, nova_senha)

            # Atualiza a lista na janela principal e mostra mensagem de sucesso
            self.callback_atualizar_lista()
            self.callback_status_label(f"Usuário '{novo_nome}' atualizado com sucesso!", "green")
            self.destroy()  # Fecha a janela de edição
        except ValueError as e:
            # Mostra mensagem de erro se houver problema conhecido (ex: nome já existe)
            CTkMessagebox(title="Erro", message=str(e), icon="cancel")
        except Exception as e:
            # Mostra erro genérico caso ocorra algo inesperado
            CTkMessagebox(title="Erro Inesperado", message=f"Ocorreu um erro ao atualizar: {e}", icon="cancel")

# Página de gerenciamento de usuários
class Pagina_usuarios(ctk.CTkFrame):
    def __init__(self, parent, editar_callback):
        super().__init__(parent)
        self.editar_callback = editar_callback  # Função chamada ao clicar em "Editar"
        
        # Configura layout para ocupar todo o espaço disponível
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Frame com rolagem para conter todo o conteúdo da página
        self.scroll_geral = ctk.CTkScrollableFrame(self)
        self.scroll_geral.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scroll_geral.grid_columnconfigure(0, weight=1)

        # Título da seção de gerenciamento
        ctk.CTkLabel(self.scroll_geral, text="Gerenciamento de Usuários", font=("Arial", 24, "bold")).pack(pady=20)

        # Área que lista os usuários cadastrados com rolagem separada
        self.lista_scroll = ctk.CTkScrollableFrame(self.scroll_geral, height=250, corner_radius=10, fg_color="gray20")
        self.lista_scroll.pack(pady=10, fill="x", expand=False, padx=20)

        # Campos de entrada para adicionar novo usuário
        input_frame = ctk.CTkFrame(self.scroll_geral)
        input_frame.pack(pady=10, fill="x", padx=20)
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=3)

        # Campo: nome do usuário
        ctk.CTkLabel(input_frame, text="Novo Usuário:", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.usuario = ctk.CTkEntry(input_frame, placeholder_text="Nome de usuário")
        self.usuario.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Campo: senha do usuário
        ctk.CTkLabel(input_frame, text="Senha:", font=("Arial", 14)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.senha = ctk.CTkEntry(input_frame, placeholder_text="Senha", show="*")
        self.senha.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Mensagem de status (sucesso/erro)
        self.mensagem_label = ctk.CTkLabel(self.scroll_geral, text="", font=("Arial", 12))
        self.mensagem_label.pack()

        # Botão para adicionar novo usuário
        ctk.CTkButton(self.scroll_geral, text="Adicionar Usuário", command=self.adicionar,
                      font=("Arial", 16, "bold"), fg_color="#28a745", hover_color="#218838").pack(pady=15)

        # Chamada inicial para preencher a lista de usuários
        self.atualizar_lista()

    # Atualiza a mensagem de status com texto e cor
    def _atualizar_status_label(self, message, color="white"):
        self.mensagem_label.configure(text=message, text_color=color)

    # Atualiza visualmente a lista de usuários
    def atualizar_lista(self):
        # Remove todos os widgets antigos da lista
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()

        usuarios = listar_usuarios()  # Busca os usuários do banco
        if not usuarios:
            ctk.CTkLabel(self.lista_scroll, text="Nenhum usuário cadastrado.", font=("Arial", 14), text_color="gray").pack(pady=20)
            return

        # Para cada usuário, cria uma linha com dados e botões de ação
        for id_usuario, usuario in usuarios:
            linha = ctk.CTkFrame(self.lista_scroll, fg_color="gray25", corner_radius=8)
            linha.pack(fill="x", pady=4, padx=8)
            linha.grid_columnconfigure(0, weight=1)

            # Exibe ID e nome do usuário
            ctk.CTkLabel(linha, text=f"ID: {id_usuario} | Usuário: {usuario}", anchor="w", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5, sticky="ew")

            # Frame com botões "Editar" e "Excluir"
            btn_frame = ctk.CTkFrame(linha, fg_color="transparent")
            btn_frame.grid(row=0, column=1, padx=5, pady=5, sticky="e")

            # Botão para editar, usando o callback passado no construtor
            ctk.CTkButton(btn_frame, text="Editar", font=("Arial", 12, "bold"), fg_color="#007bff", hover_color="#0056b3",
                          command=lambda id=id_usuario, nome=usuario: self.editar_callback(id, nome, self.atualizar_lista)).pack(side="left", padx=3)

            # Botão para excluir usuário
            ctk.CTkButton(btn_frame, text="Excluir", font=("Arial", 12, "bold"), fg_color="red", hover_color="darkred",
                          command=lambda id=id_usuario: self.excluir(id)).pack(side="left", padx=3)

    # Lógica para adicionar novo usuário ao sistema
    def adicionar(self):
        usuario = self.usuario.get().strip()
        senha = self.senha.get().strip()

        if usuario and senha:
            try:
                adicionar_usuario(usuario, senha)  # Função externa para adicionar ao banco
                self.atualizar_lista()  # Atualiza a lista de usuários na tela
                self.usuario.delete(0, "end")
                self.senha.delete(0, "end")
                self._atualizar_status_label("Usuário adicionado com sucesso!", "green")
            except ValueError as e:
                self._atualizar_status_label(str(e), "red")  # Erro conhecido (ex: usuário já existe)
            except Exception as e:
                self._atualizar_status_label(f"Erro ao adicionar: {e}", "red")  # Erro inesperado
        else:
            self._atualizar_status_label("Por favor, preencha todos os campos.", "red")

    # Lógica para excluir um usuário com confirmação
    def excluir(self, id_usuario):
        msg = CTkMessagebox(title="Confirmação de Exclusão", message=f"Tem certeza que deseja excluir o usuário ID {id_usuario}?",
                            icon="question", option_1="Não", option_2="Sim")
        response = msg.get()
        if response == "Sim":
            deletar_usuario(id_usuario)  # Função externa que remove o usuário do banco
            self.atualizar_lista()
            self._atualizar_status_label(f"Usuário ID {id_usuario} excluído com sucesso!", "green")

class Pagina_bd(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configurações iniciais do frame principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Frame rolável principal
        self.scroll_geral = ctk.CTkScrollableFrame(self)
        self.scroll_geral.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scroll_geral.grid_columnconfigure(0, weight=1)

        # Título da página
        ctk.CTkLabel(self.scroll_geral, text="Emissões de Gases do Efeito Estufa", font=("Arial", 24, "bold")).pack(pady=20)

        # Frame de entradas de dados
        input_frame = ctk.CTkFrame(self.scroll_geral)
        input_frame.pack(pady=10, fill="x", padx=20)
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=3)

        # Criação dinâmica dos campos de entrada
        self.entradas = {}
        campos = ["Ano", "Gás", "Atividade Econômica", "Emissão (toneladas)"]
        for i, campo in enumerate(campos):
            label = ctk.CTkLabel(input_frame, text=f"{campo}:", font=("Arial", 14))
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entrada = ctk.CTkEntry(input_frame, placeholder_text=campo)
            entrada.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entradas[campo] = entrada

        # Botão para adicionar emissão
        ctk.CTkButton(self.scroll_geral, text="Adicionar Emissão", command=self.adicionar_emissao,
                      font=("Arial", 16, "bold"), fg_color="#28a745", hover_color="#218838").pack(pady=15)

        # Label de status para mensagens de erro ou sucesso
        self.status_label = ctk.CTkLabel(self.scroll_geral, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        # Título da lista de registros
        ctk.CTkLabel(self.scroll_geral, text="Últimas 50 Emissões", font=("Arial", 18, "bold")).pack(pady=10)

        # Frame rolável com os dados
        self.lista_scroll = ctk.CTkScrollableFrame(self.scroll_geral, height=300, corner_radius=10, fg_color="gray20")
        self.lista_scroll.pack(pady=10, fill="x", expand=True, padx=20)

        # Carrega os dados iniciais
        self.atualizar_lista()

    # Limpa os campos de entrada
    def _limpar_entradas(self):
        for entrada in self.entradas.values():
            entrada.delete(0, ctk.END)

    # Atualiza o status da operação
    def _atualizar_status_label(self, message, color="white"):
        self.status_label.configure(text=message, text_color=color)

    # Verifica se os campos "Ano" e "Emissão" são numéricos
    def _validar_entradas(self, ano, emissao):
        try:
            int(ano)
        except ValueError:
            self.status_label.configure(text="Erro: O 'Ano' deve ser um número inteiro.", text_color="red")
            return False
        try:
            float(emissao)
        except ValueError:
            self.status_label.configure(text="Erro: A 'Emissão' deve ser um número.", text_color="red")
            return False
        return True

    # Adiciona nova entrada ao banco de dados
    def adicionar_emissao(self):
        ano = self.entradas["Ano"].get()
        gas = self.entradas["Gás"].get()
        atividade = self.entradas["Atividade Econômica"].get()
        emissao = self.entradas["Emissão (toneladas)"].get()

        # Verifica se todos os campos foram preenchidos
        if not all([ano, gas, atividade, emissao]):
            self._atualizar_status_label("Erro: Todos os campos são obrigatórios.", "red")
            return

        # Validação e inserção no banco
        if self._validar_entradas(ano, emissao):
            adicionar_bd(ano, gas, atividade, float(emissao))
            self._limpar_entradas()
            self._atualizar_status_label("Emissão adicionada com sucesso!", "green")
            atualizar_id_com_rowid("efeito_estufa.db", "emissoes")
            self.atualizar_lista()

    # Atualiza a lista exibida
    def atualizar_lista(self):
        # Limpa os widgets existentes
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()

        # Recarrega os dados do banco
        emissao_dados = listar_bd()
        atualizar_id_com_rowid("efeito_estufa.db", "emissoes")

        if not emissao_dados:
            ctk.CTkLabel(self.lista_scroll, text="Nenhum registro encontrado.", font=("Arial", 14), text_color="gray").pack(pady=20)
            return

        # Gera interface com dados
        for id_emissao, ano, gas, atividade, emissao in emissao_dados:
            linha = ctk.CTkFrame(self.lista_scroll, fg_color="gray25", corner_radius=8)
            linha.pack(fill="x", pady=4, padx=8)
            linha.grid_columnconfigure(0, weight=1)

            texto = f"Ano: {ano} | Gás: {gas} | Atividade: {atividade} | Emissão: {emissao} toneladas"
            ctk.CTkLabel(linha, text=texto, anchor="w", wraplength=450, font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5, sticky="ew")

            btn_frame = ctk.CTkFrame(linha, fg_color="transparent")
            btn_frame.grid(row=0, column=1, padx=5, pady=5, sticky="e")

            # Botões de ação
            ctk.CTkButton(btn_frame, text="Editar", font=("Arial", 12, "bold"), fg_color="#007bff", hover_color="#0056b3",
                          command=lambda i=id_emissao, a=ano, g=gas, act=atividade, e=emissao: self.editar_emissao_dialog(i, a, g, act, e)).pack(side="left", padx=3)

            ctk.CTkButton(btn_frame, text="Excluir", font=("Arial", 12, "bold"), fg_color="red", hover_color="darkred",
                          command=lambda i=id_emissao: self.excluir_emissao(i)).pack(side="left", padx=3)

    # Exclui um registro após confirmação
    def excluir_emissao(self, id_emissao):
        msg = CTkMessagebox(title="Confirmação de Exclusão", message=f"Tem certeza que deseja excluir a emissão ID {id_emissao}?",
                            icon="question", option_1="Não", option_2="Sim")
        response = msg.get()
        if response == "Sim":
            deletar_bd(id_emissao)
            self.atualizar_lista()
            self._atualizar_status_label(f"Emissão ID {id_emissao} excluída com sucesso!", "green")

    # Abre janela de edição de registro
    def editar_emissao_dialog(self, id_emissao, ano, gas, atividade, emissao):
        dialog = EditarEmissaoDialog(
            self.master, id_emissao, ano, gas, atividade, emissao,
            self.atualizar_lista, self._atualizar_status_label
        )
        self.wait_window(dialog)

# Define uma janela secundária (popup) para editar os dados de uma emissão já existente
class EditarEmissaoDialog(ctk.CTkToplevel):
    def __init__(self, parent, id_emissao, ano, gas, atividade, emissao, callback_atualizar_lista, callback_status_label):
        super().__init__(parent)  # Inicializa a janela toplevel com o parent (janela principal)

        # Tentativa de carregar e definir um ícone para a janela
        try:
            icon_image = Image.open("imagens/efeito_estufa_icone.png")
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.iconphoto(False, icon_photo)  # Define o ícone da janela
            self._icon_image_ref = icon_photo  # Mantém referência para não ser coletado pelo garbage collector
        except Exception as e:
            print("Erro ao carregar ícone:", e)  # Exibe erro se o ícone não puder ser carregado
            
        self.grab_set()  # Impede interação com a janela principal enquanto essa estiver aberta
        self.transient(parent)  # Faz com que essa janela seja fechada junto com a principal
        self.title(f"Editar Emissão ID: {id_emissao}")  # Define título da janela

        # Armazena informações e funções para uso posterior
        self.id_emissao = id_emissao
        self.callback_atualizar_lista = callback_atualizar_lista
        self.callback_status_label = callback_status_label

        # Configurações do layout de grade
        self.grid_columnconfigure(1, weight=1)  # Segunda coluna pode expandir
        self.grid_rowconfigure((0,1,2,3,4,5), weight=0)  # Linhas fixas (sem expansão)

        # Título da janela
        ctk.CTkLabel(self, text=f"Editando Emissão ID: {id_emissao}", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

        # Campos do formulário com seus respectivos valores iniciais
        self.entradas = {}  # Dicionário para guardar os widgets de entrada
        campos = {"Ano": ano, "Gás": gas, "Atividade Econômica": atividade, "Emissão (toneladas)": emissao}

        # Loop para criar os campos de entrada (labels + entries)
        for i, (campo, valor) in enumerate(campos.items()):
            ctk.CTkLabel(self, text=f"{campo}:", font=("Arial", 14)).grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
            entrada = ctk.CTkEntry(self, placeholder_text=campo)
            entrada.insert(0, str(valor))  # Pré-preenche o campo com o valor atual
            entrada.grid(row=i+1, column=1, padx=10, pady=5, sticky="ew")
            self.entradas[campo] = entrada  # Armazena o widget de entrada para uso posterior

        # Frame para os botões (Salvar e Cancelar)
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=len(campos) + 1, column=0, columnspan=2, pady=20)

        # Botão de salvar alterações
        ctk.CTkButton(btn_frame, text="Salvar Alterações", command=self._salvar_edicao,
                      font=("Arial", 16, "bold"), fg_color="#007bff", hover_color="#0056b3").pack(side="left", padx=10)

        # Botão de cancelar (fecha a janela)
        ctk.CTkButton(btn_frame, text="Cancelar", command=self.destroy,
                      font=("Arial", 16, "bold"), fg_color="gray", hover_color="darkgray").pack(side="right", padx=10)

        # Centraliza a janela em relação à janela principal
        self.update_idletasks()  # Atualiza layout antes de posicionar
        x = parent.winfo_x() + (parent.winfo_width() / 2) - (self.winfo_width() / 2)
        y = parent.winfo_y() + (parent.winfo_height() / 2) - (self.winfo_height() / 2)
        self.geometry(f"+{int(x)}+{int(y)}")  # Posiciona a janela no centro da principal

    # Valida se os campos "ano" e "emissão" têm valores numéricos corretos
    def _validar_entradas(self, ano, emissao):
        try:
            int(ano)  # Verifica se o ano é inteiro
        except ValueError:
            CTkMessagebox(title="Erro de Validação", message="Erro: O 'Ano' deve ser um número inteiro.", icon="warning")
            return False
        try:
            float(emissao)  # Verifica se a emissão é um número (int ou float)
        except ValueError:
            CTkMessagebox(title="Erro de Validação", message="Erro: A 'Emissão' deve ser um número.", icon="warning")
            return False
        return True  # Entradas válidas

    # Lógica para salvar as edições feitas pelo usuário
    def _salvar_edicao(self):
        # Captura os dados inseridos nos campos
        novo_ano = self.entradas["Ano"].get()
        novo_gas = self.entradas["Gás"].get()
        nova_atividade = self.entradas["Atividade Econômica"].get()
        nova_emissao = self.entradas["Emissão (toneladas)"].get()

        # Verifica se todos os campos foram preenchidos
        if not all([novo_ano, novo_gas, nova_atividade, nova_emissao]):
            CTkMessagebox(title="Erro de Validação", message="Todos os campos são obrigatórios.", icon="warning")
            return

        # Se os dados forem válidos, atualiza o banco
        if self._validar_entradas(novo_ano, nova_emissao):
            atualizar_bd(self.id_emissao, novo_ano, novo_gas, nova_atividade, float(nova_emissao))  # Atualiza no BD
            self.callback_atualizar_lista()  # Atualiza a lista na interface principal
            self.callback_status_label(f"Emissão ID {self.id_emissao} atualizada com sucesso!", "green")  # Mensagem de sucesso
            self.destroy()  # Fecha a janela de edição

# Inicializa a aplicação
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = App()
    app.mainloop()
