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
from uummuuWord import add_to_index;
from styleParser import styleParser;
from myParser import myParser;
from HTMLObject import HTMLObject;
from StyledObject import StyledObject;
#from nltk import PorterStemmer;


def time_test(curr_time,  curr_time_counter):
    print curr_time_counter,"it took:", (time.clock() - curr_time), 'to get here';
    return time.clock(),  (curr_time_counter+1);


class Site():
    '''
        Site is a class that is defined to hold all the information 
        about a site including the words used on the site,
        the title, the meta data and the domain.
    '''
    def __init__(self, desc='', title='', url='', domain='', info=''):
        self.id = 0;
        self.description = desc;
        self.title = title;
        self.url = url;
        self.domain = domain;
        self.information = info;

'''
# add_priorities takes in a list of tags and determines how important the webmaster considers this tag
# based on how many ids or classes they use to describe the parent tags. If tags are given ids, they
# are assumed to be more important, followed by classes. The more nested tags, the more important this
# tag is considered to be.
'''
def add_priorities(tags):
    total = 0;
    for tag in tags:
        if(re.search(r'#[0-9|A-Z|a-z|_|\-]+$', tag)): #this element has an id in it
            if tag[0] != '#': #this is a tag with an id ( more descriptive)
                total += 5;
            else:
                total += 4; #this is only an id, not as descriptive
        elif(re.search(r'\.[0-9|A-Z|a-z|_|\-]+$', tag)): #this element has a class in it
            if tag[0] != '.': #this is a tag and a class (more descriptive)
                total += 3;
            else:
                total += 2; #this is just a class
        else:
            total += 1; #this is just a tag, give it a little boost for being nested
    return total;

'''
# get_comma_arr takes in a string and splits it up based on commas
# This function was made to order elements by importance including ids first, classes second and
# simple elements last.
# This function takes in a string and returns a sorted array.
# This function would be slow for large strings but large strings would not normally be used.
'''
def get_comma_arr(whole_tag):
    whole_tag = whole_tag.split(',');
    new_whole_tag = [];
    if(len(whole_tag)==1):
        return whole_tag;
    else:
        got_tag_id = False;
        got_tag_class = False;
        got_id = False;
        got_class = False;
        while len(whole_tag) > 0:
            for num_el,el in enumerate(whole_tag):
                if len(el) < 1:
                    pass;
                elif re.search('#', el) and el[0] != '#':
                    new_whole_tag.append(whole_tag.pop(num_el));
                elif el[0] == '#' and got_tag_id:
                    new_whole_tag.append(whole_tag.pop(num_el));
                elif re.search('\.', el) and el[0] != '.' and got_id:
                    new_whole_tag.append(whole_tag.pop(num_el));
                elif el[0] == '.' and got_tag_class:
                    new_whole_tag.append(whole_tag.pop(num_el));
                elif got_class:
                    new_whole_tag.append(whole_tag.pop(num_el));
            if not got_tag_id:
                got_tag_id = True;
            elif not got_id:
                got_id = True;
            elif not got_tag_class:
                got_tag_class = True;
            elif not got_class:
                got_class = True;
    return new_whole_tag;
        
def return_style(el, dictionary):
    if(not el):
        return False;
    try:
        return dictionary[el]['$style'];
    except:
        return False;
        
def return_comp_style(parts, comp_styles):
    curr_dict = comp_styles;
    styles = StyledObject();
    for part in parts:
        try:
            curr_dict = curr_dict[part];
            styles.add_Object(curr_dict['$style'],  90);
        except Exception, e:
            continue;
    return styles;
        
