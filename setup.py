import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="carbone-sdk",
    version="1.0.7",
    author="CarboneIO",
    author_email="support@carbone.io",
    description="Carbone API Python SDK to generate documents (PDF, docx, xlsx, ods, odt, ...) from a JSON and a template.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carboneio/carbone-sdk-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license='Apache-2.0'
)