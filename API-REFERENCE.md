# Python Carbone SDK

The Python Carbone SDK provide an simple interface to communicate with Carbone Render easily.

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
The render function takes `file_or_template_id` the path of your local file OR a templateID, `json_data` a stringified JSON, and an optional `payload`.

It returns the report as a `bytes`. Carbone engine deleted files that have not been used for a while. By using this method, if your file has been deleted, the SDK will automatically upload it again and return you the result.

When a **template file path** is passed as an argument, the function verifies if the template has been uploaded to render the report. If not, it calls `add_template` to upload the template to the server and generate a new template ID. Then it calls `render_report` and `get_report` to generate the report. If the path does not exist, an error is returned.

When a **template ID** is passed as an argument, the function renders with `render_report` then call `get_report` to return the report. If the templateID does not exist, an error is returned.

**Example**
```python
import carbone_sdk

csdk = carbone_sdk.CarboneSDK(_token)

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
