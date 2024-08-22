from database import db

class Lagoa(db.Model):
  __tablename__ ="lagoa"

  id_lagoa = db.Column(db.Integer, primary_key = True,autoincrement=True)
  alerta = db.Column(db.String(120))
  nome = db.Column(db.String(120))
  latitude = db.Column(db.Float)
  longitude = db.Column(db.Float)
  nivel = db.Column(db.String(120))
  alertas = db.relationship("Alerta")
 

  def __init__(self,id_lagoa,alerta,nome,latitude,longitude,nivel):
    self.id_lagoa = id_lagoa
    self.alerta = alerta
    self.nome = nome
    self.latitude = latitude
    self.longitude = longitude
    self.nivel = nivel
   