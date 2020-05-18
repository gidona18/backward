from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent
README = (HERE / "README.rst").read_text()

setup(
    name="backward",
    version="0.0.1",
    packages=find_packages(exclude=["tests"]),
    description="A small programming language that can deduce new information when given a set of rules and facts.",
    long_description=README,
    url="https://github.com/jellowfish/backward",
    license="Apache-2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points={"console_scripts": ["main=backward.__main__:main"],},
    install_requires=["lark-parser", "protoclass"],
    zip_safe=True,
    author="Armando Herrera",
    author_email="mail@jellowfish.com",
)
