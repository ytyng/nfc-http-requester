#!/usr/bin/env python3
import argparse
import datetime
import time
from typing import Optional, Callable
from dataclasses import dataclass
import logging
import requests
import nfc
import uuid

_logger = logging.getLogger('nfc_http_requester')


@dataclass
class NfcHttpRequesterState:
    # 最後にタッチした NFC の ID (7bytes)
    latest_identifier: bytes = b''
    latest_processed_datetime: datetime.datetime = datetime.datetime.now()
    url: str = ''
    user_agent: str = 'nfc-http-requester'
    response_handler: Optional[Callable] = None

    def update_latest_processed_datetime(self):
        self.latest_processed_datetime = datetime.datetime.now()

    def update_latest_processed_datetime_is_old(self):
        return (datetime.datetime.now() - self.latest_processed_datetime
                ).total_seconds() > 30


_state: Optional[NfcHttpRequesterState] = None


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--url', type=str, dest='url', required=True
    )
    parser.add_argument(
        '--frontend-path', type=str, dest='frontend_path',
        required=False, default='usb',
        help='ContactlessFrontend path. default is "usb"'
    )
    parser.add_argument(
        '--user-agent', type=str, dest='user_agent',
        required=False, default='nfc-http-requester',
    )
    return parser.parse_args()


def _get_ndef_records_data(tag) -> list:
    if not tag.ndef or not tag.ndef.is_readable or not tag.ndef.length:
        return []

    def _to_dict(record):
        return {
            'type': record.type,
            'name': record.name,
            'data': record.data.decode('utf-8'),
        }

    return [
        _to_dict(record) for record in tag.ndef.records
    ]


def _request(tag, ndef_data: list):
    transaction_id = uuid.uuid4().hex
    nfc_id = tag.identifier.hex()
    _logger.info(f'transaction:{transaction_id}, nfc_id:{nfc_id}')

    _logger.debug(f'request url: {_state.url}, user-agent:{_state.user_agent}')
    _logger.debug('request tag_data:\n' + '\n'.join(
        [f'  {r}' for r in tag.dump()]))
    _logger.debug('request ndef_data:\n' + '\n'.join(
        [f'  {r}' for r in ndef_data]))

    response = requests.post(
        _state.url,
        headers={
            'User-Agent': _state.user_agent,
        },
        json={
            'identifier': nfc_id,
            'transaction_id': transaction_id,
            'ndef': ndef_data,
        }
    )

    _logger.debug(f'response status:{response.status_code}, '
                  f'headers:{response.headers}')
    _logger.debug(f'response content: {response.content.decode()}')

    _state.update_latest_processed_datetime()

    if _state.response_handler:
        _state.response_handler(response)


def _response_handler(response: requests.Response):
    if not response.ok:
        _logger.warning(f'_response_handler: response is NG. abort')
        return

    data = response.json()
    _logger.info(data)


def on_connected(tag):
    # IDm, PMM等を出力
    _logger.debug(
        f'class={tag.__class__.__name__}, str={tag}, '
        f'id={tag.identifier.hex()}')
    if (
        tag.identifier == _state.latest_identifier and
        not _state.update_latest_processed_datetime_is_old()
    ):
        # 最後にタッチした NFC と同じ ID で、かつ、30秒以内の場合、処理をしない
        return tag
    else:
        _state.latest_identifier = tag.identifier

    _request(tag, _get_ndef_records_data(tag))

    return tag


def setup_logger():
    _logger.setLevel(logging.DEBUG)
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter(
        '%(asctime)s %(thread)d %(name)s %(levelname)s %(message)s'
    ))
    _logger.addHandler(_handler)


def main():
    setup_logger()
    args = _parse_arguments()

    global _state
    _state = NfcHttpRequesterState(
        url=args.url,
        user_agent=args.user_agent,
        response_handler=_response_handler,
    )

    # タッチ時のハンドラを設定して待機する
    clf = nfc.ContactlessFrontend(args.frontend_path)
    while True:
        tag = clf.connect(rdwr={'on-connect': on_connected})
        if not tag:
            break
        time.sleep(1)


if __name__ == '__main__':
    main()
