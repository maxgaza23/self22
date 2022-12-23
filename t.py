# -*- coding: utf-8 -*-
from MAX import *
from CyberTKAPI.api import API
import time, random
import sys, json, codecs
import threading, glob, re
import string, os, requests, subprocess
import ast, pytz
import urllib.request, urllib.parse, urllib.error, urllib.parse

settingsOpen = codecs.open("71.json","r","utf-8")
settings = json.load(settingsOpen)

apiKey = "LosAngeles"
version = "v2"
app = "DESKTOPWIN\t7.5.0\tWindows\t10\t20H"
uagnt = "Mozilla/5.0 (X11; CrOS x86_64 14268.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.111 Safari/537.36"

a = API(apiKey,version)
qrResult = a._lineqr(app,uagnt)

print(f'QRCode Image: {qrResult["QrImage"]}')
#print(f'QR: {qrResult["QR"]}')

pinResult = a._linepin(qrResult['Key'],qrResult['Session'],app,uagnt)
print(f'Pincode: {pinResult["Pincode"]}')

authResult = a._lineauthToken(qrResult['Key'],qrResult['Session'],app,uagnt)
authToken,certificate = authResult["authToken"],authResult["Certificate"]
tokenyr = authToken   
cline = LINE(tokenyr)

oepoll = OEPoll(cline)

def logError(text):
    cline.log("ERROR:" + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))


def exceBot(op):
    try:
        if op.type == 0:return
        if op.type == 25:
           print('SENDM ESSAGE [ 25 ] ')
           msg = op.message
           text = msg.text
           to = msg.to
           sender = msg._from
           if msg.toType == 0:
               if sender != cline.profile.mid:
                  to = sender
               else:to = receiver
           else:to = receiver
           if msg.contentType == 0:
              if text is None:return
              if text.lower() == 'test':
                 cline.sendMessage(to,'5555')
           

while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                exceBot(op)
                oepoll.setRevision(op.revision)
    except KeyboardInterrupt:
        sys.exit()