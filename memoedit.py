#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
import memo

def write_memo_file(fn, memo_items):
    f = open(fn, "wb")
    f.write(struct.pack("B",0x5d))
    f.write(struct.pack("B",len(memo_items)))
    for mi in memo_items:
        f.write(mi.to_bin_format())

    f.close()

def generate_memo_file(fn):
    f = open(fn)
    lines = f.read().strip()

    judges = []
    subjects = lines.split("\n\n")

    for sub in subjects:
        sub = sub.strip()
        arr = sub.split("\n")
#        mij = memo.MemoItemSingleSelect(sub[:-1].strip(), sub[-1])
        mij = memo.MemoItemSingleSelect(arr[0], arr[1])
        #print mij.get_type()
        judges.append(mij)

    f.close()


    write_memo_file("test.memo", judges)

def main():
	generate_memo_file("single_select")

if __name__ == '__main__':
	main()