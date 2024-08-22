
class usuario:
  def __init__(self, id,nome,telefone):
    self.id = id
    self.nome = nome
    self.telefone = telefone





    db=pymysql.connect(
            host="albalopes.tech",
            user="psi2023_alberto",
            password="AnVkUR51P_bvm[jm",
            db="psi2023_alberto",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor)
