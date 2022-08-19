from ast import main
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLAlchemy_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)


class Pessoa(db.Model):

    __tablename__ = 'cliente'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    telefone = db.Column(db.String)
    CPF = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, nome, telefone, CPF, email):
        self.nome = nome
        self.telefone = telefone
        self.CPF = CPF
        self.email = email


db.create_all()


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")


@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        CPF = request.form.get("CPF")
        email = request.form.get("email")

        if nome and telefone and CPF and email:
            p = Pessoa(nome, telefone, CPF, email)
            db.session.add(p)
            db.session.commit()

    return redirect(url_for("index"))


@app.route("/excluir/<int:id>")
def excluir(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()

    db.session.delete(pessoa)
    db.session.commit()

    pessoas = Pessoa.query.all()
    return render_template("lista.html", pessoas=pessoas)


@app.route("/lista")
def lista():
    pessoas = Pessoa.query.all()
    return render_template("lista.html", pessoas=pessoas)


@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()

    if request.method == "POST":
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        CPF = request.form.get("CPF")
        email = request.form.get("email")

        if nome and telefone and CPF and email:
            pessoa.nome = nome
            pessoa.telefone = telefone
            pessoa.CPF = CPF
            pessoa.email = email

            db.session.commit()

            return redirect(url_for("lista"))

    return render_template("atualizar.html", pessoa=pessoa)


if __name__ == '__main__':
    app.run(debug=True)
