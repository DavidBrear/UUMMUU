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

from StyledObject import StyledObject;



class styleParser():
    
    def __init__(self, full_style=''):
        self.style = re.sub(r'[\n|\t|\r]+', '', full_style);
        self.style = re.sub(r',[\s]*', ',', self.style);
        while self.style.find('/*') >= 0:
            comment_start = self.style.find('/*');
            comment_end = self.style.find('*/', comment_start);
            self.style = self.style[0:comment_start] + self.style[comment_end+2:];
            
        self.comp_styles = dict();
        self.tag_styles = dict();
        self.id_class_styles = dict();
        self.id_styles = dict();
        self.class_styles = dict();
        self.id_specific_styles = dict();
        self.class_specific_styles = dict();
        
        ##set up some default styles that html tags exhibit by default
        ##this includes bold font for <b> and bold/55px font for <h1>
        default_styles = 'body{font-size: 16px; color: #000; font-family:Arial;font-weight:normal; background-color: #FFF;} b {font-weight: bold;} h1 {font-weight: bold; font-size: 55px;}';
        default_styles += 'h2 { font-weight: bold; font-size 38px;}';
        default_styles += 'h3 {font-weight: bold; font-size: 28px;}';
        default_styles += 'h4 {font-weight: bold; font-size: 25px;}';
        default_styles += 'h5 {font-weight: bold; font-size: 21px;}';
        default_styles += 'a {color: #0000FF;}';
        self.add(default_styles, 0);
        
    def get_styles(self, styled_objects):
        pass;
        
    def add(self, style='', priority=0):
        self.style = re.sub(r'[\n|\t|\r]+', '', style);
        self.style = re.sub(r',[\s]*', ',', self.style);
        while self.style.find('/*') >= 0:
            comment_start = self.style.find('/*');
            comment_end = self.style.find('*/', comment_start);
            self.style = self.style[0:comment_start] + self.style[comment_end+2:];
            
        for el in self.style.split("}"):
            try:
                whole_tag, style = el.split('{');
                whole_tag = re.sub("\s[\s]*", " ", whole_tag);
                whole_tag = whole_tag.lstrip().rstrip();
                whole_tag = whole_tag.encode('ascii', 'replace');
                if(re.search('[^ a-z A-Z 0-9 \. \- # \s _ :]', whole_tag)):
                    continue;
            except:
                continue;
            if(re.search(' ', whole_tag)):
                curr_style = self.comp_styles;
                parts = whole_tag.split(' ');
                for part in parts[:0:-1]:
                    try:
                        curr_style = curr_style[part];
                    except:
                        curr_style[part] = dict();
                        curr_style = curr_style[part];
                try:
                    curr_style[parts[0]]['$style'].append_stylesheet(style, priority);
                except:
                    try:
                        curr_style[parts[0]]['$style'] = StyledObject();
                        curr_style[parts[0]]['$style'].append_stylesheet(style, priority);
                    except:
                        curr_style[parts[0]] = dict();
                        curr_style[parts[0]]['$style'] = StyledObject();
                        curr_style[parts[0]]['$style'].append_stylesheet(style, priority);
                    
            else:
                generic_style = self.tag_styles;
                whole_tag = getTagID(whole_tag);
                if(re.search(".*#.*\..*", whole_tag)):
                    generic_style = self.id_class_styles;
                elif(whole_tag[0] =='#'):
                    generic_style = self.id_styles;
                elif (whole_tag[0] == '.'):
                    generic_style = self.class_styles;
                elif(re.search('#', whole_tag)):
                    generic_style = self.id_specific_styles;
                elif(re.search('\.', whole_tag)):
                    generic_style = self.class_specific_styles;
                try:
                    generic_style[whole_tag]['$style'].append_stylesheet(style, priority);
                except:
                    try:
                        generic_style[whole_tag]['$style'] = StyledObject();
                        generic_style[whole_tag]['$style'].append_stylesheet(style, priority);
                    except:
                        generic_style[whole_tag] = dict();
                        generic_style[whole_tag]['$style'] = StyledObject();
                        generic_style[whole_tag]['$style'].append_stylesheet(style, priority);

def getTagID(string):
    '''
        getTagID takes in a string and prints out the string in the order of tag
    '''
    tag = id = cls = '';
    try:
        tag = re.search('([a-zA-Z0-9_\-]*)', string).group();
    except:
        pass;
    try:
        id = re.search('(#[a-zA-Z0-9_\-]*)', string).group();
    except:
        pass;
    try:
        cls = re.search('(\.[a-zA-Z0-9_\-]*)', string).group();
    except:
        pass;
    return tag + id + cls;
