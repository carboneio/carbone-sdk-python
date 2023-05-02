# Carbone Render Python SDK
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/carboneio/carbone-sdk-python?style=for-the-badge&logo=python)](https://pypi.org/project/carbone-sdk)
[![Documentation](https://img.shields.io/badge/documentation-yes-brightgreen.svg?style=for-the-badge)](./API-REFERENCE.md)


Python SDK to use Carbone Render easily.

## About Carbone

Carbone is a powerful document generator (PDF, DOCX, XLSX, ODT, PPTX, ODS, XML, CSV...) using templates and JSON data. It is based on LibreOffice and can convert any document. It is also possible to convert HTML to PDF. Learn more about [supported files and features](https://carbone.io/documentation.html#supported-files-and-features-list).

### 🔖 [API REFERENCE](./API-REFERENCE.md)

## Install

```sh
pip install carbone-sdk
```

## Usage

You can copy and run the code bellow to try.
Get your API token on your Carbone account: https://account.carbone.io/.

```python
import carbone_sdk

# SDK constructor
# The access token can be passed as an argument to the constructor CarboneSDK
# Or by the environment variable "CARBONE_TOKEN", use the command "export CARBONE_TOKEN=secret-token"
csdk = carbone_sdk.CarboneSDK("secret-token")
# Set API version (default : 4)
csdk.set_api_version("4")
# Set API URL for Carbone On-Premise for example (default: "https://api.carbone.io")
csdk.set_api_url("https://api.carbone.io")

# The template ID, it could be an ODT, DOCX, PPTX, XLSX, ODS file, etc...
template_id = "template"
render_options = {
  # REQUIRED: the "data" object contains all the data to inject into the template
  "data": {
    "id": 42,
    "date": 1492012745,
    "company": {
        "name": "myCompany",
        "address": "here",
        "city": "Notfar",
        "postalCode": 123456
    },
    "customer": {
      "name":"myCustomer",
      "address":"there",
      "city":"Faraway",
      "postalCode":654321
    },
    "products":[
      {"name":"product 1","priceUnit":0.1,"quantity":10,"priceTotal":1}
    ],
    "total":140
  },
  # REQUIRED: the "convertTo" attribute defines the format to generate or convert
  "convertTo":"pdf"
  # All rendering options are available on the following API specification:
  # https://carbone.io/api-reference.html#pdf-export-filter-options
}

# Render and return the report as bytes and a unique report name
report_bytes, unique_report_name = csdk.render(template_id, render_options)
fd = open(unique_report_name, "wb")
fd.write(report_bytes)
fd.close()
# voila 🎉
```
## Documentation

- [API REFERENCE](./API-REFERENCE.md)

## Tests

### Tests - Run with Makefile
Install the test packages:
```shell
$ make install
```
To run the tests:
```shell
$ make test
```
To uninstall the test packages:
```shell
$ make uninstall
```

### Tests - Run manually
Install:
```
$ pip install pytest
$ pip install requests_mock
```

To run all the test (-v for verbose output):
```shell
$ pytest -s -v tests
```

To run a groupe of tests:
```shell
$ pytest -s -v ./tests/test_carbone_sdk.py::TestRender
```

To run a single test:
```shell
$ pytest -s -v ./tests/test_carbone_sdk.py::TestRender::test_render_a_report_error_file_missing
```

To run a single test with all the DEBUG:
```
$ pytest ./tests/test_carbone_sdk.py::TestRender::test_render_a_report_from_an_existing_template_id --log-cli-level=10
```
If you need to test the generation of templateId, you can use the nodejs `main.js` to test the sha256 generation.
```bash
$ node ./tests/main.js
```

## 👤 Author

- [**@steevepay**](https://github.com/steevepay)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

Feel free to check [issues page](https://github.com/carboneio/carbone-sdk-python/issues).

## Show your support

Give a ⭐️ if this project helped you!