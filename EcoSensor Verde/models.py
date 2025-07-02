import sqlite3

def conectar():
    return sqlite3.connect("database/ecosensor.db")

def cadastrar_usuario(nome, email, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
    conn.commit()
    conn.close()

def cadastrar_terreno(nome, localizacao, usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO terrenos (nome, localizacao, usuario_id) VALUES (?, ?, ?)', (nome, localizacao, usuario_id))
    conn.commit()
    conn.close()

def registrar_medicao(terreno_id, temperatura, umidade, luminosidade, ph):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO medicoes (terreno_id, temperatura, umidade, luminosidade, ph)
        VALUES (?, ?, ?, ?, ?)
    ''', (terreno_id, temperatura, umidade, luminosidade, ph))
    conn.commit()
    conn.close()
