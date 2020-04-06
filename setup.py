from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ctlz",
    version="0.1.0",
    author="Theo Henson",
    author_email="theodorehenson@protonmail.com",
    description="Easy and fast multi-purpose library for Python cli applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tteeoo/ctlz",
    packages=find_packages(),
    # install_requires=[""],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)