"""
Fallback setup.py for legacy setuptools installations.

This project now uses pyproject.toml with modern packaging.
Use `uv build` or `pip install .` for development installations.

For legacy setuptools support, run:
    python -m pip install .
"""

from setuptools import setup

setup(
    name="agents-collector-cli",
    version="0.1.0",
    install_requires=[
        "typer>=0.9.0",
        "pyyaml>=6.0",
        "requests>=2.31.0",
        "questionary>=2.0.0",
        "rapidfuzz>=3.0.0",
        "rich>=13.0.0",
    ],
)
