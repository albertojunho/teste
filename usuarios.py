from database import db
from flask_login import UserMixin

class usuarios(db.Model,UserMixin):
  __tablename__ ="Usuarios"

  id_usuario = db.Column(db.Integer, primary_key = True, autoincrement=True)
  nome = db.Column(db.String(120))
  senha = db.Column(db.String(120))
  celular = db.Column(db.String(20))
  email = db.Column(db.String(120))
  endereco = db.Column(db.String(120))
  adm = db.Column(db.String(120))
   

  def __init__(self,nome, senha,celular,email,endereco,adm):
    self.nome = nome
    self.senha = senha
    self.celular = celular
    self.email = email
    self.endereco = endereco
    self.adm = adm


  def get_id(self):
    return self.id_usuario