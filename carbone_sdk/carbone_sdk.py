import requests
import json
import hashlib
import os

class CarboneSDK:
  'Carbone SDK class used to call Carbone Render easily'

  def __init__(self, api_token = None):
    if ('CARBONE_TOKEN' in os.environ):
      api_token = os.environ.get('CARBONE_TOKEN')
    if api_token is None:
      raise ValueError('CarboneSDK: "API access token" is missing')
    self._api_url = "https://render.carbone.io"
    self._api_timeout = 10
    self._api_headers = {
      "Authorization": "Bearer " + api_token,
      "carbone-version": "2"
    }

  def add_template(self, template_file_name = None, payload = ""):
    if template_file_name is None:
      raise ValueError('CarboneSDK: add_template method: the argument template_file_name is missing')
      return
    file_data = open(template_file_name, "rb")
    multipart_form_data = {
      "template": ("template.odt", file_data),
      "payload": (None, payload)
    }
    return requests.post(self._api_url + '/template', files=multipart_form_data, headers=self._api_headers, timeout=self._api_timeout)

  def get_template(self, template_id = None):
    if template_id is None:
      raise ValueError('Carbone SDK get_template error: argument is missing: template_id')
      return
    with requests.get(self._api_url + "/template/" + template_id,  stream=True, headers=self._api_headers, timeout=self._api_timeout) as r:
      return r.content

  def delete_template(self, template_id = None):
    if template_id is None:
      raise ValueError('Carbone SDK delete_template error: argument is missing: template_id')
      return
    return requests.delete(self._api_url + "/template/" + template_id, headers=self._api_headers, timeout=self._api_timeout)

  def render_report(self, template_id = None, json_data = None):
    if template_id is None:
      raise ValueError('Carbone SDK render_report error: argument is missing: template_id')
      return
    if json_data is None:
      raise ValueError('Carbone SDK render_report error: argument is missing: json_data')
      return
    return requests.post(self._api_url + "/render/" + template_id, json=json_data, headers=self._api_headers, timeout=self._api_timeout)

  def get_report(self, render_id = None):
    if render_id is None:
      raise ValueError('Carbone SDK get_report error: argument is missing: render_id')
      return
    with requests.get(self._api_url + "/render/" + render_id,  stream=True, headers=self._api_headers, timeout=self._api_timeout) as r:
      return r.content

  def generate_template_id(self, template_file_name = None, payload = ""):
    if template_file_name is None:
      raise ValueError('Carbone SDK render_report error: argument is missing: template_file_name')
    with open(template_file_name,"rb") as f:
      bytes = f.read() # read entire file as bytes
      h = hashlib.sha256()
      h.update(payload.encode('utf-8'))
      h.update(bytes)
      return h.hexdigest()

  def set_access_token(self, api_token = None):
    if api_token is None:
      raise ValueError('Carbone SDK set_access_token error: argument is missing: api_token')
    self._api_headers["Authorization"] = "Bearer " + api_token

  def set_api_version(self, api_version = None):
    if api_version is None:
      raise ValueError('Carbone SDK set_api_version error: argument is missing: api_version')
    if isinstance(api_version, str):
      self._api_headers["carbone-version"] = api_version
    elif isinstance(api_version, int):
      self._api_headers["carbone-version"] = str(api_version)
    else:
      raise ValueError('Carbone SDK set_api_version error: an argument is invalid: api_version is not a number nor a string')

  def render(self, file_or_template_id = None, json_data = None, payload = ""):
    if file_or_template_id is None:
      raise ValueError('Carbone SDK render error: argument is missing: file_or_template_id')
    if file_or_template_id is None:
      raise ValueError('Carbone SDK render error: argument is missing: json_data')
      return

    resp = None
    # 1 - if file_or_template_id is a template_id => return the result
    if os.path.exists(file_or_template_id) == False:
      resp = self.render_report(file_or_template_id, json_data)
      resp = json.loads(resp.text)
    # 2 - if file_or_template_id
    #   a - generate the template_id and try to render => return the result
    #   b - upload the template => get the template_id => render => return the result



    if resp['success'] == False:
      raise Exception(resp.error)
      return
    if len(resp['data']['renderId']) == 0:
      raise Exception('Carbone SDK render error: render_id empty')
    return self.get_report(resp['data']['renderId'])


# _token = "eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIxNjY3IiwiYXVkIjoiY2FyYm9uZSIsImV4cCI6MjIxNzY3NTMwNSwiZGF0YSI6eyJpZEFjY291bnQiOjE2Njd9fQ.ABf57FFgQVX2nwo9gbYIruE17GNtvWKrWsgL7MP_dvgNEYAW5Kr-i9gXVKEBtHNTRtgr_rLHgnkyn4H-JsE2CqI8AXi-T8WGMR5DWdLn352VuA1xge39g9glZpNLVLVGalAZTp-u2ziZTbqlodtfOGzzZSPQnXCmOApsrHWfRhnLyfJX"
_template_id = "cb03f7676ef0fbe5d7824a64676166ac2c7c789d9e6da5b7c0c46794911ee7a7"

# CSDK = CarboneSDK(_token)
CSDK = CarboneSDK()

json_data = {}
json_data["data"] = {
  "firstname": "John",
  "lastname": "Wick"
}
json_data["convertTo"] = "odt"
resp = CSDK.render("cb03f7676ef0fbe5d7824a64676166ac2c7c789d9e6da5b7c0c46794911ee7a7", json_data)
print(resp)

# ADD TEMPLATE
# try:
#   resp = CSDK.add_template('./tests/template.test.odt', 'salt1234')
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