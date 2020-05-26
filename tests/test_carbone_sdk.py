import carbone_sdk
import pytest
import requests_mock
import requests
import json
import os
import mimetypes

@pytest.fixture
def csdk():
    return carbone_sdk.CarboneSDK("eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIxNjY3IiwiYXVkIjoiY2FyYm9uZSIsImV4cCI6MjIxNzY3NTMwNSwiZGF0YSI6eyJpZEFjY291bnQiOjE2Njd9fQ.ABf57FFgQVX2nwo9gbYIruE17GNtvWKrWsgL7MP_dvgNEYAW5Kr-i9gXVKEBtHNTRtgr_rLHgnkyn4H-JsE2CqI8AXi-T8WGMR5DWdLn352VuA1xge39g9glZpNLVLVGalAZTp-u2ziZTbqlodtfOGzzZSPQnXCmOApsrHWfRhnLyfJX")

class TestInitSDK:
  def test_init_sdk_simple(self):
    c = carbone_sdk.CarboneSDK("Token")
    assert c._api_headers["Authorization"] == "Bearer Token"
    assert c._api_headers["carbone-version"] == "2"
    assert c._api_url == "https://render.carbone.io"

  def test_init_sdk_error_missing_token(self):
    with pytest.raises(Exception) as e:
      c = carbone_sdk.CarboneSDK()

  def test_simple_http_request(self, csdk, requests_mock):
    requests_mock.get(csdk._api_url + "/path", text="content")
    assert requests.get(csdk._api_url + "/path").text == "content"
    assert requests.get(csdk._api_url + "/path").status_code == 200

class TestAddTemplate:
  def test_add_template(self, csdk, requests_mock):
    expected_result = {"success": True, "data": {"templateId": "0545253258577a632a99065f0572720225f5165cc43db9515e9cef0e17b40114"}}
    requests_mock.post(csdk._api_url + "/template", json=expected_result)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'template.test.odt')
    print(filename)
    resp = csdk.add_template(filename)
    assert json.loads(resp.text) == expected_result

  def test_add_template_with_payload(self, csdk, requests_mock):
    expected_result = {"success": True, "data": {"templateId": "cb03f7676ef0fbe5d7824a64676166ac2c7c789d9e6da5b7c0c46794911ee7a7"}}
    requests_mock.post(csdk._api_url + "/template", json=expected_result)
    filename = os.path.join(os.path.dirname(__file__), 'template.test.odt')
    print(filename)
    resp = csdk.add_template(filename, "salt1234")
    assert json.loads(resp.text) == expected_result

  def test_add_template_error_missing_args(self, csdk):
    with pytest.raises(ValueError) as e:
      csdk.add_template()

  def test_add_template_error_with_a_non_existing_file(self, csdk):
    with pytest.raises(FileNotFoundError) as e:
      csdk.add_template("ShouldThrowAnError")

  def test_add_template_error_with_directory(self, csdk):
    with pytest.raises(FileNotFoundError) as e:
      csdk.add_template("../tests")


class TestGetTemplate:
  def test_get_template(self, csdk, requests_mock):
    _template_id = "0545253258577a632a99065f0572720225f5165cc43db9515e9cef0e17b40114"
    filename = os.path.join(os.path.dirname(__file__), 'template.test.odt')
    file_data = open(filename, "rb")
    requests_mock.get(csdk._api_url + "/template/" + _template_id, body=file_data)
    resp = csdk.get_template(_template_id)
    file_data = open(filename, "rb")
    assert file_data.read() == resp

  def test_get_template_error_missing_template_id(self, csdk):
    with pytest.raises(ValueError) as e:
      csdk.add_template()

class TestDeleteTemplate:
  def test_delete_template(self, csdk, requests_mock):
    tid = "foiejwoi21e093ru3209jf2093j"
    expected_result = {"success": True, "error": None}
    requests_mock.delete(csdk._api_url + "/template/" + tid , json=expected_result)
    resp = csdk.delete_template(tid)
    assert json.loads(resp.text) == expected_result

  def test_delete_template_error_already_deleted(self, csdk, requests_mock):
    tid = "foiejwoi21e093ru3209jf2093j"
    expected_result = {"success": False, "error": "Error: Cannot remove template, does it exist ?"}
    requests_mock.delete(csdk._api_url + "/template/" + tid , json=expected_result)
    resp = csdk.delete_template(tid)
    assert json.loads(resp.text) == expected_result

  def test_delete_template_error_missing_template_id(self, csdk):
    with pytest.raises(ValueError) as e:
      csdk.delete_template()

# {'success': False, 'error': 'Error: Cannot remove template, does it exist ?'}