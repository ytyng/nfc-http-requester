#!/usr/bin/env python3

from setuptools import setup

setup(
    name='nfc-http-requester',
    version='0.0.1',
    description='Send HTTP request when NFC tag is touched.',
    license='BSD',
    author='ytyng',
    author_email='ytyng@live.jp',
    url='https://github.com/ytyng/nfc-http-requester.git',
    keywords='NFC, RC-S380, PaSoRi',
    packages=['nfc_http_requester'],
    entry_points={
        'console_scripts': [
            'nfc-http-requester = '
            'nfc_http_requester.nfc_http_requester:main',
        ]
    },
    install_requires=[
        'nfcpy',
    ],
)
