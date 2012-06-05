#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
import memo
import memo2

def write_memo_file(fn, memo_items):
    f = open(fn, "wb")
    f.write(struct.pack("B",0x5d))
    f.write(struct.pack("B",len(memo_items)))
    for mi in memo_items:
        #f.write(mi.to_bin_format_data())
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
        #mij = memo.MemoItemSingleSelect(sub[:-1].strip(), sub[-1])
        mij = memo.MemoItemSingleSelect(arr[0], arr[1])
        #print mij.get_type()
        #mij = memo2.JudgeMemoItem(sub[:-1].strip(), sub[-1])
        judges.append(mij)

    f.close()


    write_memo_file("test.memo", judges)

def main():
    import sys

    plan_file = "single_select"

    # if len(sys.argv) == 2:
    #     memo_file = sys.argv[1]

#    print memo_file
#    sys.exit(-1)
    generate_memo_file(plan_file)

if __name__ == '__main__':
	main()