def main_style_parse(parser, write=True):
    
    curr_time = time.clock();
    curr_time_counter = 0;
    objs = {};
    
    for key in parser.styled_objects.keys():
        parts = key.lstrip().rstrip().split(' ');
        parts.reverse();
        style = StyledObject();
        #the number of elements in this whole line tag
        num_elements = len(parts);
        #add any composite styles
        style.add_Object(return_comp_style(parts, parser.styleParser.comp_styles), 100+num_elements);
        #start the current element to 0
        curr_el = 0;
        for part in parts:
            #split up this tag into its tag, id and class fields
            sections = re.match('([a-z A-Z 0-9 \- _]+)?(#[a-z A-Z 0-9 \- _]+)?(\.[a-z A-Z 0-9 \- _]+)?', part);
            groups = sections.groups();
            if groups[1] and groups[2]: #if there is a class assigned to an id
                style.add_Object(return_style(groups[1]+groups[2], parser.styleParser.id_class_styles), 90+num_elements-curr_el);
            if groups[0] and groups[1]: #if there is an id assigned to a tag, it is most specific
                style.add_Object(return_style(groups[0]+groups[1], parser.styleParser.id_specific_styles), 80+num_elements-curr_el);
            if groups[0] and groups[2]: #if there is a class assigned to a tag it is more specific
                style.add_Object(return_style(groups[0]+groups[2], parser.styleParser.class_specific_styles), 60+num_elements-curr_el);
            if groups[1]: #if there is an id it is specific
                style.add_Object(return_style(groups[1], parser.styleParser.id_styles), 40+num_elements-curr_el);
            if groups[2]: #if there is a class it is less specific
                style.add_Object(return_style(groups[2], parser.styleParser.class_styles), 20+num_elements-curr_el);
            if groups[0]: #if there is only a tag, it is least specific
                style.add_Object(return_style(groups[0], parser.styleParser.tag_styles), 10+num_elements-curr_el);
            curr_el += 1;
        try:
            objs[key].add_Object(style);
        except Exception, e:
            objs[key] = style;
        objs[key].text = parser.styled_objects[key];
        
    
    if write:
        ###    FUNCTIONALITY TO WRITE STYLES TO XML FILE    ###
        try:
            f = open("styles.DHB", "w");
        except Exception, e:
            print e;
            
        f.write('<styles>\n');
        for obj_key in objs.keys():
            f.write("\t<text_style>\n");
            f.write("\t\t<text>"+objs[obj_key].text + '</text>\n');
            f.write('\t\t<font-size>'+str(objs[obj_key].fontsize.value)+'</font-size>\n');
            f.write('\t\t<font-family>'+str(objs[obj_key].fontfam.value)+'</font-family>\n');
            f.write('\t\t<bgcolor>'+objs[obj_key].bgcolor.value+'</bgcolor>\n');
            f.write('\t\t<font-weight>' + objs[obj_key].fontweight.value+'</font-weight>\n');
            f.write('\t\t<font-color>' + objs[obj_key].font.value+'</font-color>\n');
            f.write('\t</text_style>\n');
        f.write('</styles>\n');
        f.close();
    fam_dict = {};
    size_dict = {};
    weight_dict = {};
    color_dict = {};
    bgcolor_dict = {};

    #keep track of the number of different styles used.
    diff_colors = 0;
    diff_sizes = 0;
    diff_bgcolors = 0;
    diff_weights = 0;
    diff_fams = 0;

    #test to see if I can get a percentage of a font size for comparing large and small fonts.
    #larger fonts should get a higher percentage of the view from smaller fonts.
    total_font_size = 0;
    #iterate over all the styles in the site.
    for obj_key in objs.keys():
        try:
            fam_dict[objs[obj_key].fontfam.value] += len(objs[obj_key].text.split(' '));
        except:
            fam_dict[objs[obj_key].fontfam.value] = len(objs[obj_key].text.split(' '));
            diff_fams += 1;
        try:
            size_dict[objs[obj_key].fontsize.value] += len(objs[obj_key].text.split(' '));
        except:
            size_dict[objs[obj_key].fontsize.value] = len(objs[obj_key].text.split(' '));
            diff_sizes += 1;
            try:
                total_font_size += objs[obj_key].fontsize.value;
            except:
                print 'the error was caused by value:',objs[obj_key].fontsize.value;
        try:
            weight_dict[objs[obj_key].fontweight.value] += len(objs[obj_key].text.split(' '));
        except:
            weight_dict[objs[obj_key].fontweight.value] = len(objs[obj_key].text.split(' '));
            diff_weights += 1;
        try:
            color_dict[objs[obj_key].font.value] += len(objs[obj_key].text.split(' '));
        except:
            color_dict[objs[obj_key].font.value] = len(objs[obj_key].text.split(' '));
            diff_colors += 1;
        try:
            bgcolor_dict[objs[obj_key].bgcolor.value] += len(objs[obj_key].text.split(' '));
        except:
            bgcolor_dict[objs[obj_key].bgcolor.value] = len(objs[obj_key].text.split(' '));
            diff_bgcolors += 1;

    total_word_weight = {};
    total_term_count = {};
    test_weight = 0;
    for obj_key in objs.keys():
        for term in objs[obj_key].text.split(' '):
            term = term.lower();
            total_weight = 0;
            total_weight += (.2/diff_bgcolors)/bgcolor_dict[objs[obj_key].bgcolor.value];
            total_weight += (.2/diff_colors)/color_dict[objs[obj_key].font.value];
            #the following line calculates the weight this font should receive based on the assumption
            #that bigger fonts will be viewed more. The bigger the font, the more of the percentage it
            #receives from this weight. This comes out to: size_percentage * different_sizes * .2
            total_weight += (.3/diff_sizes*(diff_sizes*(objs[obj_key].fontsize.value/total_font_size)))/size_dict[objs[obj_key].fontsize.value];
            total_weight += (.2/diff_weights)/weight_dict[objs[obj_key].fontweight.value];
            #took away .1 from family because that is the least significant style differentiation.
            total_weight += (.1/diff_fams)/fam_dict[objs[obj_key].fontfam.value];
            total_weight = round(total_weight,3);
            test_weight += total_weight;
            try:
                total_word_weight[term] += total_weight;
            except:
                total_word_weight[term] = total_weight;
            try:
                total_term_count[term] += 1;
            except:
                total_term_count[term] = 1;
    return total_word_weight, total_term_count;

