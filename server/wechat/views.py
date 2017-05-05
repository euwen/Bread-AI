from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.template import loader, Context
from xml.etree import ElementTree as ET
import time
import hashlib
import socket
import os, sys
sys.path.append('.')
import core

class WeChat(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(WeChat, self).dispatch(*args, **kwargs)
        
    def get(self, request):
        token = 'Mark_Young'
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)

        list = [token,timestamp,nonce]
        list.sort()
        hashcode = ''.join([s for s in list])
        hashcode = hashlib.sha1(hashcode.encode('ascii')).hexdigest()
        if hashcode == signature:
            return HttpResponse(echostr)

    def _is_super(self, name):
        super_users = []
        for user in super_users:
            if user == name:
                return True
        return False

    def post(self, request):
        str_xml = ET.fromstring(request.body)
        fromUser = str_xml.find('FromUserName').text
        toUser = str_xml.find('ToUserName').text
        content = str_xml.find('Content').text
        currentTime = str(int(time.time()))
        if self._is_super(fromUser):
            result = core.bot.chat().private_response(content)
        else:
            result = core.bot.chat().response(content)

        template = loader.get_template('wechat/text_message_template.xml')
        context = Context({'toUser': fromUser, 'fromUser': toUser, 'currentTime': currentTime, 'content': result})
        context_xml = template.render(context)
        #print(context_xml)
        return HttpResponse(context_xml)
