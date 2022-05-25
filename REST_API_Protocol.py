from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
import requests
import mysql.connector
requests.packages.urllib3.disable_warnings()

GET_json = '{ "ProgramId": "" , "MachineNumber": "" , "ProgramTime": ""}' # json if user send a GET request

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

        status_code = request_miele(programId,machineNumber,programTime)

        if (status_code[0] == 204 and status_code[1] == 200):
            update_status(machineNumber)
            return {
                       'ProgamId': args['ProgramId'],
                       'MachineNumber': args['MachineNumber'],
                       'ProgramTime': args['ProgramTime']
                   }, 200

        else:
            return {'Failed': status_code} # returns status code from Miele machine





def request_miele(programId, machineNumber, programTime):

    print('programID: {} en machineNumber {}'.format(programId, machineNumber))

    if programTime == 0:
        print("wasmchine")
        machine_ID, machine_IP = get_Ip_Id(machineNumber)
        Bearer_token = GET_token(machine_ID, machine_IP)
        status_code_program = PUT_program(programId, machine_ID, machine_IP, Bearer_token)
        status_code_payment = PUT_payment_washing(machine_ID, machine_IP, Bearer_token)

        return (status_code_program, status_code_payment)

    elif programTime > 0:
        print("droogkast")
        machine_ID, machine_IP = get_Ip_Id(machineNumber)
        Bearer_token = GET_token(machine_ID, machine_IP)
        status_code_program = PUT_program(programId, machine_ID, machine_IP, Bearer_token)
        status_code_payment = PUT_payment_dryer(machine_ID, machine_IP, Bearer_token, programTime)

        return (status_code_program, status_code_payment)


def get_Ip_Id(machineNumber):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="machine_info"
    )
    mycursor = mydb.cursor()
    sql = """SELECT MachineIP, MachineID FROM machine_info WHERE ID = %s"""

    mycursor.execute(sql, (machineNumber,))

    data = mycursor.fetchall()
    data = list(data)
    for i in range(len(data)):
        data = str(data[i])
        machine_IP, machine_ID = data.split(",")
        cut_str_Machine_IP = machine_IP[2:15]
        cut_str_Machine_ID = machine_ID[2:14]

    return (cut_str_Machine_ID, cut_str_Machine_IP)






def GET_token(machine_ID, machine_IP):


    url = "https://" + machine_IP + "/Devices/" + machine_ID + "/profSession"
    print(url)
    payload = json.dumps({
        "loginName": "Admin",
        "Password": "Miele123"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response_token = requests.request("POST", url, headers=headers, verify=False, data=payload)
    response_token = response_token.json()
    token = response_token["SessionId"]
    return token





def PUT_program(programId, machine_ID, machine_IP, Bearer_token):

    url = "https://"+machine_IP+"/Devices/" +machine_ID+ "/profProgram/Selection/Select"
    print(url)
    payload = json.dumps({
        "ProgId": programId,
        "SelectionType": 1
    })

    headers = {
        'Authorization': 'Bearer {}'.format(Bearer_token),
        'Content-Type': 'application/json'
    }

    response_program = requests.request("PUT", url, headers=headers, verify=False, data=payload)
    return (response_program.status_code)


def PUT_payment_washing(machine_ID,machine_IP, Bearer_token):

    url = "https://"+machine_IP+"/Devices/" +machine_ID+ "/profPayment"
    print(url)
    payload = json.dumps({
     "PaymentMode": 1,
     "PaymentState": 1,
     "PaidTime": 0
    })

    headers = {
        'Authorization': 'Bearer {}'.format(Bearer_token),
        'Content-Type': 'application/json'
    }

    response_program = requests.request("PUT", url, headers=headers, verify=False, data=payload)
    return (response_program.status_code)


def PUT_payment_dryer(machine_ID, machine_IP, Bearer_token, programTime):

    url = "https://" + machine_IP + "/Devices/" + machine_ID + "/profPayment"
    print(url)
    payload = json.dumps({
        "PaymentMode": 1,
        "PaymentState": 1,
        "TimeMode": 1,
        "PaidTime": programTime
    })

    headers = {
        'Authorization': 'Bearer {}'.format(Bearer_token),
        'Content-Type': 'application/json'
    }

    response_program = requests.request("PUT", url, headers=headers, verify=False, data=payload)
    return (response_program.status_code)


def update_status(machineNumber):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="machine_info"
    )
    mycursor = mydb.cursor()
    sql = "UPDATE machine_info SET Status = 'bussy' WHERE ID = ({})".format(machineNumber)
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")


api.add_resource(Start, '/start')


if __name__ == '__main__':
    app.run(port=8091)

