from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
import requests
import time

response = '{ "SessionId":"0000650471314B9CBF4265A6D98CFFB459521B52E8A7553BA63C68CDCD76F4BB99", "Timeout":600}'

machineIp = ["192.168.34.51", "192.168.34.52", "192.168.34.53", "192.168.34.54"]

machines_Id = ["000161228811", "161228811000", "000000000000", "111111111111"]

GET_json = '{ "ProgramId":11, "MachineNumber":1, "ProgramTime":8}' # json is user send a GET request

GET_json = json.loads(GET_json)

app = Flask(__name__)
api = Api(app)


class Start(Resource):
    def get(self):
        return {'Required Json objects': GET_json}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ProgramId', required=True, type=int)
        parser.add_argument('MachineNumber', required=True, type=int)
        parser.add_argument('ProgramTime', type=int)

        args = parser.parse_args()

        programId = args['ProgramId']
        machineNumber = args['MachineNumber']
        programTime = args['ProgramTime']

        request_miele(programId,machineNumber,programTime)

        return {
            'ProgamId': args['ProgramId'],
            'MachineNumber': args['MachineNumber'],
            'ProgramTime': args['ProgramTime']
        }, 200


def request_miele(programId, machineNumber, programTime):

    print("%d, %d, %d" % (programId, machineNumber, programTime))

    Bearer_token = GET_token(programId, machineNumber)
    print(Bearer_token)
    POST_program(programId, machineNumber, Bearer_token)



def GET_token(programId, machineNumber):


    url = "https://" + machineIp[machineNumber - 1] + "/Devices/" + machines_Id[machineNumber - 1] + "/profSession"
    print(url)

    payload = json.dumps({
        "loginName": "Admin",
        "Password": "Miele123"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    #response = requests.request("POST", url, headers=headers,verify=False, data=payload)

    parsed_data = json.loads(response)  # test_json will be replaced by the json of response
    token = parsed_data["SessionId"]
    return token

def POST_program(programId, machineNumber,Bearer_token ):

    return 0


api.add_resource(Start, '/start')


if __name__ == '__main__':
    app.run(port=8091)

