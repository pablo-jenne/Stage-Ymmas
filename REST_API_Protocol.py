from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
import requests
import mysql.connector

response_token = '{ "SessionId":"0000650471314B9CBF4265A6D98CFFB459521B52E8A7553BA63C68CDCD76F4BB99", "Timeout":600}'

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

        if (status_code == 204):
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
    machine_ID, machine_IP = get_Ip_Id(machineNumber)

    Bearer_token = GET_token(machine_ID, machine_IP)

    status_code_miele = PUT_program(programId, machine_ID, machine_IP, Bearer_token)

    return (status_code_miele)





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

    #response_token = requests.request("POST", url, headers=headers, verify=False, data=payload)

    parsed_data = json.loads(response_token)
    token = parsed_data["SessionId"]
    return token





def PUT_program(programId, machine_ID, machine_IP, Bearer_token):

    url = "https://"+machine_IP+"/Devices/" +machine_ID+ "/profProgram/Selection/Select"
    print(url)
    payload = json.dumps({
        "ProgId": programId,
        "SelectionType": 1
    })

    headers = {
        'Authorization': Bearer_token,
        'Content-Type': 'application/json'
    }

    #response_program = requests.request("PUT", url, headers=headers, verify=False, data=payload)
    #return (response_program.status_code)
    return (204)





def update_status(machineNumber):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="machine_info"
    )
    mycursor = mydb.cursor()
    sql = "UPDATE machine_info SET Status = 'bezet' WHERE ID = ({})".format(machineNumber)
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")





api.add_resource(Start, '/start')


if __name__ == '__main__':
    app.run(port=8091)

