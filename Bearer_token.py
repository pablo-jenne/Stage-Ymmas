import requests
import json
import time


test_json = '{ "SessionId":"0000650471314B9CBF4265A6D98CFFB459521B52E8A7553BA63C68CDCD76F4BB99", "Timeout":600}'

machines_id = ["000161228811", "161228811000", "000000000000", "111111111111"]
machines_ip = ["192.168.34.51", "192.168.34.52", "192.168.34.53", "192.168.34.54"]

bearer_tokens = []
 
while True:

    for i in range(len(machines_id)):

        url = "https://" + machines_ip[i] +"/Devices/" + machines_id[i] + "/profSession"
        print(url)


        payload = json.dumps({
            "loginName": "Admin",
            "Password": "Miele123"
            })
        headers = {
          'Content-Type': 'application/json'
        }

        #response = requests.request("POST", url, headers=headers,verify=False, data=payload)

        x = json.loads(test_json) # test_json will be replaced by the json of response
        x = x["SessionId"]
        bearer_tokens.append(x)


    #JSON DUMP
        time.sleep(1)
    myjson = {
        'Token_1': bearer_tokens[0],
        'Token_2': bearer_tokens[1],
        'Token_3': bearer_tokens[2],
        'Token_4': bearer_tokens[3]
    }

    myjson = json.dumps(myjson)
    print(myjson)

    with open("sample.json", "w") as outfile:
        outfile.write(myjson)
    time.sleep(540)
