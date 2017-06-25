# This is the core function of Bread

import os
import sys
import re
import core
import pydblite
import random

class brain:

    def __init__(self):
        cur_dir = os.path.dirname(__file__)
        cur_dir_list = cur_dir.split('/')
        cur_dir_list.pop()
        data_dir = '/'.join(cur_dir_list)
        nom_db_dir = data_dir + r'/data/db/nom_db'
        sec_db_dir = data_dir + r'/data/db/sec_db'
        dia_db_dir = data_dir + r'/data/db/dia_db'
        self.nom_db = pydblite.Base(nom_db_dir)
        self.sec_db = pydblite.Base(sec_db_dir)
        self.dia_db = pydblite.Base(dia_db_dir)
        if self.nom_db.exists(): self.nom_db.open()
        if self.sec_db.exists(): self.sec_db.open()
        if self.dia_db.exists(): self.dia_db.open()

    def _init_input(self, input_str):
        input_str = input_str.lower()
        input_str_list = list(input_str)
        right_letters = 'abcdefghijklmnopqrstuvwxyz0123456789 '
        for i, letter in enumerate(input_str_list):
            if letter in right_letters:
                continue
            else:
                input_str_list[i] = ' '
        input_str = ''.join(input_str_list)
        input_str = re.sub(r'\s{2,}',' ',input_str)
        input_str = re.sub(r'(^ +| +$)','',input_str)
        return input_str

    def _find_question(self, db, input_str):
        regex_str = '(^|.* )' + input_str + '( .*|$)'
        result = 'Do you mean:\n'
        for e in db:
            question = e['question']
            if re.match(regex_str, question):
                result += '- ' + question + '\n'
        result = result[:-1]
        if not '\n' in result:
            return None
        else:
            return result

    def response(self, input_str):
        input_str = self._init_input(input_str)
        res = self.nom_db(question=input_str)
        if not res:
            res = self.dia_db(question=input_str)
            if not res:
                res = self._find_question(self.nom_db, input_str)
            else:
                if not res[0]['random']:
                    res = res[0]['answer']
                else:
                    res = res[0]['random']
                    res = res.replace('- ','')
                    res = res.split('\n')
                    res = random.choice(res)
        else:
            res = res[0]['answer']
        return res

    def private_response(self, input_str):
        input_str = self._init_input(input_str)
        res = self.sec_db(question = input_str)
        if not res:
            res = self._find_question(self.sec_db, input_str)
            if not res:
                res = self.response(input_str)
        else:
            res = res[0]['answer']
        return res

class chat:

    def __init__(self):
        self._bot = core.bot.brain()
        self.dont_know = "Sorry, I don't know."

    def response(self,input_str):
        if re.match(u'^s .*$', input_str):
            content = re.sub(u'^s ','',input_str)
            if not len(content):
                res = '[Not Found]'
            else:
                res = core.misc.translate(content)
        elif re.match(u'^d .*$', input_str):
            content = re.sub(u'^d ','',input_str)
            if not len(content):
                res = '[Not Found]'
            else:
                res = core.misc.baiduSearch(content)
        elif re.match(u'^(n|next)$', input_str):
            res = core.white_board().read()
        else:
            for s in input_str:
                if re.match(u'[\u4e00-\u9fa5]', s):
                    return 'Sorry, I speak English only'
            res = self._bot.response(input_str)
        if not res:
            res = self.dont_know
        res = core.white_board().check(res)
        return res

    def private_response(self,input_str):
        res = self.response(input_str)
        if res == self.dont_know:
            res = self._bot.private_response(input_str)
        if not res:
            res = self.dont_know
        res = core.white_board().check(res)
        return res
