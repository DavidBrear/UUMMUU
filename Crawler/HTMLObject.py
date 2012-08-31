import urllib2;
import socket;
import sgmllib;
import re;
import MySQLdb;
import httplib;
#from htmlentitydefs import name2codepoint as n2cp;
import sys;
import threading;
import time;
from uummuuObjects import *;

#this is an html object which is used to get the html from the remote server
# this object handles all of the GET requests to the server.
class HTMLObject():
    def getHTML(self, site):
        try:
            #set the socket timeout so we don't get hung up looking for one page.
            socket.setdefaulttimeout(10);
            self.url = site;
            self.content_type = '';
            request = urllib2.Request(site);
            #set up the user agent so the server knows who's asking for this page and how to contact us.
            request.add_header("User-agent",  "UUMMUU crawler (Mozilla/5.0 compatible; http://uummuu.com/about/UUMMUUCrawl)");
            self.res = urllib2.urlopen(request);
            self.Found = True;
            self.redirected_url = '';
            try:
                self.content_type = self.res.headers['content-type'].split(';')[0];
                redirect_url = self.res.headers['content-location'];
                self.redirected_url = makeURL(self.res.url, redirect_url);
            except:
                pass;
            self.page = self.res.read();
            return True;
        except urllib2.URLError, e:
            self.Found = False;
            self.page = '';
            return False;
            
    def getPage(self):
        return self.page;

    def __str__(self):
        return self.page;
