from setuptools import find_namespace_packages, setup

setup(
    name="code-repair",
    packages=find_namespace_packages(include=["src.*"]),
)
