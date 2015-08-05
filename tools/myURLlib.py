# -*- coding: utf-8 -*-
import urllib2
import socket
import re

def getResponse(url, userAgent = True):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0'
    headers = { 'User-Agent' : user_agent,
               'Referer' : 'http://www.williamlong.infoq/'}
    if userAgent:
        return urllib2.Request(url, headers = headers)
    else:
        return urllib2.Request(url)

def getRawContent(url, timeout = 30):
    rawContent = None
    errormsg = None

    try:
        req = getResponse(url, userAgent = True)
        response = urllib2.urlopen(req, timeout = int(timeout))
        rawContent = response.read()
        # we don't check out the charset unless we should process the page
        # if re.search(r'charset.*?=.*?gb2312', rawContent, re.I):
        #     rawContent = rawContent.decode('gbk')
    except urllib2.HTTPError, e:
        errormsg = 'ERROR from urllib2.HTTPError:\t%s.\t'%str(e) + url
    except socket.timeout, e:
        errormsg = 'ERROR from socket.timeout:\t%s.\t'%str(e) + url
    except urllib2.URLError, e:
        errormsg = 'ERROR from urllib2.URLError:\t%s.\t'%str(e) + url
    except Exception, e:
        errormsg = 'ERROR from Exception:\t%s.\t'%str(e) + url

    return  rawContent, errormsg