from flask_login import UserMixin
from app import db, login_manager

"""
	Devido ao tamanho do projeto, mantive todos os modelos no mesmo arquivo. Caso seja necessária a criação de mais modelos,
	em meu ponto de vista seria necessário a criação de arquivos especificos para cada modelo para melhor organização do código.
 
	Due to the size of the project, I kept all the models in the same file. If more models are needed,
	in my opinion it would be necessary to create specific files for each model for better code organization.
"""

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer)
    mes = db.Column(db.Integer)
    mercado = db.Column(db.String(50))
    rpk = db.Column(db.Float)
    
    
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String())
    

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))