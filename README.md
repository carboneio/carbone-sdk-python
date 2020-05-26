
```
$ pip install pytest
$ pip install requests_mock
```

Run all the test:
```shell
$ pytest -v tests
```

Run a groupe of tests:
```shell
$ pytest -v ./tests/test_carbone_sdk.py::TestRender
```

Run a single test:
```shell
$ pytest -v ./tests/test_carbone_sdk.py::TestRender::test_render_a_report_error_file_missing
```

Run a single test with all the DEBUG:
```
$ pytest ./tests/test_carbone_sdk.py::TestRender::test_render_a_report_from_an_existing_template_id --log-cli-level=10
```