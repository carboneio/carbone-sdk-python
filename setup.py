import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="carbone-sdk",
    version="1.1.1",
    author="CarboneIO",
    author_email="support@carbone.io",
    description="Carbone API Python SDK to generate documents (PDF DOCX XLSX PPTX CSV XML HTML ODS ODT and more) from a JSON and a template.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carboneio/carbone-sdk-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=3.6',
    license='Apache-2.0',
    install_requires=[
        'requests',
    ]
)