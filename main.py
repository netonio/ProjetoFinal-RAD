import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from db import *
from graficos import *

# Cria a tabela se não existir
criar_tabela()

# Classe principal da aplicação
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("950x500")
        self.title("Estufatos")

        # Inicia com a tela de login
        self.login_frame = Tela_login(self, self.entrar)
        self.login_frame.pack(fill="both", expand=True)

    # Faz login e muda para a interface principal
    def entrar(self, usuario, senha):
        user = buscar_usuario_senha(usuario, senha)
        if user:
            self.login_frame.destroy()
            self.menu_principal()
            self.abrir_inicio()
        else:
            self.login_frame.mensagem("Usuário ou senha incorretos")

    # Monta menu lateral fixo
    def menu_principal(self):
        self.menu = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu.pack(side="left", fill="y")

        ctk.CTkLabel(self.menu, text="Menu", font=("Arial", 20)).pack(pady=20)
        ctk.CTkButton(self.menu, text="Início", command=self.abrir_inicio).pack()
        ctk.CTkButton(self.menu, text="Gráficos", command=self.abrir_graficos).pack()
        ctk.CTkButton(self.menu, text="Usuários", command=self.abrir_usuarios).pack()

        # Container para carregar páginas
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="left", fill='both', expand=True)

    # Métodos para troca de página
    def abrir_inicio(self):
        self._abrir_pagina(Pagina_inicio)

    def abrir_graficos(self):
        self._abrir_pagina(Pagina_graficos)

    def abrir_usuarios(self):
        self._abrir_pagina(Pagina_usuarios)

    def _abrir_pagina(self, Pagina):
        # Limpa página anterior
        for widget in self.container.winfo_children():
            widget.destroy()
        Pagina(self.container).pack(fill="both", expand=True)

    # Volta à tela de login
    def mostrar_login(self):
        if hasattr(self, "cadastro_frame"):
            self.cadastro_frame.destroy()
        self.login_frame = Tela_login(self, self.entrar)
        self.login_frame.pack(fill="both", expand=True)

    # Mostra tela de cadastro
    def mostrar_cadastro(self):
        self.login_frame.destroy()
        self.cadastro_frame = Tela_cadastro(self, self.mostrar_login)
        self.cadastro_frame.pack(fill="both", expand=True)

# Tela de login
class Tela_login(ctk.CTkFrame):
    def __init__(self, parent, entrar_callback):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Login", font=("Arial", 24)).pack(pady=30)

        self.entrada_usuario = ctk.CTkEntry(self, placeholder_text="Digite seu usuário")
        self.entrada_usuario.pack(pady=10)

        self.entrada_senha = ctk.CTkEntry(self, placeholder_text="Digite sua senha", show="*")
        self.entrada_senha.pack(pady=10)

        ctk.CTkButton(self, text="Entrar", command=self.login).pack(pady=20)

        self.label_erro = ctk.CTkLabel(self, text="", text_color="red")
        self.label_erro.pack()

        self.entrar_callback = entrar_callback

        ctk.CTkLabel(self, text="Ainda não possui conta?", font=("Arial", 20)).pack(pady="10")
        ctk.CTkButton(self, text="Criar Conta", command=lambda: self._get_app().mostrar_cadastro()).pack(pady=20)

    def login(self):
        usuario = self.entrada_usuario.get()
        senha = self.entrada_senha.get()
        self.entrar_callback(usuario, senha)

    def mensagem(self, texto):
        self.label_erro.configure(text=texto)

    def _get_app(self):
        parent = self.master
        while parent and not isinstance(parent, App):
            parent = parent.master
        return parent

