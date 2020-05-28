# Carbone Render Python SDK

The Carbone Python SDK provides a simple interface to communicate with Carbone Render easily.

## Install the Python SDK

```sh
$ pip install carbone-sdk
```

## Quickstart with the Python SDK

Try the following code to render a report in 10 seconds. Just replace your API key, the template you want to render, and the data object.

```python
import carbone_sdk

csdk = carbone_sdk.CarboneSDK("ACCESS-TOKEN")

template_path = "./path/to/template.odt"
json_data = {
  # Add the data here
  "data": {}
}

# Render and return the report as bytes
report_bytes = csdk.render(template_id, json_data)

# Create the file
fd = open("Report.odt", "wb")
fd.write(report_bytes)
fd.close()
```

## Python SDK API

### CarboneSDK Constructor
```python
import carbone_sdk

# Carbone access token passed as parameter
csdk = carbone_sdk.CarboneSDK("ACCESS-TOKEN")
# Carbone access token passed as environment variable "CARBONE_TOKEN"
csdk = carbone_sdk.CarboneSDK()
```
Constructor to create a new instance of CarboneSDK.
The access token can be pass as an argument or by the environment variable "CARBONE_TOKEN".
To set a new environment variable, use the command:
```bash
$ export CARBONE_TOKEN=your-secret-token
```
Check if it is set by running:
```bash
$ printenv | grep "CARBONE_TOKEN"
```
### Render
```python
def render(self, file_or_template_id = None, json_data = None, payload = "")
```
The render function takes `file_or_template_id` the path of your local file OR a template ID, `json_data` a stringified JSON, and an optional `payload`.

It returns the report as a `bytes`. Carbone engine deletes files that have not been used for a while. By using this method, if your file has been deleted, the SDK will automatically upload it again and return you the result.

When a **template file path** is passed as an argument, the function verifies if the template has been uploaded to render the report. If not, it calls [add_template](#add_template) to upload the template to the server and generate a new template ID. Then it calls [render_report](#render_report) and [get_report](#get_report) to generate the report. If the path does not exist, an error is returned.

When a **template ID** is passed as an argument, the function renders with [render_report](#render_report) then call [get_report](#get_report) to return the report. If the template ID does not exist, an error is returned.

**Example**
```python
import carbone_sdk

csdk = carbone_sdk.CarboneSDK("your_access_token")

template_path = "./templates/invoice.docx"
json_data = {
  # Add the data here
  "data": {
    "firstname": "John",
    "lastname": "Wick",
    "price": 1000
  },
  "convertTo": "pdf"
}

# Render and return the report as bytes
try:
  report_bytes = csdk.render(template_path, json_data)
except Exception as err:
  print("Something went wrong: {0}".format(err))

# Create the file
fd = open("invoice.pdf", "wb")
fd.write(report_bytes)
fd.close()
```

### add_template
```python
def add_template(self, template_file_name = None, payload = "")
```
Add the template to the API and returns the response (that contains a `template_id`).
You can add multiple times the same template and get different template ID thanks to the optional `payload`.

**Example**
```python
import carbone_sdk

csdk = carbone_sdk.CarboneSDK("your_access_token")

try:
  resp = csdk.add_template('./tests/template.test.odt', 'salt1234')
  print("Template ID: " + resp['data']['templateId'])
except Exception as err:
  print("Something went wrong: {0}".format(err))
```
### get_template
```python
def get_template(self, template_id = None)
```

Pass a `template ID` to the function and it returns the template as `bytes`. The template ID must exist otherwise an error is returned by the server.

```python
import carbone_sdk

csdk = carbone_sdk.CarboneSDK("your_access_token")

try:
  f = csdk.get_template("cb03f7676ef0fbe5d7824a64676166ac2c7c789d9e6da5b7c0c46794911ee7a7")
  fd = open("template.odt", "wb")
  fd.write(f)
  fd.close()
except Exception as err:
  print("Something went wrong: {0}".format(err))
```
### delete_template
```python
def delete_template(self, template_id = None)
```
**Example**
```python
import carbone_sdk

csdk = carbone_sdk.CarboneSDK("your_access_token")

try:
  resp = csdk.delete_template("template_id")
  print(resp)
except Exception as err:
  print("Something went wrong: {0}".format(err))
```
### render_report
```python
def render_report(self, template_id = None, json_data = None)
```
Function to render the report from a template ID and a stringified JSON Object with [your data and options](https://carbone.io/api-reference.html#rendering-a-report). It returns the API response. The generated report and link are destroyed one hour after rendering.

**Example**
```python
import carbone_sdk

csdk = carbone_sdk.CarboneSDK("your_access_token")

try:
  template_id = "9910a..."
  json_data = {
    "data": {
      "firstname": "John",
      "lastname": "Wick",
      "price": 1000
    },
    "convertTo": "odt"
  }
  resp = csdk.render_report(template_id, json_data)
  print("Render ID: " + resp['data']['renderId'])
except Exception as err:
  print("Something went wrong: {0}".format(err))
```
### get_report
```python
def get_report(self, render_id = None)
```
Return the Report from a renderID.

**Example**

```python

import carbone_sdk

csdk = carbone_sdk.CarboneSDK("your_access_token")

# replace with your render ID
render_id = "MTAuMjAuMTEuMTEgICAg01E9ANTANYSD20YN1HY4SHC9R5.odt"

try:
  f = csdk.get_report(render_id)
except Exception as err:
  print("Something went wrong: {0}".format(err))

# Create the report
fd = open(render_id, "wb")
fd.write(f)
fd.close()
```
### generate_template_id
```python
def generate_template_id(self, template_file_name = None, payload = "")
```
The Template ID is predictable and idempotent, pass the template path and it will return the `template_id`.
You can get a different template ID thanks to the optional `payload`.


### set_access_token
```python
def set_access_token(self, api_token = None)
```
It sets the Carbone access token.

### set_api_version
```python
def set_api_version(self, api_version = None)
```
It sets the the Carbone version requested. By default, it is calling the version `2` of Carbone.

*Note:* You can only set a major version of carbone.