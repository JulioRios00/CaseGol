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

- SQLite

**Containerização**

- Docker


## Como preparar e executar o projeto manualmente

## Acesse a pasta raiz do projeto
cd GolCase

python -m venv venv

## ubuntu:
source venv/bin/activate

## Windows:
venv\Scripts\activate


__Instale as dependências__

pip install -r requirements.txt

# Inicialize o banco de dados
flask db init
flask db migrate
flask db upgrade

# Execute a aplicação
flask run
# ou
python run.py


## Executando a aplicação utilizando Docker

## Acesse a pasta raiz do projeto
cd GolCase

docker-compose up -d --build (se quiser analisar os logs, bastar remover o comando -d da linha de comando)

Utilizando Docker a execução será executada assim que o container estiver funcionando!


A aplicação está definida para rodar na porta:

http://localhost:5000

## Primeiro Acesso
- Acesse a aplicação em http://localhost:5000
- Você será redirecionado para a página de login
- Clique em "Registrar" para criar uma nova conta
- Após o registro, faça login com suas credenciais
- Você será direcionado ao dashboard principal



## Developer Case

This project aims to execute the technical test for the Python Developer position.

## Technologies Used

**Backend**

- Flask
- SQLAlchemy

**Frontend**

- Dash
- Plotly
- HTML/CSS

**Database**

- SQLite

**Containerization**

- Docker


## How to Prepare and Run the Project Manually

## Access the project's root folder
cd GolCase

python -m venv venv

## Ubuntu:
source venv/bin/activate

## Windows:
venv\Scripts\activate


__Install dependencies__

pip install -r requirements.txt

# Initialize the 

flask db init
flask db migrate
flask db upgrade

# Run the application
flask run
# or
python run.py


## Running the Application Using Docker

## Access the project's root folder

cd GolCase

docker-compose up -d --build 

(If you want to analyze the logs, simply remove the -d flag from the command.)

When using Docker, the application will start running as soon as the container is up and running!

The application is set to run on:

http://localhost:5000

## First Access

- Open the application at http://localhost:5000
- You will be redirected to the login page
- Click "Register" to create a new account
- After registering, log in with your credentials
- You will be directed to the main dashboard

