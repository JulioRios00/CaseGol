## Case Desenvolvedor

Esse projeto tem como objetivo a execução do teste técnico para a vaga de Desenvolvedor - Python. 

## Técnologias utilizadas


**Backend**

- Flask
- SQLAlchemy

**Frontend**

- Dash
- Plotly
- HTML/CSS

**Banco de dados**

- PostgreSQL

**Containerização**

- Docker



## Executando a aplicação utilizando Docker

**Acesse a pasta raiz do projeto**
```
cd GolCase
```
Rode no terminal
```
docker-compose up -d --build 
```
(se quiser analisar os logs, bastar remover o comando -d da linha de comando)

Utilizando Docker a execução será executada assim que o container estiver funcionando! O banco de dados PostgreSQL será automaticamente configurado e populado com os dados necessários.


## Como preparar e executar o projeto manualmente

__Acesse a pasta raiz do projeto__
```
cd GolCase

python -m venv venv
```
**Ative o ambiente virtual no Ubuntu**:
```
source venv/bin/activate
```
**Ou no Windows**:
```
venv\Scripts\activate
```

__Instale as dependências__
```
pip install -r requirements.txt
```

__Configure o banco de dados__

Crie um arquivo `.env` baseado no `.env.example` e configure a URL do banco de dados PostgreSQL:
```
SECRET_KEY=golcase
SQLALCHEMY_DATABASE_URI=postgresql://usuario:senha@localhost:5432/golcase
```

# Inicialize o banco de dados
```
flask db init
flask db migrate
flask db upgrade
```

# Popule o banco de dados com dados de voos
```
python populate_db.py
```

# Execute a aplicação
```
flask run
# ou
python run.py
```


**A aplicação está definida para rodar na porta:**
```
http://localhost:5000
```

## Primeiro Acesso
- Acesse a aplicação em http://localhost:5000
- Você será redirecionado para a página de login
- Clique em "Registrar" para criar uma nova conta
- Após o registro, faça login com suas credenciais
- Você será direcionado ao dashboard principal



## Developer Case

This project aims to execute the technical test for the Python Developer position.

**Technologies Used**

**Backend**

- Flask
- SQLAlchemy

**Frontend**

- Dash
- Plotly
- HTML/CSS

**Database**

- PostgreSQL

**Containerization**

- Docker


## Running the Application Using Docker

**Access the project's root folder**
```
cd GolCase
```
Run on terminal:
```
docker-compose up -d --build 
```
(If you want to analyze the logs, simply remove the -d flag from the command.)

When using Docker, the application will start running as soon as the container is up and running! The PostgreSQL database will be automatically configured and populated with the necessary data.

## How to Prepare and Run the Project Manually

**Access the project's root folder**
```
cd GolCase
python -m venv venv
```
**Activate the virtual env on Ubuntu:**
```
source venv/bin/activate
```
## Or on Windows:
```
venv\Scripts\activate
```

__Install dependencies__

```
pip install -r requirements.txt
```

__Configure the database__

Create a `.env` file based on `.env.example` and configure the PostgreSQL database URL:
```
SECRET_KEY=golcase
SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost:5432/golcase
```

# Initialize the Database
```
flask db init
flask db migrate
flask db upgrade
```

# Populate the database with flight data
```
python populate_db.py
```

# Run the application
```
flask run
# or
python run.py
```

The application is set to run on:
```
http://localhost:5000
```

## First Access

- Open the application at http://localhost:5000
- You will be redirected to the login page
- Click "Register" to create a new account
- After registering, log in with your credentials
- You will be directed to the main dashboard

