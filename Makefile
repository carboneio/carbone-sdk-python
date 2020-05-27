install:
	pip install -r requirements.txt

test:
	pytest tests -v

uninstall:
	pip uninstall -r requirements.txt

.PHONY: install test uninstall