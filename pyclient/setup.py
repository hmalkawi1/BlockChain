
'''
Python package setup (used by Dockerfile).
'''

from setuptools import setup, find_packages

setup(
    name='notary-cli',
    version='1.0',
    description='Sawtooth Notary',
    author='Sina Khalili',
    url='https://github.com/sinakhalili/sawtooth-notary',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'colorlog',
        'protobuf',
        'sawtooth-sdk',
        'sawtooth-signing',
        'PyYAML',
    ],
    data_files=[],
    entry_points={
        'console_scripts': [
            'notary = notary_cli:main',
        ]
    })

