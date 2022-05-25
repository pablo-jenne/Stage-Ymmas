import mysql.connector
import requests
import json
import time
import pymongo
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
requests.packages.urllib3.disable_warnings()

wachtwoord_miele = os.environ.get('wachtwoord_miele')
wachtwoord_miele = "{}".format(wachtwoord_miele)

wachtwoord_mongodb = os.environ.get('wachtwoord_mongodb')
wachtwoord_mongodb = "{}".format(wachtwoord_mongodb)

def get_data():
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="machine_info"
  )

  mycursor = mydb.cursor()
  mycursor.execute("SELECT ID,MachineIP, MachineID FROM machine_info WHERE Status = 'bussy'")

  myresult = mycursor.fetchall()
  alist = list(myresult)
  return alist


def get_status(MachineIP, MachineID, Bearer_token, ID):
  url = "https://"+MachineIP+"/Devices/"+MachineID+"/State"
  payload = ""
  headers = {
    'Authorization': 'Bearer {}'.format(Bearer_token),
    'Content-Type': 'application/json'
  }

  Response_Status = requests.request("GET", url, headers=headers, verify=False, data=payload)

  Data_Status = Response_Status.json()
  add_id = {"machineNumber": ID}
  Data_Status.update(add_id)
  Main_Status = Data_Status["Status"]
  Door_status = Data_Status["pExtended"]["DoorOpen"]

  if Main_Status == 7 or Main_Status == 9 or Door_status == True :
    update_status_free(ID) # set machine free in database

  return Data_Status


def insert_database(Data_Status):
  cluster = MongoClient(
    "mongodb+srv://Pablo:"+wachtwoord_mongodb+"@cluster0.vitsu.mongodb.net/myFirstDatabase")
  db = cluster["test"]
  collection = db["test"]

  collection.insert_one(Data_Status)
  return "inserted"


def update_status_free(MachineNumber):
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="machine_info"
  )
  mycursor = mydb.cursor()
  sql = "UPDATE machine_info SET Status = 'free' WHERE ID = ({})".format(MachineNumber)
  mycursor.execute(sql)
  mydb.commit()
  print(mycursor.rowcount, "record(s) affected free")



def get_Bearer_token_database(MachineNumber):
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="machine_info"
  )
  mycursor = mydb.cursor()
  sql = "SELECT Bearer_token FROM machine_info WHERE ID = '{}'".format(MachineNumber)

  mycursor.execute(sql)

  myresult = mycursor.fetchall()

  for rows in myresult:
    Bearer_token = rows[0]
  return Bearer_token


while True:

  try:
    data = get_data()

    if(len(data) > 0):
      for rows in data:
        ID = rows[0]
        MachineIP = rows[1]
        MachineID = rows[2]

        Bearer_token = get_Bearer_token_database(ID)
        Data_Status = get_status(MachineIP, MachineID, Bearer_token, ID)
        insert_database(Data_Status)

    else:
      time.sleep(1)
  except:
    cluster = MongoClient(
      "mongodb+srv://Pablo:"+wachtwoord_mongodb+"@cluster0.vitsu.mongodb.net/myFirstDatabase")
    db = cluster["test"]
    collection = db["errors"]

    status = {
      "Failed_to_read_status": datetime.now(),
      "MachineNumber": ID
    }

    collection.insert_one(status)
