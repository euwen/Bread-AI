#!/usr/bin/env python3
import os,sys
import pydblite

class show:

    def __init__(self):
        self.db_dir = r'./db/'
        fileList = os.listdir(self.db_dir)
        print('Select the database you want show')
        for i in range(len(fileList)):
            print('[%d] %s' % (i,fileList[i]))
        num = int(input('input: '))
        self.db_name = fileList[num]

    def show_data(self):
        self.db = pydblite.Base(self.db_dir + self.db_name)
        if self.db.exists(): 
            self.db.open()
        for r in self.db:
            print(r)

if __name__ == '__main__':
    
    show().show_data()
