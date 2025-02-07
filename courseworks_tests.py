import requests
import base64
import json


CONVERT_URL = "http://localhost:3002/user/convert"

def test1():
    # json input? ask about this
    cropped_file = base64.b64encode(open("_Blinding Lights.wav", 'rb').read())
    
    print(cropped_file)
    #cropped_file = open("_Blinding Lights.wav", 'rb')

    print("yes")
    hdrs = {"Content-Type" : "multipart/form-data"}#, "audio" : cropped_file}
    js   =  { "audio" : str(cropped_file) }

    rsp  = requests.post(CONVERT_URL, json=js)#, data=hdrs)

    print(rsp.text)


if __name__ == "__main__":
    test1()