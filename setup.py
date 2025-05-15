from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="World Bank Data",
    version="0.1",
    author="Rahul Srinivas",
    packages=find_packages(),
    install_requires = requirements,
)