##get the domain of a url sent to this function
def getDomain(string):
    """
    Usage: getDomain( URL );
    Returns: the domain of the string passed
    """
    temp_domain = '';
    if(string.startswith('http://')):
        string = string[7:];
    if(string.find('/') > -1):
        temp_domain = string[0:string.find('/')];
    else:
        temp_domain = string;
    subs = temp_domain.split('.');
    if(len(subs) ==1):
        return 'http://'+subs[0]+'/';
    else:
        return 'http://'+subs[-2]+'.'+subs[-1]+'/';



###FUNCTIONS BELOW HERE###
#makeURL is a function to turn a long url and a given uri into one url.
def makeURL(domain, uri):
    '''
    **combines a domain and a uri.
    **If uri is a url, it is returned**
    **If uri contains more "previous folder" marks than folders. It returns the root combined
    **with the first real folder from the uri.**
    '''
    
    page = domain;
    url = uri;

    if(page.rfind('/', 7) == -1):
        page = page + '/';

    if(url.startswith('http://')): ##if the value passed in as URI is a url, return it.
        return url;

    #make sure domain is a proper domain name
    while(len(url) > 0):
        if(url[0] == '/'): 
            ##a relative link...
            domain_start = page.find('/', 7); 
            #go to the root
            if(domain_start == -1):
                ##if you cannot find the root folder, the entire thing is the root
                domain_start = len(page); 
                ##set the domain to the whole thing
            while('../' in url): 
                ##check for folder up options
                if(url.startswith('/../')): 
                    ##if the person wants to go up from the root
                   url = url.replace('../', '', 1);
                   ##take this out, that's a pointless command
                else: 
                    ##the person has SOME sense
                   folder_pos = url.find('../'); 
                   ##find the first occurance of folder up.
                   folder_pos = url[0:folder_pos-1].rfind('/'); 
                   ##find the folder to go to.
                   url = url[0:folder_pos+1] + url[url.find('../')+3:];
                   ##delete the portion of the url that is risen from
            if(page[0] != '/' and url[0] != '/'):
                ##if the first character is not the root character.
                url = url.replace('./', ''); 
                ##replace any 'this folder options'
                url = url.replace('//', '/', 7);
                return page[0:domain_start] + '/' + url;
                ##return the domain and the url
            else:
                ##there is not a root directed link.
                url = url.replace('./', '');
                ##replace any this folder options.
                url = url.replace('//', '/', 7);
                return page[0:domain_start] + url; 
                ##go to root and return domain and url.
        elif(url.startswith('../')):
            ## folder up options for the domain url.
            folder_start = page.rfind('/', 7);
            ##find the ending folder
            folder_end = page.rfind('/', 7, folder_start);
            ##find the parent directory from that
            if(folder_end == -1 and folder_end == -1): 
                ##if the parent does not exists...
                url = url.replace('../', '', 1);
                ## get rid of the folder up option, you're at the root dummy.
            else:
                ##there is some parent directory.
                page = page[:folder_end+1];
                ##take it out.
                url = url.replace('../', '', 1);
                ##remove the folder up option since the folder is up.
        else:
            ##the uri starts with something else...
            curr_folder = page.rfind('/', 7);
            page = page[0:curr_folder+1];
            while('../' in url): 
                ##check for folder up options
                if(url.startswith('/../')): 
                    ##if the person wants to go up from the root
                   url = url.replace('../', '', 1);
                   ##take this out, that's a pointless command
                else: 
                    ##the person has SOME sense
                   folder_pos = url.find('../'); 
                   ##find the first occurance of folder up.
                   folder_pos = url[0:folder_pos-1].rfind('/'); 
                   ##find the folder to go to.
                   url = url[0:folder_pos+1] + url[url.find('../')+3:];
                   ##delete the portion of the url that is risen from
            page = page + url;
            url = '';
    page = page.replace('./', '');
    url = url.replace('//', '/', 7);
    return page;


