import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir,"carbone_sdk"))
import carbone_sdk
import pytest
import requests_mock
import requests
import json
import os
import time

@pytest.fixture
def csdk():
  return carbone_sdk.CarboneSDK("Token")

class TestInitSDK:
  def test_sdk_default_values(self, csdk):
    assert csdk._api_headers["Authorization"] == "Bearer Token"
    assert csdk._api_headers["carbone-version"] == "3"
    assert csdk._api_url == "https://render.carbone.io"

  def test_init_sdk_error_missing_token(self):
    with pytest.raises(Exception) as e:
      c = carbone_sdk.CarboneSDK()
    assert e.value.args[0] == 'CarboneSDK: "API access token" is missing'

  def test_simple_mock_http_request(self, csdk, requests_mock):
    requests_mock.get(csdk._api_url + "/path", text="content")
    resp = requests.get(csdk._api_url + "/path")
    assert resp.text == "content"
    assert resp.status_code == 200

  def test_set_access_token(self, csdk):
    new_token = "ThisIsANewToken"
    csdk.set_access_token(new_token)
    assert csdk._api_headers["Authorization"] == "Bearer " + new_token

  def test_set_access_token_error_missing_token(self, csdk):
    with pytest.raises(ValueError) as e:
      csdk.set_access_token()
    assert e.value.args[0] == 'Carbone SDK set_access_token error: argument is missing: api_token'

  def test_set_api_version_int(self, csdk):
    new_version = 2
    csdk.set_api_version(new_version)
    assert csdk._api_headers["carbone-version"] == str(new_version)

  def test_set_api_version_string(self, csdk):
    new_version = "2"
    csdk.set_api_version(new_version)
    assert csdk._api_headers["carbone-version"] == new_version

  def test_set_api_version_error_missing_version(self, csdk):
    with pytest.raises(ValueError) as e:
      csdk.set_api_version()
    assert e.value.args[0] == 'Carbone SDK set_api_version error: argument is missing: api_version'

class TestRender:
  def test_render_a_report_error_file_missing(self, csdk):
    with pytest.raises(ValueError) as e:
      csdk.render()
    assert e.value.args[0] == 'Carbone SDK render error: argument is missing: file_or_template_id'

  def test_render_a_report_error_json_data_missing(self, csdk):
    with pytest.raises(ValueError) as e:
      csdk.render("template_id")
    assert e.value.args[0] == 'Carbone SDK render error: argument is missing: json_data'

  def test_render_a_report_error_from_a_non_existing_template_id(self, csdk, requests_mock):
    fake_template_id = "ThisTemplateIdDoesNotExist"
    requests_mock.post(csdk._api_url + "/render/" + fake_template_id , json={'success': False, 'error': 'Error while rendering template Error: 404 Not Found'})
    with pytest.raises(Exception) as e:
      csdk.render(fake_template_id, {"data": {"firstname": "john", "lastname": "wick"}})
    assert e.value.args[0] == 'Carbone SDK render error: Error while rendering template Error: 404 Not Found'

  def test_render_a_report_error_from_a_directory(self, csdk, requests_mock):
    fake_template_id = "./tests"
    requests_mock.post(csdk._api_url + "/render/" + fake_template_id , json={'success': False, 'error': 'Error while rendering template Error: 404 Not Found'})
    with pytest.raises(Exception) as e:
      csdk.render(fake_template_id, {"data": {"firstname": "john", "lastname": "wick"}})
    assert e.value.args[0] == 'Carbone SDK render error: failled to generate the template id'

  def test_render_a_report_from_an_existing_template_id(self, csdk, requests_mock):
    template_id = "0545253258577a632a99065f0572720225f5165cc43db9515e9cef0e17b40114"
    expected_report_name = "DGW298DWIU28939DOWIJ.odt"
    # Request to post the render the report
    render_id="MTAuMjAuMjEuMTAgICAg01E98H4R7PMC2H6XSE5Z6J8XYQ.odt"
    requests_mock.post(csdk._api_url + "/render/" + template_id , json={'success': True, 'data': {'renderId': render_id, 'inputFileExtension': 'odt'}})
    # Request to get the report
    filename = os.path.join(os.path.dirname(__file__), 'template.test.odt')
    file_data = open(filename, "rb")
    requests_mock.get(csdk._api_url + "/render/" + render_id , body=file_data, headers={'content-disposition': 'filename="'+expected_report_name+'"'})
    # Call the function
    resp, unique_report_name = csdk.render(template_id, {"data": {"firstname": "john", "lastname": "wick"}})
    file_data = open(filename, "rb")
    assert file_data.read() == resp
    assert expected_report_name == unique_report_name

  def test_render_from_a_template_already_uploaded(self, csdk, requests_mock):
    file_name = "template.test.html"
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    template_id="75256dd5c260cdf039ae807d3a007e78791e2d8963ea1aa6aff87ba03074df7f"
    render_id="MTAuMjAuMjEuMTAgICAg01E98H4R7PMC2H6XSE5Z6J8XYQ.odt"
    expected_report_name = "DGW298DWIU28939DOWIJ2322EWFEW.odt"
    # mock render report
    requests_mock.post(csdk._api_url + "/render/" + template_id , json={'success': True, 'data': {'renderId': render_id, 'inputFileExtension': 'html'}})
    # mock request to get the report
    file_data = open(file_path, "rb")
    requests_mock.get(csdk._api_url + "/render/" + render_id , body=file_data, headers={'content-disposition': 'filename="'+expected_report_name+'"'})
    # Call the function
    resp, unique_report_name = csdk.render(file_path, {"data": {"firstname": "john", "lastname": "wick"}})
    file_data = open(file_path, "rb")
    assert file_data.read() == resp
    assert unique_report_name == expected_report_name

  def test_render_a_report_from_a_new_template(self, csdk, requests_mock):
    expected_report_name = "DGW298DWIU28939DOWIJ2322EWFEW.html"
    # Creating the temporary template
    time_str = str(time.time())
    content_template = "<!DOCTYPE html><html><body> {d.name} date:" + time_str + "</body></html>"
    file_name = "template." + time_str + ".tmp.html"
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    fd = open(file_path, "w")
    fd.write(content_template)
    fd.close()
    template_id = csdk.generate_template_id(file_path)
    # # register mock add template
    requests_mock.post(csdk._api_url + "/template", json={"success": True, "data": {"templateId": template_id}})
    # register mock render report
    render_id = 'MTAuMjAuMjEuMTAgICAg01E98H4R7PMC2H6XSE5Z6J8XYQ.html'
    render_resp_1 = {"success": False, "error": "Error while rendering template Error: 404 Not Found"}
    render_resp_2 = {'success': True, 'data': {'renderId': render_id, 'inputFileExtension': 'html'}}
    requests_mock.register_uri("POST", csdk._api_url + "/render/" + template_id, [{'json': render_resp_1, 'status_code': 300}, {'json': render_resp_2, 'status_code': 200}])
    # register the mock request to get the report
    file_data = open(file_path, "rb")
    requests_mock.get(csdk._api_url + "/render/" + render_id , body=file_data, headers={'content-disposition': 'filename="'+expected_report_name+'"'})
    # Call the function
    resp, unique_report_name = csdk.render(file_path, {"data": {"name": "john"}})
    file_data = open(file_path, "rb")
    assert file_data.read() == resp
    assert unique_report_name == expected_report_name
    try:
      os.remove(file_path)
    except Exception:
      print("Can't remove the tmp template.")


