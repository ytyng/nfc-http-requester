#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import nfc

latest_identifier = None


def connected(tag):
    global latest_identifier
    # IDm, PMM等を出力
    print(f'class={tag.__class__.__name__}, str={tag}, id={tag.identifier.hex()}')
    if tag.identifier == latest_identifier:
        return tag
    else:
        latest_identifier = tag.identifier
    # 内容を16進数で出力する
    print(('  ' + '\n  '.join(tag.dump())))
    if tag.ndef:
        print("NDEF Capabilities:")
        print("  readable  = %s" % ("no", "yes")[tag.ndef.is_readable])
        print("  writeable = %s" % ("no", "yes")[tag.ndef.is_writeable])
        print("  capacity  = %d byte" % tag.ndef.capacity)
        print("  message   = %d byte" % tag.ndef.length)
        if tag.ndef.length > 0:
            print("NDEF Message:")
            for i, record in enumerate(tag.ndef.records):
                print("record", i + 1)
                print("  type =", repr(record.type))
                print("  name =", repr(record.name))
                print("  data =", repr(record.data))
                # response = requests.get("https://repr(record.data)")
                # print(curlify.to_curl(response.request))
    return tag


if __name__ == '__main__':
    # タッチ時のハンドラを設定して待機する
    clf = nfc.ContactlessFrontend('usb')
    while True:
        tag = clf.connect(rdwr={'on-connect': connected})
        if not tag:
            break
        time.sleep(1)
