import carbone_sdk
import pytest
import requests_mock
import requests

@pytest.fixture
def csdk():
    return carbone_sdk.CarboneSDK("Token")

class TestInitSDK:
  def test_init_sdk_simple(self):
    c = carbone_sdk.CarboneSDK("Token")
    assert c._api_headers["Authorization"] == "Bearer Token"
    assert c._api_headers["carbone-version"] == "2"
    assert c._api_url == "https://render.carbone.io"

  def test_init_sdk_error_missing_token(self):
    with pytest.raises(Exception) as e:
      c = carbone_sdk.CarboneSDK()

class TestAddTemplate:
  def test_simple_http_request(self, csdk, requests_mock):
    requests_mock.get(csdk._api_url + "/path", text="content")
    assert requests.get(csdk._api_url + "/path").text == "content"
    assert requests.get(csdk._api_url + "/path").status_code == 200

  def test_add_template_simple(self, csdk, requests_mock):
    # requests_mock.get(csdk._api_url + "/template", text="lala")
    resp = csdk.add_template('./template.test.odt')
    print(json.loads(resp.text))


