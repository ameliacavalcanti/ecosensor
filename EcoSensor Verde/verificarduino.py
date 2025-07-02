import serial
import time
import sqlite3
import os
from datetime import datetime

# === CONFIGURAÇÕES ===
porta = 'COM4'  # Altere se necessário
baud_rate = 9600
tempo_salvamento = 10  # segundos
db_nome = 'dados_sensores.db'
caminho_db = os.path.join(os.path.dirname(__file__), db_nome)

# === Criação do banco e da tabela, se não existirem ===
def verificar_ou_criar_banco():
    conexao = sqlite3.connect(caminho_db)
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperatura REAL,
            umidade INTEGER,
            luminosidade TEXT,
            data_hora TEXT
        )
    ''')
    conexao.commit()
    conexao.close()
    print(f"✅ Banco de dados pronto em: {caminho_db}")

# === Função para salvar os dados ===
def salvar_dados(temperatura, umidade, luminosidade):
    try:
        conexao = sqlite3.connect(caminho_db)
        cursor = conexao.cursor()
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO medicoes (temperatura, umidade, luminosidade, data_hora)
            VALUES (?, ?, ?, ?)
        ''', (temperatura, umidade, luminosidade, data_hora))
        conexao.commit()
        conexao.close()
        print(f"📌 Salvo: {temperatura}°C, {umidade}%, Lum: {luminosidade} ({data_hora})")
    except Exception as e:
        print("❌ Erro ao salvar dados:", e)

# === Início ===
verificar_ou_criar_banco()

# Variáveis para armazenar os últimos dados lidos
ultima_temperatura = None
ultima_umidade = None
ultima_luminosidade = None
ultimo_salvamento = time.time()

try:
    arduino = serial.Serial(porta, baud_rate, timeout=2)
    time.sleep(2)
    print("🚀 Lendo dados do Arduino... (CTRL+C para encerrar)\n")

    while True:
        if arduino.in_waiting:
            linha = arduino.readline().decode('utf-8').strip()
            print("📥 Recebido:", linha)

            if linha.startswith("Temperatura:"):
                try:
                    temp_str = linha.split(":")[1].strip().replace("°C", "")
                    ultima_temperatura = float(temp_str)
                except:
                    print("⚠️ Falha ao interpretar temperatura.")

            elif linha.startswith("Umidade do Solo:"):
                try:
                    umid_str = linha.split(":")[1].strip().replace("%", "")
                    ultima_umidade = int(umid_str)
                except:
                    print("⚠️ Falha ao interpretar umidade.")

            elif linha.startswith("Luminosidade"):
                try:
                    ultima_luminosidade = linha.split(":")[1].strip()
                except:
                    print("⚠️ Falha ao interpretar luminosidade.")

        # Salvar a cada 10 segundos os últimos dados lidos
        if time.time() - ultimo_salvamento >= tempo_salvamento:
            if (ultima_temperatura is not None and
                ultima_umidade is not None and
                ultima_luminosidade is not None):
                
                salvar_dados(ultima_temperatura, ultima_umidade, ultima_luminosidade)
                ultimo_salvamento = time.time()

        time.sleep(0.3)

except serial.SerialException as e:
    print("❌ Erro ao conectar na porta serial:", e)

except KeyboardInterrupt:
    print("\n⛔ Programa encerrado pelo usuário.")

finally:
    if 'arduino' in locals():
        arduino.close()
        print("🔌 Conexão com Arduino encerrada.")
