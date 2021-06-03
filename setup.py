import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="carbone-sdk",
    version="1.0.2",
    author="CarboneIO",
    author_email="support@carbone.io",
    description="Carbone Render Python SDK to generate reports easily (PDF, docx, xlsx, ods, odt, ...) from a JSON",
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