##SITE MAP PARSER###
class SitemapParser(sgmllib.SGMLParser):
    def parse(self, s):
        self.feed(s);
        self.close();

    def __init__(self, verbose=0, myurl='', domain=''):
        sgmllib.SGMLParser.__init__(self, verbose);
        #are we inside a url?
        self.inside_url = False;
        #are we inside a loc?
        self.inside_loc = False;
        #are we inside a mod?
        self.inside_mod = False;
        #are we inside a frequency?
        self.inside_freq = False;
        #are we inside a priority?
        self.inside_priority = False;
        #the links from this site map
        self.links = [];
        #the sites on this sitemap
        self.site = dict();
        self.counter = 1;

    ##url is an object that has several attributes. It should have no hard data of its own.
    def start_url(self, attributes):
        self.inside_url = True;
        self.site = dict();
        self.site['id'] = self.counter;
        self.counter += 1;

    def end_url(self):
        self.links.append(self.site);
        self.inside_url = False;

    def start_loc(self, attributes):
        self.inside_loc = True;
        
    def end_loc(self):
        self.inside_loc = False;

    def start_lastmod(self, attributes):
        self.inside_mod = True;

    def end_lastmod(self):
        self.inside_mod = False;

    def start_changefreq(self, attributes):
        self.inside_freq = True;

    def end_changefreq(self):
        self.inside_freq = False;

    def start_priority(self, attributes):
        self.inside_priority = True;

    def end_priority(self):
        self.inside_priority = False;

    def handle_data(self, data):
        if(self.inside_url):
            if(self.inside_loc):
                self.site['loc'] = decode_htmlentities(data);
            elif(self.inside_mod):
                self.site['lastmod'] = data;
            elif(self.inside_freq):
                self.site['changefreq'] = data;
            elif(self.inside_priority):
                self.site['priority'] = data;