# Tela de cadastro
class Tela_cadastro(ctk.CTkFrame):
    def __init__(self, parent, voltar_callback):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Criar Conta", font=("Arial", 24)).pack(pady=40)

        self.usuario = ctk.CTkEntry(self, placeholder_text="Digite um nome de usuário")
        self.usuario.pack(pady=10)

        self.senha = ctk.CTkEntry(self, placeholder_text="Digite uma senha", show="*")
        self.senha.pack(pady=10)

        self.label_erro = ctk.CTkLabel(self, text="", text_color="red")
        self.label_erro.pack()

        ctk.CTkButton(self, text="Cadastrar", command=self.cadastrar).pack(pady=10)

        self.voltar_callback = voltar_callback
        ctk.CTkButton(self, text="Voltar", command=self.voltar_callback).pack(pady=5)

    def cadastrar(self):
        usuario = self.usuario.get().strip()
        senha = self.senha.get().strip()
        if usuario and senha:
            if buscar_usuario(usuario):  # Corrigido: usa coluna correta do banco
                self.label_erro.configure(text="Usuário já existe!", text_color="red")
            else:
                try:
                    adicionar_usuario(usuario, senha)
                    self.usuario.delete(0, "end")
                    self.senha.delete(0, "end")
                    self.label_erro.configure(text="Usuário adicionado!", text_color="green")

                    app = self._get_app()
                    app.cadastro_frame.destroy()
                    app.menu_principal()
                    app.abrir_inicio()
                except Exception as e:
                    self.label_erro.configure(text=f"Erro: {e}", text_color="red")
        else:
            self.label_erro.configure(text="Preencha todos os campos", text_color="red")

    def _get_app(self):
        parent = self.master
        while parent and not isinstance(parent, App):
            parent = parent.master
        return parent

