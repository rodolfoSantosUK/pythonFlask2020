from flask_restful import Resource, reqparse
from modelos.hotel import HotelModel

hoteis = [
    {
        "hotel_id": "alpha",
        "nome": "Aplha Hotel",
        "estrelas": 4.3,
        "diaria": 420.34,
        "cidade": "Rio de Janeiro"
    },
    {
        "hotel_id": "bravo",
        "nome": "Bravo Hotel",
        "estrelas": 4.9,
        "diaria": 420.34,
        "cidade": "Santa Catarina"
    },
    {
        "hotel_id": "alpha",
        "nome": "Alpha Hotel",
        "estrelas": 4.3,
        "diaria": 420.34,
        "cidade": "Sao Paulo"
    }
]


class Hoteis(Resource):

    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome", type=str, required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument("estrelas", type=str, required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument("diaria")
    argumentos.add_argument("cidade")


    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' alredy exists.".format(hotel_id)}, 400

        dados = Hotel.argumentos.parse_args()
        hotel =  HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message" : "Ocorreu um erro interno"}, 500
        return hotel.json()


    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200

        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "Ocorreu um erro interno"}, 500
        return hotel.json(), 201

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            hotel.delete_hotel()
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found'}, 404
     # hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]



