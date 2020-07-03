import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="carbone-sdk",
    version="1.0.0",
    author="Ideolys",
    author_email="support@carbone.io",
    description="Python SDK to use Carbone Render easily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ideolys/carbone-sdk-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)