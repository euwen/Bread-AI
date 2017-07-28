:%s/^.*pattern/question/g
:%s/^.*template/answer/g
:%s/  -//g
:%s/"//g
:%s/\\n//g
:%s/ \././g
:%s/^ *toString:.*\n//g
:%s/\n    __text://g
:%s/  / /g
:%s/question: \(.*\)/question: \r- \L\1/g
:%s/^- \n//g
:%s/\n \n/\r\r/g
:%s/ \*//g
:%s/\n *srai: //g
:%s/_ //g
:%s/answer: \n  random: \n   li: /random: |/g
:%s/question: \n.*\nanswer: \n *sr: \n//g
:%s/^.*__text: //g
:%s/^.*_name: //g
:%s/\n\n\n/\r\r/g
:%s/\\//g
:%s/\///g
:%s/^it //g
:%s/ +\././g
:%s/ +,/,/g
:%s/ +?/?/g
:%s/\(^answer: .*\)/\L\1/g
:%s/^answer: \(.\)/answer: \U\1/g
:%s/\(^ - .*\)/\L\1/g
:%s/^ - \(.\)/ - \U\1/g
:%s/ aiml / AIML /g
:%s/aiml /AIML /g
:%s/ aiml/ AIML/g
:%s/ i / I /g
:%s/ i\'/ I'/g
:%s/\(^question: .*\)/\L\1/g
:%s/\(^- .*\)/\L\1/g
:%s/^answer: Yes *$/random: |\r - OK, then\r - Sure\r - Alright/g
:%s/^answer: True *$/random: |\r - OK, then\r - Sure\r - Alright/g
:%s/^answer: No *$/random: |\r - Well\r - So what's next?\r - Alright/g
:%s/^answer: False *$/random: |\r - Well\r - So what's next?\r - Alright/g
