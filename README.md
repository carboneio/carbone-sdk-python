# Carbone Python SDK

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/carboneio/carbone-sdk-python?style=for-the-badge&logo=python)](https://pypi.org/project/carbone-sdk)
[![Documentation](https://img.shields.io/badge/documentation-yes-brightgreen.svg?style=for-the-badge)](./API-REFERENCE.md)

Generate Documents in Python: Seamless Integration with Carbone API.

## About Carbone

Carbone is a document generator that utilizes Templates and JSON data to create a wide range of file formats, including PDF, DOCX, XLSX, ODT, PPTX, ODS, XML, CSV, and more. With Carbone, you can produce professional, high-quality, rich reports without limitations and streamline document creation processes across all industries:
- **For Organizations**: Effortlessly generate contracts, agreements, invoices, receipts, financial statements, marketing materials, employment contracts, NDAs, training manuals, and compliance documents.
- **For Governments**: Create legislation and regulations, policy documents, budget reports, permits and licenses, public records, certificates, audit reports, and health and safety regulations with ease.
- **For Finance**: Produce budget reports, tax returns, investment portfolios, loan agreements, audit reports, insurance policies, and financial forecasts efficiently.
- **For Health**: Generate medical records, prescriptions, medical certificates, lab reports, and health insurance claims seamlessly.

Learn more about [Carbone](https://carbone.io) and [Supported files and features](https://carbone.io/documentation.html#supported-files-and-features-list).

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

# Generate and return the document as bytes and a unique report name
report_bytes, unique_report_name = csdk.render(template_id, render_options)
fd = open(unique_report_name, "wb")
fd.write(report_bytes)
fd.close()
# voila 🎉
```
## Documentation

- [🔖 API REFERENCE](./API-REFERENCE.md)

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
$ pip install -r requirements.txt
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