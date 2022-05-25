import time

import mysql.connector
import json
import requests
import os
requests.packages.urllib3.disable_warnings()

wachtwoord_miele = os.environ.get('wachtwoord_miele')
wachtwoord_miele = "{}".format(wachtwoord_miele)
print(wachtwoord_miele)

def GET_TotalMachines():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="machine_info"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT ID FROM machine_info")

    myresult = mycursor.fetchall()
    for row in myresult:
        TotalMachines = row[0]
    return TotalMachines

def GET_IP_db(MachineNumber):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="machine_info"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT MachineIP FROM machine_info WHERE ID = '{}'".format(MachineNumber))

    myresult = mycursor.fetchall()
    for row in myresult:
        MachineIP = row[0]
    return MachineIP


def GET_MachineID(MachineIP):
    url = "https://"+MachineIP+"/Devices"
    print(url)
    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, verify=False, data=payload)
    response = response.json()
    response = str(response)
    MachineID = response[2:14]
    return MachineID


def insert_ID(MachineNumber,MachineID):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="machine_info"
    )
    mycursor = mydb.cursor()
    sql = "UPDATE machine_info SET MachineID = '{}' WHERE ID = ({})".format(MachineID, MachineNumber)
    mycursor.execute(sql)
    mydb.commit()


def GET_ID_db(MachineNumber):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="machine_info"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT MachineID FROM machine_info WHERE ID = ({})".format(MachineNumber))

    myresult = mycursor.fetchall()
    for row in myresult:
        MachineID = row[0]
    return MachineID


def login(MachineIP, MachineID):
    url = "https://" + MachineIP + "/Devices/" + MachineID + "/profSession"
    payload = json.dumps({
        "loginName": "Admin",
        "Password": "",
        "PasswordNew": wachtwoord_miele
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, verify=False, data=payload)

    return 0


def GET_token(MachineIP, MachineID):
    url = "https://" + MachineIP + "/Devices/" + MachineID + "/profSession"
    payload = json.dumps({
        "loginName": "Admin",
        "Password": wachtwoord_miele
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, verify=False, data=payload)
    token = response.json()
    token = token["SessionId"]
    return token


def PUT_permissions(MachineIP, MachineID, token):
    url = "https://" +MachineIP+"/Devices/"+ MachineID+"/profUser/users/101"

    payload = json.dumps({
        "Roles": [
            1,
            2,
            101,
            102,
            103,
            104,
            105,
            106,
            107,
            108,
            109,
            111,
            112,
            113,
            121,
            122
        ]
    })
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, verify=False, data=payload)
    return 0




def machine_ID_db():
    TotalMachines = GET_TotalMachines()
    for i in range(1,TotalMachines + 1):
        MachineIP = GET_IP_db(i)
        MachineID = GET_MachineID(MachineIP)
        print(MachineID,MachineIP)
        insert_ID(i, MachineID)


def create_user():
    TotalMachines = GET_TotalMachines()
    for i in range (0, TotalMachines):
        MachineIP = GET_IP_db(i)
        MachineID = GET_ID_db(i)
        login(MachineIP, MachineID)
        token = GET_token(MachineIP, MachineID)
        PUT_permissions(MachineIP, MachineID, token)



machine_ID_db()
create_user()
