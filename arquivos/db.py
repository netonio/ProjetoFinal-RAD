import sqlite3

def criar_tabela():
    con = sqlite3.connect("usuarios.db")
    cursor = con.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   usuario TEXT UNIQUE NOT NULL,
                   senha TEXT NOT NULL
                   )
        ''')
    
    con.commit()
    con.close()

def adicionar_usuario(usuario, senha):
    con = sqlite3.connect("usuarios.db")
    cursor = con.cursor()
    
    cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))

    con.commit()
    con.close()

def buscar_usuario_senha(usuario, senha):
    con = sqlite3.connect("usuarios.db")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
    user = cursor.fetchone()

    con.close()
    return user

def buscar_usuario(usuario):
    con = sqlite3.connect("usuarios.db")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()

    con.close()
    return resultado

def listar_usuarios():
    con = sqlite3.connect("usuarios.db")
    cursor = con.cursor()

    cursor.execute("SELECT id, usuario, senha FROM usuarios")
    usuarios = cursor.fetchall()

    con.close()
    return usuarios

def deletar_usuario(id_usuario):
    con = sqlite3.connect("usuarios.db")
    cursor = con.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))

    con.commit()
    con.close()