import os,sys
import re
import core
import pydblite

class brain:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        current_dir_list = current_dir.split('/')
        current_dir_list.pop()
        data_dir = ''
        for dir in current_dir_list:
            data_dir += dir + '/'
        nom_db_1_dir = data_dir +'data/db/nom_db_1'
        sec_db_1_dir = data_dir +'data/db/sec_db_1'
        dia_db_1_dir = data_dir +'data/db/dia_db_1'
        self.nom_db_1 = pydblite.Base(nom_db_1_dir)
        self.sec_db_1 = pydblite.Base(sec_db_1_dir)
        self.dia_db_1 = pydblite.Base(dia_db_1_dir)
        if self.nom_db_1.exists(): self.nom_db_1.open()
        if self.sec_db_1.exists(): self.sec_db_1.open()
        if self.dia_db_1.exists(): self.dia_db_1.open()

    def _init_input(self, input_str):
        # Initialize the input string
        input_str = input_str.lower()
        # Change string to list
        input_str_list = list(input_str)
        right_letters = 'abcdefghijklmnopqrstuvwxyz0123456789 '
        # Check the list
        for i, letter in enumerate(input_str_list):
            if letter in right_letters:
                continue
            else:
                input_str_list[i] = ' '
        # Change list back to string
        input_str = ''
        for letter in input_str_list:
            input_str += letter
        # Delete useless spaces and only left single spaces
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
        result = self.nom_db_1(question = input_str)
        if not result:
            result = self.dia_db_1(question = input_str)
            if not result:
                result = self._find_question(self.nom_db_1, input_str)
            else:
                result = result[0]['answer']
        else:
            result = result[0]['answer']
        return result

    def private_response(self, input_str):
        input_str = self._init_input(input_str)
        result = self.sec_db_1(question = input_str)
        if not result:
            result = self._find_question(self.sec_db_1, input_str)
            if not result:
                result = self.response(input_str)
        else:
            result = result[0]['answer']
        return result

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
            #res = input_str
        if not res:
            res = self.dont_know
        res = core.white_board().check(res)
        return res

    def private_response(self,input_str):
        if re.match(u'^(note|Note) .*$', input_str):
            content = re.sub(u'^(note|Note) ','',input_str)
            res = core.misc.note(content)
        else:
            res = self.response(input_str)
            if res == self.dont_know:
                res = self._bot.private_response(input_str)
        if not res:
            res = self.dont_know
        res = core.white_board().check(res)
        return res
