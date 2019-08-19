from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# Inicio do app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Classe do produto
class Produto(db.Model):
  id         = db.Column(db.Integer, primary_key=True)
  nome       = db.Column(db.String(100), unique=True)
  descricao  = db.Column(db.String(200))
  preco      = db.Column(db.Float)
  quantidade = db.Column(db.Integer)

  def __init__(self, nome, descricao, preco, quantidade):
    self.nome       = nome
    self.descricao  = descricao
    self.preco      = preco
    self.quantidade = quantidade

# Schema do produto
class ProdutoSchema(ma.Schema):
  class Meta:
    fields = ('id', 'nome', 'descricao', 'preco', 'quantidade')

# Inicio do schema
produto_schema = ProdutoSchema(strict=True)
produto_schema = ProdutoSchema(many=True, strict=True)

# Criar um produto (POST)
@app.route('/produto', methods=['POST'])
def add_produto():
  nome       = request.json['nome']
  descricao  = request.json['descricao']
  preco      = request.json['preco']
  quantidade = request.json['quantidade']

  novo_produto = Produto(nome, descricao, preco, quantidade)

  db.session.add(novo_produto)
  db.session.commit()

  return produto_schema.jsonify(novo_produto)

# Retornar todos os produtos (GET)
@app.route('/produto', methods=['GET'])
def get_produtos():
  all_produtos = Produto.query.all()
  resultado    = produto_schema.dump(all_produtos)
  return jsonify(resultado.data)

# Retornar um produto especifico GET
@app.route('/produto/<id>', methods=['GET'])
def get_produto(id):
  produto = Produto.query.get(id)
  return produto_schema.jsonify(produto)

# Atualizar um produto (PUT)
@app.route('/produto/<id>', methods=['PUT'])
def update_produto(id):
  produto = produto.query.get(id)

  nome = request.json['nome']
  descricao = request.json['descricao']
  preco = request.json['preco']
  quantidade = request.json['quantidade']

  produto.nome = nome
  produto.descricao = descricao
  produto.preco = preco
  produto.quantidade = quantidade

  db.session.commit()

  return produto_schema.jsonify(produto)

# Deletar produto (DELETE)
@app.route('/produto/<id>', methods=['DELETE'])
def deletar_produto(id):
  produto = produto.query.get(id)
  db.session.delete(produto)
  db.session.commit()

  return produto_schema.jsonify(produto)

# Rodando o servidor
if __name__ == '__main__':
  app.run(debug=True)
