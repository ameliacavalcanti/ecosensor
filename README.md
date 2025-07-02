# 🌿 EcoSensor

**EcoSensor** é um sistema web desenvolvido com **FastAPI + SQLite** para monitoramento ambiental em tempo real.  
Ele permite cadastrar usuários, terrenos e registrar medições como temperatura, umidade, luminosidade e pH, podendo ser alimentado por dados de sensores via Arduino.

O projeto utiliza **dois bancos de dados**:
- `ecosensor.db`: banco principal definitivo, com relacionamentos entre usuários, terrenos e medições.
- `dados_sensores.db`: banco temporário, utilizado durante o desenvolvimento para registrar medições em tempo real.

---

## ⚙️ Funcionalidades

- Cadastro de usuários com nome, e-mail e senha
- Cadastro de terrenos vinculados a usuários
- Visualização das últimas medições em uma dashboard web
- Coleta automática de dados em tempo real do Arduino (via porta serial)
- Banco de dados leve e local usando SQLite
- Classificação da luminosidade (ex.: "450 - Dia" ou "120 - Noite")

---

## 🗂️ Estrutura do Projeto

```
ecosensor/
├── main.py               # Backend principal (site e dashboard)
├── verificarduino.py     # Script de leitura serial em tempo real
├── models.py             # Funções para acesso ao banco de dados
├── init_db.py            # Script para criar as tabelas SQLite
├── database/
│   ├── ecosensor.db      # Banco SQLite principal
│   └── dados_sensores.db # Banco SQLite temporário (coleta de dados)
├── static/               # CSS, JS, imagens
├── templates/            # HTML com Jinja2
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação (este arquivo)
```

---

## 🚀 Como Executar o Projeto

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 2. Crie o banco de dados principal

```bash
python init_db.py
```

---

### 3. Inicie o backend principal (interface web)

```bash
uvicorn main:app --reload
```

Acesse no navegador: [http://localhost:8000](http://localhost:8000)

---

### 4. Inicie a coleta de dados do Arduino (via porta serial)

```bash
python verificarduino.py
```

Este script conecta ao Arduino pela porta serial e insere medições automaticamente no banco temporário `dados_sensores.db`.

---

## 🔁 Exemplo de JSON (caso precise integração futura via API)

```json
{
  "terreno_id": 1,
  "temperatura": 25.5,
  "umidade": 60,
  "luminosidade": 450,
  "ph": 6.8
}
```

> ⚠️ O campo **luminosidade** contém o valor numérico. O sistema classifica automaticamente como "Dia" ou "Noite" ao salvar.

---

## 🌐 Futuro da Implementação

Em etapas futuras:
- As medições passarão a ser enviadas **via WiFi** diretamente ao banco principal (`ecosensor.db`), eliminando o banco temporário.
- Cada medição ficará vinculada ao terreno e ao usuário responsável, tornando o sistema mais seguro, integrado e escalável.

---

## 📄 Licença

Este projeto é de uso livre para fins acadêmicos e educacionais.