# Página inicial com rolagem
class Pagina_inicio(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Início", font=("Arial", 20)).pack(pady=10)
        scroll = ctk.CTkScrollableFrame(self)
        scroll.pack(expand=True, fill="both", pady=10)
        for i in range(30):
            ctk.CTkLabel(scroll, text=f"Conteúdo exemplo {i+1}").pack(pady=2)

# Página de gráficos com rolagem
class Pagina_graficos(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.df = carregar_dados()  # Carrega os dados uma vez
        self.canvas_widget = None   # Para limpar o gráfico anterior

        ctk.CTkLabel(self, text="Gerar gráficos", font=("Arial", 20)).pack(pady=10)

        # Seleção do tipo de gráfico
        self.tipo_grafico = ctk.CTkOptionMenu(self, values=["Linha (Ano)", "Barras (Gás/Atividade)", "Pizza (Atividade)"])
        self.tipo_grafico.pack(pady=5)

        # Entrada para ano ou intervalo
        self.ano_inicio = ctk.CTkEntry(self, placeholder_text="Ano início (opcional)")
        self.ano_inicio.pack(pady=5)
        self.ano_fim = ctk.CTkEntry(self, placeholder_text="Ano fim (opcional)")
        self.ano_fim.pack(pady=5)

        # Filtro por gás ou atividade
        self.filtro = ctk.CTkEntry(self, placeholder_text="Filtro (gás ou atividade)")
        self.filtro.pack(pady=5)

        # Botão para gerar gráfico
        ctk.CTkButton(self, text="Gerar Gráfico", command=self.gerar_grafico).pack(pady=10)

        # Frame para o gráfico
        self.grafico_frame = ctk.CTkFrame(self)
        self.grafico_frame.pack(expand=True, padx=10, pady=10)

    def gerar_grafico(self):
        # Limpa o gráfico anterior, se houver
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()

        tipo = self.tipo_grafico.get()
        filtro = self.filtro.get().strip() or None

        try:
            ano_ini = int(self.ano_inicio.get()) if self.ano_inicio.get().strip() else None
            ano_fim = int(self.ano_fim.get()) if self.ano_fim.get().strip() else None
        except ValueError:
            ano_ini = ano_fim = None

        fig, ax = plt.subplots(figsize=(7, 4))

        try:
            if tipo == "Linha (Ano)":
                df_filtrado = self.df.copy()
                if filtro:
                    df_filtrado = df_filtrado[df_filtrado['gas'] == filtro]
                if ano_ini and ano_fim:
                    df_filtrado = df_filtrado[(df_filtrado['ano'] >= ano_ini) & (df_filtrado['ano'] <= ano_fim)]
                dados = df_filtrado.groupby("ano")["emissao"].sum()
                dados.plot(kind="line", ax=ax)
                ax.set_title("Emissões por Ano")
                ax.set_ylabel("Emissões")
                ax.grid(True)

            elif tipo == "Barras (Gás/Atividade)":
                df_filtrado = self.df.copy()
                if ano_ini:
                    df_filtrado = df_filtrado[df_filtrado["ano"] == ano_ini]
                categoria = "atividade_economica" if filtro and filtro.lower() in df_filtrado["atividade_economica"].unique() else "gas"
                dados = df_filtrado.groupby(categoria)["emissao"].sum()
                dados = dados[dados > 0]
                dados.plot(kind="bar", ax=ax)
                ax.set_title(f"Emissões por {categoria.replace('_',' ').capitalize()}")
                ax.set_ylabel("Emissões")
                plt.setp(ax.get_xticklabels(), rotation=45)

            elif tipo == "Pizza (Atividade)":
                df_filtrado = self.df.copy()
                if ano_ini:
                    df_filtrado = df_filtrado[df_filtrado["ano"] == ano_ini]
                dados = df_filtrado.groupby("atividade_economica")["emissao"].sum()
                dados = dados[dados > 0]
                ax.pie(dados.values, labels=dados.index, autopct='%1.1f%%', startangle=90)
                ax.set_title(f"Emissões por Atividade Econômica - {ano_ini or 'Todos os anos'}")
                ax.axis("equal")

            # Renderiza o gráfico no tkinter
            self.canvas_widget = FigureCanvasTkAgg(fig, master=self.grafico_frame)
            self.canvas_widget.draw()
            self.canvas_widget.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            print("Erro ao gerar gráfico:", e)


# Página de gerenciamento de usuários
class Pagina_usuarios(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        ctk.CTkLabel(self, text="Usuários", font=("Arial", 20)).pack(pady=10)

        # Área de rolagem para lista de usuários
        self.lista_scroll = ctk.CTkScrollableFrame(self, height=200)
        self.lista_scroll.pack(pady=10, fill="both", expand=False)

        self.usuario = ctk.CTkEntry(self, placeholder_text="Novo usuário")
        self.usuario.pack(pady=5)

        self.senha = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.senha.pack(pady=5)

        self.mensagem_label = ctk.CTkLabel(self, text="", text_color="red")
        self.mensagem_label.pack()

        ctk.CTkButton(self, text="Adicionar Usuário", command=self.adicionar).pack(pady=10)

        self.atualizar_lista()

    def atualizar_lista(self):
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()
        for id_usuario, usuario, *_ in listar_usuarios():
            linha = ctk.CTkFrame(self.lista_scroll)
            linha.pack(fill="x", pady=2, padx=10)
            ctk.CTkLabel(linha, text=f"{usuario}", anchor="w").pack(side="left", expand=True)
            ctk.CTkButton(linha, text="Excluir", fg_color="red", hover_color="darkred",
                          command=lambda id=id_usuario: self.excluir(id)).pack(side="right", padx=10)

    def adicionar(self):
        usuario = self.usuario.get().strip()
        senha = self.senha.get().strip()
        if usuario and senha:
            if buscar_usuario(usuario):  # Corrigido: usa coluna correta
                self.mensagem_label.configure(text="Usuário já existe!", text_color="red")
            else:
                try:
                    adicionar_usuario(usuario, senha)
                    self.atualizar_lista()
                    self.usuario.delete(0, "end")
                    self.senha.delete(0, "end")
                    self.mensagem_label.configure(text="Usuário adicionado!", text_color="green")
                except Exception as e:
                    self.mensagem_label.configure(text=f"Erro: {e}", text_color="red")
        else:
            self.mensagem_label.configure(text="Preencha todos os campos", text_color="red")

    def excluir(self, id_usuario):
        deletar_usuario(id_usuario)
        self.atualizar_lista()

# Inicializa a aplicação
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = App()
    app.mainloop()