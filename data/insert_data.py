#!/usr/bin/env python3
import os,sys
import re
import yaml
import pydblite

def insert_to_db(db_name, data_dir):
    # Init database
    db = pydblite.Base(db_name)
    if db.exists():
        os.remove(db_name)
    db.create('question', 'answer')
    # Read the yml files
    data_file_list = os.listdir(data_dir)
    for data_file in data_file_list:
        # Check the extension
        if os.path.splitext(data_file)[1] != '.yml': continue
        print('Reading %s and insert data...' % data_file)
        f = open(data_dir+data_file, 'r')
        data = f.read().split('\n\n')
        # Insert the data into database
        try:
            for d in data:
                dd = yaml.load(d)
                if not dd: continue
                for q in dd['question']:
                    db.insert(question = q, answer = dd['answer'])
                    #print('question = ', q, 'answer = ', dd['answer'])
        except:
            raise
    db.create_index('question')
    print(db_name, ' data insert OK!')

if __name__ == '__main__':
    insert_to_db(r'./db/nom_db_1', r'./yml/nom_yml/')
    insert_to_db(r'./db/dia_db_1', r'./yml/dia_yml/')
    insert_to_db(r'./db/sec_db_1', r'./yml/sec_yml/')
