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

