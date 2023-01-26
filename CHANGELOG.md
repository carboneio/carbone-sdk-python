### v1.0.7
  - Fix install script  https://github.com/carboneio/carbone-sdk-python/issues/7
  - Add function `get_status` to get the Carbone API status

### v1.0.6
  - Update to Carbone version 4
  - Set default request timeout to 60s

### v1.0.5
  - Fix "add_template": Add the template mime-type to the form-data

### v1.0.4
  - Update to Carbone version 3
  - Add examples on the documentation

### v1.0.3
  - Fix #2 - render function: check if the json argument is empty

### v1.0.2
  - Add license and update setup

### v1.0.1
  - **Breaking changes**: the `render` method returns a tuple of 2 elements: the generated report as bytes and a unique report name.
    for example before:
    ```python
    report_bytes = csdk.render(template_id, json_data)
    ```
    now:
    ```python
    report_bytes, unique_report_name = csdk.render(template_id, json_data)
    ```

### v1.0.0
  - Release July 3rd, 2020
  - It is possible to interact with the Carbone Render API with the following methods:
    - add_template: upload a template and return a templateID
    - get_template: return an uploaded template from a templateID
    - delete_template: delete a template from a templateID
    - render: render a report from a templateID
    - generate_template_id: Pre compute the templateID
