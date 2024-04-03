# setup.py
from setuptools import setup, find_packages

setup(
    name='coderevise',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'coderevise=coderevise.revise:main',
        ],
    },
    install_requires=[
        'appdirs',  # Add other dependencies as needed
    ],
    python_requires='>=3.6',
    description='A CLI tool for managing and revising coding practice questions.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='IoTcat',
    author_email='i@iotcat.me',
    url='https://github.com/iotcat/CodeRevise',
)