class TestAddTemplate:
  def test_add_template(self, csdk, requests_mock):
    expected_result = {"success": True, "data": {"templateId": "0545253258577a632a99065f0572720225f5165cc43db9515e9cef0e17b40114"}}
    requests_mock.post(csdk._api_url + "/template", json=expected_result)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'template.test.odt')
    resp = csdk.add_template(filename)
    assert resp == expected_result

  def test_add_template_with_payload(self, csdk, requests_mock):
    expected_result = {"success": True, "data": {"templateId": "cb03f7676ef0fbe5d7824a64676166ac2c7c789d9e6da5b7c0c46794911ee7a7"}}
    requests_mock.post(csdk._api_url + "/template", json=expected_result)
    filename = os.path.join(os.path.dirname(__file__), 'template.test.odt')
    resp = csdk.add_template(filename, "salt1234")
    assert resp == expected_result

  def test_add_template_error_missing_args(self, csdk):
    with pytest.raises(ValueError) as e:
      csdk.add_template()
    assert e.value.args[0] == 'CarboneSDK: add_template method: the argument template_file_name is missing'

  def test_add_template_error_with_a_non_existing_file(self, csdk):
    with pytest.raises(FileNotFoundError):
      csdk.add_template("ShouldThrowAnError")

  def test_add_template_error_with_directory(self, csdk):
    with pytest.raises(IsADirectoryError):
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
      csdk.get_template()
    assert e.value.args[0] == 'Carbone SDK get_template error: argument is missing: template_id'

class TestDeleteTemplate:
  def test_delete_template(self, csdk, requests_mock):
    tid = "foiejwoi21e093ru3209jf2093j"
    expected_result = {"success": True, "error": None}
    requests_mock.delete(csdk._api_url + "/template/" + tid , json=expected_result)
    resp = csdk.delete_template(tid)
    assert resp == expected_result

  def test_delete_template_error_already_deleted(self, csdk, requests_mock):
    tid = "foiejwoi21e093ru3209jf2093j"
    expected_result = {"success": False, "error": "Error: Cannot remove template, does it exist ?"}
    requests_mock.delete(csdk._api_url + "/template/" + tid , json=expected_result)
    resp = csdk.delete_template(tid)
    assert resp == expected_result

  def test_delete_template_error_missing_template_id(self, csdk):
    with pytest.raises(ValueError) as e:
      csdk.delete_template()
    assert e.value.args[0] == 'Carbone SDK delete_template error: argument is missing: template_id'

