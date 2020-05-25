import requests
import json
import hashlib

class CarboneSDK:
  'Carbone SDK class used to call Carbone Render easily'

  def __init__(self, api_token = None):
    if api_token is None:
      raise ValueError('CarboneSDK: "API access token" is missing')
    self.__api_url = "https://render.carbone.io"
    self.__api_timeout = 10
    self.__api_headers = {
      "Authorization": "Bearer " + api_token,
      "carbone-version": "2"
    }

  def add_template(self, template_file_name = None, payload = ""):
    if template_file_name is None:
      raise ValueError('CarboneSDK: AddTemplate method: the argument template_file_name is missing')
    file_data = open(template_file_name, "rb")
    multipart_form_data = {
      "template": ("template.odt", file_data),
      "payload": (None, payload)
    }
    return requests.post(self.__api_url + '/template', files=multipart_form_data, headers=self.__api_headers, timeout=self.__api_timeout)

  def get_template(self, template_id = None):
    if template_id is None:
      raise ValueError('Carbone SDK get_template error: argument is missing: template_id')
    with requests.get(self.__api_url + "/template/" + template_id,  stream=True, headers=self.__api_headers, timeout=self.__api_timeout) as r:
      return r.content

  def delete_template(self, template_id = None):
    if template_id is None:
      raise ValueError('Carbone SDK get_template error: argument is missing: template_id')
    return requests.delete(self.__api_url + "/template/" + template_id, headers=self.__api_headers, timeout=self.__api_timeout)

  def render_report(self, template_id = None, json_data = None):
    if template_id is None:
      raise ValueError('Carbone SDK get_template error: argument is missing: template_id')
    if json_data is None:
      raise ValueError('Carbone SDK get_template error: argument is missing: json_data')
    return requests.post(self.__api_url + "/render/" + template_id, json=json_data, headers=self.__api_headers, timeout=self.__api_timeout)

  def get_report(self, render_id = None):
    if render_id is None:
      raise ValueError('Carbone SDK get_template error: argument is missing: render_id')
    with requests.get(self.__api_url + "/render/" + render_id,  stream=True, headers=self.__api_headers, timeout=self.__api_timeout) as r:
      return r.content

  def generate_template_id(self, template_file_name = None, payload = ""):
    with open(template_file_name,"rb") as f:
      bytes = f.read() # read entire file as bytes
      h = hashlib.sha256()
      h.update(payload.encode('utf-8'))
      h.update(bytes)
      return h.hexdigest()


_token = "eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIxNjY3IiwiYXVkIjoiY2FyYm9uZSIsImV4cCI6MjIxNzY3NTMwNSwiZGF0YSI6eyJpZEFjY291bnQiOjE2Njd9fQ.ABf57FFgQVX2nwo9gbYIruE17GNtvWKrWsgL7MP_dvgNEYAW5Kr-i9gXVKEBtHNTRtgr_rLHgnkyn4H-JsE2CqI8AXi-T8WGMR5DWdLn352VuA1xge39g9glZpNLVLVGalAZTp-u2ziZTbqlodtfOGzzZSPQnXCmOApsrHWfRhnLyfJX"
_template_id = "3b912b4f9adffcd8e8abd88dfb4db5c49e89a8cc1e111f6aa661cb3ef1d9459f"

CSDK = CarboneSDK(_token)

# ADD TEMPLATE
# try:
#   resp = CSDK.add_template('../template.odt')
#   print(json.loads(resp.text))
# except Exception as e:
#   print(e)

# GET TEMPLATE
# try:
#   f = CSDK.get_template(_template_id)
#   fd = open("tmp.odt", "wb")
#   fd.write(f)
#   fd.close()
# except Exception as e:
#   print(e)

# DELETE TEMPLATE
# try:
#   resp = CSDK.delete_template(_template_id)
#   print(json.loads(resp.text))
# except Exception as e:
#   print(e)

# RENDER TEMPLATE
# try:
#   _template_data = {}
#   _template_data["data"] = {
#     "firstname": "John",
#     "lastname": "Wick"
#   }
#   _template_data["convertTo"] = "odt"
#   resp = CSDK.render_report(_template_id, _template_data)
#   print(json.loads(resp.text))
# except Exception as e:
#   print(e)

_render_id = "MTAuMjAuMjEuMTAgICAg01E96E77G4CBP2MZSRXW4YYQHZ.odt"

# GET REPORT
# try:
#   f = CSDK.get_report(_render_id)
#   fd = open(_render_id, "wb")
#   fd.write(f)
#   fd.close()
# except Exception as e:
#   print(e)


# print("Test1: ", CSDK.generate_template_id("../tests/template.test.odt"))
# print("Test2: ", CSDK.generate_template_id("../tests/template.test.odt", "ThisIsAPayload"))
# print("Test3: ", CSDK.generate_template_id("../tests/template.test.odt", "8B5PmafbjdRqHuksjHNw83mvPiGj7WTE"))
# print("Test4: ", CSDK.generate_template_id("../tests/template.test.html"))
# print("Test5: ", CSDK.generate_template_id("../tests/template.test.html", "This is a long payload with different characters 1 *5 &*9 %$ 3%&@9 @(( 3992288282 29299 9299929"))