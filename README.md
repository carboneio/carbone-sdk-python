# Carbone Render Python SDK
[![Pypi Package](https://img.shields.io/badge/pypi-1.0.0-brightgreen.svg?cacheSeconds=2592000&logo=python&style=flat-square)](https://pypi.org/project/carbone-sdk)
[![Documentation](https://img.shields.io/badge/documentation-yes-blue.svg?style=flat-square)](https://carbone.io/api-reference.html#carbone-sdk-python)

> Python SDK to use Carbone Render easily.

### 🔖 [API REFERENCE](./API-REFERENCE.md)

## Install

```sh
pip install carbone-sdk
```

## Usage

You can copy and run the code bellow to try.
```python
import carbone_sdk

# SDK constructor
# The access token can be passed as an argument to NewCarboneSDK
# Or by the environment variable "CARBONE_TOKEN", use the command "export CARBONE_TOKEN=secret-token"
csdk = carbone_sdk.CarboneSDK("secret-token")

#  The template ID, it could be a file
template_id = "template"
json_data = {
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
  "convertTo":"pdf"
}

# Render and return the report as bytes
report_bytes = csdk.render(template_id, json_data)
fd = open("Invoice.pdf", "wb")
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
To run all the tests:
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
$ pytest -v tests
```

To run a groupe of tests:
```shell
$ pytest -v ./tests/test_carbone_sdk.py::TestRender
```

To run a single test:
```shell
$ pytest -v ./tests/test_carbone_sdk.py::TestRender::test_render_a_report_error_file_missing
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

Feel free to check [issues page](https://github.com/Ideolys/carbone-sdk-python/issues).

## Show your support

Give a ⭐️ if this project helped you!