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
    file_data = open(template_file_name, "rb")
    multipart_form_data = {
      "template": ("template.odt", file_data),
      "payload": (None, payload)
    }
    return requests.post(self._api_url + '/template', files=multipart_form_data, headers=self._api_headers, timeout=self._api_timeout).json()

  def get_template(self, template_id = None):
    if template_id is None:
      raise ValueError('Carbone SDK get_template error: argument is missing: template_id')
    with requests.get(self._api_url + "/template/" + template_id,  stream=True, headers=self._api_headers, timeout=self._api_timeout) as r:
      return r.content

  def delete_template(self, template_id = None):
    if template_id is None:
      raise ValueError('Carbone SDK delete_template error: argument is missing: template_id')
    return requests.delete(self._api_url + "/template/" + template_id, headers=self._api_headers, timeout=self._api_timeout).json()

  def render_report(self, template_id = None, json_data = None):
    if template_id is None:
      raise ValueError('Carbone SDK render_report error: argument is missing: template_id')
    if json_data is None:
      raise ValueError('Carbone SDK render_report error: argument is missing: json_data')
    return requests.post(self._api_url + "/render/" + template_id, json=json_data, headers=self._api_headers, timeout=self._api_timeout).json()

  def get_report(self, render_id = None):
    if render_id is None:
      raise ValueError('Carbone SDK get_report error: argument is missing: render_id')
    with requests.get(self._api_url + "/render/" + render_id,  stream=True, headers=self._api_headers, timeout=self._api_timeout) as r:
      return r.content, self.get_report_name_from_header(r.headers)

  def generate_template_id(self, template_file_name = None, payload = ""):
    if template_file_name is None:
      raise ValueError('Carbone SDK generate_template_id error: argument is missing: template_file_name')
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
    resp = None
    # 1 - if file_or_template_id is a template_id => render from the template_id
    if os.path.exists(file_or_template_id) == False:
      resp = self.render_report(file_or_template_id, json_data)
    # 2 - if file_or_template_id
    else:
      # a - generate the template_id and try to render
      try:
        template_id = self.generate_template_id(file_or_template_id, payload)
      except Exception:
        raise Exception("Carbone SDK render error: failled to generate the template id")
      resp = self.render_report(template_id, json_data)
      # b - if the render fail => upload the template => get the template_id => render
      if resp['success'] == False:
        resp_add_template = self.add_template(file_or_template_id, payload)
        if resp_add_template['success'] == False:
          raise Exception("Carbone SDK render error:" + resp_add_template['error'])
        resp = self.render_report(resp_add_template['data']['templateId'], json_data)
    if resp is None:
      raise Exception('Carbone SDK render error: something went wrong')
    if resp['success'] == False:
      # if RenderReport return one of the following error, it means the template does not exist otherwhise something went wrong.
			# - Error while rendering template Error: ENOENT:File not found
			# - Error while rendering template Error: 404 Not Found
      raise Exception('Carbone SDK render error: ' + resp['error'])

    if len(resp['data']['renderId']) == 0:
      raise Exception('Carbone SDK render error: render_id empty')
    return self.get_report(resp['data']['renderId'])

  def get_report_name_from_header(self, headers):
    content_disposition = headers.get('content-disposition')
    if (content_disposition is None):
      return None
    split_content_disposition = content_disposition.split("=")
    if (len(split_content_disposition) != 2):
     return None
    report_name = split_content_disposition[1]
    if (report_name[0] == '"' and report_name[len(report_name) -1] == '"'):
      report_name = report_name[1:len(report_name)-1]
    return report_name
