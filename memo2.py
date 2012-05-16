#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct

class NotMemoFileError(Exception):
    pass        

class MemoItemType:
    """ MemoItem's type """
    QA = 0
    SINGLE_SELECT = 1
    JUDGE = 2


class MemoItem(object):
    """ parent of MenuItem. """
    FMT = "<BII%ss%ss"

    def __init__(self, _subject, _answer, _mitype):
        super(MemoItem, self).__init__()
        self.subject = _subject
        self.answer = _answer
        self.mitype = _mitype

    def vaild(self, _answer):
        if _answer.upper() == self.answer:
            return True

    @staticmethod
    def _generate_fmt(_q, _a):
        fmt = MemoItem.FMT
        q_len = len(_q)
        a_len = len(_a)

        fmt = fmt % (q_len, a_len) 
        return fmt

    def get_type(self):
        """ return MemoMemoItemType """
        return self.mitype

    def to_bin_format_data(self):
        fmt = self._generate_fmt(self.subject, self.answer)
        data = struct.pack(fmt, 
                           self.mitype, 
                           len(self.subject), 
                           len(self.answer),
                           self.subject, 
                           self.answer)
        return data

class SingleSelectMemoItem(MemoItem):
    """docstring for MemoItemSingleSelect"""
    CHOOSE_CAST = {0: "A", 1: "B", 2: "C", 3: "D"}

    def __init__(self, _subject, _answer):
        super(SingleSelectMemoItem, self).__init__(_subject, _answer, 
                                                   MemoItemType.SINGLE_SELECT)
        self.subject = _subject
        s = _answer
        #print _answer
        self.chooses = s.split("##")
        #print self.chooses
#        import sys
#        print self.chooses[-1][-3:]
#        sys.exit(-1)
        answ = self.chooses[-1][-3:][-2]
        print answ
        #sys.exit(-1)
        self._answer = answ
        self.chooses[-1] = self.chooses[-1][:-3]

        for i in xrange(0,len(self.chooses)):
            self.chooses[i] = self.chooses[i].replace("#", "")

    def __str__(self):
        s = self.subject
        arr = []

        i = 0
        for ch in self.chooses:
            arr.append("\t")
            arr.append(SingleSelectMemoItem.CHOOSE_CAST[i])
            arr.append(ch)
            arr.append("\n")
            i += 1
        cs = "".join(arr[:-1])

        tostr = "".join((s, "\n", cs))
        return tostr

    def vaild(self, _answer):
#        choose_dic = dict([(v, k) for k , v in CHOOSE_CAST.iteritems() ])
        if _answer.upper() == self.answer:
            print "right"
            return True
        print self.answer
        return False

class QAMemoItem(MemoItem):
    """docstring for QA"""
    def __init__(self, _subject, _answer):
        super(QAMemoItem, self).__init__(_subject, _answer,
                                         MemoItemType.QA)
    def __str__(self):
        s = "".join([self.subject, "\n", "请回答"])
        return s



class JudgeMemoItem(MemoItem): 
    """docstring for Judge"""
    def __init__(self, _subject, _answer):
        super(JudgeMemoItem, self).__init__(_subject, _answer, 
                                                MemoItemType.JUDGE)
    def __str__(self):
        s = "".join([self.subject, "\n", "请输入T或F"])
        return s

memo_class_list = { MemoItemType.JUDGE : JudgeMemoItem, 
                    MemoItemType.QA : QAMemoItem,
                    MemoItemType.SINGLE_SELECT : SingleSelectMemoItem}

class Memo(object):
    """ Memo object """
    LOADFILE = 0
    CREATE_FILE = 1
    MEMO_FLAG = 0x5d
    MEMO_HEAD_FMT = "BB"

    def __init__(self, _init_type, _fn):
        super(Memo, self).__init__()
        self.ss_list = []
        self.judge_list = []
        self.qa_list = []

        self.mi_dict = {MemoItemType.JUDGE : self.judge_list, 
                        MemoItemType.QA : self.qa_list,
                        MemoItemType.SINGLE_SELECT : self.ss_list}

        self.filename = _fn
        if _init_type == Memo.LOADFILE:
            self._load_memo()

    def _load_memo(self):
        _read_memo_head = lambda _f: \
                        struct.unpack(Memo.MEMO_HEAD_FMT, _f.read(2))

        def _read_and_create_memo_item(_f):
            """ read a memo item, if success return (item_type, subject, answ) \
            else return (False, None, None) """
            
            typ = f.read(1)
            typ = struct.unpack("B", typ)[0]
        
            k_len = f.read(4)
            v_len = f.read(4)

            k_len = struct.unpack("I", k_len)[0]
            v_len = struct.unpack("I", v_len)[0]


            k = struct.unpack((str(k_len)+"s"), f.read(k_len))[0]
            v = struct.unpack((str(v_len)+"s"), f.read(v_len))[0]

            # print "k", k
            # print "v", v
            # print "type", typ

            return memo_class_list[typ](k,v)

        f = open(self.filename)
        mh = _read_memo_head(f)
        if mh[0] != Memo.MEMO_FLAG:
            raise NotMemoFileError()
        i = mh[1]

        for x in xrange(0, i):
            item = _read_and_create_memo_item(f)
            self.mi_dict[item.get_type()].append(item)
        f.close()        

    def save():
        pass

    def start_study_judge(self):
        """ start study judge """
        failure = self.judge_list
        #print self.judge_list

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

    def add_memo_item(self, _type, _s, _a):
        """ add memo item to array """

        pass

    def start_study_single_select(self):
        failure = self.ss_list
        while failure != []:
            for i in xrange(0, len(self.ss_list)):
                print failure[i]
                answ = raw_input("请输入选项：")
                if failure[i].vaild(answ):
                    del failure[i]




def main():
    memo = Memo(Memo.LOADFILE, "single_select.memo")
#    memo.start_study_judge()
    memo.start_study_single_select()

if __name__ == '__main__':
    main()