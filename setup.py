import re
from setuptools import setup, find_packages

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = ''
with open('fastapi/oauth/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(
    name='fastapi-oauth',
    version=version,
    description='A simple oauth2 package for FastAPI.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Alex Hutz',
    packages=['fastapi.oauth'],
    install_requires=requirements,
)