from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from modelos.usuario import UserModel
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")

class User(Resource):

    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}


class User(Resource):


    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'Hotel not found'}, 404

    def delete(self, user_id):
        user = UserModel.find_user(user_id)

        if user:
            user.delete_user()
            return {'message': 'User deleted.'}
        return {'message': 'User not found'}, 404
     # hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]


class UserRegister(Resource):

    def post(self):

        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message" : "The login '{}' already existis.".format(dados['login'])}

        user = UserModel( **dados )
        user.save_user()
        return {"message" : 'User created succesfully'}, 201


class UserLogin(Resource):

    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])
        print(user)
        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity= user.user_id)
            return {'access_token': token_de_acesso}, 200
        return {'message': 'The username or password is incorrect.'}, 401