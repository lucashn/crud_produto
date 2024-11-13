from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

PRODUTOS = {
    'p1': {
        'id': 'p1',
        'nome': 'Camiseta',
        'quantidade': 10,
        'preco': 29.99
    },
    'p2': {
        'id': 'p2',
        'nome': 'Calça',
        'quantidade': 5,
        'preco': 59.99
    },
    'p3': {
        'id': 'p3',
        'nome': 'Kit de meias',
        'quantidade': 7,
        'preco': 23.56
    },
}


def abortar_se_nao_existir(id):
    if id not in PRODUTOS:
        abort(404, message="Produto {} não existe".format(id))


parser = reqparse.RequestParser()
parser.add_argument('nome')
parser.add_argument('quantidade')
parser.add_argument('preco')
parser.add_argument('id')


def le_produto(args):
    return {
        'nome': args['nome'],
        'quantidade': int(args['quantidade']),
        'preco': float(args['preco'])
    }


class Produto(Resource):
    def get(self, id):
        abortar_se_nao_existir(id)
        return PRODUTOS[id]

    def delete(self, id):
        abortar_se_nao_existir(id)
        del PRODUTOS[id]
        return '', 204

    def put(self, id):
        args = parser.parse_args()
        PRODUTOS[id] = le_produto(args)
        PRODUTOS[id]["id"] = id 
        return PRODUTOS[id], 201

class ListaProdutos(Resource):
    def get(self):
        return list(PRODUTOS.values())

    def post(self):
        args = parser.parse_args()
        id = int(max(PRODUTOS.keys()).lstrip('p')) + 1
        id = f'p{id}'
        PRODUTOS[id] = le_produto(args)
        PRODUTOS[id]["id"] = id 
        return PRODUTOS[id], 201

api.add_resource(ListaProdutos, '/produto')
api.add_resource(Produto, '/produto/<id>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0") # colocar o IP da máquina para possibilitar acesso externo
