import carbone_sdk
import pytest
import requests_mock
import requests
import json
import os

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
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'template.test.odt')
    print(filename)
    resp = csdk.add_template(filename, "salt1234")
    assert json.loads(resp.text) == expected_result

  def test_add_template_error_missing_args(self, csdk):
    with pytest.raises(ValueError) as e:
      c = csdk.add_template()

  def test_add_template_error_with_a_non_existing_file(self, csdk):
    with pytest.raises(FileNotFoundError) as e:
      c = csdk.add_template("ShouldThrowAnError")

  def test_add_template_error_with_directory(self, csdk):
    with pytest.raises(FileNotFoundError) as e:
      c = csdk.add_template("../tests")



