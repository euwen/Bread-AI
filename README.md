## Overview
* Bread-AI is a pure-Python chatbot with artificial intelligence, based on WeChat platform, to help people live better. 

## Folder explain
* console.py: The console of Bread-AI for testing on the terminal.
* core/: Contains the core code of Bread-AI
* data/: Contains the data of Bread-AI
* run.sh: The main running script
* server/: The Django code work for WeChat platform

## Quick start
* Make sure you have installed python3, django, pyaml and pydblite.
* Run console.py to talk with Bread-AI.

## How to connect to WeChat platform
* Edit server/server/settings.py, add your public ip address to ALLOWED_HOSTS, For example:
>ALLOWED_HOSTS = [
>    '11.75.120.83',
>]
* Add your public ip address and port number to run.sh, and make sure your port is open to the public network, then execute run.sh to start the Django server.
* Login https://mp.weixin.qq.com/, finish connecting to your server.

## How to add super user
* Super user could get more server.
* Edit server/wechat/views.py, add the wechat user id to super_users in _is_super() function.
* Where to get your wechat user id? Just check the post message then you will find it.

## Extra functions
* Enter "help" to see this functions' explaination.
* Tip: your should install "sdcv" before you can use the dictionary function.

## How to add data
* the data source files are yaml files stored in the data/yml folder.
* There're 3 folders in yml: dia_yml, nom_yml, sec_yml.
 * dia_yml: used for dialogue, there is already a file in the folder, watch it.
 * nom_yml: used to store public content which everyone could see.
 * sec_yml: used to store private content which only super user could see.
* After add yaml files in yml folder, execute insert_data.py to insert this yaml files to database that store in the db folder.

## To know more
* Author: Mark Young
* Email: ideamark@qq.com
