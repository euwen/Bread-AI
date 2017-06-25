from . import bot
from . import misc
import os, re

class white_board():

    def __init__(self):
        self.max_words = 140
        current_dir = os.path.dirname(__file__)
        self.wb_dir = current_dir + r'/white_board.txt'
        self.next_signal = r' ....'
        self.split_signal = r'/// '

    def _erase(self):
        wb = open(self.wb_dir,'w')
        wb.close()
    
    def _split(self,text):
        all_blocks = len(text) // self.max_words
        if len(text) % self.max_words != 0:
            all_blocks += 1
        current_block = 1
        wb = open(self.wb_dir,'w')
        wb.writelines([str(all_blocks)+self.split_signal, str(current_block)+self.split_signal])
        wb.writelines([text[i:i+self.max_words]+self.split_signal for i in range(0,len(text),self.max_words)])
        wb.close()

    def read(self):
        rb = open(self.wb_dir,'r')
        list = rb.read().split(self.split_signal)
        for i in range(len(list)):
            if list[i] == '' or list[i] == '\n':
                del list[i]
                continue
            list[i] += self.split_signal
        rb.close()
        if len(list) > 2:
            all_blocks = int(list[0].replace(self.split_signal,''))
            current_block = int(list[1].replace(self.split_signal,''))
            if current_block < all_blocks:
                res = list[current_block+1] + self.next_signal
                list[1] = str(current_block+1)+self.split_signal
                wb = open(self.wb_dir,'w')
                wb.writelines(list)
                wb.close()
            elif current_block == all_blocks:
                res = list[current_block+1]
                self._erase()
        else:
            res = 'no more'
        return res.replace(self.split_signal,'')

    def check(self,text):  # check if the input string is longer than max value
        if len(text) <= self.max_words or self.next_signal in text:
            return text
        elif 'http://' in text or 'https://' in text:
            return text
        elif re.match(u'[\u4e00-\u9fa5]+', text):
            return text
        else:
            self._split(text)
            return self.read()

