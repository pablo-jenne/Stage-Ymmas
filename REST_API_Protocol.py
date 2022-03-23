from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
import time

x = '{ "ProgramId":11, "MachineNumber":1, "ProgramTime":8}'

x = json.loads(x)

app = Flask(__name__)
api = Api(app)


class Start(Resource):
    def get(self):
        return {'Required Json objects': x}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ProgramId', required=True, type=int)
        parser.add_argument('MachineNumber', required=True, type=int)
        parser.add_argument('ProgramTime', type=int)

        args = parser.parse_args()

        programmaId = args['ProgramId']
        machinenummer = args['MachineNumber']
        programmatijd = args['ProgramTime']
        request_miele(programmaId,machinenummer,programmatijd)

        return {
            'ProgamId': args['ProgramId'],
            'MachineNumber': args['MachineNumber'],
            'ProgramTime': args['ProgramTime']
        }, 200


def request_miele(programmaId, machinenummer, programmatijd):
    # API requests for controlling Miele machines
    print("%d, %d, %d" % (programmaId, machinenummer, programmatijd))


api.add_resource(Start, '/start')

if __name__ == '__main__':
    app.run(port=8091)