class TestRenderReport:
  def test_render_report(self, csdk, requests_mock):
    template_id = "foiejwoi21e093ru3209jf2093j"
    # mock
    expected_result = {'success': True, 'data': {'renderId': 'MTAuMjAuMjEuMTAgICAg01E98H4R7PMC2H6XSE5Z6J8XYQ.odt', 'inputFileExtension': 'odt'}}
    requests_mock.post(csdk._api_url + "/render/" + template_id , json=expected_result)
    # request
    template_data = {}
    template_data["data"] = {
      "firstname": "John",
      "lastname": "Wick"
    }
    template_data["convertTo"] = "odt"
    resp = csdk.render_report(template_id, template_data)
    assert resp == expected_result

  def test_render_report_error_missing_template_id(self, csdk):
    with pytest.raises(ValueError) as e:
      csdk.render_report()
    assert e.value.args[0] == 'Carbone SDK render_report error: argument is missing: template_id'

  def test_render_report_error_missing_json_data(self, csdk):
    with pytest.raises(ValueError) as e:
      csdk.render_report("template_id")
    assert e.value.args[0] == 'Carbone SDK render_report error: argument is missing: json_data'

class TestGetReport:
  def test_get_report(self, csdk, requests_mock):
    render_id = "0545253258577a632a99065f0572720225f5165cc43db9515e9cef0e17b40114.odt"
    filename = os.path.join(os.path.dirname(__file__), 'template.test.html')
    expected_report_name = "01EEYYHV0ENQE07JCKW8BD2QRP.odt"
    content_disposition = 'filename="'+expected_report_name+'"'
    file_data = open(filename, "rb")

    requests_mock.get(csdk._api_url + "/render/" + render_id, body=file_data, headers={'content-disposition': content_disposition})
    resp, report_name = csdk.get_report(render_id)
    file_data = open(filename, "rb")
    assert file_data.read() == resp
    assert report_name == expected_report_name

  def test_get_report_error_missing_render_id(self, csdk):
    with pytest.raises(ValueError) as e:
      csdk.get_report()
    assert e.value.args[0] == 'Carbone SDK get_report error: argument is missing: render_id'

class TestGenerateTemplateID:
  def test_generate_template_id_odt_1(self, csdk):
    filename_odt = os.path.join(os.path.dirname(__file__), 'template.test.odt')
    res = csdk.generate_template_id(filename_odt)
    assert res == "0545253258577a632a99065f0572720225f5165cc43db9515e9cef0e17b40114"

  def test_generate_template_id_odt_2_payload_1(self, csdk):
    filename_odt = os.path.join(os.path.dirname(__file__), 'template.test.odt')
    res = csdk.generate_template_id(filename_odt, "ThisIsAPayload")
    assert res == "7de8d1d8676abb32291ea5119cb1f78fe37fdfdc75332fcdae28f1e30d064ac0"

  def test_generate_template_id_odt_3_payload_2(self, csdk):
    filename_odt = os.path.join(os.path.dirname(__file__), 'template.test.odt')
    res = csdk.generate_template_id(filename_odt, "8B5PmafbjdRqHuksjHNw83mvPiGj7WTE")
    assert res == "a62eb407a5d5765ddf974636de8ab47bda7915cebd61197d7a2bb42ae70ffcd6"

  def test_generate_template_id_html_1(self, csdk):
    filename_html = os.path.join(os.path.dirname(__file__), 'template.test.html')
    res = csdk.generate_template_id(filename_html)
    assert res == "75256dd5c260cdf039ae807d3a007e78791e2d8963ea1aa6aff87ba03074df7f"

  def test_generate_template_id_html_2_payload_1(self, csdk):
    filename_html = os.path.join(os.path.dirname(__file__), 'template.test.html')
    res = csdk.generate_template_id(filename_html, "This is a long payload with different characters 1 *5 &*9 %$ 3%&@9 @(( 3992288282 29299 9299929")
    assert res == "70799b421cc9cf75d9112273a8e054c141d484eb8d5988bd006fac83e3990707"

  def test_generate_template_id_error(self, csdk):
    with pytest.raises(ValueError) as e:
      csdk.generate_template_id()
    assert e.value.args[0] == 'Carbone SDK generate_template_id error: argument is missing: template_file_name'

class TestGetReportName:
  def test_get_report_name_from_header(self, csdk):
    expected_report_name = "01EEYYHV0ENQE07JCKW8BD2QRP.odt"
    content_disposition = 'filename="'+expected_report_name+'"'
    headers = {
      'content-disposition': content_disposition
    }
    report_name = csdk.get_report_name_from_header(headers)
    assert report_name == expected_report_name

  def test_get_report_name_from_header_without_double_quotes(self, csdk):
    expected_report_name = "OIEQWJFEWO122312ES.pdf"
    content_disposition = 'filename='+expected_report_name
    headers = {
      'content-disposition': content_disposition
    }
    report_name = csdk.get_report_name_from_header(headers)
    assert report_name == expected_report_name

  def test_get_report_name_from_header_without_content_disposition(self, csdk):
    report_name = csdk.get_report_name_from_header({})
    assert report_name == None

  def test_get_report_name_from_header_without_filename(self, csdk):
    headers = {
      'content-disposition': 'filename'
    }
    report_name = csdk.get_report_name_from_header(headers)
    assert report_name == None
