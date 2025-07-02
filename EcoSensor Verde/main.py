from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import conectar, cadastrar_usuario, cadastrar_terreno, registrar_medicao
import sqlite3
import os

app = FastAPI()

# Monta a pasta de arquivos estáticos (CSS/JS/imagens)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Diretório dos templates HTML
templates = Jinja2Templates(directory="templates")

# Função para obter o último dado do banco
def get_ultimo_dado():
    db_path = "dados_sensores.db"
    if not os.path.exists(db_path):
        return {"temperatura": "--", "umidade": "--", "luminosidade": "--", "ph": "--"}

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT temperatura, umidade, luminosidade FROM medicoes ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
    except Exception as e:
        print("Erro ao acessar banco:", e)
        row = None
    finally:
        if conn:
            conn.close()

    if row:
        return {
            "temperatura": f"{row[0]} °C",
            "umidade": f"{row[1]} %",
            "luminosidade": f"{row[2]} Lux",
            "ph": "--"
        }

    return {"temperatura": "--", "umidade": "--", "luminosidade": "--", "ph": "--"}

# Página inicial (EcoSensor)
@app.get("/", response_class=HTMLResponse)
async def painel(request: Request):
    dados = get_ultimo_dado()
    return templates.TemplateResponse("EcoSensor.html", {"request": request, **dados})

# Outras páginas (rotas)
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("Dashboard.html", {"request": request})

@app.get("/desempenho", response_class=HTMLResponse)
async def desempenho(request: Request):
    return templates.TemplateResponse("Desempenho.html", {"request": request})

@app.get("/contato", response_class=HTMLResponse)
async def contato(request: Request):
    return templates.TemplateResponse("Contato.html", {"request": request})

@app.get("/solucoes", response_class=HTMLResponse)
async def solucoes(request: Request):
    return templates.TemplateResponse("Solucoes.html", {"request": request})

@app.get("/historico", response_class=HTMLResponse)
async def historico(request: Request):
    return templates.TemplateResponse("Historico.html", {"request": request})

@app.get("/especies", response_class=HTMLResponse)
async def especies(request: Request):
    return templates.TemplateResponse("Especie.html", {"request": request})

@app.get("/cadastro_especies", response_class=HTMLResponse)
async def cadastro(request: Request):
    return templates.TemplateResponse("Cadastro_especies.html", {"request": request})

@app.get("/")
def root():
    return {"message": "API funcionando"}

# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT temperatura, umidade, luminosidade, ph, timestamp FROM medicoes ORDER BY timestamp DESC LIMIT 10")
    medicoes = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "medicoes": medicoes})

@app.post("/cadastrar_usuario")
def cadastrar_usuario_endpoint(nome: str = Form(...), email: str = Form(...), senha: str = Form(...)):
    cadastrar_usuario(nome, email, senha)
    return RedirectResponse(url="/", status_code=303)

@app.post("/cadastrar_terreno")
def cadastrar_terreno_endpoint(nome: str = Form(...), localizacao: str = Form(...), usuario_id: int = Form(...)):
    cadastrar_terreno(nome, localizacao, usuario_id)
    return RedirectResponse(url="/", status_code=303)

