from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity,
)
from models.client import ClientModel


class Client(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('client_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('msanum',
                        type=int,
                        required=True,
                        help="Every client needs a msa number."
                        )
    parser.add_argument('url',
                        type=str,
                        required=True,
                        help="Every client needs a url."
                        )
    parser.add_argument('create_date',
                        type=str,
                        required=True,
                        help="Every client needs a create date."
                        )
    parser.add_argument('client_info',
                        type=str,
                        required=True,
                        help="Every client needs some client info."
                        )

    @jwt_required()
    def get(self, client_name):
        client = ClientModel.find_by_name(client_name)
        if client:
            return client.json()
        return {'message': 'Client not found!'}, 404

    @jwt_required(fresh=True)
    def post(self, client_name):
        if ClientModel.find_by_name(client_name):
            return {'message': "An client with name '{}' already exists.".format(client_name)}, 400

        data = self.parser.parse_args()

        client = ClientModel(
            client_name, data['msanum'], data['url'], data['create_date'], data['client_info'])

        try:
            client.save_to_db()
        except:
            return {"message": "An error occurred inserting the client."}, 500

        return client.json(), 201

    @jwt_required()
    def delete(self, client_name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin priviledge required!'}, 401

        client = ClientModel.find_by_name(client_name)
        if client:
            client.delete_from_db()
            return {'message': 'Client deleted.'}
        return {'message': 'Client not found.'}, 404

    def put(self, client_name):
        data = Client.parser.parse_args()

        client = ClientModel.find_by_name(client_name)

        if client:
            client.client_info = data['client_info']
            client.msanum = data['msanum']
            client.create_date = data['create_date']
            client.url = data['url']
        else:
            client = ClientModel(client_name, **data)

        client.save_to_db()

        return client.json()


class ClientList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        clients = [client.json() for client in ClientModel.find_all()]
        if user_id:
            return {'clients': [client.json() for client in ClientModel.find_all()]}, 200
        return {
            'clients': [client['client_name'] for client in clients],
            'message': 'More data available if you log in.'
        }, 200
