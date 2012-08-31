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

from styleParser import styleParser;
from HTMLObject import HTMLObject;
import uummuuObjects;


'''
    MyThread is a class which extends the Thread class
    I included threads so the style sheets can be retrieved quickly.
'''
class MyThread(threading.Thread):

    def __init__(self):
        self.status = '';
        self.url = '';
        self.myHTML = HTMLObject();
        threading.Thread.__init__(self);
        
    def run(self):
        
        self.myHTML.getHTML(self.url);
        return self.myHTML.page;

    def status_to(self, string):
        self.status = string;

# this object parses out the html from the server to grab the css files
# this object then creates a thread for each style sheet found and gets the style
# this object retains not only a list of the styled object but of the style applied to them
class myParser(sgmllib.SGMLParser):

    def parse(self, s):
        self.feed(s);
        self.close();

    def __init__(self, verbose=0, myurl='', domain=''):
        sgmllib.SGMLParser.__init__(self, verbose);
        self.main_url = myurl;
        self.stylesheet = False;
        self.in_style = False;
        self.inside_title = False;
        self.inside_script = False;
        self.num_stylesheet = 0;
        self.style_href = [];
        self.full_style = '';
        self.curr_thread = 0;
        self.threads = []; # a list to keep track of all the threads retrieving style
        self.style_tag = False;
        self.styled_objects = {};
        self.unnamed_count = 0;
        self.data = '';
        self.this_style = '';
        self.curr_tag = '';
        self.whole_tag = '';
        self.title = '';
        self.url = myurl;
        self.domain = domain;
        #the links on this page.
        self.hyperlinks = [];
        #no follow links
        self.no_follow_links = [];
        self.meta = {};
        #does this page have a meta refresh?
        self.has_meta_refresh = False;
        #what is the meta refresh url?
        self.meta_refresh_url = '';
        #the full text
        self.full_text = "";
        
        self.styleParser = styleParser();
        
        #self.stemmer = PorterStemmer();

    def start_link(self, attributes):
        url = '';
        self.in_style = False;
        media = "screen";
        for name, value in attributes:
            if name.lower() == 'rel' and value.lower() == 'stylesheet':
                if self.stylesheet:
                    self.num_stylesheet += 1;
                else:
                    self.stylesheet = True;
                    self.num_stylesheet = 1;
                self.in_style = True;
            elif name.lower() == 'href':
                url = value;
            elif name.lower() == 'media':
                media = value.lower();
        if self.in_style and media == 'screen':
            self.threads.append(MyThread()); #create a thread
            self.threads[self.curr_thread].url = uummuuObjects.makeURL(self.main_url, url); #assign the thread a .css url to crawl
            self.styleParser.add(self.threads[self.curr_thread].run(), 50); #crawl the css url
            self.curr_thread += 1; #increment the thread counter
        self.in_style = False;
        
    def start_style(self, attributes):
        self.style_tag = True;
        self.setliteral();
        self.this_style = '';
        
    def end_style(self):
        self.style_tag = False;
        self.full_style = self.this_style + self.full_style;
        self.this_style = '';
    def start_br(self, attributes):
        pass;
    def start_meta(self, attributes):
        #we should usually accept meta information
        #it is becoming less and less useful.
        #Maybe in the future this will be taken out.
        #this is just a place for the web master to tell us about the page.
        #we should usually be able to find this from the page itself.
        in_desc = 0;
        in_title = 0;
        for name, value in attributes:
            if name.lower() == 'name' and value.lower()=="description":
                in_desc = 1;
            if name.lower() == 'name' and value.lower()=='title':
                in_title = 1;
            if name.lower() =='value' and in_desc:
                self.meta['description'] = value;
            if name.lower() =='value' and in_title:
                self.meta['title'] = value;
            
            #if this is a meta refresh it should have http-equiv in its name
            if name.lower() == 'http-equiv' and value.lower() == 'refresh':
                #tell that it has a meta refresh
                self.has_meta_refresh = True;
            #if this also has a content and it contains a url to refresh to
            if name.lower() == 'content' and 'url=' in value.lower():
                start_pos = value.lower().find('url=');
                end_pos = value.lower().find(';', start_pos);
                if(end_pos == -1):
                    self.meta_refresh_url = uummuuObjects.makeURL(self.url, value[start_pos+4:]);
                else:
                    self.meta_refresh_url = uummuuObjects.makeURL(self.url, value[start_pos+4:end_pos]);
                    
    def add_to_StyledObjects(self):
        self.data = self.data.lstrip().rstrip();
        if len(self.data) > 0:
            try:
                self.styled_objects[self.whole_tag] += self.data;
            except:
                self.styled_objects[self.whole_tag] = self.data;
            self.data = '';
                
                
    def start_a(self, attributes):
        #we are in a link
        #there are many different types of links
        #we need to make sure to not follow javascript
        #we also need to not follow location tags
        #these are the tags that have a pound sign then just redirect on this page.
        link = '';
        no_follow = False;
        this_id = '';
        this_class = '';
        this_style = '';
        this_has_style = False;
        #make sure to add data to styled objects
        self.add_to_StyledObjects();
        
        for name, value in attributes:
            if name.lower() == 'id':
                this_id = value;
            if name.lower() == 'class':
                this_class = value;
            if name == 'rel':
                if value.lower() == 'nofollow':
                    no_follow = True;
            if name == "href":
                urlName = self.url;
                self.inside_an_element = 1;
                #remove any anchor references
                if(value[0] == '#'):
                    break;
                if(value.find('#') > 0):
                    value = value[:value.find("#")];
                if(value[0:4] == "http"):
                    link = value;
                elif (value[0] == '/'):
                    link = uummuuObjects.makeURL(self.domain, value);
                elif (value == ''):
                    #got an anchor reference...not adding it.
                    pass;
                elif ('javascript:' in value[0:15]):
                    #got a javascript... not adding it.
                    pass;
                elif ('mailto' in value[0:6]):
                    #got a mailto...not adding it
                    pass;
                else:
                    link = uummuuObjects.makeURL(self.url, value);
            elif name.lower() == 'style':
                this_style = value;
                this_has_style = True;
        if(no_follow):
            self.no_follow_links.append(link);
        elif link != '':
            self.hyperlinks.append(link);
        if this_id == '':
            this_id = "#UummuuUnnamed"+str(self.unnamed_count);
            self.unnamed_count += 1;
        self.curr_tag = 'a'+this_id+this_class;
        self.whole_tag = self.whole_tag.lstrip().rstrip() + ' ' + 'a'+this_id+this_class; #set the current tag
        if this_has_style:
            if this_style[-1] != ';':
                this_style += ";";
            self.styleParser.add(self.whole_tag+"{"+this_style+"}", 100);
        
    def start_title(self, attributes):
        #we are inside a title
        self.inside_title = 1;
    def end_title(self):
        #we are outside the title
        self.inside_title = 0;
    def end_a(self):
        self.add_to_StyledObjects();
        #we are no longer in an anchor tag
        self.inside_an_element = 0;
        parts = self.whole_tag.rfind(' a');
        self.whole_tag = self.whole_tag[0:parts];
        second_space = self.whole_tag[0:-1].rfind(' ');
        self.curr_tag = self.whole_tag[second_space:parts];

    def start_script(self, attributes):
        self.inside_script = True;
        
    def end_script(self):
        self.inside_script = False;
        
    def start_noscript(self, attributes):
        pass;
    
    def end_noscript(self):
        pass;
        
    def start_hr(self, attributes):
        pass;
    def end_hr(self):
        pass;
    def start_br(self, attributes):
        pass;
    def end_br(self):
        pass;

    def start_img(self, attributes):
        alt = '';
        this_id = '';
        this_class = '';
        for name,value in attributes:
            if name.lower() == 'alt':
                alt = value;
            elif name.lower() == 'id':
                this_id = '#'+value;
            elif name.lower() == 'class':
                this_class = '.'+value;
        if this_id == '':
            this_id = "#UummuuUnnamed"+str(self.unnamed_count);
            self.unnamed_count += 1;
        self.styled_objects[self.curr_tag + 'img'+this_id+this_class] = alt;
    def end_img(self):
        pass;

    def unknown_starttag(self, tag, attributes):
        if len(self.data) > 0:
            self.add_to_StyledObjects();
        self.curr_tag = tag;
        this_id = ''; #set this id to blank
        this_class = ''; #set this class to blank
        this_style = ''; #set this inline style to blank
        this_has_style = False;
        for name,value in attributes:
            if name.lower() == 'id':
                this_id = '#'+value;
            elif name.lower() == 'class':
                this_class = '.'+value;
            elif name.lower() == 'style':
                this_style = value;
                this_has_style = True;
            elif name.lower()[0:2] == 'on':
                continue;
        if this_has_style and this_id == '':
            this_id = "#UummuuUnnamed"+str(self.unnamed_count);
            self.unnamed_count += 1;
            self.whole_tag = self.whole_tag.lstrip().rstrip() + ' ' + tag + this_id + this_class; #set the current tag
        else:
            self.whole_tag = self.whole_tag.lstrip().rstrip() + ' ' + tag + this_id + this_class; #set the current tag
        if this_has_style:
            if this_style[-1] != ';':
                this_style += ";";
            self.styleParser.add(self.whole_tag+"{"+this_style+"}", 100);

    def unknown_endtag(self, tag):
        if(len(self.data) > 0):
            try:
                self.styled_objects[self.whole_tag] += " " + self.data;
            except:
                self.styled_objects[self.whole_tag] = self.data;
        self.data = '';
        parts = self.whole_tag.rfind(tag);
        self.whole_tag = self.whole_tag[0:parts];
        second_space = self.whole_tag[0:-1].rfind(' ');
        self.curr_tag = self.whole_tag[second_space:parts];

    def handle_entityref(self, ref):
        pass;
        '''
        if ref != 'nbsp':
            self.data = self.data + '&'+ref+';';
        '''

    def handle_data(self, data):
        if self.inside_title:
            self.title = data;
        elif self.inside_script:
            pass;
        elif self.style_tag:
            self.styleParser.add(data, 60);
        else:
            #make sure the regular expressions work in the case that the data is a sole punctuation mark.
            if(len(data) == 1):
                data = data + ' ';
            #remove all non alpha numeric characters
            data = re.sub('([^(a-z 0-9 A-Z \s \- # \$)])+', '', data);
            data = data.replace('\n', '');
            data = data.replace('\r', '');
            data = data.replace('\t', '');
            data = re.sub('(\s)(\s)*', ' ', data);
            if(data == ' '):
                data = '';
            first = True; #set the first switch to true
            for word in data.split(' '):
                try:
                    word = unicode(word, 'ascii');
                except Exception, e:
                    continue;
                #word = self.stemmer.stem(word);
                #for the first we want to make sure not to add a space.
                #this is mainly for html encoded characters which are moderately important
                if first:
                    self.data = self.data + word;
                    first = False;
                else:
                    #else add a space
                    self.data = self.data + " " + word;
                if word != " " and word != "" and word != "\r\n":
                    self.full_text += " " + word;
                    
    ### returning the data ###
    def get_hyperlinks(self):
        #returns the hyperlinks
        return self.hyperlinks;
    def get_descriptions(self):
        #returns the meta description if it is there
        return self.descriptions;
    def get_meta(self):
        #return the meta information
        return self.meta;
    def get_no_follow_links(self):
        #get the links this page does not want the crawler to go to.
        return self.no_follow_links;
    def get_full_text(self):
        return self.full_text;
    def get_title(self):
        return self.title;
