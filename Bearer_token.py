import requests
import json
import time
machines = ["000161228811", "161228811000", "000000000000", "111111111111"]


while True:

    for i in machines:

        url = "https://192.168.34.51/Devices/" + i + "/profSession"
        payload = json.dumps({
            "loginName": "Admin",
            "Password": "Miele123"
            })
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers,verify=False, data=payload)

        print(response.text)
        time.sleep(1)








payload = json.dumps({
  "loginName": "Admin",
  "Password": "Miele123"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers,verify=False, data=payload)

print(response.text)

