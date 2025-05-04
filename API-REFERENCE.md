# Carbone API Python SDK

The Carbone Python SDK provides a simple interface to communicate with Carbone Cloud API.

## Install the Python SDK

```sh
$ pip install carbone-sdk
```

## Quickstart with the Python SDK

Try the following code to render a report in 10 seconds. Just replace your API key, the template you want to render, and the data object. Get your API key on your Carbone account: https://account.carbone.io/.

```python
import carbone_sdk

csdk = carbone_sdk.CarboneSDK("ACCESS-TOKEN")

template_path = "./path/to/template.odt"
json_data = {
  # Add the data here
  "data": {}
}

# Render and return the report as bytes and a unique report name (for example "01EEYYHV0ENQE07JCKW8BD2QRP.odt")
report_bytes, unique_report_name = csdk.render(template_id, json_data)

# Create the file
fd = open(unique_report_name, "wb")
fd.write(report_bytes)
fd.close()
```

## Python SDK API

### Functions overview

- [CarboneSDK Constructor](#carbonesdk-constructor)
- [Render function](#render)
- [Add a template](#add_template)
- [Delete a template](#delete_template)
- [Get a template](#get_template)
- [Generate template ID](#generate_template_id)
- [Set access token](#set_access_token)
- [Set timeout](#set_timeout)
- [Set API version](#set_api_version)
- [Get API status](#get_status)
- [Webhook Rendering](#webhook-rendering)

### CarboneSDK Constructor
**Definition**
```python
import carbone_sdk

# Carbone access token passed as parameter
csdk = carbone_sdk.CarboneSDK("ACCESS-TOKEN")
# Carbone access token passed as environment variable "CARBONE_TOKEN"
csdk = carbone_sdk.CarboneSDK()
```
Constructor to create a new instance of CarboneSDK.
The access token can be pass as an argument or by the environment variable "CARBONE_TOKEN".
Get your API key on your Carbone account: https://account.carbone.io/.
To set a new environment variable, use the command:
```bash
$ export CARBONE_TOKEN=your-secret-token
```
Check if it is set by running:
```bash
$ printenv | grep "CARBONE_TOKEN"
```
---
### Render
**Definition**
```python
def render(self, file_or_template_id = None, json_data = None, payload = "")
```
The render function takes `file_or_template_id` the path of your local file OR a template ID, `json_data` a stringified JSON, and an optional `payload`.

It returns the report as a `bytes` and a unique report name as a `string`. Carbone engine deletes files that have not been used for a while. By using this method, if your file has been deleted, the SDK will automatically upload it again and return you the result.

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

# Render and return the report as bytes and a unique report name
try:
  report_bytes, unique_report_name = csdk.render(template_path, json_data)
except Exception as err:
  print("Something went wrong: {0}".format(err))

# Create the invoice report
fd = open(unique_report_name, "wb")
fd.write(report_bytes)
fd.close()
```
---
### add_template
**Definition**
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
---
### get_template
**Definition**
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
---
### delete_template

**Definition**

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
---
### generate_template_id
**Definition**
```python
def generate_template_id(self, template_file_name = None, payload = "")
```
The Template ID is predictable and idempotent, pass the template path and it will return the `template_id`.
You can get a different template ID thanks to the optional `payload`.

**Example**
```python
import carbone_sdk

csdk = carbone_sdk.CarboneSDK("your_access_token")

try:
  resp = csdk.generate_template_id("./tests/template.test.odt")
  print(resp) ## Template ID
except Exception as err:
  print("Something went wrong: {0}".format(err))
```

---
### set_access_token
**Definition**
```python
def set_access_token(self, api_token = None)
```
It sets the Carbone access token.

**Example**
```python
import carbone_sdk

csdk = carbone_sdk.CarboneSDK("your_access_token")

try:
  csdk.set_access_token("NEW_CARBONE_RENDER_API_ACCESS_TOKEN")
except Exception as err:
  print("Something went wrong: {0}".format(err))
```

---
### set_api_version
**Definition**
```python
def set_api_version(self, api_version = None)
```
It sets the the Carbone version requested. By default, it is calling the version `5` of Carbone.

*Note:* You can only set a major version of carbone.

**Example**
```python
import carbone_sdk

csdk = carbone_sdk.CarboneSDK("your_access_token")

try:
  csdk.set_api_version("5")
except Exception as err:
  print("Something went wrong: {0}".format(err))
```

---
### set_timeout

Configures the HTTP client timeout for requests made to the Carbone server. The default timeout value is set to 60 seconds, which matches the Carbone Cloud server's default timeout.

If you are generating documents using a Carbone On-Premise server with a custom timeout configuration, you may need to adjust the timeout value accordingly. Increase the timeout value to ensure that the HTTP client waits long enough for the server to process the request.

```python
import carbone_sdk

csdk = carbone_sdk.CarboneSDK("your_access_token")

csdk.set_timeout(120) # = 2 minutes
csdk.set_timeout(300) # = 5 minutes
```

---
### get_status

**Definition**

```python
def get_status()
```

**Example**
```python
import carbone_sdk

csdk = carbone_sdk.CarboneSDK("your_access_token")

try:
  resp = csdk.getStatus()
  # resp["success"] => True / False
  # resp["code"] => 200 / or any HTTP code
  # resp["message"] => "OK" / or an error message
  # resp["version"] => "4.6.7" / Version of Carbone running
except Exception as err:
  print("Something went wrong: {0}".format(err))
```

### Webhook Rendering

**Example**
```python
import carbone_sdk

csdk = carbone_sdk.CarboneSDK("your_access_token")
csdk._api_headers['carbone-webhook-url'] = 'https://custom.webhook/''

try:
  resp = csdk.render_report(templateId, json_data)
  # resp["success"] => True / False
  # resp["message"] => "A render ID will be sent to your callback URL when the document is generated"
except Exception as err:
  print("Something went wrong")
  print(err)
```

