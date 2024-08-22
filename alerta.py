from database import db

class Alerta(db.Model):
  __tablename__ = "Alerta"

  id_alerta = db.Column(db.Integer, primary_key=True,autoincrement=True)
  alerta = db.Column(db.String(120))
  dt_alerta = db.Column(db.DateTime())
  fk_lagoa = db.Column(db.Integer, db.ForeignKey('lagoa.id_lagoa'))
  lagoa = db.relationship('Lagoa', foreign_keys=fk_lagoa)

  def __init__(self, id_alerta, alerta, dt_alerta, fk_lagoa):
    self.id_alerta = id_alerta
    self.alerta = alerta
    self.dt_alerta = dt_alerta
    self.fk_lagoa = fk_lagoa
