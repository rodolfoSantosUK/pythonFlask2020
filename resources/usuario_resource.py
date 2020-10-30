from flask_restful import Resource, reqparse
from modelos.usuario import UserModel

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
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
        atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")

        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message" : "The login '{}' already existis.".format(dados['login'])}

        user = UserModel( **dados )
        user.save_user()
        return {"message" : 'User created succesfully'}, 201

