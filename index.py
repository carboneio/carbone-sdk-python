import requests
import json
import hashlib

api_url = "https://render.carbone.io"
token = "Bearer eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIxNjY3IiwiYXVkIjoiY2FyYm9uZSIsImV4cCI6MjIxNzY3NTMwNSwiZGF0YSI6eyJpZEFjY291bnQiOjE2Njd9fQ.ABf57FFgQVX2nwo9gbYIruE17GNtvWKrWsgL7MP_dvgNEYAW5Kr-i9gXVKEBtHNTRtgr_rLHgnkyn4H-JsE2CqI8AXi-T8WGMR5DWdLn352VuA1xge39g9glZpNLVLVGalAZTp-u2ziZTbqlodtfOGzzZSPQnXCmOApsrHWfRhnLyfJX"
_templateID = "3b912b4f9adffcd8e8abd88dfb4db5c49e89a8cc1e111f6aa661cb3ef1d9459f"
headers = {
  'Authorization': token,
  'carbone-version': 2
}

def AddTemplate(templateFileName, payload = ""):
  fileData = open(templateFileName, "rb")
  multipart_form_data = {
    'template': ('template.odt', fileData),
    'payload': (None, payload)
  }
  return requests.post(api_url + '/template', files=multipart_form_data, headers=headers)

# try:
#   resp = AddTemplate("./template.odt")
#   print(json.loads(resp.text))
# except Exception as e:
#   print(e)

def GetTemplate(templateID):
  with requests.get(api_url + "/template/" + templateID,  stream=True, headers=headers) as r:
    return r.content

# try:
#   fileContent = GetTemplate(templateID)
#   fd = open("tmp.odt", "w")
#   fd.write(fileContent.decode())
#   fd.close()
# except Exception as e:
#   print(e)


def DeleteTemplate(templateID):
  return requests.delete(api_url + "/template/" + templateID, headers=headers)

# try:
#   resp = DeleteTemplate(templateID)
#   print(json.loads(resp.text))
# except Exception as e:
#   print(e)

def RenderReport(templateID, jsonData):
  return requests.post(api_url + "/render/" + templateID, json=jsonData, headers=headers)

# try:
#   templateData = {}
#   templateData["data"] = {
#     "firstname": "Steeve",
#     "lastname": "Payraudeau"
#   }
#   templateData["convertTo"] = "pdf"
#   print(templateData)
#   resp = RenderReport(_templateID, templateData)
#   print(json.loads(resp.text))
# except Exception as e:
#   print(e)

_renderID = "MTAuMjAuMTEuMTEgICAg01E95JJ9B74QWW81QYT1QYVBY5.pdf"

def GetReport(renderID):
  with requests.get(api_url + "/render/" + renderID,  stream=True, headers=headers) as r:
    return r.content

# try:
#   fileContent = GetReport(_renderID)
#   fd = open(_renderID, "wb")
#   fd.write(fileContent)
#   fd.close()
# except Exception as e:
#   print(e)

def GenerateTemplateID(templateFileName, payload = ""):
  with open(templateFileName,"rb") as f:
    bytes = f.read() # read entire file as bytes
    h = hashlib.sha256()
    h.update(payload.encode('utf-8'))
    h.update(bytes)
    return h.hexdigest()

# print("Test1: ", GenerateTemplateID("./tests/template.test.odt"))
# print("Test2: ", GenerateTemplateID("./tests/template.test.odt", "ThisIsAPayload"))
# print("Test3: ", GenerateTemplateID("./tests/template.test.odt", "8B5PmafbjdRqHuksjHNw83mvPiGj7WTE"))
# print("Test4: ", GenerateTemplateID("./tests/template.test.html"))
# print("Test5: ", GenerateTemplateID("./tests/template.test.html", "This is a long payload with different characters 1 *5 &*9 %$ 3%&@9 @(( 3992288282 29299 9299929"))