nfc-http-requester
~~~~~~~~~~~~~~~~~~~

.. image:: https://img.shields.io/pypi/v/nfc-http-requester.svg
    :target: https://pypi.python.org/pypi/nfc-http-requester/
    :alt: Latest PyPI version


Install
-------
::

  python3 -m pip install nfc-http-requester


Usage
-----

Start daemon:

::

  nfc-http-requester --url="https://www.example.com"


What is it
----------

デバイスに接続した NFC カードリーダーにカードをタッチした時、
そのカードの ID と NDEF データを指定した URL に POST 送信します。

社員証を使った出退勤管理システムや、物品貸し出しシステムの
フロントエンドとしての利用を想定しています。

Support devices
---------------

nfcpy を使っているので、nfcpy の対応デバイスが使えます。

https://nfcpy.readthedocs.io/en/latest/overview.html#supported-devices

Sony の RC-S380 などが使用できます。 開発は RC-S380 で行っています。
