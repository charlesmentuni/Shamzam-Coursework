import base64
import requests
import unittest

alexa = "http://localhost:3004/alexa"
stt = "http://localhost:3001/stt"
tts = "http://localhost:3002/tts"
class Testing(unittest.TestCase):
  ###########################################################
  ## Test [1]                                              ##
  ###########################################################
    def test1(self):
        hdrs = {"Content-Type":"application/json"}
        js   = {"text": "What are you?"}
        rsp  = requests.post(tts,headers=hdrs,json=js)


        hdrs = {"Content-Type":"application/json"}
        js   = {"speech": rsp.json()["speech"]}
        rsp1 = requests.post(alexa,headers=hdrs,json=js)
        print(rsp1.json().keys())
        speech = rsp1.json()["speech"]
        wav    = base64.b64decode(speech)
        f      = open("answer.wav","wb")
        f.write(wav)
        f.close()
        self.assertEqual(rsp.status_code,200)
        # verify speech somehow? Use speech to text

    def test2(self):
        f = open("good 4 u.wav","rb")
        wav = f.read()
        f.close()

        hdrs = {"Content-Type":"application/json"}
        js   = {"speech": base64.b64encode(wav).decode("utf-8")}
        rsp1 = requests.post(alexa,headers=hdrs,json=js)
        print(rsp1.json().keys())
        speech = rsp1.json()["speech"]
        wav    = base64.b64decode(speech)
        f      = open("answer.wav","wb")
        f.write(wav)
        f.close()
        self.assertEqual(rsp.status_code,200)
