#!/usr/bin/env python3
import os
import sys
import re
import yaml
import pydblite
import re

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
        f = open(data_dir+data_file, 'r')
        readStr = f.read()
        readStr = re.sub(r'\n +\n', '\n\n', readStr)
        data = readStr.split('\n\n')
        # Insert the data into database
        try:
            for d in data:
                dd = yaml.load(d)
                print('\n[%s]\n%s' % (data_file, d))
                if not dd: continue
                for q in dd['que']:
                    ans = dd['ans']
                    if type(ans) == bool:
                        print('\n[Error] Bool value\n[%s]\n%s' % (data_file, d))
                        sys.exit(1)
                    db.insert(question=q, answer=ans)
        except:
            raise
    db.create_index('question')
    print(db_name, ' data insert OK!')

if __name__ == '__main__':
    insert_to_db(r'./database/nom.db', r'./yaml/nom/')
    insert_to_db(r'./database/dia.db', r'./yaml/dia/')
    insert_to_db(r'./database/sec.db', r'./yaml/sec/')
    print('\n All Complete!')
