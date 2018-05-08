# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 11:38:58 2014

@author: zzhang
"""
import pickle


class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = []
        self.index = {}
        self.total_msgs = 0
        self.total_words = 0

    def get_total_words(self):
        return self.total_words

    def get_msg_size(self):
        return self.total_msgs

    def get_msg(self, n):
        return self.msgs[n]

    # implement
    def add_msg(self, m):
        self.msgs.append(m)
        self.total_msgs += 1

    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.total_msgs - 1
        self.indexing(m, line_at)


    # implement
    def indexing(self, m, l):
        words = m.strip().split()
        self.total_words += len(words)
        if len(words) != 1:
            for i in range(len(words)):
                words[i] = self.replace_punctuation_with_space(words[i])
        for i in words:
            try:
                self.index[i].append(l)
            except:
                self.index[i] = [l]

    def replace_punctuation_with_space(self, content):
        l_punc = ['~', '!', '@', '#', '$', '%'] + \
                 ['^', '&', '*', '(', '{', '[', ']', '}', ')'] + \
                 [':', ';', '"', "'", '<', '>', ',', '.', '?'] + \
                 ['/', "|", '......', '...']

        for item in l_punc:
            content = content.replace(item, '')

        return content

    # implement: query interface
    '''
    return a list of tuple. if index the first sonnet (p1.txt), then
    call this function with term 'thy' will return the following:
    [(7, " Feed'st thy light's flame with self-substantial fuel,"),
     (9, ' Thy self thy foe, to thy sweet self too cruel:'),
     (9, ' Thy self thy foe, to thy sweet self too cruel:'),
     (12, ' Within thine own bud buriest thy content,')]

    '''

    def search(self, term):
        msgs = []
        # for i in range(self.get_msg_size()):
        #     index = self.get_msg(i).find(term)
        #     count = 0
        #     while index != -1:
        #         count += 1
        #         index = self.get_msg(i).find(term, index + 1)
        #     for j in range(count):
        #         msgs.append((i, self.get_msg(i)))
        # print(self.index)

        key_words = term.split()
        index = [[] for i in range(len(key_words))]
        try:
            for i in range(len(key_words)):
                for j in self.index[key_words[i]]:
                    if len(index[i]) == 0:
                        index[i].append(j)
                    else:
                        if j != index[i][-1]:
                            index[i].append(j)
        except:
            return "This word doesn't exist."
        common_index = []
        result_index = []
        for i in index:
            common_index.extend(i)
        for i in common_index:
            if common_index.count(i) == len(key_words) and i not in result_index:
                result_index.append(i)
        for i in result_index:
            if term in self.get_msg(i):
                msgs.append(self.get_msg(i) + "\n")

        return msgs


class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        # print(self.int2roman)
        self.load_poems()

        # implement: 1) open the file for read, then call
        # the base class's add_msg_and_index

    def load_poems(self):
        file = open(self.name, "r")
        content = file.readlines()
        for i in content:
            self.add_msg_and_index(i.strip())

        # implement: p is an integer, get_poem(1) returns a list,
        # each item is one line of the 1st sonnet

    def get_poem(self, p):
        poem = []
        number = self.int2roman[p] + "."
        next_number = self.int2roman[p + 1] + "."
        print(self.index[number])
        index1 = self.index[number][0]
        index2 = self.index[next_number][0]
        for i in range(index1 + 1, index2):
            if self.msgs[i] != " " and self.get_msg(i) != "":
                poem.append(self.get_msg(i))
        return poem


if __name__ == "__main__":
    # sonnets = PIndex("AllSonnets.txt")
    # # the next two lines are just for testing
    # p3 = sonnets.get_poem(3)
    # print(p3)
    # s_love = sonnets.search("five hundred")
    # print(s_love)
    c = Index("ethan")
    c.add_msg_and_index("hi man")
    print(c.index)
    print(c.search("hi"))
