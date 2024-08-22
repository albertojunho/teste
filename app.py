from flask import Flask, render_template, request, redirect, url_for
import pymysql
from database import db, lm
from database import db
from flask_migrate import Migrate
from lagoas import Lagoa
from alerta import Alerta
from usuarios import usuarios
from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user
from flask_login import login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SEILA'
conexao = 'mysql+pymysql://Alberto:Americatmv/1@sos-alagamentos.mysql.database.azure.com/sosa'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
lm.init_app(app)
migrate = Migrate(app, db)

@app.route('/', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('telacadastro.html')
    
    else:
        nome = request.form.get('nome')
        email = request.form.get('email')
        celular = request.form.get('celular')
        senha = request.form.get('senha')
        endereco = request.form.get('endereco')
        user = usuarios(nome, senha, celular, email, endereco,"NÃO")
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('telalogin'))


@app.route('/informacaousuario')
@login_required
def informacaousuario():
    return render_template('informacaousuario.html')




@app.route('/update/<int:id_usuario>',methods = ['GET', 'POST'])
@login_required
def update(id_usuario):
    user = usuarios.query.get(id_usuario)
    
    if request.method=='GET':
        return render_template('updateusuario.html', user = user)
    
    else:
        nome = request.form.get('nome')
        email = request.form.get('email')
        celular = request.form.get('celular')
        endereco = request.form.get('endereco')

        user.nome = nome
        user.email = email
        user.celular = celular
        user.endereco = endereco

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('informacaousuario'))
    

@app.route('/usuarios')
@login_required
def usuario():
    users = usuarios.query.all() 
    if current_user.adm == "SIM":
        return render_template('listarusuarios.html',users = users)
    
    else:
        return redirect(url_for('telalogin'))

    

    

@app.route('/adm/<int:id_usuario>',methods = ['GET', 'POST'])
@login_required
def adm(id_usuario):
    users = usuarios.query.get(id_usuario)
    if request.method=='GET': 
        return render_template('usuariosadm.html',users = users)
    else:
        adm = request.form.get('adm')

        users.adm = adm
        db.session.add(users)
        db.session.commit()
        return redirect(url_for('usuario'))





@app.route('/excluirconta/<int:id_usuario>',methods = ['GET', 'POST'])
@login_required
def excluirconta(id_usuario):
    user = usuarios.query.get(id_usuario)
    if request.method =='GET':
        return render_template('excluirconta.html', user = user)
    
    else:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('add'))



@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@lm.user_loader
def load_user(id_usuario):
    user = usuarios.query.filter_by(id_usuario=id_usuario).first()
    return user

@app.route('/telalogin')
def telalogin():
    return render_template('telalogin.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('telalogin')

@app.route('/autenticar', methods=['POST'])
def autenticar():
  email = request.form.get('email')
  senha = request.form.get('senha')
  usuario = usuarios.query.filter_by(email = email).first()
  if usuario and (senha == usuario.senha):
    login_user(usuario)
    return redirect('/home')
  else:
    return redirect('/telalogin')





@app.route('/graficoslagoas')
@login_required
def grafico():
    return render_template('graficoslagoas.html')



@app.route('/configuracao')
@login_required
def configuracao():
    return render_template('configuracao.html')







@app.route('/map',methods = ['GET', 'POST'])
@login_required
def map():
    if request.method =='GET':
        return render_template('map.html')
    
    else:
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        nome = request.form.get("nome")
        nivel = int(request.form.get("nivel"))
        if nivel > int("5"):
            nivel = "Alto"
        elif nivel == int("5"):
            nivel = "Medio"
        else:
            nivel = "Baixo"
        lagoas = Lagoa(0,"-",nome,latitude,longitude,nivel)
        db.session.add(lagoas)
        db.session.commit()
        return redirect(url_for('listalagoa'))
        
@app.route('/listadelagoas')
@login_required
def listalagoa():
    listalagoas = Lagoa.query.all()
    return render_template('listadelagoas.html', listalagoas = listalagoas)


@app.route('/Excluirlagoa/<int:id_lagoa>',methods = ['GET', 'POST'])
@login_required
def deletelagoa(id_lagoa):
    lagoa = Lagoa.query.get(id_lagoa)
    if request.method =='GET':
        return render_template('Excluirlagoa.html', lagoa = lagoa)
    
    else:
        db.session.delete(lagoa)
        db.session.commit()
        return redirect(url_for('listalagoa'))
    


@app.route('/atualizarnivel/<int:id_lagoa>',methods = ['GET', 'POST'])
@login_required
def atualizarnivel(id_lagoa):
    lagoas = Lagoa.query.get(id_lagoa)
    
    if request.method=='GET':
        return render_template('atualizarnivel.html', lagoas = lagoas)
    
    else:
        nivel = int(request.form.get("nivel"))
        if nivel > int("5"):
            nivel = "Auto"
        elif nivel == int("5"):
            nivel = "Medio"
        else:
            nivel = "Baixo"
        
        lagoas.nivel = nivel
        

        db.session.add(lagoas)
        db.session.commit()
        return redirect(url_for('listalagoa'))

@app.route('/verlagoa/<int:id_lagoa>')
def verlagoa(id_lagoa):
    lagoas = Lagoa.query.filter_by(id_lagoa = id_lagoa).first()
    return render_template('verlagoa.html', lagoas = lagoas)

if __name__ == '__main__':
    app.run(debug=True)