def checkSitemap(domain):
    '''
        checkSitemap takes in a domain, this can be any url with a uri appended.
        The function takes the current directory and checks for a sitemap.xml file.
        If this file is found an array of dictionaries is returned. This dictionary
        is defined with all the same attributes as a standard site map.

        @author: David Brear
        @date: July 14th 2008
        @version: 1.0
        @param: domain - string - the url to check for a sitemap.xml file
        @return: array of dictionary types.

        Usage: links = checkSitemap(**link**);
    '''
    httplib.HTTPConnection.debuglevel = 1;

    curr_folder = domain.rfind('/', 7);
    if(curr_folder != -1):
        url = domain[0:curr_folder];
        request = urllib2.Request(url + '/sitemap.xml');
    else:
        url = domain;
        request = urllib2.Request(url + '/sitemap.xml');

    opener = urllib2.build_opener();
    f = opener.open(request);

    ##create an instance of the sitemap parser class from above##
    parser = SitemapParser();
    parser.parse(f.read());

    return parser.links; #return an array of dictionaries from the sitemap

##The following code is dedicated to decoding sitemaps which are XML encoded###
def substitute_entity(match):
    ent = match.group(2);
    if(match.group(1) == '#'):
        return unichr(int(ent));
    else:
        cp = n2cp.get(ent);

        if(cp):
            return unichr(cp);
        else:
            return match.group();

def decode_htmlentities(string):
    #we set up a regular epression to take out html entities which are encoded.
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});");

    return entity_re.subn(substitute_entity, string)[0];

def find_RobotsTxt(url):
    """
    *   returns an array of all the urls that this web crawler is not allowed to visit.
        @param: url (string) the url to search for a robots.txt.
        @return: list of strings which can be used as regular expressions
    """
    link = getDomain(url)+'robots.txt';
    timeout = 1; #set the timeout before we don't care anymore

    socket.setdefaulttimeout(timeout); #set the timeout

    request = urllib2.Request(link);#append the headers to the request

    opener = urllib2.build_opener();#build the http opener

    dont_follow_links = [];
    try:
        f = opener.open(request);
        respect = False;
        for line in f.readlines():
            if line.find('#') > -1:
                line = line[0:line.find('#')];
            if(re.search('User-agent:',line)):
                if re.search('\*',line):
                    respect = True;
                elif re.search('UUMMUUBot',line):
                    respect = True;
                else:
                    respect = False;
            elif respect:
                if(re.search('disallow:',line.lower())):
                    stripped_link = line[line.find(':')+1:].lstrip().rstrip();
                    print 'dont follow link is:', stripped_link;
                    if(len(stripped_link) > 0):
                        dont_follow_links.append(makeURL(getDomain(url),stripped_link));
        f.close();
    except Exception, e:
        print 'find_RobotsTxt error:',e;
    return dont_follow_links;
    
'''
### This is a test method to see what is returned from an individual url.
### The parameter is the url to crawl.
'''
def test_one(url):
    myHTML = HTMLObject();
    myHTML.getHTML(url);
    parser = myParser(myurl = url, domain = getDomain(url));
    parser.parse(myHTML.page);
    styled_objs, no_style_objs = main_style_parse(parser.styled_objects, parser.full_style, True);
    
    for key in styled_objs.keys():
        print key + ' ==> ' + str(styled_objs[key]);
        
def insert_into_db(cursor, doc_id, word, weight, freq, in_title):
    word = word.replace("'", "");
    if len(word) == 0:
        return;
    cursor.execute("SELECT invert_list FROM sites_index WHERE word = '%s';" %word);
    results = cursor.fetchall();
    present = False;
    if(len(word) > 124):
        word = word[0:124];
    try:
        entry = results[0][0];
        present = True;
    except Exception, e:
        entry = "";
        present = False;
    entry = add_to_index(entry, doc_id, weight, freq, in_title);
    if not present:
        cursor.execute("INSERT into sites_index(word, invert_list, freq, length, num_docs) VALUES ('%s', '%s', %d, %d, 1);" %(word, entry, freq, len(word)));
    else:
        cursor.execute("UPDATE sites_index set invert_list = '%s', num_docs = num_docs + 1, freq = freq + %d where word = '%s';" %(entry, freq, word));
    try:
        cursor.execute("INSERT INTO sites_worddoc(word, doc_id, occurrence, weight, in_title) VALUES ('%s', %d, %d, %d, %d);" %(word, doc_id, freq, weight, in_title));
    except Exception, e:
        print "word was:", word, 'length is:', len(word);
        print 'I quit because:', e;
