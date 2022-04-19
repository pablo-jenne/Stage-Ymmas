import mysql.connector
import requests
import json

test_json_status = '{ "Status":5, "ProgramID":43, "ProgramPhase":15, "pRemainingTime": "PT12H30M17S", "pElapsedTime": "PT12H30M17S", "pSystemTime": "2014-10-22T14:00:00+02:00", "pStartTime": "2014-10-22T13:48:00+02:00", "pEndTime": "2014-10-22T17:20:00+02:00", "pLastNotificationTime": "2014-10-22T13:30:40.123+02:00"}'


def get_data():
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="machine_info"
  )

  mycursor = mydb.cursor()
  alist = []
  mycursor.execute("SELECT * FROM machine_info")

  myresult = mycursor.fetchall()
  alist = list(myresult)
  return alist



def get_status(cut_str_Machine_Ip, cut_str_Machine_Id):
  url = "https://"+cut_str_Machine_Ip+"/Devices/"+cut_str_Machine_Id+"/State"

  payload = ""
  headers = {
  }

  #Response_Status = requests.request("GET", url, headers=headers, verify=False, data=payload)

  Data_Status = json.loads(test_json_status)
  #Data_Status = Data_Status["SessionId"]
  return Data_Status



data = get_data()

for i in range(len(data)):
  merker = str(data[i])

  a, Machine_Ip, Machine_Id, Status = merker.split(",")

  cut_str_Machine_Ip = Machine_Ip[2:15]
  cut_str_Machine_Id = Machine_Id[2:14]
  cut_str_Status = Status[2:7]
  print(cut_str_Status)

  if (cut_str_Status == 'bezet'):
    #print(cut_str_Machine_Id, Machine_Ip)
    Data_Status = get_status(cut_str_Machine_Ip,cut_str_Machine_Id)
    print(Data_Status)


