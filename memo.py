#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import struct

QA = 0
JUDGE = 2
SINGLESELECT = 1

class NotMemoFile(Exception):
    """docstring for NotMemoFile"""
    pass        

def generate_fmt(q,a):
    fmt = "<BII%ss%ss"
    q_len = len(q)
    a_len = len(a)

    fmt = fmt % (q_len, a_len) 

    return fmt

def generate_test_file():
    f = open("drive.memo","wb")

    head = struct.pack("BB", 0x5D, 2)

    f.write(head)
    
    q = "早饭吃什么"
    a = "豆浆和油条"

    fmt = generate_fmt(q,a)
#    print fmt
#    sys.exit(-1)
    s1 = struct.pack(fmt, QA, len(q), len(a), q, a)

    print fmt

    f2 = open("test","wb")
    f2.write(s1)
    f2.close()
#    sys.exit(0)


    f.write(s1)

    q = "晚饭吃什么"
    a = "小米粥和咸菜"

    fmt = generate_fmt(q,a)
    s2 = struct.pack(fmt, QA, len(q), len(a), q, a)
    f.write(s2)

    f.close()

class MemoItem(object):
    """docstring for MemoItem"""
    def __init__(self, _data):
        super(MemoSelf, self).__init__()

    def get_type(self):
        raise NotImplementedError()

    def vaild(self, vlaue):
        raise NotImplementedError()

    def to_bin_format(self):
        return NotImplementedError()

class MemoItemSingleSelect(object):
    """ 单选 """
    def __init__(self, _subject, _key):
        #super(MenuItemJudge, _data).__init__()
        self.subject = _subject
        self.key = _key
        
    def __str__(self):
        return self.subject
    
    def get_type(self):
        return SINGLESELECT

    def vaild(self, _value):
        if _value == self.key:
            return True
        return False

    def to_bin_format(self):
        fmt = generate_fmt(self.subject, self.key)
        data = struct.pack(fmt, 1, len(self.subject), len(self.key), self.subject, self.key)
        return data


class MenuItemJudge(object):
    """ 判断 """
    def __init__(self, _subject, _key):
        #super(MenuItemJudge, _data).__init__()
        self.subject = _subject
        self.key = _key
        
    def __str__(self):
        return self.subject
    
    def get_type(self):
        return JUDGE

    def vaild(self, _value):
        if _value == self.key:
            return True
        return False

    def to_bin_format(self):
        fmt = generate_fmt(self.subject, self.key)
        data = struct.pack(fmt, 2, len(self.subject), len(self.key), self.subject, self.key)
        return data
        
class MenuItemQA(object):
    """ 问答 """
    def __init__(self, _q, _a):
        super(MenuItemQA, self).__init__()
        self.question = _q
        self.answer = _a

    def get_type(self):
        return QA

    def __str__(self):
        s = "".join(("question:", self.question,"\n","answer:", self.answer))
        return s

    def vaild(self, _answ):
        if _answ == self.answer:
            return True
        return False
    
    def to_bin_format(self):
        fmt = generate_fmt(self.question, self.answer)
        data = struct.pack(fmt, QA, len(self.question), len(answer), self.question, self.answer)
        return data

class Memo(object):
    """ """
    menu_item_classes = { QA : MenuItemQA, JUDGE : MenuItemJudge, 
                   SINGLESELECT : MemoItemSingleSelect }

    def __init__(self):
        super(Memo, self).__init__()
        
        self.judge_list = []
        self.qa_list = []
        self.si_list = []

        self.mi_items = {QA:self.qa_list, JUDGE:self.judge_list, SINGLESELECT:self.si_list}


    def get_count(self):
        return self._count

    def load_memo(self, fn): 
        """ 加载memo文件，通过fn """
        f = open(fn, "rb")
        mh = f.read(2)
        mh = struct.unpack("BB", mh)

        if mh[0] != 0x5D:
            raise NotMemoFile()
            return False



        self._count = mh[1]

        for x in xrange(1,self._count+1):
            item = self._create_memo_item(f)

            print item.get_type()
            self.mi_items[item.get_type()].append(item)

        f.close()

    def _create_memo_item(self, f):
        typ = f.read(1)
        typ = struct.unpack("B", typ)[0]
        
        k_len = f.read(4)
        v_len = f.read(4)

        k_len = struct.unpack("I", k_len)[0]
        v_len = struct.unpack("I", v_len)[0]


        k = struct.unpack((str(k_len)+"s"), f.read(k_len))[0]
        v = struct.unpack((str(v_len)+"s"), f.read(v_len))[0]

        print typ
        print k
        print v

        return Memo.menu_item_classes[typ](k,v)

    def start_judge(self):
        failure = self.judge_list

        print self.judge_list

        while failure != []:
            i = 0
            while i < len(failure):
                print failure[i]
                an = raw_input()
                if failure[i].vaild(an) == True:
                    print "right"
                    del(failure[i])
                i += 1
            print failure

    def start_single_select(self):
        pass

def main():
    memo = Memo()
    memo.load_memo("test.memo")
#    memo.start_judge()

if __name__ == '__main__':
    main()